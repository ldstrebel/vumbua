---
description: Add a new character profile (PC or NPC)
---

# Add Character Profile

Use this workflow to create a new player character or NPC profile.
There are two modes: **Stub** (minimal, for live-session reveals) and **Full** (after session, with transcript details).

---

## Mode A — NPC Stub (live session or prep)

Use this when an NPC is about to appear and you want them in Foundry with just a name and portrait — no detailed write-up yet.

**What you need:** Name, session number, portrait image (if available)

### Steps

1. **Create the minimal file**

   Filename: `characters/npcs/[kebab-name].md` (lowercase, hyphens)

   ```markdown
   # [Character Name]

   | | |
   |---|---|
   | **Role** | [1–3 words, e.g. "Maintenance Worker"] |
   | **First Appearance** | [[session-N\|Session N]] |
   ```

   That's the minimum. The `First Appearance` tag is the only field `build_codex.py` needs to include this NPC.

2. **Add a portrait** (optional but recommended)

   - Save the image to `meta/foundry-exports/portraits/[slugified_name]_portrait.png`
   - Slug rule: lowercase → remove quotes/punctuation → spaces to underscores
     - "Professor Kante" → `professor_kante_portrait.png`
     - `Seraphina "Serra" Vox` → `seraphina_serra_vox_portrait.png`
   - Any resolution is fine — the build script auto-compresses to ~40 KB JPEG

3. **Rebuild and import**

   ```bash
   cd vumbua/meta/foundry-exports
   python build_codex.py          # full rebuild
   # or
   python build_codex.py N        # delta — only session N page + new NPCs
   ```

   Copy `vumbua-codex.json` → paste into the Foundry macro.

4. **Fill in the profile later** using Mode B below after the session.

---

## Mode B — Full Profile (post-session)

Use this after a session when you have transcript details.

### Prerequisites
- Character name and type (PC or NPC)
- Session(s) where they appeared
- Check `characters/npcs/` — if a stub already exists, update it instead of creating a new file

### Steps

1. **Check for existing profile**
   - Search `characters/npcs/` for NPCs; `characters/player-characters/` for PCs
   - If a stub exists from Mode A, add to it — never overwrite

2. **Fill in the profile using the template**

   > **CORE RULE: Never hallucinate.** Only include details explicitly stated in session transcripts or GM narration. If a field is unknown, leave it blank or write "Unknown".
   >
   > **CORE RULE: Add, don't replace.** When updating an existing profile with new session info, ADD new entries — never overwrite earlier descriptions.

   ```markdown
   # [Character Name]

   > *"Signature quote if available"*

   | | |
   |---|---|
   | **Origin** | [Clan/Faction/Location] |
   | **Role** | [Role at time of first appearance] |
   | **Affiliation** | [Current group/faction] |
   | **First Appearance** | [[session-N\|Session N]] |

   ## Overview
   [2–3 sentences: who they are, what the players know. Player-facing only.]

   ## Personality
   [Key traits as demonstrated in sessions — no speculation]

   ## Session Appearances
   ### Session N
   - [What happened with this character this session]

   ## Relationships
   | Character | Relationship |
   |-----------|-------------|
   | **[[Name]]** | Description |

   ## Source References
   - **[[session-N\|Session N]]** — [scene context]

   ---

   ## GM Narration

   > [!warning]-
   > The following information is not known to the player characters.

   [Secret details, hidden motivations, future plot hooks — GM only]
   ```

3. **Update the character index**
   - Add entry to `characters/index.md` under the appropriate section

4. **Cross-reference**
   - Link from any clan/faction pages if relevant
   - Update `characters/index.md` with the new NPC

5. **Update lore-index**
   - Add the new character to `.agent/workflows/lore-index.md` canonical spellings

6. **Rebuild Foundry export** (see `update-foundry-journals.md`)

---

## Spoiler safety rules for character profiles

| Section heading | Stripped by pipeline? |
|---|---|
| `## Overview`, `## Personality`, `## Relationships`, `## Session Appearances`, `## Source References` | **Included** — player-facing |
| `## GM Narration`, `## GM Notes`, `## GM Description`, `## Secret`, `## Hidden` | **Stripped** — never reaches players |
| `> [!warning]-` callout blocks | **Stripped** |

Never put hidden information in a player-facing section. If it's in `## Overview`, players will see it.

---

## File locations

| Type | Location |
|---|---|
| Player Characters | `characters/player-characters/` |
| NPCs | `characters/npcs/` |
| Portrait sources | `meta/foundry-exports/portraits/` |
| Character index | `characters/index.md` |
| Lore reference | `.agent/workflows/lore-index.md` |
