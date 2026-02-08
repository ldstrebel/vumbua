---
description: Add a new session recap after gameplay
---

# Add New Session

Use this workflow after each game session to properly document what happened.

## Prerequisites
- Raw transcript or notes from the session
- Know which session number this is

## Steps

1. **Determine the session number**
   - Check `docs/sessions/index.md` for the last session number
   - New session will be N+1

2. **Create the raw transcript file** (if not already done)
   - Create `docs/sessions/sN-raw.md` with the transcript
   - Include date at the top

3. **Create the cleaned session file**
   // turbo
   - Copy `docs/sessions/_template.md` to `docs/sessions/session-NN.md`
   - Fill in the header information (date, players present)

4. **Extract scenes from the transcript**
   - Identify major scene breaks (location changes, time jumps)
   - For each scene, document:
     - Location and NPCs present
     - Key events and dialogue
     - Player discoveries
     - GM notes (hidden information)

5. **Update the session index**
   - Add entry to `docs/sessions/index.md`
   - Include 2-3 sentence summary

6. **Update related documentation**
   - Run `/add-character` for any new NPCs introduced
   - Update `docs/lore/knowledge-tracker.md` with new discoveries
   - Update `docs/lore/timeline.md` with session events
   - Update character profiles if significant events occurred

7. **Commit changes**
   ```bash
   git add docs/sessions/
   git commit -m "Add Session N recap"
   git push
   ```

## File Locations
- Raw transcripts: `docs/sessions/sN-raw.md`
- Cleaned sessions: `docs/sessions/session-NN.md`
- Template: `docs/sessions/_template.md`
- Session index: `docs/sessions/index.md`
