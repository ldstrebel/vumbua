---
description: Add a new character profile (PC or NPC)
---

# Add Character Profile

Use this workflow to create a new player character or NPC profile.

## Prerequisites
- Character name and type (PC or NPC)
- Session(s) where they appeared
- Read `.agent/workflows/lore-index.md` to check if a profile already exists

## Steps

1. **Check for existing profile**
   - Search `docs/lore/characters/npcs/` for NPCs
   - Search `docs/characters/player-characters/` for PCs
   - If profile exists, update it instead of creating a new one

2. **Determine character type and location**
   - Player Character → `docs/characters/player-characters/`
   - NPC → `docs/lore/characters/npcs/`

3. **Create the character file**
   - Filename: lowercase with hyphens (e.g., `lady-ignis.md`)
   // turbo
   - Use the template structure below

4. **Fill in the profile**

   > **CORE RULE: Never hallucinate.** Only include details explicitly stated in session transcripts or GM narration. If a field is unknown, leave it blank or write "Unknown".

   Use this template:
   ```markdown
   # [Character Name]

   > *"Signature quote if available"*

   ## Overview

   | | |
   |---|---|
   | **Origin** | [Clan/Faction/Location] |
   | **Rank** | [If applicable] |
   | **Affiliation** | [Current role/group] |
   | **First Appearance** | [Session N] |

   ## GM Description
   [Physical description and details as narrated by the GM. Only include what the DM actually said.]

   ## Personality
   [Key traits and behavior as demonstrated in sessions]

   ## Background
   [Origin story and relevant history — only confirmed details]

   ## Session Appearances
   ### Session N
   - [What happened with this character]

   ## Relationships
   | Character | Relationship |
   |-----------|-------------|
   | **Name** | Description |

   ---

   ## GM Narration [NOT YET REVEALED TO PLAYERS]

   > [!CAUTION]
   > The following information has been narrated by the GM but is not known to the player characters.

   [Secret information, plot hooks, future plans — only from GM narration, never invented]
   ```

5. **Update the character index**
   - Add entry to `docs/characters/index.md`
   - Place in appropriate section (Students, Staff, Notable Figures)

6. **Cross-reference**
   - Link from any clan/faction pages if relevant
   - Update session recap if they appeared in one

7. **Update lore-index**
   - Add the new character to `.agent/workflows/lore-index.md` canonical spellings and character reference

8. **Commit changes**
   ```bash
   git add docs/lore/characters/ docs/characters/
   git commit -m "Add [Character Name] profile"
   git push
   ```

9. **Update changelog**
   - Append to `CHANGELOG.md` under today's date
   - Bullet: character added/updated, file path

## File Locations
- Player Characters: `docs/characters/player-characters/`
- NPCs: `docs/lore/characters/npcs/`
- Character Index: `docs/characters/index.md`
- Lore Index: `.agent/workflows/lore-index.md`
