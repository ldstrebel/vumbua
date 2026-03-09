# Vumbua Campaign Repository

A **Daggerheart campaign** set in a Magitek-Steampunk world inspired by *Atlantis: The Lost Empire*.

**System:** Daggerheart (v1.5/1.6) | **Current Session:** 2.5 | **Schedule:** Every 2 weeks | **Party Size:** 5

**[View the Campaign Wiki](https://ldstrebel.github.io/vumbua/)**

---

## First Time Here? (AI or Human)

| Step | What to read | Why |
|------|-------------|-----|
| 1 | `.agent/workflows/ai-entry.md` | 30-second story summary, cast, current plot state |
| 2 | `.agent/workflows/lore-index.md` | Canonical spellings, file map, NPC roster, session delta |
| 3 | `sessions/index.md` | What happened each session |
| 4 | `knowledge-tracker.md` | What players know vs. what's hidden |

For **humans** wanting to use AI workflows: `.agent/workflows/human-instructions.md`

---

## Quick Links

| For... | Go to... |
|--------|----------|
| Story + current state (AI) | `.agent/workflows/ai-entry.md` |
| Canonical spellings + file map (AI) | `.agent/workflows/lore-index.md` |
| How to use AI workflows (humans) | `.agent/workflows/human-instructions.md` |
| Session recaps | `sessions/index.md` |
| Campaign hub | `index.md` |
| Terms & definitions | `glossary.md` |
| Timeline | `timeline.md` |
| All characters | `characters/index.md` |
| All locations | `locations/index.md` |

---

## The Setting

**The Great Stitching** is a process where isolated civilizations and their reality-Nodes are physically integrated into a growing empire called **Harmony**. Vumbua Academy is a mobile city-state that has just relocated to a new frontier after 80 years of stagnation.

The party of five unlikely students must navigate:
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
index.md                          # Campaign hub (includes former lore hub)
glossary.md                       # A-Z terms
timeline.md                       # Full chronological history
knowledge-tracker.md              # Player knowledge vs GM narration

characters/                       # ★ ALL CHARACTER PROFILES
├── index.md                      # Character codex (PCs + NPCs)
├── player-characters/            # 5 PC profiles
└── npcs/                         # ★ CANONICAL NPC profiles (45+ files)

sessions/                         # Session transcripts + planning
├── index.md                      # Session recap index
├── transcripts/
│   ├── raw/                      # Raw transcript input (sN-raw.md)
│   └── clean/                    # Cleaned session output (session-NN.md)
└── planning/                     # GM session prep

factions/                         # Clans + Harmony houses
world/                            # World mechanics
locations/                        # Place descriptions
bestiary/                         # Creature profiles

meta/                             # ★ APP MANAGEMENT & TOOLING
├── scripts/                      # Python/bash automation scripts
├── docs/                         # Jekyll/NotebookLM exports
├── exports/                      # Export output
├── radio-scripts/                # Radio-style session recaps
├── Excalidraw/                   # Excalidraw test files
├── Ink/                          # Ink drawing/writing files
├── Daggerheart-Core/             # System reference PDFs
└── legacy/                       # Pre-migration source material
    ├── Vumbua/                   # Original source documents
    └── lore-dump/                # Temporary lore imports

.agent/workflows/                 # AI + human workflow instructions
├── ai-entry.md                   # AI onboarding brief (read FIRST)
├── lore-index.md                 # AI quick reference (spellings, file map)
├── add-session.md                # Process raw transcripts
├── add-character.md              # Create/update character profiles
├── add-lore.md                   # Add/update world lore
├── radio-recap.md                # Generate radio recap scripts
├── deploy.md                     # Deploy to Netlify
└── human-instructions.md         # User guide for AI workflows
```

### Documentation Layers

| Layer | Purpose | Updated |
|-------|---------|---------|
| **Campaign content** (repo root) | Single source of truth for all campaign content | After each session via AI workflows |
| **NotebookLM exports** (`meta/docs/notebooklm/`) | Consolidated copies for NotebookLM ingestion | Manually re-exported after major updates |
| **Legacy docs** (`meta/legacy/`) | Original pre-migration source material | Not actively maintained |
| **AI reference** (`.agent/workflows/lore-index.md`) | Quick reference for AI session processing | After each session |

---

## Dual-Track Documentation

Lore pages include both **player-facing information** and **GM narration** (not "secrets" — this is narrated content from real-play sessions):

- **"What Players Know"** sections are safe to share
- **"GM Narration"** sections contain unrevealed DM content, marked with caution boxes
- `knowledge-tracker.md` tracks what's been revealed

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
| **Processing a session** | `knowledge-tracker.md`, `timeline.md`, `.agent/workflows/lore-index.md` (session delta + session status), `CHANGELOG.md` |
| **Adding/updating a character** | `characters/index.md`, `.agent/workflows/lore-index.md` (NPC list + spellings), `CHANGELOG.md` |
| **Adding/updating lore** | `index.md`, `glossary.md` (if new terms), `.agent/workflows/lore-index.md`, `CHANGELOG.md` |
| **Any AI action** | `CHANGELOG.md` — date-stamped bullet with TLDR + file(s) changed |

---

## Changelog

All AI-driven changes are logged in `CHANGELOG.md` with date stamps. Every workflow appends to this file upon completion.

---

## Deployment

Deploy changes via the `/deploy` workflow or manually:

```bash
git add index.md characters/ sessions/ factions/ world/ locations/ bestiary/ glossary.md timeline.md knowledge-tracker.md
git commit -m "Session XX recap and lore updates"
git push
```

---

## License

Campaign content © 2026 ldstrebel

*This is a personal campaign wiki. Content may reference Daggerheart rules (Darrington Press) but all lore, characters, and story are original.*
