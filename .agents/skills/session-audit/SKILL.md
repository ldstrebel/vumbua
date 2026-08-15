---
name: session-audit
description: Comprehensive workflow and post-mortem protocol for auditing session transcripts, novelization prose, and storyboards against raw audio recordings.
---

# Session Transcript Audit & Post-Mortem Protocol

Use this skill when processing session recordings, cleaning transcripts, novelizing campaign chapters, generating storyboards, or performing post-mortems when gaps or discrepancies are identified.

---

## 🏗️ The 5-Stage Data Transformation Pipeline

Every TTRPG session in Vumbua follows a strict, non-destructive 5-stage transformation pipeline:

```
  ┌─────────────────────────────────────────────────────────┐
  │ 1. Raw Audio Recording (sessions/transcripts/raw/sN-raw.md) │
  │    Line-by-line Whisper STT capture of table audio.    │
  └────────────────────────────┬────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 2. Indexed Raw Transcript (index/sN-raw-indexed.md)     │
  │    Indexed with line markers (L0001...) and line ranges. │
  └────────────────────────────┬────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 3. Clean Transcript (clean/sN-clean.md)                 │
  │    Categorized into Tier A (In-World), Tier B (Action),│
  │    and Tier C (Meta/Table Talk).                        │
  └────────────────────────────┬────────────────────────────┘
                               │
                               ▼
  ┌─────────────────────────────────────────────────────────┐
  │ 4. Novelized Story Blocks (clean/blocks/sN-scene-XX.md)  │
  │    Sanderson-style prose with Direct Dialogue Locking   │
  │    and verbatim character line markers (<!-- Lxxxx -->).│
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

## 🚫 Historical Failure Modes & Post-Mortem Register

This section documents verified failure modes encountered during campaign processing so the engine never regresses:

### 1. Gist-Level Manifest Truncation
* **Symptom:** High-value character dialogue, comedic beats, or world-tech explanations present in `sN-raw.md` vanish from the novelization.
* **Root Cause:** Initial indexing scripts (`build_manifest.py`) compressed 50–100 lines of raw transcript into brief summary bullets in `dialogue_ledger`. If a line was omitted from the manifest ledger, downstream prose generators never saw it.
* **Prevention:** Always run `python sessions/scripts/audit_transcript_gaps.py sN` to scan `sN-raw-indexed.md` against `sN-clean-story.md` for skipped player/NPC dialogue turns.

### 2. Heuristic Keyword Coarseness
* **Symptom:** Audit tools report `[PASS]` even though critical spoken exchanges are completely missing.
* **Root Cause:** Audit scripts checked *binary presence* of broad keywords (e.g. checking if "Sterling Broadcast" appeared anywhere in the text), ignoring whether the actual spoken dialogue between characters was included.
* **Prevention:** Never rely on simple keyword regex to claim coverage. Combine `audit_sN_raw_coverage.py` with line-by-line differential dialogue audits.

### 3. Fused Interjections & Turn Order Compression
* **Symptom:** Character A starts speaking, Character B interjects, and Character A finishes—but the novelization fusses Character A's lines into one continuous block, dropping Character B's interjection.
* **Root Cause:** Skipping interjections in `dialogue_ledger` as "table chatter" causes LLM prose generators to fuse non-contiguous speech turns.
* **Prevention:** Every character interjection (e.g. Lucky interrupting Lomi, Britt admitting she forgot the flare) must preserve its exact line order and marker tag (`<!-- Lxxxx -->`).

### 4. OOC Table Talk vs. In-World Character Banter Misclassification
* **Symptom:** Real in-world character dialogue is accidentally stripped as "table talk", OR actual out-of-character GM meta-comments (e.g. reminding a player they are upstairs on the bridge) are erroneously novelized into in-universe canon.
* **Root Cause:** Relying on automated regex without human context verification.
* **Prevention:** 
  * In-world spoken dialogue $\rightarrow$ Novelize with verbatim quotes.
  * OOC table chatter (location reminders, rule checks, dice math) $\rightarrow$ Purge from story prose.

### 5. STT Phonetic Mishearings & Entity Name Drift
* **Symptom:** Character names or locations are mangled (e.g. `Rill` misheard as `Real`, `Professor Ink` misheard as `Professor Inc.`, `Lassi Zizi` misheard as `Lazizi`, `Brent & Aggie` misheard as `Brian Nagy`).
* **Root Cause:** Speech-to-text models phonetically guessing names not present in their dictionary.
* **Prevention:** Cross-reference every entity against `characters/` and `lore/` dossiers before writing scene blocks.

---

## 🛠️ Differential Verification Audit Suite

Before declaring any session clean or presenting story blocks for approval, run the full 4-pass verification suite:

```bash
# 1. Tile line ranges and validate manifest JSON structure
python sessions/scripts/verify_manifest.py sN

# 2. Verify 100% transcript coverage and line marker ascending order
python sessions/scripts/verify_parity.py sN

# 3. Detect any omitted player/NPC dialogue turns between rendered bounds
python sessions/scripts/audit_transcript_gaps.py sN

# 4. Audit canon plot anchors against raw, clean, and story files
python sessions/scripts/audit_s12_raw_coverage.py
```

---

## 📋 Mandatory Post-Mortem Checklist

Whenever the user identifies a missing gap, ordering error, or prose inconsistency:

1. **Acknowledge & Isolate:** Identify the exact raw line numbers (`Lxxxx`) in `sN-raw-indexed.md`.
2. **Determine Category:** Is it an omitted turn, a turn-order interjection, an STT entity mishearing, or an OOC table-talk leak?
3. **Update Block Files:** Edit `sessions/transcripts/clean/blocks/sN-scene-XX.md` with verbatim dialogue and correct line markers (`<!-- Lxxxx -->`).
4. **Update Manifest Ledger:** Ensure `sN-manifest.json` reflects the added line numbers in `dialogue_ledger`.
5. **Re-Assemble & Verify:**
   ```bash
   python sessions/scripts/assemble_story.py sN --title "..."
   python sessions/scripts/build_dossier.py sN
   python sessions/scripts/verify_parity.py sN
   python sessions/scripts/audit_transcript_gaps.py sN
   ```
6. **Log Learnings:** If a new failure mode or pattern was discovered, add a new entry to the **Historical Failure Modes & Post-Mortem Register** in this skill file!

---

## 📋 Systemic Checks for Every Scene Block

Apply these before finalizing any scene (in addition to the 4-pass suite):

| Check | Rule |
|---|---|
| **Turn cluster fusion** | When two speakers alternate rapidly across 5+ lines, read the full cluster holistically before writing any paragraph. The emotional payoff of a turn often completes 5–10 lines after the last interruption. |
| **STT nickname drift** | Pre-load character nicknames from `characters/` before writing each scene. Any proper noun not in a character file must be flagged. |
| **Clipped STT lines** | Any line ending without punctuation or syntactically incomplete → flag `[CLIPPED]`, resolve using adjacent context before writing prose. |
| **Tier B in quotes** | Any line where a player speaks about their character in third person → Tier B, convert to narrator prose — never quoted dialogue. |
| **Missing interjections** | Any gap of 3+ unanswered lines between a question and the next rendered response → manual gap review required. |

### 6. Clipped STT Lines Rendered as Stylistic Ellipsis
* **Symptom:** A line ending mid-sentence in the raw (e.g. *"you're much heavier than"*) is rendered with a trailing-off ellipsis rather than flagged as a clipped recording.
* **Root Cause:** STT clips audio at segment boundaries; the model treats syntactic incompleteness as intentional style rather than a data gap.
* **Prevention:** Flag all syntactically incomplete raw lines with `[CLIPPED]`. Resolve by checking surrounding context and character relationships. Example fix: *"you're much heavier than"* → cross-reference who is present → *"you're much heavier than... Britt"*.

### 7. Tier B Player Narration Rendered as Tier A In-World Dialogue
* **Symptom:** A player describing their character's state in third person (*"Britt is just zoned"*, *"I think Britt is like..."*) gets novelized as a spoken character line in quotes.
* **Root Cause:** The 3-Tier classification pass was skipped before novelization. All spoken audio was treated as Tier A dialogue without checking whether the speaker was narrating their character's state rather than performing in-world speech.
* **Prevention:** Before writing any quoted dialogue line, verify: is the speaker talking *as* their character (Tier A), or talking *about* their character (Tier B)? Third-person self-reference (*"Britt is..."*, *"she just..."*) always signals Tier B → convert to narrator prose action description.
