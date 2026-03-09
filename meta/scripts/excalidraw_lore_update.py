#!/usr/bin/env python3
"""
Part 2: Excalidraw Lore Update

Reads new transcription files produced by Part 1, identifies proper nouns,
creates stub pages for new entities, updates wikilinks across the vault,
and writes a summary for the GitHub Issue.

Environment variables:
  DRY_RUN  -- Optional. "true" to log what would change without modifying files.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXCALIDRAW_DIR = os.path.join(REPO_ROOT, "meta", "Excalidraw")
MANIFEST_PATH = os.path.join(REPO_ROOT, ".excalidraw-manifest.json")
SUMMARY_PATH = os.path.join(REPO_ROOT, ".excalidraw-lore-summary.md")
CHANGELOG_PATH = os.path.join(REPO_ROOT, "CHANGELOG.md")
CONVERT_SCRIPT = os.path.join(REPO_ROOT, "meta", "scripts", "convert_to_obsidian.py")
LORE_INDEX_PATH = os.path.join(REPO_ROOT, ".agent", "workflows", "lore-index.md")

DRY_RUN = os.environ.get("DRY_RUN", "false").lower() == "true"

STUB_TEMPLATE = """---
aliases: []
tags: [{category}, stub, needs-review]
---

# {name}

> Stub page auto-generated from Excalidraw transcription.
> Source: `{source}`
> Date: {date}

## Context

{context}

---

> [!warning]- Needs Review
> This page was auto-generated from a drawing transcription. A human should review and expand it.
"""

CATEGORY_HINTS = {
    "npc": ["character", "person", "npc", "student", "professor", "captain", "dean",
            "lady", "lord", "baron", "dr", "sir"],
    "location": ["location", "place", "academy", "spire", "core", "hull", "block",
                 "district", "lounge", "room", "forest", "isle"],
    "faction": ["faction", "clan", "house", "guild", "union", "trust", "syndicate",
                "order"],
    "creature": ["creature", "beast", "monster", "jelly", "moth", "shepherd"],
    "lore": ["concept", "system", "power", "artifact", "event", "ceremony"],
}

CATEGORY_TO_DIR = {
    "npc": "characters/npcs",
    "location": "locations",
    "faction": "factions",
    "creature": "bestiary",
    "lore": "world",
}


def load_manifest():
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH) as f:
            return json.load(f)
    return {"version": 1, "last_run": None, "files": {}}


def load_registry():
    """Import the REGISTRY dict from convert_to_obsidian.py."""
    registry = {}
    sys.path.insert(0, os.path.join(REPO_ROOT, "meta", "scripts"))
    try:
        import convert_to_obsidian
        registry = convert_to_obsidian.REGISTRY
    except Exception as e:
        print(f"WARNING: Could not load REGISTRY: {e}")
    return registry


def find_new_transcriptions():
    """Find transcription files that are new or modified since last Part 2 run."""
    transcriptions = []
    if not os.path.isdir(EXCALIDRAW_DIR):
        return transcriptions
    for root, _dirs, files in os.walk(EXCALIDRAW_DIR):
        for f in files:
            if f.endswith("-transcription.md"):
                transcriptions.append(os.path.join(root, f))
    return sorted(transcriptions)


def extract_wikilinks(text):
    """Extract all [[wikilinks]] from transcription text."""
    pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
    return list(set(re.findall(pattern, text)))


def read_transcription(filepath):
    """Read a transcription file, return (frontmatter_dict, body_text)."""
    with open(filepath) as f:
        content = f.read()

    frontmatter = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().split("\n"):
                if ":" in line:
                    key, val = line.split(":", 1)
                    frontmatter[key.strip()] = val.strip().strip('"')
            body = parts[2]

    return frontmatter, body


def guess_category(name, context):
    """Guess entity category from name and surrounding context."""
    name_lower = name.lower()
    context_lower = context.lower()

    for category, hints in CATEGORY_HINTS.items():
        for hint in hints:
            if hint in name_lower or hint in context_lower:
                return category

    return "npc"


def get_context_for_entity(name, body):
    """Extract the sentence/paragraph where an entity is mentioned."""
    for line in body.split("\n"):
        if name in line:
            return line.strip()
    return f"Mentioned in Excalidraw drawing transcription."


def slugify(name):
    """Convert entity name to file slug."""
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def create_stub_page(name, category, source, context):
    """Create a stub markdown page for a new entity."""
    directory = os.path.join(REPO_ROOT, CATEGORY_TO_DIR.get(category, "world"))
    os.makedirs(directory, exist_ok=True)

    slug = slugify(name)
    filepath = os.path.join(directory, f"{slug}.md")

    if os.path.exists(filepath):
        return None

    content = STUB_TEMPLATE.format(
        category=category,
        name=name,
        source=source,
        date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        context=context,
    )

    if not DRY_RUN:
        with open(filepath, "w") as f:
            f.write(content)

    rel = os.path.relpath(filepath, REPO_ROOT)
    return rel


def update_changelog(summary_lines):
    """Append pipeline summary to CHANGELOG.md."""
    if not os.path.exists(CHANGELOG_PATH):
        return

    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    entry = f"\n### {date_str} — Excalidraw Pipeline\n\n"
    for line in summary_lines:
        entry += f"- {line}\n"

    if DRY_RUN:
        print(f"  [DRY RUN] Would append to CHANGELOG.md:\n{entry}")
        return

    with open(CHANGELOG_PATH) as f:
        existing = f.read()

    with open(CHANGELOG_PATH, "w") as f:
        f.write(existing.rstrip() + "\n" + entry)


def write_summary(summary_lines, new_entities, known_entities):
    """Write the summary file for the GitHub Issue."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    content = f"# Excalidraw Lore Update Summary\n\n**Run:** {now}\n\n"

    if new_entities:
        content += "## New Entities (stub pages created)\n\n"
        for name, info in new_entities.items():
            content += f"- **{name}** → `{info['file']}` ({info['category']})\n"
        content += "\n"

    if known_entities:
        content += "## Known Entities Referenced\n\n"
        for name in sorted(known_entities):
            content += f"- [[{name}]]\n"
        content += "\n"

    content += "## Actions Taken\n\n"
    for line in summary_lines:
        content += f"- {line}\n"

    content += "\n---\n*Auto-generated by Part 2: Excalidraw Lore Update*\n"

    if not DRY_RUN:
        with open(SUMMARY_PATH, "w") as f:
            f.write(content)

    return content


def run_conversion_script():
    """Re-run the Obsidian conversion script to propagate new wikilinks."""
    print("\n  Re-running convert_to_obsidian.py...")
    if DRY_RUN:
        print("  [DRY RUN] Would re-run conversion script")
        return True
    try:
        result = subprocess.run(
            [sys.executable, CONVERT_SCRIPT],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            print("  Conversion script completed successfully")
            return True
        else:
            print(f"  WARNING: Conversion script failed:\n{result.stderr}")
            return False
    except Exception as e:
        print(f"  ERROR running conversion script: {e}")
        return False


def main():
    print("=" * 60)
    print("EXCALIDRAW LORE UPDATE (Part 2)")
    print("=" * 60)

    if DRY_RUN:
        print("[DRY RUN] No files will be modified\n")

    registry = load_registry()
    registry_names = set(registry.keys())

    alias_to_canonical = {}
    for canonical, info in registry.items():
        alias_to_canonical[canonical.lower()] = canonical
        for alias in info.get("aliases", []):
            alias_to_canonical[alias.lower()] = canonical

    transcriptions = find_new_transcriptions()
    if not transcriptions:
        print("No transcription files found")
        return

    print(f"Found {len(transcriptions)} transcription file(s)\n")

    all_wikilinks = set()
    new_entities = {}
    known_entities = set()
    summary_lines = []

    for t_path in transcriptions:
        rel = os.path.relpath(t_path, REPO_ROOT)
        print(f"  Processing: {rel}")

        frontmatter, body = read_transcription(t_path)
        source = frontmatter.get("source", rel)

        links = extract_wikilinks(body)
        print(f"    Found {len(links)} wikilink(s): {links}")

        for link_name in links:
            all_wikilinks.add(link_name)

            if link_name.lower() in alias_to_canonical:
                canonical = alias_to_canonical[link_name.lower()]
                known_entities.add(canonical)
                print(f"    [KNOWN] {link_name} -> {canonical}")
            elif link_name in registry_names:
                known_entities.add(link_name)
                print(f"    [KNOWN] {link_name}")
            else:
                context = get_context_for_entity(link_name, body)
                category = guess_category(link_name, context)
                print(f"    [NEW]   {link_name} (guessed: {category})")

                stub_file = create_stub_page(link_name, category, source, context)
                if stub_file:
                    new_entities[link_name] = {
                        "file": stub_file,
                        "category": category,
                    }
                    summary_lines.append(
                        f"Created stub: **{link_name}** -> `{stub_file}`"
                    )

    summary_lines.insert(0, f"Processed {len(transcriptions)} transcription(s)")
    summary_lines.append(f"Found {len(known_entities)} known entities")
    summary_lines.append(f"Created {len(new_entities)} new entity stubs")

    if new_entities:
        run_conversion_script()
        summary_lines.append("Re-ran vault conversion to propagate new wikilinks")

    update_changelog(summary_lines)
    summary_content = write_summary(summary_lines, new_entities, known_entities)

    print(f"\n{'=' * 60}")
    print(f"DONE:")
    print(f"  Transcriptions processed: {len(transcriptions)}")
    print(f"  Known entities found:     {len(known_entities)}")
    print(f"  New entity stubs created: {len(new_entities)}")
    print(f"{'=' * 60}")

    if new_entities:
        print("\nNew entity stubs (needs human review):")
        for name, info in new_entities.items():
            print(f"  - {name} -> {info['file']}")


if __name__ == "__main__":
    main()
