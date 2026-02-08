---
description: Add a new character profile (PC or NPC)
---

# Add Character Profile

Use this workflow to create a new player character or NPC profile.

## Prerequisites
- Character name
- Know if they're a PC or NPC
- Session(s) where they appeared

## Steps

1. **Determine character type**
   - Player Character → `docs/characters/player-characters/`
   - NPC → `docs/characters/npcs/`

2. **Create the character file**
   - Filename: lowercase with hyphens (e.g., `lady-ignis.md`)
   // turbo
   - Use the template structure below

3. **Fill in the profile**
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

   ## Appearance
   [Physical description]

   ## Personality
   [Key traits and behavior]

   ## Background
   [Origin story and relevant history]

   ## Session Appearances
   ### Session N
   - [What happened with this character]

   ## Relationships
   | Character | Relationship |
   |-----------|-------------|
   | **Name** | Description |

   ---

   ## GM Notes [HIDDEN FROM PLAYERS]

   > [!CAUTION]
   > The following information is not known to the player characters.

   [Secret information, plot hooks, future plans]
   ```

4. **Update the character index**
   - Add entry to `docs/characters/index.md`
   - Place in appropriate section (Students, Staff, Notable Figures)

5. **Cross-reference**
   - Link from any clan/faction pages if relevant
   - Update session recap if they appeared in one

6. **Commit changes**
   ```bash
   git add docs/characters/
   git commit -m "Add [Character Name] profile"
   git push
   ```

## File Locations
- Player Characters: `docs/characters/player-characters/`
- NPCs: `docs/characters/npcs/`
- Character Index: `docs/characters/index.md`
