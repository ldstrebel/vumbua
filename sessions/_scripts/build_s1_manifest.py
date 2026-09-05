"""Generates sessions/data/index/s1-manifest.json and validates it."""

import json
import os
import re
import hashlib

def get_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def build_manifest():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    indexed_path = os.path.join(base_dir, "data", "index", "s1-raw-indexed.md")
    manifest_path = os.path.join(base_dir, "data", "index", "s1-manifest.json")

    with open(indexed_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    total_lines = len(raw_lines)
    file_hash = get_sha256(indexed_path)

    # 14 Contiguous Blocks tiling 1 to 1389
    scene_defs = [
        {"id": 1, "title": "OOC Backstory Alignment & Clan Lore", "range": [1, 136], "ooc": True},
        {"id": 2, "title": "Intake World Primer & Rules Overview", "range": [137, 240], "ooc": True},
        {"id": 3, "title": "Daggerheart Rules & Subclass Customization", "range": [241, 315], "ooc": True},
        {"id": 4, "title": "The Intake Exam & Typewriter Crash", "range": [316, 376], "ooc": False},
        {"id": 5, "title": "The Costco Checkpoint & The Working Man", "range": [377, 415], "ooc": False},
        {"id": 6, "title": "Iggy's Chaos at the Testing Machine", "range": [416, 480], "ooc": False},
        {"id": 7, "title": "Campus Emergence & Harbor Scaffolding", "range": [481, 605], "ooc": False},
        {"id": 8, "title": "Lomi & Sarge: Working Class Reunion", "range": [606, 750], "ooc": False},
        {"id": 9, "title": "Ignatius & Valentine Sterling", "range": [751, 890], "ooc": False},
        {"id": 10, "title": "Dorm Assignments: Blocks 04, 12, 99", "range": [891, 970], "ooc": False},
        {"id": 11, "title": "The Crane Ascent: Iggy Maps the Campus", "range": [971, 1080], "ooc": False},
        {"id": 12, "title": "Serra Vox's Approach & The Bonfire Invite", "range": [1081, 1180], "ooc": False},
        {"id": 13, "title": "The Bonfire Gathering at Block 99", "range": [1181, 1285], "ooc": False},
        {"id": 14, "title": "First Night Closing Reflections", "range": [1286, 1389], "ooc": False},
    ]

    scene_blocks = []

    for sdef in scene_defs:
        sid = sdef["id"]
        title = sdef["title"]
        start, end = sdef["range"]
        is_ooc = sdef["ooc"]

        speakers_present = set()
        ledger = []

        if not is_ooc:
            for l_idx in range(start - 1, end):
                line = raw_lines[l_idx].strip()
                m = re.match(r"^L(\d+):\s+\*\*([^*]+):\*\*\s*(.*)$", line)
                if m:
                    l_num = int(m.group(1))
                    speaker_stream = m.group(2).strip()
                    text = m.group(3).strip()

                    # Map stream to identity
                    # Stream mappings for s1:
                    # 'Luke S' -> 'GM' or 'Aggie'
                    # 'Luke F' -> 'Lomi' or 'Britt'
                    # 'John' -> 'Ignatius'
                    # 'Holly' -> 'Iggy'
                    speaker = speaker_stream
                    if speaker_stream == "John":
                        speaker = "Ignatius"
                    elif speaker_stream == "Holly":
                        speaker = "Iggy"
                    elif speaker_stream == "Luke S":
                        # In S1, Kristina speaks Aggie, Luke S speaks GM
                        # Distinguish by dialogue cues or default to GM
                        if "I " in text and any(w in text.lower() for w in ["sketch", "draw", "stomp", "look"]):
                            speaker = "Aggie"
                        else:
                            speaker = "GM"
                    elif speaker_stream == "Luke F":
                        # Luke F speaks Lomi and Sophie speaks Britt
                        if any(w in text.lower() for w in ["brit", "aggie", "bluetooth", "ticket", "stall"]):
                            speaker = "Britt"
                        else:
                            speaker = "Lomi"

                    speakers_present.add(speaker)
                    # Gist truncation: clean text
                    gist = text.replace('"', "'")
                    if len(gist) > 60:
                        gist = gist[:57] + "..."

                    ledger.append({
                        "line": l_num,
                        "speaker": speaker,
                        "gist": gist
                    })

        scene_blocks.append({
            "scene_id": sid,
            "title": title,
            "line_range": [start, end],
            "ooc": is_ooc,
            "speakers_present": sorted(list(speakers_present)),
            "dialogue_ledger": ledger
        })

    manifest = {
        "session_id": "s1",
        "indexed_file": "sessions/data/index/s1-raw-indexed.md",
        "raw_file_hash": file_hash,
        "total_raw_lines": total_lines,
        "scene_blocks": scene_blocks
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Wrote manifest: {manifest_path}")

if __name__ == "__main__":
    build_manifest()
