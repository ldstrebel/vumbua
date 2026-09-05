"""Propagate speaker attribution across s2.5 lines and generate s2.5-attribution-decisions.json."""

import json
import os
import re

def build_decisions():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    indexed_path = os.path.join(base_dir, "data", "index", "s2.5-raw-indexed.md")
    guesses_path = os.path.join(base_dir, "data", "index", "s2.5-speaker-guesses.json")
    out_path = os.path.join(base_dir, "data", "index", "s2.5-attribution-decisions.json")

    with open(guesses_path, "r", encoding="utf-8") as f:
        guesses_data = json.load(f)
    line_guesses = guesses_data.get("lines", {})

    with open(indexed_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    current_speaker = "Luke S"
    mic_lines = {}

    for line in raw_lines:
        m = re.match(r"^L(\d+):\s+\[undiarized\](\s+\[TURN\?\])?\s*(.*)$", line)
        if not m:
            continue
        l_num = int(m.group(1))
        is_turn = bool(m.group(2))
        text = m.group(3).strip()

        # Check guess from guesses_data
        guess_entry = line_guesses.get(str(l_num))
        if guess_entry:
            current_speaker = guess_entry["guess"]
        elif is_turn:
            # Turn boundary with no explicit guess -> flip or infer from text
            if any(w in text.lower() for w in ["i think", "iggy", "my sheet", "i would", "can i"]):
                current_speaker = "Holly"
            elif any(w in text.lower() for w in ["you see", "roll", "what does", "the map", "the building"]):
                current_speaker = "Luke S"

        identity = "GM" if current_speaker == "Luke S" else "Iggy"
        mic_lines[str(l_num)] = [{"identity": identity}]

    # OOC ranges: pre-game chit-chat (1-187) and post-game chatter (1330-end)
    decisions = {
        "session_id": "s2.5",
        "_note": "Heuristic turn-propagated attribution for undiarized session s2.5 (Luke S as GM, Holly as Iggy).",
        "ooc_ranges": [
            {"from": 1, "to": 187, "note": "Pre-session chit-chat: gym, diets, and healthy drinks."},
            {"from": 1330, "to": len(raw_lines), "note": "Post-session chit-chat: flights, wedding plans, and bachelorette party."}
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

    print(f"Wrote decisions: {out_path} ({len(mic_lines)} lines decomposed)")

if __name__ == "__main__":
    build_decisions()
