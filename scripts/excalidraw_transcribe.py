#!/usr/bin/env python3
"""
Part 1: Excalidraw Transcribe

Scans Excalidraw/ for new or modified PNG files, sends them to GPT-4o vision
for transcription, and writes companion markdown files.

Uses .excalidraw-manifest.json for incremental processing (only new/changed PNGs).

Environment variables:
  OPENAI_API_KEY  -- Required. GPT-4o API key.
  FORCE_ALL       -- Optional. "true" to re-process all PNGs regardless of manifest.
  DRY_RUN         -- Optional. "true" to log what would be processed without calling API.
  VISION_MODEL    -- Optional. Defaults to "gpt-4o".
  MAX_IMAGES      -- Optional. Safety limit per run. Defaults to 20.
"""

import base64
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCALIDRAW_DIR = os.path.join(REPO_ROOT, "Excalidraw")
MANIFEST_PATH = os.path.join(REPO_ROOT, ".excalidraw-manifest.json")

VISION_MODEL = os.environ.get("VISION_MODEL", "gpt-4o")
MAX_IMAGES = int(os.environ.get("MAX_IMAGES", "20"))
FORCE_ALL = os.environ.get("FORCE_ALL", "false").lower() == "true"
DRY_RUN = os.environ.get("DRY_RUN", "false").lower() == "true"

KNOWN_ENTITIES = [
    "Britt", "Aggie", "Ignatius", "Lomi", "Iggy",
    "Dean Isolde Vane", "Celia Vance", "Hesperus", "Ratchet", "Kojo",
    "Pyrrhus", "Professor Kante", "Valerius Sterling", "Serra Vox",
    "Cassius Thorne", "Iron-Jaw Jax", "Maria Wall", "Brawn", "Nyx",
    "Kaelen", "Mira", "Calculus Prime", "Theorem", "Lemma",
    "Dr. Rose Halloway", "Silas Thorne", "Bramble", "Cinder-4",
    "Hearth", "Kindle", "Captain Barnacle", "Pressure", "Depth",
    "Percival Vane-Smythe III", "Lady Glimmer", "Baron Bolt",
    "Sarge", "Lucky", "Pudge", "Lady Ignis", "Rill", "Zephyr",
    "Lance", "Valerius Sterling Sr.", "Lady Glissade", "Ember",
    "Tommy", "Lucina", "Marla", "Soot",
    "Mizizi", "Ash-Bloods", "Trench-Kin", "Renali", "Wadi", "Fulgur-Born",
    "House Gilded", "Vane Lineage", "Scrivener Guild", "Iron Union",
    "Verdant Trust", "High-Justiciars", "Grand Architects", "Syndicate of Sails",
    "Vumbua Academy", "The Bleed", "The Minimum", "Harmony Nodes",
    "Power System", "Pre-Stitch Artifacts", "The Loom",
    "Ether-Jelly", "Void-Beast", "Rot-Shepherd", "Whispering Moth",
]

TRANSCRIPTION_PROMPT = """You are transcribing a handwritten/drawn note from a TTRPG campaign wiki called "Vumbua."

Read everything in this image and produce a structured markdown transcription:

1. Transcribe ALL text exactly as written (typed and handwritten)
2. Preserve structure: if text is in boxes, use blockquotes. If bulleted, use bullets. If there are arrows between items, note the relationships.
3. For any proper nouns that might be campaign entities (character names, locations, factions), wrap them in [[wikilinks]]
4. If something is illegible, write [illegible]
5. Note any non-text elements: [diagram: ...], [drawing: ...], [arrow from X to Y]

Known campaign entities for reference: {entities}

Output ONLY the transcription in markdown format. No commentary."""


def load_manifest():
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH) as f:
            return json.load(f)
    return {"version": 1, "last_run": None, "files": {}}


def save_manifest(manifest):
    manifest["last_run"] = datetime.now(timezone.utc).isoformat()
    with open(MANIFEST_PATH, "w") as f:
        json.dump(manifest, f, indent=2)


def sha256_file(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def find_pngs():
    pngs = []
    if not os.path.isdir(EXCALIDRAW_DIR):
        return pngs
    for root, _dirs, files in os.walk(EXCALIDRAW_DIR):
        for f in files:
            if f.lower().endswith(".png") and not f.endswith("-transcription.png"):
                pngs.append(os.path.join(root, f))
    return sorted(pngs)


def needs_processing(filepath, manifest):
    rel = os.path.relpath(filepath, REPO_ROOT)
    current_hash = sha256_file(filepath)
    if FORCE_ALL:
        return True, current_hash
    entry = manifest.get("files", {}).get(rel)
    if entry is None or entry.get("sha256") != current_hash:
        return True, current_hash
    return False, current_hash


def transcribe_image(filepath):
    """Send a PNG to GPT-4o vision and return the transcription text."""
    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: openai package not installed. Run: pip install openai")
        sys.exit(1)

    client = OpenAI()

    with open(filepath, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")

    entity_list = ", ".join(KNOWN_ENTITIES)
    prompt = TRANSCRIPTION_PROMPT.format(entities=entity_list)

    response = client.chat.completions.create(
        model=VISION_MODEL,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_data}",
                            "detail": "high",
                        },
                    },
                ],
            }
        ],
        max_tokens=4096,
    )

    return response.choices[0].message.content


def write_transcription(png_path, text, sha):
    base = os.path.splitext(png_path)[0]
    out_path = base + "-transcription.md"
    rel_png = os.path.relpath(png_path, REPO_ROOT)
    now = datetime.now(timezone.utc).isoformat()

    name = os.path.splitext(os.path.basename(png_path))[0]

    content = f"""---
source: "{rel_png}"
transcribed: "{now}"
sha256: "{sha}"
model: "{VISION_MODEL}"
---

# Transcription: {name}

{text}
"""
    with open(out_path, "w") as f:
        f.write(content)
    return os.path.relpath(out_path, REPO_ROOT)


def main():
    print("=" * 60)
    print("EXCALIDRAW TRANSCRIBE (Part 1)")
    print("=" * 60)

    if DRY_RUN:
        print("[DRY RUN] No API calls will be made\n")

    manifest = load_manifest()
    pngs = find_pngs()

    if not pngs:
        print("No PNG files found in Excalidraw/")
        return

    print(f"Found {len(pngs)} PNG file(s) in Excalidraw/\n")

    to_process = []
    for png in pngs:
        needs, sha = needs_processing(png, manifest)
        if needs:
            to_process.append((png, sha))

    if not to_process:
        print("All PNGs already processed (manifest up to date)")
        return

    if len(to_process) > MAX_IMAGES:
        print(f"WARNING: {len(to_process)} PNGs to process, capping at {MAX_IMAGES}")
        to_process = to_process[:MAX_IMAGES]

    print(f"Processing {len(to_process)} new/modified PNG(s):\n")

    processed = 0
    for png_path, sha in to_process:
        rel = os.path.relpath(png_path, REPO_ROOT)
        print(f"  [{processed + 1}/{len(to_process)}] {rel}")

        if DRY_RUN:
            print(f"    [DRY RUN] Would transcribe (sha256: {sha[:12]}...)")
            processed += 1
            continue

        try:
            text = transcribe_image(png_path)
            out_rel = write_transcription(png_path, text, sha)
            print(f"    -> {out_rel}")

            manifest.setdefault("files", {})[rel] = {
                "sha256": sha,
                "transcribed_at": datetime.now(timezone.utc).isoformat(),
                "transcription_file": out_rel,
                "model": VISION_MODEL,
                "status": "complete",
            }
            processed += 1
        except Exception as e:
            print(f"    ERROR: {e}")
            manifest.setdefault("files", {})[rel] = {
                "sha256": sha,
                "transcribed_at": datetime.now(timezone.utc).isoformat(),
                "transcription_file": None,
                "model": VISION_MODEL,
                "status": f"error: {e}",
            }

    save_manifest(manifest)

    print(f"\n{'=' * 60}")
    print(f"DONE: {processed}/{len(to_process)} PNGs transcribed")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
