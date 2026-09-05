# Handoff: Sessions 2+ Pipeline (Antigravity)

**From:** Devin (indexing & audit layer)
**State:** All sessions indexed. You own attribution → manifest → blocks →
assembly → parity/lint for every session from s2 onward.
**Baseline:** `verify_parity.py s0` and `s1` both pass. Match that bar.

---

## 1. Per-Session Status

| Session | Config | Source | Watch for |
|---|---|---|---|
| s2 | `s2-session-config.json` | diarized, 1,107 turns | Shared mic `Luke S` = GM + Aggie (label `GM or Aggie`). Roster: Luke F, John, Sophie, Kristina |
| s2.5 | none needed | **undiarized**, 2,042 sents | Two-person session (Luke S + Holly, "Dnd iggy"). See §3 |
| s3 | none | **ai-summary**, 270 lines | No real transcript exists. Generation-only; every beat gets `source_unverifiable` |
| s4 | `s4-session-config.json` | diarized, 2,230 turns | Solo `Luke S` stream — FM5 spot-check for silent Kristina |
| s4.5 | `s4.5-session-config.json` | diarized, 512 turns | Shared mic `Luke S or Kristina` declared. Tiny session — Luke S + Sophie only |
| s5 | `s5-session-config.json` | diarized, 971 turns | Solo Luke S — FM5 check. No Sophie/Kristina |
| s6 | `s6-session-config.json` | diarized, 1,050 turns | 1 `Result` artifact line (post-transcript dump) — mark OOC |
| s7 | `s7-session-config.json` | diarized, 1,954 turns | Kristina on OWN mic (`Kristina Raine` → `Kristina`) |
| s7.5 | none needed | **survey**, 198 lines | `s7.5-clean.md` IS the source. Primary canon — players' `Decision:` entries are verbatim input |
| s8 | `s8-session-config.json` | diarized, 900 turns | Solo Luke S — FM5 check |
| s9 | `s9-session-config.json` | diarized, 2,339 turns | Full roster |
| s10 | `s10-session-config.json` | diarized, 4,876 turns | Largest session. Screenshare stream folded into John |
| s11 | `s11-session-config.json` | diarized, 2,217 turns | Full roster |
| s12 | existing | diarized, 1,595 turns | Already partially done on canonical |

Master register: `sessions/data/PROVENANCE.md`.

---

## 2. Standard Pipeline Order (per diarized session)

```powershell
# config already exists — verify it
python sessions/_scripts/attribute_speakers.py sN --strict
# writes data/index/sN-attribution.json; --strict fails if any
# shared-mic line lacks a decomposition in sN-attribution-decisions.json

python sessions/_scripts/render_clean.py sN
# writes data/clean/sN-clean-attributed.md

# manifest: build sN-manifest.json (topic/scene cuts), then blocks
python sessions/_scripts/build_sN_manifest.py   # pattern from build_s0/s1
# draft blocks/sN-scene-XX.md with <!-- L#### --> anchors + LEDGER footers

python sessions/_scripts/assemble_story.py sN --title "..."
python sessions/_scripts/verify_parity.py sN    # must print [PASS]
```

## 3. Special Cases

### s2.5 — undiarized ("Dnd iggy", Feb 16)
- Index is sentence-level (`L####`), `[TURN?]` marks = likely turn boundaries
  (Q→A transitions, vocatives only — ~126 of them).
- `index/s2.5-speaker-guesses.json` has per-line Luke S/Holly guesses with
  confidence 0.4–0.9. Propagate speaker state across unknown lines inside
  confident runs rather than trusting line-level guesses.
- Two voices: Luke S = long narration/"what Iggy sees"/questions;
  Holly = "I think Iggy..." intent statements, backchannels.
- Flag every derived beat `low_confidence_attribution`.

### s3 — ai-summary only (Feb 25)
- No real transcript; the raw is a Granola-style summary.
- Generate canon from the summary; mark `source_unverifiable` in assumptions.
- Don't pretend speaker attribution exists.

### s7.5 — survey source
- `s7.5-clean.md` is the primary doc (Britt & Aggie's VIP Day, Aunt Angela).
- `Decision:` entries are verbatim player input — first-class canon.
- If beats need anchors, `s7.5-raw-indexed.md` stamps L#### on its nodes.

## 4. Contracts You Must Preserve

- **Shared-mic declaration**: never silently default a stream to its owner.
  s2 and s4.5 have declared shared mics; s4–s11 have solo `Luke S` streams
  that may still hide Kristina — spot-check address cues ("Christina", ...)
  before accepting a stream as pure GM. (Failure Mode 5.)
- **Uncertainty is written down**: `sN-assumptions.json` gets
  `author_review_required: true` entries for every interpretive call.
- **Ledger parity**: `verify_parity.py sN` must print `[PASS]` — 100% coverage,
  monotonic anchors, no phantom ledger entries, `(ooc)` tags on skips.
- **Lint**: `assemble_story.py` runs the editorial harness — player names,
  mechanics jargon, phonetic drifts are hard errors.
- **Canon vs OOC**: post-s0, OOC = non-canon table/social talk. Creation
  talk and lore are canon (prologue bucket for the author agent).
- **Sessions ≠ chapters**: monotonic chapter numbering; the book-1
  storyboard is `campaign/prep/book-1-narrative-structure.md`.
- **The 5 failure modes**: POV contamination, speculative overreach,
  clan-lore-as-truth, double-event redundancy, silent speaker absorption —
  all cataloged in `_ops/review/s1-pipeline-process-notes.md`.

## 5. My Role After Handoff

Devin = auditor, not co-author. I'll run `diff_runs.py`, parity, and lint
against your output and report divergence — especially on s2/s4.5 shared mics
and the FM5 spot-checks. Ping me when a session's artifacts land.
