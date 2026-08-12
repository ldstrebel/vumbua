# Implementation Plan v2: Zero-Loss Raw Transcript Novelization Pipeline

**Status:** Revised after audit — supersedes `Pasted--Implementation-Plan-Zero-Loss-Raw-Transcript-Novelizat` draft.
**Core principle:** Python for mechanical work, LLM for semantic work, and never trust the LLM to self-report coverage *or fidelity*.

---

## 1. Problem Statement

During recent transcript novelizations, critical narrative beats, dialogue turns, and character arcs were dropped or truncated (e.g., Rill's *"Momentum is life"* speech, Raphael's 60-line triage exchange).

**Root causes:**
1. **Unconstrained LLM summarization bias** — given 3,000+ lines, LLMs compress dialogue and skip intermediate exchanges.
2. **Brittle Python semantic parsing** — regex cannot segment chaotic TTRPG cross-talk into scenes.
3. **Fuzzy-match false positives** — matching raw quotes against novelized prose fails on indirect speech and literary adaptation.
4. **(New, from audit) Coverage ≠ fidelity** — range accounting alone proves every line was *assigned* to a scene, not that its content *survived* novelization. An LLM can claim a range, write three sentences, and pass a pure coverage audit. v2 adds per-block fidelity checks.

---

## 2. Pipeline Architecture (5 Steps)

```
[STEP -1: USER-PROVIDED SESSION CONFIG (sN-session-config.json)] ← HARD GATE
  • gm + players + shared_mics, provided by the user before any analysis
  • prep_raw.py / attribute_speakers.py refuse to run without it (exit 2)
       │
       ▼
[sN-raw.md] (Raw Audio Output)
       │
       ▼
[STEP 0: Python Normalization + Speaker Aliasing (prep_raw.py)]
  • Normalizes line endings, strips trailing whitespace & blank lines
  • Normalizes speaker labels to canonical PERSON labels (Luke Strebel→Luke S, …)
  • Prefixes immutable L0001: line numbers
  • Writes sessions/transcripts/index/sN-raw-indexed.md
  • Computes SHA-256 of the INDEXED file (the single canonical artifact)
       │
       ▼
[STEP 1: LLM Manifest Extraction (sN-manifest.json)]
  • Groups lines into Scene Blocks (MAX 150 raw lines per block)
  • Per block: line_range, title, speakers_present, ooc flag
  • Per block: dialogue_ledger — every distinct dialogue turn (speaker + line no.)
       │
       ▼
[STEP 2: Python Manifest Validation (verify_manifest.py)]
  • Hash lock against sN-raw-indexed.md
  • Contiguity from line 1 → total_raw_lines: zero gap, zero overlap
  • Block size ≤ 150 lines
  • Every dialogue_ledger line number falls inside its block's range
  • HARD PASS required before any novelization begins
       │
       ▼
[STEP 3: Micro-Chunk Novelization (sN-clean-story.md)]
  • ONE Scene Block per LLM pass, Sanderson-style prose
  • Header: <!-- RAW_RANGE: [start, end] | SCENE_ID: N -->
  • Footer: <!-- LEDGER: rendered=[L0972,L0975,…] skipped=[L0980(ooc)] -->
  • OOC blocks are covered but intentionally not novelized (one-line marker)
       │
       ▼
[STEP 4: Mechanical Python Audit (verify_parity.py)]
  • Hash lock (indexed file unchanged since manifesting)
  • Contiguous line coverage across story RAW_RANGE tags: zero gap, zero overlap
  • Story ranges must exactly match manifest scene blocks
  • Ledger reconciliation: every ledger entry rendered OR explicitly skipped with reason
  • Compression-ratio guardrail per block (flag, not fail)
  • Header whitelist enforcement
  • Collects ALL violations, then reports — no first-error exit
  • Outputs HARD PASS / FAIL report
```

---

## 3. Step Specifications

### §2.0 — Session config (Step -1): `sessions/sN-devin/sN-session-config.json`

The GM identity and mic sharing are **user-provided facts, not pipeline inferences.**
The user supplies both before any analysis begins; the pipeline records them
verbatim and gates on them. Nothing downstream is permitted to derive "who is the
GM" or "whose lines are on this mic" from transcript content.

```json
{
  "session_id": "sN",
  "gm": "<person label of the GM>",
  "players": { "<person label>": "<character>" },
  "shared_mics": [
    {
      "mic_label": "<stream label diarization emits>",
      "note": "why this mic carries more than one identity",
      "carries": [
        { "person": "<owner>", "identity": "GM",          "kind": "gm" },
        { "person": "<rider>", "identity": "<character>", "kind": "player_character" }
      ]
    }
  ],
  "raw_speaker_labels": { "<garbled label>": "<canonical person label>" }
}
```

* **Discovery order** (`sessions/scripts/session_config.py`): `sN-devin/`, then
  `config/`, then `transcripts/index/`.
* **Hard gate.** Missing file, wrong `session_id`, missing/empty `gm`, missing
  `players`, or a missing `shared_mics` key → exit status 2 with a message telling
  the operator to get the facts from the user. `shared_mics: []` is the explicit
  way to declare *no mics are shared* — omission is an error, because silence is
  not a declaration.
* **Validated cross-references.** A `gm` slot must name the declared `gm`; a
  `player_character` slot's `identity` must equal `players[person]`; every
  `raw_speaker_labels` value must be a declared person label.
* **`raw_speaker_labels` is spelling normalization only** (`John Hagey` → `John`).
  Diarization is per-mic, not per-person: a raw label names a microphone stream,
  which may carry several identities — but only the ones `shared_mics` declares.
* **Separation of concerns.** `sessions/scripts/speaker_aliases.json` keeps global
  *spelling* maps only (`person_labels`, `character_labels`). It no longer encodes
  `"Luke S": "GM"` or person→character routing, neither of which generalizes across
  sessions — those live in the per-session config.

### Step 0: `sessions/scripts/prep_raw.py`

* **Input:** `sessions/transcripts/raw/sN-raw.md`
* **Output:** `sessions/transcripts/index/sN-raw-indexed.md` + printed SHA-256
* **Actions:**
  1. Normalize `\r\n` → `\n`, strip trailing whitespace, drop blank lines.
  2. Apply **spelling normalization** to speaker labels only — never to dialogue content. Sources: `sessions/scripts/speaker_aliases.json` (global) and the session config's `raw_speaker_labels` (per-session, wins on conflict). Labels normalize to canonical **person** labels; they are NOT collapsed into characters or into `GM`, because a diarized label is a mic, and mapping mic→identity is the attribution stage's job (§3.0b). Prints a per-stream summary marking which streams the config declares as shared.
  3. Prefix every line with `L0001: `, `L0002: `, ….
  4. Compute and print SHA-256 **of the indexed file**. This is the one canonical artifact all later steps verify against — never hash the pre-normalization raw file (re-running prep must be detectable).

**Speaker alias map (spelling only — two sections):**
```json
{
  "person_labels":    { "John Hagey": "John", "Luke Foreman": "Luke F", "Christina": "Kristina" },
  "character_labels": { "Ignatious": "Ignatius", "Loami": "Lomi", "Aggy": "Aggie", "Brit": "Britt" }
}
```
Extend as new mishearings appear. Never add GM identity or person→character routing here.

### Step 0b: `sessions/scripts/attribute_speakers.py` (attribution stage, §3.0b)

Turns streams into identities, driven entirely by the config:

* A stream **not** listed in `shared_mics` carries exactly one identity — `gm` or
  `players[person]`. No decomposition is attempted.
* A stream **listed** in `shared_mics` is decomposed into its declared identities
  **only**. The per-line calls are semantic work recorded in
  `sN-attribution-decisions.json`; allowed identity values per line are the mic's
  declared identities plus `NPC:<Name>` (a GM-voiced NPC, permitted only for a mic
  that carries the GM). Each segment's text must be a verbatim substring of its raw
  line, and any other identity is a hard violation.
* Shared-mic lines with no decision are emitted as `kind: "needs_decomposition"`
  with the config's candidate identities — never silently defaulted to the mic's
  owner. `--strict` fails while any remain.
* Output: `sN-attribution.json` (segments + per-stream/per-identity counts +
  violations).
* **Harness (`sessions/sN-devin/test_attribution.py`)** generates its assertions
  from the config: each declared solo mic must resolve to its declared character,
  and each declared shared mic must yield ≥ 1 segment per carried identity. For s12
  the config declares that `Luke S` carries Kristina's Aggie, so the
  `raw_person: Luke S → character: Aggie` assertion is mandatory and
  config-derived; a config declaring no shared mics generates no such assertion.
  This removes the guess in both directions.

### Step 1: LLM Manifest Extraction → `sessions/transcripts/index/sN-manifest.json`

* **Mode:** extraction only — classification accuracy over prose. The LLM reads `sN-raw-indexed.md` and segments it.
* **Hard constraints (validated mechanically in Step 2):**
  * Max **150 raw lines** per scene block.
  * Blocks tile the file exactly: block 1 starts at line 1, block k+1 starts at block k's end + 1, last block ends at `total_raw_lines`.
  * Every line is assigned — including OOC chatter. Meta/rules-talk/snack-break blocks get `"ooc": true` so "dropped on purpose" is distinguishable from "dropped by accident."
* **Schema:**
```json
{
  "session_id": "s12",
  "indexed_file": "sessions/transcripts/index/s12-raw-indexed.md",
  "raw_file_hash": "<sha256 of s12-raw-indexed.md>",
  "total_raw_lines": 3638,
  "scene_blocks": [
    {
      "scene_id": 4,
      "title": "Triage — Raphael Firefighter Exchange",
      "line_range": [972, 1078],
      "ooc": false,
      "speakers_present": ["Lomi", "Raphael"],
      "dialogue_ledger": [
        { "line": 975, "speaker": "Lomi", "gist": "offers to stay and help triage" },
        { "line": 1041, "speaker": "Raphael", "gist": "Let the guys handle the fix—you figure out the big one" }
      ],
      "key_narrative_beats": [
        "Raphael charges Lomi to 'figure out the big one'."
      ]
    },
    {
      "scene_id": 5,
      "title": "OOC — rules lookup and snack break",
      "line_range": [1079, 1121],
      "ooc": true,
      "speakers_present": [],
      "dialogue_ledger": []
    }
  ]
}
```
* **Dialogue ledger rules:** one entry per distinct in-character dialogue turn (speaker change = new turn). The `gist` is a ≤ 12-word paraphrase — it exists so a human or checker can spot a dropped beat, not for fuzzy matching.

### Step 2: `sessions/scripts/verify_manifest.py` (NEW — the manifest itself is untrusted LLM output)

Fails hard (exit 1) on any of:
1. `raw_file_hash` ≠ SHA-256 of the indexed file on disk.
2. Blocks do not tile `[1, total_raw_lines]` exactly (any gap or overlap).
3. Any block spans > 150 lines.
4. Any `dialogue_ledger` line number outside its block's `line_range`.
5. Duplicate `scene_id`s or non-monotonic ranges.

Collects **all** violations before reporting. Novelization may not begin without a PASS. (The v1 example manifest had a 475-line block — this gate is what catches that.)

### Step 3: Micro-Chunk Novelization → `sessions/transcripts/clean/sN-clean-story.md`

* One scene block per LLM pass. The prompt receives only that block's raw lines + its manifest entry + a one-paragraph "story so far" summary for continuity.
* **Per-scene format:**
```markdown
<!-- RAW_RANGE: [972, 1078] | SCENE_ID: 4 -->
Lomi flagged down Raphael, a firefighter technician working the triage line... <!-- L0975 -->

"Just breathe. You made it," Raphael said, pressing a canteen into her hands. <!-- L1041 -->
<!-- LEDGER: rendered=[975, 1041] skipped=[] -->
```
* **Ledger footer contract:** every `dialogue_ledger` entry from the manifest must appear in `rendered` (as direct or indirect speech in the prose) or in `skipped` with a parenthesized reason. Reasons other than `(ooc)` or `(duplicate)` are audit flags.
* **Inline spoken-turn markers (ordering contract):** every paragraph that renders a dialogue turn ends with `<!-- Lxxxx -->` pointing at its raw line. Motivation (s12 incident): a writer can scramble dialogue chronology in the prose while emitting a perfectly sorted ledger footer, and set-membership checks pass. The ledger proves *presence*; only inline markers prove *order*. Markers must appear as trailing clusters at paragraph ends, in strictly ascending order within each scene, and their set must equal the ledger's `rendered` list. The footer itself is validated first: `rendered` and `skipped` must be disjoint and their union must exactly equal the manifest ledger. `seed_markers.py` can fuzzy-seed markers into an existing draft (unmatched turns are listed for manual placement; it refuses to run on an already-annotated draft unless `--force`). It writes `sN-clean-story.annotated.md`; once annotation is complete and reviewed, **promote it over `sN-clean-story.md`** — the verifier only ever audits the canonical story file.
* **Garble policy (transcription errors):** raw transcripts contain speech-to-text garbage ("go for stacks", "Professor Inc."). The writer must never novelize gibberish literally. At manifest time, obviously garbled turns get `"garbled": true` plus a `"normalized"` gist (best-guess intent), logged as an `ambiguous_audio` assumption (§8.1) with the raw text quoted. The writer renders the normalized intent; the dossier surfaces every garble repair for human review. A garbled line with no plausible reading is rendered as indirect/uncertain speech, never invented dialogue.
* **OOC blocks** are emitted as a single marker line, keeping coverage intact:
```markdown
<!-- RAW_RANGE: [1079, 1121] | SCENE_ID: 5 | OOC -->
```
* **Allowed headers (whitelist):** `#` (session title, once) and `##` (chapter/act breaks). Everything else — including the historically problematic `### Subscene` — is a format violation.

### Step 4: `sessions/scripts/verify_parity.py`

Non-LLM mechanical gate. Checks, collecting all violations before reporting:

1. **Hash lock** — indexed file hash matches the manifest.
2. **Coverage** — RAW_RANGE tags in the story tile `[1, total_raw_lines]`: zero gap, zero overlap.
3. **Manifest agreement** — story ranges and SCENE_IDs exactly match manifest blocks (the story can't quietly re-segment).
4. **Ledger reconciliation** — for each non-OOC block: `rendered ∪ skipped` in the footer == manifest `dialogue_ledger` line numbers. Any missing entry = FAIL. Any `skipped` with a non-whitelisted reason = FAIL.
5. **Dialogue ordering gate** — per non-OOC block: extract inline `<!-- Lxxxx -->` markers (ledger footer excluded); FAIL if the manifest expects rendered turns but no markers exist, if markers are not strictly ascending, or if the marker set ≠ the rendered set. This closes the s12 silent-scramble gap.
6. **Compression guardrail (WARN, not FAIL)** — flag any non-OOC block where prose word count < 35% of the block's raw dialogue word count. Tunable; catches "three sentences for 100 lines" without punishing legitimately terse scenes.
7. **Header whitelist** — only `#`/`##` headers permitted.
8. Prints a full violation report, then `✅ AUDIT PASSED` or `❌ AUDIT FAILED (n violations)`.

---

## 4. File Layout

```
sessions/
├── sN-devin/
│   ├── sN-session-config.json           (user-provided GM + shared mics — hard gate)
│   ├── sN-attribution-decisions.json    (per-line decomposition of declared shared mics)
│   └── test_attribution.py              (config-derived harness)
├── scripts/
│   ├── session_config.py
│   ├── prep_raw.py
│   ├── attribute_speakers.py
│   ├── speaker_aliases.json
│   ├── verify_manifest.py
│   └── verify_parity.py
└── transcripts/
    ├── raw/        sN-raw.md              (untouched originals)
    ├── index/      sN-raw-indexed.md      (canonical hashed artifact)
    │               sN-manifest.json
    └── clean/      sN-clean-story.md
```

---

## 5. Workflow Integration (`.agent/workflows/add-session.md`)

0. **Get the GM and shared-mic config from the user** and record
   `sessions/sN-devin/sN-session-config.json`. Every later step is gated on it.
1. `python sessions/scripts/prep_raw.py sN` → indexed file + hash.
1b. `python sessions/scripts/attribute_speakers.py sN` → `sN-attribution.json`;
   `python sessions/sN-devin/test_attribution.py` → config-derived assertions.
2. LLM manifesting → `sN-manifest.json` (≤ 150 lines/block, ledger per block, OOC flagged).
3. `python sessions/scripts/verify_manifest.py sN` → **must PASS before step 4.**
4. Micro-chunk novelization, one block per pass → `sN-clean-story.md`.
5. `python sessions/scripts/verify_parity.py sN` → proceed only on HARD PASS. On FAIL, re-novelize only the failing blocks (the report names them) — never regenerate the whole story.

---

## 6. Storyboard-Parity Extension (Graphic Novel Pipeline)

The novelization pipeline above is **fully mechanical**. The storyboard pipeline reuses its bones — Python accounting, LLM semantic work, manifest-locked micro-chunks — and is roughly **80% mechanical** once prompts are persisted. Only final image approval requires a human.

### 6.1 Ordering Contract

The storyboard pipeline consumes `sN-clean-story.md` and may only start **after** `verify_parity.py` reports HARD PASS for that story. At storyboard-manifest time, the clean story's SHA-256 is locked into the storyboard manifest — exactly as the indexed raw file was locked at novelization time. If the prose is edited afterward, the hash breaks and the storyboard audit fails loudly instead of dialogue silently diverging.

```
sN-raw-indexed.md ──(novelization, gated)──► sN-clean-story.md ──(HARD PASS + hash lock)──► storyboard pipeline
```

### 6.2 New Canonical Inputs

| File | Purpose |
|---|---|
| `characters/visual-tokens.json` | Canonical visual token block per character (e.g. Iggy → moss sprouts; Lomi → grease smudges). Single source of truth for prompt completeness checks. Keys are canonical names — the speaker alias map from Step 0 applies here too. |
| `sN-clean-story.md` | Locked dialogue source. All baked dialogue must be verbatim substrings of this file — never of `sN-raw.md`. |

### 6.3 Storyboard Manifest — `sessions/transcripts/index/sN-storyboard-manifest.json`

**Immutable plan only. No runtime state.** (Mutable status lives in a separate file — see 6.5.)

```json
{
  "session_id": "s12",
  "clean_story_hash": "<sha256 of sN-clean-story.md>",
  "raw_manifest": "s12-manifest.json",
  "pages": [
    {
      "page": 9,
      "scene_id": 8,
      "line_range": [972, 1078],
      "layout_type": "2-Panel Asymmetrical Vertical Split",
      "layout_justification": "Vertical split mirrors the triage line dividing Lomi from the wounded.",
      "panels": [
        {
          "panel": 1,
          "characters_present": ["Lomi", "Raphael"],
          "dialogue_baked": ["Lomi, good to see you man."]
        },
        {
          "panel": 2,
          "characters_present": ["Raphael"],
          "dialogue_baked": ["Let the guys handle the fix—you figure out the big one."]
        }
      ]
    }
  ]
}
```

Rules:
- Every non-OOC scene block from the novelization manifest maps to **≥ 1 page** (zero-loss carries over to paneling).
- Character names must be canonical (alias map enforced at validation).
- `dialogue_baked` strings must be exact substrings of `sN-clean-story.md`.

### 6.4 Prompt Persistence — `sessions/storyboards/sN/prompts/p09-panel1.txt`

Every `generate_image` prompt is **saved to disk before generation**. This is what makes prompt-completeness auditing possible — without persisted prompts, nothing stops prompt drift between what was planned and what was sent.

### 6.5 Status File — `sessions/storyboards/sN/status.json`

Mutable runtime state, kept out of the hash-locked manifest:

```json
{
  "p09-panel1": {
    "prompt_file": "prompts/p09-panel1.txt",
    "image_file": "images/p09-panel1.png",
    "image_generated": true,
    "machine_vision_check": "pass",
    "human_audit_passed": null
  }
}
```

### 6.6 `verify_storyboard.py` — Mechanical Gates (all Python, all hard)

Collects all violations, then reports:

1. **Hash locks** — `clean_story_hash` matches `sN-clean-story.md` on disk; novelization manifest hash chain intact.
2. **Scene coverage** — every non-OOC scene block maps to ≥ 1 page; no page references an unknown scene; `line_range`s match the novelization manifest.
3. **Dialogue verbatim** — every `dialogue_baked` string is an exact substring of `sN-clean-story.md`. Catches paraphrase/invention at prompt-writing time.
4. **Prompt completeness** — for every panel, every character in `characters_present` has their **full token block** from `visual-tokens.json` present in the persisted prompt file. Missing prompt file = FAIL.
5. **Layout rules** — `layout_justification` non-empty on every page; adjacent pages never share identical `layout_type`; declared panel count matches `panels` array length; actual page count per scene matches plan.
6. **Alias enforcement** — all character names canonical per the alias map.
7. **Status reconciliation** — every panel has `image_generated: true` and `human_audit_passed: true` before the storyboard is declared complete. The script verifies the *attestation exists* — not the image content.

### 6.7 Visual Audit — Two-Tier Gate

Python cannot pass/fail image content, but the human shouldn't review raw generator output either:

- **Tier 1 (machine, cheap filter):** a vision-capable LLM pass per image with a mechanical checklist derived from the manifest: correct character count, each character's distinguishing tokens visible, baked dialogue legible and matching the expected string. Auto-reject obvious failures (wrong count, garbled text) and regenerate — the human never sees them. Result recorded as `machine_vision_check` in status.
- **Tier 2 (human, final authority):** approve/reject surviving images. Approval flips `human_audit_passed: true` in status. This is the only non-automatable step in either pipeline.

### 6.8 Workflow (`.agent/workflows/add-storyboard.md`)

1. Prerequisite: `sN-clean-story.md` has a HARD PASS from `verify_parity.py`.
2. LLM drafts `sN-storyboard-manifest.json` (pages, panels, layouts, dialogue).
3. `python sessions/scripts/verify_storyboard.py sN --pre` → validates gates 1–6 **before any image generation** (fail fast on plan defects).
4. Write all prompt files; re-run `--pre` (gate 4 now checks real prompts).
5. Generate images one panel at a time; Tier 1 machine-vision check each; regenerate rejects.
6. Human review (Tier 2); record approvals in `status.json`.
7. `python sessions/scripts/verify_storyboard.py sN --final` → all 7 gates → HARD PASS = storyboard complete.

### 6.9 What This Fixes vs. the Draft Analysis

| # | Draft-analysis gap | Fix |
|---|---|---|
| 1 | Dialogue-verbatim treated as human-ish check | Mechanical substring gate (6.6.3) |
| 2 | Prompt completeness unverifiable — prompts never persisted | Prompt persistence (6.4) + token-block gate (6.6.4) |
| 3 | Layout rules left to convention | Mechanical layout gates (6.6.5) |
| 4 | Visual audit = human reviews everything | Two-tier gate: machine filter first, human approves survivors (6.7) |
| 5 | Runtime state (`image_generated`) embedded in manifest, breaking immutability | Manifest = immutable plan; `status.json` = mutable state (6.3/6.5) |
| 6 | No ordering enforcement between prose and panels | Clean-story hash lock + HARD-PASS prerequisite (6.1) |
| 7 | Name drift inside token lookups ("Loami" vs "Lomi") | Alias map enforced in storyboard manifest (6.6.6) |
| 8 | `expected_page_count` declared but never audited | Actual-vs-plan page/panel count checks (6.6.5) |

---

## 7. Craft Layer — From "Faithful" to "Sanderson-Level"

The gates above guarantee nothing is *lost*. They do nothing to make the prose *good*. Fidelity-first drafting produces seams, flat transitions, and inconsistent voice — because each block is novelized in isolation. The craft layer fixes that **after** fidelity is locked, so polish can never silently delete content.

### 7.1 Two-Draft Contract

- **Draft A (fidelity draft):** the existing Step 3 output. Must pass `verify_parity.py` first.
- **Draft B (craft draft):** revision passes over Draft A. **Additive-and-rephrase only** — transitions, sensory grounding, interiority, pacing. The RAW_RANGE headers and LEDGER footers are carried through unchanged, and `verify_parity.py` is re-run on Draft B. Any polish that drops a ledger entry fails the audit. This is the key invariant: **craft passes are free to add, never free to subtract.**

### 7.2 Craft Passes (each is a separate, small LLM pass)

1. **Seam pass** — the highest-value fix. Blocks are novelized independently, so block boundaries are where transitions clunk. For each adjacent pair, the pass reads the last ~3 paragraphs of block N and first ~3 of block N+1 and rewrites only the junction (bridging beat, time/location connective, motif echo). Seams are exactly where "extra prose to clean up transitions" belongs — and added connective prose is legal under 7.1.
2. **Voice pass** — per-character **voice cards** (`sessions/craft/voice-cards.json`: diction, sentence rhythm, verbal tics, what they'd never say) fed into every novelization and revision pass. Lomi shouldn't narrate like Iggy.
3. **Continuity state** — a running `sN-story-state.json` updated after each block (who knows what, injuries, held items, time of day, emotional trajectory). Each block's prompt receives the state, not just a vague "story so far" paragraph. Prevents the classic micro-chunk failures: healed wounds, re-introduced characters, sunset happening twice.
4. **Style bible** — `sessions/craft/style-bible.md`: POV discipline (one head per scene), show-don't-summarize rules for high-ledger-density blocks, scene-sealing final lines, banned filter words ("he felt", "she saw"), metaphor domains per culture (Ash-Blood imagery ≠ Harmony imagery). Referenced by every prose pass so style is a checked input, not vibes.

### 7.3 Storyboard Craft Equivalents

- **Beat-to-panel discipline:** each page's manifest entry gains a `visual_beat` (one sentence: what this page *does* dramatically). Prevents "characters standing and talking" pages.
- **Shot variety guardrail:** mechanical check alongside layout rules — no 3+ consecutive panels with the same shot type (`shot` field per panel: close/medium/wide/insert).
- **Motif registry** (`sessions/craft/motifs.json`): recurring visual symbols (the gold receipt, moss, spire silhouettes) the prompt-writer can draw from, so pages rhyme visually.

---

## 8. Human Review Layer — The Review Dossier

The human should never re-read a 3,600-line raw file to check the pipeline's work. Every judgment call the LLM makes gets **recorded at the moment it's made**, then compiled into one reviewable artifact at the end.

### 8.1 Assumption Log — `sessions/transcripts/index/sN-assumptions.json`

Every pass (manifesting, novelization, craft, paneling) appends entries whenever it infers rather than transcribes:

```json
{
  "id": "A-017",
  "stage": "novelization",
  "scene_id": 8,
  "raw_lines": [1002, 1005],
  "type": "speaker_attribution",
  "assumption": "Attributed the unlabeled line 'not my circus' to Lomi based on context",
  "confidence": "low",
  "alternatives": ["Could be Ignatius — both were present"]
}
```

Types: `speaker_attribution`, `ambiguous_audio` (garbled/inaudible), `paraphrase` (indirect speech rewording), `invented_connective` (seam prose with no raw source), `visual_inference` (storyboard: appearance/setting details not in text), `chronology` (reordered cross-talk). Confidence: `high | medium | low`.

### 8.2 The Dossier — `sessions/review/sN-dossier.md` (generated by `build_dossier.py`, pure Python)

One document, ordered so the human reads the risky 5% instead of everything:

1. **Verdict header** — all gate results, counts, compression warnings.
2. **Low/medium-confidence assumptions first**, grouped by scene, each with: the raw lines quoted verbatim, the prose/panel that resulted, and the alternatives. High-confidence assumptions collapsed at the bottom.
3. **Seam gallery** — every block junction shown as before/after craft-pass text, since seams contain the only prose with no raw-line source.
4. **Compression outliers** — the WARN blocks from gate 4.5 with raw dialogue and prose side by side.
5. **Quote fidelity table** — every direct quotation in the prose next to its raw source line, so misquotes jump out.
6. **Storyboard contact sheet** — every page as thumbnail + layout type + `visual_beat` + baked dialogue + Tier-1 machine-vision result, in reading order. Flipping through the contact sheet **is** the Tier-2 human audit.
7. **Sign-off block** — checklists the human ticks; `verify_*.py --final` requires the sign-off markers to be present.

### 8.3 Review Efficiency Rules

- Anything the pipeline is *sure* about is collapsed, not shown. The dossier surfaces only inferences, seams, warnings, and images.
- Every dossier item deep-links raw line numbers (`L1002–L1005`) so spot-checking the ground truth is one lookup, not a search.
- Rejections are recorded in the dossier itself (tick "rework" + one-line note); `build_dossier.py --rework` emits the exact list of blocks/panels to regenerate — nothing else is touched, matching the existing partial-regeneration rule.

---

## 9. File Layout (Extended)

```
sessions/
├── scripts/
│   ├── prep_raw.py
│   ├── speaker_aliases.json
│   ├── verify_manifest.py
│   ├── verify_parity.py
│   ├── verify_storyboard.py
│   └── build_dossier.py
├── craft/
│   ├── style-bible.md
│   ├── voice-cards.json
│   └── motifs.json
├── review/
│   └── sN-dossier.md
├── storyboards/
│   └── sN/
│       ├── prompts/    p09-panel1.txt …
│       ├── images/     p09-panel1.png …
│       └── status.json
└── transcripts/
    ├── raw/    index/    clean/    (as in section 4)
    └── index/  sN-storyboard-manifest.json
characters/
└── visual-tokens.json
```

---

## 10. What Changed From v1 (Audit Findings)

| # | v1 gap | v2 fix |
|---|--------|--------|
| 1 | Coverage proved, fidelity unmeasured — a 3-sentence block passed | Dialogue ledger + reconciliation (Step 4.4) + compression guardrail (4.5) |
| 2 | Manifest was unverified LLM output; v1's own example violated the 150-line cap | New `verify_manifest.py` hard gate (Step 2) |
| 3 | Hash target ambiguous (raw vs. indexed) | Hash the indexed file only — one canonical artifact |
| 4 | First-error `sys.exit(1)` — one violation per run | Collect all violations, report together |
| 5 | No meta-talk policy — OOC lines indistinguishable from accidental drops | `ooc` blocks: covered, marker-only, excluded from fidelity checks |
| 6 | `### Subscene` blacklist of one | Header whitelist (`#`, `##` only) |
| 7 | Speaker-name drift (Ignatious/Loami) pollutes manifests | Canonical alias map applied at Step 0 |
| 8 | Everything dumped in `raw/` | `index/` directory for derived artifacts |
| 9 | GM identity and mic sharing lived in workflow prose and a global hardcoded `"Luke S": "GM"` alias | Per-session `sN-session-config.json` as a hard gate (§2.0); alias map demoted to spelling only |
