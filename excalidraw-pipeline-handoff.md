# Excalidraw Pipeline -- Handoff Document

> **Author:** Devin (AI), requested by Luke S
> **Date:** February 2026
> **Purpose:** Two-part automated pipeline that transcribes Excalidraw drawings and propagates new information into the campaign wiki.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Part 1: Transcribe](#3-part-1-transcribe)
4. [Part 2: Lore Update](#4-part-2-lore-update)
5. [Manifest & Incremental Processing](#5-manifest--incremental-processing)
6. [Secrets & Configuration](#6-secrets--configuration)
7. [File Map](#7-file-map)
8. [Testing & Validation](#8-testing--validation)

---

## 1. Overview

When Luke draws in Excalidraw (on tablet or desktop), the Excalidraw plugin auto-exports a `.png` alongside the `.excalidraw.md` file. GitSync commits both to the repo. This pipeline picks up from there:

```
[Draw in Excalidraw]
        |
        v
[GitSync commits .excalidraw.md + .png]
        |
        v
  Part 1: TRANSCRIBE
  - Detect new/modified PNGs (SHA-256 manifest)
  - Send to GPT-4o vision API
  - Write companion transcription .md
  - Commit transcription + updated manifest
        |
        v
  Part 2: LORE UPDATE
  - Read new transcriptions
  - Identify proper nouns (match against REGISTRY)
  - Flag new entities not in registry
  - Update wikilinks in impacted files
  - Create stub pages for new entities
  - Update CHANGELOG.md
  - Commit all changes
  - Alert user (GitHub Issue comment)
```

**Key design decisions:**
- **Incremental only** -- SHA-256 manifest tracks what's been processed. Only new/modified PNGs trigger work.
- **GPT-4o vision over Tesseract** -- Luke's drawings are handwritten. GPT-4o vision reads handwriting far more accurately than Tesseract (~95% vs ~60-80%).
- **PNG over SVG** -- PNG is a rasterized image that vision models can interpret. SVG stores vector paths that are no more readable than the raw Excalidraw JSON.
- **Two separate workflows** -- Part 1 is stateless (image in, text out). Part 2 requires understanding the full repo structure. Separating them allows re-running Part 2 independently and makes debugging easier.

---

## 2. Architecture

### Trigger Options

| Trigger | Part 1 | Part 2 |
|---------|--------|--------|
| **Nightly schedule** (recommended) | `cron: '0 6 * * *'` (6 AM UTC) | Runs after Part 1 via `workflow_run` |
| **On push** (reactive) | When `Excalidraw/**/*.png` changes | After Part 1 completes |
| **Manual** (`workflow_dispatch`) | Yes | Yes |

**Recommended:** Nightly schedule. GitSync commits frequently (every few minutes while editing), so running on every push would be wasteful. A nightly batch processes everything created that day in one pass.

### Data Flow

```
Excalidraw/
  Drawing A.excalidraw.md    <-- Excalidraw source (compressed JSON)
  Drawing A.png              <-- Auto-exported by Excalidraw plugin
  Drawing A-transcription.md <-- OUTPUT of Part 1

.excalidraw-manifest.json    <-- Tracks SHA-256 hashes of processed PNGs

lore/characters/npcs/        <-- Part 2 may update wikilinks here
lore/factions/               <-- Part 2 may update wikilinks here
CHANGELOG.md                 <-- Part 2 appends summary
```

---

## 3. Part 1: Transcribe

**Goal:** Convert every new/modified Excalidraw PNG into a searchable markdown transcription.

### Workflow: `.github/workflows/excalidraw-transcribe.yml`

**Trigger:** Nightly schedule + manual dispatch + on push to `Excalidraw/**/*.png`

**Steps:**
1. Checkout the repo
2. Set up Python 3.12
3. Run `scripts/excalidraw_transcribe.py`
4. Commit transcription files + updated manifest (if any changes)

### Script: `scripts/excalidraw_transcribe.py`

**Logic:**
1. Load `.excalidraw-manifest.json` (create if missing)
2. Walk `Excalidraw/` for all `*.png` files
3. For each PNG:
   - Compute SHA-256 hash
   - Compare against manifest
   - If new or changed:
     a. Send to OpenAI GPT-4o vision API with transcription prompt
     b. Write response to `<name>-transcription.md` alongside the PNG
     c. Update manifest entry
4. Save updated manifest
5. Exit with code 0 if changes were made, 1 if nothing to process

### Transcription Prompt

The prompt sent to GPT-4o vision is critical. It must:
- Read ALL text (typed and handwritten)
- Preserve the spatial structure (headers, bullets, arrows, boxes)
- Identify any proper nouns that match campaign entities
- Note any diagrams, arrows, or spatial relationships
- Flag anything illegible with `[illegible]`

**Prompt template:**
```
You are transcribing a handwritten/drawn note from a TTRPG campaign wiki called "Vumbua."

Read everything in this image and produce a structured markdown transcription:

1. Transcribe ALL text exactly as written (typed and handwritten)
2. Preserve structure: if text is in boxes, use blockquotes. If bulleted, use bullets. If there are arrows between items, note the relationships.
3. For any proper nouns that might be campaign entities (character names, locations, factions), wrap them in [[wikilinks]]
4. If something is illegible, write [illegible]
5. Note any non-text elements: [diagram: ...], [drawing: ...], [arrow from X to Y]

Known campaign entities for reference: {entity_list}

Output ONLY the transcription in markdown format. No commentary.
```

### Output Format

Each transcription file (`<name>-transcription.md`) will have:

```markdown
---
source: "Excalidraw/Drawing A.png"
transcribed: "2026-02-17T06:00:00Z"
sha256: "abc123..."
model: "gpt-4o"
---

# Transcription: Drawing A

[Transcribed content here with [[wikilinks]] for identified proper nouns]
```

---

## 4. Part 2: Lore Update

**Goal:** Propagate information from transcriptions into the campaign wiki -- update wikilinks, create stub pages for new entities, update changelog.

### Workflow: `.github/workflows/excalidraw-lore-update.yml`

**Trigger:** After Part 1 completes (`workflow_run`) + manual dispatch

**Steps:**
1. Checkout the repo
2. Set up Python 3.12
3. Run `scripts/excalidraw_lore_update.py`
4. Commit all changes (if any)
5. Post summary as GitHub Issue comment

### Script: `scripts/excalidraw_lore_update.py`

**Logic:**
1. Find transcription files modified since last run (compare git status or use a separate manifest)
2. For each new/modified transcription:
   a. Parse for `[[wikilinks]]` -- these are the identified proper nouns
   b. Cross-reference against `scripts/convert_to_obsidian.py` REGISTRY
   c. Categorize:
      - **Known entities**: Verify wikilinks are correct, log for reference
      - **New entities**: Flag for stub page creation
      - **Ambiguous**: Flag for human review
3. For new entities:
   - Create a stub page in the appropriate directory (NPC → `lore/characters/npcs/`, location → `lore/locations/`, etc.)
   - Add to REGISTRY in `scripts/convert_to_obsidian.py`
   - Add to `lore-index.md`
4. Re-run `scripts/convert_to_obsidian.py` to propagate new wikilinks across all files
5. Update `CHANGELOG.md` with a summary of what was processed
6. Output a summary for the GitHub Issue comment

### Stub Page Template

When Part 2 creates a new entity page:

```markdown
---
aliases: []
tags: [stub, needs-review]
---

# {Entity Name}

> Stub page auto-generated from Excalidraw transcription.
> Source: `{source_drawing}`
> Date: {date}

## Context

{Relevant excerpt from transcription where this entity was mentioned}

---

> [!warning]- Needs Review
> This page was auto-generated. A human should review and expand it.
```

### What Part 2 Does NOT Do

- Does NOT summarize or interpret the drawing content
- Does NOT move information from GM notes to player-facing sections
- Does NOT delete or overwrite existing content (additive only, per the campaign's core rule)
- Does NOT modify the original Excalidraw file or PNG
- Does NOT run if Part 1 produced no new transcriptions

---

## 5. Manifest & Incremental Processing

### `.excalidraw-manifest.json`

```json
{
  "version": 1,
  "last_run": "2026-02-17T06:00:00Z",
  "files": {
    "Excalidraw/Devin OCR test.png": {
      "sha256": "abc123...",
      "transcribed_at": "2026-02-17T06:00:00Z",
      "transcription_file": "Excalidraw/Devin OCR test-transcription.md",
      "model": "gpt-4o",
      "status": "complete"
    }
  }
}
```

**Rules:**
- Only PNGs with a new or changed SHA-256 get processed
- If a PNG is deleted, its manifest entry persists (but transcription file can be cleaned up manually)
- The manifest is committed to the repo so all environments share state
- Part 2 checks `transcribed_at` timestamps to find new transcriptions since its last run

---

## 6. Secrets & Configuration

### Required GitHub Secrets

| Secret | Purpose | Required By |
|--------|---------|-------------|
| `OPENAI_API_KEY` | GPT-4o vision API calls | Part 1 |

### Optional Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `VISION_MODEL` | `gpt-4o` | Model for OCR. Can swap to `gemini-1.5-pro` if Google is preferred |
| `MAX_IMAGES_PER_RUN` | `20` | Safety limit to prevent runaway API costs |
| `DRY_RUN` | `false` | If true, logs what would be processed without calling the API |

### Cost Estimates

| Item | Cost | Notes |
|------|------|-------|
| GPT-4o vision per image | ~$0.01-0.05 | Depends on image size and detail level |
| Typical nightly run (1-5 new drawings) | ~$0.05-0.25 | Very low cost |
| Re-processing all images (first run) | ~$0.50-2.00 | One-time bootstrap cost |

---

## 7. File Map

```
.github/workflows/
  excalidraw-transcribe.yml     # Part 1 GitHub Action
  excalidraw-lore-update.yml    # Part 2 GitHub Action

scripts/
  excalidraw_transcribe.py      # Part 1 script (PNG → transcription)
  excalidraw_lore_update.py     # Part 2 script (transcription → lore updates)
  convert_to_obsidian.py        # Existing conversion script (Part 2 re-runs this)

Excalidraw/
  *.excalidraw.md               # Source drawings (committed by GitSync)
  *.png                         # Auto-exported PNGs (committed by GitSync)
  *-transcription.md            # Transcriptions (committed by Part 1)

.excalidraw-manifest.json       # Incremental processing state
```

---

## 8. Testing & Validation

### Smoke Test (Manual)

Before enabling the GitHub Actions, test locally:

```bash
# Part 1: Transcribe
export OPENAI_API_KEY="sk-..."
python scripts/excalidraw_transcribe.py

# Check output
cat Excalidraw/Devin\ OCR\ test-transcription.md
cat .excalidraw-manifest.json

# Part 2: Lore update
python scripts/excalidraw_lore_update.py

# Check output
git diff  # See what changed
```

### Validation Checklist

- [ ] Part 1 only processes new/modified PNGs (run twice, second run should be no-op)
- [ ] Transcription captures all text from drawings (compare against original)
- [ ] Proper nouns are wrapped in `[[wikilinks]]` in transcriptions
- [ ] Part 2 correctly identifies known vs new entities
- [ ] Stub pages are created in the correct directories
- [ ] REGISTRY is updated with new entities
- [ ] `convert_to_obsidian.py` runs successfully after Part 2 updates
- [ ] CHANGELOG.md is updated with run summary
- [ ] No existing content is deleted or overwritten
- [ ] Manifest is updated correctly
- [ ] Cost per run is within expected range

### Known Limitations

1. **Handwriting accuracy**: GPT-4o is good but not perfect. Unusual spellings (campaign-specific terms) may be misread. The entity list in the prompt helps, but novel terms won't be in it.
2. **Spatial relationships**: The transcription captures text and notes arrows/boxes, but complex diagrams (relationship maps, battle plans) lose spatial meaning when flattened to markdown.
3. **GitSync race condition**: If Part 1 commits while GitSync is also committing, there could be a merge conflict. The nightly schedule (running at 6 AM when Luke is likely not editing) mitigates this.
4. **New entity classification**: Part 2 guesses the category (NPC, location, faction) based on context. It may guess wrong. All stubs are tagged `needs-review`.
