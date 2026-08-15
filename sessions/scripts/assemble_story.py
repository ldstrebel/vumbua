"""Assemble sN-clean-story.md from per-scene block files.

Reads the manifest for scene order and OOC flags, pulls non-OOC blocks from
sessions/transcripts/clean/blocks/sN-scene-XX.md, emits OOC scenes as bare
RAW_RANGE marker lines, merges per-scene assumption logs into
sessions/transcripts/index/sN-assumptions.json, and writes the canonical
story file. Fails loudly if a required block file is missing or its
RAW_RANGE header disagrees with the manifest.

Usage: python assemble_story.py s12 --title "SESSION TITLE"
"""

import argparse
import json
import os
import re
import sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("session_id")
    ap.add_argument("--title", default=None, help="Top-level # title for the story")
    args = ap.parse_args()
    sid = args.session_id

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manifest_path = os.path.join(base, "transcripts", "index", f"{sid}-manifest.json")
    blocks_dir = os.path.join(base, "transcripts", "clean", "blocks")
    out_path = os.path.join(base, "transcripts", "clean", f"{sid}-clean-story.md")
    assumptions_out = os.path.join(base, "transcripts", "index", f"{sid}-assumptions.json")

    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    errors = []
    parts = []
    assumptions = []

    if args.title:
        parts.append(
            "---\n"
            f'title: "{args.title}"\n'
            'author: "Novel Adaptation in the Style of Brandon Sanderson"\n'
            "campaign: Vumbua\n"
            "genre: Epic Fantasy / Sci-Fantasy\n"
            "---\n\n"
            f"# {args.title.upper()}\n"
        )

    for block in manifest["scene_blocks"]:
        scene_id = block["scene_id"]
        start, end = block["line_range"]
        if block.get("ooc", False):
            parts.append(f"<!-- RAW_RANGE: [{start}, {end}] | SCENE_ID: {scene_id} | OOC -->\n")
            continue

        block_path = os.path.join(blocks_dir, f"{sid}-scene-{scene_id:02d}.md")
        if not os.path.exists(block_path):
            errors.append(f"MISSING BLOCK FILE: {block_path}")
            continue
        with open(block_path, encoding="utf-8") as f:
            content = f.read().strip()

        m = re.match(
            r"<!--\s*RAW_RANGE:\s*\[(\d+),\s*(\d+)\]\s*\|\s*SCENE_ID:\s*(\d+)\s*-->",
            content,
        )
        if not m:
            errors.append(f"BLOCK {scene_id}: missing/malformed RAW_RANGE header")
        elif (int(m.group(1)), int(m.group(2)), int(m.group(3))) != (start, end, scene_id):
            errors.append(
                f"BLOCK {scene_id}: header [{m.group(1)}, {m.group(2)}] scene {m.group(3)} "
                f"disagrees with manifest [{start}, {end}] scene {scene_id}"
            )
        if "LEDGER:" not in content:
            errors.append(f"BLOCK {scene_id}: missing LEDGER footer")
        parts.append(content + "\n")

        a_path = os.path.join(blocks_dir, f"{sid}-scene-{scene_id:02d}-assumptions.json")
        if os.path.exists(a_path):
            try:
                with open(a_path, encoding="utf-8") as f:
                    entries = json.load(f)
                if isinstance(entries, list):
                    assumptions.extend(entries)
                else:
                    errors.append(f"ASSUMPTIONS {scene_id}: not a JSON array")
            except json.JSONDecodeError as e:
                errors.append(f"ASSUMPTIONS {scene_id}: invalid JSON ({e})")

    if errors:
        print("[FAIL] ASSEMBLY ABORTED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    full_raw_text = "\n".join(parts)
    # Strip HTML comments like <!-- L0123 -->, <!-- RAW_RANGE... -->, and <!-- LEDGER... --> for final clean reader output
    clean_story_text = re.sub(r"<!--\s*L\d+\s*-->", "", full_raw_text)
    clean_story_text = re.sub(r"<!--\s*RAW_RANGE:.*?-->\n?", "", clean_story_text)
    clean_story_text = re.sub(r"<!--\s*LEDGER:.*?-->\n?", "", clean_story_text)
    clean_story_text = re.sub(r"\n{3,}", "\n\n", clean_story_text).strip() + "\n"

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(clean_story_text)

    for i, a in enumerate(assumptions, 1):
        a["id"] = f"A-{i:03d}"
    with open(assumptions_out, "w", encoding="utf-8") as f:
        json.dump(assumptions, f, indent=2)

    print(f"[OK] Wrote {out_path} ({len(manifest['scene_blocks'])} scenes)")
    print(f"[OK] Wrote {assumptions_out} ({len(assumptions)} assumptions)")


if __name__ == "__main__":
    main()
