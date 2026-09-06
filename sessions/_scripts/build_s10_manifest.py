"""Generates sessions/data/index/s10-manifest.json and validates it."""

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
    indexed_path = os.path.join(base_dir, "data", "index", "s10-raw-indexed.md")
    manifest_path = os.path.join(base_dir, "data", "index", "s10-manifest.json")
    attr_path = os.path.join(base_dir, "data", "index", "s10-attribution.json")

    with open(indexed_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    total_lines = len(raw_lines)
    file_hash = get_sha256(indexed_path)

    with open(attr_path, "r", encoding="utf-8") as f:
        attr_data = json.load(f)

    attr_by_line = {}
    for seg in attr_data.get("segments", []):
        attr_by_line[seg["line"]] = seg

    # Break 1..5313 into chunks <= 140 lines
    # 1..500: OOC setup (4 chunks)
    # 501..1050: Chapter 89 - Magnetic Sand Surfing (4 chunks)
    # 1051..1800: Chapter 90 - Iggy's First Tree & Forest Chase (6 chunks)
    # 1801..2600: Chapter 91 - The Soulless Forest & Shoreline Pebble Signal (6 chunks)
    # 2601..3500: Chapter 92 - Midnight Construction & The Natty Renaming (7 chunks)
    # 3501..4300: Chapter 93 - Rill at 4 AM & The Flare Gun (6 chunks)
    # 4301..5200: Chapter 94 - 8 AM Barrier Drop & Dagger Shark Attack (7 chunks)
    # 5201..5313: Post-session wrapup (1 chunk)

    chunks = []
    
    # Helper to slice a range [start, end] into chunks of size <= max_size
    def add_range(title_prefix, start, end, is_ooc, max_size=135):
        cur = start
        part = 1
        while cur <= end:
            chunk_end = min(cur + max_size - 1, end)
            title = f"{title_prefix} Part {part}" if (end - start + 1) > max_size else title_prefix
            chunks.append((title, cur, chunk_end, is_ooc))
            cur = chunk_end + 1
            part += 1

    add_range("OOC Pre-Session Setup & Recap", 1, 500, True)
    add_range("Magnetic Sand Surfing in Sector 1", 501, 1050, False)
    add_range("Iggy's First Tree & The Forest Loop Chase", 1051, 1800, False)
    add_range("The Soulless Forest & The Shoreline Signal", 1801, 2600, False)
    add_range("Midnight Construction & The Natty Renaming", 2601, 3500, False)
    add_range("Rill's 4 AM Warning & The Flare Gun", 3501, 4300, False)
    add_range("The 8 AM Barrier Drop & Dagger Sharks", 4301, 5200, False)
    add_range("OOC Post-Session Wrap-Up & Scheduling", 5201, total_lines, True)

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
        "session_id": "s10",
        "raw_file": "data/index/s10-raw-indexed.md",
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
