---
description: AI-facing quick reference for the Vumbua campaign repo
---

# Vumbua Campaign — Lore Index

> **Purpose**: Read this file FIRST before any session processing or lore work. It provides canonical spellings, character mappings, and a complete file map so you can work accurately without reading 10+ files.
>
> **Last Updated**: Session 2.5 (February 2026)

---

## Last Session Delta (Session 2.5: The Power Room)

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


**New NPCs introduced**: None ([[Tommy]], [[Lucina]], [[Marla]], [[Professor Kante]] already had files)
**New locations**: Power Plant interior (Walker-Core)
**Key reveals** ([[Iggy]] only):
- [[The Power System|Global Amplitude]] measures total ether energy — has been declining 30-40 years (unprecedented)
- Ash-Blood integration produced only ~20 amps (expected +300 to +800)
- Panda 5 batteries are surge regulators/receptors, not storage — powered by umber crystals
- Night of Sparks (~400 years ago) burned the world for two months before umber crystals
- Kante's theory: integration works through cultural connection, not resource extraction
- Apex 1 battery line scrapped — Kante's career in jeopardy
- "Trail tales from the Trench" — [[Trench-Kin]] known to Harmony as border defenders
**Iggy's new assets**: Umber crystal from Kante, five connection experiments planned
**Plot threads opened**: Kante invited Iggy to return for tea and collaboration; Iggy's worldview challenged (connection vs. isolation)

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
| **Sophie** | **Britt** | Mizizi (gray fungal-turtle) | Gold | `docs/characters/player-characters/britt.md` |
| **Kristina** | **Aggie** | Mizizi (red-and-white spotted mushroom-turtle) | Silver | `docs/characters/player-characters/aggie.md` |
| **John** | **Ignatius** | Ash-Blood (Ember Islander) | Silver | `docs/characters/player-characters/ignatius.md` |
| **Luke F** | **Lomi** | Harmony-born (Octoumba, Iron-Union) | Copper | `docs/characters/player-characters/lomi.md` |
| **Holly** | **Iggy** | "Earthkin" (secretly Trench-Kin) | Gold | `docs/characters/player-characters/iggy.md` |

**Speaker attribution**: Use character name for in-character dialogue, player name for out-of-character talk. Determine from context.

---

## Key NPCs

### Academy Faculty & Staff

| NPC | Role | File |
|-----|------|------|
| **Dean Isolde Vane** | Head of Vumbua Academy | `docs/lore/characters/npcs/dean-isolde-vane.md` |
| **Celia Vance** | Operations Director | `docs/lore/characters/npcs/celia-vance.md` |
| **Senior Exploranaut Hesperus** | Instructor, Field Training | `docs/lore/characters/npcs/hesperus.md` |
| **Ratchet** | Copper-Rank Student, Block 99-Piston | `docs/lore/characters/npcs/ratchet.md` |
| **Kojo** | Mizizi Student, Help Desk Tutor | `docs/lore/characters/npcs/kojo.md` |
| **Pyrrhus** | Ash-Blood Student, Map Room Researcher | `docs/lore/characters/npcs/pyrrhus.md` |
| **Professor Kante** | Tortoise professor of harmonics | `docs/lore/characters/npcs/professor-kante.md` |

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

*All NPC files are in `docs/lore/characters/npcs/`*

### Notable Figures

| NPC | Role | File |
|-----|------|------|
| **Lady Ignis** | Ash-Blood Matriarch, Harmony High Councilor | `lady-ignis.md` |
| **Rill** | Wadi researcher (poses as Mizizi), Dean's assistant | `rill.md` |
| **Zephyr** | Storm-Kin exchange member, purple lightning | `zephyr.md` |
| **Lance** | Harmony Student (Independent?) | `lance.md` |
| **Valerius Sterling Sr.** | Legendary Explorer | `valerius-sterling-sr.md` |
| **Lady Glissade** | Harmony Noble | `lady-glissade.md` |
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
| Session 0 | `transcripts/s0-raw.md` | `transcripts/session-00.md` | ✅ Complete |
| Session 1 | `transcripts/s1-raw.md` | `transcripts/session-01.md` | ✅ Complete |
| Session 2 | (in s1-raw / bonfire_scene) | `transcripts/session-02.md` | ✅ Complete |
| Session 2.5 | `transcripts/s2.5-raw.md` | `transcripts/session-02pt5.md` | ✅ Complete |

---

## File Map

```
docs/                              # Public wiki content (GitHub Pages)
├── index.md                       # Campaign homepage
├── characters/
│   ├── index.md                   # Master character index (links to all PCs + NPCs)
│   ├── player-characters/         # 5 PC profiles (britt, aggie, ignatius, lomi, iggy)
│   └── npcs/                      # ⚠️ LEGACY — only 3 files, being deprecated
├── sessions/
│   ├── index.md                   # Session index with summaries
│   ├── _template.md               # Template for new session files
│   ├── bonfire_scene.md           # Standalone bonfire scene extract
│   ├── s2-planning.md             # Session 2 GM planning doc
│   ├── s2.5-planning.md           # Session 2.5 GM planning doc
│   └── transcripts/              # All raw + cleaned transcripts
│       ├── sN-raw.md              # Raw transcripts from sessions
│       └── session-NN.md          # Cleaned, organized session recaps
├── lore/
│   ├── index.md                   # Lore hub — links to all lore pages
│   ├── glossary.md                # A-Z term definitions (346 lines)
│   ├── timeline.md                # Full chronological history
│   ├── knowledge-tracker.md       # What players know vs GM secrets
│   ├── characters/npcs/           # ✅ CANONICAL NPC directory (45 files)
│   ├── factions/
│   │   ├── clans/                 # Clan lore pages
│   │   └── harmony/               # House/guild lore pages
│   ├── world/                     # World-building mechanics
│   ├── locations/                 # Location descriptions
│   └── bestiary/                  # Creature profiles
├── notebooklm/                    # Consolidated exports for NotebookLM ingestion
│   ├── campaign-compendium.md     # Full world reference (740 lines)
│   ├── campaign-chronicle.md      # Timeline + session history
│   ├── character-codex.md         # All character profiles merged
│   └── gm-master.md              # GM-only secrets consolidated
├── gm-notes/                      # Private GM prep (excluded from Pages)
└── mechanics/                     # Daggerheart system reference

Vumbua/                            # Original source documents (being migrated)
├── Lore/                          # Raw lore notes
└── Sessions/                      # Original session scripts

.agent/workflows/                  # AI workflow instructions
├── add-session.md                 # Process raw transcripts → cleaned recaps
├── add-character.md               # Create PC/NPC profiles
├── add-lore.md                    # Add/update world lore pages
├── deploy.md                      # Deploy to Netlify
├── lore-index.md                  # THIS FILE — AI quick reference
└── human-instructions.md          # User guide for leveraging AI workflows
```

### Key Distinctions

| Directory | Purpose | Updated By |
|-----------|---------|------------|
| `docs/lore/` | Source of truth for all lore | AI via `/add-lore` |
| `docs/lore/characters/npcs/` | Canonical NPC profiles | AI via `/add-character` |
| `docs/characters/` | Character index + PC profiles | AI via `/add-character` |
| `docs/notebooklm/` | Consolidated exports for NotebookLM | Manual re-export after major updates |
| `docs/sessions/transcripts/` | Raw + cleaned session files | AI via `/add-session` |
| `Vumbua/` | Original source docs (legacy) | Not actively updated |
