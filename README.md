# Vumbua Campaign Repository

A **Daggerheart campaign** set in a Magitek-Steampunk world inspired by *Atlantis: The Lost Empire*.

**System:** Daggerheart (v1.5/1.6) · **Current Session:** 2 · **Schedule:** Every 2 weeks · **Party Size:** 5

**[📖 View the Campaign Wiki](https://ldstrebel.github.io/vumbua/)**

---

## Quick Links

| For... | Go to... |
|--------|----------|
| **AI agents** — rapid orientation | [[Lore Index|`.agent/workflows/lore-index.md`]] |
| **Humans** — how to use AI workflows | [[Human Instructions|`.agent/workflows/human-instructions.md`]] |
| **Players** — catching up on sessions | [[Session Index|`sessions/transcripts/`]] |
| **Players** — learning the world | [[Lore Index|`lore/index.md`]] |
| **Quick reference** — terms & definitions | [[Glossary|`lore/glossary.md`]] |
| **Quick reference** — timeline | [[Timeline|`lore/timeline.md`]] |
| **Quick reference** — characters | [[Character Index|`characters/index.md`]] |

---

## The Setting

**The Great Stitching** is a process where isolated civilizations and their reality-Nodes are physically integrated into a growing empire called **Harmony**. [[Vumbua Academy]] is a mobile city-state that has just relocated to a new frontier after 80 years of stagnation.

Our party of five unlikely students must navigate:
- Political intrigue between Harmony's houses
- Cultural tensions with newly integrated clans
- The mystery of why integration sometimes fails
- Personal quests for identity, power, and truth

### The Party

| Player | Character | Clan/Origin | Rank |
|--------|-----------|-------------|------|
| Sophie | **Britt** | Mizizi (gray fungal-turtle) | Gold |
| Kristina | **Aggie** | Mizizi (red-and-white spotted mushroom-turtle) | Silver |
| John | **Ignatius** | Ash-Blood (Ember Islander) | Silver |
| Luke F | **Lomi** | Harmony-born (Octoumba, Iron-Union) | Copper |
| Holly | **Iggy** | "Earthkin" (Trench-Kin) | Gold |

---

## Repository Structure

```
characters/                        # Character profiles (Obsidian vault)
├── index.md                       # Master character index
├── player-characters/             # PC profiles (5 files)
└── npcs/                          # Notable NPCs with dual-vault copies

sessions/                          # Session transcripts + planning
├── transcripts/                   # Raw + cleaned session transcripts
│   ├── _template.md               # Template for new sessions
│   ├── sN-raw.md                  # Raw transcript input
│   └── session-NN.md              # Cleaned session output
└── planning/                      # GM session prep

lore/                              # ★ CANONICAL LORE (Obsidian vault)
├── index.md                       # Lore hub
├── glossary.md                    # A-Z terms
├── timeline.md                    # Full chronological history
├── knowledge-tracker.md           # Player knowledge vs GM narration
├── characters/npcs/               # ★ CANONICAL NPC profiles (45 files)
├── factions/                      # Clans + Harmony houses
├── world/                         # World mechanics
├── locations/                     # Place descriptions (14 files)
└── bestiary/                      # Creature profiles

docs/                              # Export / publish target
├── notebooklm/                    # Consolidated exports for NotebookLM
└── _config.yml                    # Jekyll config (if using GitHub Pages)

Vumbua/                            # Original source documents (legacy)

.agent/workflows/                  # AI + human workflow instructions
├── add-session.md                 # Process raw transcripts
├── add-character.md               # Create/update character profiles
├── add-lore.md                    # Add/update world lore
├── deploy.md                      # Deploy to Netlify
├── lore-index.md                  # ★ AI QUICK REFERENCE (read first)
└── human-instructions.md          # ★ USER GUIDE (how to use workflows)
```

### Documentation Layers

| Layer | Purpose | Updated |
|-------|---------|---------|
| **Obsidian vault** (`lore/`, `characters/`, `sessions/`) | Single source of truth for all campaign content | After each session via AI workflows |
| **NotebookLM exports** (`docs/notebooklm/`) | Consolidated copies for NotebookLM ingestion | Manually re-exported after major updates |
| **Legacy docs** (`Vumbua/`) | Original pre-migration source material | Not actively maintained |
| **AI reference** (`.agent/workflows/lore-index.md`) | Quick reference for AI session processing | After each session |

---

## Dual-Track Documentation

Lore pages include both **player-facing information** and **GM narration** (not "secrets" — this is narrated content from real-play sessions):

- **"What Players Know"** sections are safe to share
- **"GM Narration"** sections contain unrevealed DM content, marked with caution boxes
- The [[Knowledge Tracker]] tracks what's been revealed

### Truth tiers (reduces RAG confusion)
To prevent planned content from masquerading as session-truth, we treat information as one of:
- **transcript**: said/seen in-session (highest confidence)
- **gm-narration**: narrated by GM but not yet known to PCs (still canon, but hidden)
- **gm-plan**: prep/rosters/intent (not yet occurred in-session)

If something is `gm-plan` (e.g. a squad roster before the Loom selection happens), it must be clearly labeled and kept out of player-facing sections.

---

## Content Guidelines

### Session Recaps
- **Keep ALL story-relevant dialogue** — zero detail loss
- **Screenplay format** with speaker attribution (character name for IC, player name for OOC)
- **Scene-by-scene structure** for easy reference
- **Only correct 99%-confidence transcription errors** — never summarize or embellish
- See `.agent/workflows/add-session.md` for full rules

### Lore & Character Pages
- **Never hallucinate** — only record information from session transcripts or GM narration
- **Dual-track format**: "What Players Know" + "GM Narration"
- **Link between related pages** and update the Knowledge Tracker
- See `.agent/workflows/add-lore.md` and `.agent/workflows/add-character.md`

---

## Update Dependencies

When completing any task, the AI must update all downstream files. Use this as a checklist:

| After... | Always update... |
|----------|-----------------|
| **Processing a session** | `lore/knowledge-tracker.md`, `lore/timeline.md`, `.agent/workflows/lore-index.md` (session delta + session status), `CHANGELOG.md` |
| **Adding/updating a character** | `characters/index.md`, `.agent/workflows/lore-index.md` (NPC list + spellings), `CHANGELOG.md` |
| **Adding/updating lore** | `lore/index.md`, `lore/glossary.md` (if new terms), `.agent/workflows/lore-index.md`, `CHANGELOG.md` |
| **Any AI action** | `CHANGELOG.md` — date-stamped bullet with TLDR + file(s) changed |

---

## Changelog

All AI-driven changes are logged in [[Changelog|`CHANGELOG.md`]] with date stamps. Every workflow appends to this file upon completion.

---

## Deployment

Deploy changes via the `/deploy` workflow or manually:

```bash
git add lore/ characters/ sessions/
git commit -m "Session XX recap and lore updates"
git push origin main
```

---

## License

Campaign content © 2026 ldstrebel

*This is a personal campaign wiki. Content may reference Daggerheart rules (Darrington Press) but all lore, characters, and story are original.*
