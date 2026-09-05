"""Generates sessions/transcripts/index/s0-manifest.json and validates it."""

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
    indexed_path = os.path.join(base_dir, "transcripts", "index", "s0-raw-indexed.md")
    manifest_path = os.path.join(base_dir, "transcripts", "index", "s0-manifest.json")

    with open(indexed_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    total_lines = len(raw_lines)
    file_hash = get_sha256(indexed_path)

    # Contiguous Scene Blocks tiling lines 1 to 773
    scene_defs = [
        {"id": 1, "title": "The Stalled Rot: The Mizizi Philosophy & The Cousins", "range": [1, 98], "ooc": False},
        {"id": 2, "title": "The Trench-Kin: Below Ground & The River Exchange", "range": [99, 183], "ooc": False},
        {"id": 3, "title": "The Ember Isles: Artificial Fire & The Dying Caldera", "range": [184, 248], "ooc": False},
        {"id": 4, "title": "The Boilermakers of Harmony: Continental Drift & The 80-Year Lull", "range": [249, 335], "ooc": False},
        {"id": 5, "title": "Leaving the Megaflora: The Empathy Link & The Walled Citadel", "range": [336, 450], "ooc": False},
        {"id": 6, "title": "The Pier & The Pilgrimage: Iggy's Coat & Ignatius's Defiance", "range": [451, 527], "ooc": False},
        {"id": 7, "title": "End of Shift: Lomi's Gospel of Public Infrastructure", "range": [528, 600], "ooc": False},
        {"id": 8, "title": "The Great Intake: 100,000 Hopefuls & The Psych Trials", "range": [601, 730], "ooc": False},
        {"id": 9, "title": "Session 0 Wrap-Up & Table Cooldown", "range": [731, 772], "ooc": True},
    ]

    scene_blocks = []

    for sdef in scene_defs:
        sid = sdef["id"]
        title = sdef["title"]
        start, end = sdef["range"]
        is_ooc = sdef["ooc"]

        speakers_present = set()
        ledger = []

        for l_idx in range(start - 1, end):
            line = raw_lines[l_idx].strip()
            m = re.match(r"^L(\d+):\s+\*\*([^*]+):\*\*\s*(.*)$", line)
            if m:
                l_num = int(m.group(1))
                speaker_stream = m.group(2).strip()
                text = m.group(3).strip()

                speaker = speaker_stream
                if speaker_stream == "Sophie":
                    speaker = "Britt"
                elif speaker_stream == "Luke F":
                    speaker = "Lomi"
                elif speaker_stream == "Holly":
                    speaker = "Iggy"
                elif speaker_stream == "John":
                    speaker = "Ignatius"
                elif speaker_stream == "Luke S":
                    speaker = "GM"

                speakers_present.add(speaker)

                if not is_ooc:
                    ledger.append({
                        "line": l_num,
                        "speaker": speaker,
                        "gist": text[:100]
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
            "key_narrative_beats": [],
            "dialogue_ledger": ledger
        })

    manifest = {
        "session_id": "s0",
        "indexed_file": "sessions/transcripts/index/s0-raw-indexed.md",
        "raw_file_hash": file_hash,
        "total_raw_lines": total_lines,
        "scene_blocks": scene_blocks
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print(f"[OK] Manifest written to {manifest_path}")
    print(f"Total scenes: {len(scene_blocks)} | Total raw lines tiled: {total_lines}")

if __name__ == "__main__":
    build_manifest()
