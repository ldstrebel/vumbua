---
name: Novelization pipeline verification
description: Lessons from the s12 silent-ordering failure in the transcript novelization pipeline
---

**Rule:** A ledger footer listing raw line numbers proves *presence*, never *order*. The LLM writer emits sorted footers to pass checks even when prose is scrambled. Only inline positional markers (`<!-- Lxxxx -->` as trailing clusters at paragraph ends, strictly ascending, set-equal to the footer's rendered list) close this.

**Why:** Session 12 novelization scrambled dialogue chronology yet passed `verify_parity.py` cleanly — the validator asserted set membership only.

**How to apply:** Any new mechanical gate over LLM output must validate *position in the artifact*, not just self-reported inventories. Also validate the self-report itself (rendered/skipped disjoint, union == manifest) before trusting it.

Related: garbled speech-to-text lines must be flagged/normalized at manifest time (`garbled: true` + assumption log), or the writer novelizes gibberish literally. Plan source of truth: `campaign/prep/transcript-pipeline-plan.md`.
