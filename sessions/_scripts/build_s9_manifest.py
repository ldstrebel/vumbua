"""Generates sessions/data/index/s9-manifest.json and validates it."""

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
    indexed_path = os.path.join(base_dir, "data", "index", "s9-raw-indexed.md")
    manifest_path = os.path.join(base_dir, "data", "index", "s9-manifest.json")
    attr_path = os.path.join(base_dir, "data", "index", "s9-attribution.json")

    with open(indexed_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    total_lines = len(raw_lines)
    file_hash = get_sha256(indexed_path)

    with open(attr_path, "r", encoding="utf-8") as f:
        attr_data = json.load(f)

    attr_by_line = {}
    for seg in attr_data.get("segments", []):
        attr_by_line[seg["line"]] = seg

    # Split lines 1 to 650 into 6 OOC chunks <= 110 lines each
    ooc_chunks = [
        (1, 110), (111, 220), (221, 330), (331, 440), (441, 550), (551, 650)
    ]

    scene_defs = []
    sc_id = 1
    for s, e in ooc_chunks:
        scene_defs.append({
            "id": sc_id,
            "title": f"OOC Pre-Session Setup & Planning Part {sc_id}",
            "range": [s, e],
            "ooc": True
        })
        sc_id += 1

    in_game_chunks = [
        ("Flashback: Five Sectors on the Zephyr", 651, 780),
        ("The Firefighter Guard Bribe & Stand Security", 781, 920),
        ("The Loom Drop & Bleacher Address", 921, 1060),
        ("The Steam Lift & The Pixie Cadet Save", 1061, 1200),
        ("Ignatius Wakes & The Gravity Scramble", 1201, 1350),
        ("Air Shopping: Scavenging Sector 2", 1351, 1500),
        ("Iggy in Sector 4: Steam Vent Spa", 1501, 1650),
        ("The Cyclops Troll & Raw Crystal Mining", 1651, 1800),
        ("The Mud Lash Escape & Peace Offering", 1801, 1950),
        ("Loami in Sector 1: Gravity Wall Climbing", 1951, 2100),
        ("The 200-Foot Overclock Tunnel Fall", 2101, 2250),
        ("Sector 5 Basin & Center Canyon Recovery", 2251, 2400),
        ("Sector 3 Wetlands Rendezvous", 2401, 2500),
    ]

    for title, s, e in in_game_chunks:
        scene_defs.append({
            "id": sc_id,
            "title": title,
            "range": [s, e],
            "ooc": False
        })
        sc_id += 1

    # Final post-session wrap-up OOC
    scene_defs.append({
        "id": sc_id,
        "title": "OOC Post-Session Wrap-Up & Scheduling",
        "range": [2501, total_lines],
        "ooc": True
    })

    indexed_by_num = {}
    for line in raw_lines:
        m = re.match(r"^L(\d+):\s+(?:\*\*([^*]+):\*\*|\[(?:undiarized|ai-summary)\](?:\s+\[TURN\?\])?)\s*(.*)$", line.strip())
        if m:
            indexed_by_num[int(m.group(1))] = m.group(3).strip()

    scene_blocks = []

    for sdef in scene_defs:
        sid = sdef["id"]
        title = sdef["title"]
        start, end = sdef["range"]
        is_ooc = sdef["ooc"]

        speakers_present = set()
        ledger = []

        if not is_ooc:
            for l_num in range(start, end + 1):
                text = indexed_by_num.get(l_num)
                if text is None:
                    continue

                attr = attr_by_line.get(l_num)
                if attr and not attr.get("ooc", False):
                    speaker = attr.get("identity") or "GM"
                    if speaker == "Lomi":
                        speaker = "Loami"
                    speakers_present.add(speaker)
                    gist = text.replace('"', "'")
                    if len(gist) > 60:
                        gist = gist[:57] + "..."
                    ledger.append({
                        "line": l_num,
                        "speaker": speaker,
                        "gist": gist
                    })

        # Set contiguous covers spans for ledger items
        if not is_ooc and ledger:
            for idx in range(len(ledger)):
                cur_line = ledger[idx]["line"]
                if idx == 0:
                    span_start = start
                else:
                    span_start = cur_line

                if idx < len(ledger) - 1:
                    span_end = ledger[idx + 1]["line"] - 1
                else:
                    span_end = end

                ledger[idx]["covers"] = [span_start, span_end]

        scene_blocks.append({
            "scene_id": sid,
            "title": title,
            "line_range": [start, end],
            "raw_line_count": end - start + 1,
            "speakers_present": sorted(list(speakers_present)),
            "dialogue_ledger": ledger,
            "ooc": is_ooc
        })

    manifest = {
        "session_id": "s9",
        "raw_file": "data/index/s9-raw-indexed.md",
        "raw_file_hash": file_hash,
        "total_raw_lines": total_lines,
        "target_word_budget": 6500,
        "scene_blocks": scene_blocks
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Manifest written to {manifest_path} with {len(scene_blocks)} scene blocks.")

if __name__ == "__main__":
    build_manifest()
