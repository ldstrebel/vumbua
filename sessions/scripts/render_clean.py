#!/usr/bin/env python3
"""Render a clean transcript from a config-gated attribution run.

Every line of speech comes from `sN-attribution.json`, so a speaker label here is
only ever an identity the session config declared (or an NPC the GM voiced). Nothing
is inferred from sentence content, and no line of the indexed transcript is dropped:
text inside a shared-mic line that no decision claims is emitted separately and marked
as an unsegmented remainder rather than being folded into a neighbouring speaker's quote.
A remainder is only ever credited to the mic's GM slot — the narration and NPC voices the
GM owns by declaration — and stays unattributed on a mic that does not carry the GM.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import session_config as sc

LINE_RE = re.compile(r"^L(\d+): \*\*(.+?):\*\* (.*)$")


def read_indexed(path):
    bodies = {}
    for raw in open(path, encoding="utf-8"):
        match = LINE_RE.match(raw.rstrip("\n"))
        if match:
            bodies[int(match.group(1))] = match.group(3)
    return bodies


def label(segment):
    identity = segment["identity"]
    kind = segment["kind"]
    if segment.get("ooc"):
        return f"[[{identity}]] (table talk)"
    if kind == "npc":
        return f"[[{identity}]] (NPC, voiced by GM)"
    if kind == "gm":
        return "[[GM]] (narration)"
    return f"[[{identity}]] (PC, {segment['person']} on {segment['stream']}'s mic)"


def remainder(body, texts):
    """Whatever the decisions did not claim, in order, so nothing is silently lost."""
    spans = []
    for text in texts:
        start = body.find(text)
        if start >= 0:
            spans.append((start, start + len(text)))
    spans.sort()
    out = []
    cursor = 0
    for start, end in spans:
        if start > cursor:
            out.append(body[cursor:start])
        cursor = max(cursor, end)
    if cursor < len(body):
        out.append(body[cursor:])
    return " ".join(part.strip() for part in out if part.strip())


def render(session_id, sessions_dir=None, index_dir=None, attribution_path=None, out_path=None):
    base_dir = sessions_dir or sc.default_sessions_dir()
    config = sc.gate(session_id, "render_clean.py", sessions_dir=base_dir)

    index_dir = index_dir or os.path.join(base_dir, "transcripts", "index")
    bodies = read_indexed(os.path.join(index_dir, f"{session_id}-raw-indexed.md"))
    attribution = json.load(open(
        attribution_path or os.path.join(index_dir, f"{session_id}-attribution.json"),
        encoding="utf-8"))

    if attribution.get("unresolved_shared_mic_lines"):
        print("Error: attribution still has needs_decomposition lines; render would be "
              "incomplete. Resolve them in the decisions file first.", file=sys.stderr)
        sys.exit(1)

    by_line = {}
    for segment in attribution["segments"]:
        by_line.setdefault(segment["line"], []).append(segment)

    rows = []
    for line_no in sorted(by_line):
        segments = by_line[line_no]
        body = bodies.get(line_no, "")
        texts = [s.get("text") for s in segments if s.get("text")]
        for segment in segments:
            rows.append((line_no, label(segment), segment.get("text") or body))
        if texts:
            rest = remainder(body, texts)
            if rest:
                mic = config.shared_mic(segments[0]["stream"])
                owns_gm = mic and any(identity.is_gm for identity in mic.identities)
                speaker = ("[[GM]] (narration, unsegmented remainder)" if owns_gm
                           else "[[unattributed remainder]]")
                rows.append((line_no, speaker, rest))

    # Collapse consecutive rows with the same speaker into one entry.
    merged = []
    for line_no, speaker, text in rows:
        if merged and merged[-1][1] == speaker:
            merged[-1][2].append(text)
            merged[-1][3] = line_no
        else:
            merged.append([line_no, speaker, [text], line_no])

    counts = {}
    for _, speaker, _, _ in merged:
        counts[speaker] = counts.get(speaker, 0) + 1

    out_path = out_path or os.path.join(base_dir, "transcripts", "clean",
                                        f"{session_id}-clean-attributed.md")
    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(f"# {session_id.upper()} Clean Transcript (attribution-derived)\n\n")
        handle.write(f"**GM:** {config.gm}  \n")
        for mic in config.shared_mics:
            handle.write(f"**Shared mic `{mic.mic_label}`:** carries "
                         f"{', '.join(mic.identity_labels())}  \n")
        handle.write(f"**Source attribution:** `{attribution['indexed_file']}` via "
                     f"`{attribution['decisions_file']}`  \n")
        handle.write("\nEvery speaker label below is a config-declared identity or a "
                     "GM-voiced NPC. Line anchors are the immutable `L####` indices.\n\n---\n\n")
        for start, speaker, texts, end in merged:
            anchor = f"L{start:04d}" if start == end else f"L{start:04d}–L{end:04d}"
            handle.write(f"**{speaker}** [{anchor}]: {' '.join(texts).strip()}\n\n")

    print(f"Clean transcript written: {os.path.relpath(out_path, base_dir)}")
    print(f"  entries: {len(merged)}")
    for speaker, count in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {count:5d}  {speaker}")
    return out_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session_id")
    parser.add_argument("--sessions-dir")
    parser.add_argument("--index-dir")
    parser.add_argument("--attribution")
    parser.add_argument("--out")
    args = parser.parse_args()
    render(args.session_id, sessions_dir=args.sessions_dir, index_dir=args.index_dir,
           attribution_path=args.attribution, out_path=args.out)


if __name__ == "__main__":
    main()
