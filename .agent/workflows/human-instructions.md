---
description: User guide for leveraging AI workflows in this repo
aliases:
- Human Instructions
---

# How to Use This Repo with AI

This guide explains how to get the most out of the AI workflows for managing the Vumbua campaign.

---

## Quick Start: After a Session

1. **Record or transcribe the session** (Granola, Otter, manual notes — whatever works)
2. **Drop the raw transcript** into `lore/sessions/transcripts/sN-raw.md` (where N = session number)
3. **Tell the AI**: `/add-session` — it will handle the rest
4. **Review the cleaned transcript** — check speaker attributions and flagged items
5. **Deploy**: `/deploy` to push changes to the wiki

---

## Workflow Reference

### `/add-session` — Process a Raw Transcript

**When**: After every game session

**What to prepare**:
- Raw transcript file placed at `lore/sessions/transcripts/sN-raw.md`
- Know the session number (check `lore/sessions/transcripts/` for the latest)

**Prompt examples**:
```
/add-session
Process the raw transcript for session 3. The raw file is at lore/sessions/transcripts/s3-raw.md.
Players present: Sophie (Britt), Kristina (Aggie), John (Ignatius), Luke (Lomi), Holly (Iggy).
Session date: February 16, 2026.
```

**What the AI will do**:
1. Read the lore-index for canonical spellings
2. Scan for all NPCs, locations, and new terms
3. Organize into scenes with proper speaker attribution
4. Fix only 99%-confidence transcription errors
5. Flag uncertain attributions for your review
6. Update session index, knowledge tracker, timeline

**What to review**:
- `[UNIDENTIFIED]` or `[review needed]` tags — the AI wasn't sure who was speaking
- New NPC names — confirm spellings
- Scene breaks — make sure they feel right
- Any corrections the AI made (it will note these)

**Important rules the AI follows**:
- **Zero detail loss** — nothing is summarized or cut
- **No hallucination** — it never adds details not in the transcript
- **Conservative corrections** — only fixes words it's 99% sure are wrong

---

### `/add-character` — Create a Character Profile

**When**: After a new NPC appears in a session, or to update an existing profile

**What to prepare**:
- Character name and type (PC or NPC)
- Which session they appeared in

**Prompt examples**:
```
/add-character
Create a profile for Professor Kante. He's an NPC who appeared in Session 2.5.
He's a tortoise professor of harmonics from House Gilded.
```

```
/add-character
Update Zephyr's profile with what happened in Session 2 (the purple lightning event).
```

**What the AI will do**:
1. Check if a profile already exists
2. Create or update the profile using only confirmed details
3. Update the character index
4. Update the lore-index

---

### `/add-lore` — Add or Update World Lore

**When**: After sessions reveal new world information, or when adding GM planning material

**What to prepare**:
- The information to add (from session transcripts or your notes)
- Which category it belongs to (world, location, faction, bestiary)

**Prompt examples**:
```
/add-lore
Add a lore page for the Celestial Lounge. It's a location that appeared in Session 2.
It's an upscale club on the top floor of the tallest building in the northwest fancy district.
```

```
/add-lore
Update the Ash-Bloods page — in Session 2, the cultural divide between traditionalists
(Ignatius) and modernizers (Ember) was revealed.
```

---

### `/deploy` — Push to the Wiki

**When**: After you've reviewed changes and want them live

**Prompt**: Just type `/deploy`

---

## Tips for Best Results

### Asking for the right truth tier (prevents "planned" bleeding into canon)
When prompting the AI, specify which tier you want:
- **Player handout**: use only **What Players Know** + transcript-derived facts
- **GM assistant**: include **GM Narration** (unrevealed but narrated canon)
- **Prep mode**: include **GM Plan** (future rosters/intent); otherwise the AI should avoid it

If you see something like a squad roster referenced before the Loom/team selection has happened in-session, that should be treated as **GM Plan** until the transcript establishes it.

### Providing Transcripts
- **Any format works** — the AI will organize it. Raw Granola/Otter output, manual notes, etc.
- **More is better** — include everything, even table talk. The AI will identify what's in vs. out of character.
- **Note the GM** — if possible, identify which speaker is the GM in the transcript so the AI can distinguish narration from player talk.

### Handling Uncertain Attributions
- The AI will tag anything uncertain with `[review needed]`
- Just tell it: *"That line was Serra, not an unidentified NPC"* and it will fix it
- Batch corrections are fine: *"Lines tagged for review: 1 is Serra, 2 is [[Iron-Jaw Jax|Jax]], 3 is the GM describing the room"*

### Requesting Corrections
- Be specific: *"Change all instances of 'Lasidian' to 'Leidian'"*
- Or general: *"Scan the transcript for name misspellings and fix them per the canonical list"*
- The AI will always show you what it changed

### Player Names vs Character Names
- The AI will use **player names** (Sophie, Holly, etc.) for out-of-character moments
- And **character names** ([[Britt]], [[Iggy]], etc.) for in-character dialogue
- If you prefer a different convention, just say so

---

## File Quick Reference

| What | Where |
|------|-------|
| Raw transcripts | `lore/sessions/transcripts/sN-raw.md` |
| Cleaned sessions | `lore/sessions/transcripts/session-NN.md` |
| Character index | `lore/characters/index.md` |
| NPC profiles | `lore/characters/npcs/` |
| PC profiles | `lore/characters/player-characters/` |
| World lore | `lore/` |
| Glossary | `lore/glossary.md` |
| Timeline | `lore/timeline.md` |
| Knowledge tracker | `lore/knowledge-tracker.md` |
| AI lore index | `.agent/workflows/lore-index.md` |
