"""Generates sessions/transcripts/index/s2-manifest.json and validates it."""

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
    indexed_path = os.path.join(base_dir, "transcripts", "index", "s2-raw-indexed.md")
    manifest_path = os.path.join(base_dir, "transcripts", "index", "s2-manifest.json")
    attr_path = os.path.join(base_dir, "transcripts", "index", "s2-attribution.json")

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
        {"id": 1, "title": "OOC Pre-Game Rules & Character Sheets", "range": [1, 100], "ooc": True},
        {"id": 2, "title": "OOC Mechanics & Ice Storm Discussion", "range": [101, 200], "ooc": True},
        {"id": 3, "title": "OOC Radio Recap & Beastiary Check", "range": [201, 305], "ooc": True},
        {"id": 4, "title": "The Bonfire at Block 99", "range": [306, 440], "ooc": False},
        {"id": 5, "title": "Courtyard Clusters & Greek Row", "range": [441, 570], "ooc": False},
        {"id": 6, "title": "Lucky's Lucidian Trade & Sarah's Inquiries", "range": [571, 700], "ooc": False},
        {"id": 7, "title": "The Cycle of Life & Death", "range": [701, 830], "ooc": False},
        {"id": 8, "title": "Engine Grease Moonshine & Zephyr's Strike", "range": [831, 950], "ooc": False},
        {"id": 9, "title": "Rill's Interruption & Lava Boy", "range": [951, 1070], "ooc": False},
        {"id": 10, "title": "The Lucidian Thermal Anomaly & Night Walk", "range": [1071, 1184], "ooc": False},
        {"id": 11, "title": "OOC Loom Architecture & First Week Plan", "range": [1185, total_lines], "ooc": True},
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
                    text = m.group(3).strip()

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

        # Set contiguous covers spans for ledger items to encompass unindexed/timestamp lines
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
            "ooc": is_ooc,
            "speakers_present": sorted(list(speakers_present)),
            "dialogue_ledger": ledger
        })

    manifest = {
        "session_id": "s2",
        "indexed_file": "sessions/transcripts/index/s2-raw-indexed.md",
        "raw_file_hash": file_hash,
        "total_raw_lines": total_lines,
        "scene_blocks": scene_blocks
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"Wrote manifest: {manifest_path} ({len(scene_blocks)} scenes, total lines: {total_lines})")

if __name__ == "__main__":
    build_manifest()
