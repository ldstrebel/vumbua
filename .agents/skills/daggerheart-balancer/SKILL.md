# Custom Skill: Daggerheart Adversary Balancer

Use this skill when designing, balancing, or flavoring Daggerheart 1.6.1+ custom adversaries (NPCs) for the Vumbua campaign. This skill acts as a balancing agent, ensuring all stats, thresholds, attacks, and special features align with the official System Reference Document (SRD) from @[DH-SRD-May202025.pdf](file:///d:/Code/vumbua/meta/Daggerheart-Core/DH-SRD-May202025.pdf).

---

## 1. Official Adversary Stat Benchmarks (SRD p. 72)

When designing or scaling an adversary, baseline statistics MUST align with the official benchmarks below based on the creature's Tier:

| Adversary Statistic | Tier 1 (Level 1) | Tier 2 (Levels 2–4) | Tier 3 (Levels 5–7) | Tier 4 (Levels 8–10) |
| :--- | :--- | :--- | :--- | :--- |
| **Attack Modifier** | +1 | +2 | +3 | +4 |
| **Difficulty** | 11 | 14 | 17 | 20 |
| **Damage Thresholds** | Major 7 / Severe 12 | Major 10 / Severe 20 | Major 20 / Severe 32 | Major 25 / Severe 45 |
| **Damage Dice Range** | 1d6+2 to 1d12+4 | 2d6+3 to 2d12+4 | 3d8+3 to 3d12+5 | 4d8+10 to 4d12+15 |

*Note: In the Foundry VTT implementation, set both `evasion` and `difficulty` to the Difficulty benchmark value unless a feature or archetype dictates a higher/lower Evasion.*

---

## 2. Encounter Building & Point Budgets (SRD p. 71)

Use the following point budget values to balance encounters based on the party size:
* **Encounter Budget**: Start with `[(3 x number of PCs) + 2] Battle Points`.
* **Budget Adjustments**:
  * `-1` Battle Point for an easier/shorter fight.
  * `+2` Battle Points for a harder/longer fight.
  * `-2` Battle Points if using 2 or more Solo adversaries.
  * `-2` Battle Points if adding a static `+2` (or `+1d4`) to all adversaries' damage rolls.
  * `+1` Battle Point if choosing an adversary from a lower tier.
  * `+1` Battle Point if the encounter contains no Bruisers, Hordes, Leaders, or Solos.

### Adversary Cost Table:
* **1 Point**: Social, Support, or a group of Minions equal to the party size.
* **2 Points**: Standard, Horde, Ranged, or Skulk.
* **3 Points**: Leader.
* **4 Points**: Bruiser.
* **5 Points**: Solo.

---

## 3. Official Passive Templates (SRD p. 71)

When applying standard traits, use the exact SRD-approved nomenclature and formulas:

* **Minion (X)**:
  `Minion (X) - Passive: This adversary is defeated when they take any damage. For every X damage a PC deals to this adversary, defeat an additional Minion within range the attack would succeed against.`
  *(X maps to the creature's Major threshold size, e.g., Minion (3) or Minion (4)).*
  
* **Horde (X)**:
  `Horde (X) - Passive: When the Horde has marked half or more of their HP, their standard attack deals X damage instead.`

* **Relentless (X)**:
  `Relentless (X) - Passive: This adversary can be spotlighted up to X times per GM turn. Spend Fear as usual to spotlight them.`

* **Slow**:
  `Slow - Passive: When you spotlight this adversary and they don’t have a token on their stat block, they can’t act yet. Place a token on their stat block and describe what they’re preparing to do. When you spotlight this adversary and they have a token on their stat block, clear the token and they can act.`

* **Arcane Form**:
  `Arcane Form - Passive: This adversary is resistant to magic damage.`

* **Armored Carapace**:
  `Armored Carapace - Passive: When this adversary takes physical damage, reduce it by X.`

---

## 4. Vumbua Campaign Flavoring Rules

Apply the following flavoring parameters to align the mechanical SRD templates with the campaign's setting:

> [!WARNING]
> **NO SRD SETTING BLEED-IN**: The Daggerheart SRD PDF contains its own built-in setting called **"The Witherwild"** (including location names like *Haven*, *Fanewick*, *Archmage Phylax*, *The Great Owl Nikta*, and the *Serpent's Sickness*). 
> **Never** use or refer to these SRD setting elements. 
> All narrative beats, sensory descriptions, names, and dialogues must be strictly grounded in the **Vumbua** campaign setting (using locations like *Campus Harbor*, *Apex Arena*, *The Colonnade*, *Deep-Hull*, and campaign-specific NPCs/lore from the rules).

* **Setting Aesthetic Integration**: Sensory details and visual descriptions must reflect the campaign's unique tech-fantasy, ancient ruins, airships, and Witherwild overgrowth motif (e.g. *glowing copper runework, metal-feathered raptors, moss-veined constructs, and airship rigging*).
* **Geographical Consistency**: Align establishing shots and action beats with the exact local geography of the encounter (e.g. *high-altitude storm winds for the Tempest Clearing, thick toxic sludge for the Sunken Bogs, steep terraced basalt canyons for the Apex Arena*).
* **Session & Transcript Alignment**: Dialogues, quotes, and tactical beats must directly support the narrative flow and events in the corresponding clean transcript (`sessions/data/clean/sN-clean.md`), using ground-truth names and motifs.
* **Attack Reskinning**: Replace default attacks (like "Sword" or "Claws") with setting-rich options:
  * *Storm Raptor* -> *Wind-Cutter Talons* (deals physical damage + pushes target back).
  * *Ember Warg* -> *Cinder Bite* (deals magical damage + spends Stress to ignite).
* **Motives & Tactics**: Always document the creature's specific impulses, motives, and tactics (e.g. *Defend territory, isolate prey, flank targets*) to guide GM spotlight turns.
* **Cost Mechanics**: Distribute Stress and Fear costs meaningfully:
  * Minor/standard abilities should cost `1 Stress`.
  * Major environment-altering or high-damage attacks (e.g., breath weapons, area explosions) must cost `1 Fear` (GM metacurrency) to activate.


---

## 5. Official Environment & DM Guide Design Rules

When creating DM guides, master journal entries, or environment hazard sheets for encounters, they must align with the official SRD rules:

### 🏞️ Environment Stat Blocks (SRD p. 100)
Every encounter environment must be structured as a formal stat block containing:
* **Name**, **Tier**, and **Type** (Exploration, Social, Traversal, or Event).
* **Description**: A one-line summary.
* **Impulses**: Active verbs describing how the environment pushes/pulls the scene.
* **Difficulty Benchmark**: Standard Difficulty benchmark DC (Tier 1: 11, Tier 2: 14, Tier 3: 17, Tier 4: 20).
* **Features**: Specific mechanical hazards, traps, or rules changes (e.g., *Gondola Equilibrium*).
* **Feature Questions**: 3 narrative/plot prompts for the GM to customize the scene.

### ⏱️ Official Countdown Mechanics (SRD p. 68)
Countdowns (such as stabilization tasks or hazards) must use the official advancement tables:
* **Standard Countdowns**: Advance (decrement) by `1` every time any PC makes an action roll.
* **Consequence Countdowns (Dynamic Clocks)**: Advance based on action roll results:
  * *Failure with Fear*: Tick down 3.
  * *Failure with Hope*: Tick down 2.
  * *Success with Fear*: Tick down 1.
  * *Success with Hope*: No advancement.
  * *Critical Success*: No advancement.

### 🎮 GM Moves & DM Running Guides (SRD p. 63-65)
Tactical running guides must describe how the GM spotlight shifts, how soft and hard moves are applied, and how Fear is spent:
* **GM Moves**: Signal when the GM can make moves (e.g., PC rolls with Fear, fails an action roll, or there is a "golden opportunity").
* **Spending Fear**: Explicitly list what Fear actions are available to the GM (e.g., *steal the spotlight, make an additional move, activate an environment or adversary Fear feature*).
* **Tension Spending Guide**:
  * *Incidental Scene*: Spend 0–1 Fear.
  * *Minor Scene*: Spend 1–3 Fear.
  * *Standard Combat*: Spend 2–4 Fear.
  * *Major Boss (Solo/Leader)*: Spend 4–8 Fear.
  * *Climactic Encounter*: Spend 6–12 Fear.

### 🧠 Mandatory Running DM Reminders Page
Every generated encounter journal entry must contain a dedicated **"Running DM Reminders"** page or section containing these exact SRD reference tools:
1. **Duality Action Roll Quick Reference**:
   * *Success with Hope*: Action succeeds. Gain 1 Hope.
   * *Success with Fear*: Action succeeds with a cost/complication. GM gains 1 Fear.
   * *Failure with Hope*: Action fails. Gain 1 Hope. Spotlight swings to GM.
   * *Failure with Fear*: Action fails with a major consequence. GM gains 1 Fear. Spotlight swings to GM.
   * *Critical Success (Matching Dice)*: Automatic success with a bonus. Gain 1 Hope + clear 1 Stress. Deals critical damage.
2. **GM Spotlight Shifting Triggers**:
   * Reminder that spotlight shifts to the GM on any PC action roll failure or when the narrative dictates.
3. **GM Fear Spent Cheat Sheet**:
   * *Spend 1 Fear to*: Interrupt players to steal the spotlight; Make an additional GM move; Activate an adversary's Fear feature; Activate an environment's Fear feature; Add an adversary's Experience to a roll.

---

## 6. Narrative Presentation & Tactical GM Guidance

To make encounters feel dynamic and narrative-rich, every encounter journal must contain clear instructions on creature behaviors, sensory presentation, and dialogue:

### ⚔️ "The Monsters Know What They're Doing" (Tactical GM Guidance)
Every adversary stat sheet page in the journal must include a **"Tactics & GM Running Advice"** section containing plain-text bullet points that advise the GM on:
* **Target Priorities**: Which types of PCs the creature is naturally motivated to attack first (e.g. *Storm Raptor targets isolated scouts to prevent them from rallying; Ember Warg targets frontliners to wear down their Armor Slots*).
* **Movement & Positioning**: Plain-text tips on how the creature uses its mobility (e.g. *Skulks stay near shadows and move between cover; Snipers maintain Close-to-Far range and avoid getting tied up in Melee*).
* **Environment Synergy**: Plain-text tips on how the creature utilizes environment features (e.g. *Wargs drag tokens toward the Gondola Eyewall eyewall; Raptors attempt to pounce and knock targets off walkways*).
* **Morale & Flight Thresholds**: Clear guidelines for when the creature changes tactics, retreats, or surrenders:
  * *Wild Beasts*: Flee or retreat when reduced to 1 HP, or when their pack leader is killed.
  * *Mercenaries/Intelligent Foes*: Attempt to parley, yield, or flee when outnumbered 2-to-1, or when reduced to their last HP.
  * *Constructs/Undead/Fanatics*: Fight to the death without fear or hesitation.

### 🎭 Narrative Presentation & Creative Templates (SRD p. 62, 100)
Every encounter guide must include ready-to-use narrative blocks to relieve the GM's creative burden. Every running guide page must contain:

#### 🌅 1. Sensory Establishing Shot
A blockquote (`> [!NOTE]`) containing read-aloud text for the GM to set the scene, following this sensory template:
> **Sight**: [Vivid visual detail of the lighting, terrain, and adversary positioning]
> **Sound**: [Sensory noises, wind whistling, mechanical grinding, growls]
> **Smell**: [Environmental odor details: ozone, sulfur, damp loam, decay]
> **Atmosphere**: [Tension level, temperature, environmental humidity]
> 
> *"[Read-aloud flavor block summarizing the immediate threat as the scene opens]"*

#### 👤 2. Physical & Visual Descriptions
Plain-text physical profiles for every unique adversary type present on the field:
* **Ancestry/Type & Size**: [e.g. A hulking, soot-stained clay-and-dirt construct, standing 8 feet tall]
* **Clothing/Armor**: [e.g. Wrapped in a heavy, grease-smudged woolen traveling cloak]
* **Weapons/Features**: [e.g. Glowing, lava-veined cracks along its arms; primary attack is Fist Slam]
* **Distinguishing Marks**: [e.g. A crown of orange sparks floating above its head]

#### 💥 3. Narrative Action Sequences (Feature Beats)
For every major feature (Action/Reaction), provide a pre-written narrative prompt explaining **how to describe the action visually** when it triggers:
* *e.g. "When the Storm Raptor uses Lightning Talons, describe arcs of blue electricity leaping between its metal feathers, leaving the smell of ozone in the air."*
* *e.g. "When the Gondola Equilibrium countdown reaches 0, describe the wooden deck tilting sharply, ropes groaning as wood splinters and the wind pulls player tokens toward the eyewall."*

#### 💬 4. NPC Dialogue & Combat Quotes
Provide a quick-reference cheat sheet of flavorful quotes for intelligent NPCs corresponding to combat states:
* **Entering Combat (The Spotlight)**: *"[Flavorful quote setting their motive, e.g., 'This clearing belongs to the wind, intruders!']"*
* **Parley / Pressure (Marking Stress)**: *"[Quote showing tactical negotiation or combat stress, e.g., 'Stand down and I might spare your balloon!']"*
* **Defeat / Fleeing ( Morale threshold met)**: *"[Final quote or dying breath setting narrative seeds, e.g., 'The Storm will consume Haven... it has already begun...']"*





