---
name: novel-critic
description: Adversarial editorial review and forensic bloat scanning for novelized fantasy chapters and storyboards.
---

# 🗡️ The Ruthless Novel Critic & Bloat Auditor

Use this skill when auditing novel chapters, evaluating scene pacing, identifying purple prose, detecting talking-heads dialogue, and annotating narrative utility tiers (`[CORE-CANON]`, `[CHARACTER-COLOR]`, `[TABLE-BRIDGING]`) for developmental editing and abridgment passes.

---

## 🏛️ Prime Directive: The Aggressive Editor Persona

**Assume the prose is bloated until proven lean.** 

TTRPG actual plays are inherently conversational, meandering, and full of table warm-up rituals. Left unchecked, a novel adaptation will faithfully preserve every plate of muffins, every repetitive corridor walk, and every cyclical circular debate.

The Critic's job is **NOT** to praise the author for hitting word budgets or matching transcript line numbers. The Critic's job is to ruthlessly ask:
1. **Did anything change in this scene?** If no status, inventory, emotional stake, or physical position changed, the scene is dead weight.
2. **Are the characters standing around talking?** If dialogue exceeds 40% of the word budget without characters interacting with their physical environment, flag as **Talking Heads**.
3. **Is the setting description fresh or recycled?** If "polished brass," "warm mahogany," or "basalt canyon" appears for the fifth time in three chapters, strike it down.
4. **Is this table-warmup filler?** Eating breakfast, gathering syllabus papers, and walking down hallway berths are low-utility table filler.

---

## 🔬 Automated Telemetry: `critique_prose.py`

Run the forensic scanner against any novelized story file:

```powershell
python .agents/skills/novel-critic/scripts/critique_prose.py sN
```

To output a persistent critique artifact:
```powershell
python .agents/skills/novel-critic/scripts/critique_prose.py sN --out sessions/data/index/sN-critique.md
```

### Metrics Evaluated:
1. **Dialogue vs. Action Dynamic:** Measures spoken quotes against physical motion verbs (`ACTION_VERBS`). Flags scenes with high dialogue and <3 physical action verbs as `[TALKING HEADS]`.
2. **Sensory Overkill & Purple Lexical Echoes:** Tracks repetitive architectural and atmospheric clichés (`warm mahogany`, `gaslight lanterns`, `acrid ozone`) across rolling 1,000-word windows.
3. **Logistics & Filler Density:** Calculates the frequency of dining hall, corridor transit, and classroom syllabus banter per 1,000 words.
4. **Voice Profile Differentiation:** Tracks turn frequency, average words per turn, and distinct vocabulary profiles per POV character (`Lomi`, `Aggie`, `Britt`, `Ignatius`, `Iggy`).

---

## 🏷️ The 3-Tier Narrative Utility Taxonomy

Every scene block in `sN-manifest.json` should be annotated with its narrative utility tier:

| Tier | Tag | Definition | Action in Developmental Cut |
|---|---|---|---|
| **Tier 1** | `[CORE-CANON]` | High-stakes setpieces, exam challenges, boss encounters, major plot twists, and critical lore reveals. | **Preserve & Expand.** Do not cut. |
| **Tier 2** | `[CHARACTER-COLOR]` | Improvised comedy, chaotic character hustle, running gags (Lomi's Ambrosia of Luck, baby root-kin handoff). | **Preserve.** Keeps the book buoyant and distinct. |
| **Tier 3** | `[TABLE-BRIDGING]` | Breakfast buffets, corridor transit, polite diplomatic greetings repeated across POVs, syllabus chatter. | **Condense.** Compress into 1–2 transitional sentences. |

---

## 📋 The 5-Point Adversarial Audit Checklist

When evaluating newly assembled chapters or reviewing a finished session:

1. **The Cluttered Breakfast Test:**
   * Does the chapter open with characters grabbing food or stretching?
   * *Correction:* Cut directly to the conflict or the inciting arrival.
2. **The Ventriloquist Test:**
   * If you strip the dialogue tags, can you tell who is speaking?
   * *Correction:* Give Lomi shorter, blunter technical syntax; give Aggie watchful, sparse sentences; give Britt grounded botanical metaphors.
3. **The Sensory Overkill Test:**
   * Are we describing the room's woodwork while two characters are having an intense argument?
   * *Correction:* Anchor sensory details to emotional tension, not room catalogs.
4. **The Redundant Encounter Test:**
   * Did two characters experience the same conversation in different chapters (e.g. parallel survey runs)?
   * *Correction:* Weave parallel POVs into a single alternating chapter or summarize the known greeting in the second pass.
5. **The Zero-Delta Test:**
   * Did any secret get revealed, any coin get spent, any fear get stoked, or any injury occur?
   * *Correction:* If nothing changed, compress the scene by 50% or inject a mechanical obstacle.
