# Master Campaign Novelization Framework & Playbook

> **The Reusable TTRPG-to-Epic-Fantasy Blueprint**: This document synthesizes the entire architecture, auditing methodology, and narrative weaving framework developed for the *Vumbua* campaign. 
> 
> Use this playbook as a portable, turn-key index whenever starting a new campaign, novelizing tabletop gameplay, or passing instructions to an AI author/auditing agent.

---

## 📑 Master Index of Framework Components

```
                     CAMPAIGN NOVELIZATION FRAMEWORK
                     
  1. THE 4-LAYER DATA & PARITY ARCHITECTURE
     ├── Layer 1: Immutable Audio Manifest (Hash-Locked L#### indices)
     ├── Layer 2: Disentanglement & Session Config (Strict schema & shared mics)
     ├── Layer 3: Mathematical Ledger Parity (100% transcript accounting)
     └── Layer 4: Sanderson-Caliber Story Blocks (Scene staging & anchors)
     
  2. SESSION ZERO & CHARACTER CREATION ARCHITECTURE
     ├── Person-Level vs. PC Identity Contract (Anti-anachronism rule)
     ├── The "OOC" Semantic Shift (Canon creation vs. logistics/social)
     ├── Topic-Rotation Partitioning (Handoff cuts vs. spatial cuts)
     └── Author-Agent Sovereignty (Cross-session beat portability)
     
  3. DIFFERENTIAL MULTI-AGENT AUDITING (diff_runs.py)
     ├── Independent Benchmarking (Antigravity vs. Devin)
     ├── Substantive Attribution Diff (Catching silent speaker absorption)
     └── Skip-Rate as a First-Class Metric (Per-speaker retention matrix)
     
  4. ORCHESTRATION & EDITORIAL OVERREACH PROTOCOL
     ├── Failure Mode 1: POV Contamination (Meta-Name Leaks)
     ├── Failure Mode 2: Speculative Physics & Drama Overreach
     ├── Failure Mode 3: Confusing Clan Lore with Universal Truth
     ├── Failure Mode 4: Double-Event Redundancy (Tooling vs. In-World)
     └── Failure Mode 5: Silent Speaker Absorption (Shared-Mic Blindspots)
     
  5. PRE-STORY NARRATIVE WEAVING & FLOW AUDIT (The Author Gate)
     ├── Long-Horizon Trajectory Audit (Destination Awareness)
     ├── Anti-Frontloading Pacing Rule (Streamlined Prologue)
     ├── The 4-Part Narrative Weaving Matrix (Trigger ──► Cue ──► Origin ──► Seed)
     └── Monotonic Chapter Progression (Continuous 1...N Chapter Index)
     
  6. MASTER STORYBOARD & BOOK ARCHITECTURE
     ├── 5-Act Volume Structure (Acts I through V)
     ├── 5 Continuous Plot Lines (Cosmic, Survival, Political, Emotional, Wanderer)
     └── Chapter-by-Chapter Storyboard Beat Sheet
     
  7. PORTABILITY GUIDE: BOOTSTRAPPING A NEW CAMPAIGN
```

---

## 1. The 4-Layer Data & Parity Architecture

The core foundation of this framework guarantees **zero hallucination, zero narrative drift, and 100% auditable provenance** between spoken table audio and published fiction.

```
  Layer 1: Raw Indexed Audio (data/index/sN-raw-indexed.md)
           SHA-256 locked, 1-indexed lines (L0001..Lxxxx), verbatim text.
                           │
                           ▼
  Layer 2: Session Config & Decisions (config/sN-session-config.json)
           Declared GM, players, and shared-mic decompositions. Strict schema.
                           │
                           ▼
  Layer 3: Intermediate Story Blocks (clean/blocks/sN-scene-XX.md)
           Monotonic line coverage, dialogue dramatization, line anchors (<!-- Lxxxx -->).
                           │
                           ▼
  Layer 4: Compiled Novel Manuscript (clean/sN-clean-story.md)
           Continuous chapter headings, ledger footers, 100% verified parity.
```

### Key Scripts
* `prep_raw.py`: Normalizes diarization and stamps immutable `L0001` line numbers.
* `attribute_speakers.py`: Enforces strict session config declarations. Refuses undeclared identities.
* `assemble_story.py`: Compiles scene blocks into session manuscripts with ledger validation.
* `verify_parity.py`: Hard mathematical gate. Verifies that every single raw audio line is either rendered in prose or accounted for in the skipped ledger.

---

## 2. Session Zero & Character-Creation Architecture

Session Zero is fundamentally different from active gameplay sessions. Applying standard gameplay heuristics to a creation session destroys 80% of player worldbuilding.

1. **Person-Level vs. PC Identity Contract:**
   * *Rule:* In Session 0, player characters are unnamed and unplayed (characters do not exist as spoken identities).
   * *Config Schema:* The session config must map players to themselves (`players: {"Kristina": "Kristina", "John": "John"}`). Mapping players to future character names (e.g. `Aggie`) is anachronistic and violates strict schema validation (`players[person] == identity`).
2. **The "OOC" Semantic Shift:**
   * *Rule:* In standard gameplay (S1+), OOC marks table chatter vs. in-character action. In Session 0, *all speech is at the table*.
   * *Principle:* OOC must strictly separate **canon creation material** (clan lore, backstories, aesthetic choices, relationship seeds) from **non-canon social/logistics** (Google Forms links, dice roller bugs, personal travel chatter, audio artifacts). Treating creation talk as OOC causes a catastrophic 79% skip rate that silences player collaboration.
3. **Round-Robin / Topic-Rotation Partitioning:**
   * *Rule:* Session 0 has no physical environmental transitions. Block boundaries must follow the GM's round-robin **topic handoffs and thematic clusters** across player concepts.
4. **Author-Agent Sovereignty & Beat Portability:**
   * *Rule:* How Session 0 creation beats are surfaced (standalone prologue vs. woven flashbacks vs. backmatter) belongs strictly to the **author agent (orchestration layer)**. The pipeline's duty is delivering topic-segmented, anchored blocks whose ledger spans remain monotonic under cross-session movement.

---

## 3. Differential Multi-Agent Auditing (`diff_runs.py`)

When collaborating with independent AI agents (e.g. Antigravity vs. Devin), never rely on subjective text comparison. Use automated differential benchmarking.

### The Tool: `sessions/_scripts/diff_runs.py sN`
Generates an automated markdown comparison report (`sessions/_compare/sN-diff-report.md`) covering:

1. **Executive Metrics Matrix:** Word counts, scene counts, rendered turns, skipped turns, and logged assumptions.
2. **Substantive Attribution Disagreements:** Isolates genuine identity disagreements (e.g. `GM` vs. `Kristina` on a shared mic) while ignoring cosmetic string aliases (`Person` vs. `PC`).
3. **Skip-Rate as a First-Class Metric:**
   * **Per-Speaker Retention Table:** Measures raw turns, rendered turns, and skip percentages per character to expose which player voices were silenced.
   * **Line-Level Dropped Beat Catalog:** Lists every single collaborative line preserved by one run but dropped as `(ooc)` by the other, complete with speaker and raw transcript snippet.
   * **Inverted Drop Analysis:** Catalogs lines rendered in prose by one run that were skipped by the other.
4. **Explicit Assumptions & Review Flags:** Highlights ambiguity calls flagged in `sN-assumptions.json`.

---

## 4. Orchestration & Editorial Overreach Protocol

To ensure early-campaign worldbuilding remains completely retcon-safe and immersion-intact, every scene must pass the **Five Failure Mode Gates**:

| Failure Mode | Symptom | Rule & Solution |
|---|---|---|
| **1. POV Contamination (Meta-Name Leaks)** | Using world/faction names (e.g. "Harmony") in the thoughts of isolated clan members. | Characters only know what their senses and culture have experienced. Mizizi know "the strangers on the shore" and "the Paper Man," not the imperial entity "Harmony." |
| **2. Speculative Physics & Drama Overreach** | Inventing specific ship classes ("brass dreadnoughts") or military treaties from abstract GM metaphors. | Stick strictly to GM-stated metaphors. Committing to speculative military or technological mechanics creates false canon that breaks in future sessions. |
| **3. Confusing Clan Lore with Cosmic Truth** | Stating a local clan legend as an absolute narrator fact. | Present clan beliefs as *folklore, faith, or superstition*, especially when neighboring clans hold conflicting myths. |
| **4. Double-Event Redundancy** | Dramatizing table character surveys as a full in-world exam hall that duplicates an upcoming gameplay scene. | Distinguish table setup tooling from diegetic events. Frame setup around cultural context (broadsheets, city intake) rather than phantom pre-exams. |
| **5. Silent Speaker Absorption** | Defaulting shared-mic lines to the primary speaker (`Luke S -> GM`) at `confidence: 1.0`, erasing secondary speakers. | High confidence must never mask unverified attribution. Decompose shared streams and log explicit review flags in `sN-assumptions.json`. |

---

## 5. Pre-Story Narrative Weaving & Flow Audit (The Author Gate)

**The Golden Pacing Rule:** Never front-load 6,000 words of static worldbuilding before introducing characters taking active agency in the present.

### The 4-Part Narrative Weaving Matrix
Extract deep character backstories from the prologue and weave them directly into present-day story chapters as **reflective flashback beats**:

```
  [Present Action Trigger] ──► [Sensory / Emotional Cue] ──► [Origin Beat Revealed] ──► [Climax Seed / S12 Payoff]
```

1. **Present Action Trigger:** An active, physical event the character experiences in the present timeline *(e.g. Britt smashing the typewriter desk; Iggy tearing down the gantry; Ignatius on fire at the harbor; Lomi inspecting the cranes).*
2. **Sensory / Emotional Cue:** A physical sensation or pause that sparks the memory *(e.g. escaping the proctor into the crowd; blinking at open sky for the first time; watching a noble scrub soot from his skin).*
3. **Origin Beat Revealed:** The essential piece of clan lore, relationship dynamic, or personal philosophy from Session 0 that is dramatized *(e.g. the Mizizi's sacred decay; the Earthkin's terror of the void; the Ash-Blood's pride in raw hot rocks; the boilermaker's explorer knots).*
4. **Climax Seed (S12 Payoff):** The subtle clue or thematic contrast planted for the climax *(e.g. Iggy's water affinity; Lomi's mechanical intuition; Ignatius's belief in cooperation over cold knowledge).*

### Monotonic Novel Chapter Progression
* **Sessions $\neq$ Chapters:** Sessions are tabletop scheduling boundaries; Chapters are novel milestones.
* **Never reset to "Chapter 1" at the start of a new session.**
* Count chapters monotonically upward across the entire novel (`CHAPTER 1` through `CHAPTER N`). The novel begins with `PROLOGUE: [Title]`, Session 1 opens with `CHAPTER 1`, and alternating action and reflection chapters count upward continuously across all subsequent sessions.

---

## 6. Master Storyboard & Book Architecture

Consult [`campaign/planning/book-1-narrative-structure.md`](file:///d:/Code/vumbua/campaign/planning/book-1-narrative-structure.md) for the complete Volume 1 architecture (*The Basalt Run*, Sessions 0–12):

* **Act I: The Call of the Spires (Sessions 0–2.5):** Intake gauntlet, character origins, bonfire debate, power core infiltration.
* **Act II: Friction & Contraband (Sessions 3–6):** Classes, study guide hustles, Apex Ring scouting, Hangar 12 infiltration, The Minimum crisis.
* **Act III: The Proving Grounds (Sessions 7–8):** The Reso Race on the *Zephyr*, toxic shell crisis, written exam at Apex Arena, sorting into Squad 907.
* **Act IV: Five Sectors in the Sand (Sessions 9–11):** 24-hour scavenge in the 3-mile basin, rig construction, the storm breaking the spires, canopy beasts.
* **Act V: The Awakening of the Clans (Session 12):** Surviving the ruins, following Mwaza-Kasa, the shell of sparks, and the revelation of the deep ocean trenches.

### Five Persistent Plot Lines
* **Plot Line A (Cosmic):** The Six Sparks vs. The Minimum Crisis (Isolation as decay vs. exponential connection).
* **Plot Line B (Survival):** The Intake Gauntlet & Squad 907 (Culling vs. cross-clan interdependence).
* **Plot Line C (Political):** The Imperial Monopoly & The Paper Man (Council exploitation of frontier nodes).
* **Plot Line D (Emotional):** Cultural Exile & The Lie of Separation (Iggy, Lomi, Ignatius, Britt & Aggie).
* **Plot Line E (Wanderers):** The Wanderer's Trail (Rill & Zephyr).

---

## 7. Portability Guide: Bootstrapping a New Campaign

To reuse this framework for a brand new campaign or novel project:

1. **Initialize Directory Tree:**
   ```text
   sessions/
   ├── config/              <-- sN-session-config.json
   ├── data/
   │   ├── raw/             <-- sN-raw.md (unmodified recording audio)
   │   ├── index/           <-- sN-raw-indexed.md, sN-attribution.json, sN-manifest.json
   │   └── clean/           <-- sN-clean.md, sN-clean-story.md
   │       └── blocks/      <-- sN-scene-XX.md
   ├── planning/            <-- book-1-narrative-structure.md, campaign-narrative-bible.md
   ├── review/              <-- process-notes.md
   └── scripts/             <-- Python verification & compilation suite
   ```
2. **Copy Verification Tooling:**
   - Copy `prep_raw.py`, `session_config.py`, `attribute_speakers.py`, `assemble_story.py`, `verify_parity.py`, and `diff_runs.py` into `sessions/_scripts/`.
3. **Declare Session Config First:**
   - Declare GM, players, and shared mics in `config/sN-session-config.json` before writing any prose.
4. **Run the Pre-Story Flow Audit:**
   - Define the macro book structure, map chapters through the 4-part Weaving Matrix, and establish continuous chapter numbering.
5. **Enforce the Parity Gate:**
   - Require `verify_parity.py sN` to pass with 0 errors before generating storyboards or audiobooks.
