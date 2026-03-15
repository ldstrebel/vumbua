---
description: Export campaign journals to Foundry VTT via the Codex macro
aliases:
- Export to Foundry
---

# Export to Foundry

Use this workflow to generate and import the Vumbua Codex into Foundry VTT. This creates spoiler-safe player-facing journals with cross-linked pages and embedded NPC portraits.

## What Gets Created

| Journal | Contents |
|---------|----------|
| **Campaign Chronicle** | Session-by-session narrative recap |
| **Player Characters** | Each PC's profile, abilities, and open quests |
| **NPCs** | Each NPC's portrait, role, and interactions with the party |
| **Locations** | What players have learned about each place |

All pages are cross-linked — clicking an NPC name in a session recap navigates to their NPC page.

## Prerequisites

- Clean transcripts exist for all sessions being exported (`sessions/transcripts/clean/`)
- Foundry VTT is running and you are logged in as **GM**
- The macro has been created in Foundry (one-time setup — see Step 3)

## Steps

### 1. Generate the Codex JSON

Ask the AI to generate or update `meta/foundry-exports/vumbua-codex.json`:

```
Generate the Foundry Codex JSON for sessions 0 through N.
Cross-reference clean transcripts for spoiler safety.
Include NPC portraits as embedded base64.
Use {{page:Name}} placeholders for cross-links.
```

**AI instructions:**
- Read each clean transcript (`sessions/transcripts/clean/session-NN.md`)
- Use ONLY player-known information — never include GM Notes, secrets, or planned content
- Generate NPC portrait art for any new NPCs using the image generation tool
- Encode portraits as base64 and embed in the JSON under `portraits` key
- Use `{{page:PageName}}` syntax for all cross-links between pages
- Output structure must follow the 4-journal format (see `meta/foundry-exports/vumbua-codex.json` for reference)

### 2. Validate the JSON
// turbo
```bash
python -c "import json; f=open('meta/foundry-exports/vumbua-codex.json','r',encoding='utf-8'); d=json.load(f); pages=[p for j in d['journals'].values() for p in j['pages']]; print(f'OK: {len(pages)} pages, {len(d.get(\"portraits\",{}))} portraits')"
```

### 3. Set Up the Foundry Macro (One-Time)

1. In Foundry VTT → **Macro Directory** → Create Script Macro
2. Name it `Vumbua Codex Importer`
3. Paste the entire contents of `meta/foundry-exports/foundry-macro.js`
4. Save

### 4. Run the Import

1. Click the macro in Foundry
2. Paste the contents of `meta/foundry-exports/vumbua-codex.json` into the dialog
3. Click **Import Fresh**
4. Wait for the success dialog — it will show counts for pages, links, and portraits

> **⚠️ This is destructive** — it deletes existing Vumbua Codex journals and recreates them. This is intentional for clean imports.

### 5. Verify

- [ ] Open **Campaign Chronicle** → check session recaps render correctly
- [ ] Click an NPC link in a session recap → should navigate to their NPC page (no new tab)
- [ ] Open an NPC page → portrait should display inline
- [ ] Open **Locations** → verify descriptions match player knowledge only
- [ ] Spot-check for spoilers — no GM secrets, future plans, or hidden character details

### 6. Commit

```bash
git add meta/foundry-exports/
git commit -m "foundry: Update Vumbua Codex (sessions 0-N)"
```

## File Reference

| File | Purpose |
|------|---------|
| `meta/foundry-exports/vumbua-codex.json` | All journal data + embedded portraits |
| `meta/foundry-exports/foundry-macro.js` | Foundry import macro (3-pass: create → resolve links → write) |
| `meta/foundry-exports/portraits/` | Source portrait PNGs (originals) |

## Linking System

Content uses `{{page:PageName}}` placeholders. The macro resolves these in-memory before writing to Foundry:

```
{{page:Serra Vox}}              → @UUID[JournalEntry.X.JournalEntryPage.Y]{Serra Vox}
{{page:Serra Vox|the Gold-Rank}} → @UUID[JournalEntry.X.JournalEntryPage.Y]{the Gold-Rank}
```

Portraits use `src='portraits/filename.png'` in the JSON. The macro replaces these with `data:image/png;base64,...` data URIs from the embedded portrait data.

## Spoiler Rules

When generating content for the Codex, the AI must:
- **Only** reference clean transcripts and player-facing knowledge
- List Iggy's race as "Earthkin" (not Trench-Kin)
- List Zephyr's race as "Unknown"
- List Rill as "Mizizi exchange student" (not her heritage details)
- Present Percy's Sixfold Theory as a fringe belief, not confirmed lore
- Never reference GM Notes, planned encounters, or unrevealed backstory
