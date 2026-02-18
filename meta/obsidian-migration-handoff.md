# Obsidian Vault Migration -- Handoff Document

> **Author:** Devin (AI), requested by Luke S
> **Date:** February 2026
> **Purpose:** Complete specification for converting the Vumbua campaign wiki from Jekyll/GitHub Pages into a fully interactive Obsidian vault with linked proper nouns, search, AI chat, and multi-device sync.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Current State](#2-current-state)
3. [Target State (The Vision)](#3-target-state-the-vision)
4. [Conversion Specification](#4-conversion-specification)
5. [Obsidian Setup Instructions](#5-obsidian-setup-instructions)
6. [Community Plugins](#6-community-plugins)
7. [AI Integration](#7-ai-integration)
8. [Git Workflow & Excalidraw OCR](#8-git-workflow--excalidraw-ocr)
9. [Multi-Device Sync](#9-multi-device-sync)
10. [Maintenance & Future AI Workflows](#10-maintenance--future-ai-workflows)
11. [Migration Checklist](#11-migration-checklist)

---

## 1. Project Overview

**Vumbua** is a Daggerheart TTRPG campaign wiki. The content lives in a GitHub repo (`ldstrebel/vumbua`) as markdown files, currently served as a static Jekyll site via GitHub Pages + Netlify.

**The goal:** Convert this into an Obsidian vault so that:
- Every proper noun (character, faction, location, term) is a clickable wikilink
- Clicking a name shows its definition in a hover preview or side panel
- Full-text search works across all content
- Content can be edited in real time
- An AI assistant can read the vault and act as an informed writing partner
- Works across all devices (phone, tablet, laptop)

---

## 2. Current State

### Content Inventory

| Category | Count | Location |
|----------|-------|----------|
| Markdown files (docs/) | 104 | `docs/` |
| NPC profiles | 44 | `docs/lore/characters/npcs/` |
| PC profiles | 5 | `docs/characters/player-characters/` |
| Faction/clan pages | 14 | `docs/lore/factions/` |
| World lore pages | 6 | `docs/lore/world/` |
| Bestiary entries | 5 | `docs/lore/bestiary/` |
| Location pages | 2 | `docs/lore/locations/` |
| Session transcripts | 7 | `docs/sessions/transcripts/` |
| Glossary | 1 (~358 lines, ~60 terms) | `docs/lore/glossary.md` |
| Timeline | 1 | `docs/lore/timeline.md` |
| NotebookLM exports | 4 | `docs/notebooklm/` |
| AI workflow docs | 7 | `.agent/workflows/` |

### Current Link Format

Files use **standard markdown links** with relative paths:
```markdown
[[Ash-Bloods]]
[[The Bleed]]
[[Britt]]
```

### Existing Metadata

- **No YAML frontmatter** on most files (only a few session transcripts and workflow files have it)
- **Aliases** are written inline in NPC profiles as plain text, e.g.:
  ```
  **Aliases:** Lightning Girl (Ignatius's nickname)
  **Aliases:** Real, Rill, The River-Born
  **Aliases:** Serra Vox, Serra
  ```
- **Canonical spellings** and common transcription errors are tracked in `.agent/workflows/lore-index.md`

### Current Tech Stack

- Jekyll 4.3 with Cayman theme
- GitHub Pages + Netlify deployment
- Ruby Gemfile (`docs/Gemfile`)
- Netlify config (`netlify.toml`)

---

## 3. Target State (The Vision)

### Must-Have

1. **Wikilinks everywhere** -- Every proper noun is a `[[wikilink]]` that resolves to its page
2. **Hover preview** -- Hovering/clicking a link shows the definition without leaving the current page
3. **Alias support** -- `[[Rill]]` also matches "Real", "[[Rill|The River-Born]]"; `[[Seraphina "Serra" Vox]]` matches "Serra", "[[Serra Vox]]"
4. **Full-text search** -- Instant search across all 104+ files
5. **Graph view** -- Visual map of how entities connect
6. **Live editing** -- Edit any page in place, changes persist immediately
7. **Multi-device** -- Works on Mac, Windows, iOS, Android

### Nice-to-Have

8. **AI chat** -- Ask questions about the lore from within Obsidian
9. **Excalidraw drawings** -- Visual maps, relationship diagrams, battle maps
10. **Backlinks panel** -- See every page that mentions a given entity
11. **GM-only content toggle** -- Ability to hide/show spoiler content

---

## 4. Conversion Specification

### 4.1 Add YAML Frontmatter to All Entity Pages

Every character, faction, location, bestiary, and glossary-term page needs frontmatter with `aliases` so that Obsidian's wikilink resolution works across alternate names.

**Format:**
```yaml
---
aliases:
  - Serra
  - Serra Vox
tags:
  - npc
  - squad-01
  - gold-rank
---
```

**Alias sources** (merge all of these):
1. The `**Aliases:**` line in each NPC/PC file
2. The "Common Errors" column in `.agent/workflows/lore-index.md` (canonical spellings table)
3. Known nicknames from session transcripts (e.g., "[[Ignatius|Lava Boy]]" for [[Ignatius]], "[[Zephyr|Lightning Girl]]" for Zephyr)
4. Faction alternate names from the glossary (e.g., [[Mizizi]] = "[[Mizizi|Root-Kin]]" = "[[Mizizi|Deep-Root Clan]]" = "[[Mizizi|Mycelium Clan]]")

**Tag taxonomy** (suggested):
- `pc`, `npc`, `faction`, `clan`, `harmony-house`, `location`, `creature`, `world-lore`, `session`, `mechanic`
- Squad tags: `squad-01` through `squad-09`
- Rank tags: `gold-rank`, `silver-rank`, `copper-rank`, `rust-rank`
- Secrecy tags: `gm-only`, `player-facing`

### 4.2 Convert Markdown Links to Wikilinks

Replace all `[[Path|Display Text]]` with `[[Page Name]]` or `[[Page Name|Display Text]]`.

**Rules:**
1. Match link targets to the actual `# H1 heading` or filename of the destination file
2. Obsidian resolves by filename, so `[[rill]]` finds `rill.md` regardless of folder depth
3. If the display text differs from the page name, use pipe syntax: `[[rill|Rill the River-Born]]`
4. Absolute paths like `/lore/factions/clans/ash-bloods.md` become `[[Ash-Bloods]]`
5. Relative paths like `player-characters/britt.md` become `[[Britt]]`
6. Index pages that are primarily link lists (`index.md` files) should use `[[Page Name]]` format for each bullet

**Example conversions:**
```markdown
# Before (Jekyll markdown)
| **Clan** | [[Ash-Bloods]] |
- **[[Britt]]** - Mizizi (Gray fungal-turtle) - Gold Rank
- [[The Bleed]] - Where reality dissolves

# After (Obsidian wikilinks)
| **Clan** | [[Ash-Bloods]] |
- **[[Britt]]** - Mizizi (Gray fungal-turtle) - Gold Rank
- [[The Bleed]] - Where reality dissolves
```

### 4.3 Convert Inline Proper Noun Mentions to Wikilinks

Scan all files for mentions of proper nouns that are NOT already links and wrap them in `[[wikilinks]]`.

**Proper noun registry** (build from these sources):
- All filenames in `docs/lore/characters/npcs/` (44 NPCs)
- All filenames in `docs/characters/player-characters/` (5 PCs)
- All entries in `docs/lore/glossary.md` (bold terms)
- All faction/clan names from `docs/lore/factions/`
- All location names from `docs/lore/locations/`
- All bestiary entries from `docs/lore/bestiary/`
- All aliases defined in frontmatter (after step 4.1)

**Rules:**
1. Only link the **first occurrence** of each proper noun per section (under each `##` heading) to avoid link spam
2. Do NOT link proper nouns inside their own page's H1 heading or the `**Aliases:**` line
3. Do NOT link inside code blocks or YAML frontmatter
4. Match case-insensitively but preserve original casing in display
5. Match aliases: if "Real" appears and [[Rill]]'s aliases include "Real", link it as `[[Rill|Real]]`
6. Do NOT link common English words that happen to match (e.g., "Depth" the squad member vs. "depth" the word -- use context/capitalization)

### 4.4 Restructure Folder Layout for Obsidian

Keep the existing folder structure mostly intact. Obsidian doesn't care about folder depth for link resolution, but a clean structure helps navigation.

**Proposed vault root:** The `docs/` folder becomes the Obsidian vault root.

```
docs/                          <-- Vault root (open this folder in Obsidian)
├── .obsidian/                 <-- Obsidian config (new)
├── _templates/                <-- Note templates (new, migrated from _template.md)
├── index.md                   <-- Campaign homepage (rename to "Home.md" or keep)
├── characters/
│   ├── player-characters/
│   └── index.md
├── sessions/
│   ├── transcripts/
│   └── planning/
├── lore/
│   ├── glossary.md
│   ├── timeline.md
│   ├── knowledge-tracker.md
│   ├── characters/npcs/       <-- 44 NPC files
│   ├── factions/
│   ├── world/
│   ├── locations/
│   └── bestiary/
├── notebooklm/                <-- Keep for export compatibility
├── maps/                      <-- New: for Excalidraw drawings
└── ai-reference/              <-- New: AI-optimized context files
    └── lore-index.md          <-- Migrated from .agent/workflows/
```

**Changes from current structure:**
- Add `.obsidian/` config folder
- Add `_templates/` for Obsidian templates
- Add `maps/` for Excalidraw files
- Move `lore-index.md` into the vault (currently in `.agent/workflows/` which is outside `docs/`)
- Remove or ignore Jekyll-specific files: `_config.yml`, `Gemfile`

### 4.5 Handle the Glossary

The glossary (`docs/lore/glossary.md`) is currently a single 358-line file with ~60 defined terms. Two options:

**Option A (Recommended): Keep as single file, add wikilinks**
- Add wikilinks to terms that have their own pages (e.g., `**[[Rill]]** ([[Rill|The River-Born]])`)
- Terms without dedicated pages stay as glossary entries
- Advantage: single file is easy to search and scroll

**Option B: Explode into individual notes**
- Each glossary term becomes its own note in `lore/glossary/`
- Advantage: each term gets its own backlinks and graph node
- Disadvantage: 60+ tiny files, harder to browse

### 4.6 Handle GM-Only Content

Currently marked with `> [!CAUTION]` blockquotes and `[GM ONLY]` tags.

**In Obsidian:**
- Use the `> [!warning]` callout syntax (Obsidian renders these as collapsible callouts)
- These are **collapsed by default**, so GM secrets are hidden until clicked
- Add `gm-only` tag to pages that contain secrets

```markdown
> [!warning]- GM ONLY: The Minimum
> Power threshold below which Harmony tech fails.
> When crossed, lights and medical devices lose charge.
```

The `-` after `[!warning]` makes it collapsed by default.

---

## 5. Obsidian Setup Instructions

### 5.1 Install Obsidian

1. Download from [obsidian.md](https://obsidian.md/) (free for personal use)
2. Install on all devices you want to use (Mac, Windows, iOS, Android)

### 5.2 Open the Vault

1. Clone the repo: `git clone https://github.com/ldstrebel/vumbua.git`
2. Open Obsidian
3. Click "Open folder as vault"
4. Select the `docs/` folder inside the cloned repo
5. When prompted about community plugins, click "Trust author and enable plugins"

### 5.3 Core Settings (Settings > Editor)

| Setting | Value | Why |
|---------|-------|-----|
| Default editing mode | Live Preview | See rendered markdown while editing |
| Readable line length | ON | Prevents ultra-wide lines on big screens |
| Strict line breaks | OFF | Matches how the markdown was written |
| Auto-convert HTML | ON | Handles any residual HTML from Jekyll |
| Fold heading | ON | Collapse long sections |
| Fold indent | ON | Collapse nested lists |

### 5.4 Core Settings (Settings > Files & Links)

| Setting | Value | Why |
|---------|-------|-----|
| New link format | Shortest path when possible | Cleaner wikilinks |
| Use [[Wikilinks]] | ON | Enable `[[wikilink]]` syntax |
| Default location for new notes | Same folder as current file | Keeps related content together |
| Default location for attachments | In subfolder: `attachments` | Keeps images organized |
| Detect all file extensions | ON | Needed for Excalidraw files |

---

## 6. Community Plugins

Enable community plugins: Settings > Community Plugins > Turn on community plugins.

### 6.1 Essential Plugins

| Plugin | Purpose | Config Notes |
|--------|---------|--------------|
| **Excalidraw** | Visual maps, relationship diagrams, battle maps | See Section 8 for Git/OCR workflow |
| **Obsidian Copilot** | AI chat with your vault (uses your OpenAI/Google API key) | See Section 7 |
| **Templater** | Advanced templates for new session notes, NPC profiles | Point to `_templates/` folder |
| **Dataview** | Query your vault like a database (e.g., "show all NPCs tagged gold-rank") | Enables dynamic indexes |
| **Hover Editor** | Edit a linked note in a floating window without leaving the current page | This is the "side panel" editing experience |

### 6.2 Recommended Plugins

| Plugin | Purpose | Config Notes |
|--------|---------|--------------|
| **Calendar** | Visual calendar tied to session dates | Link daily notes to session dates |
| **Graph Analysis** | Enhanced graph view with clustering | Groups characters by faction/squad |
| **Tag Wrangler** | Rename/merge tags across the vault | Useful for maintaining tag taxonomy |
| **Obsidian Git** | Auto-commit and push/pull from within Obsidian | See Section 8 |
| **Style Settings** | Customize theme appearance | Pairs with themes below |
| **Quick Switcher++** | Enhanced search that searches aliases and tags | Better than default switcher |
| **Breadcrumbs** | Shows hierarchical navigation (Lore > Factions > Clans > Mizizi) | Set up hierarchy via frontmatter |
| **Various Complements** | Auto-complete proper nouns as you type | Reduces typos; learns from vault content |

### 6.3 Optional But Cool

| Plugin | Purpose |
|--------|---------|
| **Dice Roller** | Roll dice directly in notes (for Daggerheart mechanics) |
| **Initiative Tracker** | Combat initiative tracking |
| **Kanban** | Visual board for plot threads / session planning |
| **Mind Map** | Generate mind maps from note structure |
| **Strange New Worlds** | Shows how many other notes link to a given phrase inline |

### 6.4 Recommended Theme

**ITS Theme** or **Minimal Theme** -- both support callout customization (important for GM-only sections) and have excellent readability.

---

## 7. AI Integration

### 7.1 Obsidian Copilot Plugin

The **Obsidian Copilot** plugin lets you chat with an AI that has your vault as context.

**Setup:**
1. Install "Copilot" from community plugins
2. Settings > Copilot > Set your API key:
   - OpenAI: Paste your OpenAI API key, select `gpt-4o` model
   - Google: Paste your Google AI API key, select `gemini-2.0-flash` or `gemini-2.0-pro`
3. Enable "Index vault for QA" -- this creates embeddings of your notes for RAG
4. Set embedding model (OpenAI `text-embedding-3-small` or Google equivalent)

**Usage:**
- Open the Copilot side panel (ribbon icon or hotkey)
- Ask questions: "What does [[Ignatius]] know about the power crisis?"
- It retrieves relevant notes and answers with citations
- You can ask it to draft new content, summarize sessions, or brainstorm plot threads

**Cost estimate:** ~$0.01-0.05 per conversation turn (RAG retrieval + completion).

### 7.2 AI + Git Workflow (External AI like Devin/ChatGPT)

For heavier AI work (processing full session transcripts, bulk lore updates), the existing `.agent/workflows/` system still works:

1. AI reads the repo via Git
2. AI processes content using the workflow instructions
3. AI commits changes to a branch
4. You pull into your Obsidian vault (via Obsidian Git plugin or manual `git pull`)
5. Changes appear instantly in Obsidian

**The `ai-reference/lore-index.md` file** should be kept updated as the master AI context file. Any external AI should read this file first for canonical spellings, character mappings, and plot thread status.

### 7.3 Keeping AI Context Current

After each session:
1. Process the transcript (via Devin or manual AI workflow)
2. Updated files land in the vault via Git
3. Obsidian Copilot re-indexes automatically (or trigger manual re-index)
4. The AI now knows the latest session content

---

## 8. Git Workflow & Excalidraw OCR

### 8.1 Obsidian Git Plugin Setup

1. Install "Obsidian Git" from community plugins
2. Settings:
   - Auto pull interval: 10 minutes (or on startup)
   - Auto push after commit: ON
   - Pull on startup: ON
   - Commit message format: `vault: {{date}}`
3. The vault syncs with GitHub automatically

### 8.2 Excalidraw in Git

**The problem:** Excalidraw files (`.excalidraw.md` in Obsidian) contain JSON drawing data. These are:
- Not human-readable in diffs
- Large binary-like blobs in Git
- Cannot be searched as text
- Embedded text (labels, annotations) is invisible to search and AI

**The solution: A two-stage pipeline — automated text/OCR extraction on push, then AI review for linking.**

### Stage 1: Automated Text + OCR Extraction (GitHub Action)

Runs on every push, but only processes **new or modified** drawings. Uses a manifest file to track what's already been extracted, saving time and tokens.

**What gets extracted:**
1. **Text elements** — typed labels, annotations, titles inside the Excalidraw JSON
2. **Embedded images** — any imported screenshots, photos, hand-drawn sketches get OCR'd via Tesseract (free, open-source) so handwriting and image text become searchable
3. **Embedded note references** — any `[[wikilinks]]` used inside the drawing
4. **Freehand text** — Excalidraw's "text-to-diagram" labels

```yaml
# .github/workflows/excalidraw-extract.yml
name: Excalidraw Text + OCR Extraction

on:
  push:
    paths:
      - 'docs/maps/**/*.excalidraw.md'
      - 'docs/maps/**/*.png'
      - 'docs/maps/**/*.jpg'

jobs:
  extract:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2  # Need parent commit to detect changes

      - name: Install dependencies
        run: |
          sudo apt-get update -qq
          sudo apt-get install -y tesseract-ocr python3-pip
          pip3 install Pillow pytesseract

      - name: Extract text from changed Excalidraw files only
        run: |
          # Load manifest of already-processed files + their hashes
          MANIFEST="docs/maps/.extraction-manifest.json"
          if [ ! -f "$MANIFEST" ]; then
            echo '{}' > "$MANIFEST"
          fi

          python3 << 'EXTRACT_SCRIPT'
          import json, hashlib, os, re, glob, subprocess

          MANIFEST_PATH = "docs/maps/.extraction-manifest.json"
          MAPS_DIR = "docs/maps"

          with open(MANIFEST_PATH) as f:
              manifest = json.load(f)

          changed = False

          for filepath in glob.glob(f"{MAPS_DIR}/**/*.excalidraw.md", recursive=True):
              # Hash the file to check if it's changed since last extraction
              with open(filepath, "rb") as f:
                  file_hash = hashlib.sha256(f.read()).hexdigest()

              if manifest.get(filepath) == file_hash:
                  print(f"SKIP (unchanged): {filepath}")
                  continue

              print(f"PROCESSING: {filepath}")
              changed = True

              with open(filepath) as f:
                  content = f.read()

              output_lines = []
              wikilinks = []

              # 1. Extract typed text elements from Excalidraw JSON
              json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
              if json_match:
                  try:
                      data = json.loads(json_match.group(1))
                      elements = data.get("elements", [])
                      for el in elements:
                          if el.get("type") == "text" and el.get("text", "").strip():
                              text = el["text"].strip()
                              output_lines.append(text)
                              # Find wikilinks within text elements
                              wikilinks.extend(re.findall(r'\[\[([^\]]+)\]\]', text))
                  except json.JSONDecodeError:
                      output_lines.append("[ERROR: Could not parse Excalidraw JSON]")

              # 2. OCR any embedded images (base64 data URIs in the JSON)
              if json_match:
                  try:
                      data = json.loads(json_match.group(1))
                      files_data = data.get("files", {})
                      for file_id, file_info in files_data.items():
                          if file_info.get("mimeType", "").startswith("image/"):
                              # Decode base64 image and OCR it
                              import base64
                              from PIL import Image
                              from io import BytesIO
                              import pytesseract

                              img_data = base64.b64decode(file_info.get("dataURL", "").split(",")[-1])
                              img = Image.open(BytesIO(img_data))
                              ocr_text = pytesseract.image_to_string(img).strip()
                              if ocr_text:
                                  output_lines.append(f"[OCR from embedded image]: {ocr_text}")
                  except Exception as e:
                      output_lines.append(f"[OCR error: {e}]")

              # 3. Write companion text file
              basename = filepath.replace(".excalidraw.md", "")
              output_path = f"{basename}-extracted.md"

              with open(output_path, "w") as f:
                  f.write(f"---\n")
                  f.write(f"source: \"{os.path.basename(filepath)}\"\n")
                  f.write(f"type: excalidraw-extraction\n")
                  f.write(f"auto_generated: true\n")
                  f.write(f"---\n\n")
                  f.write(f"# Extracted Content: {os.path.basename(basename)}\n\n")
                  f.write(f"> Auto-extracted from Excalidraw drawing. Do not edit — regenerated on each push.\n\n")

                  if wikilinks:
                      f.write("## Linked Notes\n\n")
                      for link in sorted(set(wikilinks)):
                          f.write(f"- [[{link}]]\n")
                      f.write("\n")

                  if output_lines:
                      f.write("## Text Content\n\n")
                      for line in output_lines:
                          f.write(f"- {line}\n")
                  else:
                      f.write("*No text content found in this drawing.*\n")

              # Update manifest
              manifest[filepath] = file_hash

          # Also OCR standalone images (screenshots, photos dropped in maps/)
          for img_path in glob.glob(f"{MAPS_DIR}/**/*.png", recursive=True) + \
                          glob.glob(f"{MAPS_DIR}/**/*.jpg", recursive=True):
              with open(img_path, "rb") as f:
                  file_hash = hashlib.sha256(f.read()).hexdigest()

              if manifest.get(img_path) == file_hash:
                  print(f"SKIP (unchanged): {img_path}")
                  continue

              print(f"OCR IMAGE: {img_path}")
              changed = True

              try:
                  from PIL import Image
                  import pytesseract
                  img = Image.open(img_path)
                  ocr_text = pytesseract.image_to_string(img).strip()

                  basename = os.path.splitext(img_path)[0]
                  output_path = f"{basename}-ocr.md"

                  with open(output_path, "w") as f:
                      f.write(f"---\nsource: \"{os.path.basename(img_path)}\"\ntype: image-ocr\nauto_generated: true\n---\n\n")
                      f.write(f"# OCR: {os.path.basename(img_path)}\n\n")
                      f.write(f"> Auto-extracted via Tesseract OCR. Do not edit.\n\n")
                      if ocr_text:
                          f.write(ocr_text + "\n")
                      else:
                          f.write("*No text detected in this image.*\n")

                  manifest[img_path] = file_hash
              except Exception as e:
                  print(f"OCR failed for {img_path}: {e}")

          # Save updated manifest
          with open(MANIFEST_PATH, "w") as f:
              json.dump(manifest, f, indent=2)

          if not changed:
              print("No new or modified files to process.")
          EXTRACT_SCRIPT

      - name: Commit extracted text
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add docs/maps/.extraction-manifest.json
          git add docs/maps/*-extracted.md docs/maps/*-ocr.md 2>/dev/null || true
          git diff --staged --quiet || git commit -m "chore: extract text + OCR from new/modified drawings"
          git push
```

**Output per drawing:**
- `maps/world-map.excalidraw.md` — the drawing itself
- `maps/world-map-extracted.md` — auto-generated: all text labels, OCR'd image text, wikilinks found
- `maps/world-map.svg` — auto-exported by Excalidraw plugin (visual preview)

**Output per standalone image:**
- `maps/whiteboard-photo.png` — the image
- `maps/whiteboard-photo-ocr.md` — auto-generated: OCR'd text from the image

The manifest (`docs/maps/.extraction-manifest.json`) tracks SHA-256 hashes. Only files with new/changed hashes get reprocessed — no wasted compute on untouched drawings.

### Stage 2: AI Review for Linking (Devin Workflow)

After the GitHub Action extracts text, an AI review pass can be triggered to:
1. Read all `*-extracted.md` and `*-ocr.md` files
2. Identify proper nouns that match the registry (Appendix A)
3. Create stub pages for any NEW entities not yet in the registry
4. Add `[[wikilinks]]` in the extracted companion files
5. Optionally update the Excalidraw JSON itself to add links to text elements

**This should also be incremental.** The AI workflow should:
- Check the extraction manifest to see which files were just processed
- Only review those files (not the whole `maps/` folder)
- Update `.agent/workflows/lore-index.md` if new entities are discovered

**Suggested AI workflow file** (`.agent/workflows/review-drawings.md`):

```markdown
# Review Excalidraw Drawings

## When to Run
After the GitHub Action `excalidraw-extract.yml` commits new `*-extracted.md` or `*-ocr.md` files.

## Steps
1. Read `docs/maps/.extraction-manifest.json` to identify recently processed files
2. Read the corresponding `*-extracted.md` / `*-ocr.md` companion files
3. Cross-reference all text against the proper noun registry in this lore-index
4. For each proper noun found:
   - If a page exists: add `[[wikilink]]` in the extracted companion file
   - If NO page exists: create a stub page with frontmatter, add to lore-index
5. Update `CHANGELOG.md` with what was reviewed and linked
6. Do NOT reprocess files whose companion .md files already contain wikilinks
   unless the source drawing was modified (check manifest hash)
```

### Why This Gives You OneNote-Like Searchability

In OneNote, everything is searchable because Microsoft runs server-side OCR on all your content. This pipeline replicates that:

| Content Type | OneNote | Our Pipeline |
|-------------|---------|--------------|
| Typed text in drawings | Searchable | Extracted to companion `.md` -> searchable in Obsidian |
| Handwritten annotations | OCR'd server-side | OCR'd via Tesseract in GitHub Action |
| Imported images/photos | OCR'd server-side | OCR'd via Tesseract in GitHub Action |
| Embedded file text | Indexed | Extracted via JSON parsing |
| Proper noun linking | Manual `@mentions` only | Auto-linked by AI review pass |

The difference: OneNote does OCR silently in the cloud. Here, the GitHub Action does it on push, and the results live as searchable markdown files in your vault. **You never have to think about it** — push a drawing, and within minutes the text is searchable everywhere (Obsidian search, AI chat, Git grep).

### 8.3 Excalidraw Plugin Config

| Setting | Value | Why |
|---------|-------|-----|
| Excalidraw folder | `maps` | Keeps drawings organized |
| Auto-export SVG | ON | Creates preview images for Git viewers |
| Auto-export PNG | OFF | SVG is smaller and scalable |
| Embed drawings as | Native Excalidraw | Best editing experience |

### 8.4 .gitignore Updates

Add to `.gitignore`:
```
# Obsidian
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/graph.json
.obsidian/hotkeys.json
```

Keep in Git (so plugin config is shared):
```
.obsidian/app.json
.obsidian/appearance.json
.obsidian/community-plugins.json
.obsidian/core-plugins.json
.obsidian/plugins/
```

---

## 9. Multi-Device Sync

### Option A: Obsidian Sync ($4/month) -- Recommended

- Native, encrypted, real-time sync
- Works on all platforms including iOS and Android
- Syncs vault settings and plugins
- No Git conflicts

### Option B: iCloud (Free, Apple only)

- Place vault in iCloud Drive
- Works on Mac + iOS
- Does NOT work on Windows/Android
- Occasional sync conflicts with `.obsidian/` files

### Option C: Git Sync (Free, all platforms) -- Recommended Starting Point

- **Desktop:** Use the **Obsidian Git** community plugin for auto pull/push (stable on desktop)
- **Mobile:** Use the **GitSync** community plugin (not the same as "Obsidian Git" -- GitSync is designed for mobile and avoids the instability issues). Note: the older "Obsidian Git" plugin self-reports as "highly unstable on mobile" and recommends GitSync instead.
- Both plugins talk to the same GitHub repo, so desktop and mobile stay in sync via Git
- Free and keeps everything in the repo with full version history

### Recommendation

Start with **Option C (Git Sync)** -- it's free, keeps the repo as single source of truth, and enables AI workflows directly. Use **Obsidian Git** on desktop and **GitSync** on mobile. If Git sync proves too fiddly on mobile, upgrade to **Obsidian Sync** ($4/mo) later -- it can coexist with the Git integration (Obsidian Sync handles device-to-device, Git handles version history and AI access).

---

## 10. Maintenance & Future AI Workflows

### How New Content Flows Through the System

This section walks through exactly what happens when new lore arrives -- whether from an AI processing a lore dump, a session transcript, or you manually creating a note in Obsidian.

**Example: The February 17, 2026 Lore Dump**

This is a real example. PR #7 processed a lore dump and produced:
- A rewritten [[Dean Isolde Vane]] profile (85 lines, added GM backstory)
- A brand new NPC: **Soot** ([[Lomi]]'s roommate)
- Backstory/bond/flaw additions to 7 existing NPCs ([[Sarge]], [[Lucky]], [[Pudge]], [[Pyrrhus]], [[Kojo]], [[Ratchet]], [[Valerius Sterling]])
- Updated harmony-nodes.md and power-system.md with new GM-only details
- Updated lore-index.md with new NPC roles

Here's how each workflow would handle it:

#### Flow A: AI commits to Git, you consume in Obsidian

```
1. AI (Devin) processes lore dump on a branch
2. AI commits changes + creates PR
3. PR is merged to main
4. Obsidian Git plugin auto-pulls (or you pull manually)
5. New/updated files appear instantly in your vault
6. Obsidian Copilot re-indexes (the AI chat now knows about Soot, Dean Isolde's secrets, etc.)
```

**What works automatically:**
- All existing `[[wikilinks]]` to updated files (e.g., `[[Dean Isolde Vane]]`) now show the new content on hover/click
- Backlinks panel updates -- if Soot's page mentions `[[Lomi]]`, Lomi's backlinks now show Soot
- Search finds the new content immediately
- Graph view adds Soot as a new node connected to Lomi, Ratchet, Block 99

**What needs manual attention:**
- If the AI created Soot's file in standard markdown format (no frontmatter, no wikilinks), you need to:
  1. Add YAML frontmatter with aliases and tags
  2. Convert inline mentions to wikilinks (e.g., "Lomi" -> `[[Lomi]]`)
- Existing files that mention "Soot" as plain text won't auto-link -- you'd search for "Soot" and add `[[Soot]]` links where appropriate
- The `Various Complements` plugin helps here: once Soot's page exists, the plugin auto-suggests `[[Soot]]` as you type in other notes

**How to minimize manual work:** Update the AI workflows (`.agent/workflows/add-character.md`, etc.) to output Obsidian-native format:
- Always include YAML frontmatter with aliases and tags
- Use `[[wikilinks]]` instead of markdown links
- Use `> [!warning]-` callouts instead of `> [!CAUTION]`
- This way, AI-generated content arrives vault-ready

#### Flow B: You create/edit content directly in Obsidian

```
1. You create a new note in Obsidian (e.g., maps/battle-map.excalidraw.md)
2. You type [[Soot]] and it auto-links because the page exists
3. You edit Dean Isolde's page -- add a relationship, fix a detail
4. Obsidian Git plugin auto-commits and pushes to GitHub
5. Next time Devin (or any AI) reads the repo, it sees your changes
6. The GitHub Action extracts text from Excalidraw files (if applicable)
```

**What works automatically:**
- Wikilinks resolve immediately as you type
- Hover preview shows the target note
- Backlinks update in real time
- Graph view updates in real time
- If you use Templater, new NPC notes come pre-filled with the right frontmatter structure

**What needs attention:**
- If you create a note for a new entity, existing files that mention it as plain text won't auto-link retroactively. You can:
  - Use Obsidian's "Find and Replace" (Ctrl+Shift+H) to convert `Soot` -> `[[Soot]]` across the vault
  - Or let it happen organically -- old files link when you next edit them
- Excalidraw drawings: text labels inside drawings are NOT searchable by Obsidian or AI until the GitHub Action extracts them (see Section 8.2)

#### Flow C: Hybrid (Recommended)

The most realistic workflow combines both:

| Task | Who Does It | Where |
|------|------------|-------|
| Process raw session transcripts | AI (Devin) | Git branch -> PR -> merge |
| Bulk lore dumps / NPC backstories | AI (Devin) | Git branch -> PR -> merge |
| Quick edits (fix a typo, add a relationship) | You | Obsidian (auto-pushes via Git plugin) |
| Create Excalidraw maps | You | Obsidian |
| Creative brainstorming | You + Obsidian Copilot | Obsidian AI chat panel |
| Review AI-generated content | You | Obsidian (after pull) |

The key principle: **Git is the single source of truth.** Both Obsidian and AI read/write to the same repo. Obsidian Sync handles device-to-device convenience; Git handles version history and AI access.

### After Each Session

1. Drop raw transcript into `sessions/transcripts/sN-raw.md`
2. Run AI processing (Devin `/add-session` workflow or manual)
3. AI commits updated files to the repo
4. Pull into Obsidian via Git plugin
5. Review and edit in Obsidian (live preview)
6. Obsidian Copilot re-indexes for AI chat

### When Adding New Entities

1. Create a new note using the Templater template (NPC, location, faction, etc.)
2. Fill in frontmatter with aliases and tags
3. The entity is immediately linkable as `[[Entity Name]]` across the vault
4. Backlinks automatically show everywhere it's mentioned

### Keeping Wikilinks Current

When new proper nouns are introduced:
1. Add a page for the entity (even a stub)
2. Add aliases in frontmatter
3. Consider doing a vault-wide search-and-replace to convert plain text mentions to `[[wikilinks]]`
   - Obsidian's search + replace can do this
   - Or use a script (see conversion spec above)

### Coexistence with Jekyll/GitHub Pages

If you want to keep the Jekyll site running alongside Obsidian:
- Wikilinks `[[like this]]` will break in Jekyll
- You'd need a build step that converts wikilinks back to markdown links for Jekyll
- **Recommendation:** Drop Jekyll. Obsidian IS the wiki now. If you need a public-facing site later, use the Obsidian Publish service ($8/mo) or build the custom web app.

---

## 11. Migration Checklist

### Phase 1: Conversion (Automated Script)

- [ ] Build proper noun registry from all entity files + glossary + lore-index
- [ ] Generate YAML frontmatter with aliases for all 50 character files (45 NPC + 5 PC)
- [ ] Generate YAML frontmatter for all faction, location, bestiary, and world pages
- [ ] Convert all markdown links (`[[Path|text]]`) to wikilinks (`[[Page]]`)
- [ ] Scan all files and convert inline proper noun mentions to wikilinks (first occurrence per section)
- [ ] Convert `> [!CAUTION]` blocks to collapsible `> [!warning]-` callouts
- [ ] Create `_templates/` folder with templates for: NPC, PC, Session, Lore Page, Location

### Phase 2: Vault Config

- [ ] Create `.obsidian/` folder with base config
- [ ] Set up core settings (see Section 5.3 and 5.4)
- [ ] Install and configure essential community plugins
- [ ] Set up Obsidian Git plugin
- [ ] Update `.gitignore` for Obsidian workspace files

### Phase 3: AI Setup

- [ ] Copy `lore-index.md` into vault as `ai-reference/lore-index.md`
- [ ] Configure Obsidian Copilot with API key
- [ ] Index vault for RAG
- [ ] Test AI chat with sample questions

### Phase 4: Excalidraw & OCR

- [ ] Create `maps/` folder
- [ ] Add Excalidraw GitHub Action (Section 8.2)
- [ ] Create initial world map drawing (optional)
- [ ] Verify OCR extraction pipeline works

### Phase 5: Multi-Device

- [ ] Set up Obsidian Sync or preferred sync method
- [ ] Install Obsidian on mobile devices
- [ ] Verify sync works across devices
- [ ] Test editing on mobile

### Phase 6: Cleanup

- [ ] Remove Jekyll-specific files (`_config.yml`, `Gemfile`, `netlify.toml`) or move to repo root
- [ ] Verify all wikilinks resolve (Obsidian shows broken links in red)
- [ ] Run Obsidian's "Show unresolved links" to find any missed conversions
- [ ] Update `README.md` to reflect new Obsidian-based workflow
- [ ] Update `.agent/workflows/` to reference Obsidian conventions

---

## Appendix A: Complete Proper Noun Registry

The following is the full list of entities that should be wikilinked. This registry should be used by the conversion script.

### Player Characters (5)

| Page Name | Aliases |
|-----------|---------|
| Britt | -- |
| Aggie | -- |
| Ignatius | Lava Boy |
| Lomi | Lomi Sultano |
| Iggy | -- |

### NPCs (45)

| Page Name | Aliases |
|-----------|---------|
| Dean Isolde Vane | Dean Vane, Isolde, The Dean |
| Celia Vance | -- |
| Hesperus | Senior Exploranaut Hesperus |
| Ratchet | -- |
| Kojo | -- |
| Pyrrhus | -- |
| Professor Kante | Kante |
| Valerius Sterling | Val, Val Sterling |
| Seraphina "Serra" Vox | Serra, Serra Vox, Seraphina Vox |
| Cassius Thorne | Cassius |
| Iron-Jaw Jax | Jax |
| Maria Wall | Wall, Wall Maria |
| Brawn | -- |
| Nyx | -- |
| Kaelen | -- |
| Mira | -- |
| Calculus Prime | -- |
| Theorem | -- |
| Lemma | -- |
| Dr. Rose Halloway | Rose Halloway |
| Silas Thorne | Old Man Thorne, Silas |
| Bramble | -- |
| Cinder-4 | Cinder |
| Hearth | -- |
| Kindle | -- |
| Captain Barnacle | Barnacle |
| Pressure | -- |
| Depth | -- |
| Percival Vane-Smythe III | Percy, Percival |
| Lady Glimmer | Glimmer |
| Baron Bolt | Bolt |
| Sarge | -- |
| Lucky | -- |
| Pudge | -- |
| Lady Ignis | Ignis |
| Rill | Real, The River-Born |
| Zephyr | Lightning Girl |
| Lance | -- |
| Valerius Sterling Sr. | Sterling Sr. |
| Lady Glissade | Glissade |
| Ember | -- |
| Tommy | -- |
| Lucina | -- |
| Marla | -- |
| Soot | -- |

### Factions & Clans

| Page Name | Aliases |
|-----------|---------|
| Mizizi | Root-Kin, Deep-Root Clan, Mycelium Clan |
| Ash-Bloods | Ember-Kin, Pyre-Keepers, Ash Bloods |
| Trench-Kin | Earthkin, Abyssal |
| Renali | Air Clan, Cloud-Kin |
| Wadi | River Clan, Dry Vein |
| Fulgur-Born | Storm-Chasers |
| House Gilded | The Highborne, The Vault |
| Vane Lineage | House Vane, The Shield, The Orderborne |
| Scrivener Guild | The Loreborne |
| Iron-Union | The Ridgeborne, Iron Union |
| The Verdant Trust | Verdant Trust, The Agri-Lords |
| High-Justiciars | The Scales |
| Grand Architects | House Mason |
| Syndicate of Sails | -- |

### Key Terms (from Glossary)

| Term | Aliases |
|------|---------|
| The Great Stitching | Great Stitching |
| Harmony | The New Empire |
| Harmony Prime | The Seat, Harmony Seat, The Seat of Harmony |
| The Bleed | Dissolution |
| The Minimum | -- |
| Global Amplitude | -- |
| The Loom | -- |
| Crystal Batteries | Vox Batteries |
| Leidian | -- |
| Chime Spires | Resonators |
| Aether | The Ether, Ether |
| Safe-Flame | -- |
| True Flame | -- |
| Void-Beast | -- |
| Ether-Jelly | -- |
| Engine Grease | -- |
| Exchange Ritual | -- |
| Inverse Power Doctrine | -- |
| Exploranaut | -- |
| Savant | -- |

### Locations

| Page Name | Aliases |
|-----------|---------|
| Vumbua Academy | Vumbua, The Safiri |
| Sky-Spire | -- |
| Walker-Core | -- |
| Deep-Hull | -- |
| Spire-Scape | -- |
| Block 99 | -- |
| Celestial Lounge | -- |

---

## Appendix B: Estimated Effort

| Phase | Effort | Notes |
|-------|--------|-------|
| Phase 1: Conversion script | 2-4 hours | Python/Node script to do bulk conversion |
| Phase 2: Vault config | 30 min | Manual config in Obsidian |
| Phase 3: AI setup | 30 min | API key + plugin config |
| Phase 4: Excalidraw/OCR | 1 hour | GitHub Action + initial test |
| Phase 5: Multi-device | 30 min | Sync setup |
| Phase 6: Cleanup/QA | 1-2 hours | Fix broken links, verify |
| **Total** | **5-8 hours** | Can be done in one session |
