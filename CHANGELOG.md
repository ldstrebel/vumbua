# Changelog

All AI-driven changes to the Vumbua campaign repo, in reverse chronological order.

---

## 2026-06-19

- **Surveyor Agent Protocols & Daggerheart integration**: Created the surveyor protocols workflow for building Daggerheart choice/dice surveys with GM preconditions check-ins, Stress, Hope/Fear, and Tier 1 loot tracking. Added references in human-instructions. → `.agent/workflows/surveyor-protocols.md`, `.agent/workflows/human-instructions.md`

## 2026-06-16

- **Session 6 Planning Refactoring**: Reorganized and expanded the Session 6 planning guide into a playable chronological Daggerheart v1.6 DM guide. Added Scene 1: Lomi's Crossroads (Union shift choice, study group ticket pressure, heist slip-past), Scene 2: Hangar Infiltration & Rill's Save (Prism Gate, Rovaldi monocle scan table, Rill's rescue & limits, pushing luck), Scene 3: Thursday morning class & Valerius's ticket confrontation (entourage escape roleplay, ground vs. air, Presence checks), Scene 4: The Reso Race Sandbox (Bleachers vs. Zephyr actions, grog selling with Lucky & Lomi, active NPC prompts, 4-beat roll-interpretation guide), Scene 5: Curfew & Study Night (Loom-Guard curfew enforcement, study guides checks), and Scene 6: The Written Exam & Confluence (Resonant Ink, Copper baseline math, Loom prophecies). → `sessions/planning/s6/S6 Planning.md`
- **Agent Alignment & Lore Sync**: Updated visual and mechanical campaign guidelines to reflect the clean Victorian-academic aesthetic, the Loom's organic confluence, and the empirical nature of harmonics → `.agent/workflows/lore-index.md`, `.agent/workflows/ai-entry.md`
- **Lore Corrections**: Refined Settika's Prism Falls water and the Loom's definitions to replace legacy calculated/sci-fi computer descriptions with the organic, conceptual imbuement, and diagnostic magic science → `locations/settika.md`, `world/harmony-nodes.md`, `glossary.md`, `locations/walker-core.md`

## 2026-03-09

- **New NPC**: Created Finch Gable (Harmony-born Logistics Student) → `characters/npcs/finch-gable.md`

## 2026-03-06

- **Full race simulation**: Created `world/circuit-run-simulation.md` — complete play-by-play for the First Vumbua Circuit-Run with all teams, full CU math per sync, terrain-band breakdown, Loom-Pulse sequence, major dramatic moments, final standings (Pudge wins), and GM narrative touchpoints keyed to each PC
- **Resonance Racers update**: Added Sail & Stun (Team 2) full profile to `characters/npcs/resonance-racers.md` — rig details (The Stinger-Ketch), strategy, Nyx connection, and Pudge alliance note; added simulation link header
- **Circuit-Run rule refinements**: Added **Rule Clarifications & Refinements** section to `world/circuit-run.md` covering: spire charge counts by tier, minimum 3-spire requirement, boon expiry clarification (one active boon per rig, holder-only expiry), Grand Resonator aerial approach ruling, disabled rig protocol, organic-drive (gryphon) ruling, and pre-race alliance optional rule; replaced TODO note with simulation link; updated Related Pages

- **Circuit-Run ruleset expansion**: Built a full Academy race rules reference with match flow phases, connection-deficit math, rig build/launch standards, full basin node ledger (CU + boons), and race-balance tuning levers → `world/circuit-run.md`

## 2026-02-17

- **Lore dump processing**: Integrated content from `lore-dump/onenote-temp.md` and `Taratannen.pdf`
- **Dean Isolde Vane rewrite**: Full NPC profile based on Session 1 canon (small, bouncy, scattered persona vs. planning doc) → `characters/npcs/dean-isolde-vane.md`
- **Great Surge endgame**: Added 2000+ amplitude spike detail (GM-only) to `world/power-system.md`
- **Harmony nodes**: Added faction ownership links (Gilded→Chime Spires, Vox→Umbra, Scrivener→Bloomfield) → `world/harmony-nodes.md`
- **NPC backstory audit**: Added GM-only backstory/bond/flaw/motive from lore dump to: Sarge, Lucky, Pudge, Pyrrhus, Kojo, Ratchet, Valerius Sterling
- **New NPC**: Created Soot (Lomi's Block 99-Piston roommate) → `characters/npcs/soot.md`
- **Lore-index update**: Updated NPC roles (Ratchet, Kojo, Pyrrhus), added Block 99-Piston entry

## 2026-02-16

- **Session 2.5 processed**: Cleaned transcript (`session-02pt5.md`) — Iggy's 1-on-1 power room exploration with Professor Kante. Updated session index, knowledge tracker, timeline, professor-kante.md, lore-index

- **Workflow overhaul**: Rewrote `add-session.md` with zero-detail-loss cleanup rules, IC/OOC speaker attribution, GM Narration terminology → `.agent/workflows/add-session.md`
- **Workflow update**: Updated `add-character.md` with GM Description/Narration terminology, no-hallucination rule → `.agent/workflows/add-character.md`
- **Workflow update**: Updated `add-lore.md` with GM Narration terminology, lore-index update steps → `.agent/workflows/add-lore.md`
- **New file**: Created `lore-index.md` — AI quick reference with canonical spellings, character mapping, factions, plot threads, file map → `.agent/workflows/lore-index.md`
- **New file**: Created `human-instructions.md` — user guide with prompt examples per workflow → `.agent/workflows/human-instructions.md`
- **New file**: Created `CHANGELOG.md` — date-stamped change log updated by all AI workflows → `CHANGELOG.md`
- **README rewrite**: Converted to AI rapid-index with quick links, annotated file structure, documentation layers, update dependencies → `README.md`
- **Deleted stale file**: Removed `sarah-fox.md` (duplicate of `serra-vox.md`) → `characters/npcs/sarah-fox.md`
