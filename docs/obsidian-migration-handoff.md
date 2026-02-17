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
[Ash Bloods](/lore/factions/clans/ash-bloods.md)
[The Bleed](world/the-bleed.md)
[Britt](player-characters/britt.md)
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
3. **Alias support** -- `[[Rill]]` also matches "Real", "The River-Born"; `[[Seraphina "Serra" Vox]]` matches "Serra", "Serra Vox"
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
3. Known nicknames from session transcripts (e.g., "Lava Boy" for Ignatius, "Lightning Girl" for Zephyr)
4. Faction alternate names from the glossary (e.g., Mizizi = "Root-Kin" = "Deep-Root Clan" = "Mycelium Clan")

**Tag taxonomy** (suggested):
- `pc`, `npc`, `faction`, `clan`, `harmony-house`, `location`, `creature`, `world-lore`, `session`, `mechanic`
- Squad tags: `squad-01` through `squad-09`
- Rank tags: `gold-rank`, `silver-rank`, `copper-rank`, `rust-rank`
- Secrecy tags: `gm-only`, `player-facing`

### 4.2 Convert Markdown Links to Wikilinks

Replace all `[Display Text](relative/path.md)` with `[[Page Name]]` or `[[Page Name|Display Text]]`.

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
| **Clan** | [Ash Bloods](/lore/factions/clans/ash-bloods.md) |
- **[Britt](player-characters/britt.md)** - Mizizi (Gray fungal-turtle) - Gold Rank
- [The Bleed](world/the-bleed.md) - Where reality dissolves

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
5. Match aliases: if "Real" appears and Rill's aliases include "Real", link it as `[[Rill|Real]]`
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
- Add wikilinks to terms that have their own pages (e.g., `**[[Rill]]** (The River-Born)`)
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
- Ask questions: "What does Ignatius know about the power crisis?"
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

**The solution: OCR + text extraction after each push.**

**Recommended workflow:**

1. **Create drawings in Obsidian** using the Excalidraw plugin (maps, diagrams, relationship charts)
2. **Save as `.excalidraw.md`** in the `maps/` folder
3. **On push to Git**, a GitHub Action extracts all text from Excalidraw files and writes companion `.md` files:

```yaml
# .github/workflows/excalidraw-ocr.yml
name: Excalidraw Text Extraction

on:
  push:
    paths:
      - 'docs/maps/**/*.excalidraw.md'

jobs:
  extract-text:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Extract Excalidraw text
        run: |
          for file in docs/maps/*.excalidraw.md; do
            if [ -f "$file" ]; then
              basename="${file%.excalidraw.md}"
              # Extract text elements from Excalidraw JSON
              # The JSON is embedded between ```json and ``` markers
              python3 -c "
          import json, sys, re
          content = open('$file').read()
          # Find JSON block in excalidraw.md
          match = re.search(r'\`\`\`json\n(.*?)\n\`\`\`', content, re.DOTALL)
          if match:
              data = json.loads(match.group(1))
              texts = [e.get('text','') for e in data.get('elements',[]) if e.get('type')=='text']
              with open('${basename}-text.md', 'w') as f:
                  f.write('# Text from ${file}\n\n')
                  f.write('> Auto-extracted from Excalidraw drawing. Do not edit manually.\n\n')
                  for t in texts:
                      if t.strip():
                          f.write(f'- {t.strip()}\n')
          " 2>/dev/null || true
            fi
          done
      
      - name: Commit extracted text
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add docs/maps/*-text.md
          git diff --staged --quiet || git commit -m "chore: extract text from Excalidraw drawings"
          git push
```

This means:
- `maps/world-map.excalidraw.md` (the drawing)
- `maps/world-map-text.md` (auto-generated searchable text)

The companion text file is searchable by both Obsidian and external AI.

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

### Option C: Git Sync (Free, all platforms)

- Use the Obsidian Git plugin (see Section 8.1)
- Works on desktop (Mac/Windows/Linux)
- On mobile: use Working Copy (iOS) or Termux (Android) to pull/push
- More technical but free and keeps everything in the repo

### Recommendation

Use **Obsidian Sync** for seamless cross-device experience. Keep the **Git integration** as well for backup and AI workflow compatibility. They can coexist -- Obsidian Sync handles device-to-device, Git handles version history and AI integration.

---

## 10. Maintenance & Future AI Workflows

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
- [ ] Generate YAML frontmatter with aliases for all 49 character files (44 NPC + 5 PC)
- [ ] Generate YAML frontmatter for all faction, location, bestiary, and world pages
- [ ] Convert all markdown links (`[text](path.md)`) to wikilinks (`[[Page]]`)
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

### NPCs (44)

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
