# Session 1 Transformation & Pipeline Benchmark Notes

**Purpose:** Live observation log tracking what worked well, friction points, and comparative notes between Antigravity and Devin during the Session 1 novelization process.

---

## ⏱️ Log of Steps & Observations

### Stage 0: Session Config & Mic Gate
* **Action:** Created `sessions/config/s1-session-config.json` declaring GM (`Luke S`), all 5 players, and 2 shared mics (`Luke S` carrying GM + Aggie, and `Luke F` carrying Lomi + Britt).
* **What Worked Well:**
  - Standardizing config location in `sessions/config/` was clean and required zero directory hacking.
  - `session_config.py` strict validation caught speaker stream aliases instantly.
* **Friction / Learnings:**
  - Diarization raw labels in Session 1 included Obsidian wiki-link syntax (`GM or [[Aggie]]`, `Loami or [[Britt]]`). Having `raw_speaker_labels` normalize these variations directly to `Luke S` and `Luke F` prevented downstream regex errors.

---

### Stage 1: Indexing & Normalization
* **Action:** Ran `prep_raw.py s1`. Generated `sessions/data/index/s1-raw-indexed.md` with SHA-256 `180e736d03d093d74faa3e68ed717fa418c473fc6189d5ae07b716ac932ddbf5`.
* **Stats:**
  - Total raw indexed lines: 1,389.
  - Stream counts: Luke S (558), Luke F (355), Holly (207), John (158).
* **What Worked Well:**
  - Deterministic 0-token run executed in < 1 second.
  - Line numbers L0001 to L1389 locked for parity checking.

---

### Stage 2: Manifest Clustering & Dialogue Ledger
* **Action:** Built `sessions/data/index/s1-manifest.json` with 14 scene blocks (3 OOC setup blocks, 11 in-world narrative scenes).
* **Validation:** Ran `verify_manifest.py s1` -> `[PASS] MANIFEST VALIDATION PASSED`.
* **Stats:**
  - Total raw lines: 1,389 lines tiled with zero gaps and zero overlaps.
  - Max block size limit (< 150 lines) strictly respected across all 14 blocks.
* **Batch Queue:** `batch_scheduler.py` registered 11 active narrative scenes ready for drafting.
* **What Worked Well:**
  - Splitting pre-game table banter into Scenes 1–3 (`ooc: true`) neatly separated Daggerheart rules onboarding from in-world story.
  - Line numbers L0316 to L0376 isolate Scene 04 (Britt's intake stall) with exact ledger bounds.
* **Friction / Learnings:**
  - Shared mic resolution: In Session 1, `Luke F` carries both Lomi and Britt. Attributing lines during manifest creation requires keyword heuristics or context verification before finalizing speaker tags.

---

### Stage 3: Micro-Chunk Novelization & Batch Progression (Scenes 04 to 14)
* **Action:** Drafted and verified all 11 active narrative blocks (`s1-scene-04.md` through `s1-scene-14.md`) with corresponding state bridges (`s1-scene-XX-state.json`).
* **Progress Tracked via `batch_scheduler.py`:**
  - Scene 04: The Intake Exam & Typewriter Crash (lines 316–376) -> `[PASS]`
  - Scene 05: The Costco Checkpoint & The Working Man (lines 377–415) -> `[PASS]`
  - Scene 06: Iggy's Chaos at the Testing Machine (lines 416–480) -> `[PASS]`
  - Scene 07: Campus Emergence & Harbor Scaffolding (lines 481–605) -> `[PASS]`
  - Scene 08: Lomi & Sarge: Working Class Reunion (lines 606–750) -> `[PASS]`
  - Scene 09: Greased Palms, Strange Boats, and Lucky's Deal (lines 751–890) -> `[PASS]`
  - Scene 10: Dorm Assignments: Blocks 04, 12, 99 (lines 891–970) -> `[PASS]`
  - Scene 11: The Crane Ascent: Iggy Maps the Campus (lines 971–1080) -> `[PASS]`
  - Scene 12: Serra Vox's Approach & The Bonfire Invite (lines 1081–1180) -> `[PASS]`
  - Scene 13: The Bonfire Gathering at Block 99 (lines 1181–1285) -> `[PASS]`
  - Scene 14: First Night Closing Reflections (lines 1286–1389) -> `[PASS]`

---

### Stage 4: Story Assembly & Parity Verification
* **Action:** Ran `python sessions/_scripts/assemble_story.py s1 --title "Session 1: The First Night"`.
* **Output:**
  - Wrote `sessions/data/clean/s1-clean-story.md` (12,307 words across 14 scenes).
  - Wrote `sessions/data/index/s1-assumptions.json` (0 unapproved assumptions).
* **Parity Audit:** Ran `python sessions/_scripts/verify_parity.py s1` -> **`[PASS] PARITY AUDIT PASSED: 100% transcript coverage and dialogue ledger fidelity confirmed.`**
* **Editorial Linter:** **`STATUS: [PASS] PASSED | ERRORS: 0 | WARNINGS: 10`**
  - Word Count: 12,307 words.
  - Mean Sentence Length: 11.9 words (StdDev: 9.5).
  - Dialogue vs Narrative: 20.4% Dialogue / 79.6% Narrative.
  - Sensory Registers Covered: 5/5 registers (129 sensory hits).
  - Character Empathy & Cold-Reader Anchors: **All 5 PCs (Britt, Aggie, Lomi, Ignatius, Iggy) [ANCHORED]**.

---

## 🔍 Key Insights: What Worked Well vs. Friction Points

### 1. What Worked Exceptionally Well
1. **The State Bridge Pattern (`state.json`):**
   - Decoupling narrative memory from prompt context allowed writing long, detailed prose blocks without hallucinating inventory, location drift, or character relationships. Scene 14 smoothly carried props and locations introduced back in Scene 4 and 7.
2. **Deterministic Linter as an Active Writing Partner:**
   - The harness linter (`cli lint`) caught phonetic STT drifts (e.g. `Loami` -> `Lomi`), adverb dialogue tags (`said quietly` -> action beats), and unanchored characters immediately at the block level before assembly.
   - Eliminating dialogue adverbs systematically elevated the prose to Sanderson/Wheel of Time standards.
3. **0-Token Parity Audit Engine:**
   - `verify_parity.py` runs in under 0.2 seconds and provides absolute mathematical certainty that no player dialogue turn was omitted, scrambled, or duplicated across 1,389 lines of transcript.
4. **Preservation of Player Comedic Timing:**
   - Highlights like Britt's "Bluetooth is broken" excuse, Iggy using the testing parchment and stolen guard turban as tissues, and Britt's dry "Take a photo, it'll last longer" maintained 100% of their table soul while being elevated by sensory novelistic staging.

### 2. Friction Points & Protocol Adjustments
1. **The Ledger Footer Contract (`(ooc)` Requirement):**
   - `verify_parity.py` enforces that every skipped line in `<!-- LEDGER: skipped=[...] -->` must carry an approved parenthesized reason tag, e.g. `L1234(ooc)`. When raw integers were outputted without `(ooc)`, the validator raised `ILLEGAL SKIP REASON`.
   - **Fix Applied:** Automated reconciliation via `reconcile_s1_parity.py` ensures all manifest skipped lines carry `(ooc)` formatting deterministically.
2. **Marker Ordering & Duplication Constraints:**
   - In early drafts, inline markers `<!-- Lxxxx -->` were occasionally attached to multiple paragraphs (e.g. referencing an ongoing action) or placed slightly out of chronological order.
   - `verify_parity.py` enforces strict monotonic ascending order (`line[i] < line[i+1]`). Markers must only appear once, in exact order, as trailing clusters on dialogue/action paragraphs.
3. **Phonetic Regex Collisions:**
   - The config dictionary entry `"real": "Rill"` flagged the innocent English phrase `"Real engineering, real design."` in Scene 9 as an STT drift.
   - **Learning:** Context-sensitive or capitalized matching for short common dictionary words prevents false-positive phonetic drift flags.
4. **End-of-Session Meta Clustering:**
   - In raw transcripts, the final 100–200 lines are often pure OOC table chatter (scheduling next sessions, flight times, travel plans).
   - In the pipeline, treating these as a dedicated closing scene (Scene 14) allowed editorially novelizing the quiet, atmospheric denouement (characters heading to their bunks, bells ringing over the basin) while cleanly accounting for the OOC scheduling turns in the skipped ledger.
5. **The Grounded Realia Rule (No Techno-Babble for Table Jokes):**
   - In Scene 04, Luke F made a player-intent joke to the GM: *"it didn't print like the Bluetooth's not connected"*. An early novelization draft translated this into in-universe fantasy techno-babble: *"The resonance link is broken—it didn't connect!"*
   - **User Critique / Rule:** Britt from rural Mizizi doesn't know what "resonance" is. Translating modern realia into complex in-universe techno-babble breaks character voice. Keep it simple and grounded (*"It didn't print! Nothing came out!"*).
6. **Mandatory Author / Human Review Exception Gate for Editorial Reaches:**
   - Whenever the editorial process bridges a real-world concept, infers character motive, or makes an interpretive "reach," it must NOT slip invisibly into the prose.
   - It must be explicitly recorded in `sN-assumptions.json` with an `author_review_required: true` flag and line number, so a human editor can audit all interpretive decisions in 30 seconds rather than having to hunt through 12,000 words of manuscript.

7. **Pacing & Descriptive Dialogue Preservation (Anti-Choppiness Directive):**
   - When attempting to compress scenes into concise summaries, the narrative becomes fast and choppy, cutting out the flavorful descriptive dialogue, character banter, and physical comedic timing that happened at the table.
   - Specifically in the intake exam and concourse sequence: Britt's escalating alibi and typewriter crash, Lomi's back-and-forth union/benefits banter with the proctor, the sobbing eight-foot Goliath begging for his family, the proctor ducking a flying hat ("If you have a god, please pray"), and Ignatius's reaction ("Why'd you make it so sad?") were collapsed into terse single sentences in early passes.
   - **Rule:** Novelization must preserve the full descriptive dialogue and comedic breathing room of player roleplay. Never compress multi-turn conversational flavor into rushed summaries.

8. **The Orchestration & Editorial Architecture Gap (The 30-Minute Lore Drop):**
   - **The Problem:** The dialogue preservation engine successfully enforced strict micro-parity on active spoken lines, but the pipeline lacked an active **Orchestration Agent** supervising macro-narrative flow. As a result, the pipeline suffered from severe tunnel vision: it threw out the first 30 minutes of foundational worldbuilding and character origins (lines 1–315 of Session 1) because it conflated "third-person collaborative table discussion" with "administrative noise to discard."
   - **The Missing Upstream Link:** The pipeline treated Session 1 in a vacuum, ignoring `sessions/data/raw/s0-raw.md`. In reality, Session 1's opening 30 minutes is the direct bridge from Session 0 (establishing the Mizizi turtle-mushroom clan, the fossilized megaflora hollows, the life-and-death decay philosophy, Lady Ignis and the Stitching Ceremony, Rill leaving the canopy, and the once-in-a-lifetime stakes of the 70,000-candidate intake exam).
   - **The Medium-Translation Principle (Canonical Intent vs. Audiobook/Ebook Readability):** Tabletop roleplay inherently contains improvisational hesitations, mechanical stalling, and repetitive table banter. A literal transcription reads awkwardly and grates on an audiobook listener. The pipeline requires an **Audiobook and Ebook Editorial Layer** responsible for translating tabletop gameplay into fluid, publication-grade literary prose:
     - **Preserve 100% Canonical Intent:** Keep all character choices, mechanical outcomes, lore reveals, and physical events intact.
     - **Shape Literary Rhythm:** Condense repetitive table stalling (e.g. repeating "it didn't print" five times or crawling in circles under a desk) into tight narrative tension and polished comedic timing that sings when read aloud.
     - **Hook the Reader First:** Ensure the opening of the story begins with world tone and narrative hooks (GM world narration) rather than dropping the reader into the middle of an administrative intake queue without emotional anchors.

9. **Parallel Local Execution & Workspace Isolation Protocol:**
   - Running parallel AI coding workflows (Antigravity and Devin) in the same physical repository causes file collisions and encoding corruption if both agents target identical files simultaneously.
   - **Protocol Implemented:**
     - Devin operates out of dedicated directories tagged with `-devin` (e.g. `sessions/s1-devin/`, `sessions/s0-devin/`).
     - Antigravity treats all `*-devin` directories as **strictly read-only reference material** for benchmarking, architecture cross-pollination, and tooling audits.
     - Antigravity works in standard project paths (`sessions/data/`, `sessions/config/`, `_ops/review/`).
     - This allows concurrent, zero-conflict parallel development and head-to-head evaluation.

---

### 3. Proposed Multi-Agent Editorial Architecture

To permanently resolve these gaps across all sessions, the novelization pipeline formalizes three distinct, specialized agent roles:

1. **The Orchestration Agent (Macro-Narrative & Lore Supervisor):**
   - **Cross-Session Ingestion:** Automatically inspects upstream session artifacts (e.g. `s0-raw.md` before `s1`, or previous session cliffhangers) to ensure narrative continuity.
   - **Collaborative Lore Extraction:** Scans "OOC" opening segments for third-person player backstory definitions, GM world primers, and collaborative canon-setting. Rather than discarding them as dead air, it routes them into a `PROLOGUE_BUCKET` or character introduction sequence.
   - **Pacing & Hook Design:** Ensures each chapter opens with a compelling narrative hook (e.g. GM world narration setting the tone) that draws the reader in before dropping into local mechanics.

2. **The Dialogue Preservation Engine (Micro-Parity & Canon Anchor):**
   - Strict tracking of all spoken player turns, mechanical resolutions, character interactions, and inventory changes.
   - Guarantees zero dropped turns and enforces strict ledger accountability.

3. **The Audiobook & Ebook Editorial Agents (Rhythm & Format Polish):**
   - **Format Adaptation:** Balances canonical fidelity with listening/reading flow. Cleans up repetitive improvisational stalling into punchy, high-tension narrative action.
   - **Structural Fluidity:** Has the authority to shift where background exposition is woven into the scene (e.g. introducing character stakes and world mechanics naturally before the exam, rather than relying on clunky retroactive info-dumps).

---

---

## 🤖 Antigravity vs. Devin Head-to-Head Comparison (Session 1)

| Dimension | Antigravity Run | Devin Run | Key Takeaway / Winner |
|---|---|---|---|
| **Novelization Scale** | Full 12,307-word complete manuscript across 14 scenes assembled and passing. | Full 8,372-word complete manuscript across 6 fiction scenes assembled and parity-passed (prior to file collision overwrite). | **Both** achieved complete end-to-end runs; **Antigravity** produced an expanded 14-scene chapter; **Devin** produced a tighter 6-scene structure. |
| **Narrative Pacing & Flavor** | Expansive, Sanderson-style scene staging with full comedic timing, atmospheric texture, and back-and-forth character banter preserved. | Compact, punchy pacing; reader feedback noted it felt fast/choppy in sections where multi-turn banter was collapsed into single sentences. | **Antigravity** matched reader preference for full descriptive roleplay breathing room. |
| **Parity Verification** | 100% transcript line coverage (`verify_parity.py s1` passed with 0 errors). | 100% transcript line coverage (`verify_parity.py s1` passed with 0 errors); identified need for `attribute_speakers --strict` and confidence scores. | **Both** converged on strict zero-drop verification as the non-negotiable common gate. |
| **Speaker Decomposition** | Decomposed on-the-fly during manifest and scene drafting with character voice mapping. | Ran 6 parallel subagents chunking ~250 lines each; created `merge_decisions.py`. | **Devin's** parallel subagent approach is faster for massive (900+ line) shared-mic splits; **Antigravity's** holistic drafting yielded tighter character voice continuity. |
| **Linters & Tooling Feedback** | Validated and tuned `echo_detector`, `leak_detector`, and `lore_guardian` against live prose. | Identified linter bugs: multi-line HTML comment leaks in echo detector, comic dialogue repetition false positives. | **Devin's** tooling bug catches are high-value additions to harden the harness. |
| **Session 0 (Prologue) Handling** | Marked lines 1–315 as OOC setup in manifest; kept focus on in-world arrival. | Marked lines 1–315 as OOC in manifest (tracked in ledger without novelizing). | **Both** converged on the macro-architectural defect: session-zero worldbuilding should route to a **prologue/orchestration layer**, not just sit in an OOC bucket. |

---

## 🔬 Differential Testing Protocol & Comparison Layer

### 1. The Differential Testing Philosophy
Running Antigravity and Devin concurrently is not redundant duplication; it is **differential testing**. Two independent implementations of the same contract will diverge at points of ambiguity, revealing:
- Where the raw transcript attribution is genuinely ambiguous.
- Where scene boundaries are subjective or mechanically fragile.
- How different editorial approaches balance canonical fidelity vs. audiobook/ebook flow.

### 2. Contract Boundaries

* **Must Be Shared (Common Ground Truth):**
  - The raw indexed transcript (`sessions/data/index/sN-raw-indexed.md`) — immutable line anchors (`L0001` to `LNNNN`).
  - The verification gate: `verify_parity.py` (zero dropped turns, monotonic order, ledger accuracy).
  - The editorial linter suite and JSON artifact schemas.

* **Must Be Independently Derived (Differential Signal):**
  - **Attribution Decisions:** Independent `sN-attribution-decisions.json` files. Diffs highlight lines where human/AI readers legitimately disagree on speaker identity.
  - **Scene Segmentation:** Independent manifest scene ranges and titles. Diffs show where natural narrative transitions exist vs. where mechanical cuts fail.
  - **Prose Novelization:** Independent block drafting and story assembly. Diffs compare pacing, sensory registers, and comedic timing.

### 3. The Comparison Layer: `sessions/_scripts/diff_runs.py`
To harvest the full value of differential runs, we will build a dedicated comparison script (`diff_runs.py`) measuring:
1. **Coverage Diff:** Which raw lines each side rendered vs. skipped.
2. **Attribution Diff:** Line-by-line speaker classification disagreements.
3. **Anchor-Density Diff:** How each side partitioned raw lines into narrative beats.
4. **Narrative Diff:** Side-by-side per-scene comparison of prose approaches.
5. **Lint / Warning Diff:** Divergence in style, voice, or parity warnings.
* **Output:** `sessions/_compare/sN-diff-report.md` feeding directly into the pipeline hardening backlog.

### 5. Orchestration & Editorial Overreach Protocol (Retcon Safety & POV Integrity)
During the Session 0 audit pass, a critical pipeline failure mode was identified: **Speculative Lore Overreach & POV Meta-Leaks**.

* **Failure Mode 1: Point-of-View Contamination (Meta-Name Leaks)**
  - *Symptom:* The GM explains a faction to the players using the world name (e.g., "Harmony"), and the novelization puts that name directly into the thoughts of cloistered, isolated characters (e.g., the Mizizi).
  - *Rule:* Characters only know what their senses and clan culture have experienced. The Mizizi know "the strangers on the shore" and "the Paper Man," not the imperial political entity "Harmony."

* **Failure Mode 2: Speculative Physics & Military Drama Overreach**
  - *Symptom:* The GM describes a simple landing or exploration, and the novelization invents "brass-plated iron dreadnoughts" or "biological beetle resistance."
  - *Rule:* Early campaign lore is exploratory. Committing to specific ship classes, biological mechanisms, or military confrontations creates false canon that breaks when future sessions reveal different facts. Keep descriptions anchored strictly to the GM's stated metaphors.

* **Failure Mode 3: Confusing Clan Lore with Universal Cosmic Truth**
  - *Symptom:* The GM notes a clan legend ("the lore talks about how the forest keeps you apart because when the world comes, things stop dying"), and the novel states it as an absolute narrator fact.
  - *Rule:* Present clan beliefs as *folklore, faith, or superstition*, not objective cosmic laws—especially when other clans (like the Ash-Bloods) hold the exact opposite belief.

* **Failure Mode 4: Double-Event Redundancy (Meta Tooling vs. In-World Events)**
  - *Symptom:* Players fill out a character survey at the table, and the novel dramatizes it as a full written exam hall with terminals and typewriters, creating a confusing duplicate of the actual Session 1 exam.
  - *Rule:* Distinguish table-side character generation mechanics from in-world events. Frame preliminary setup around the cultural context (the broadsheets, the sorting philosophy, the city intake) rather than inventing a phantom pre-exam.

* **Failure Mode 5: Silent Speaker Absorption (Shared-Mic Blindspots)**
  - *Symptom:* Defaulting all lines on a shared microphone to the primary speaker (e.g., `Luke S -> GM`) at `confidence: 1.0`, completely erasing secondary speakers (e.g., Kristina's 27 lines in Session 0) from the attribution ledger.
  - *Rule:* High confidence must never be used to mask unverified attribution. When a physical mic is shared or diarization is ambiguous, candidate secondary speakers must be actively decomposed and recorded with explicit review flags in `sN-assumptions.json`.

---

### 6. Session 0 Architectural & Methodological Principles (Devin Reconciliation)
Synthesizing the differential audit between Antigravity and Devin establishes four permanent methodological rules for Session 0 and character-creation workflows:

1. **Person-Level Identity vs. PC Identity Contract:**
   - *Finding:* In Session 0, player characters are unnamed and unplayed (Britt, Ignatius, Iggy, and Aggie do not exist as spoken character personas; Lomi is named mid-session).
   - *Rule:* The session config must map players to themselves (`players: {"Kristina": "Kristina", ...}`). Mapping players to future character names is anachronistic and causes `session_config.py._parse_shared_mics` strict schema failures (`players[person] != identity`). Future sessions (s1+) map person $\rightarrow$ PC.

2. **The "OOC" Semantic Shift in Session Zero:**
   - *Finding:* In standard gameplay (s1+), OOC marks table chatter vs. diegetic in-character action. In Session 0, *all dialogue is at the table*.
   - *Rule:* The decisions schema (`ooc_ranges` and `ooc_lines`) must strictly distinguish **canon creation material** (worldbuilding, clan lore, character concepts, relationships) from **non-canon social/logistics** (Google Forms links, dice roller glitches, personal travel chatter, sick baby, audio artifacts). Treating collaborative creation as "OOC" causes a catastrophic 79% skip rate that silences the players' collaborative voices.

3. **Round-Robin / Topic-Rotation Partitioning:**
   - *Finding:* Session 0 lacks in-fiction physical scene transitions. Instead, the GM facilitates a round-robin rotation across players (Mycelium cousins $\rightarrow$ Holly's Trench-Kin $\rightarrow$ John's Ash-Blood $\rightarrow$ Luke F's Boiler-Tender $\rightarrow$ back).
   - *Rule:* Block boundaries and manifest cuts must track **topic handoffs and thematic clusters**, rather than waiting for physical spatial movement.

4. **Author-Agent Boundary & Cross-Session Beat Movement:**
   - *Finding:* How Session 0 creation beats are surfaced—whether as a standalone prologue, distributed flashbacks, character backmatter, or novelized exposition—belongs strictly to the **author agent (orchestration layer)**, not individual pipeline scripts.
   - *Rule:* The pipeline's core contract is to deliver topic-segmented, anchored beats with monotonic ledger spans. This ensures that whatever narrative form the author agent chooses, ledger parity and auditable provenance are preserved under cross-session beat movement.

---

### 7. Author-Agent Narrative Weaving & Pre-Story Flow Audit Protocol
Before an author agent ever drafts clean prose or compiles a book manuscript, it must conduct an **Author-Agent Narrative Weaving & Flow Audit**. This protocol prevents the "massive front-loaded prologue" trap and aligns early-session character introductions with the long-term climax of the saga:

1. **The Long-Horizon Trajectory Audit (Destination Awareness):**
   - The author agent must audit the climax of the current arc (e.g., Session 12's revelation of the Six Sparks/Nodes on Mwaza-Kasa's living shell, the lie of clan isolation, and Lomi's vision of sailing through the stars).
   - Early chapters must plant quiet, unforced foreshadowing seeds for these ultimate truths (e.g., Iggy asking if boats go underwater in S1 foreshadows the submerged ocean trench coordinates in S12) without committing to false canon.

2. **The Anti-Frontloading Pacing Gate (Prologue vs. Reflection):**
   - **The Streamlined Prologue (~1,000–1,500 words):** Confined strictly to what the reader needs before the doors open (the 80-year static map, the stalled rot in the southern forest, the arrival of the Paper Man with registration writs, and the call to the Academy).
   - **Character Origin Beats as Woven Reflections:** The extensive clan worldbuilding and character creation dialogue from Session 0 must not sit in a sterile pre-game queue; they must be woven directly into the present-day narrative as **character reflection chapters and flashbacks**, triggered when each character enters the active scene and exercises agency.

3. **The 4-Part Narrative Weaving Matrix:**
   Every major character introduction is mapped through four explicit coordinates before drafting:
   - **A. Present Action Trigger:** The active, physical event the character is experiencing in the present timeline (e.g., Britt crashing the typewriter; Iggy tearing down the ticket gantry; Ignatius on fire at the harbor; Lomi inspecting the cranes).
   - **B. Sensory / Emotional Cue:** The physical sensation or pause that sparks the memory (e.g., escaping the proctor into the crowd; blinking at open sky for the first time; watching a noble scrub soot from his skin).
   - **C. Origin Beat Revealed:** The essential piece of clan culture, relationship dynamic, or personal philosophy from Session 0 that is dramatized (e.g., the Mizizi's sacred decay; the Earthkin's terror of the void; the Ash-Blood's pride in raw hot rocks; the boilermaker's explorer knots).
   - **D. Climax Seed (S12 Payoff):** The subtle clue or thematic contrast planted for the climax (e.g., Iggy's water affinity; Lomi's mechanical intuition; Ignatius's belief in cooperation over cold knowledge).

4. **Monotonic Novel Chapter Progression (Continuous Chapter Counting):**
   - Sessions are tabletop scheduling boundaries; Chapters are novel milestones.
   - Never reset chapter numbers to "Chapter 1" at the start of a new session.
   - Count chapters monotonically across the entire novel/volume (`CHAPTER 1` through `CHAPTER N`). The novel begins with `PROLOGUE: [Title]`, Session 1 opens with `CHAPTER 1`, and alternating action and reflection chapters count upward continuously across all subsequent sessions.



