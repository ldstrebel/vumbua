"""Generate s3-attribution-decisions.json for AI-summary secondary source."""

import json
import os
import re

def build_decisions():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    indexed_path = os.path.join(base_dir, "transcripts", "index", "s3-raw-indexed.md")
    out_path = os.path.join(base_dir, "transcripts", "index", "s3-attribution-decisions.json")

    with open(indexed_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    mic_lines = {}
    for line in raw_lines:
        m = re.match(r"^L(\d+):\s+\[(undiarized|ai-summary)\](?:\s+\[TURN\?\])?\s*(.*)$", line.strip())
        if not m:
            continue
        l_num = int(m.group(1))
        text = m.group(3).strip()

        # Simple character attribution based on text cues
        speaker = "GM"
        if any(w in text.lower() for w in ["loami", "luke f"]):
            speaker = "Loami"
        elif any(w in text.lower() for w in ["britt", "sophie"]):
            speaker = "Britt"
        elif any(w in text.lower() for w in ["iggy", "holly"]):
            speaker = "Iggy"
        elif any(w in text.lower() for w in ["ignatious", "john h"]):
            speaker = "Ignatius"
        elif any(w in text.lower() for w in ["aggie", "kristina"]):
            speaker = "Aggie"

        mic_lines[str(l_num)] = [{"identity": speaker}]

    decisions = {
        "session_id": "s3",
        "_note": "Attribution decisions for s3 secondary-source AI summary.",
        "ooc_ranges": [
            {"from": 1, "to": 12, "note": "Pre-session chit-chat: winter gear, New York trip, and meeting metadata."},
            {"from": 196, "to": len(mic_lines), "note": "Post-session table talk, rest mechanics, scheduling, and Granola notes."}
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
