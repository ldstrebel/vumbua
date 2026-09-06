"""Generates sessions/data/index/s11-manifest.json and validates it."""

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
    indexed_path = os.path.join(base_dir, "data", "index", "s11-raw-indexed.md")
    manifest_path = os.path.join(base_dir, "data", "index", "s11-manifest.json")
    attr_path = os.path.join(base_dir, "data", "index", "s11-attribution.json")

    with open(indexed_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    total_lines = len(raw_lines)
    file_hash = get_sha256(indexed_path)

    with open(attr_path, "r", encoding="utf-8") as f:
        attr_data = json.load(f)

    attr_by_line = {}
    for seg in attr_data.get("segments", []):
        attr_by_line[seg["line"]] = seg

    chunks = []
    
    def add_range(title_prefix, start, end, is_ooc, max_size=125):
        cur = start
        part = 1
        while cur <= end:
            chunk_end = min(cur + max_size - 1, end)
            title = f"{title_prefix} Part {part}" if (end - start + 1) > max_size else title_prefix
            chunks.append((title, cur, chunk_end, is_ooc))
            cur = chunk_end + 1
            part += 1

    add_range("OOC Pre-Session Setup & Recap", 1, 250, True)
    add_range("The Mewoders in the Canopy", 251, 550, False)
    add_range("Pip and the Storm Raptor", 551, 850, False)
    add_range("Mwaza-Chui and the Static Roar", 851, 1150, False)
    add_range("Bramble in the Trees", 1151, 1450, False)
    add_range("Don't Touch My Biscuits", 1451, 1750, False)
    add_range("The Sacred Memory Network", 1751, 2100, False)
    add_range("The Spirit Tortoise Descends", 2101, 2400, False)
    add_range("OOC Post-Session Wrap-Up & Level 5", 2401, total_lines, True)

    indexed_by_num = {}
    for line in raw_lines:
        m = re.match(r"^L(\d+):\s+(?:\*\*([^*]+):\*\*|\[(?:undiarized|ai-summary)\](?:\s+\[TURN\?\])?)\s*(.*)$", line.strip())
        if m:
            indexed_by_num[int(m.group(1))] = m.group(3).strip()

    scene_blocks = []
    sc_id = 1

    for title, start, end, is_ooc in chunks:
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
            "scene_id": sc_id,
            "title": title,
            "line_range": [start, end],
            "raw_line_count": end - start + 1,
            "speakers_present": sorted(list(speakers_present)),
            "dialogue_ledger": ledger,
            "ooc": is_ooc
        })
        sc_id += 1

    manifest = {
        "session_id": "s11",
        "raw_file": "data/index/s11-raw-indexed.md",
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
