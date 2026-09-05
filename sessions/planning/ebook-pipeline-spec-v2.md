# Transcript → Ebook + Audiobook Pipeline — Process Specification v2

**Status:** Draft for review
**Supersedes:** `ebook-process-audit.md` (architecture validated; this doc adds the missing contract, packaging, and audio stages)
**Scope:** Story-agnostic. All campaign/player/entity data lives in config files, never in code.

---

## 0. Design Invariants

1. **Fidelity Over Polish** — Player canon and soul beat literary smoothing. No retconning; connective tissue serves player intent, never replaces it.
2. **Deterministic first** — Zero tokens on anything regex/structure can prove. Tokens only where judgment is required.
3. **Closed-world accounting** — Every raw line is either rendered in prose, explicitly skipped (`ooc`), or logged in the assumptions ledger. Nothing silently vanishes.
4. **Speaker identity is resolved once** — at attribution time, never re-derived downstream. The audiobook never guesses speakers from prose.
5. **Atomic artifacts** — Every generated file is written write-then-rename. A crash can never produce a half-written block.
6. **Story-agnostic code** — All names, deny-lists, phonetic maps, voice casting, and character anchors are data, loaded per campaign.

---

## 1. Pipeline Overview (Left → Right)

```
STAGE 0  Session Config & Mic Gate          [deterministic + human]
STAGE 1  Line Indexing & Attribution        [deterministic + human gate on low-confidence]
STAGE 2  Scene Manifest & Dialogue Ledger   [LLM proposes, Python verifies]
STAGE 3  Micro-Chunk Novelization           [LLM, one block at a time]
         └─ emits: scene.md + state.json + assumptions.json
STAGE 4  3-Layer Editorial Suite            [Python lint → Showrunner → Cold Reader]
STAGE 5  Assembly & Parity Gate             [deterministic, hard-fail]
         └─ also extracts audio.json deterministically (Python, 0 tokens)

─── Primary milestone: validated sN-clean-story.md + per-scene audio.json ───

Downstream pipelines (on-demand, decoupled — see §3.7):
STAGE 6  Chapter Mapping                    [deterministic + bounded LLM assist]
STAGE 7  EPUB Packaging                     [deterministic]
STAGE 8  Audio Preflight & TTS Batch        [deterministic math → API]
```

---

## 2. Artifact Contracts

### 2.1 Raw Indexed Transcript — `index/sN-raw-indexed.md`
- Immutable `L####:` line indices. Hash of the raw file stored in the manifest.
- **Never edited after indexing.** Corrections happen at attribution/cleaning layers.

### 2.2 Session Config — `sN-session-config.json`
```json
{
  "session_id": "sN",
  "gm": "<label>",
  "players": [{ "label": "...", "mic": "..." }],
  "shared_mics": [{ "mic_label": "...", "carries": ["..."], "note": "..." }],
  "ooc_ranges": [[start, end]],
  "ooc_lines": [123, 456]
}
```
- Pipeline refuses to infer identity. Undeclared mic-sharing = hard stop.

### 2.3 Scene Manifest — `index/sN-manifest.json`
```json
{
  "session_id": "sN",
  "indexed_file": "...",
  "raw_file_hash": "sha256:...",
  "total_raw_lines": 1821,
  "scene_blocks": [{
    "scene_id": 3,
    "title": "...",
    "line_range": [231, 320],
    "ooc": false,
    "speakers_present": ["..."],
    "dialogue_ledger": [
      { "line": 240, "speaker": "...", "gist": "...", "confidence": "high|medium|low" }
    ]
  }]
}
```
- **NEW:** `confidence` on every ledger entry. `low`/`medium` entries are routed to human review before novelization. Shared-mic-decomposed lines must record `"decomposed_from_mic": "<label>"`.
- Python gate: zero gaps, zero overlaps across `line_range`s, hash matches raw file.

### 2.4 Scene Block — `clean/blocks/sN-scene-XX.md`
```
<!-- RAW_RANGE: [start, end] | SCENE_ID: n -->
<prose with <!-- Lxxxx --> anchors on every rendered turn>

<!-- LEDGER:
   rendered: [240, 243, ...]
   skipped_ooc: [255]
   assumption_refs: [A-003, A-007]
-->
```

### 2.5 Context Bridge — `clean/blocks/sN-scene-XX-state.json`
As specified in v1 (~200 tokens): `location_and_environment`, `characters_present[]`, `key_items_or_props[]`, `immediate_preceding_action`, `emotional_tone_or_tension`. **Emitted by the novelization step, consumed by the next block.**

### 2.6 Audio Manifest — `clean/blocks/sN-scene-XX-audio.json`  *(NEW — first-class artifact, extracted by Python)*
```json
{
  "scene_id": 3,
  "segments": [
    { "speaker": "Narrator", "text": "...", "source_lines": [231, 242] },
    { "speaker": "Ignatius", "text": "You hear that, guys? We passed.", "source_lines": [240] }
  ],
  "char_counts": { "Narrator": 412, "Ignatius": 33 }
}
```
- **Extracted deterministically by Python during Stage 5 assembly — never emitted by the LLM.** The novelization LLM writes only creative artifacts (`scene.md` + `state.json` + `assumptions.json`); it is never asked to do JSON bookkeeping or character arithmetic mid-prose (cognitive-overload failure mode: rushed prose or malformed JSON).
- Extraction algorithm: each rendered turn carries a `<!-- Lxxxx -->` anchor; the manifest `dialogue_ledger` maps every line → speaker. Python parses each scene block, matches quoted dialogue to its nearest anchor, attributes via `anchor → ledger → speaker`, assigns unquoted narration to `Narrator`, and counts characters arithmetically.
- **Orphan handling:** any quoted segment that cannot be attributed to an anchored ledger line is *not* guessed — it is flagged into the parity report for human ruling (prose quotes aren't always verbatim transcript: Tier-B narration, merged lines).
- `audio.json` segment count must equal `rendered` ledger count (parity cross-check).
- `char_counts` is precomputed per speaker — the "backup math" that isolates broken text and gives exact TTS cost without tokens.
- A scene-local phonetics map (`"Mwaza-Kasa": "mm-WAH-zah KAH-sah"`) may be attached for TTS tuning.

### 2.7 Assumptions Ledger — `index/sN-assumptions.json`
```json
{ "id": "A-001", "stage": "novelization", "scene_id": 3,
  "raw_lines": [275], "type": "ambiguous_audio|paraphrase|ooc_adjudication|anachronism",
  "assumption": "...", "confidence": "high|medium|low", "raw_text": "..." }
```
- Per-scene fragments merged at assembly; IDs reassigned sequentially.
- **Human review surface:** entries with `medium`/`low` confidence are the primary human gate (see §4).

### 2.8 Campaign Canon Config — `campaign-config.json` *(NEW — moves data out of code)*
```json
{
  "deny_list_players": ["..."],
  "deny_list_mechanics": ["..."],
  "deny_list_realia": ["..."],
  "phonetic_replacements": { "bad": "Good" },
  "canonical_entities": { "pcs": [...], "npcs": [...], "locations": [...] },
  "character_anchors": { "name": { "keywords": [...], "empathy_core": "..." } },
  "voice_map": { "Character": { "voice_id": "...", "stability": 0.5, ... } }
}
```

### 2.9 Rolling Campaign Ledger — `campaign-state.json` *(NEW — drift prevention)*
Persisted across sessions; updated at each session's end by the Showrunner pass:
- `character_state`: location, injuries, gear, unresolved personal threads
- `inventory`: canonical item locations
- `foreshadowing`: `{seeded_in, description, status: open|paid_off, expected_payoff}`
- Injected (~300 tokens) alongside the per-scene bridge. Scene state is ephemeral; campaign state is durable.

---

## 3. Stage Specifications

### Stage 2 — Manifest Generation
- LLM proposes scene cuts (80–150 lines) + dialogue ledger.
- Python verifies: contiguous coverage of `[1, total_raw_lines]`, no overlap, `ooc` blocks contain no in-world lines, ledger lines ⊆ block range.

### Stage 3 — Micro-Chunk Novelization
- Input: one scene block + previous `state.json` + campaign ledger + canon config.
- Output: three creative artifacts (`.md`, `state.json`, `assumptions.json`), written atomically. `audio.json` is **not** emitted here — it is derived deterministically at Stage 5.
- Prose rules enforced (from the Ebook Standard): quoted dialogue only, dedicated paragraph per speaker change, no embedded italic dialogue, full comedic arcs (Setup→Escalation→Punchline→Reaction), Tier-B player narration → narrator prose, game-state questions → sensory observation.

### Stage 5 — Assembly & Parity Gate *(hardened)*
For every non-OOC block, verify **all** of:
1. `RAW_RANGE` header matches manifest exactly.
2. Every `dialogue_ledger` line appears in the block's `rendered`/`skipped_ooc`/`assumption_refs` lists — **rendered lines must have a matching `<!-- Lxxxx -->` anchor in the prose.**
3. `audio.json` extraction succeeds: every quoted dialogue segment attributes to an anchored ledger line; **orphan quotes are flagged to the parity report, never guessed.**
4. `audio.json` segment count == rendered count; every segment's `source_lines` ⊆ rendered.
5. Layer-1 lint passes (leaks, embedded italics, phonetic drift, tense).
6. Block content hash recorded; a re-cut manifest auto-invalidates stale blocks.
- **Any failure aborts assembly.** Missing/invalid blocks never reach the story file.

### Stage 6 — Chapter Mapping *(NEW — downstream, on-demand)*
- **Narrative beats govern; word count is a soft guideline, not a quota.** Chapter cuts follow emotional resolution, POV shifts, and scene-ending hooks. A punchy 2,500-word ambush chapter is correct output; it is never merged just to hit a floor.
- Guideline band (~4,000–6,500 words) is used only to flag outliers for the Showrunner to re-examine — e.g., a bloated chapter that should be split, or a stub that might read better joined to a neighbor. Flagging ≠ forcing.
- Deterministic pass: group contiguous scene blocks at natural boundaries; prefer scene boundaries marked `cliffhanger|resolution` in the manifest. Never splits a scene mid-block.
- Bounded LLM assist: only when two candidate breaks are comparable does the Showrunner pick the stronger hook.
- Output: `sN-chapters.json` → `[{chapter: 1, title, scenes: [3,4], word_count}]`.

### Stage 7 — EPUB Packaging *(NEW — downstream, on-demand)*
- `sN-chapters.json` + scene blocks → valid EPUB 3: `mimetype`, `container.xml`, OPF manifest/spine, NCX/nav TOC, per-chapter XHTML, front matter (title page, campaign blurb, dramatis personae from canon config).
- Deterministic; a canonical-name sweep runs as a final lint inside the packager.

### Stage 8 — Audio Preflight & TTS *(NEW — downstream, on-demand)*
1. **Preflight (0 credits):** aggregate `char_counts` across all scenes → `chars × per-char rate` for the selected model → exact credit quote + per-voice breakdown, printed for approval before any API call.
2. **MVP:** single narrator voice for all segments (cheapest tier). `audio.json` already segments per speaker, so multi-voice is a later casting change, not a re-parse.
3. **Batch:** per-scene TTS calls with checkpointed outputs (`sN-scene-XX-seg-YY.mp3`), retry cap 3, quarantine on persistent failure, concat per chapter.

### 3.7 Downstream Decoupling
Stages 0–5 are the primary milestone: they produce a **complete, validated story** (`sN-clean-story.md` + per-scene `audio.json` + merged assumptions). Stages 6–8 are **on-demand consumers** of those artifacts, never part of the linear run:
- EPUB packaging is free and can be run anytime after Stage 5.
- TTS spends real credits and may happen weeks later — it must never gate or slow text production.

---

## 4. Human Review Protocol (≤ 1 hour/session)

| Gate | What you review | Est. |
|---|---|---|
| G1 — Attribution | Low-confidence speaker attributions, shared-mic decompositions | ~20 min |
| G2 — Assumptions | `medium`/`low` confidence ledger entries: approve / edit / reject | ~25 min |
| G3 — Parity report | List of unrendered ledger lines + unattributable orphan quotes (read the list, not the prose) | ~10 min |
| G4 — Exception spot-check | **Targeted prose read of the 2–3 most-flagged scenes** (stylistic warnings, assumption density, tension anomalies). Layers 1–3 act as an *exception highlighter* pointing at where human voice/tone judgment matters — inside jokes, voice drift, melodrama. Full-book read is never required. | ~10 min |

Review outputs feed back into the ledger (`"human_ruling": "approved|edited:<text>|rejected"`). This data model is designed so a future review UI (distant roadmap) is a thin frontend over the assumptions JSON — no schema change needed.

---

## 5. Batch Robustness (Nightly Runs)

- Atomic writes on every artifact (write `.tmp` → rename).
- Per-block retry cap (3), then `QUARANTINED` status — does not block other scenes.
- Assembly refuses to run with any `MISSING`/`INVALID`/`QUARANTINED` block.
- Manifest re-cuts invalidate stale blocks via `line_range` + content hash mismatch.
- Scheduler produces a run report: `{session, attempted, passed, failed, quarantined, cost_estimate}`.

---

## 6. Known Issues From Commit Audit (fix in Step 1)

- [x] ~~**Encoding corruption**~~ — **FALSE POSITIVE (verified at byte level):** zero U+FFFD characters exist; the `?"` hits were valid question-mark dialogue (`"What happened?"`) plus terminal display-mangling of em-dashes. No fix needed — and any automated "repair" would have corrupted real prose. One genuine style slip remains: `"Hey-what..."` uses a hyphen where an em-dash belongs; handle via normal prose lint, not encoding repair.
- [ ] **`__pycache__`/`.pyc` committed** — add Python `.gitignore` rules, remove tracked bytecode.
- [ ] **`verify_parity.py` not wired** into assembly or scheduler.
- [ ] **`batch_scheduler` doesn't schedule** — no loop/retry; currently a status reporter.
- [ ] **Hardcoded canon** in `harness/config.py` + `macro_auditor.py` → move to `campaign-config.json`.
- [ ] **Divergent misspelling tables** in `audit_scene_cluster.py` (has `Kim→Pip`, `Lazizi→Mizizi` not in config).
- [ ] **Common-word deny-list risk** — `john`, `holly` will false-positive on real prose; scope per-session or require explicit opt-in.
- [ ] **`audit_scene_cluster` bigram coverage** = the "Heuristic Keyword Coarseness" failure mode; replace with ledger-anchored verification.
- [ ] **Old audiobook scripts** guess speakers via pronoun regex — deprecated by `audio.json`; mark for rewrite.

---

## 7. Build Order

| Step | Deliverable | Depends on |
|---|---|---|
| 1 | Schemas + `campaign-config.json` + hygiene/encoding fixes | — |
| 2 | Parity gate wired into assembly; deterministic `audio.json` extraction; atomic writes; block hashing | 1 |
| 3 | `state.json` + `campaign-state.json` emission/consumption | 2 |
| 4 | Chapter mapper → `sN-chapters.json` | 2 |
| 5 | EPUB packager | 4 |
| 6 | Audio preflight + narrator-only TTS MVP | 2 (audio.json), 4 (chapter concat) |
| 7 (later) | Multi-voice casting registry; review frontend | 6 |
