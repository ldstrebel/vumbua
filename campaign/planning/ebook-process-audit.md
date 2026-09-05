# Ebook Transformation & Editorial Harness — Process Audit & Architecture Review

**Target:** External Reviewing / Auditing Agent  
**Document Type:** Story-Agnostic Process Audit & Handoff  
**Version:** 1.0.0  
**Scope:** TTRPG Raw Audio Transcripts $\rightarrow$ Literary Ebook Novels

---

## 🎯 Executive Summary & Mission

This document outlines an end-to-end editorial pipeline and deterministic software harness designed to transform raw, multi-speaker, conversational tabletop roleplaying game (TTRPG) transcripts into publication-grade, long-form novels (e.g. Brandon Sanderson or Joe Abercrombie style) while maintaining absolute canon fidelity to the original gameplay session.

### Core Philosophy: Player Canon & Soul Over Literary Smoothing
When transferring across mediums (from chaotic oral gameplay to literary prose), many AI workflows commit the fatal error of **"literary sanitization"**: replacing weird, funny, or specific player choices with bland, generic prose tropes. 

Our cardinal rule is:
> **Fidelity Over Polish**: We prioritize capturing what the players actually describe, say, and do. We do not retcon or smooth over player actions. Connective tissue (sensory details, physical mannerisms, internal reflections) must *serve* the players' comedic and dramatic intent, never replace it.

---

## 🏗️ The 5-Stage System Architecture

```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ STAGE 0: GROUND-TRUTH & STREAM DISENTANGLEMENT (Hard Config Gate)       │
  │  • Session config declares GM, player roster, and shared microphones.   │
  │  • Pipeline refuses to infer identities or guess mic sharing.           │
  └────────────────────────────────────┬────────────────────────────────────┘
                                       │
                                       ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ STAGE 1: IMMUTABLE LINE NUMBERING & MANIFEST LEDGER (0 Tokens)          │
  │  • Raw text indexed with permanent line numbers (L0001:, L0002:).       │
  │  • LLM/Python slices session into contiguous 80–150 line scene blocks.  │
  │  • Explicit dialogue ledger created for every spoken turn.              │
  │  • Python gate verifies: zero line gaps, zero overlaps, hash locked.    │
  └────────────────────────────────────┬────────────────────────────────────┘
                                       │
                                       ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ STAGE 2: CONTEXT-BRIDGED MICRO-CHUNK NOVELIZATION (Scoped LLM)          │
  │  • Novelize ONE scene block per pass (never whole transcripts).         │
  │  • Injects a compact ~200-token Context Bridge (location, gear, state). │
  │  • Embeds line markers (<!-- Lxxxx -->) and ledger footers.             │
  │  • Saves block: clean/blocks/sN-scene-XX.md                             │
  └────────────────────────────────────┬────────────────────────────────────┘
                                       │
                                       ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ STAGE 3: THE 3-LAYER EDITORIAL & READER AUDIT SUITE                     │
  │  • Layer 1: Deterministic Python Linter (Leaks, echoes, style, lore).   │
  │  • Layer 2: Orchestration Author (Macro story arc, foreshadowing).      │
  │  • Layer 3: Cold Alpha Reader (Spatial clarity, empathy, confusion idx).│
  └────────────────────────────────────┬────────────────────────────────────┘
                                       │
                                       ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ STAGE 4: CHECKPOINTED ASSEMBLY & BATCH SCHEDULING                       │
  │  • assemble_story.py merges verified blocks into complete story file.   │
  │  • Checkpoint cache skips previously validated blocks.                  │
  │  • Batch scheduler throttles execution for unattended/nightly runs.     │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## 🔍 The 3-Layer Editorial Engine in Detail

To prevent both mechanical errors and literary blindness, audits occur in three distinct, sequential layers:

### Layer 1: The Deterministic Mechanical Linter (Pure Python, 0 Tokens)
Runs locally in milliseconds before any human or LLM review:
1. **Deny-List & Leak Detector**:
   - Catches real player names with regex word boundaries.
   - Detects TTRPG system mechanics (`Roll20`, `D20`, `armor slot`, `saving throw`, `hit points`).
   - Identifies technical audio artifacts (`wi-fi`, `mic check`, `mute yourself`, `push to talk`, `screenshare`).
   - Bans embedded italic dialogue (e.g. `*I don't know,* she said`), enforcing standard quoted dialogue (`"..."`) with dedicated paragraphs.
2. **Proximity Echo & Repetition Detector**:
   - Uses sliding n-grams (3–5 words) to catch proximity echoes within a 400-word window.
   - Flags sentence starter monotony (3+ consecutive sentences opening with the same pronoun or structure).
   - Audits filter-word density (weak fiction crutches like `felt like`, `seemed to`, `could hear`, `suddenly`, `started to`) per 1,000 words.
3. **Style & Pacing Analytics (ProWritingAid / AutoCrit Model)**:
   - Calculates sentence length mean and standard deviation (ensuring dynamic musical prose rather than monotone drone).
   - Measures dialogue vs. narrative prose ratio (targeting optimal 30%–55% dialogue for active scenes).
   - Flags dialogue tags relying on `-ly` adverbs (`said angrily`), recommending active physical character beats.
   - Evaluates sensory register coverage (Sight, Sound, Smell/Taste, Touch/Kinetic, Magic/Energy).
4. **Lore & Tense Guardian (ProofreaderPro Model)**:
   - Detects speech-to-text (STT) phonetic drift.
   - Enforces third-person past tense throughout narrative prose, catching accidental present-tense slips (`Britt turns and watches`).
5. **Ledger Parity Gate (`verify_parity.py`)**:
   - Reconciles every raw line number against the scene ledger: every spoken turn must be either rendered in quotes or explicitly marked as skipped (e.g., OOC table talk).

---

### Layer 2: The Orchestration Author (Developmental Showrunner)
*Evaluates the chapter from 30,000 feet across the multi-session campaign arc.*
* **Information Density & Lore Seeding**: Are world concepts introduced through tactile props and interactions, or did the author infodump?
* **Foreshadowing & Payoff Tracks**: Are clues for future arcs planted early? Does this chapter contradict past or future canonical events?
* **Macro Pacing & Tension Curves**: Does the session follow a clear dramatic arc (Beginning hook $\rightarrow$ Escalating crisis $\rightarrow$ Cliffhanger/Resolution)?
* **Theme & Motif Tracking**: Are core campaign philosophical themes actively felt in the character dilemmas?

---

### Layer 3: The "Potential Reader" (The Cold Alpha Reader)
*Evaluates the prose with zero knowledge of the gaming table, character sheets, or GM notes.*
* **The "Confusion Index" & Spatial Geography**: Can a reader who was not at the table picture the room? Where are characters standing? What do key objects look like?
* **Empathy Anchors**: Does the reader understand *why* characters take risks? Are internal motivations, vulnerabilities, and emotional stakes transparent?
* **The "Cold Reader" Lore Rule**: Never assume the reader knows background lore. If a concept appears, it must be introduced through physical observation, not unanchored proper nouns.
* **Comedic & Dramatic Landing**: Audio comedy often relies on player laughter and vocal cadence; in prose, humor must be staged with clear comedic timing (**Setup $\rightarrow$ Escalation $\rightarrow$ Punchline $\rightarrow$ Reaction**).

---

## 💡 Token Economy & Micro-Chunk State Architecture

### The Anti-Summarization Micro-Chunk Method
* **The Problem**: Dumping 20,000–50,000 raw transcript tokens into an LLM causes severe summarization bias. The LLM compresses rapid dialogue exchanges, drops intermediate interjections, and hallucines events.
* **The Solution**: 
  - Transcripts are sliced into strictly bounded **80–150 line scene blocks**.
  - An LLM processes *only one scene block at a time*.
  - To maintain narrative continuity across blocks without re-sending the whole manuscript, each block emits and consumes a lightweight **`sN-scene-XX-state.json` Context Bridge**:
    ```json
    {
      "location_and_environment": "Basalt canyon riverbank, heavy morning mist, freezing rapids",
      "characters_present": [
        {"name": "Character A", "status": "levitating over water, fatigued"},
        {"name": "Character B", "status": "riding Character A's shoulders, flat cap smudged"}
      ],
      "key_items_or_props": ["ancient copper slate", "glass vial"],
      "immediate_preceding_action": "Character A stepped off the ledge to cross the rapids.",
      "emotional_tone_or_tension": "Exhausted relief after surviving the trials"
    }
    ```
  - Result: **70%+ token savings** and near-zero context drift.

---

## 📋 Evaluation Questions for the Auditing Agent

Please critically examine our framework and provide actionable critique, risk identification, and refinement suggestions across the following areas:

1. **Division of Labor (Python vs. LLM)**:
   - Are there checks currently assigned to the Python linter that require nuanced semantic understanding?
   - Conversely, are there tasks currently delegated to the LLM that could be handled deterministically at zero token cost?
2. **The "Player Intent vs. Prose Polish" Boundary**:
   - How should the pipeline handle player anachronisms or modern slang (e.g. a player joking about "Bluetooth" or "Costco")? When should it be adapted into an in-universe arcanatech equivalent vs. kept verbatim vs. flagged?
   - How can we systematically protect against the LLM "sanitizing" a player's chaotic or suboptimal roleplay choice into generic heroic competence?
3. **Multi-Speaker Diarization & Shared Microphones**:
   - In TTRPG recordings where two players share one physical microphone, or where players speak over each other in rapid cross-talk, what failure modes exist in our manifest ledger approach, and how can they be hardened?
4. **Macro Story Arc & Continuity Drift**:
   - As a campaign scales to 20+ sessions (hundreds of scenes), how can the Orchestration Author prevent cumulative continuity drift across separate `state.json` context bridges?
5. **Nightly / Unattended Batch Robustness**:
   - For unattended overnight batch processing, what circuit-breakers, retry policies, or validation checkpoints should be added to ensure a single failed block does not corrupt downstream story chapters?

---

*Handoff document ready for external agent audit.*
