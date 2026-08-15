# Session 12: old `s12-clean.md` vs. the attribution-derived clean

Two artifacts, both called "clean", built by different methods:

| | old | new |
|---|---|---|
| file | `sessions/transcripts/clean/s12-clean.md` (committed) | `sessions/s12-devin/artifacts/s12-clean-attributed.md` (generated, git-ignored) |
| built by | reading the raw transcript and writing scenes | `render_clean.py` over `s12-attribution.json` |
| speaker labels come from | the author's reading of sentence content | `s12-session-config.json` + `s12-attribution-decisions.json` |
| lines | 383 | 3,396 |
| words | 3,396 | 32,687 (indexed source: 29,993) |
| coverage of the 1,821 indexed lines | curated subset | every line, verified character-for-character |
| shared mic (`Luke S`) | one identity: `GM` | 692 lines decomposed: GM narration, 14 GM-voiced NPCs, Aggie |

The audit that made the new one possible is complete: all 692 `Luke S` lines now carry an
explicit decision, so `attribute_speakers.py --strict` passes and nothing is left as
`needs_decomposition`.

## Where the shared mic went

Old chain: 692 lines labelled `**GM:**`. New attribution of the same 692 lines:

```
444  GM narration          121  Rill          86  Professor Inc     29  Zephyr
 22  Lucky                  15  Aggie (Kristina)  15  Raphael        14  Pip
 10  Walker pilot            7  Bramble        6  Kale              5  Val
  3  Professor Kante         1  Camp bystanders  1  Ironclad captain
```

136 of the GM-narration entries are marked `ooc: true` — pre-session hotspot talk, character
sheet distribution, vial bookkeeping, the post-session campaign wrap-up. The old clean drops
that material entirely; the new one keeps it and labels it as table talk, which is what the
Tier C rule asks for.

## What the new clean fixes

1. **`"Whoa! Have you never seen a mushroom turtle?!"`** — old clean line 191 credits Britt.
   The sentence is on Luke's mic (`L0683`); Sophie's adjacent lines are just `Whoa.`, and Pip
   smacks Ignatius four lines later. New clean: `[[Pip]] (NPC, voiced by GM) [L0683]`.
2. **Aggie's tortoise plea is no longer trimmed.** The old clean ends it at "…happy with that
   answer. This is really important." The raw and the new clean keep "not just for our pe my
   people but for everyone I think."
3. **Aggie exists.** Old clean: 2 quoted Aggie lines. New clean: 13 Aggie entries / 377 words,
   each carrying `Kristina on Luke S's mic` — the mind-link attempt with Britt (`L0750`), going
   to Zephyr's cot (`L0818`), the yes/no interrogation of the tortoise (`L0900`, `L0929`),
   taking the speaking stone and negotiating provisions (`L0936`, `L0938`), the snack detour for
   Pip (`L1025`), following Britt into the lab (`L1054`), questioning tortoise protocol
   (`L1448`), and asking the outer trees for information (`L1600`).
4. **`s12-assumptions.json` A-001 is contradicted.** It read `L0279` as Ignatius crosstalk on
   Luke's mic. Ignatius is not declared on that mic, so the decision leaves the line with the
   GM and records why — the config refuses to widen attribution by inference.

## What the old clean still has that the new one does not

- **Scene and subscene structure**, locations, a session delta header, and NPC roster — the new
  render is a flat, anchored speaker list.
- **Readable prose.** The new clean is verbatim diarized speech: disfluencies, restarts,
  interleaved narration mid-sentence.
- **Campaign lore names not spoken in this session's audio:** `Mwaza-Kasa` (19×),
  `Mwangi`/`Brakkan`, `Valerius Sterling`, `Stadium Intercom` — none of those strings appear
  anywhere in `s12-raw-indexed.md`. Some of it is the ancestral vision, which was delivered to
  the players as text, not spoken, so no transcript-derived artifact can contain it.

That last point cuts both ways: the old clean is enriched beyond what the recording can support,
*and* it drops ~89% of the recorded words. Both are departures from the zero-loss rule, in
opposite directions.

## Verdict

The new clean is the accurate one on attribution and completeness:

- every speaker label traces to a user-declared fact (`gm`, `players`, `shared_mics`) or to a
  GM-voiced NPC on a mic the config says carries the GM;
- shared-mic speech names both the person and the character (`Kristina` → `Aggie`), so parity
  audits can see her;
- the render is provably lossless — the harness compares the rendered text against the indexed
  text character-for-character (punctuation aside) and now fails if a single word is dropped;
- the fixes above are each anchored to an `L####` line, so they are checkable rather than
  asserted.

The old clean remains the better *narrative* artifact: it is the only one with scene structure
and the only place the vision content lives. It is not, however, a trustworthy attribution
source for Luke's mic, and its Aggie coverage is not recoverable by re-reading it.

Recommended next step: keep `s12-clean.md`'s structure, but rebuild its dialogue from
`s12-clean-attributed.md` line by line — every quote gets an `L####` anchor and a speaker the
config can justify, with the vision section kept and marked as out-of-audio canon. Regenerating
the manifest/ledger afterwards means re-basing the s12 hash chain, which is a deliberate
decision to make separately.

## Follow-up: readability and table talk (after the comparison above)

Two problems the flat render had, both now fixed in `render_clean.py`:

**1. Characters were speaking during table talk.** Out-of-character was recorded per *mic*, and
only Luke's mic had been audited line by line — so while the GM read as table talk, the players
read as `[[Britt]]`, `[[Iggy]]`, `[[Ignatius]]` through the pre-session Wi-Fi and character-sheet
chatter: 203 of 918 PC segments sat inside stretches the GM's own decisions already marked as
table talk. Out-of-character is a fact about the *table*, so `s12-attribution-decisions.json` now
declares it table-wide, in `ooc_ranges` (L0093–L0230 pre-session, L1646–L1708 while everyone reads
the texted storyboard, L1731–L1821 wrap-up) plus 34 scattered `ooc_lines` (rules questions, "John
is saying this not Ignatius", the character-sheet/Roll20 delivery asides threaded through play, the
GM's NPC-voice mix-up). Anything they cover is labelled with the **person**:
`[[Sophie]] (out of character)`, not `[[Britt]]`. 347 segments are now out of character.
Boundaries were read off the raw lines; the criterion is written into the file — real-world/table/
meta content is out of character, while a player narrating their own character's action in the
third person is still play and keeps the character label.

**2. Dialogue was confetti.** Diarization splits a sentence every time somebody else makes a
noise, and the render emitted one entry per line, e.g. `[[Iggy]] "that's"` / `[[GM]] "Super"` /
`[[Iggy]] "annoying."`. The render now stitches each speaker's fragments back into sentence-level
turns in place — a fragment continues that speaker's previous turn when the turn was left
unterminated (or the fragment opens lower-case), the interruption was short, and the lines are
close in the index — so the example above becomes one entry, `[[Holly]] (out of character)
[L0107–L0112]: Wow, that's annoying.` 1,682 line-entries collapse to 1,244 turns. Nothing is
reordered (a turn is emitted where its first fragment fell), nothing is reworded, and the harness
still proves the render carries every word of the indexed transcript; `--no-stitch` returns the
line-per-line view.

The storyboard vision is also merged in now (see the kit README), so this clean is no longer
missing the content that only existed in the old one.
