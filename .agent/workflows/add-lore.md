---
description: Add or update lore documentation
---

# Add/Update Lore

Use this workflow to add new lore pages or update existing ones with new information.

## Prerequisites
- Know what category the lore belongs to (world, location, faction, bestiary)
- Source material (session transcript, planning docs)
- Read `.agent/workflows/lore-index.md` to check for existing pages and canonical spellings

## Lore Categories

| Category | Location | Examples |
|----------|----------|----------|
| **World Events** | `world/` | The Great Stitching, Integration Mechanics |
| **Locations** | `locations/` | Vumbua Academy, The Frontier |
| **Clans** | `factions/clans/` | Mizizi, Ash-Bloods, Trench-Kin |
| **Harmony Factions** | `factions/harmony/` | House Gilded, Iron Union |
| **Bestiary** | `bestiary/` | Ether-Jelly, Void-Beast |

## Steps for New Lore Page

1. **Create the file**
   - Filename: lowercase with hyphens (e.g., `the-great-stitching.md`)
   // turbo
   - Place in appropriate category folder

2. **Use the dual-track format**

   > **CORE RULE: Only record information from session transcripts and GM narration.** Never invent or extrapolate lore.
   >
   > **Truth tiers (RAG safety):**
   > - **transcript**: said/seen in-session
   > - **gm-narration**: narrated by GM but not yet known to PCs
   > - **gm-plan**: prep/intent/rosters that have not happened in-session yet
   >
   > Keep `gm-plan` information clearly labeled and out of “What the Players Know”.

   ```markdown
   ---
   aliases: []
   tags: []
   canon: transcript # transcript | gm-narration | gm-plan | legacy
   reveal: players # players | gm
   ---

   # [Topic Name]

   ## What the Players Know
   [Player-facing lore — information revealed during sessions]

   ### [Subsections as needed]
   [Details organized logically]

   ---

   ## GM Narration [NOT YET REVEALED TO PLAYERS]

   > [!warning]-
   > The following information has been narrated by the GM but is NOT known to the player characters.

   [Hidden lore, future revelations, secret connections — from GM planning/narration only]
   ```

3. **Update navigation**
   - Add to `index.md`
   - Add to `glossary.md` if it defines new terms

4. **Update knowledge tracker**
   - Add entries to `knowledge-tracker.md`
   - Mark what players know (✅) vs don't know (❌)

5. **Update lore-index**
   - Add new entries to `.agent/workflows/lore-index.md`

## Steps for Updating Existing Lore

1. **Check what changed**
   - Review session transcript for new revelations
   - Identify what moved from "GM Narration" to "Players Know"

2. **Update the lore page**

   > **CORE RULE: Add, don't replace.** Session canon is always additive. When new sessions reveal updated information, add new entries alongside old ones — never delete or overwrite earlier descriptions. The evolution of understanding should be visible. For example, if a faction was described as "mysterious" in Session 1 but Session 3 reveals their true motives, keep the original note and add the new revelation with its session tag.

   - Move revealed info from GM section to player section
   - Add new discoveries to player section
   - Update GM section with new narrated implications

3. **Update knowledge tracker**
   - Change ❌ to ✅ for revealed information
   - Add new unknowns

4. **Update lore-index**
   - Update `.agent/workflows/lore-index.md` with any changes

5. **Commit changes**
   ```bash
   git add characters/ sessions/ factions/ world/ locations/ bestiary/ glossary.md timeline.md knowledge-tracker.md CHANGELOG.md
   git commit -m "Update [topic] lore from Session N"
   git push
   ```

6. **Update changelog**
   - Append to `CHANGELOG.md` under today's date
   - Bullet: lore added/updated, file path

## File Locations
- Lore Hub: `index.md`
- Knowledge Tracker: `knowledge-tracker.md`
- Glossary: `glossary.md`
- Timeline: `timeline.md`
- Lore Index (AI reference): `.agent/workflows/lore-index.md`
