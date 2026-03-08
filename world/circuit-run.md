---
aliases:
  - Circuit-Run
  - Resonance Race
  - Reso Race
  - The Circuit-Run
  - Reso-Race
tags:
  - world-lore
  - sport
  - harmony
---

# The Circuit-Run

> *"I also hear there is a RESO-RACE coming after the first week of classes! A perfect place to prove your metal to the Captains."*
> — [[Valerius Sterling]], radio broadcast

The **Circuit-Run** (colloquially: **Reso Race**) is the premier sport of Harmony — a brutal combination of exploration race, engineering competition, and living simulation of the Great Stitching, the ancient territorial unification that defined the Republic.

Teams or soloists pilot custom craft through a wilderness arena, striking resonance Spires to build a stored connection. The first team to accumulate enough connection to overcome their craft's deficit — and then reach the Grand Resonator at the arena's centre — wins. Beyond that: anything goes.

---

## Core Concept

The Reso Race exploits the same technology that powers Harmony's infrastructure — but in reverse.

In ordinary life, umber crystals let devices carry a stored connection to the land's resonance network. In the Circuit-Run, a rig's umber gutter is calibrated to do the opposite: it **severs** the craft's natural ambient connection, creating an artificial deficit. The crew must manually rebuild that connection by striking **Spires** — simulated resonance nodes erupting from the arena floor at timed intervals.

The bigger and more powerful the craft, the larger the deficit it must overcome. A racing sailboat crew might need three or four Spire strikes. A dreadnought crew might need a dozen. This creates the central tension of the sport: **brute force is a liability, not an advantage.**

There is more than one path to victory. A team that cannot outrun rivals can attempt to destroy or disable them — clearing the field and then completing the race at leisure. Aggression is a recognised and legal strategy; it simply carries costs the same as everything else.

---

## The Arena: The Apex Ring

The Circuit-Run takes place in a large natural basin called the **Apex Ring** — a roughly circular geographic depression, open at its southern face.

### Shape and Orientation

The basin is horseshoe-shaped, opening toward the south. Its rim is high stone, and the inner circumference carries the **Apex Compass** — the race's primary spectator and racer information system. The **Grand Resonator** pylon stands at the geographic centre: an obsidian obelisk that serves as the race's finish line.

### Terrain

The basin floor contains varied terrain, and this matters: **Spires spawn in terrain matching their origin city's geography.** A node from a coastal city appears near water. A node from a mountain city appears in rocky elevation. Teams that understand the geography of Harmony's cities can read the Apex Compass and predict *where* in the arc to look — not just which arc is active.

| Terrain Zone | Geography | Nodes Typically Found |
|---|---|---|
| **Southern Estuary / Open Water** | Shallow water deepening to navigable channel | Trail-Tail Trench, Bay of Breath, Prima, Minnow, Nstyl |
| **Petrified Forest (west)** | Dense stone trunks — visible through from above or out to the rim, opaque at ground level | Feltland, Relina, Bloomfield |
| **Rocky Canyons (south/inner)** | Carved stone, narrow passages, elevation variance | Shepta, Lenoa, Settika |
| **Open Volcanic Flats (north)** | Wide and treeless; exposed; no cover | Gilded, Juxta, Elysium, Timon |
| **Mid-Basin (centre)** | Mixed terrain, open sight-lines to the Grand Resonator | Octo, Umbra Mountain |

> **Petrified Forest visibility note:** The stone trunks are large enough to block horizontal sight-lines completely at ground level — rigs inside the forest are invisible to rigs outside it. However, from the bleachers and from Gilded Zephyr altitude, the forest is fully visible top-down; and from *inside* the forest, the trunk spacing is wide enough that crews can still see *out* toward the rim and read the Apex Compass.

### The Southern Gate — Mixed Start Line

The horseshoe's open south face is the **Southern Gate** — the race's start line, divided down the middle:

- **West half — Land approach:** Rocky canyon floor, wide enough for side-by-side heavy rigs
- **East half — Water approach:** Shallow estuary that deepens into navigable open water as it enters the basin; navigable by boats, amphibious rigs, and shallow-draft hulls

Ground and water rigs queue at the gate and charge through simultaneously at the Opening Horn. No weight-class separation for the ground start.

### The Drop — Aerial Launch

[[walker-core|The Walker-Core]] (Vumbua Academy's four-legged industrial mech) parks two legs on the southern rim during race day, its raised arm functioning as the official **drop gantry** for aerial and slung rigs. Aerial rigs launch from the Walker-Core in weight order (lightest first), timed to coincide with the ground horn.

The Drop is dramatic and precise. Gryphon rigs bank immediately on thermal catch. Slung light rigs are fired at calculated angles. Heavy aerial rigs release into controlled descent.

> **This year:** The Walker-Core gantry is present at Vumbua-hosted races. Other venues use fixed launch towers or cliff-edge sling rails.

---

## The Energy System

### Stored Connection and the Deficit

Every rig enters the race with a **Connection Deficit (CD)** — the gap between how much resonance it currently holds in its umber gutter and how much it needs to prove it has truly reconnected.

`CD = Global Amplitude + Craft Draw + Launch Penalty − Stored Connection`

- **Global Amplitude (GA):** Set pre-race by Scrivener Guild, reflecting the basin's ambient resonance output. Not publicly disclosed — spectators see LEDs, not numbers.
- **Craft Draw:** The rig's rated power consumption, including all mounted weapons and equipment. Declared at Certification Lock and fixed for the race.
- **Launch Penalty:** A fixed handicap by rig class, applied at the starting moment.
- **Stored Connection:** Accumulated through Spire syncs. Starts at zero.

> **Two separate concepts:** A rig's **harmonic energy** (what it uses to move, operate, and fire weapons) is distinct from its **stored connection** (the CU accumulated in the umber gutter through Spire syncs). The race deficit is a measure of stored connection, not fuel. A rig can be fully operational with a large deficit — it simply hasn't proven its reconnection yet.

### Cascade Drain — The Ongoing Cost

Operating a rig is not free. Every Loom-Pulse interval in which a rig does **not** sync a Spire, its deficit grows:

**Drain Rate = Craft Draw ÷ 10 (rounded up), added to CD at the end of each pulse without a sync.**

This means:
- Heavy rigs bleed fast if they park, block, or hunt without farming
- Light rigs can afford to be more selective — their drain is minimal
- Any tactic that delays syncing has a quantifiable cost

Mounted weapons, battering equipment, and heavy mechanical systems are **always included in the Craft Draw calculation**, whether used or not. A ballista on deck costs Drain Rate every pulse it sits unfired.

### The Two-Stage Win Condition

Progress is tracked through two independent LEDs on the Apex Ring scoreboard:

**LED 1 — Rig Power** *(the craft can sustain itself)*
| State | Condition |
|---|---|
| 🔴 Red | `Stored Connection < Craft Draw + Launch Penalty` |
| 🟢 Green | `Stored Connection ≥ Craft Draw + Launch Penalty` |

**LED 2 — Resonator Eligible** *(ready to discharge)*
| State | Condition |
|---|---|
| 🔴 Red | `Stored Connection < Craft Draw + Launch Penalty + Global Amplitude` |
| 🟢 Green | `Stored Connection ≥ Craft Draw + Launch Penalty + Global Amplitude` — **CD ≤ 0** |

**LED 2 cannot go green before LED 1.** Because the Global Amplitude is always positive, the second threshold is always higher than the first — teams pass through LED 1 green before reaching LED 2 green. Both LEDs can revert to red if cascade drain reduces stored connection below either threshold.

A team may only attempt a Grand Resonator discharge when **both LEDs are green**.

---

## Race Structure: The Four Horns

The Circuit-Run is structured around four horns, each audible across the entire basin. Three are timed; one is condition-triggered.

### Horn 1 — Opening Horn *(T+0)*

The race begins. Simultaneously:
- The **Walker-Core drops** aerial rigs (lightest first)
- Ground and water rigs **charge the Southern Gate**
- **All Phase 1 Spires erupt** across the basin — positions are **fully random**. No team knows where they will be. The Apex Compass illuminates as the nodes breach the surface, giving the first directional read to anyone watching.

The randomness of the opening wave is intentional and non-negotiable. Pre-planned routes become liabilities; teams that read the Compass and adapt fastest gain the early advantage.

### Horn 2 — Loom-Pulse 2 *(T+40 min, fixed)*

A second wave of Spires erupts. Spawn logic:
- **Reactive placement:** New Spires prefer arcs furthest from currently occupied (rig-dense) sectors. The Compass shows which arcs are quiet; new nodes appear there.
- **Companion spawns:** Any Spire from Horn 1 that went completely unsynced since eruption spawns a **companion node** nearby. Companion nodes are generic — no city, no boon, just raw connection CU. They do not count toward the canonical node set. They represent resonance pooling in neglected areas of the network.

### Horn 3 — Loom-Pulse 3 *(T+80 min, fixed)*

The third and final timed wave. Same spawn logic as Horn 2 — reactive placement, companion spawns for anything still untouched since Horn 2.

By Horn 3, every active node type from the 16 Harmony cities will have appeared at least once in the race. Charges determine how many teams can sync each node — a Major node with three charges can serve three teams; a Minor node with one charge is first come, first served.

### Horn 4 — Convergence Horn *(Condition-triggered)*

**Fires immediately when the first team reaches both LEDs green.**

This horn signals the endgame:
- No new Spire waves
- No new companion spawns  
- The Apex Compass shows only what remains active
- The race ends when a team with both LEDs green strikes the Grand Resonator
- Cascade drain continues — teams not yet eligible are bleeding toward zero without new nodes to recoup from

Teams that cannot reach eligibility from the remaining active Spires are effectively eliminated by drain. No formal elimination announcement is made; the math handles it.

**There is no tiebreak.** First team with both LEDs green to physically strike the Grand Resonator wins. Everyone else loses.

---

## The Harvest-Prong

The **Harvest-Prong** is the tool used to physically strike a Spire and initiate a sync. Every certified rig must carry one.

**Critical design requirement: the Harvest-Prong is man-portable.**

The Scrivener Guild mandates that all certified Prongs be detachable from their mount and operable by hand. Spires spawn in terrain rigs cannot always reach — shallow water, gaps between stone trunks, cliff faces, sub-surface in the estuary. Someone has to physically get to the Spire.

**In practice, this means:**

| Scenario | Approach |
|---|---|
| **Well-designed rig** | Extended or articulated Prong arm lets the operator strike from inside the cockpit without dismounting |
| **Standard crew** | Designated striker dismounts, navigates to the Spire on foot, deploys the hand-held Prong, syncs, returns to rig |
| **Solo pilot / tight terrain** | Pilot must leave the rig to strike, leaving the vehicle unattended and unprotected |
| **Aerial approach** | Pilot holds the Prong out while the rig descends over the Spire crown — no dismount, but high precision required |

The crew-size advantage: a large crew can designate strikers by terrain type (swimmer for water nodes, climber for rocky elevation) while keeping the rig manned. A solo racer has no such luxury.

**Syncing a Spire:**

| Step | Action |
|---|---|
| **1. Tune** | Operator matches the Prong's frequency to the Spire's vibration |
| **2. Strike** | Prong physically contacts the Spire |
| **3. Consume** | Connection energy transfers into the rig's umber gutter |

---

## The Spires (Nodes)

Spires are large resonance pillars that erupt from the ground (or water floor) during Loom-Pulse intervals. Each is constructed and maintained by the city whose node it represents, sharing a common mechanical skeleton — tall pillar, Prong-contact terminal at the apex, charge counter inset in the column face — but built in the unmistakable aesthetic of its origin.

### Node Activation and the Contention Window

When a rig (or crew member on foot) enters **Harvest-Prong reach** of an active Spire, the node **activates**:
- The Spire's crystal crown brightens visibly
- The corresponding Apex Compass arc begins **pulsing** instead of holding steady
- The node has entered an **activation window**: the sync must complete before the next horn fires

**If the next horn fires before the sync completes:** the activation window resets. The rig may attempt again next interval — but pays another full pulse of Drain Rate for the delay, and the window closure removes any companion-spawn benefit that might have accumulated.

**Pulse-and-retreat:** A team that intentionally enters Harvest-Prong reach and retreats without syncing causes the Compass arc to pulse and then reset. This is a legal tactic — it signals intent to spectators and may disrupt rival positioning — but it costs Drain Rate and yields nothing.

### Contention Bonus

When two or more rigs have crew within **Harvest-Prong reach** of the same Spire at the moment one team's sync completes, that team earns **+10 CU bonus**.

- Contention is checked at the **moment the sync finalises** — not when the approach started
- The bonus is flat (+10 CU) regardless of how many rivals are in range
- No declaration required — contention fires automatically when the condition is met
- A team that cannot win a sync race may still approach the Spire to deny the rival the bonus, even if they cannot complete themselves — this is a legal sacrifice play

> *"Within Harvest-Prong reach" = Close range. This is the same bracket used for Tier 1 weapon effects.*

### Companion Nodes

If a Spire has gone completely unsynced since its eruption when the next horn fires, a **companion node** spawns nearby:

- Generic structure — no city aesthetic, no boon
- Provides raw connection CU only (amount set by GM, typically 15–20 CU)
- Does not count toward the "one of each node type per race" canon
- Represents resonance pooling in neglected areas — lore-consistent with how real nodes grow through proximity and activity, not isolation
- Companion nodes spawn near the unsynced Spire they're adjacent to; the Compass arc for that sector shows two close indicators

### Node Charges

| Tier | CU | Charges | Examples |
|---|---|---|---|
| **Major** | 70–80 | 3 | Gilded (Chime), Umbra Mountain (Umber Crystal) |
| **Moderate** | 35–45 | 2 | Juxta (Lift Stone), Feltland (Live Soil), Relina (Soft Forge), Timon (Focus Glass) |
| **Standard** | 25–35 | 2 | Shepta (Whetstone), Lenoa (Friction Needles), Settika (Prism Falls), Octo (Speaking Stone), Prima (Dew Crystal) |
| **Minor** | 15–20 | 1 | Minnow (Living Scent Wood), Bloomfield (Clockwork Blooms), Nstyl (Silent Silt), Bay of Breath (Breathable Algae), Elysium (Snow Sand), Trail-Tail Trench |

### Spire Visual Design

Each Spire is architecturally distinct — built to its city's visual identity, with the Apex Compass color drawing from the same palette:

| Origin | Node | CU | Compass Color | Visual Identity |
|---|---|---:|---|---|
| [[gilded\|Gilded]] | Chime Spire | 80 | **Gold** | Organ-pipe brass columns. Layered and elaborate. Audible — actual tones ring when activated. Unmissable. |
| [[umbra-mountain\|Umbra Mountain]] | Umber Crystal | 70 | **Deep violet** | Faceted obsidian, glowing from within. Cold to touch. Looks powered before it's struck. |
| [[juxta\|Juxta]] | Lift Stone | 40 | **Blue-grey** | Smooth monolithic granite, orbiting rock fragments at the apex. Upward air current — felt before seen. |
| [[relina\|Relina]] | Soft Forge | 45 | **Bronze-amber** | Surface shimmers like slow liquid metal. Warm to touch. Slightly unsettling to approach. |
| [[feltland\|Feltland]] | Live Soil | 35 | **Earth brown** | Organic casing, vines at the base. The only Spire that smells like something. Always warm. |
| [[timon\|Timon]] | Focus Glass | 35 | **Clear/prismatic** | Lens architecture. Refracts light in unexpected angles — creates optical distortion nearby. |
| [[settika\|Settika]] | Prism Falls | 30 | **Rainbow facet** | Multi-surface crystal. Looking through or near it shows the world slightly differently. |
| [[shepta\|Shepta]] | Whetstone | 30 | **Dark charcoal** | Sharp geometric facets. Sparks visibly when struck. |
| [[lenoa\|Lenoa]] | Friction Needles | 30 | **Silver** | Multiple thin parallel needles rather than one column. Frictionless surface — requires deliberate Prong placement. |
| [[octo\|Octo]] | Speaking Stone | 25 | **Pale grey** | Rounded, smooth, inscribed with text. Hums at low frequency before and during sync. |
| [[prima\|Prima]] | Dew Crystal | 25 | **Ice blue** | Condensation runs down it constantly. Small puddle always at the base. |
| [[minnow\|Minnow]] | Living Scent Wood | 20 | **Warm amber** | Organic wood rather than metal or crystal. Faintly fragrant. Softer Prong contact than stone. |
| [[bloomfield\|Bloomfield]] | Clockwork Blooms | 20 | **Copper** | Mechanical flowers that open and close rhythmically. Ticking audible near the base. |
| [[nstyl\|Nstyl]] | Silent Silt | 20 | **Matte grey-brown** | Almost invisible in low light. Produces no sound when struck — the only silent sync in the race. |
| [[bay-of-breath\|Bay of Breath]] | Breathable Algae | 20 | **Bioluminescent green** | Erupts from the water floor. Produces bubbles and light mist. Faintly biological smell. |
| [[trail-tail-trench\|Trail-Tail Trench]] | Trench Seeds | 15 | **Deep teal** | Emerges from deep water — only reachable by swimmers or water-craft strikers. The Prong contact feels like touching open ocean floor. |

> **Permanently dark arcs:** The [[ash-blood-isles\|Ash-Blood Isles]] Compass arc never illuminates — its node data has not been submitted to the Scrivener Guild. Two versions of the terrain exist in the basin (the Ash-Blood topography is accurately rendered), but no Spire rises from it. Spectators notice. Officials do not comment.

---

## The Apex Compass

A continuous ring of **16 directional indicators** mounted on the Apex Ring's inner rim wall — one per 22.5° arc of the basin floor. The Compass is the primary information source for spectators and crews throughout the race.

| Signal | Meaning |
|---|---|
| **Dark** | No active Spire in this arc |
| **Dim / Steady** | Active Spire in this arc — distance varies |
| **Two close indicators in one arc** | Two Spires in the same arc (original + companion, or two simultaneous spawns) |
| **Pulsing** | A Harvest-Prong is within reach — activation window open |
| **Color** | Origin city identity (see Spire Visual Design table) |

**Multiple Spires in one arc:** The node physically closest to the arena rim appears on the **left (clockwise) edge** of the arc indicator. The furthest appears on the **right (counter-clockwise) edge**. Teams reading the Compass from inside the forest or from their rig can distinguish near from far within the same sector without coordinates.

**Reading the Compass well is a skill.** All arcs are visible simultaneously. Teams that understand node geography can infer *which* node is lighting an arc and *where in that terrain zone* to look for it. Teams that don't, see only a direction.

---

## Combat and Weapons

All combat draws from the same connection pool as the win condition. Fighting is always a trade-off.

### Weapon Tiers

| Tier | Type | Craft Draw Impact | CD Cost at Firing | Notes |
|---|---|---|---|---|
| **0 — Manual / Body** | Unaided human action | None | Free | Boarding, hand weapons, grappling. No amplification. |
| **1 — Vehicle-Assisted** | Passive systems/mass | Included at Certification Lock | Minor (−5 CD per use) | Rams, battering prows, spiked wheels, speed boosters, magnetic grapples. Close range only. |
| **2 — Direct Fire** | Armed weapon systems | Included at Certification Lock | Moderate (−15 to −25 CD per shot) | Ballistas, arc projectors, kinetic lances. Requires line of sight. |
| **3 — Indirect / Ranged** | High-payload arc fire | Included at Certification Lock | Heavy (−30 to −50 CD per use) | Scatter mortars, net launchers. Can arc over terrain. Extreme range shots arrive on the next horn interval. |

### Range and Cost

| Range Bracket | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| **Close** (Harvest-Prong reach) | Base | Base | Base |
| **Near** | Not available | ×1.5 | ×1.5 |
| **Far** | Not available | ×2.5 | ×2.0 |
| **Extreme** | Not available | Not available | ×3.0 + delayed impact |

**Mounting rules:** All weapons and heavy equipment are declared at Certification Lock alongside Craft Draw. They are **always in the Craft Draw calculation** — they affect Drain Rate whether fired or not because they add mass, affect handling, and signal intent. Only firing produces additional CD cost.

### What Combat Cannot Do

- **Kill:** No lethal actions permitted. Crash webbing and emergency dead-switches are mandatory equipment.
- **Steal stored connection:** Gutter contents are locked to the rig they were synced with and bleed to ambient on rig destruction. Another team's umber gutter — the physical component — is useless to a rival crew. Its calibration is specific to the destroyed rig's Craft Draw and cannot transfer.

---

## The Craft: Venture-Rigs

### Mandatory Equipment

| Component | Purpose |
|---|---|
| **Harvest-Prong** | Man-portable sync tool. Must be detachable from mount and operable by a single crew member on foot. |
| **Umber Gutter** | Reversed umber crystal creating the calibrated deficit. Set to the rig's specific Craft Draw at Certification Lock. |
| **HTech Power System** | Rig must operate via Harmony technology to interface with the node network. |

### Certification Lock Standards

| Standard | Requirement |
|---|---|
| **Declared Craft Draw** | All equipment, weapons, and systems included. Fixed at lock — cannot change. |
| **Prong Integrity** | Must survive 3 dry-strikes under inspection. |
| **Umber Gutter Tolerance** | Must pass containment and overheat checks at 120% projected load. |
| **Prong Detachability** | Must demonstrate hand-held operation by a single unassisted crew member. |
| **Launch Coupler** | Aerial rigs: certified Walker-Core anchor points. Ground: gate clearance. |
| **Crew Survival Kit** | Crash webbing, flare dye, emergency dead-switch — mandatory per crew member. |
| **Telemetry Beacon** | Passive location ping for all entrants. Allows marshals to locate and retrieve disabled crews. |

---

## Rules of Engagement

| Rule | Detail |
|---|---|
| **No lethal force** | Everything else is within the rules of the race |
| **No stored connection transfer** | Umber gutter contents are rig-specific. Stealing or repurposing a destroyed rig's gutter is illegal and mechanically impossible — it cannot help the team that takes it |
| **Gutter theft is illegal** | Attempting to remove and use a rival's umber gutter core is grounds for immediate disqualification |
| **Destruction is strategy** | Disabling all other rigs is a legal path to victory — but the aggressor still must overcome their own deficit and reach the Grand Resonator |
| **Harvest-Prong must be certified** | Only Guild-certified Prongs may be used for Spire syncing. Improvised tools will not interface with the node infrastructure. |
| **Contention bonus** | Automatic +10 CU when a rival's crew is within Harvest-Prong reach at the moment of sync completion |
| **No tiebreak** | First team with both LEDs green to strike the Grand Resonator wins. Period. |

---

## Racing Archetypes

### The Soloist
Ultra-light rig. Near-zero Drain Rate. Two or three nodes and both LEDs go green. Zero combat tolerance — a single effective hit and the race is over. Wins by being irrelevant to everyone's threat model until it's too late.

### The Hunter
Heavy rig with Tier 1–2 weapons. Enters the race planning to disable competitors rather than farm nodes first. **Only viable if the hunt is fast** — every pulse spent hunting without syncing is paid in Drain Rate. The correct hunter strategy: eliminate the two or three fastest threats in the first two horn intervals, then pivot immediately to node farming from an uncontested field. Hunters who over-hunt bleed themselves to elimination.

### The Seven-Man Crew
Massive craft with enormous Craft Draw and enormous firepower. Requires mostly Major Nodes to reach LED 2. Has the capacity to dictate terms to any other rig in the basin — but must actually reach and sync nodes before its Drain Rate outpaces its progress. Despite the firepower, often the riskiest strategy in a short race.

### The Couples Racer
Two-person craft. Low Drain Rate. No meaningful combat capacity. Wins on efficiency, terrain knowledge, and routes other rigs can't follow. Pre-race terrain surveys are worth more than weapons to this archetype.

---

## Viewing the Spectacle

### The Scoreboard

Every active rig has a row on the gate scoreboard:

| Display | Meaning |
|---|---|
| 🔴 **LED 1 Red** | Rig is in power deficit — bleeding connection faster than it's recovering |
| 🟢 **LED 1 Green** | Rig running clean under its own power |
| 🔴 **LED 2 Red** | Not yet enough connection to fire the Grand Resonator |
| 🟢 **LED 2 Green** | Discharge eligible — can attempt the Resonator |

No raw CU numbers are shown publicly. Spectators read LEDs, interpret the Compass color and direction, and listen to Scout-Spotters.

### Three Viewing Tiers

**The Gilded Zephyrs (Elite):** Luxury airships with magnifying-glass floors. Altitude rules strictly enforced. The discharge column rises to roughly eye level.

**The Rim-Tracker (Middle Class):** A steam trolley running the basin rim at speed, rushing toward the most actively pulsing Compass arcs. Passengers can hop stations.

**The Bleacher-Walls (The Masses):** Stone amphitheatres built into the rim. Brass binoculars. The loudest section. Scout-Spotters here shout Compass readings to anyone nearby.

---

## Cultural Significance

The Circuit-Run re-enacts the **Great Stitching** — Harmony's historical expansion into new territory, the exploranauts who struck nodes in unknown land and brought that connection back to the Republic's centre. Every race is a miniature iteration of that founding act.

Each Spire in the race is built by the city it represents — a physical contribution from every level of the Harmony hierarchy to the shared spectacle. The node layout is one of the few places in civic life where Frontier settlements stand beside Major city infrastructure as equals. A Trail-Tail Trench node is worth fewer CU than a Gilded Chime Spire — but it's in the race.

The **absent arcs** — Ash-Blood and, in some years, Frontier nodes pending submission — are visible to everyone. Their darkness is a public record of what's unresolved.

---

## Notable Rules Clarifications

### Boon Expiry
Boons last until the holder's next sync. One active boon per rig. New sync immediately replaces the current boon. Boons cannot stack.

### Grand Resonator Approach Angles
Any unobstructed angle is legal — including from above. The Harvest-Prong must contact the pylon at any point along its structure. Aerial descent is explicitly permitted.

### Disabled Rig Protocol
- All accumulated stored connection bleeds to ambient on disablement — the umber gutter empties
- The rig's physical components (including the gutter) may not be retrieved by another team for race use — gutter theft is an illegal action regardless of intent
- The disabled crew is retrieved by marshals under the telemetry beacon protocol
- A disabled rig is out of contention and cannot be repaired or re-entered

### Organic Drive Ruling
An organic component (gryphon, trained animal) operates outside the umber gutter's dead zone — it runs on ambient metabolism. The gutter is calibrated to impose artificial drag equal to the organic component's rated contribution. If the gutter is damaged mid-race:

- *Minor:* −10 CD reduction benefit
- *Moderate:* −15 CD reduction
- *Severe:* −20 CD reduction + heat-stress; must sync a Moderate or Major node before the next horn or face forced withdrawal

This is a mechanical failure, not a strategy.

### Pre-Race Alliances *(Optional)*
Teams may declare a Pre-Race Alliance at Certification Lock. Allied teams may share sync intelligence. If an allied team fires the Grand Resonator, their partner receives Secondary Credit placement immediately after them in official standings. Alliances are public record. Allied teams may not deliberately ram or disable each other.

---

## Related Pages

- [[circuit-run-simulation|The First Vumbua Circuit-Run — Full Simulation]]
- [[The Power System]]
- [[professor-kante|Professor Kante]]
- [[Vumbua Academy]]
- [[walker-core|The Walker-Core]]
