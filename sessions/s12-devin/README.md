# Session 12 — attribution kit (cold-start runbook)

Self-contained kit for re-running the speaker-attribution stage of Session 12 from
a cold start. Everything the pipeline needs to know about **who the GM is** and
**which mics are shared** is declared in `s12-session-config.json` — it is never
inferred from the transcript.

---

## Step 0 — Get the config from the user (HARD PREREQUISITE)

**Before any analysis, obtain and record the GM and shared-mic config from the user.**
The user always provides these two facts up front; the pipeline never guesses them:

1. **who the GM is**, and
2. **whether any mics are shared** — and which player rides whose mic.

They live in `sN-session-config.json`. `prep_raw.py` and `attribute_speakers.py`
refuse to run (exit code 2) when the file is missing or `gm` is absent:

```bash
$ python sessions/scripts/prep_raw.py s13
❌ BLOCKED — prep_raw.py cannot run for s13.
No session config found for 's13'. Searched:
    - sessions/s13-devin/s13-session-config.json
    - sessions/config/s13-session-config.json
    - sessions/transcripts/index/s13-session-config.json
```

Generic form (`sN-session-config.json`, schema documented in
`sessions/planning/transcript-pipeline-plan.md` §2.0 and the repo `README.md`):

```json
{
  "session_id": "sN",
  "gm": "<person label of the GM>",
  "players": { "<person label>": "<character>" },
  "shared_mics": [
    {
      "mic_label": "<the stream label diarization emits>",
      "note": "why this mic carries more than one identity",
      "carries": [
        { "person": "<owner>",  "identity": "GM",          "kind": "gm" },
        { "person": "<rider>",  "identity": "<character>", "kind": "player_character" }
      ]
    }
  ],
  "raw_speaker_labels": { "<garbled label>": "<canonical person label>" }
}
```

`shared_mics: []` is a valid, meaningful declaration: *no mics are shared this
session.* Leaving the key out is an error — silence is not a declaration.

### Session 12's declared facts

| Fact | Value |
|---|---|
| GM | **Luke S** |
| Shared mic | **`Luke S`** carries GM narration, GM-voiced NPCs, **and Kristina's Aggie** |
| Players | Sophie → Britt, Kristina → Aggie, John → Ignatius, Luke F → Lomi, Holly → Iggy |

Kristina has no stream of her own: Google Meet diarization filed all 692 of her
lines under `Luke S`. `raw_speaker_labels` documents that diarization is per-mic,
not per-person.

---

## Step 1 — Normalize the raw transcript

```bash
python sessions/scripts/prep_raw.py s12 --out-dir sessions/s12-devin/artifacts
```

Labels are normalized to canonical **person** labels (`Luke Strebel` → `Luke S`,
`John Hagey` → `John`) — never collapsed into characters or into `GM`. Output:
`artifacts/s12-raw-indexed.md` plus its SHA-256 and a per-stream summary that
marks which streams the config declares as shared.

> `--out-dir` keeps the kit's artifacts out of `sessions/transcripts/index/`, whose
> `s12-raw-indexed.md` is hash-locked into the completed `s12-manifest.json`
> novelization chain (that file predates person-label normalization).

## Step 2 — Attribute streams to identities

```bash
python sessions/scripts/attribute_speakers.py s12 \
    --index-dir sessions/s12-devin/artifacts \
    --out-dir sessions/s12-devin/artifacts
```

* Streams the config does **not** list as shared get exactly one identity, straight
  from `players` — no decomposition is attempted.
* Streams the config **does** list as shared are decomposed into the declared
  identities only. The per-line calls live in `s12-attribution-decisions.json`
  (`GM`, `Aggie`, or `NPC:<Name>` for a GM-voiced NPC); anything else is rejected.
  `NPC:<Name>` may not name a declared player character — the NPC path can't be used
  to launder a PC line out of its `person` attribution.
  Each segment's text must be a verbatim substring of its raw line.
* Undecomposed shared-mic lines are emitted as
  `kind: "needs_decomposition"` with the config's candidate identities — visible
  work, never a silent default to the mic's owner. `--strict` fails while any remain.

All 692 `Luke S` lines have been audited and carry an explicit decision, so
`--strict` passes. Out-of-character table talk is marked `"ooc": true` (Tier C)
rather than dropped.

## Step 3 — Render the clean transcript

```bash
python sessions/scripts/render_clean.py s12 \
    --index-dir sessions/s12-devin/artifacts \
    --attribution sessions/s12-devin/artifacts/s12-attribution.json \
    --out sessions/s12-devin/artifacts/s12-clean-attributed.md
```

Every speaker label in the output is a config-declared identity or a GM-voiced NPC,
anchored to its `L####` line. Text inside a shared-mic line that no decision claims is
emitted as an *unsegmented remainder* credited to the mic's GM slot — never folded into
a neighbouring speaker's quote. The renderer refuses to run while any line is still
`needs_decomposition`. See `s12-clean-comparison.md` for how the result differs from the
committed `sessions/transcripts/clean/s12-clean.md`.

## Step 4 — Run the harness

```bash
python sessions/s12-devin/test_attribution.py --list   # what the config generates
python sessions/s12-devin/test_attribution.py          # run it
```

The harness runs both stages into a scratch dir and asserts against the result.
Its per-stream assertions are **generated from the config**:

* every declared solo mic resolves to exactly its declared character;
* the `Luke S` mic must yield ≥ 1 GM-narration segment **and** ≥ 1 segment whose
  `character` is `Aggie` with `person: Kristina` — mandatory because the config
  declares that shared mic. Declare no shared mics and this assertion is simply
  not generated;
* no segment may carry an identity the config never declared, and NPC segments must
  be voiced by the declared GM;
* the rendered clean transcript is lossless — its text is compared against the indexed
  transcript character-for-character, so a dropped word fails the harness.

---

## Files

| File | Role |
|---|---|
| `s12-session-config.json` | User-provided facts: GM, players, shared mics, label spellings |
| `s12-attribution-decisions.json` | Per-line decomposition of the declared shared mic |
| `test_attribution.py` | Config-derived harness |
| `s12-clean-comparison.md` | Old committed clean vs. the attribution-derived clean |
| `artifacts/` | Generated (git-ignored): indexed transcript, `s12-attribution.json`, `s12-clean-attributed.md` |
| `sessions/scripts/session_config.py` | Loader + hard-gate validation |
| `sessions/scripts/attribute_speakers.py` | Attribution stage |
| `sessions/scripts/render_clean.py` | Clean-transcript renderer (attribution-driven) |
