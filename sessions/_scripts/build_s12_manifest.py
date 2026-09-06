import json
import os

manifest_path = "sessions/data/index/s12-manifest.json"
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

for block in manifest["scene_blocks"]:
    if block.get("ooc", False):
        continue
    start, end = block["line_range"]
    ledger = block.get("dialogue_ledger", [])
    if not ledger and block["scene_id"] == 19:
        ledger.append({
            "line": 1651,
            "speaker": "GM",
            "gist": "GM narration of the shared ancestral vision of the 5 clans.",
            "covers": [1651, 1710]
        })
        block["dialogue_ledger"] = ledger
    if ledger:
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

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

print("Updated s12-manifest.json with contiguous covers spans.")
