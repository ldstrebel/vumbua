"""Builds s4.5-attribution-decisions.json by classifying Luke S mic lines."""

import json
import re

def main():
    lines = open("sessions/transcripts/index/s4.5-raw-indexed.md", encoding="utf-8").readlines()
    
    # 1. Identify OOC ranges
    # 1 to 122: Pre-game chatter
    # 621 to 649: Post-game wrapup
    ooc_ranges = [
        {"from": 1, "to": 122, "note": "Pre-session chit-chat: migraines, margaritas with neighbors, radio broadcast, and codex review."},
        {"from": 621, "to": 649, "note": "Post-session table talk: next session scheduling, Tuesday availability, and session recap."}
    ]
    
    # 2. Extract all lines on Luke S stream
    luke_lines = {}
    for l in lines:
        m = re.match(r"^L(\d+):\s+\*\*Luke S:\*\*\s*(.*)$", l.strip())
        if m:
            l_num = int(m.group(1))
            luke_lines[l_num] = m.group(2).strip()
            
    # Distinct lines where Kristina / Aggie is speaking
    # Known Aggie indicators: Kristina speaking directly to Sophie/Britt, first person Aggie,
    # or responding as Aggie to Britt's questions.
    aggie_lines = set()
    
    # Check lines in in-game range 123 to 620
    for l_num, text in luke_lines.items():
        if l_num < 123 or l_num > 620:
            continue
        lower = text.lower()
        # Explicit Aggie actions/speech by Kristina
        if l_num in [136, 138, 219, 221, 223, 323, 419, 421, 605]:
            aggie_lines.add(l_num)
        elif lower.startswith("i'll like") or lower.startswith("then i'll") or lower.startswith("brace yourself"):
            aggie_lines.add(l_num)
        elif "karma came quickly" in lower or "like i just want to like sit down" in lower:
            aggie_lines.add(l_num)
            
    # Build decisions structure
    decisions = {
        "session_id": "s4.5",
        "_note": "Attribution decisions for s4.5 shared mic Luke S (carries GM and Aggie).",
        "ooc_ranges": ooc_ranges,
        "ooc_lines": {},
        "mics": {
            "Luke S": {
                "lines": {}
            }
        }
    }
    
    for l_num in sorted(luke_lines.keys()):
        identity = "Aggie" if l_num in aggie_lines else "GM"
        decisions["mics"]["Luke S"]["lines"][str(l_num)] = [{"identity": identity}]
        
    with open("sessions/transcripts/index/s4.5-attribution-decisions.json", "w", encoding="utf-8") as f:
        json.dump(decisions, f, indent=2)
        
    print(f"Wrote s4.5-attribution-decisions.json with {len(luke_lines)} mic lines ({len(aggie_lines)} Aggie, {len(luke_lines)-len(aggie_lines)} GM).")

if __name__ == "__main__":
    main()
