---
description: Add a new session recap after gameplay
---

# Add New Session

Use this workflow after each game session to properly document what happened.

## Prerequisites
- Raw transcript or notes from the session (placed in `docs/sessions/transcripts/sN-raw.md`)
- Know which session number this is
- Read `.agent/workflows/lore-index.md` first to orient on canonical spellings and existing characters

## Steps

1. **Determine the session number**
   - Check `docs/sessions/index.md` for the last session number
   - New session will be N+1

2. **Review the raw transcript file**
   - Located at `docs/sessions/transcripts/sN-raw.md`
   - If it doesn't exist, ask the user to provide one
   - Read `lore-index.md` canonical spellings section before starting cleanup

3. **Create the cleaned session file**
   // turbo
   - Copy `docs/sessions/_template.md` to `docs/sessions/transcripts/session-NN.md`
   - Fill in the header information (date, players present)

3.5. **Pre-scan: Build entity lists from transcript**
   - Scan entire transcript for all NPCs mentioned (name + first appearance line)
   - List all locations visited or referenced
   - List all new terms or concepts introduced
   - Cross-reference against `lore-index.md` to identify NEW vs EXISTING entities
   - This informs scene extraction and batches character creation for step 6

4. **Extract and organize scenes from the transcript**

   > **CORE RULE: Zero detail loss.** This step is about *organizing* the transcript into a readable screenplay format, NOT summarizing. Every story-relevant detail must be preserved.

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
   - Use **character name** (Iggy, Britt, Ignatius, etc.) when speaking **in-character**
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
   - ❓ **Tag for review**: Ambiguous NPC names, unclear speaker attribution, uncertain corrections

   **NPC Handling:**
   - Index every NPC that appears or is mentioned
   - Record any GM description of an NPC verbatim as "GM Description"
   - If an NPC is new (not in `lore-index.md`), flag them for character creation in step 6
   - Never invent NPC details — only record what the DM actually says

5. **Update the session index**
   - Add entry to `docs/sessions/index.md`
   - Include 2-3 sentence summary
   - List key events and player discoveries

6. **Update related documentation**
   - Run `/add-character` for any new NPCs introduced (flagged in step 3.5)
   - Update `docs/lore/knowledge-tracker.md` with new discoveries
   - Update `docs/lore/timeline.md` with session events
   - Update character profiles if significant events occurred
   - Update `lore-index.md` with new entities, spellings, and session status

7. **Commit changes**
   ```bash
   git add docs/sessions/ docs/lore/ docs/characters/
   git commit -m "Add Session N recap"
   git push
   ```

8. **Update changelog**
   - Append to `CHANGELOG.md` under today's date
   - Bullet: session processed, key files updated

## File Locations
- Raw transcripts: `docs/sessions/transcripts/sN-raw.md`
- Cleaned sessions: `docs/sessions/transcripts/session-NN.md`
- Template: `docs/sessions/_template.md`
- Session index: `docs/sessions/index.md`
- Lore index (AI reference): `.agent/workflows/lore-index.md`