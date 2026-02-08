---
description: Add or update lore documentation
---

# Add/Update Lore

Use this workflow to add new lore pages or update existing ones with new information.

## Prerequisites
- Know what category the lore belongs to (world, location, faction, bestiary)
- Source material (session transcript, planning docs)

## Lore Categories

| Category | Location | Examples |
|----------|----------|----------|
| **World Events** | `docs/lore/world/` | The Great Stitching, Integration Mechanics |
| **Locations** | `docs/lore/locations/` | Vumbua Academy, The Frontier |
| **Clans** | `docs/lore/factions/clans/` | Mizizi, Ash-Bloods, Trench-Kin |
| **Harmony Factions** | `docs/lore/factions/harmony/` | House Gilded, Iron Union |
| **Bestiary** | `docs/lore/bestiary/` | Ether-Jelly, Void-Beast |

## Steps for New Lore Page

1. **Create the file**
   - Filename: lowercase with hyphens (e.g., `the-great-stitching.md`)
   // turbo
   - Place in appropriate category folder

2. **Use the dual-track format**
   ```markdown
   # [Topic Name]

   ## What the Players Know
   [Player-facing lore - can be shared freely]

   ### [Subsections as needed]
   [Details organized logically]

   ---

   ## GM Secrets [HIDDEN FROM PLAYERS]

   > [!CAUTION]
   > The following information is NOT known to the player characters.

   [Hidden lore, future revelations, secret connections]
   ```

3. **Update navigation**
   - Add to `docs/lore/index.md`
   - Add to `docs/lore/glossary.md` if it defines new terms

4. **Update knowledge tracker**
   - Add entries to `docs/lore/knowledge-tracker.md`
   - Mark what players know (✅) vs don't know (❌)

## Steps for Updating Existing Lore

1. **Check what changed**
   - Review session transcript for new revelations
   - Identify what moved from "GM Secret" to "Players Know"

2. **Update the lore page**
   - Move revealed info from GM section to player section
   - Add new discoveries to player section
   - Update GM section with new secret implications

3. **Update knowledge tracker**
   - Change ❌ to ✅ for revealed information
   - Add new unknowns

4. **Commit changes**
   ```bash
   git add docs/lore/
   git commit -m "Update [topic] lore from Session N"
   git push
   ```

## File Locations
- Lore Hub: `docs/lore/index.md`
- Knowledge Tracker: `docs/lore/knowledge-tracker.md`
- Glossary: `docs/lore/glossary.md`
- Timeline: `docs/lore/timeline.md`
