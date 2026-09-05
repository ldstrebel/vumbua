"""Generates sessions/data/index/s2.5-manifest.json and validates it."""

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
    indexed_path = os.path.join(base_dir, "data", "index", "s2.5-raw-indexed.md")
    manifest_path = os.path.join(base_dir, "data", "index", "s2.5-manifest.json")
    attr_path = os.path.join(base_dir, "data", "index", "s2.5-attribution.json")

    with open(indexed_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    total_lines = len(raw_lines)
    file_hash = get_sha256(indexed_path)

    # Load attribution segments
    with open(attr_path, "r", encoding="utf-8") as f:
        attr_data = json.load(f)

    attr_by_line = {}
    for seg in attr_data.get("segments", []):
        attr_by_line[seg["line"]] = seg

    scene_defs = [
        {"id": 1, "title": "OOC Pre-Session Chit-Chat (Gym & Diets)", "range": [1, 100], "ooc": True},
        {"id": 2, "title": "OOC Pre-Session Chit-Chat (Drinks & Sodas)", "range": [101, 187], "ooc": True},
        {"id": 3, "title": "The Loner & The Crane", "range": [188, 284], "ooc": False},
        {"id": 4, "title": "Irish Goodbye to the Bonfire", "range": [285, 400], "ooc": False},
        {"id": 5, "title": "Infiltrating L-Power", "range": [401, 525], "ooc": False},
        {"id": 6, "title": "Tommy, Lucina & The Catwalk", "range": [526, 658], "ooc": False},
        {"id": 7, "title": "The Overengineered Battery & The Global Decline", "range": [659, 760], "ooc": False},
        {"id": 8, "title": "The Tortoise in the Top Hat", "range": [761, 884], "ooc": False},
        {"id": 9, "title": "Nodes of Harmony & The Missing Surge", "range": [885, 1000], "ooc": False},
        {"id": 10, "title": "The Ship of Many Oars", "range": [1001, 1126], "ooc": False},
        {"id": 11, "title": "The Clan Exchange", "range": [1127, 1225], "ooc": False},
        {"id": 12, "title": "The Amber Core & Night Experiments", "range": [1226, 1329], "ooc": False},
        {"id": 13, "title": "OOC Post-Session Chat (New York Flights & Schedule)", "range": [1330, 1450], "ooc": True},
        {"id": 14, "title": "OOC Post-Session Chat (Delta Booking & Miles)", "range": [1451, 1570], "ooc": True},
        {"id": 15, "title": "OOC Post-Session Chat (Wedding Bands & Attire)", "range": [1571, 1685], "ooc": True},
        {"id": 16, "title": "OOC Post-Session Chat (Bachelorette Decor & Book Pages)", "range": [1686, 1800], "ooc": True},
        {"id": 17, "title": "OOC Post-Session Chat (Driving vs Flying & Activities)", "range": [1801, 1925], "ooc": True},
        {"id": 18, "title": "OOC Post-Session Chat (Sedona Tours & Wedding Budget)", "range": [1926, total_lines], "ooc": True},
    ]

    indexed_by_num = {}
    for line in raw_lines:
        m = re.match(r"^L(\d+):\s+(?:\*\*([^*]+):\*\*|\[undiarized\](?:\s+\[TURN\?\])?)\s*(.*)$", line.strip())
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
        "session_id": "s2.5",
        "raw_file": "data/index/s2.5-raw-indexed.md",
        "raw_file_hash": file_hash,
        "total_raw_lines": total_lines,
        "target_word_budget": 8000,
        "scene_blocks": scene_blocks
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Manifest written to {manifest_path} with {len(scene_blocks)} scene blocks.")

if __name__ == "__main__":
    build_manifest()
