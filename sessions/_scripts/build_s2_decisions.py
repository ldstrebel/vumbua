"""Build sessions/data/index/s2-attribution-decisions.json deterministically."""

import json
import os
import re

def build_decisions():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    indexed_path = os.path.join(base_dir, "data", "index", "s2-raw-indexed.md")
    out_path = os.path.join(base_dir, "data", "index", "s2-attribution-decisions.json")

    with open(indexed_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    luke_s_lines = {}
    for line in raw_lines:
        m = re.match(r"^L(\d+):\s+\*\*Luke S:\*\*\s*(.*)$", line)
        if m:
            luke_s_lines[int(m.group(1))] = m.group(2).strip()

    # Lines specifically voiced by Kristina / Aggie
    aggie_lines = {
        51, 54, 56, 62, 70, 72, 74,
        691, 706, 710, 798, 802, 824, 834, 844, 849, 945, 964, 974, 1136
    }

    mic_lines = {}
    for l_num in sorted(luke_s_lines.keys()):
        if l_num in aggie_lines:
            mic_lines[str(l_num)] = [{"identity": "Aggie"}]
        else:
            mic_lines[str(l_num)] = [{"identity": "GM"}]

    decisions = {
        "session_id": "s2",
        "_note": "Session 2 attribution decisions for shared mic Luke S (carrying GM and Kristina/Aggie).",
        "ooc_ranges": [
            {
                "from": 1,
                "to": 305,
                "note": "Pre-game setup, Daggerheart rules discussion, character sheet checking, and radio recap."
            },
            {
                "from": 1185,
                "to": 1221,
                "note": "Post-session wrap-up, Loom structure mechanics preview, and sign-off."
            }
        ],
        "ooc_lines": {},
        "mics": {
            "Luke S": {
                "lines": mic_lines
            }
        }
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(decisions, f, indent=2)

    print(f"Wrote decisions: {out_path} ({len(mic_lines)} lines on Luke S mic decomposed)")

if __name__ == "__main__":
    build_decisions()
