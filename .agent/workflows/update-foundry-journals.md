# Update Foundry Journals (Automated)

Use this workflow to sync the Foundry VTT Campaign Codex with the latest session data. The process is now largely automated via `build_codex.py`.

## Prerequisites
- A finalized transcript in `sessions/transcripts/clean/sX-clean.md`.
- New NPCs encountered must have their `.md` files in `characters/npcs/` with a `First Appearance` tag.

## Steps

1. **Verify Session Transcript**
   - Ensure the new session file follows the naming convention `s[Number]-clean.md` in `sessions/transcripts/clean/`.

2. **Update NPC 'First Appearance' Tags**
   - For any NPC who debuted this session, ensure their markdown file in `characters/npcs/` contains the following metadata in the `Overview` table:
     `| **First Appearance** | [[session-[Number]|Session [Number]] |`
   - **Crucial:** The `build_codex.py` script uses this tag to decide if an NPC is "active" and should be exported.

3. **Check for New Locations**
   - If a major new location was introduced, add its name to the `key_locations` list in `meta/foundry-exports/build_codex.py` (lines 191+).

4. **Run the Dynamic Export**
   // turbo
   - Execute the build script. It will automatically scan all NPCs, filter those with active session debutes, embed their portraits, and extract player-safe info.
   ```powershell
   cd d:\Code\vumbua\meta\foundry-exports
   python build_codex.py
   ```

5. **Provide JSON and Macro to User**
   - Direct the user to the updated `vumbua-codex.json`.
   - Remind them to run the `foundry-macro.js` in Foundry VTT to perform the non-destructive additive import.

## Why this works
The script dynamically extracts the **Overview** and **What Players Know** sections while ignoring any **GM Secrets** or **GM Description** blocks, ensuring a spoiler-free experience for players.

## AI Spoiler Rules (Critical)
When generating or auditing content for the Codex, the AI must:
- **Only** reference clean transcripts and player-facing knowledge.
- **Race Corrections**:
  - List Iggy's race as "Earthkin" (not Trench-Kin).
  - List Zephyr's race as "Unknown".
  - List Rill as "Mizizi exchange student" (not her heritage details).
- **Lore Context**:
  - Present Percy's Sixfold Theory as a fringe belief, not confirmed lore.
- **GM Boundary**:
  - Never reference GM Notes, planned encounters, or unrevealed backstory.
