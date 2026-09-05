# Session 12 — old pipeline vs. config-gated pipeline: delta and accuracy audit

Compares the artifacts committed before this change —
`sessions/transcripts/index/s12-raw-indexed.md`, `s12-manifest.json`,
`sessions/transcripts/clean/s12-clean.md` — against what the config-gated pipeline
produces (`sessions/s12-devin/artifacts/`).

**Scope caveat, stated up front:** no new `s12-clean.md` was produced. The new
pipeline output is a per-line attribution artifact with decisions for **6 of 692**
`Luke S` lines. So this is not "old story vs. new story"; it is a comparison of the
*attribution layer* underneath the story, plus an audit of the old clean transcript's
speaker calls against the raw lines.

---

## 1. Mechanical label layer (`sN-raw-indexed.md`)

Same 1821 lines, same text; the only diff is speaker labels — 28 diff hunks, all of
them label-only.

| Raw stream | Old label | New label | New identities |
|---|---|---|---|
| Luke's mic | `**GM:**` ×692 | `**Luke S:**` ×692 | 8 GM · 8 Aggie (person `Kristina`) · 1 NPC (`Professor Inc`) · 686 `needs_decomposition` |
| John's mic | `**Ignatius:**` ×316 | `**John:**` | 316 Ignatius (`source: config`) |
| Luke F's mic | `**Lomi:**` ×273 | `**Luke F:**` | 273 Lomi |
| Sophie's mic | `**Britt:**` ×217 | `**Sophie:**` | 217 Britt |
| Holly's mic | `**Iggy:**` ×97 | `**Holly:**` | 97 Iggy |

**Deltas that matter**

1. **692 lines were asserted to be the GM.** That assertion is provably false: Aggie
   speaks on that mic (raw L0464, L0900, L0931, L0936 …), and 26 of those lines
   reference Aggie by name. The old artifact had no way to represent her.
2. **Kristina does not exist anywhere in the old chain** — not in the indexed labels,
   not in the manifest, not in the clean transcript's speaker set. Aggie appears only
   where the novelizing pass re-inferred her from sentence content.
3. **Routing was irreversible.** The old pipeline collapsed person → character inside
   `prep_raw.py` using a global alias (`"Luke S": "GM"`), so the character claim was
   baked into the hash-locked artifact and could not be re-derived or contested. The
   new artifact keeps the *observed* fact (which mic) separate from the *declared*
   fact (which identity), and every identity carries `source: "config"` or
   `source: "decision"`.

## 2. Manifest layer (`s12-manifest.json`)

The blocks containing Aggie's two biggest beats list:

```
[389, 492]  Basin Docks Field Hospital Triage   speakers_present: ['Ignatius','Lomi','GM','Britt']
[890, 1008] Pip Snack Break & Recruiting Lucky  speakers_present: ['GM','Iggy','Ignatius','Lomi']
```

Aggie is absent from both — the L0464 condolences to Val and the L0931 tortoise-stomp
line are filed under `GM`. Consequence: `verify_parity.py` could confirm 100 % line
coverage while Aggie's dialogue was rendered as GM narration, because the ledger it
audits against never claimed she was there. **This is the structural failure the config
gate removes**, and it is invisible to any Python check that trusts the manifest.

## 3. Old clean transcript audit (63 quoted lines vs. raw)

I traced every `**[[Speaker]] (PC/NPC):**` quote in `s12-clean.md` back to its raw line.

**Where the old clean is right (and the new pipeline agrees):**

* Every solo-mic PC quote I could match lands on the right mic — Britt ← Sophie
  (L0581, L0588, L0615, L0675), Ignatious ← John (L0240, L0250, L0262, L0585, L0677,
  L0847, L0880 …), Loami ← Luke F (L0299, L0987), Iggy ← Holly (L1713).
* Every NPC quote comes off the GM mic and is voiced by the GM — Rill (L0578, L0610,
  L0616), Zephyr (L0843, L0885), Bramble (L0298), Pip (L0690), Val (L0484),
  Raphael (L0499). The new model reproduces this as `kind: "npc"`,
  `voiced_by: "GM"`, `person: "Luke S"`.
* Genuine garble fixes are correct, e.g. raw L0675 `"Wait, am I calling the god turtle
  or **zaggy**?"` → Britt, "or Aggie" — right speaker, right cleanup.

**Where the old clean is wrong or lossy:**

| # | Old clean | Raw | Verdict |
|---|---|---|---|
| D1 | L191 `**[[Britt]] (PC):** "Whoa! Have you never seen a mushroom turtle?!"` | L0683 is on **Luke's mic**; Sophie's adjacent lines (L0680/0682/0684) are only `"Whoa."`. Two lines later Pip smacks Ignatius in the face. | **Misattributed.** A GM-mic utterance (contextually Pip) was merged with Sophie's "Whoa" and handed to Britt. The new pipeline cannot make this call: `Britt` is not a declared identity on the `Luke S` mic, and a decisions file saying so is rejected with `identity 'Britt' is not declared for mic 'Luke S'`. |
| D2 | L271 Aggie: `"…I don't think the god tortoise is happy with that answer. This is really important."` | L0931: `"…And I have a feeling this is really really important for not just for our pe my people but for everyone I think."` | **Lossy.** "not just for my people but for everyone" — an explicit Mizizi-worldview beat — is compressed away, against the zero-loss rule. |
| D3 | Aggie has **2 quoted lines in the entire session** (vs. Ignatious 18, Loami 11, Britt 6) | 26 `Luke S` lines name Aggie; her speech/intent appears in at least L0459, L0464, L0900, L0929, L0931, L0936 | **Under-represented.** Direct consequence of §1.1: a player whose mic was labeled `GM` gets summarized as narration. |
| D4 | No coverage of: Aggie establishing the subconscious comms link (L0757–L0759); the speaking-stone exchange where Aggie asks for snacks and Professor Inc. answers (L0936 — only Inc.'s side survives, relocated to a different scene at L319); Aggie's read on why the tortoise refuses (L0933); `"Agie follows"` (L1054) | present in raw | **Dropped beats**, all of them on the collapsed mic. |

## 4. Which one is accurate, and why

* **On solo mics (Sophie/John/Luke F/Holly) and on GM-voiced NPCs: both agree, and the
  old clean is accurate.** Nothing in this change contradicts it. The new pipeline just
  derives those calls from the declared config instead of from a global alias table, so
  they are reproducible rather than re-inferred each pass.
* **On Luke's mic the old artifacts are inaccurate by construction.** They asserted a
  single identity (`GM`) for 692 lines that demonstrably carry at least three (GM,
  GM-voiced NPCs, Aggie). Where the old *clean* transcript gets Aggie right, it does so
  by the novelizing pass re-reading sentence content — the very inference this change
  forbids — and the audit chain beneath it could not check the result, which is how D1
  survived.
* **The new artifact is accurate in the strict sense**: it never claims an identity the
  user didn't declare, it labels 686 lines `needs_decomposition` with
  `candidate_identities: ["GM","Aggie"]` instead of defaulting them to the mic's owner,
  and it rejects the class of error in D1 outright. Every one of its 17 resolved
  shared-mic segments was cross-checked against the clean transcript and holds.
* **But it is not a replacement yet.** The old clean transcript is the only complete
  narrative artifact (383 lines covering all 1821 raw lines). The new one resolves ~1 %
  of the shared stream. Accurate-but-1 %-complete does not beat
  complete-but-unverified for reading; it beats it for *auditing*.

**Recommendation.** Keep `s12-clean.md` as the narrative of record, and fix it against
the new attribution rather than re-novelizing: correct D1, restore D2's clause, and work
through the remaining 686 `Luke S` lines to recover Aggie's dialogue (D3/D4). That
audit is now a bounded, checkable task — `attribute_speakers.py --strict` fails until
every shared-mic line has an explicit call, so "done" is a machine-verifiable state
rather than a judgement.
