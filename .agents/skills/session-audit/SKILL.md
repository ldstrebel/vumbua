---
name: session-audit
description: Auditing, fixing, and maintaining parity across raw transcripts, clean attributed transcripts, novelized story blocks, and storyboards.
---

# Session Audit & Novelization Skill (Ebook Standard)

Use this skill when auditing session transcripts, cleaning dialogue, novelizing session chapters, or running post-mortems on prose quality and transcript fidelity.

---

## 🏛️ Ground-Truth Hierarchy

```
  ┌─────────────────────────────────────────────────────────┐
  │ 1. Raw Indexed Transcript (transcripts/index/sN-raw-indexed.md)│
  │    Immutable L#### line indices with raw audio.         │
  └────────────────────────────┬────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 2. Session Config (sessions/sN-devin/sN-session-config.json)│
  │    Declared GM, players, and shared mic mappings.       │
  └────────────────────────────┬────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 3. Attributed Clean Transcript (clean/sN-clean-attributed.md)│
  │    100% audited speaker attributions, table talk OOC    │
  │    declarations, turn stitching, and storyboard splices.│
  └────────────────────────────┬────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 4. Novelized Story Blocks (clean/blocks/sN-scene-XX.md)  │
  │    Sanderson-caliber prose, full scene staging,         │
  │    proper quoted dialogue, and line markers (<!-- Lxxxx -->).│
  └────────────────────────────┬────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 5. Graphic Novel Storyboard (storyboards/sN-storyboard.md)│
  │    Visual panel descriptions, verified profile tokens, │
  │    and baked verbatim dialogue bubbles.                │
  └─────────────────────────────────────────────────────────┘
```

---

## 🚫 Comprehensive Failure Modes & Post-Mortem Register

### 1. Gist-Level Manifest Truncation
* **Symptom:** High-value character dialogue, comedic beats, or world-tech explanations present in raw audio vanish from the novelization.
* **Root Cause:** Compressing raw transcript turns into summary bullets. Downstream prose generators never see the skipped turns.
* **Prevention:** Every spoken turn must be tracked in the manifest ledger and accounted for in prose.

### 2. Heuristic Keyword Coarseness
* **Symptom:** Audit tools report `[PASS]` even though critical spoken exchanges are completely missing.
* **Root Cause:** Checking binary keyword presence rather than verbatim line-by-line dialogue representation.
* **Prevention:** Never rely on regex matchers alone. Conduct granular scene-by-scene dialogue audits.

### 3. Fused Interjections & Turn Order Compression
* **Symptom:** Rapid speaker alternation gets collapsed into a single speaker's continuous monologue, dropping interjections.
* **Root Cause:** Skipping interjections as "table chatter".
* **Prevention:** Read multi-speaker clusters holistically. Every interjection must have its own prose beat.

### 4. OOC Table Talk vs. In-World Character Banter Misclassification
* **Symptom:** Real in-world banter stripped as table talk, or OOC meta questions novelized into in-universe canon.
* **Prevention:** Config-gated attribution with explicit `ooc_ranges` and `ooc_lines` declaring table talk with real names.

### 5. STT Phonetic Mishearings & Entity Name Drift
* **Symptom:** Names mangled (`Rill` $\rightarrow$ `Real`, `Professor Ink` $\rightarrow$ `Professor Inc.`, `Aggie` $\rightarrow$ `Nagy`, `Bramble` $\rightarrow$ `Vanball`, `Pip` $\rightarrow$ `Kim`).
* **Prevention:** Cross-reference every entity against `characters/` and `lore/` dossiers before writing scene blocks.

### 6. Clipped STT Lines Rendered as Stylistic Ellipsis
* **Symptom:** Incomplete STT lines rendered as intentional trailing-off rather than resolving the full sentence.
* **Prevention:** Flag all syntactically incomplete lines with `[CLIPPED]` and reconstruct intent from surrounding context.

### 7. Tier B Player Narration Rendered as Tier A In-World Dialogue
* **Symptom:** Player talking about their character in third person (*"Britt is just zoned"*) gets quoted as in-world speech.
* **Prevention:** Convert Tier B third-person player intent into vivid narrator prose and character action.

### 8. The "Dialogue-Dense Scene" Compression Trap
* **Symptom:** Scenes with 3+ simultaneous speakers compressed to a single-voice monologue.
* **Prevention:** In multi-speaker scenes (e.g. lab debates, bridge banter), write every speaker interjection as a separate paragraph with its own action beat.

### 9. Vision POV Inversion (First-Person vs. Second-Hand Outsider)
* **Symptom:** Ancestral visions written as immersive first-person possession rather than secondhand memories viewed through ancient eyes.
* **Prevention:** Frame visions through the Spirit Tortoise's memory: characters are witnesses watching secondhand history, not possessors.

### 10. Embedded / Italicized Summary Dialogue Anti-Pattern
* **Symptom:** Spoken dialogue is stripped of quotation marks and buried into running narrative sentences with em-dashes and italics (e.g., `*No, dude, they like me way more than you,* Pip said...`).
* **Root Cause:** Attempting to summarize conversational pacing rather than dramatizing the scene.
* **Prevention:** **STRICT BAN ON EMBEDDED ITALIC DIALOGUE.** All spoken character lines MUST be formatted as standard quoted dialogue (`"..."`) with proper paragraph breaks, dialogue tags, and physical beats.

### 11. Truncated Comedic Timing & Lost Character Dynamics
* **Symptom:** Comedic setups, escalations, punchlines, and physical slapstick (e.g., Pip realizing she volunteered, demanding the vial, slamming her forehead into the tree) are flattened into a single passive sentence.
* **Root Cause:** Treating comedic exchanges as "minor filler" rather than essential characterization.
* **Prevention:** Comedic beats must receive full scene staging: **Setup $\rightarrow$ Escalation $\rightarrow$ Punchline $\rightarrow$ Reaction**.

### 12. Player Game-State Clarification Rendered as In-World Character Dialogue
* **Symptom:** A player asking the GM an environmental or game-state question (*"Is the turtle still walking ahead of us?"*, *"Is the door open?"*, *"Can I see the bridge?"*) is rendered literally as spoken in-universe character dialogue.
* **Root Cause:** Treating all speech on a player's microphone as in-character speech without recognizing game-state clarification queries.
* **Prevention:** Translate player environment/state questions into sensory prose observations and character focus, not spoken dialogue by a character looking right at the object.

### 13. Anachronistic Naming & Harmony Name Collisions in Ancestral Visions
* **Symptom:** Using proper character names in narrative descriptions during secondhand memory sequences when the watching characters have never met or heard these ancient figures, or using names that overlap with modern Harmony characters (e.g. `Vox`).
* **Root Cause:** Treating storyboard shorthand as in-universe omniscient labels.
* **Prevention:** Use pure physical/clan descriptors for all ancient figures in narrative prose (*the root-kin elder*, *the smoldering ember chieftain*, *the sky-weaver*, *the Empress of the Golden Age*). Only use spoken names if they are declared in-universe, and ensure they are uniquely clan-driven with zero modern Harmony collisions.

### 14. Dialogue Paraphrase & Summary Compression (The "Told, Not Shown" Trap)
* **Symptom:** Key verbal exchanges (e.g. Lomi bantering with the goblin driver, Aggie comforting Val, Ignatius flirting with Zephyr) are summarized into a narrator sentence rather than written out as active dialogue.
* **Root Cause:** Prioritizing word economy over character voice and emotional immersion.
* **Prevention:** If characters speak in the raw audio, write out the verbatim dialogue lines with emotional cadence and micro-actions.

### 15. Broken Sequential Cause-and-Effect Bridges
* **Symptom:** An action or line happens without the prerequisite trigger (e.g., Pip yelling about not dying before Aggie explains that they have to come with the turtle).
* **Root Cause:** Dropping connective lines between speakers during scene drafting.
* **Prevention:** Trace every conversation as an unbroken causal chain: **Trigger $\rightarrow$ Reaction $\rightarrow$ Resolution**.

### 16. Dropped World-Media & Atmospheric Broadcasts
* **Symptom:** Radio broadcasts, speaker horns, public speeches, and ambient environmental lore (e.g., Valerius Sterling's radio dispatches, naval cannon salutes, background clinic triage announcements) are omitted.
* **Prevention:** Always scan raw audio and session planning materials for in-universe media broadcasts and integrate them into the physical scene environment.

### 17. Omission of Post-Session Thematic Reflections
* **Symptom:** Profound out-of-character GM/player discussions regarding core campaign themes (e.g. Sparks vs. Nodes, Exponential Connection, Stagnation as Death, Unending Horizons of Exploration) are discarded as mere "table talk."
* **Prevention:** Channel deep OOC thematic insights into rich, philosophical narrative prose and character epiphanies during chapter resolutions.

---

## ✍️ The Ebook Standard: Mandatory Novelization Checklist

Every generated scene block (`clean/blocks/sN-scene-XX.md`) and compiled story chapter must satisfy this 6-point standard before being marked complete:

1. **Full Dialogue Dramatization**:
   - All spoken lines formatted with double quotes (`"..."`).
   - Every speaker change gets a dedicated paragraph.
   - Zero embedded italic dialogue summaries.

2. **Sensory & Physical Anchoring**:
   - Include distinct physical mannerisms: Iggy's water goggles sloshing, Lomi adjusting his woolen flat cap, Ignatius's cuffs flaring embers, Britt's intense botanical gaze, Ink furiously scribbling in her logbook.

3. **Complete Comedic & Emotional Arcs**:
   - Multi-speaker banter preserved with full setup, timing, escalation, and reactions intact.

4. **Deep World-Building & Mechanical Magic**:
   - Fully describe world-tech and elemental physics (Embodied Energy, acoustic resonance, living keratin maps, copper conductors, pneumatic walkers).

5. **Logical Causal Continuity**:
   - Every character action and reaction must have an explicit in-world trigger.

6. **Line Traceability & Ledger Parity**:
   - Every scene must contain line anchors (`<!-- Lxxxx -->`) mapping back to `sN-raw-indexed.md` and a clean ledger comment at the bottom.
