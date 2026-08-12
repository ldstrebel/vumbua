"""Attribution stage — turn diarized streams into declared identities.

Every routing decision here comes from the session config:

* a stream that is NOT listed in `shared_mics` carries exactly one identity, the
  one the config declares (`gm` or `players[person]`);
* a stream that IS listed in `shared_mics` is decomposed into the identities the
  config declares for it — and only those. The per-line decomposition itself is
  semantic work (an LLM/human pass over the raw lines) recorded in
  `sN-attribution-decisions.json`; this script validates it against the config
  and refuses identities the config never declared.

If a session declares no shared mics, no decomposition is attempted at all — the
pipeline neither guesses that a stream is shared nor guesses that it isn't.

Usage:
    python attribute_speakers.py s12 \
        --index-dir sessions/s12-devin/artifacts \
        --out-dir sessions/s12-devin/artifacts [--strict]
"""

import argparse
import json
import os
import re
import sys

import session_config as sc

INDEXED_LINE = re.compile(r"^L(\d+): (.*)$")
SPEAKER_LINE = re.compile(r"^\*\*([^*]+):\*\*\s*(.*)$")
NPC_IDENTITY = re.compile(r"^NPC:(.+)$")

DECISIONS_SEARCH_DIRS = ("{session_id}-devin", "config", os.path.join("transcripts", "index"))


class AttributionError(Exception):
    pass


def find_decisions_path(session_id, sessions_dir):
    filename = f"{session_id}-attribution-decisions.json"
    for template in DECISIONS_SEARCH_DIRS:
        path = os.path.join(sessions_dir, template.format(session_id=session_id), filename)
        if os.path.exists(path):
            return path
    return None


def load_decisions(session_id, sessions_dir, decisions_path=None):
    path = decisions_path or find_decisions_path(session_id, sessions_dir)
    if not path:
        return {}, None
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if data.get("session_id") != session_id:
        raise AttributionError(
            f"{path} declares session_id {data.get('session_id')!r}, expected {session_id!r}."
        )
    return data.get("mics", {}), path


def read_indexed(indexed_path):
    """Yield (line_number, stream_label, body) for every labeled line."""
    with open(indexed_path, "r", encoding="utf-8") as handle:
        for raw in handle:
            match = INDEXED_LINE.match(raw.rstrip("\n"))
            if not match:
                continue
            line_no = int(match.group(1))
            speaker = SPEAKER_LINE.match(match.group(2))
            if not speaker:
                continue
            yield line_no, speaker.group(1).strip(), speaker.group(2)


def resolve_identity(config, mic, identity_label):
    """Map a decision's identity label onto a config-declared identity."""
    npc = NPC_IDENTITY.match(identity_label)
    if npc:
        name = npc.group(1).strip()
        gm_slots = [i for i in mic.identities if i.is_gm]
        if not gm_slots:
            raise AttributionError(
                f"mic {mic.mic_label!r} does not carry the GM, so it cannot voice "
                f"NPC {npc.group(1)!r}."
            )
        if name in config.characters or name == sc.GM_IDENTITY or name == config.gm:
            raise AttributionError(
                f"{name!r} is a player character declared in the session config, so it "
                f"cannot be attributed as an NPC. Use the identity {name!r} directly if "
                f"mic {mic.mic_label!r} declares it."
            )
        return {
            "identity": npc.group(1).strip(),
            "kind": "npc",
            "person": gm_slots[0].person,
            "character": None,
            "voiced_by": sc.GM_IDENTITY,
        }
    declared = config.identity(mic.mic_label, identity_label)
    if not declared:
        raise AttributionError(
            f"identity {identity_label!r} is not declared for mic {mic.mic_label!r} "
            f"(declared: {mic.identity_labels()}). Update the session config if the "
            "mic really carries it — never widen attribution by inference."
        )
    return {
        "identity": declared.identity,
        "kind": declared.kind,
        "person": declared.person,
        "character": declared.character,
        "voiced_by": None,
    }


def attribute(session_id, index_dir=None, out_dir=None, config_path=None,
              decisions_path=None, sessions_dir=None, strict=False):
    base_dir = sessions_dir or sc.default_sessions_dir()
    config = sc.gate(session_id, "attribute_speakers.py", sessions_dir=base_dir,
                     config_path=config_path)
    print(sc.describe(config))

    index_dir = index_dir or os.path.join(base_dir, "transcripts", "index")
    indexed_path = os.path.join(index_dir, f"{session_id}-raw-indexed.md")
    if not os.path.exists(indexed_path):
        print(f"Error: indexed transcript not found at {indexed_path}. Run prep_raw.py first.",
              file=sys.stderr)
        sys.exit(1)

    decisions, used_decisions_path = load_decisions(session_id, base_dir, decisions_path)
    for mic_label in decisions:
        if not config.is_shared_mic(mic_label):
            raise AttributionError(
                f"decisions file declares decomposition for {mic_label!r}, which the "
                "session config does not list as a shared mic."
            )

    violations = []
    segments = []
    unresolved = []
    stream_counts = {}

    for line_no, stream, body in read_indexed(indexed_path):
        stream_counts[stream] = stream_counts.get(stream, 0) + 1
        mic = config.shared_mic(stream)

        if not mic:
            solo = config.solo_identity(stream)
            if not solo:
                violations.append(
                    f"L{line_no:04d}: stream {stream!r} is not declared in the session "
                    "config (add it to `raw_speaker_labels`/`players`)."
                )
                continue
            segments.append({
                "line": line_no,
                "stream": stream,
                "shared_mic": False,
                "person": solo.person,
                "identity": solo.identity,
                "kind": solo.kind,
                "character": solo.character,
                "source": "config",
            })
            continue

        line_decisions = decisions.get(stream, {}).get("lines", {}).get(str(line_no))
        if not line_decisions:
            unresolved.append(line_no)
            segments.append({
                "line": line_no,
                "stream": stream,
                "shared_mic": True,
                "identity": None,
                "kind": "needs_decomposition",
                "candidate_identities": mic.identity_labels(),
                "source": "pending",
            })
            continue

        for slot, decision in enumerate(line_decisions):
            identity_label = decision.get("identity")
            text = decision.get("segment", "")
            if not identity_label:
                violations.append(f"L{line_no:04d}[{slot}]: decision is missing `identity`.")
                continue
            try:
                resolved = resolve_identity(config, mic, identity_label)
            except AttributionError as exc:
                violations.append(f"L{line_no:04d}[{slot}]: {exc}")
                continue
            if text and text not in body:
                violations.append(
                    f"L{line_no:04d}[{slot}]: segment text is not a verbatim substring "
                    f"of the raw line ({text[:40]!r}…)."
                )
                continue
            segments.append({
                "line": line_no,
                "stream": stream,
                "shared_mic": True,
                "person": resolved["person"],
                "identity": resolved["identity"],
                "kind": resolved["kind"],
                "character": resolved["character"],
                "voiced_by": resolved["voiced_by"],
                "text": text,
                "source": "decision",
                "note": decision.get("note", ""),
            })

    identity_counts = {}
    for segment in segments:
        key = f"{segment['stream']} -> {segment['identity'] or '(pending)'}"
        identity_counts[key] = identity_counts.get(key, 0) + 1

    report = {
        "session_id": session_id,
        "session_config": os.path.relpath(config.path, base_dir),
        "decisions_file": os.path.relpath(used_decisions_path, base_dir) if used_decisions_path else None,
        "indexed_file": os.path.relpath(indexed_path, base_dir),
        "gm": config.gm,
        "shared_mics": [
            {"mic_label": mic.mic_label, "carries": mic.identity_labels(), "note": mic.note}
            for mic in config.shared_mics
        ],
        "stream_counts": stream_counts,
        "identity_counts": identity_counts,
        "unresolved_shared_mic_lines": unresolved,
        "violations": violations,
        "segments": segments,
    }

    out_dir = out_dir or index_dir
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{session_id}-attribution.json")
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    print(f"Attribution written: {out_path}")
    for key, count in sorted(identity_counts.items(), key=lambda item: -item[1]):
        print(f"  {count:>5}  {key}")
    if unresolved:
        print(f"  {len(unresolved)} shared-mic line(s) still need decomposition "
              f"(first: L{unresolved[0]:04d})")
    if violations:
        print(f"❌ {len(violations)} violation(s):", file=sys.stderr)
        for violation in violations:
            print(f"    - {violation}", file=sys.stderr)
        sys.exit(1)
    if strict and unresolved:
        print("❌ --strict: every shared-mic line must be decomposed.", file=sys.stderr)
        sys.exit(1)
    print("✅ attribution consistent with the session config")
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session_id", help="e.g. s12")
    parser.add_argument("--config", dest="config_path")
    parser.add_argument("--decisions", dest="decisions_path")
    parser.add_argument("--index-dir", dest="index_dir")
    parser.add_argument("--out-dir", dest="out_dir")
    parser.add_argument("--strict", action="store_true",
                        help="fail if any shared-mic line lacks a decomposition")
    args = parser.parse_args(argv)
    try:
        attribute(args.session_id, index_dir=args.index_dir, out_dir=args.out_dir,
                  config_path=args.config_path, decisions_path=args.decisions_path,
                  strict=args.strict)
    except AttributionError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
