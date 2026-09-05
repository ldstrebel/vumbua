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

- Raw transcript at `sessions/data/raw/sN-raw.md` (Granola, Otter, manual notes — any format)
- Know the session number
- `sN-session-config.json` exists and declares the GM (see Step 0)
- DO NOT start until the raw transcript file exists

---

## Step 0 — Session config: GM + shared mics (HARD PREREQUISITE)

**Before any analysis, obtain and record the GM and shared-mic config from the user.**
These are user-provided facts. The pipeline NEVER infers them from the transcript.

The user supplies, with the roster:
1. **who the GM is**, and
2. **whether any mics are shared** — and which player rides whose mic.

Record them in `sessions/sN-devin/sN-session-config.json` (schema and examples:
`sessions/s12-devin/README.md`, `campaign/planning/transcript-pipeline-plan.md` §2.0):

```json
{
  "session_id": "sN",
  "gm": "Luke S",
  "players": { "Sophie": "Britt", "Kristina": "Aggie", "John": "Ignatius", "Luke F": "Lomi", "Holly": "Iggy" },
  "shared_mics": [
    {
      "mic_label": "Luke S",
      "note": "Kristina speaks Aggie's lines through Luke's GM mic",
      "carries": [
        { "person": "Luke S", "identity": "GM", "kind": "gm" },
        { "person": "Kristina", "identity": "Aggie", "kind": "player_character" }
      ]
    }
  ],
  "raw_speaker_labels": { "John Hagey": "John", "Luke Strebel": "Luke S" }
}
```

- `shared_mics: []` is a real declaration — *no mics are shared*. Omitting the key is an error.
- If the user hasn't given you the GM or the mic sharing, **stop and ask.** Do not proceed to Step 3.
- `prep_raw.py` and `attribute_speakers.py` exit with status 2 when the config is missing or `gm` is absent, so a session cannot be processed around this gate.
- `raw_speaker_labels` fixes garbled **person** labels only. Diarization is per-mic, not per-person.

---

## Step 1 — Orient: read context files

Read these before touching anything:

1. **`.agent/workflows/lore-index.md`** — canonical spellings, recent session delta
   - Note: this file may be stale. Cross-check its "Last Updated" against the clean transcripts in `sessions/data/clean/`. If stale, treat it as a reference only — verify against actual NPC files.
2. **`campaign/planning/sN-plan.md`** (or `campaign/planning/old/`) — the intended session plan. Read this BEFORE the raw transcript so you know canonical NPC names and planned events.
3. **`characters/index.md`** — existing characters, to distinguish new NPCs from known ones

---

## Step 2 — Session number and file check

- List files in `sessions/data/clean/` to confirm the highest session number
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

## Step 4 — Create the clean transcript (Editor Pass 1: 0-Bias Audio & Disentanglement Audit)

**Filename:** `sessions/data/clean/sN-clean.md` — e.g., `s12-clean.md`  
*(The build script requires this exact pattern. `session-12.md` will be silently ignored.)*

**Role:** Editor 1 (Zero-Bias Audio & Disentanglement Auditor).

### Mandatory First-Pass Categorization Protocol
Every line from `sN-raw.md` MUST be evaluated and categorized into one of three explicit tiers in `sN-clean.md`:

1. **Tier A: In-World Spoken Dialogue (`**[[Speaker]] (PC/NPC):** "..."`)**
   * Direct, in-universe spoken lines.
   * **Disentanglement Rule (config-driven):** Disentangle a stream **only** for the mics listed in `shared_mics` in `sN-session-config.json`, and only into the identities that mic declares. For Session 12 the config declares that `Luke S` carries GM narration, GM-voiced NPCs, and Kristina's Aggie, so a line-by-line audit MUST assign the exact character attributions (`**[[Aggie]] (PC):**`). If the config declares no shared mics, do not disentangle — and never widen attribution by inference. Record each per-line call in `sN-attribution-decisions.json` and validate with `python sessions/_scripts/attribute_speakers.py sN`.
   * **NPC Disentanglement:** Disentangle NPC spoken dialogue from GM scene descriptions into explicit NPC dialogue blocks (`**[[NPC Name]] (NPC):**`).

2. **Tier B: Player Action & Intent Context (`*Player Action Intent:*`)**
   * Player descriptions of what their character is physically doing, feeling, or aiming to accomplish (e.g., *"I think Britt is zoned and focused on following the turtle"*, *"Iggy does a grounding ritual with basalt rocks over the bodies"*, *"Ignatious carries Loami on his back"*).
   * **CRITICAL RULE (No Meta-in-Dialogue):** NEVER place player action descriptions inside character speech bubbles or spoken quotes. Tag them as `*Player Action Intent:*` so Editor 2 (Novelization) transforms them into rich **Narrator Prose & Character Movement**!

3. **Tier C: Pure Technical & Meta Table Talk (`*Table Note:*`)**
   * Technical glitches, Wi-Fi drops, Roll20 backups, character sheet HTML files, gas bills, and dice mechanics chatter.
   * Tagged as `*Table Note:*` to preserve OOC context without leaking into narrative story files or audiobooks.

---

### First-Pass Audit Gate (Line-by-Line Inspection)
Before advancing to Step 4b (Novelization), the LLM must perform a **direct line-by-line inspection of `sessions/data/raw/sN-raw.md`** using `view_file` to verify:
1. **100% Attribution Accuracy:** No shared-stream lines misattributed to the GM or wrong player.
2. **Zero Meta-Talk Leaks:** No player action descriptions or dice talk written as character dialogue quotes.
3. **100% Beat Completeness:** Zero dropped player actions, NPC interactions, comedic beats, or lore reveals.

---

## Step 4b — Create the novelized story file (Editor Pass 2: Novelization, Dialect & Prose Audit)

**Filename:** `sessions/data/clean/sN-clean-story.md` — e.g., `s11-clean-story.md`

**Role:** Editor 2 (Single Master File — Novel + Audiobook Source).

### Mandatory Pre-Writing Narrative Flow Gate
Before drafting any chapters:
1. **Load the Master Storyboard**: Consult [`campaign/planning/book-1-narrative-structure.md`](file:///d:/Code/vumbua/campaign/planning/book-1-narrative-structure.md) and [`campaign/planning/campaign-narrative-bible.md`](file:///d:/Code/vumbua/campaign/planning/campaign-narrative-bible.md) to check macro 5-Act placement, active plot lines (A through E), and character reflection triggers.
2. **Execute the Pre-Story Weaving Audit**: Follow [`.agents/skills/session-audit/SKILL.md`](file:///d:/Code/vumbua/.agents/skills/session-audit/SKILL.md) to verify long-horizon trajectory alignment (Session 12 destination) and avoid front-loaded worldbuilding dumps.
3. **Monotonic Chapter Progression (Never Reset to Chapter 1)**: Determine the global continuous chapter numbers (`## CHAPTER N: TITLE`), picking up monotonically from the previous session rather than resetting per session.

### Novelization Standards
- Convert `sN-clean.md` into **Brandon Sanderson-style high-fantasy prose chapters** using global chapter numbering.
- **Pristine Prose & Rhythmic Flow:** Eliminate repetitive sentences, awkward passive phrasing, and typos from day one. The prose must read out loud like a published fantasy novel.
- **Character Dialect & Phonetics (baked into dialogue):** Write character voice directly into spoken lines — `eyeth`, `treeth`, `yeth`, `thorry` for Iggy's lisp; `nevah`, `bettah`, `somethin'`, `frickin'` for Loami's accent. These are permanent and serve both reading and TTS narration.
- **No Bracketed TTS Tags:** Do NOT add `[screaming]`, `[panicked]`, `[gasped]` etc. ElevenLabs v2 reads them aloud. Rely on ALL CAPS, `!?`, `...`, and em-dashes for emotional delivery instead.
- **Purge Table Meta-Talk:** Remove out-of-character dice chatter and convert game mechanics into fluid in-universe actions.
- **Audit Against Clean Transcript:** Ensure NO iconic character quotes, GM lore, or key actions are lost.


**YAML front matter (required for parser):**
```yaml
---
title: "Session N: [Confirmed Title]"
author: "Novel Adaptation in the Style of Brandon Sanderson"
campaign: Vumbua
genre: Epic Fantasy / Sci-Fantasy
---
```

**H1 Title (required — becomes Narrator opening title card):**
```markdown
# DON'T TOUCH MY BISCUITS
```
*Note: Must use `# ` (H1) format only. The parser reads this as the Narrator's opening line. Do NOT include "Session N:" prefix here — it's already in the YAML `title` field.*

**Speaker attribution rules for TTS parsing (critical):**
- Every dialogue line must have the **speaking character's name immediately adjacent to a speech verb** in the narration tag outside the quotes — e.g., `"Quote," Aggie gasped, staring at Britt.` ✅
- The parser detects `Aggie gasped` (NAME + verb within 5 chars) and correctly assigns Aggie's voice even when another character's name appears later in the same sentence.
- Lines with **no character name outside the quotes** (bare quotes like `"LAZIZI!"`) must be followed by a narration tag: `"LAZIZI!" Britt screamed.`
- Pronouns (`he said`, `she asked`) are supported via context tracking — the parser tracks the last active male/female speaker.

*`sN-clean-story.md` is the SINGLE canonical source for BOTH the ebook and multi-voice ElevenLabs audiobook synthesis.*

---

## Step 4c — Narration Pre-Flight Audit (MANDATORY — zero credits)

Before spending any ElevenLabs credits, run the parser audit tool:

```powershell
python sessions/_scripts/parse_audit.py
```

This generates `sessions/_scripts/parse_audit_report.txt` with:
- Every audio block's speaker attribution and detection method
- A list of **FALLBACK WARNINGS** (lines where no name or pronoun was found)
- **Zero warnings = safe to generate.** Any warning = fix the source line before generating.

**Common warning causes and fixes:**

| Symptom | Example | Fix |
|---------|---------|-----|
| Bare quote with no tag | `"LAZIZI!"` | Add `, Britt screamed.` after the quote |
| Pronoun with no prior speaker | `"Well," he grunted.` at file start | Replace `he` with character name: `"Well," Ignatious grunted.` |
| Stadium/ambient quote | `*"Hold on!"*` in italics | Remove inner quotes — use italics only: `*Hold on!*` |

---

## Step 4d — Generate the Multi-Voice Audiobook

Once the audit reports **0 warnings**, generate:

```powershell
# Clean old files if regenerating
Remove-Item 'sessions/audio/sN/*' -Force

# Generate
python sessions/_scripts/generate_audiobook.py \
  --input sessions/data/clean/sN-clean-story.md \
  --output-dir sessions/audio/sN \
  --generate
```

**Output files produced automatically:**

| File | Description |
|------|-------------|
| `sN_audiobook_full.mp3` | Complete master audiobook |
| `CHAPTER_1__*.mp3` ... | Per-chapter MP3 tracks |
| `sN_sync_timestamps.json` | Blinkist-style line sync JSON (ms-accurate) |
| `sN_subtitles.vtt` | WebVTT subtitle track for web/mobile players |
| `segment_NNN_Speaker.mp3` | Individual per-line segment files |

**Credit budget reference:**
- ~19,000–20,000 credits per full session (~9–10% of 200,000 budget)
- Use `--parse-only` flag to estimate character count without spending credits

**Voice cast (configured in script):**

| Character | Voice ID | Type |
|-----------|----------|------|
| Narrator | `pNInz6obpgDQGcFmaJgB` | ElevenLabs premade (Adam) |
| Loami | `IM5qdLwbG2AX3RiVX0Of` | Custom voice |
| Pip | `386eQBpmCgw3emfoqL5n` | Custom voice |
| Iggy | `hxEheaxKsMWuFhE8lXGW` | Custom voice |
| Ignatious | `iP95p4xoKVk53GoZ742B` | ElevenLabs premade (Chris) |
| Britt | `21m00Tcm4TlvDq8ikWAM` | ElevenLabs premade (Rachel) |
| Aggie | `AZnzlk1XvdvUeBnXmlld` | ElevenLabs premade (Domi) |

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
2. If missing, **before generating**: call `view_file` on the NPC's profile file in `characters/npcs/[name].md` and extract every physical description detail from the transcript notes. Do not generate from the character's name alone — always use description tokens from the file.
3. Generate using the AI image tool with those description tokens. **Portrait style guidance:** match the style of existing portraits in `meta/foundry-exports/portraits/` — they are painterly fantasy character illustrations with muted/warm tones.
4. If no physical description exists in the profile yet, generate a placeholder portrait, name it correctly, and add a `<!-- regenerate: no physical description yet -->` comment to the NPC file as a reminder.
5. Filename must be: `[snake_case_name]_portrait.png` — slugify rule: lowercase, strip all quotes/punctuation, spaces → underscores
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

Check whether `campaign/planning/sN+1-plan.md` exists.
- If it exists → do not touch it (don't overwrite prep the GM has already done)
- If it doesn't exist → create a stub noting what the party was doing at session end and any obvious hooks

---

## Step 11 — Storyboard handoff (if applicable)

If a graphic novel storyboard is planned for this session, hand off to the `/storyboard` workflow now.

Tell the user:
> "The clean transcript is ready at `sessions/data/clean/sN-clean.md`. Run `/storyboard` when you're ready to generate the comic pages — it will use this file as its ground-truth source."

Do NOT begin storyboard generation inside this workflow. The `/storyboard` workflow has its own mandatory verification steps and human approval gates that must run separately.

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
| Raw transcript | `sessions/data/raw/sN-raw.md` |
| Clean transcript | `sessions/data/clean/sN-clean.md` |
| Session index (player-facing) | `sessions/index.md` |
| Session plan | `campaign/planning/sN-plan.md` |
| NPC profiles | `characters/npcs/[name].md` |
| Portraits | `meta/foundry-exports/portraits/[name]_portrait.png` |
| Foundry codex output | `meta/foundry-exports/vumbua-codex.json` |
| Lore reference | `.agent/workflows/lore-index.md` |
| Character index | `characters/index.md` |
