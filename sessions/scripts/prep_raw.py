"""Step 0 — normalize a raw transcript into the canonical indexed artifact.

HARD PREREQUISITE: `sN-session-config.json` must exist and declare `gm`. The GM
identity and mic sharing are user-provided facts; this script refuses to run
without them rather than letting a later stage infer them (see session_config.py).

Speaker labels are normalized to canonical PERSON labels — never collapsed into
characters or into "GM". Diarization is per-mic, so the label on a line names a
stream, and only `attribute_speakers.py` (driven by the session config) turns a
stream into identities.
"""

import argparse
import hashlib
import json
import os
import re
import sys

import session_config as sc

SPEAKER_LINE = re.compile(r"^\*\*([^*]+):\*\*\s*(.*)$")


def load_aliases():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    aliases_path = os.path.join(script_dir, "speaker_aliases.json")
    if not os.path.exists(aliases_path):
        return {}, {}
    with open(aliases_path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    return data.get("person_labels", {}), data.get("character_labels", {})


def normalize_label(label, config, person_aliases, character_aliases):
    """Raw diarization label -> canonical person label (or canonical character).

    Spelling fixes come from `speaker_aliases.json` and the session config's
    `raw_speaker_labels`; the session config wins. Nothing here decides who the
    GM is or which character a person plays.
    """
    canonical = person_aliases.get(label, label)
    canonical = config.canonical_person(canonical)
    if canonical in config.person_labels:
        return canonical
    canonical = character_aliases.get(canonical, canonical)
    return canonical


def prep_raw(session_id, out_dir=None, config_path=None, sessions_dir=None):
    base_dir = sessions_dir or sc.default_sessions_dir()
    config = sc.gate(session_id, "prep_raw.py", sessions_dir=base_dir, config_path=config_path)
    print(sc.describe(config))

    raw_path = os.path.join(base_dir, "transcripts", "raw", f"{session_id}-raw.md")
    index_dir = out_dir or os.path.join(base_dir, "transcripts", "index")
    os.makedirs(index_dir, exist_ok=True)
    indexed_path = os.path.join(index_dir, f"{session_id}-raw-indexed.md")

    if not os.path.exists(raw_path):
        print(f"Error: Raw transcript file not found at {raw_path}", file=sys.stderr)
        sys.exit(1)

    person_aliases, character_aliases = load_aliases()
    processed_lines = []
    stream_counts = {}

    with open(raw_path, "r", encoding="utf-8") as handle:
        for line in handle:
            # 1. Normalize line endings & strip trailing whitespace
            line = line.replace("\r\n", "\n").replace("\r", "\n").rstrip()

            # 2. Skip empty lines
            if not line:
                continue

            # 3. Normalize the speaker label only — never the dialogue content
            match = SPEAKER_LINE.match(line)
            if match:
                label = match.group(1).strip()
                dialogue = match.group(2)
                canonical = normalize_label(label, config, person_aliases, character_aliases)
                stream_counts[canonical] = stream_counts.get(canonical, 0) + 1
                line = f"**{canonical}:** {dialogue}"

            processed_lines.append(line)

    # 4. Prefix with immutable line numbers (L0001: )
    final_lines = [f"L{idx:04d}: {line}\n" for idx, line in enumerate(processed_lines, 1)]

    with open(indexed_path, "w", encoding="utf-8") as handle:
        handle.writelines(final_lines)

    # 5. Compute SHA-256 of the INDEXED file
    sha256 = hashlib.sha256()
    with open(indexed_path, "rb") as handle:
        while chunk := handle.read(8192):
            sha256.update(chunk)
    file_hash = sha256.hexdigest()

    print(f"Indexed file created: {indexed_path}")
    print(f"SHA-256: {file_hash}")
    print("Streams found:")
    for stream, count in sorted(stream_counts.items(), key=lambda item: -item[1]):
        if config.is_shared_mic(stream):
            carried = ", ".join(config.shared_mic(stream).identity_labels())
            note = f"shared mic — declared to carry: {carried}"
        elif config.solo_identity(stream):
            note = f"identity: {config.solo_identity(stream).identity}"
        else:
            note = "⚠ undeclared label — add it to `raw_speaker_labels` in the session config"
        print(f"  {count:>5}  {stream}  ({note})")
    return file_hash


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session_id", help="e.g. s12")
    parser.add_argument("--config", dest="config_path", help="explicit session config path")
    parser.add_argument(
        "--out-dir",
        dest="out_dir",
        help="where to write sN-raw-indexed.md (default sessions/transcripts/index)",
    )
    args = parser.parse_args(argv)
    prep_raw(args.session_id, out_dir=args.out_dir, config_path=args.config_path)


if __name__ == "__main__":
    main()
