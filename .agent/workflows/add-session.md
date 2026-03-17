---
description: Add a new session recap after gameplay
---

# Add New Session

Use this workflow after each game session to document what happened, update the vault, and prepare the Foundry export.

---

## Mandatory pause points (do not skip)

The AI must stop and wait for user confirmation at three points:
1. **After the Session Delta** — confirm new NPC list and canonical names before creating files
2. **After drafting the `sessions/index.md` prose summary** — user reviews the player-facing text before it goes into Foundry
3. **After generating portraits** — user approves or requests regeneration before the rebuild

---

## Prerequisites

- Raw transcript at `sessions/transcripts/raw/sN-raw.md` (Granola, Otter, manual notes — any format)
- Know the session number
- DO NOT start until the raw transcript file exists

---

## Step 1 — Orient: read context files

Read these before touching anything:

1. **`.agent/workflows/lore-index.md`** — canonical spellings, recent session delta
   - Note: this file may be stale. Cross-check its "Last Updated" against the clean transcripts in `sessions/transcripts/clean/`. If stale, treat it as a reference only — verify against actual NPC files.
2. **`sessions/planning/sN-plan.md`** (or `sessions/planning/old/`) — the intended session plan. Read this BEFORE the raw transcript so you know canonical NPC names and planned events.
3. **`characters/index.md`** — existing characters, to distinguish new NPCs from known ones

---

## Step 2 — Session number and file check

- List files in `sessions/transcripts/clean/` to confirm the highest session number
- Check for multiple raw files (e.g., `sN-raw.md`, `sN-granola.md`, `sN-alt.md`) — if multiple exist, read all and cross-reference
- Confirm the session number with the user if anything is ambiguous

---

## Step 3 — Pre-scan: build the Session Delta

Read the raw transcript and produce a Session Delta before writing anything else. Output this to the user and **wait for confirmation** before creating any files.

```markdown
## Session Delta (Session N: [draft title — user will confirm])

### Proposed canonical title
- Draft: "Session N — [Subtitle]"
- If you can't determine a natural title from the transcript, say so.

### New NPCs (need file creation)
- [Name as heard in transcript] → proposed canonical name: [Name] — [1-line role]
- ⚠ Flag any where you're uncertain: "Is 'the harbor woman' a new NPC or an existing one?"

### Existing NPCs with new appearances
- [[Name]] — what happened this session

### New locations
- [Name] — brief description

### New terms / lore
- [Term] — brief description

### Player Knowledge Changes
- ✅ [What players now know]
- ❌ [What players explicitly do NOT know yet — keep out of player-facing sections]

### Transcript issues to flag
- ⚠ Uncertain speaker attributions
- ⚠ Potential transcription errors
- ⚠ Any lines that appear to be OOC but formatted as IC
```

**Wait for user confirmation on:**
- The session title
- The new NPC list — are these all genuinely new characters?
- Any names where the transcript and session plan disagree

---

## Step 4 — Create the clean transcript

**Filename:** `sessions/transcripts/clean/sN-clean.md` — e.g., `s5-clean.md`
(The build script requires this exact pattern. `session-05.md` will be silently ignored.)

**YAML front matter:**
```yaml
---
title: "Session N: [Confirmed Title]"
date: YYYY-MM-DD
campaign: Vumbua
status: cleanup-complete
---
```

**Structure — choose based on session content:**
- If the session has discrete scenes with GM narration blocks → use `## Play-by-Play → ### Scene Name` format (like s3-clean.md)
- If the session has clear narrative phases/chapters → use `## Part N: Name` format (like s4-clean.md)
- Either way, start with the Session Delta block from Step 3

**Content rules:**
- ✅ Preserve every story-relevant detail — this is organization, not summarization
- ✅ Label speakers: `**[[Character Name]] (PC):**` or `**[[NPC Name]]:**`
- ✅ Use character names for IC dialogue, player names for OOC dialogue
- ✅ Fix transcription errors at 99% confidence only; note every correction made
- ✅ Correct to canonical spellings from lore-index (e.g., "Lasidian" → "lavsidian")
- ❌ Never summarize, compress, or skip dialogue
- ❌ Never add details not in the transcript
- ❌ Never smooth PC dialect or NPC speech quirks (Iggy's dropped letters, Kante's broken English — these are intentional)
- ❌ Never present OOC player thinking as IC character dialogue

**GM voice handling:**
- GM narration blocks → `*GM Narration:*` in italics, or format as `**GM (LUKE S):**`
- GM interjections inside scene prose (e.g., `"the GM notes..."`) → remove or move to a `**GM Notes:**` line immediately after the relevant passage
- Never leave bare `"the GM notes..."` fragments inside continuous narrative prose — the spoiler filter only strips heading-level sections, not inline text

**Speaker attribution pitfalls:**
- The GM often speaks AS an NPC, then immediately switches to narration — don't attribute narration to the NPC
- When uncertain, write `**[UNIDENTIFIED NPC]:** "[line]" [review needed]` — do not default-assign to a character
- Re-read 5 lines before/after any correction to make sure you haven't orphaned adjacent dialogue

**Failure states (learned from past sessions):**
1. **Smoothing PC dialect** — Iggy's `"'S nice to meet ya"`, `"'course"`, `"nime"` are character voice. Do not standardize.
2. **Smoothing NPC voice** — Kante's `"What do you like, know?"` is deliberate. Do not "fix" it.
3. **Swapping attribution** — `"Your home sounds like a very hard place to live"` was Kante, not Iggy. Context matters.
4. **OOC as IC** — Holly brainstorming what Iggy would say ≠ Iggy saying it.
5. **Deleting exchanges while fixing** — when editing one line, re-read surrounding 10 lines.
6. **Asking about canonical names** — always check `characters/npcs/` before asking the user.

---

## Step 5 — Update `sessions/index.md`

Add the new session entry at the bottom of the current arc section, following this exact format:

```markdown
---

### [[Session 0N|Session N: Confirmed Title]]
**Date:** YYYY-MM-DD

[2–4 sentences of narrative prose. PLAYER-FACING: write as if a player is reading a recap of what their characters experienced. Past tense. Third person. No GM voice ("the GM reveals...", "players discover..."). No spoilers. No future tense. This paragraph is exactly what appears in Foundry's Chronicle journal.]

**Key Events:**
- [bullet list of what happened]
- [use [[wikilinks]] for named characters and locations]

**Players Discovered:**
- [factual things the players now know — only confirmed in-session discoveries]
```

**Session ID padding rule for the wikilink:**
- Session 5 → `[[Session 05|Session 5: Title]]`
- Session 10 → `[[Session 10|Session 10: Title]]`
- Session 2.5 → `[[Session 02Pt5|Session 2.5: Title]]`

**Pause here** — show the user the prose paragraph before continuing. This is the text that appears in Foundry. Ask: *"Does this look right for what players should see?"*

---

## Step 6 — Create/update NPC files

For each **new** NPC confirmed in Step 3:

1. Check `characters/npcs/` — if a stub already exists, update it. Never create a duplicate.
2. Create `characters/npcs/[kebab-name].md` using the template in `add-character.md`
3. The minimum for Foundry inclusion:
   ```markdown
   # [Name]

   | | |
   |---|---|
   | **Role** | [1–3 words] |
   | **First Appearance** | [[session-N\|Session N]] |
   ```
4. Add more detail from the transcript (GM description, dialogue, relationships)
5. Put anything the players don't know under `## GM Narration` with a `> [!warning]-` callout

For **existing** NPCs with new session appearances:
- Add a `### Session N` entry to their `## Session Appearances` section
- Never overwrite earlier entries — always append

Update `characters/index.md` for any new NPCs added.

---

## Step 7 — Portraits for new NPCs

For each new NPC without a portrait:
1. Check `meta/foundry-exports/portraits/` for `[snake_name]_portrait.png`
2. If missing, generate using the AI image tool
3. **Portrait style guidance:** match the style of existing portraits in `meta/foundry-exports/portraits/` — they are painterly fantasy character illustrations with muted/warm tones
4. Filename must be: `[snake_case_name]_portrait.png` — slugify rule: lowercase, strip all quotes/punctuation, spaces → underscores
   - "Professor Kante" → `professor_kante_portrait.png`
   - `Seraphina "Serra" Vox` → `seraphina_serra_vox_portrait.png`

**Pause here** — show generated portraits to user. Ask: *"Do these portraits work, or should I regenerate any?"* Do not proceed to rebuild until confirmed.

---

## Step 8 — Update supporting docs

Use the Session Delta from Step 3 to drive updates. Only touch pages listed in the delta.

- **`knowledge-tracker.md`** — add new player discoveries
- **`timeline.md`** — add session events
- **`lore-index.md`** — update the "Last Session Delta" block with the new session's delta; add new canonical spellings; update "Last Updated" line

For any existing lore or location pages that were significantly changed by this session's events, update them directly — don't just add a link.

---

## Step 9 — Rebuild the Foundry codex

**When to use delta vs full:**
- **Delta** (`python build_codex.py N`) — if only new NPCs were added and existing NPC pages didn't change. Smaller JSON, faster.
- **Full** (`python build_codex.py`) — if existing NPC or location pages were updated, or if you changed `sessions/index.md` prose for any earlier session.

```bash
cd vumbua/meta/foundry-exports
python build_codex.py N    # replace N with session number
# or
python build_codex.py      # full rebuild
```

Verify the output: all new pages should print `✓`. Any `✗` indicates a missing file.

Tell the user: *"Ready — `vumbua-codex.json` is built. Paste it into the Foundry macro to import."*

---

## Step 10 — Verify the next session plan

Check whether `sessions/planning/sN+1-plan.md` exists.
- If it exists → do not touch it (don't overwrite prep the GM has already done)
- If it doesn't exist → create a stub noting what the party was doing at session end and any obvious hooks

---

## What NOT to do in this workflow

- ❌ Do not draft the radio recap — that's a separate `/radio-recap` workflow
- ❌ Do not run `git commit` — version control is handled automatically
- ❌ Do not update `sessions/index.md` with GM-only information
- ❌ Do not create `session-NN.md` — it must be `sN-clean.md`

---

## File locations

| File | Path |
|---|---|
| Raw transcript | `sessions/transcripts/raw/sN-raw.md` |
| Clean transcript | `sessions/transcripts/clean/sN-clean.md` |
| Session index (player-facing) | `sessions/index.md` |
| Session plan | `sessions/planning/sN-plan.md` |
| NPC profiles | `characters/npcs/[name].md` |
| Portraits | `meta/foundry-exports/portraits/[name]_portrait.png` |
| Foundry codex output | `meta/foundry-exports/vumbua-codex.json` |
| Lore reference | `.agent/workflows/lore-index.md` |
| Character index | `characters/index.md` |
