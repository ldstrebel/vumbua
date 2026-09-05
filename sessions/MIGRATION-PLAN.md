# Repository Restructure & Branch Migration Plan

**Status:** Ready, deferred until the full narrative (through s12) is complete.
**Goal:** (1) restructure the vault so the final story is findable;
(2) split `main` into a reusable campaign-pipeline template, with Vumbua
living on its own branch.

---

## Target layout

```
vumbua/
├── novel/                        THE PRODUCT
│   ├── sessions/                 sN-story.md (per-session assembled story)
│   ├── chapters/                 CH01..N, monotonic across sessions
│   └── (book-1.epub, later)
│
├── sessions/                     THE PIPELINE — one folder per session
│   ├── s0/                       config, raw, raw-indexed, attribution,
│   │   ...                       decisions, manifest, clean-attributed,
│   │                             assumptions, blocks/, story
│   ├── s2.5/                     incl. speaker-guesses + provenance
│   ├── s7.5/                     survey source
│   ├── _scripts/                 all tooling
│   ├── _compare/                 diff reports
│   ├── PROVENANCE.md
│   └── README.md                 framework playbook
│
├── campaign/                     THE WORLD (Obsidian vault)
│   ├── characters/ bestiary/ factions/ locations/ world/
│   ├── planning/                 storyboard, narrative bible, book structure
│   ├── meta/ glossary.md timeline.md knowledge-tracker.md
│   └── index.md
│
└── _ops/                         ANTIGRAVITY-HANDOFF, review notes, audits
```

## File move map (current → new)

| Current | New |
|---|---|
| `sessions/transcripts/raw/sN-raw.md` | `sessions/sN/raw.md` |
| `sessions/transcripts/index/sN-*` | `sessions/sN/*` |
| `sessions/transcripts/clean/sN-*` | `sessions/sN/*` |
| `sessions/transcripts/clean/blocks/sN-*` | `sessions/sN/blocks/` |
| `sessions/transcripts/clean/sN-clean-story.md` | `novel/sessions/sN-story.md` (copy at assembly) |
| `sessions/config/sN-*` | `sessions/sN/config.json` |
| `sessions/config/campaign-config.*` | `campaign/config.json` |
| `sessions/planning/` | `campaign/planning/` |
| `sessions/review/`, `sessions/ANTIGRAVITY-HANDOFF.md` | `_ops/` |
| `sessions/compare/` | `sessions/_compare/` |
| `sessions/scripts/` | `sessions/_scripts/` |
| `sessions/storyboards/`, `sessions/audio/` | `campaign/storyboards/`, `campaign/audio/` |
| `sessions/s12-devin/` | delete (superseded) or `_ops/archive/` |
| `characters/ bestiary/ factions/ locations/ world/ meta/ Ink/ Excalidraw/` | `campaign/` |
| `glossary.md timeline.md knowledge-tracker.md index.md` | `campaign/` |
| `diff.txt git_search*.txt temp_* _export.* Pasted*` | delete |
| `.obsidian/` | root (vault-wide, keep) |

## Code changes required

- `session_config.default_sessions_dir()` → new `sessions/` layout.
- All `transcripts/{raw,index,clean}` literals in `prep_raw.py`,
  `attribute_speakers.py`, `render_clean.py`, `assemble_story.py`,
  `verify_parity.py`, `diff_runs.py`, `index_secondary.py`,
  `gen_session_configs.py` → per-session paths. The path-override params
  added earlier make this a small patch.
- `assemble_story.py` gains a `--story-out sessions/../novel/sessions/`
  step (or copies the final story into `novel/` automatically).
- Obsidian `[[wiki-links]]` inside campaign docs: `index.md` and recap
  links to `Session NN` notes must be remapped after the move.
- `.agent/workflows/add-session.md` and `session-audit` SKILL.md path
  references updated.

## Branch sequence (execute after full narrative lands)

1. Commit all outstanding work on `main`.
2. `git checkout -b vumbua && git push -u origin vumbua` — full vault preserved.
3. On `vumbua`: run the restructure as one atomic commit (`git mv` everywhere
   + path patches + a full `verify_parity` sweep for s0–s12 as the gate).
4. On `main`: delete all campaign content; keep template skeleton —
   `_scripts/`, framework README, `campaign-config.template.json`,
   empty `speaker_aliases.json`, empty `sessions/` tree, generalized
   skills/workflows.
5. New campaigns clone main, drop raws into `sessions/`, done.

## Verification gate for the restructure commit

- `verify_parity.py` passes for every session s0–s12 (post-move).
- `attribute_speakers.py sN --strict` passes for s0, s1, s2, s4.5
  (declared-shared-mic sessions).
- `find . -name "*-clean-story.md"` resolves to `novel/sessions/` only.
- No `sessions/transcripts/` references remain in scripts or skills.

## Open items (decide at execution)

- `Ink/` contents — campaign prose or tooling?
- `.obsidian/` — keep on template main (yes, probably: new campaigns are
  also vaults).
- `_notebooklm-export/` — keep on vumbua branch or archive.
- Whether `novel/` also gets the author-agent merge of s0 beats.
