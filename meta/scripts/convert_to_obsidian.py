#!/usr/bin/env python3
"""
Convert Vumbua campaign wiki from Jekyll markdown to Obsidian vault format.

Operations:
1. Add YAML frontmatter with aliases and tags to entity pages
2. Convert markdown links [text](path.md) to [[wikilinks]]
3. Auto-link inline proper noun mentions (first occurrence per section)
4. Convert > [!CAUTION] blocks to collapsible > [!warning]- callouts
"""

import os
import re
import sys

DOCS_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

REGISTRY = {
    "Britt": {
        "file": "characters/player-characters/britt.md",
        "aliases": [],
        "tags": ["pc", "mizizi", "gold-rank"],
    },
    "Aggie": {
        "file": "characters/player-characters/aggie.md",
        "aliases": [],
        "tags": ["pc", "mizizi", "silver-rank"],
    },
    "Ignatius": {
        "file": "characters/player-characters/ignatius.md",
        "aliases": ["Lava Boy"],
        "tags": ["pc", "ash-blood", "silver-rank"],
    },
    "Lomi": {
        "file": "characters/player-characters/lomi.md",
        "aliases": ["Lomi Sultano"],
        "tags": ["pc", "harmony-born", "iron-union", "copper-rank"],
    },
    "Iggy": {
        "file": "characters/player-characters/iggy.md",
        "aliases": ["The Mole"],
        "tags": ["pc", "trench-kin", "gold-rank"],
    },
    "Dean Isolde Vane": {
        "file": "characters/npcs/dean-isolde-vane.md",
        "aliases": ["Dean Vane", "Isolde", "The Dean", "Dean Isolde"],
        "tags": ["npc", "faculty", "vane-lineage"],
    },
    "Celia Vance": {
        "file": "characters/npcs/celia-vance.md",
        "aliases": [],
        "tags": ["npc", "faculty"],
    },
    "Hesperus": {
        "file": "characters/npcs/hesperus.md",
        "aliases": ["Senior Exploranaut Hesperus"],
        "tags": ["npc", "faculty"],
    },
    "Ratchet": {
        "file": "characters/npcs/ratchet.md",
        "aliases": [],
        "tags": ["npc", "faculty"],
    },
    "Kojo": {
        "file": "characters/npcs/kojo.md",
        "aliases": [],
        "tags": ["npc", "faculty"],
    },
    "Pyrrhus": {
        "file": "characters/npcs/pyrrhus.md",
        "aliases": [],
        "tags": ["npc", "faculty", "ash-blood"],
    },
    "Professor Kante": {
        "file": "characters/npcs/professor-kante.md",
        "aliases": ["Kante"],
        "tags": ["npc", "faculty", "house-gilded"],
    },
    "Valerius Sterling": {
        "file": "characters/npcs/valerius-sterling.md",
        "aliases": ["Val", "Val Sterling"],
        "tags": ["npc", "squad-01", "gold-rank"],
    },
    "Serra Vox": {
        "file": "characters/npcs/serra-vox.md",
        "aliases": ["Serra", "Seraphina Vox"],
        "tags": ["npc", "squad-01", "gold-rank", "house-vox"],
    },
    "Cassius Thorne": {
        "file": "characters/npcs/cassius-thorne.md",
        "aliases": ["Cassius"],
        "tags": ["npc", "squad-01"],
    },
    "Iron-Jaw Jax": {
        "file": "characters/npcs/iron-jaw-jax.md",
        "aliases": ["Jax"],
        "tags": ["npc", "squad-02"],
    },
    "Maria Wall": {
        "file": "characters/npcs/maria-wall.md",
        "aliases": [],
        "tags": ["npc", "squad-02"],
    },
    "Brawn": {
        "file": "characters/npcs/brawn.md",
        "aliases": [],
        "tags": ["npc", "squad-02"],
    },
    "Nyx": {
        "file": "characters/npcs/nyx.md",
        "aliases": [],
        "tags": ["npc", "squad-03"],
    },
    "Kaelen": {
        "file": "characters/npcs/kaelen.md",
        "aliases": [],
        "tags": ["npc", "squad-03"],
    },
    "Mira": {
        "file": "characters/npcs/mira.md",
        "aliases": [],
        "tags": ["npc", "squad-03"],
    },
    "Calculus Prime": {
        "file": "characters/npcs/calculus-prime.md",
        "aliases": [],
        "tags": ["npc", "squad-04"],
    },
    "Theorem": {
        "file": "characters/npcs/theorem.md",
        "aliases": [],
        "tags": ["npc", "squad-04"],
    },
    "Lemma": {
        "file": "characters/npcs/lemma.md",
        "aliases": [],
        "tags": ["npc", "squad-04"],
    },
    "Dr. Rose Halloway": {
        "file": "characters/npcs/dr-rose-halloway.md",
        "aliases": ["Rose Halloway"],
        "tags": ["npc", "squad-05"],
    },
    "Silas Thorne": {
        "file": "characters/npcs/silas-thorne.md",
        "aliases": ["Old Man Thorne", "Silas"],
        "tags": ["npc", "squad-05"],
    },
    "Bramble": {
        "file": "characters/npcs/bramble.md",
        "aliases": [],
        "tags": ["npc", "squad-05"],
    },
    "Cinder-4": {
        "file": "characters/npcs/cinder-4.md",
        "aliases": ["Cinder"],
        "tags": ["npc", "squad-06", "ash-blood"],
    },
    "Hearth": {
        "file": "characters/npcs/hearth.md",
        "aliases": [],
        "tags": ["npc", "squad-06"],
    },
    "Kindle": {
        "file": "characters/npcs/kindle.md",
        "aliases": [],
        "tags": ["npc", "squad-06"],
    },
    "Captain Barnacle": {
        "file": "characters/npcs/captain-barnacle.md",
        "aliases": ["Barnacle"],
        "tags": ["npc", "squad-07"],
    },
    "Pressure": {
        "file": "characters/npcs/pressure.md",
        "aliases": [],
        "tags": ["npc", "squad-07"],
    },
    "Depth": {
        "file": "characters/npcs/depth.md",
        "aliases": [],
        "tags": ["npc", "squad-07"],
    },
    "Percival Vane-Smythe III": {
        "file": "characters/npcs/percival-vane-smythe-iii.md",
        "aliases": ["Percy", "Percival", "Percy Vane-Smythe III"],
        "tags": ["npc", "squad-08"],
    },
    "Lady Glimmer": {
        "file": "characters/npcs/lady-glimmer.md",
        "aliases": ["Glimmer"],
        "tags": ["npc", "squad-08"],
    },
    "Baron Bolt": {
        "file": "characters/npcs/baron-bolt.md",
        "aliases": ["Bolt"],
        "tags": ["npc", "squad-08"],
    },
    "Sarge": {
        "file": "characters/npcs/sarge.md",
        "aliases": [],
        "tags": ["npc", "squad-09", "rust-rank"],
    },
    "Lucky": {
        "file": "characters/npcs/lucky.md",
        "aliases": [],
        "tags": ["npc", "squad-09"],
    },
    "Pudge": {
        "file": "characters/npcs/pudge.md",
        "aliases": [],
        "tags": ["npc", "squad-09"],
    },
    "Lady Ignis": {
        "file": "characters/npcs/lady-ignis.md",
        "aliases": ["Ignis"],
        "tags": ["npc", "ash-blood", "harmony-council"],
    },
    "Rill": {
        "file": "characters/npcs/rill.md",
        "aliases": ["Real", "The River-Born"],
        "tags": ["npc", "wadi", "faculty"],
    },
    "Zephyr": {
        "file": "characters/npcs/zephyr.md",
        "aliases": ["Lightning Girl"],
        "tags": ["npc", "renali", "fulgur-born"],
    },
    "Lance": {
        "file": "characters/npcs/lance.md",
        "aliases": [],
        "tags": ["npc"],
    },
    "Valerius Sterling Sr.": {
        "file": "characters/npcs/valerius-sterling-sr.md",
        "aliases": ["Sterling Sr.", "The Paper Man"],
        "tags": ["npc", "explorer"],
    },
    "Lady Glissade": {
        "file": "characters/npcs/lady-glissade.md",
        "aliases": ["Glissade"],
        "tags": ["npc"],
    },
    "Ember": {
        "file": "characters/npcs/ember.md",
        "aliases": [],
        "tags": ["npc", "ash-blood"],
    },
    "Tommy": {
        "file": "characters/npcs/tommy.md",
        "aliases": [],
        "tags": ["npc"],
    },
    "Lucina": {
        "file": "characters/npcs/lucina.md",
        "aliases": [],
        "tags": ["npc"],
    },
    "Marla": {
        "file": "characters/npcs/marla.md",
        "aliases": [],
        "tags": ["npc"],
    },
    "Soot": {
        "file": "characters/npcs/soot.md",
        "aliases": [],
        "tags": ["npc", "rust-rank"],
    },
    "Mizizi": {
        "file": "factions/clans/mizizi.md",
        "aliases": ["Root-Kin", "Deep-Root Clan", "Mycelium Clan"],
        "tags": ["faction", "clan"],
    },
    "Ash-Bloods": {
        "file": "factions/clans/ash-bloods.md",
        "aliases": ["Ember-Kin", "Pyre-Keepers", "Ash Bloods", "Ash Blood"],
        "tags": ["faction", "clan"],
    },
    "Trench-Kin": {
        "file": "factions/clans/trench-kin.md",
        "aliases": ["Earthkin"],
        "tags": ["faction", "clan"],
    },
    "Renali": {
        "file": "factions/clans/renali.md",
        "aliases": ["Air Clan", "Cloud-Kin"],
        "tags": ["faction", "clan"],
    },
    "Wadi": {
        "file": "factions/clans/wadi.md",
        "aliases": ["River Clan", "Dry Vein"],
        "tags": ["faction", "clan"],
    },
    "Fulgur-Born": {
        "file": "factions/clans/fulgur-born.md",
        "aliases": ["Storm-Chasers"],
        "tags": ["faction", "clan"],
    },
    "House Gilded": {
        "file": "factions/harmony/house-gilded.md",
        "aliases": ["The Highborne", "The Vault"],
        "tags": ["faction", "harmony-house"],
    },
    "Vane Lineage": {
        "file": "factions/harmony/vane-lineage.md",
        "aliases": ["House Vane", "The Shield", "The Orderborne"],
        "tags": ["faction", "harmony-house"],
    },
    "Scrivener Guild": {
        "file": "factions/harmony/scrivener-guild.md",
        "aliases": ["The Loreborne"],
        "tags": ["faction", "harmony-house"],
    },
    "Iron-Union": {
        "file": "factions/harmony/iron-union.md",
        "aliases": ["The Ridgeborne", "Iron Union", "Diamond Union"],
        "tags": ["faction", "harmony-house"],
    },
    "The Verdant Trust": {
        "file": "factions/harmony/verdant-trust.md",
        "aliases": ["Verdant Trust", "The Agri-Lords"],
        "tags": ["faction", "harmony-house"],
    },
    "High-Justiciars": {
        "file": "factions/harmony/high-justiciars.md",
        "aliases": ["The Scales"],
        "tags": ["faction", "harmony-house"],
    },
    "Grand Architects": {
        "file": "factions/harmony/grand-architects.md",
        "aliases": ["House Mason"],
        "tags": ["faction", "harmony-house"],
    },
    "Syndicate of Sails": {
        "file": "factions/harmony/syndicate-of-sails.md",
        "aliases": [],
        "tags": ["faction", "harmony-house"],
    },
    "Vumbua Academy": {
        "file": "locations/vumbua-academy.md",
        "aliases": ["Vumbua", "The Safiri"],
        "tags": ["location"],
    },
    "The Bleed": {
        "file": "world/the-bleed.md",
        "aliases": ["Dissolution"],
        "tags": ["world-lore"],
    },
    "The Minimum": {
        "file": "world/the-minimum.md",
        "aliases": [],
        "tags": ["world-lore", "gm-only"],
    },
    "The Power System": {
        "file": "world/power-system.md",
        "aliases": ["Power System", "Global Amplitude"],
        "tags": ["world-lore"],
    },
    "Harmony Nodes": {
        "file": "world/harmony-nodes.md",
        "aliases": ["Harmony's Integrated Nodes"],
        "tags": ["world-lore"],
    },
    "Pre-Stitch Artifacts": {
        "file": "world/pre-stitch-artifacts.md",
        "aliases": [],
        "tags": ["world-lore"],
    },
    "Ether-Jelly": {
        "file": "bestiary/ether-jelly.md",
        "aliases": [],
        "tags": ["creature"],
    },
    "Void-Beast": {
        "file": "bestiary/void-beast.md",
        "aliases": [],
        "tags": ["creature"],
    },
    "Rot-Shepherd": {
        "file": "bestiary/rot-shepherd.md",
        "aliases": [],
        "tags": ["creature"],
    },
    "Whispering Moth": {
        "file": "bestiary/whispering-moth.md",
        "aliases": [],
        "tags": ["creature"],
    },
}

# ============================================================
# BUILD LOOKUPS
# ============================================================

FILENAME_TO_CANONICAL = {}
FILEPATH_TO_CANONICAL = {}

for canonical, info in REGISTRY.items():
    fpath = info["file"]
    FILEPATH_TO_CANONICAL[fpath] = canonical
    fname = os.path.basename(fpath).replace(".md", "")
    if fname not in FILENAME_TO_CANONICAL:
        FILENAME_TO_CANONICAL[fname] = canonical

ALIAS_TO_CANONICAL = {}
for canonical, info in REGISTRY.items():
    ALIAS_TO_CANONICAL[canonical] = canonical
    for alias in info["aliases"]:
        ALIAS_TO_CANONICAL[alias] = canonical

SORTED_NAMES = sorted(ALIAS_TO_CANONICAL.keys(), key=len, reverse=True)

SKIP_AUTOLINK = {
    "Wall", "Bolt", "Real", "Depth", "Pressure", "Cinder",
    "Glimmer", "Val", "Soot", "Vumbua", "The Safiri",
    "The Vault", "The Shield", "The Scales",
    "Dissolution", "Ignis", "Serra", "Cassius", "Silas",
    "Isolde", "Percival", "Kante", "Glissade",
}

# ============================================================
# FRONTMATTER
# ============================================================

def strip_existing_frontmatter(content):
    if content.startswith("---\n"):
        end_idx = content.find("\n---\n", 4)
        if end_idx != -1:
            return content[end_idx + 5:].lstrip("\n")
    return content

def build_frontmatter(canonical, info):
    lines = ["---"]
    if info["aliases"]:
        lines.append("aliases:")
        for a in info["aliases"]:
            lines.append(f'  - "{a}"')
    if info["tags"]:
        lines.append("tags:")
        for t in info["tags"]:
            lines.append(f"  - {t}")
    lines.append("---")
    return "\n".join(lines) + "\n"

def add_frontmatter(filepath, canonical, info):
    with open(filepath, "r") as f:
        content = f.read()
    body = strip_existing_frontmatter(content)
    fm = build_frontmatter(canonical, info)
    with open(filepath, "w") as f:
        f.write(fm + "\n" + body)
    return True

# ============================================================
# LINK RESOLUTION
# ============================================================

def normalize_link_path(raw_path, current_file_rel):
    if raw_path.startswith("/"):
        resolved = raw_path.lstrip("/")
    else:
        current_dir = os.path.dirname(current_file_rel)
        resolved = os.path.normpath(os.path.join(current_dir, raw_path))

    if not resolved.endswith(".md"):
        resolved += ".md"

    return resolved

def resolve_to_canonical(raw_path, current_file_rel):
    resolved = normalize_link_path(raw_path, current_file_rel)

    if resolved in FILEPATH_TO_CANONICAL:
        return FILEPATH_TO_CANONICAL[resolved]

    fname = os.path.basename(resolved).replace(".md", "")
    if fname in FILENAME_TO_CANONICAL:
        return FILENAME_TO_CANONICAL[fname]


    return None

# ============================================================
# LINK CONVERSION
# ============================================================

def convert_markdown_links(content, current_file_rel):
    def replace_link(match):
        full_match = match.group(0)
        display = match.group(1)
        path = match.group(2)

        if path.startswith(("http://", "https://", "mailto:", "#")):
            return full_match

        anchor = ""
        if "#" in path:
            path, anchor = path.split("#", 1)

        canonical = resolve_to_canonical(path, current_file_rel)

        if canonical:
            clean_display = display.strip().strip("*")
            all_names = [canonical] + REGISTRY.get(canonical, {}).get("aliases", [])

            if anchor:
                return f"[[{canonical}#{anchor}|{display}]]"

            if clean_display in all_names:
                return f"[[{canonical}]]"
            else:
                return f"[[{canonical}|{display}]]"
        else:
            basename = os.path.basename(path).replace(".md", "")
            if not basename or basename == "index":
                return full_match

            title = basename.replace("-", " ").title()

            if anchor:
                return f"[[{title}#{anchor}|{display}]]"

            clean_display = display.strip().strip("*")
            if clean_display.lower() == title.lower():
                return f"[[{title}]]"
            else:
                return f"[[{title}|{display}]]"

    pattern = r'(?<!!)\[([^\[\]]+)\]\(([^)]+)\)'
    return re.sub(pattern, replace_link, content)

# ============================================================
# AUTO-LINK PROPER NOUNS
# ============================================================

def is_inside_link(line, pos, name_len):
    before = line[:pos]
    after = line[pos + name_len:]

    last_open = before.rfind("[[")
    last_close = before.rfind("]]")
    if last_open > last_close:
        return True

    last_bracket_open = before.rfind("[")
    last_bracket_close = before.rfind("]")
    if last_bracket_open > last_bracket_close:
        return True

    if before.endswith("|"):
        return True

    return False

def autolink_line(line, linked_in_section, self_names):
    if not line.strip():
        return line
    if line.startswith(("#", "---", "```", "aliases:", "tags:", "  - ")):
        return line
    if line.startswith("**Aliases:**") or line.startswith("**Role:**"):
        return line
    # Skip table rows (contain proper nouns as display text already)
    if line.strip().startswith("|"):
        return line

    for name in SORTED_NAMES:
        if name in self_names:
            continue
        if name in SKIP_AUTOLINK:
            continue
        if name in linked_in_section:
            continue

        canonical = ALIAS_TO_CANONICAL[name]

        pattern = r'\b' + re.escape(name) + r'\b'
        match = re.search(pattern, line)
        if not match:
            continue

        pos = match.start()
        if is_inside_link(line, pos, len(name)):
            continue

        # Check if surrounded by ** (bold) - wrap the wikilink in bold
        before_chunk = line[:pos]
        after_chunk = line[pos + len(name):]

        if before_chunk.endswith("**") and after_chunk.startswith("**"):
            bold_start = len(before_chunk) - 2
            bold_end = pos + len(name)
            if name == canonical:
                replacement = f"**[[{canonical}]]**"
            else:
                replacement = f"**[[{canonical}|{name}]]**"
            line = line[:bold_start] + replacement + line[bold_end + 2:]
            linked_in_section.add(name)
            continue

        if name == canonical:
            wikilink = f"[[{canonical}]]"
        else:
            wikilink = f"[[{canonical}|{name}]]"

        line = line[:pos] + wikilink + line[pos + len(name):]
        linked_in_section.add(name)

    return line

def autolink_proper_nouns(content, filepath_rel):
    self_canonical = FILEPATH_TO_CANONICAL.get(filepath_rel)
    self_names = set()
    if self_canonical:
        self_names.add(self_canonical)
        self_names.update(REGISTRY[self_canonical].get("aliases", []))

    lines = content.split("\n")
    result = []
    linked_in_section = set()
    in_frontmatter = False
    in_code_block = False
    fm_count = 0

    for line in lines:
        if line.strip() == "---":
            fm_count += 1
            if fm_count <= 2:
                in_frontmatter = fm_count == 1
                if fm_count == 2:
                    in_frontmatter = False
            result.append(line)
            continue

        if in_frontmatter:
            result.append(line)
            continue

        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_code_block:
            result.append(line)
            continue

        if line.startswith("## "):
            linked_in_section = set()

        line = autolink_line(line, linked_in_section, self_names)
        result.append(line)

    return "\n".join(result)

# ============================================================
# CALLOUT CONVERSION
# ============================================================

def convert_callouts(content):
    content = re.sub(
        r'> \[!CAUTION\]\s*\n',
        '> [!warning]-\n',
        content
    )
    return content

# ============================================================
# MAIN PROCESSING
# ============================================================

def get_rel_path(filepath):
    return os.path.relpath(filepath, DOCS_DIR)

def process_file(filepath):
    rel_path = get_rel_path(filepath)

    with open(filepath, "r") as f:
        content = f.read()

    original = content

    content = convert_markdown_links(content, rel_path)
    content = autolink_proper_nouns(content, rel_path)
    content = convert_callouts(content)

    if content != original:
        with open(filepath, "w") as f:
            f.write(content)
        return True
    return False

SKIP_DIRS = {
    "notebooklm", ".obsidian", ".git", ".trash", "node_modules",
    "Daggerheart-Core", "Vumbua", "exports", "lore-dump", "Ink",
    "docs", "meta",
}

def collect_all_md_files():
    files = []
    for root, dirs, filenames in os.walk(DOCS_DIR):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        if any(s in root for s in SKIP_DIRS):
            continue
        for f in filenames:
            if f.endswith(".md") and f != "_template.md":
                if f.endswith(".excalidraw.md"):
                    continue
                files.append(os.path.join(root, f))
    return sorted(files)

def main():
    print("=" * 60)
    print("VUMBUA OBSIDIAN VAULT CONVERSION")
    print("=" * 60)

    print("\n--- Step 1: Adding YAML frontmatter ---")
    fm_count = 0
    fm_skip = 0
    for canonical, info in REGISTRY.items():
        filepath = os.path.join(DOCS_DIR, info["file"])
        if os.path.exists(filepath):
            add_frontmatter(filepath, canonical, info)
            fm_count += 1
            print(f"  [FM] {info['file']}")
        else:
            fm_skip += 1
            print(f"  [SKIP] {info['file']} (not found)")
    print(f"  Frontmatter added: {fm_count}, skipped: {fm_skip}")

    print("\n--- Steps 2-4: Links, auto-linking, callouts ---")
    all_files = collect_all_md_files()
    changed = 0
    unchanged = 0

    for filepath in all_files:
        rel = get_rel_path(filepath)
        if process_file(filepath):
            changed += 1
            print(f"  [CHANGED] {rel}")
        else:
            unchanged += 1
            print(f"  [OK] {rel}")

    print(f"\n  Changed: {changed}, Unchanged: {unchanged}")
    print(f"\n{'=' * 60}")
    print(f"DONE: {fm_count} frontmatter + {changed} content files modified")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()
