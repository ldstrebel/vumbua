---
description: AI-facing quick reference for the Vumbua campaign repo
aliases:
- Lore Index
---

# Vumbua Campaign — Lore Index

> **Purpose**: Read this file FIRST before any session processing or lore work. It provides canonical spellings, character mappings, and a complete file map so you can work accurately without reading 10+ files.
>
> **AI onboarding**: Start with **AI Entry Brief** (`.agent/workflows/ai-entry.md`) for story + current-state summary.
>
> **Last Updated**: Session 2.5 (February 2026)

---

## Last Session Delta (Session 03: The Celestial Lounge and The Ambush)

New entities, reveals, and changes introduced in the most recent session. Update this after each session.

**Standard format (for diff-based updates):**

```markdown
## Session Delta (Session NN: <Title>)

### New / First-Mentioned Entities
- NPC: [[Name]] — <1-line context> — Source: [[session-NN|Session NN]] (Scene X)
- Location: [[Name]] — <1-line context> — Source: [[session-NN|Session NN]] (Scene X)
- Term: [[Name]] — <1-line context> — Source: [[session-NN|Session NN]] (Scene X)

### Updated Entity Pages
- [[Name]] — add/update “Session Appearances”

### Player Knowledge Changes
- Knowledge Tracker: ✅/❌ <bullet>

### Truth / Provenance Notes
- If something is GM planning (not spoken in-session), tag it as `gm-plan` and keep it out of player-facing sections.
```


**New NPCs introduced**: [[Azor]] (Settikan Schemer), [[Zyykl]] (Nstyl Bruiser), [[Tus]] (Nstyl Bruiser) - ambushers
**New locations**: [[Celestial Lounge]] (Upper Core)
**Key reveals**:
- Valerius wrote a challenging, fundamental-focused "study guide" for the upcoming exam and sold it to [[Lucky]]
- "Crown and Ruin" is a popular game played in the Celestial Lounge
- A coordinated group using sign language is operating in the city and targeting students
**Iggy's new assets**: "Cartography" experience trait
**Britt's changes**: Lost a test receipt during the ambush but fiercely recovered her family heirloom: a petrified acorn necklace. Took Azor's pocket watch as compensation.
**Lomi's changes**: Broke Azor's rib with an 18 damage roll while he was pinned/defeated during interrogation.
**Plot threads opened**: The party must find Lucky the next day to get the "study guide" using Azor's pocket watch and the embellished story of the ambush as leverage.

### Truth tiers (RAG safety)
- **transcript**: said/seen in-session
- **gm-narration**: narrated by GM but not yet known to PCs
- **gm-plan**: prep/rosters/intent not yet occurred in-session (do not treat as established canon)
- **legacy**: older docs; may be superseded by transcripts

---

## Canonical Spellings

These are the **correct** spellings. Transcription errors are common — always correct to these:

| Correct | Common Errors |
|---------|---------------|
| **Leidian** | Lasidian, Lydian, Leidien |
| **Seraphina "Serra" Vox** | Sarah, Sara, Sera, Sarah Fox |
| **Cassius Thorne** | Casius, Cassias |
| **Percival "Percy" Vane-Smythe III** | Percy Vane-Smith, Percival Van Smythe |
| **Iron-Jaw Jax** | Iron Jaw Jacks, Ironjaw |
| **Mizizi** | Misizi, Mizisi |
| **Ash-Bloods** | Ash Bloods, Ashblood |
| **Trench-Kin** | Trenchkin, Trench Kin |
| **Renali** | Renalli, Ranali |
| **Wadi** | Waddi, Waldi |
| **Fulgur-Born** | Fulgar, Fulgurn |
| **Rill** | Ryll, Ril |
| **Ember** | (no common errors) |
| **Zephyr** | Zephir, Zepher |
| **Vumbua** | Vumba, Vumbra |
| **Aether** | Ether (both acceptable) |
| **Exploranaut** | Exploranot, Explorenaut |
| **The Loom** | (no common errors) |
| **Sky-Spire** | Sky Spire, Skyspire |
| **Walker-Core** | Walker Core |
| **Deep-Hull** | Deep Hull, Deephull |

---

## Player ↔ Character Mapping

| Player (OOC) | Character (IC) | Clan/Origin | Rank | File |
|--------------|----------------|-------------|------|------|
| **Sophie** | **Britt** | Mizizi (gray fungal-turtle) | Gold | `characters/player-characters/britt.md` |
| **Kristina** | **Aggie** | Mizizi (red-and-white spotted mushroom-turtle) | Silver | `characters/player-characters/aggie.md` |
| **John** | **Ignatius** | Ash-Blood (Ember Islander) | Silver | `characters/player-characters/ignatius.md` |
| **Luke F** | **Lomi** | Harmony-born (Octoumba, Iron-Union) | Copper | `characters/player-characters/lomi.md` |
| **Holly** | **Iggy** | "Earthkin" (secretly Trench-Kin) | Gold | `characters/player-characters/iggy.md` |

**Speaker attribution**: Use character name for in-character dialogue, player name for out-of-character talk. Determine from context.

---

## Key NPCs

### Academy Faculty & Staff

| NPC | Role | File |
|-----|------|------|
| **Dean Isolde Vane** | Head of Vumbua Academy | `characters/npcs/dean-isolde-vane.md` |
| **Celia Vance** | Operations Director | `characters/npcs/celia-vance.md` |
| **Senior Exploranaut Hesperus** | Instructor, Field Training | `characters/npcs/hesperus.md` |
| **Ratchet** | Copper-Rank Student, Block 99-Piston | `characters/npcs/ratchet.md` |
| **Kojo** | Mizizi Student, Help Desk Tutor | `characters/npcs/kojo.md` |
| **Pyrrhus** | Ash-Blood Student, Map Room Researcher | `characters/npcs/pyrrhus.md` |
| **Professor Kante** | Tortoise professor of harmonics | `characters/npcs/professor-kante.md` |

### Student Squads

| Squad | Members | Files |
|-------|---------|-------|
| **01: The Echelon** | Valerius "Val" Sterling (Cpt), Seraphina "Serra" Vox, Cassius Thorne | `valerius-sterling.md`, `serra-vox.md`, `cassius-thorne.md` |
| **02: The Breakers** | Iron-Jaw Jax (Cpt), "Wall" Maria, Brawn | `iron-jaw-jax.md`, `maria-wall.md`, `brawn.md` |
| **03: The Silence** | Nyx (Cpt), Kaelen, Mira | `nyx.md`, `kaelen.md`, `mira.md` |
| **04: The Axiom** | Calculus Prime (Cpt), Theorem, Lemma | `calculus-prime.md`, `theorem.md`, `lemma.md` |
| **05: The Harvesters** | Dr. Rose Halloway (Cpt), Silas "Old Man" Thorne, Bramble | `dr-rose-halloway.md`, `silas-thorne.md`, `bramble.md` |
| **06: The Kiln** | Cinder-4 (Cpt), Hearth, Kindle | `cinder-4.md`, `hearth.md`, `kindle.md` |
| **07: The Bathysphere** | Captain Barnacle (Cpt), Pressure, Depth | `captain-barnacle.md`, `pressure.md`, `depth.md` |
| **08: The Legacy** | Percival Vane-Smythe III (Cpt), Lady Glimmer, Baron Bolt | `percival-vane-smythe-iii.md`, `lady-glimmer.md`, `baron-bolt.md` |
| **09: The Ablative** | Sarge (Cpt, Rust Tier), Lucky, Pudge | `sarge.md`, `lucky.md`, `pudge.md` |
| **Block 99-Piston** | Ratchet, Soot (Lomi's roommates) | `ratchet.md`, `soot.md` |

*All NPC files are in `characters/npcs/`*

### Notable Figures

| NPC | Role | File |
|-----|------|------|
| **Lady Ignis** | Ash-Blood Matriarch, Harmony High Councilor | `lady-ignis.md` |
| **Rill** | Wadi researcher (poses as Mizizi), Dean's assistant | `rill.md` |
| **Zephyr** | Storm-Kin exchange member, purple lightning | `zephyr.md` |
| **Lance** | Harmony Student (Independent?) | `lance.md` |
| **Valentine Sterling Sr.** | Legendary Explorer, Father of Valentine, Uncle of Valerius | `valentine-sterling-sr.md` |
| **Lady Glissade** | Harmony Noble | `lady-glissade.md` |
| **Valentine Sterling** | Radio Host, Sterling Family | `valentine-sterling.md` |
| **Ember** | Ash-Blood student, Ignatius's cousin, modernizer | `ember.md` |
| **Tommy** | Gnome clerk (power room, Session 2.5) | `tommy.md` |
| **Lucina** | Dwarf maintenance (power room, Session 2.5) | `lucina.md` |
| **Marla** | Human who failed out (power room, Session 2.5) | `marla.md` |

---

## Factions & Clans

### Harmony Houses (8)

| House | Domain | Key Detail |
|-------|--------|------------|
| **House Vane (The Shield)** | Defense, Walls | Dean Isolde is from here |
| **House Vox (The Spark)** | Energy, Crystal Batteries | Serra Vox is the runaway daughter |
| **House Sterling (The Sail)** | Trade, Logistics | Sterling Sr. discovered Mizizi |
| **House Gilded (The Vault)** | Treasury, Banking | Originally built Chime Spires |
| **Iron-Union** | Engines, Boilers | Lomi is a member (Diamond Union subset) |
| **Scrivener Guild** | Knowledge, Maps | Decoded integration mechanics |
| **The Verdant Trust** | Agriculture | Less relevant on frontier |
| **High-Justiciars** | Law, Balance | (The Scales) |
| **Grand Architects** | Construction | (House Mason) |
| **Syndicate of Sails** | Trade routes | Logistics |

### Clans (6) — The Shattered Circuit

| Clan | Node Role | Integration Status | Key Members |
|------|-----------|-------------------|-------------|
| **Mizizi** (Root-Kin) | Memory | 15% (stalled) | Britt, Aggie |
| **Ash-Bloods** (Ember-Kin) | Power | 100% (24 mo ago) | Ignatius, Ember, Lady Ignis |
| **Trench-Kin** (Earthkin) | Resources | 0% (uncontacted) | Iggy (secret) |
| **Renali** (Air Clan) | Vision | 0% (uncontacted) | Zephyr (exchange) |
| **Wadi** (River Clan) | Life | Unknown | Rill (secret identity) |
| **Fulgur-Born** (Storm-Chasers) | — | — | Zephyr (true clan) |

---

## Key Locations

| Location | Description |
|----------|-------------|
| **Vumbua Academy (The Safiri)** | Mobile city-state, 3 Cores, currently at Ash-Blood Isles |
| **Sky-Spire** | Golden airship — Command, Elite Dorms, Dean's office |
| **Walker-Core** | Four-legged mech — Engineering, Power, The Loom |
| **Deep-Hull** | Submersible — Storage, Archives, Research |
| **Spire-Scape** | 70% temporary scaffolding structures |
| **Block 99** | Industrial district, bonfire location (geothermal plant) |
| **Celestial Lounge** | Upscale club, NW "fancy district" |
| **Harmony Prime (The Seat)** | Capital city, ~8M people, High Council |
| **Ash-Blood Isles** | Volcanic chain, Vumbua's current location |
| **Mizizi Petrified Forest** | Stone mega-flora, stalled integration |
| **The Frontier** | Uncharted territories beyond Safe Lanes |

---

## Active Plot Threads

1. **[[The Minimum]] Crisis** — Harmony approaching power failure (state secret)
2. **Ash-Blood Anomaly** — Integration produced only ~20 amp increase (expected +300-800)
3. **[[Mizizi]] Integration Stall** — Forest won't integrate; forest is actually a data archive
4. **Shattered Circuit** — All 6 clans must integrate to stop the Bleed
5. **[[Iggy]]'s Infiltration** — [[Trench-Kin]] investigating why [[Ash-Bloods]] rejected Exchange
6. **Serra's Identity** — Runaway Vox daughter hiding noble status
7. **[[Rill]]'s Research** — Secretly [[Wadi]], investigating if forest destruction is necessary
8. **[[Zephyr]]'s Lightning** — Purple bolt from clear sky; managed by Rill for the Dean
9. **The Loom's Teams** — Upcoming team formation; fail = entire team expelled

---

## Session Status

| Session | Raw Transcript | Cleaned Transcript | Status |
|---------|---------------|-------------------|--------|
| Session 0 | `sessions/transcripts/raw/s0-raw.md` | `sessions/transcripts/clean/session-00.md` | ✅ Complete |
| Session 1 | `sessions/transcripts/raw/s1-raw.md` | `sessions/transcripts/clean/session-01.md` | ✅ Complete |
| Session 2 | `sessions/transcripts/raw/s2-raw.md` | `sessions/transcripts/clean/session-02.md` | ✅ Complete |
| Session 2.5 | `sessions/transcripts/raw/s2.5-raw.md` | `sessions/transcripts/clean/session-02.5.md` | ✅ Complete |
| Session 3 | `sessions/transcripts/raw/s4-raw.md` | `sessions/transcripts/clean/session-03.md` | ✅ Complete |

---

## File Map

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
├── transcripts/                  # Raw + cleaned session transcripts
│   ├── _template.md              # Template for new sessions
│   ├── sN-raw.md                 # Raw transcript input
│   └── session-NN.md             # Cleaned session output
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

.agent/workflows/                 # AI workflow instructions
├── add-session.md                # Process raw transcripts → cleaned recaps
├── add-character.md              # Create PC/NPC profiles
├── add-lore.md                   # Add/update world lore pages
├── deploy.md                     # Deploy to Netlify
├── lore-index.md                 # THIS FILE — AI quick reference
└── human-instructions.md         # User guide for leveraging AI workflows
```

### Key Distinctions

| Directory | Purpose | Updated By |
|-----------|---------|------------|
| repo root (index + top-level content dirs) | Source of truth for all campaign content | AI via workflows |
| `characters/` | Character index, PCs, and canonical NPC profiles | AI via `/add-character` |
| `sessions/` | Raw + cleaned session files + planning | AI via `/add-session` |
| `meta/docs/notebooklm/` | Consolidated exports for NotebookLM | Manual re-export after major updates |
| `meta/legacy/` | Original source docs (legacy) | Not actively updated |
