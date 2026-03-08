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

The **Circuit-Run** (colloquially: **Reso Race**) is the most popular sport in Harmony. It is a brutal combination of exploration race, engineering competition, and religious simulation of the "Great Stitching" — the ancient conquest that unified Harmony's territory.

---

## Core Concept

Teams or soloists pilot custom craft (**Venture-Rigs**) through a wilderness arena, racing to **strike Spires** (simulated nodes) and siphon their energy. Once a team has accumulated enough resonance to overcome their craft's connection deficit *and* the race's Global Amplitude, they may reach the **Grand Resonator** at the arena's centre and discharge everything. The first team to light the Grand Resonator wins.

The genius of the format: **bigger, more powerful ships need MORE energy**. A sailboat crew might only need a few minor nodes. A dreadnought crew needs dozens. This creates natural strategic tension between speed, firepower, and efficiency.

There is more than one path to victory. A team that cannot outrun rivals can endeavour to *eliminate* them — disabling the field and then completing the race on their own terms. Aggression is a legitimate strategy; it simply has a cost.

---

## The Arena: The Apex Ring

The Circuit-Run takes place in a massive natural geographic basin called the **Apex Ring**.

| | |
|---|---|
| **Shape** | Horseshoe — open on the south face |
| **Size** | ~1 mile across |
| **Terrain** | Static wilderness — canyons, petrified forests, dry sea-beds, open water |
| **Layout** | Consistent across all Harmony venues, updated periodically to reflect newly integrated territory |
| **Grand Resonator** | Towering obsidian pylon at the exact centre — the finish line |
| **Rim** | Circular stone wall with the Apex Compass inset along the inner face; tram stops at key viewing positions |

### The Southern Gate — Mixed Start Line

The horseshoe's open mouth is the **Southern Gate** — the race's start line. It is divided down the middle:

- **West half: Land approach** — canyon floor, stone gradient, wide enough for heavy rigs side by side
- **East half: Water approach** — shallow estuary mudflat that deepens into an open-water channel at the basin interior; navigable by boats, hulls, and amphibious rigs

All ground and water rigs line up at the Southern Gate. At the opening horn, they charge through simultaneously — no weight-class ordering for the ground entry.

### The Drop — Aerial Launch

A separate start is reserved for **aerial and slung light rigs**. [[Vumbua Academy]]'s [[walker-core|Walker-Core]] parks two legs on the southern rim during race day, its elevated frame serving as the official **drop gantry**. Aerial rigs (gryphon-equipped, airship-rigged, or slung) are launched from the Walker-Core's upper arm in weight-class order, lightest first, timed to coincide with the ground entry horn.

The Drop is dramatic and specific — it is not how most rigs enter. Gryphon rigs bank immediately on release. Slung light rigs are fired at calculated angles. Heavy aerial rigs drop controlled.

> **Design note:** The Walker-Core gantry is present at every Vumbua-hosted race. Other venues use fixed launch towers or cliff-edge slings.

### This Year's Special Layout

The arena layout is being **updated for the first time** to include the **Ash-Blood Isles** and the **Mizizi Forest island**. This is a huge deal — the entire population is seeing simulated versions of the newest territories for the first time.

> **GM Note:** Part of the Reso Race's purpose is to **teach Harmony's people about newly integrated land** — what it looks like, what resources it produces, what it brings to the Republic. The race is propaganda as much as sport.

### The Controversy: Missing Ash-Blood Node

The Spire locations are determined by [[scrivener-guild|Scrivener Guild]] calculations based on known node resonance values. **However, the Ash-Blood node data has not been released.** Despite the terrain reflecting the Ash-Blood Isles, there is no Ash-Blood Spire in the arena. The [[Trail-Tail Trench]] (Trench-Kin frontier territory) is similarly absent — its amplitude data is also unsubmitted.

Both absences are visible on the Apex Compass: two arcs on the north-northeast and east-southeast that never light up across the full race.

---

## The Energy System: Stored Connection

The Circuit-Run's mechanics are built on the same technology as [[The Power System|Vox Crystal Batteries]], but used in reverse.

### How It Works

1. **Umber crystals** normally store a **connection to the land** — allowing devices to operate away from nodes (see [[The Power System#Innovation 2 Stored Connection]])
2. In a Circuit-Run, umber crystals are used **backwards** — they **sever** the craft's natural connection to the ambient ether field
3. This creates an artificial "dead zone" around the Rig — it operates at **degraded power** until the crew reconnects
4. The crew must **manually reopen** that connection by striking Spires and siphoning node energy
5. The amount of reconnection needed depends on the craft's power draw

### The Two-Stage Win Condition

A team's progress is tracked through two thresholds, displayed on the Apex Ring's twin-LED scoreboard:

**LED 1 — Rig Power:**
- 🔴 Red: `Stored Connection < Craft Draw + Launch Penalty` — the rig is operating in deficit; its own systems are consuming more than they've recouped
- 🟢 Green: `Stored Connection ≥ Craft Draw + Launch Penalty` — the rig is running clean under its own power; no longer bleeding against itself

**LED 2 — Resonator Eligible:**
- 🔴 Red: `Stored Connection < Craft Draw + Launch Penalty + Global Amplitude` — not yet enough to activate the Grand Resonator
- 🟢 Green: `Stored Connection ≥ Craft Draw + Launch Penalty + Global Amplitude` — ready to discharge

**LED 2 cannot go green before LED 1.** Because the Global Amplitude is always a positive value added on top of LED 1's threshold, the two LEDs light up sequentially. A team will always pass through "LED 1 green, LED 2 red" before reaching full readiness. Both can go back to red if cascade drain reduces their stored connection.

A team may only attempt a Grand Resonator discharge when **both LEDs show green**.

### Connection Deficit (CD) Formula

`CD = Global Amplitude + Craft Draw + Launch Penalty − Stored Connection`

- Teams begin the race with a positive CD (they are in deficit)
- Every successful Spire sync lowers CD
- LED 1 goes green when CD drops below zero by at least the Global Amplitude amount
- LED 2 (discharge eligible) occurs when CD ≤ 0
- **Launch Penalty** is a fixed opening handicap set by rig class

### Cascade Drain — The Ongoing Cost

**Rigs continuously consume connection just by operating.** A vehicle in motion, with systems running, is always drawing from its stored reserves.

Each rig has a **Drain Rate** equal to its Craft Draw ÷ 10 (round up). This amount is added to the rig's CD at the end of each Loom-Pulse segment in which the rig did **not** successfully sync a node. Mounted weapons and heavy melee equipment (battering rams, spiked wheels, speed boosters) increase the Craft Draw calculation used for Drain Rate — they are always in the math regardless of whether they are used.

| Craft Type | Example Craft Draw | Drain Rate / Pulse |
|---|---|---|
| Ultra-light solo | 10 | +1 CD |
| Racing sailboat | 20 | +2 CD |
| Speed ketch | 55 | +6 CD |
| Heavy rig | 110 | +11 CD |
| Super-heavy / land-ship | 190 | +19 CD |

**Implication:** A heavy rig that parks at the Grand Resonator approach lane to block is bleeding deficit while it sits. Blocking is a viable tactic — but it has a cost. Aggressive teams must hunt efficiently and then pivot to syncing, not hold position indefinitely.

> **Spectator read:** As a rig's connection reserves run low without syncing, its systems begin to dim — lights darken, the hull hum drops in pitch. A crew running on borrowed time *looks* like it. When LED 1 flips back to red mid-race, the crowd notices.

---

## Official Match Flow (Academy Format)

| Phase | What Happens | Strategic Meaning |
|---|---|---|
| **1. Certification Lock (T-24h to T-0)** | Officials lock each rig's declared Craft Draw, Launch Class, and safety seals. | Teams must choose speed vs armor vs weapons before the race starts. |
| **2. The Drop / Southern Rush (Opening Horn)** | Aerial rigs drop from the Walker-Core gantry; ground and water rigs charge through the Southern Gate simultaneously. | Positioning and first-contact route matter more than top speed. |
| **3. First Sync Window — Random Band** | Initial spires emerge in **randomised positions** across the basin. No team knows exact spawn locations in advance. | Forces real-time adaptation. Teams that over-prepared a fixed route suffer; teams that read the Apex Compass well thrive. |
| **4. Loom-Pulse Rotations — Reactive Spawning** | Additional spires emerge in timed pulses. New spawns skew toward the least-contested terrain band. Cascade drain is ongoing throughout. | Less random as the race progresses. Teams with positional discipline benefit; reactive spawning gives slower teams a path back in. |
| **5. Untouched Multiplier** | Any spire that has not been synced since its last emergence gains **+5 CU per Loom-Pulse** it goes untouched. Visible on the Apex Compass as increasing brightness. | Rewards teams willing to explore far terrain; punishes field-collapse where everyone farms the same nodes. |
| **6. The Convergence Horn** | Fires when the **first team reaches both LEDs green** (discharge eligible). All remaining viable teams have **2 Loom-Pulse windows** from this moment to attempt the Resonator or be eliminated from contention. | Creates a fixed endgame clock. No rig can loop indefinitely. |
| **7. Resonator Attempt** | Any team with both LEDs green may strike the centre pylon at any time. | Race can end suddenly. Teams must balance "being ready" vs "making it there." |
| **8. Tiebreak (if needed)** | If two teams discharge in the same horn-window: highest remaining stored connection wins; if still tied, fastest verified basin time wins. | Rewards efficient routing, not just brute force. |

---

## Combat and Weapons

All combat draws from the same connection pool as the win condition. Fighting is always a trade-off.

### Weapon Tiers

| Tier | Type | Craft Draw Impact | CD Cost at Use | Range Cost | Examples |
|---|---|---|---|---|---|
| **0 — Manual / Body** | No vehicle amplification | None (not in Craft Draw) | Free | None | Boarding, grappling, hand weapons wielded by crew |
| **1 — Vehicle-Assisted** | Passive systems powered by the rig | Included in Craft Draw | Minor (−5 CD per activation) | None — Close range only | Rams, ballistic bumpers, spiked wheels, magnetic grapples, speed boosters |
| **2 — Direct Fire** | Requires armed weapon system | Included in Craft Draw | Moderate (−15 to −25 CD per shot) | +50% cost per range bracket beyond Close | Ballistas, arc projectors, kinetic lances |
| **3 — Ranged / Indirect** | High payload, indirect trajectory | Included in Craft Draw | Heavy (−30 to −50 CD per use) | See below | Scatter mortars, net launchers, tethered charges |

### Range Brackets and Costs

| Range | Tier 2 Cost Modifier | Tier 3 Cost Modifier |
|---|---|---|
| Close | ×1.0 (base) | ×1.0 (base) |
| Near | ×1.5 | ×1.5 |
| Far | ×2.5 | ×2.0 |
| Extreme (mortar only) | Not available | ×3.0 + 1 pulse delay |

**Line-of-sight weapons** (Tier 2) require clear sightline — no walls, terrain, or intervening rigs. Cheaper per shot than indirect fire.

**Indirect/barrage weapons** (Tier 3) can arc over terrain and rigs. They cost more per shot due to payload energy, and at Extreme range they arrive on the **next sync window** rather than immediately — useful for area denial, not instant combat.

### Mounting Rules

- All weapons and heavy melee equipment are declared at **Certification Lock** alongside Craft Draw
- Mounted/installed equipment is **always included in the Craft Draw calculation**, whether used or not — it costs weight, affects handling, and signals intent to rivals
- Firing is the only additional CD cost; draw and ready actions are free
- A weapon that runs out of stored connection to power it is inert — it cannot fire but remains mounted

---

## The Craft: Venture-Rigs

Teams or soloists bring their own mechanical crafts. There are no restrictions on size or crew count, but every craft must follow these rules:

### Mandatory Equipment

| Component | Purpose |
|---|---|
| **Harvest-Prong** | A copper-and-crystal rod that physically strikes a Spire to siphon energy. Every rig must have one. |
| **Umber Gutter** | The reversed umber crystal creating the artificial dead zone. Calibrated to the craft's rated power. |
| **HTech Power System** | The craft must be powered by Harmony technology to store connection. |

### Build & Launch Standards

| Standard | Requirement |
|---|---|
| **Declared Craft Draw** | Each rig must publish rated draw including all weapons and equipment. |
| **Prong Integrity** | Harvest-Prong must survive 3 dry-strikes during inspection. |
| **Umber Gutter Tolerance** | Must pass overheat and containment checks at 120% projected load. |
| **Launch Coupler Spec** | Aerial rigs: approved Walker-Core anchor points. Ground rigs: gate clearance check. |
| **Crew Survival Kit** | Crash webbing, flare dye, emergency dead-switch — mandatory. |
| **Telemetry Beacon** | Passive location ping for all entrants. Lets marshals monitor and retrieve disabled crews. |

---

## The Spires (Nodes)

During the race's **Loom-Pulse** intervals, massive metallic pillars erupt from the ground across the basin. Each is constructed and maintained by the city whose node it simulates — they share the same mechanical skeleton but carry their city's aesthetic unmistakably.

### Spire Rules

**Spawn behaviour:**
- **First wave (opening):** Fully randomised — positions are not known in advance to any team. The Apex Compass is the only signal.
- **Subsequent waves:** Reactive — new spires skew toward the terrain band with the fewest active rigs. Less random, more structural as the race progresses.
- **Limited charges:** Each Spire has a finite number of syncs. Once depleted, it retracts into the floor. A new spire spawns in the least-contested area immediately after.
- **Untouched multiplier:** Any active spire that has not been synced gains **+5 CU per Loom-Pulse** it remains standing. Visible as increasing brightness on the Apex Compass.

**Syncing a Spire:**

| Step | Action |
|---|---|
| **1. Tune** | The pilot matches the Rig's frequency to the Spire's vibration |
| **2. Strike** | The Rig physically touches the Spire with the Harvest-Prong |
| **3. Consume** | The connection energy is absorbed into the Rig's umber gutter |

**Node Activation and Anti-Camping:**
When a rig enters Close range of an active Spire, the node **activates**:
- Its crystal crown brightens visibly
- The corresponding Apex Compass arc begins **pulsing** instead of holding steady
- The rig has until the **next Loom-Pulse horn** to complete the sync

If the horn fires before the sync completes: the activation resets. The rig may try again next interval — but pays another full pulse of Drain Rate for the delay. The Untouched multiplier does **not** accumulate during an active (pulsing) window — the node "knows" it is being contested and withholds the bonus until the sync is resolved or the window resets.

**Contention Bonus:**
When two or more rigs are within **Harvest-Prong reach** of the same Spire at the moment one team's sync completes, that sync earns **+10 CU bonus**. "Within range" is determined at the moment the sync finalises — not when the approach began. Contention is checked automatically; no declaration is required.

> *A team that cannot close deficit in time may still choose to approach a contested node — doing so denies their rival the bonus even if they cannot complete the sync themselves. This is a legitimate tactical sacrifice.*

### The Apex Compass

A physical fixture running the full circumference of the Apex Ring's inner rim wall. A ring of **16 directional indicators** — one per 22.5° arc — each corresponding to a sector of the basin floor.

| Signal | Meaning |
|---|---|
| **Dark** | No active spire in this arc |
| **Dim glow** | Active spire at Far range in this arc |
| **Steady glow** | Active spire at Near or Close range |
| **Bright glow** | Spire has accumulated untouched multiplier bonus — higher value than base |
| **Pulsing** | A rig is within Harvest-Prong reach — activation window is open |
| **Color** | Node type, drawn from the city's visual identity (see Spire Visual Design) |

**Multiple nodes in the same arc:** The indicator shows both simultaneously. The node physically closest to the rim appears on the **left/clockwise edge** of the arc segment; the furthest appears on the **right/counter-clockwise edge**. Spectators and pilots reading the compass can distinguish between a close and distant node in the same sector without exact coordinates.

**Absent arcs:** The Ash-Blood Isles arc (north-northeast) and Trail-Tail Trench arc (east-southeast) never illuminate across the full race. Two dead segments in a circle of active ones.

### Spire Visual Design

Each Spire shares a common mechanical skeleton — tall pillar, Harvest-Prong terminal at the apex, charge counter embedded in the column face — but is built to the aesthetic of the city whose node it represents:

| Origin City | Resource | CU | Compass Colour | Visual Identity |
|---|---|---:|---|---|
| [[gilded\|Gilded]] | Chime Spire | 80 | **Gold** | Organ-pipe columns, layered brass. Actual musical tones ring when activated. Elaborate and unmissable. |
| [[umbra-mountain\|Umbra Mountain]] | Umber Crystal | 70 | **Deep violet** | Faceted obsidian. Glows from within. Cold to touch. Looks like it's already powered. |
| [[juxta\|Juxta]] | Lift Stone | 40 | **Blue-grey** | Monolithic smooth granite. Orbiting rock fragments around the apex. You feel the upward air current before you see it. |
| [[feltland\|Feltland]] | Live Soil | 35 | **Earth brown** | Organic casing — vines at the base, warm, slightly alive-feeling. The only spire that smells like something. |
| [[relina\|Relina]] | Soft Forge | 45 | **Bronze-amber** | Surface shimmers like slow liquid metal. Warm to touch. Slightly unsettling. |
| [[timon\|Timon]] | Focus Glass | 35 | **Clear/prismatic** | Giant lens architecture. Refracts light in unusual angles — creates optical oddities nearby. |
| [[settika\|Settika]] | Prism Falls | 30 | **Rainbow facet** | Multi-surface crystal. Looking through it reveals things differently. |
| [[shepta\|Shepta]] | Whetstone | 30 | **Dark charcoal** | Extremely sharp geometric facets. Sparks visibly when a Harvest-Prong strikes it. |
| [[lenoa\|Lenoa]] | Friction Needles | 30 | **Silver** | Multiple thin parallel needles instead of one column. Frictionless surface — deliberately hard to grab. |
| [[octo\|Octo]] | Speaking Stone | 25 | **Pale grey** | Rounded, smooth, covered in inscribed text. Hums at low frequency. |
| [[prima\|Prima]] | Dew Crystal | 25 | **Ice blue** | Condensation runs down it constantly. Small puddle always at its base. |
| [[minnow\|Minnow]] | Living Scent Wood | 20 | **Warm amber** | Organic wood structure rather than metal or crystal. Faintly fragrant. |
| [[bloomfield\|Bloomfield]] | Clockwork Blooms | 20 | **Copper** | Mechanical flowers that open and close rhythmically. Ticking sound audible up close. |
| [[nstyl\|Nstyl]] | Silent Silt | 20 | **Matte grey-brown** | Almost invisible in low light. Produces no sound when struck — the only silent sync in the field. |
| [[bay-of-breath\|Bay of Breath]] | Breathable Algae | 20 | **Bioluminescent green** | Produces bubbles and light mist at the base. Faintly biological smell. |
| [[elysium\|Elysium]] | Snow Sand | 15 | **White-gold** | Slight shimmer, warm despite appearance. Mild optical distortion in a small radius — approaching crews report brief disorientation. |

> **Absent / Dark:** [[ash-blood-isles\|Ash-Blood Isles]] and [[trail-tail-trench\|Trail-Tail Trench]] have no Spires. Their Apex Compass arcs are permanently unlit.

### Basin Placement by Terrain Band

| Terrain Band | Typical Nodes Spawned | Tuning Intent |
|---|---|---|
| **South Launch Canyons** | Friction Needles, Whetstone, Live Soil | Early choices from the random opening wave; prevent opening pileups |
| **West Petrified Forest (Mizizi simulation)** | Soft Forge, Living Scent Wood, Clockwork Blooms | Technical pathing and endurance routes |
| **North Open Flats (Ash-Blood terrain)** | Lift Stone, Umber, Chime (final pulse only) | High-risk high-reward; heavily penalises isolation via Drain |
| **East Wet Shelf / Dry Sea-Bed** | Dew Crystal, Breathable Algae, Prism Falls | Utility route for disciplined teams |
| **Mid-Basin** | Speaking Stone, Silent Silt, Snow Sand, Focus Glass | Late-appearing coordination and stealth options |
| **Ash-Blood terrain slice** | None — terrain only | Narrative pressure and public controversy |

### Charges Per Tier

| Node Tier | Charges | Notes |
|---|---|---|
| **Major** (Chime, Umber, Lift Stone) | 3 | High value; multiple teams should access |
| **Moderate** (Live Soil, Soft Forge, Focus Glass, etc.) | 2 | Standard competition |
| **Minor** (Trail Mark, Breathable Algae, Snow Sand, etc.) | 1 | Reward for exploration |

### If Race Flow Feels Off: Fast Tuning Levers

1. **Too much brawling early:** Shift one high-CU north-flat spawn into the east utility band.
2. **Heavy rigs auto-win:** Raise Drain Rate for super-heavy classes by +50% for 1 pulse after each combat action.
3. **Soloists evade indefinitely:** Shorten Mute Wake / Mirage Wake duration by one pulse.
4. **No one explores full basin:** Delay first Chime spawn until after second Loom-Pulse. *(Default in standard format.)*
5. **Untouched multiplier over-rewards camping:** Cap the multiplier at +15 CU above base value per node.
6. **Reactive spawns too predictable:** Add one fully random spawn per Loom-Pulse 2+ in addition to the reactive spawn.
7. **Convergence Horn fires too early:** Raise Global Amplitude by 10 for the next race.

---

## Rules of Engagement

| Rule | Detail |
|---|---|
| **No killing** | Everything else is fair game inside the basin |
| **No stealing connection energy** | Once absorbed, connection is locked to that rig's umber gutter |
| **Destruction is strategy** | Disabling all other rigs is a legitimate path to victory — but an aggro team must still overcome its own deficit and reach the Grand Resonator |
| **Battery ownership doesn't matter** | If you can get your hands on a charged battery and bring it to the Grand Resonator, that counts |
| **Contention Bonus** | Any sync completed while a rival rig is within Harvest-Prong reach earns +10 CU bonus |
| **Convergence Horn** | When the first rig reaches discharge eligibility (both LEDs green), the Horn fires. All remaining teams have 2 Loom-Pulse windows to attempt the Resonator or face elimination |
| **Node Activation Window** | When a rig enters Harvest-Prong range of a node, the node activates. The rig must sync before the next horn or the activation resets. |

---

## Viewing the Spectacle: The Three Tiers

### The Scoreboard and Apex Compass

Every active rig has a row on the gate scoreboard:

| Indicator | Meaning |
|---|---|
| 🔴 **LED 1 Red** | Rig is in power deficit — bleeding connection just to operate |
| 🟢 **LED 1 Green** | Rig is running clean under its own power |
| 🔴 **LED 2 Red** | Not yet enough connection to fire the Grand Resonator |
| 🟢 **LED 2 Green** | Discharge eligible — can attempt the Resonator now |

LED 2 cannot go green before LED 1 — the discharge threshold is always higher than the operational threshold. Both can revert to red if cascade drain reduces stored connection.

The **Apex Compass** rings the inner basin wall — 16 arcs, each glowing, pulsing, or dark based on active node positions. Color indicates origin city; brightness indicates value; pulsing indicates a rig is within range of the node in that arc. When a node depletes, its arc goes dark. A new glow appears elsewhere as the reactive spawn emerges.

No raw numbers are displayed publicly. Spectators read the LEDs, the compass, and the Scout-Spotter shouts.

### 1. The Gilded Zephyrs (Elite)
Luxury airships with **Magnifying Glass Floors** above the basin. Strict altitude rules; limited ships. The discharge column hits at roughly eye level on approach.

### 2. The Rim-Tracker (Middle Class)
A high-speed steam trolley that runs the basin rim, rushing toward the most actively pulsing Compass arcs to follow action. Passengers can hop stations.

### 3. The Bleacher-Walls (The Masses)
Stone amphitheaters built into the basin lip. Fans use brass binoculars. The most raucous viewing. Scout-Spotters here shout compass readings and arc updates to anyone who'll listen.

---

## Notable Racing Archetypes

### The Soloist ("Stinger")
Ultra-light cycle. Near-zero Drain Rate. Minimum LED 1 threshold. One or two nodes and both LEDs go green — but zero combat tolerance. One hit from a heavy rig and the race is over.

### The Seven-Man Crew ("Goliath")
Massive land-ship. Enormous Craft Draw, enormous Drain Rate. Requires mostly Major Nodes to reach discharge eligibility. Has the firepower to dictate terms to any other rig in the basin — but has to actually reach the nodes before the Drain Rate costs more than the sync earns.

### The Couples Racer ("Dancer")
Two-person sailboat. Lowest Drain Rate in the field. No combat capability worth mentioning — but can phase through terrain other rigs can't follow. If terrain surveys are done right, a fracture in the right canyon wall is more valuable than a ballista.

### The Hunter ("Marble Wall")
Heavy rig with Tier 1–2 weapons and aggro crew. Bypasses early node farming to disable competitors, then pivots to syncing from an uncontested field. Only works if the hunting phase is *fast* — cascade drain punishes any hunter that stalks slowly. Disable the right targets first, then farm.

---

## The First Vumbua Circuit-Run

> This year's race features the updated terrain with the Ash-Blood Isles and Mizizi Forest for the first time.

### Confirmed Teams

| # | Team | Craft | Strategy | Notes |
|---|---|---|---|---|
| 1 | **Shatter Stamper** | Heavy rig, 3-person crew | Brute force node farming | — |
| 2 | **Sail & Stun** | Fast sailing ketch | Speed + disruption + intel | Loosely allied with Pudge's circle |
| 3 | **Marble Wall** | Dominant heavy body | Hunt and clear, then farm | Requires fast early kills to beat cascade drain |
| 4 | **[[Pudge]]** | Gryphon-hybrid | North run + aerial descent | Gryphon heavily calibrated; umber gutter oversized |
| 5 | **Dancer & Fabian** | Racing sailboat (2-person) | Agility, terrain, precision routing | Lowest power draw in the field |

> **Full race simulation:** See [[circuit-run-simulation|The First Vumbua Circuit-Run — Full Simulation]]

---

## Rule Clarifications & Refinements

### 1. Boon Expiry

**Boons last until the *holder's* next sync.** One active boon per rig at all times. Receiving a new sync replaces the current boon immediately, even if unexpired. Boons cannot stack.

---

### 2. Grand Resonator — Approach Angles

A legal discharge may be executed from **any unobstructed angle, including from above**. The Harvest-Prong must physically contact the pylon at any point along its structure (base, column, or crown). The rulebook does not prohibit aerial approach.

---

### 3. Disabled Rig Protocol

- All accumulated CU is forfeit — stored connection bleeds back into the ambient field
- The disabled rig's physical **battery** may be retrieved and carried to the Resonator by another team — only the battery's base charge, not accumulated CU from spire syncs
- A disabled rig is out of contention and cannot be repaired during the race

---

### 4. Gryphon / Organic Drive Ruling

The organic component (gryphon, trained animal) sits outside the umber gutter's dead zone — it operates on ambient metabolism. The gutter is calibrated to impose artificial drag equal to the organic component's contribution. If the gutter is damaged mid-race:

- *Minor damage:* −10 CD spike reduction
- *Moderate damage:* −15 CD reduction
- *Severe damage:* −20 CD reduction + heat-stress warning; must sync a Moderate or Major node before the next Loom-Pulse or face forced withdrawal

This is a mechanical failure, not a strategy.

---

### 5. Pre-Race Alliances (Optional Rule)

Teams may declare a **Pre-Race Alliance** at Certification Lock:
- Both teams log the alliance with the Race Marshal
- Allied teams may legally share Relay Ping boon data
- Allied teams may not deliberately ram or disable each other
- If an allied team fires the Grand Resonator, their partner receives a **Secondary Credit** placement immediately after them in official standings
- Alliances are public record

---

## Cultural Significance

The Circuit-Run is a **simulation of the Great Stitching** — the historical conquest that unified Harmony's territory. Every race is a miniature version of the original exploranauts who ventured into unknown land, struck nodes, and brought connection back to the centre.

For students at [[Vumbua Academy]], the Reso Race is:
- A chance to **impress the Captains** ahead of internship interviews
- A practical demonstration of [[The Power System|node science]] and the connection/energy distinction
- A window into what life on a **venture journey** will actually look like

---

## Related Pages

- [[circuit-run-simulation|The First Vumbua Circuit-Run — Full Simulation]]
- [[The Power System]]
- [[professor-kante|Professor Kante]]
- [[House Gilded]]
- [[Vumbua Academy]]
- [[harmony-nodes]]
