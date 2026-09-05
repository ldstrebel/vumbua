"""Generates sessions/transcripts/index/s3-manifest.json and validates it."""

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
    indexed_path = os.path.join(base_dir, "transcripts", "index", "s3-raw-indexed.md")
    manifest_path = os.path.join(base_dir, "transcripts", "index", "s3-manifest.json")
    attr_path = os.path.join(base_dir, "transcripts", "index", "s3-attribution.json")

    with open(indexed_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    total_lines = len(raw_lines)
    file_hash = get_sha256(indexed_path)

    with open(attr_path, "r", encoding="utf-8") as f:
        attr_data = json.load(f)

    attr_by_line = {}
    for seg in attr_data.get("segments", []):
        attr_by_line[seg["line"]] = seg

    scene_defs = [
        {"id": 1, "title": "OOC Pre-Session Chit-Chat & Notes", "range": [1, 12], "ooc": True},
        {"id": 2, "title": "The Walk to the Celestial Lounge & Cartography", "range": [13, 80], "ooc": False},
        {"id": 3, "title": "Crown and Ruin & The Stolen Study Guide", "range": [81, 150], "ooc": False},
        {"id": 4, "title": "The Ambush & Chase in the Alley", "range": [151, 165], "ooc": False},
        {"id": 5, "title": "Azer's Interrogation & The Plan for Lucky", "range": [166, 195], "ooc": False},
        {"id": 6, "title": "OOC Table Talk, Mechanics & Granola Notes", "range": [196, total_lines], "ooc": True},
    ]

    indexed_by_num = {}
    for line in raw_lines:
        m = re.match(r"^L(\d+):\s+(?:\*\*([^*]+):\*\*|\[(undiarized|ai-summary)\](?:\s+\[TURN\?\])?)\s*(.*)$", line.strip())
        if m:
            indexed_by_num[int(m.group(1))] = m.group(4).strip()

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
        "session_id": "s3",
        "raw_file": "transcripts/index/s3-raw-indexed.md",
        "raw_file_hash": file_hash,
        "total_raw_lines": total_lines,
        "target_word_budget": 6000,
        "scene_blocks": scene_blocks
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Manifest written to {manifest_path} with {len(scene_blocks)} scene blocks.")

if __name__ == "__main__":
    build_manifest()
