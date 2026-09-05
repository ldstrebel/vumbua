#!/usr/bin/env python3
"""Render a clean transcript from a config-gated attribution run.

Every line of speech comes from `sN-attribution.json`, so a speaker label here is
only ever an identity the session config declared (or an NPC the GM voiced). Nothing
is inferred from sentence content, and no line of the indexed transcript is dropped:
text inside a shared-mic line that no decision claims is emitted separately and marked
as an unsegmented remainder rather than being folded into a neighbouring speaker's quote.
A remainder is only ever credited to the mic's GM slot — the narration and NPC voices the
GM owns by declaration — and stays unattributed on a mic that does not carry the GM.

Diarization cuts a speaker's sentence in half whenever somebody else makes a noise, so the
line-per-line view reads as confetti (`Iggy: "that's"` / `GM: "Super"` / `Iggy: "annoying."`).
The render therefore stitches each speaker's fragments back into sentence-level turns, in
place: a fragment continues that speaker's previous turn when the turn was left
unterminated (or this fragment opens lower-case), the interruption was short, and the two
fragments are close in the index. Text is only ever concatenated in transcript order and a
turn is emitted where its first fragment fell, so nothing is reordered, reworded or lost.
`--no-stitch` returns the raw line-per-line view.

`--inserts` additionally splices in out-of-audio canon (a storyboard the GM handed to the
table mid-session) at the line its spec anchors it to. Inserted entries are labelled as
storyboard material, claim no microphone, and never replace or absorb recorded text, so the
render stays a superset of the indexed transcript.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import session_config as sc
import storyboard_inserts

LINE_RE = re.compile(r"^L(\d+): \*\*(.+?):\*\* (.*)$")
TERMINAL_RE = re.compile(r"[.!?…][\"')\]]*$")
MAX_INTERRUPTING_LINES = 4
MAX_LINE_GAP = 8


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
        # Out of character the person is speaking, not the character they play.
        return f"[[{segment.get('person') or segment['stream']}]] (out of character)"
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


def stitch(rows):
    """Rejoin each speaker's interrupted fragments into sentence-level turns, in place.

    `rows` is (line_number, speaker, text) in transcript order, where a line number of
    None marks a storyboard insert, which never stitches so every panel stays citable.
    Returns [first_line, speaker, [texts], last_line] in first-fragment order.
    """
    turns = []
    open_turns = {}  # speaker -> (index into turns, row position, line number)
    for position, (line_no, speaker, text) in enumerate(rows):
        slot = open_turns.get(speaker)
        joinable = False
        if slot and line_no is not None:
            index, last_position, last_line = slot
            interrupting = position - last_position - 1
            if interrupting == 0:
                joinable = True  # same speaker, adjacent rows: always one turn
            elif (interrupting <= MAX_INTERRUPTING_LINES
                  and line_no - last_line <= MAX_LINE_GAP):
                previous = turns[index][2][-1].rstrip()
                joinable = not TERMINAL_RE.search(previous) or text[:1].islower()
        if joinable:
            index = slot[0]
            turns[index][2].append(text)
            turns[index][3] = line_no
        else:
            index = len(turns)
            turns.append([line_no, speaker, [text], line_no])
        if line_no is not None:
            open_turns[speaker] = (index, position, line_no)
    return turns


def render(session_id, sessions_dir=None, index_dir=None, attribution_path=None,
           out_path=None, inserts_path=None, stitch_turns=True):
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

    inserts_spec, inserts_anchor, inserts = None, None, []
    if inserts_path:
        try:
            inserts_spec, inserts_anchor, inserts = storyboard_inserts.load(
                inserts_path, config, base_dir)
        except storyboard_inserts.InsertError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
        if inserts_anchor not in bodies:
            print(f"Error: inserts anchor L{inserts_anchor:04d} is not a line of "
                  f"{session_id}-raw-indexed.md", file=sys.stderr)
            sys.exit(1)

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
                if all(s.get("ooc") for s in segments):
                    speaker = (f"[[{segments[0].get('person') or segments[0]['stream']}]] "
                               "(out of character, unsegmented remainder)")
                elif owns_gm:
                    speaker = "[[GM]] (narration, unsegmented remainder)"
                else:
                    speaker = "[[unattributed remainder]]"
                rows.append((line_no, speaker, rest))
        if line_no == inserts_anchor:
            for entry in inserts:
                rows.append((None, storyboard_inserts.entry_label(entry), entry["text"]))

    merged = stitch(rows) if stitch_turns else [
        [line_no, speaker, [text], line_no] for line_no, speaker, text in rows]

    counts = {}
    for _, speaker, _, _ in merged:
        # Fold each storyboard page/panel reference into one bucket for the summary.
        speaker = re.sub(r"storyboard p[\d.]+", "storyboard", speaker)
        counts[speaker] = counts.get(speaker, 0) + 1

    out_path = out_path or os.path.join(base_dir, "transcripts", "clean",
                                        f"{session_id}-clean-attributed.md")

    def _safe_relpath(p):
        if not p:
            return None
        try:
            return os.path.relpath(p, base_dir)
        except ValueError:
            return os.path.abspath(p)

    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(f"# Session {session_id.upper()} — Clean Transcript (Attributed)\n\n")
        handle.write(f"**Session config:** `{_safe_relpath(config.path)}`  \n")
        handle.write(f"**GM:** {config.gm}  \n")
        for mic in config.shared_mics:
            handle.write(f"**Shared mic `{mic.mic_label}` carries:** "
                         f"{', '.join(mic.identity_labels())}  \n")
        handle.write(f"**Source attribution:** `{attribution['indexed_file']}` via "
                     f"`{attribution['decisions_file']}`  \n")
        if inserts_spec:
            handle.write(f"**Storyboard inserts:** `{inserts_spec['storyboard']}` spliced "
                         f"after L{inserts_anchor:04d} via "
                         f"`{_safe_relpath(inserts_path)}`  \n")
            handle.write(f"**Insert provenance:** {inserts_spec['delivery']}  \n")
        handle.write(f"**Turn stitching:** {'on' if stitch_turns else 'off'} — fragments a "
                     f"speaker was interrupted mid-sentence are rejoined, and the anchor "
                     f"shows the line span they came from  \n")
        handle.write("\nEvery speaker label below is a config-declared identity or a "
                     "GM-voiced NPC. Line anchors are the immutable `L####` indices; "
                     "`storyboard pN.M` marks material that was never spoken on a "
                     "microphone.\n\n---\n\n")
        for start, speaker, texts, end in merged:
            if start is None:
                anchor = "vision"
            elif start == end:
                anchor = f"L{start:04d}"
            else:
                anchor = f"L{start:04d}–L{end:04d}"
            handle.write(f"**{speaker}** [{anchor}]: {' '.join(texts).strip()}\n\n")

    print(f"Clean transcript written: {_safe_relpath(out_path)}")
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
    parser.add_argument("--inserts",
                        help="sN-vision-inserts.json: out-of-audio storyboard canon")
    parser.add_argument("--no-stitch", action="store_true",
                        help="emit one entry per diarized line instead of stitched turns")
    args = parser.parse_args()
    render(args.session_id, sessions_dir=args.sessions_dir, index_dir=args.index_dir,
           attribution_path=args.attribution, out_path=args.out,
           inserts_path=args.inserts, stitch_turns=not args.no_stitch)


if __name__ == "__main__":
    main()
