---
description: Add a new session recap after gameplay
---

# Add New Session

Use this workflow after each game session to properly document what happened.

## Prerequisites
- Raw transcript or notes from the session (placed in `sessions/transcripts/raw/sN-raw.md`)
- Know which session number this is
- Read `.agent/workflows/lore-index.md` first to orient on canonical spellings and existing characters

## Steps

1. **Determine the session number**
   - Check `sessions/transcripts/clean/` for the last session number
   - New session will be N+1

2. **Cross-Reference and Gather Context (CRITICAL STEP)**
   - Read the `.agent/workflows/lore-index.md` canonical spellings section first.
   - Read the corresponding session plan (if one exists) located in `sessions/planning/` or `sessions/planning/old/` to understand the *intended* narrative and character mappings before reading the raw transcript.
   - Example: If reading Session 3 raw transcript, first read `Session 3 Plan.md` to know who the antagonists were supposed to be (e.g., Azor and Zyykl, not "Azer" and "Nickel").

3. **Review the raw transcript file**
   - Located at `sessions/transcripts/raw/sN-raw.md`
   - If it doesn't exist, ask the user to provide one
   - **Check for alternate versions**: Look for other transcript files (e.g., `sN-granola.md`, `sessionN-alt.md`) in the transcripts folder. If multiple versions exist, cross-reference them — one may have more faithful dialogue while another has better structure.

4. **Create the cleaned session file**
   // turbo
   - Create `sessions/transcripts/clean/session-NN.md`
   - Use the structure of the most recent cleaned session in `sessions/transcripts/clean/` as your template
   - Fill in the header information (date, players present)

4.5. **Pre-scan: Build entity lists from transcript**
   - Scan the entire transcript for all entities mentioned:
     - NPCs (name + first mention line)
     - Locations
     - Factions
     - Terms/concepts
   - Cross-reference against `.agent/workflows/lore-index.md`, `characters/index.md`, and the **Session Plan** to identify **NEW vs EXISTING** entities and ensure **canonical names** are used (e.g., if the transcript says "Nickel" but the plan says "Zyykl," use "Zyykl").
   - Produce a **Session Delta** block in this exact format (copy it into both the cleaned transcript header and `.agent/workflows/lore-index.md`):

   ```markdown
   ## Session Delta (Session NN: <Title>)

   ### New / First-Mentioned Entities
   - NPC: [[Name]] — <1-line context> — Source: [[session-NN|Session NN]] (Scene X)
   - Location: [[Name]] — <1-line context> — Source: [[session-NN|Session NN]] (Scene X)
   - Term: [[Name]] — <1-line context> — Source: [[session-NN|Session NN]] (Scene X)

   ### Updated Entity Pages
   - [[Name]] — add/update “Session Appearances” (and “Source References” if you maintain curated sources)

   ### Player Knowledge Changes
   - Knowledge Tracker: ✅/❌ <bullet>

   ### Truth / Provenance Notes
   - If something is **GM planning** (not spoken in-session), tag it as `gm-plan` and keep it out of “What Players Know”.
   ```

   - This delta is what future “diff-based” runs should rely on; it makes updates fast and bounded.

5. **Extract and organize scenes from the transcript**

   > **CORE RULE: Zero detail loss.** This step is about *organizing* the transcript into a readable screenplay format, NOT summarizing. Every story-relevant detail must be preserved.

   **Cross-Referencing Check (CRITICAL)**: Before finalizing a scene, double-check the events against the Session Plan. If the plan says X happened but the transcript says Y, document Y, but ensure you aren't misinterpreting the transcript due to bad audio/transcription errors (e.g., mistaking the item a character fought over). Use your logic.

   **Scene Structure:**
   - Identify major scene breaks (location changes, time jumps, significant topic shifts)
   - For each scene, document:
     - Scene heading with location and who is present
     - **GM Narration**: Everything the DM says as narrator — descriptions, world-building, scene-setting. Preserve verbatim
     - **NPC Dialogue**: Only attribute to a specific NPC if you are **99% confident** based on context. Otherwise tag as `[NPC - UNIDENTIFIED, review needed]`
     - **PC Dialogue**: Attribute to the character
     - **Player Discoveries**: Bullet list of what was learned
     - Key events and actions

   **Speaker Attribution Rules:**
   - Use **character name** ([[Iggy]], [[Britt]], [[Ignatius]], etc.) when speaking **in-character**
   - Use **player name** (Holly, Sophie, John, etc.) when speaking **out-of-character**
   - Determine IC vs OOC from context (tone, content, GM responses)
   - When uncertain, default to character name and flag for review

   **Cleanup Rules:**
   - ✅ **Fix**: Obvious transcription errors (99% confidence you know the correct word based on lore context)
   - ✅ **Fix**: Canonical spelling corrections per `lore-index.md` (e.g., "Lasidian" → "Leidian")
   - ✅ **Organize**: Break into scenes, label speakers, format as screenplay
   - ❌ **Never**: Summarize, compress, or skip dialogue
   - ❌ **Never**: Add descriptions or details not in the transcript (no hallucination)
   - ❌ **Never**: Change character voices, word choices, or story details
   - 🚨 **FAILURE STATE — Overwriting history**: When updating character profiles, lore pages, or knowledge trackers with new session info, **ADD** new entries — never replace or overwrite earlier descriptions. A character's journey should be visible over time. If Iggy was described as "an infiltrator" in Session 1 notes but Session 2.5 reveals he's "genuinely trying to help his people," add the new understanding alongside the old — don't delete the original framing. Session canon is always additive.
   - 🚨 **FAILURE STATE — PC Dialect**: Never normalize or clean up in-character dialect. If Holly says `"I dunno"`, `"'course"`, `"nothin'"`, `"t'day"` — that IS Iggy's voice. Smoothing dialect into standard English destroys the player's character work. Preserve dropped letters, contractions, and accent exactly as spoken.
   - 🚨 **FAILURE STATE — NPC Voice**: NPC speech quirks are equally sacred. If [[Professor Kante]] says `"What do you like, know?"` or `"I am most apologetic"` — that is his broken-English character voice, NOT a transcription error. The GM chose those phrasings deliberately. Never smooth NPC dialogue into grammatically correct English.
   - ❌ **Never**: Present OOC player thoughts as IC dialogue. If Holly is *thinking out loud* about what Iggy might feel or ask (as a player brainstorming), that is OOC and should be formatted as `> **Holly (OOC):**`. Only attribute dialogue to Iggy if she is *performing* as him.
   - ❓ **Tag for review**: Ambiguous NPC names, unclear speaker attribution, uncertain corrections

   **NPC Handling:**
   - Index every NPC that appears or is mentioned
   - Record any GM description of an NPC verbatim as "GM Description"
   - If an NPC is new (not in `lore-index.md`), flag them for character creation in step 6
   - Never invent NPC details — only record what the DM actually says
   - **Always check existing NPC files** before asking the user about canonical names or details. If `professor-kante.md` already exists, never ask "is Kante canonical?" — just read the file

   **Speaker Attribution Pitfalls:**
   - Raw transcripts mash speakers together with no labels — slow down and parse who is talking
   - The GM often says a line *as an NPC*, then immediately follows with narration; don't attribute narration to the NPC
   - When the GM says a line like `"Got an interesting thing going on over here"` — determine if this is the NPC speaking or the GM describing what the PC sees. Context clues: does the next line respond to it? Is the GM still doing scene description?
   - When fixing one line of dialogue, re-read the surrounding 5-10 lines to make sure you didn't accidentally delete or orphan adjacent exchanges

6. **Update the session index and "What Actually Happened"**
   - Add an entry to `sessions/index.md`
   - Include 2-3 sentence summary
   - List key events and player discoveries
   - **Update the Session Plan**: Go to the original session plan (e.g., `sessions/planning/old/Session 3 Plan.md`) and append a `## What Actually Happened` section at the bottom, summarizing the deviations and actual outcomes.
   - If new NPCs/PCs were introduced, run `/add-character` and update `characters/index.md`. Ensure that when updating `.agent/workflows/lore-index.md`, you completely remove any misspelled/placeholder names from the transcript (like "Azer") and replace them entirely with the canonical name.

7. **Update related documentation**
   - Use the **Session Delta** block to drive updates (update only the pages listed there; avoid broad repo-wide edits)
   - Run `/add-character` for any new NPCs introduced (flagged in step 3.5)
   - Update `knowledge-tracker.md` with new discoveries
   - Update `timeline.md` with session events
   - Update character profiles if significant events occurred
   - Update `lore-index.md` with the Session Delta, new entities, spellings, and session status
   - If you need to capture GM-prep that did not occur in-session, place it under a clearly-labeled **GM Plan** section and tag it as `gm-plan`

8. **Commit changes**
   ```bash
   git add .
   git commit -m "docs: Add Session N recap and related updates"
   ```

9. **Update changelog**
   - Append to `CHANGELOG.md` under today's date
   - Bullet: session processed, key files updated

## File Locations
- Raw transcripts: `sessions/transcripts/raw/sN-raw.md`
- Cleaned sessions: `sessions/transcripts/clean/session-NN.md`
- Lore index (AI reference): `.agent/workflows/lore-index.md`
- Session Plans: `sessions/planning/` or `sessions/planning/old/`

## Common Mistakes (learned from Session 2.5 and Session 3)

These are real errors that were made and corrected. Do not repeat them:

1. **Smoothing PC dialect** — [[Iggy]]'s `"Nime"` was rewritten as `"(doesn't really answer properly)"`, his `"'S nice to meet ya"` became `"Just looking"`, etc. Every contraction, dropped letter, and accent marker is intentional character work.

2. **Smoothing NPC voice** — Kante's fumbled phrasing `"What do you like, know?"` was "corrected" to `"What do you know?"`. His broken English is his character.

3. **Swapping speaker attribution** — `"Your home sounds like a very hard place to live"` was attributed to Iggy (deadpan) when it was actually Kante (deadpan). Raw transcripts don't label speakers — you must infer from context and get it right.

4. **Presenting OOC as IC** — Holly thinking out loud about the Exchange (`"If connection is so important, why does the Exchange force people to forget?"`) was formatted as an Iggy IC line. It was Holly brainstorming OOC.

5. **Deleting exchanges during fixes** — When fixing Iggy's opening dialect, the entire Kante/Iggy student exchange (`"Are you a student here?"` / `"That is what I have been told"`) was accidentally removed.

6. **Asking about canonical names** — Asked the user if "Kante" was canonical when `professor-kante.md` already existed in the NPC files. Always check existing files first.

7. **Failing to Cross-Reference the Session Plan** — (Session 3 error) Failing to read the `Session 3 Plan.md` before processing the transcript, leading to the creation of NPCs with misspelled transcript names ("Azer" and "Nickel") instead of the canonical names already established in the plan ("Azor" and "Zyykl"). **Always read the plan first.**

8. **Missing Key Items/Details** — (Session 3 error) Misidentifying a crucial heirloom (a petrified acorn necklace) as a pocket watch because of a quick skim. **Read carefully, cross-reference, and ensure logical consistency in the narrative.**
