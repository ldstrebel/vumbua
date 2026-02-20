---
description: AI onboarding brief for the Vumbua campaign
aliases:
- AI Entry
- Campaign Brief
- Vumbua Brief
---

# Vumbua Campaign — AI Entry Brief

## What this document is
A fast on-ramp for an AI agent to understand **the setting, the cast, the current plot state, and where the canonical files live**.

If you’re doing any content work, also read: **[[lore-index|Lore Index]]** (`.agent/workflows/lore-index.md`) for canonical spellings + file map.

---

## Canon / provenance rules (do not blur these)
- **transcript**: spoken/seen in-session (highest confidence)
- **gm-narration**: narrated by GM but not yet known to PCs (canon, but hidden from players)
- **gm-plan**: prep/intent not yet occurred in-session (not canon yet)
- **legacy**: older pre-migration docs; may be superseded by transcripts

**Canonical source of truth lives in the repo root**, especially:
- `sessions/transcripts/raw/` (raw transcript input)
- `sessions/transcripts/clean/` (cleaned transcript output)
- `knowledge-tracker.md` (what players know)
- `timeline.md`

---

## Setting (30-second summary)
**The Great Stitching** is Harmony’s process of physically integrating isolated civilizations (and their “Nodes” of reality) into a growing magitek-steampunk empire. **[[vumbua-academy|Vumbua Academy]]** is a mobile city-state / academy that has relocated to a new frontier after ~80 years of stagnation.

Themes/pillars:
- Integration vs extraction (cultural connection matters)
- House politics inside Harmony
- Newly integrated clans and cultural tension
- A looming systemic crisis: Harmony’s ether power baseline is failing

---

## The Party (PCs)
| Player | Character | Clan/Origin | Rank | File |
|---|---|---|---|---|
| Sophie | Britt | Mizizi | Gold | `characters/player-characters/britt.md` |
| Kristina | Aggie | Mizizi | Silver | `characters/player-characters/aggie.md` |
| John | Ignatius | Ash-Blood | Silver | `characters/player-characters/ignatius.md` |
| Luke F | Lomi | Harmony-born (Octoumba, Iron-Union) | Copper | `characters/player-characters/lomi.md` |
| Holly | Iggy | "Earthkin" (secretly Trench-Kin) | Gold | `characters/player-characters/iggy.md` |

---

## Current campaign status (as of Session 2.5)
Arc: **The Intake** (first days at Vumbua)

Read these first:
- Session index: `sessions/index.md`
- Cleaned transcripts:
  - Session 0: `sessions/transcripts/clean/session-00.md`
  - Session 1: `sessions/transcripts/clean/session-01.md`
  - Session 2: `sessions/transcripts/clean/session-02.md`
  - Session 2.5: `sessions/transcripts/clean/session-02.5.md`

Recent key beats:
- The party forms during trials + early campus life.
- A bonfire at Block 99 becomes a major social/political exposition scene.
- **[[zephyr|Zephyr]]** manifests a **purple lightning** event (Session 2).
- **Session 2.5 (Iggy solo)** reveals major system-level stakes via **[[professor-kante|Professor Kante]]**:
  - **[[The Power System|Global Amplitude]]** (Harmony’s total ether power) has been declining 30–40 years.
  - The **Ash-Blood integration** produced ~20 amps (expected +300 to +800).
  - “Panda 5” resonator batteries are surge regulators (umber-crystal driven), not storage.
  - Integration may succeed through **cultural connection**, not extraction.

---

## High-signal NPCs (first-pass)
Faculty/staff:
- [[dean-isolde-vane|Dean Isolde Vane]]
- [[celia-vance|Celia Vance]]
- [[hesperus|Hesperus]]
- [[ratchet|Ratchet]]
- [[kojo|Kojo]]
- [[pyrrhus|Pyrrhus]]

Other high-signal:
- [[lady-ignis|Lady Ignis]] (Harmony power structure)
- [[rill|Rill]] (Mizizi researcher; important thread)
- [[serra-vox|Serra Vox]] / [[valerius-sterling|Valerius Sterling]] (student politics/rivals)

Canonical list lives at: `characters/index.md`

---

## Where to go depending on the task
- “What happened last session?” → `sessions/index.md` then latest cleaned transcript
- “What can players know?” → `knowledge-tracker.md`
- “Who is this NPC/term?” → `characters/index.md`, `glossary.md`
- “What files exist / where should I edit?” → `.agent/workflows/lore-index.md`

---

## If you only read 3 files
1. `.agent/workflows/lore-index.md`
2. `sessions/index.md`
3. `knowledge-tracker.md`
