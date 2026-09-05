# Transcript Provenance & Source Quality

Source-quality flags for every session's raw input. The parity ledger only
guarantees fidelity *to the indexed file* — it cannot detect that a source is
itself an AI-generated summary rather than a real diarized transcript.

## Canon vs. Planned — the master distinction

Everything in this repo falls into one of two trust tiers. This is the
single most important classification in the vault:

| Tier | Location | Trust |
|---|---|---|
| **Canonical** | `sessions/` pipeline outputs (diarized transcripts and everything derived from them), `campaign/` character/location/world records of things that *happened*, `novel/` | What actually occurred at the table. Ground truth. |
| **Planned** | `campaign/prep/` — session plans, DM prep notes, the narrative bible, storyboards, anything written *before* play | Intent, not fact. Always distrusted as canon; useful only as color when auditing transcripts. If prep and the session disagree, **the session wins.** |

`copilot/` conversations and AI-generated summaries sit below both —
reference material only, never canon.

Rule for every downstream stage: **planned material may inform, but may
never supply a canonical fact.** If a beat only exists in prep, it must be
flagged `planned_only: true` and cannot appear in reader-facing prose as
though it happened.

## Source Quality Classes

| Class | Meaning |
|---|---|
| `diarized` | Real per-line speaker turns (`**Speaker:** text`), indexed by `prep_raw.py`. |
| `ai-summary` | AI-generated meeting summary — NOT a transcript. Indexed by `index_secondary.py` (sentence-chunked, `[ai-summary]`-tagged lines). Secondhand input. |
| `undiarized` | Real full transcript from ONE undiarized audio source — all turns collapsed into a single "Me:" stream. Indexed by `index_secondary.py` at sentence granularity; `[TURN?]` marks heuristic turn-boundary guesses (question→answer, vocatives) — a scaffold for attribution, not speaker claims. |
| `survey` | Async choose-your-own-adventure doc; the clean file IS the primary source (no audio ever existed). Indexed by `index_secondary.py`. Verbatim by construction. |
| `missing` | No source of any kind. |
| `prep` | Planned material under `campaign/prep/` — session plans, DM notes, narrative bible, storyboards. Never canon; see "Canon vs. Planned" above. |

## Master Index (all 15 sessions)

| Session | Source | Indexed | Lines | SHA-256 (truncated) |
|---|---|---|---|---|
| s0 | diarized | `s0-raw-indexed.md` | 707 turns | 45ef1b1e |
| s1 | diarized | `s1-raw-indexed.md` | 1,278 turns | 180e736d |
| s2 | diarized | `s2-raw-indexed.md` | 1,107 turns | 6ccff56c |
| s2.5 | undiarized | `s2.5-raw-indexed.md` | 2,042 sents, 126 TURN? marks | ed50a656 |
| s3 | ai-summary | `s3-raw-indexed.md` | 270 | 9b2feb42 |
| s4 | diarized | `s4-raw-indexed.md` | 2,230 turns | 6336d494 |
| s4.5 | diarized | `s4.5-raw-indexed.md` | 512 turns | e84f5854 |
| s5 | diarized | `s5-raw-indexed.md` | 971 turns | d6221ec9 |
| s6 | diarized | `s6-raw-indexed.md` | 1,050 turns | 45227d6f |
| s7 | diarized | `s7-raw-indexed.md` | 1,954 turns | 4886cc74 |
| s7.5 | survey | `s7.5-raw-indexed.md` | 198 | 8855463c |
| s8 | diarized | `s8-raw-indexed.md` | 900 turns | 3688384b |
| s9 | diarized | `s9-raw-indexed.md` | 2,339 turns | 83e5f7cc |
| s10 | diarized | `s10-raw-indexed.md` | 4,876 turns | 444c5564 |
| s11 | diarized | `s11-raw-indexed.md` | 2,217 turns | 9eb31dbd |
| s12 | diarized | `s12-raw-indexed.md` | 1,595 turns | (pre-existing) |

Every session also has a `sN-provenance.json` (secondary sources) or
config-declared roster (diarized) describing its provenance.

## Gap Audit — `needs_generation`

| Session | Gap | Resolution path |
|---|---|---|
| **s2.5** | Full transcript exists but is undiarized (single "Me:" stream) | Attribution stage must diarize from text: `[TURN?]` marks give the boundary scaffold; speaker identity needs an LLM pass or audio review. Flag `low_confidence_attribution` on every beat |
| **s3** | No diarized transcript ever existed (Feb 25 doc checked — summary only) | Same as s2.5 |
| **s7.5** | Resolved — survey IS the primary source; not a gap | Indexed as `survey`; first-class canon |

## Notes

- s4.5's raw header confirms *"Luke S and Kristina shared same transcript
  lines"* — direct evidence the Luke S shared mic is recurring.
- The Drive doc titled "Session 7 – 2026/07/15" is a byte-identical duplicate
  of s8's transcript (mislabeled), not s7.5.
- s6 contains one `Result` artifact line (post-transcript screenshare dump).
- s10 folds `John Hagey's Presentation` (screenshare audio) into John's stream.
- Solo-labeled `Luke S` streams in s4–s11 may still silently carry Kristina
  (Failure Mode 5) — flagged in each session config's `_note`.
