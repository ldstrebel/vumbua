import base64
import os

BASE_DIR = r'd:\Code\vumbua\meta\foundry-exports'
MAPS_DIR = os.path.join(BASE_DIR, 'maps')
TOKENS_DIR = os.path.join(BASE_DIR, 'tokens')
OUT_JS_1 = os.path.join(BASE_DIR, 's10_session_macro.js')
OUT_JS_2 = r'd:\Code\vumbua\sessions\planning\s10\s10_session_macro.js'

def get_b64(folder, filename):
    path = os.path.join(folder, filename)
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode('ascii')

map_walker = get_b64(MAPS_DIR, 'map_walker_core_breach.png')
map_wetland = get_b64(MAPS_DIR, 'map_petrified_wetland.png')
map_pine_forest = get_b64(MAPS_DIR, 'map_nordic_pine_forest.png')
map_camp = get_b64(MAPS_DIR, 'map_fortified_camp.png')

token_chui = get_b64(TOKENS_DIR, 'token_mwaza_chui.png')
token_wyrm = get_b64(TOKENS_DIR, 'token_gale_wyrm.png')
token_cat = get_b64(TOKENS_DIR, 'token_canopy_cat.png')
token_shark = get_b64(TOKENS_DIR, 'token_dagger_shark.png')
token_bramble = get_b64(TOKENS_DIR, 'token_bramble.png')
token_rill = get_b64(TOKENS_DIR, 'token_rill.png')

js_template = f"""/**
 * Vumbua Session 10 — Standalone Foundry VTT Master Codex & Daggerheart NPC Setup Macro
 * System Compatibility: Daggerheart (1.6.1+) & Foundry VTT v10/v11/v12
 * 
 * INCLUDES:
 * - Daggerheart Features Tab: Native Item document features populated for all 6 Actors!
 * - Daggerheart Effects Tab: Native ActiveEffect documents wired into every Actor!
 * - Daggerheart Notes Tab: "Monsters Know What They're Doing" Tactical AI Guides EMBEDDED DIRECTLY inside each Actor's Character Sheet Biography!
 * - 8 Detailed Scene-by-Scene DM Journal Pages (Establishing Shots, Beast Descriptions, Exact Counts, Combat Moments, Tactics).
 * - Unique Token Art for Stunted Canopy Cat (Distinct from Memory Jaguar).
 * - Rill (The River-Born / Futurist) as First-Responder & Combat Aide.
 * - Professor Ink's Scrivener Guild Recruitment Pitch & Mission Goals.
 * - Nordic Pine Forest Aesthetic (Tall evergreen pines, mossy granite, timber longhouses, zero stone ruins).
 * - Interactive Scene Note Pins mapped to specific Scene DM Guide Pages.
 * - Pinpoint Dynamic Lighting & Transparent Top-Down Base64 Tokens.
 */

(async () => {{
    ui.notifications.info("Vumbua Session 10: Wiring Features, Active Effects, Notes & Battle Maps into Daggerheart...");

    const MAP_WALKER = "{map_walker}";
    const MAP_WETLAND = "{map_wetland}";
    const MAP_PINE = "{map_pine_forest}";
    const MAP_CAMP = "{map_camp}";

    const TOKEN_CHUI = "{token_chui}";
    const TOKEN_WYRM = "{token_wyrm}";
    const TOKEN_CAT = "{token_cat}";
    const TOKEN_SHARK = "{token_shark}";
    const TOKEN_BRAMBLE = "{token_bramble}";
    const TOKEN_RILL = "{token_rill}";

    // ── 1. Create Dedicated Journal Folder & Multi-Page Master Codex ─────────────
    let journalFolder = game.folders.find(f => f.name === "Session 10 - Beast Breach" && f.type === "JournalEntry");
    if (!journalFolder) {{
        journalFolder = await Folder.create({{ name: "Session 10 - Beast Breach", type: "JournalEntry" }});
    }}

    // Page 1: Narrative Arc & Nordic Forest Lore
    const p1_content = `
        <h2>🌲 Session 10 Master Narrative Arc & Nordic Worldbuilding</h2>
        <p><strong>Theme:</strong> Survival, Preparation, and Uncovering Buried History.</p>
        <p><strong>Environment Aesthetic:</strong> The Mizizi Forest is a dense, misty <em>Nordic Pine Forest</em> with towering evergreen canopies, damp pine needle floors, and moss-covered granite boulders. There are <strong>no ancient stone ruins</strong>—early Mizizi architecture consisted of heavy wooden longhouses, timber palisades, and carved pine posts that weather over time into natural forest soil.</p>
        
        <hr/>

        <h3>⚡ Rill's Arrival & Professor Ink's Recruitment Pitch</h3>
        <p><strong>Rill (The River-Born / Futurist)</strong> reaches Squad 907 first in the Nordic Pine Forest! She was already performing field research on "Weeping Nodes" in the area for <strong>Professor Ink</strong> (Scrivener Guild Captain & Fungal Biology Specialist).</p>
        <ul>
          <li><strong>Professor Ink's Motive:</strong> Ink is planning a high-stakes expedition into the deep Mizizi Forest to unlock "tree memories" stored in petrified pine bark. He wants to recruit talented cadets—specifically <strong>Britt, Aggie, and Iggy</strong>—into the Scrivener Guild.</li>
          <li><strong>Rill's Role:</strong> Rill acts as Squad 907's primary combat aide during the beast breach, using her experimental <em>Wadi Flow Tech</em> to disrupt Mwaza-Chui's signal lock while pitching Ink's offer between waves.</li>
        </ul>

        <hr/>

        <h3>📜 Three-Act Session Structure</h3>
        <ol>
          <li><strong>Act 1: Walker Core Collapse (Zone 0 & 8)</strong>
            <ul>
              <li>Resonator Coils short out from a global resonance drop. Barrier collapses. Emergency teleport beacons fail.</li>
              <li>Rill intercepts Squad 907 at the Zone 0 perimeter, guiding them away from high-voltage arc zones.</li>
            </ul>
          </li>
          <li><strong>Act 2: Nordic Pine Rescue Mission (Zone 1 & 3)</strong>
            <ul>
              <li>Party & Rill respond to Squad 06's distress signal near petrified pine stumps and bioluminescent mud pools.</li>
              <li>Gale-Wyrm drops petrified boulders pinning Bramble and Dr. Rose Halloway. Rill provides cover fire with her Reed-Runner pulse rifle.</li>
            </ul>
          </li>
          <li><strong>Act 3: Siege of Fortified Canyon Camp (Zone 5)</strong>
            <ul>
              <li>Party fortifies a wooden longhouse cliff camp using Session 9 scrap loot (tar moats, bungee tripwires, lead nets).</li>
              <li><strong>Mwaza-Chui (Memory Jaguar Boss)</strong> strikes, locking onto Britt & Aggie's mind-link frequency. Rill deploys her Aether Signal Jammer to level the field!</li>
            </ul>
          </li>
        </ol>

        <hr/>

        <h3>🌀 Potential DM Story Twists</h3>
        <ul>
          <li><strong>Twist 1 (Aether Frequency Signal Lock):</strong> Mwaza-Chui targets Britt and Aggie because their telepathic mind-link emits a portable mini-node frequency identical to the ancient buried Mizizi node. Rill's Jammer gives PCs 2 rounds of stealth.</li>
          <li><strong>Twist 2 (Stunted Cat Ambush):</strong> Stunted Canopy Cats use the pine canopy to flank players while they focus on clearing pinned boulders.</li>
          <li><strong>Twist 3 (Resonance Shift):</strong> Mid-combat, a second global resonance drop causes local gravity in Zone 1 to invert, causing floating boulders to drift horizontally.</li>
        </ul>
    `;

    // Page 2: Adversary Stat Blocks & Tactical Flowchart
    const p2_content = `
        <h2>🐆 Adversary Stat Blocks & Deadly Level 3 Balance</h2>
        <p><em>Balanced as <strong>Deadly encounters</strong> for a party of 3–4 Level 3 Cadets (Britt, Aggie, Iggy, + Loami). Incorporates Daggerheart Tier 1/2 Mechanics & Biome Hazards.</em></p>
        
        <hr/>

        <h3>🐆 Mwaza-Chui (Memory Jaguar — Tier 2 Solo Boss)</h3>
        <ul>
          <li><strong>HP / Armor Slots:</strong> 8 Armor Slots | <strong>Stress:</strong> 6 | <strong>Difficulty:</strong> 14 | <strong>Evasion:</strong> 14</li>
          <li><strong>Thresholds:</strong> Minor: 8 | Major: 16 | Severe: 24</li>
          <li><strong>Primary Attack:</strong> <strong>Shadowfang Signal Pounce</strong> (Melee, +4 to Hit / +6 vs Mind-Links | <strong>2d8+5</strong> Physical/Psychic Damage).</li>
          <li><strong>Special (Signal Lock):</strong> Gains +2 to Hit vs targets maintaining active telepathic mind-links (Britt & Aggie).</li>
          <li><strong>Special (Mirror-Step Evasion):</strong> Teleports 40ft instantly into tree shadows upon striking, leaving a purring Aether decoy (1 Armor Slot to destroy).</li>
          <li><strong>Reaction (Memory Surge):</strong> Taking Severe damage forces all nearby PCs to make a DC 14 Presence Check or gain 1 Stress from psychic feedback.</li>
        </ul>

        <h3>🐲 Gale-Wyrm (Apex Aerostatic Dragon — Tier 2 Heavy)</h3>
        <ul>
          <li><strong>HP / Armor Slots:</strong> 7 Armor Slots | <strong>Stress:</strong> 5 | <strong>Difficulty:</strong> 15 | <strong>Evasion:</strong> 13</li>
          <li><strong>Thresholds:</strong> Minor: 9 | Major: 17 | Severe: 25</li>
          <li><strong>Primary Attack:</strong> <strong>Gravity Core Cataclysm</strong> (Very Far Range, +3 to Hit | <strong>2d10+6</strong> Physical/Impact Damage).</li>
          <li><strong>Special (Gravity Drop):</strong> Lifts 500lb petrified granite boulder with gravity aura and hurls it down (DC 14 Agility dodge).</li>
          <li><strong>Reaction (Gravity Reversal):</strong> Ranged attacks made at Disadvantage; melee attackers float 15ft into the air.</li>
        </ul>

        <h3>🐱 Stunted Canopy Cat (Minion Swarm — Tier 1 Skirmisher)</h3>
        <ul>
          <li><strong>HP:</strong> 2 HP | <strong>Stress:</strong> 2 | <strong>Difficulty:</strong> 12 | <strong>Evasion:</strong> 12</li>
          <li><strong>Thresholds:</strong> Minor: 4 | Major: 8 | Severe: 12</li>
          <li><strong>Primary Attack:</strong> <strong>Canopy Ambush Shred</strong> (Melee, +3 to Hit / +5 vs Pinned | <strong>1d8+3</strong> Physical Damage).</li>
          <li><strong>Mizizi Instinct:</strong> +2 to Hit vs targets pinned under timber or boulders, caught in tar moats, or prone.</li>
        </ul>

        <h3>🦈 Dagger Shark Pod (Abyssal Interceptor — Tier 1 Shock Troop)</h3>
        <ul>
          <li><strong>HP / Armor Slots:</strong> 3 Armor Slots | <strong>Stress:</strong> 3 | <strong>Difficulty:</strong> 13 | <strong>Evasion:</strong> 12</li>
          <li><strong>Thresholds:</strong> Minor: 5 | Major: 10 | Severe: 15</li>
          <li><strong>Primary Attack:</strong> <strong>Vortical Pressure Snap</strong> (Melee, +3 to Hit / Advantage in Mud | <strong>1d10+4</strong> Physical Damage).</li>
          <li><strong>Special (Pressure Scent):</strong> Advantage vs Iggy when using pressure nodes in flooded mud.</li>
        </ul>
    `;

    // Page 3: Ally NPCs & Scrap Defense Rules
    const p3_content = `
        <h2>🪵 Ally NPCs, Recruitment & Scrap Defense Matrix</h2>
        
        <h3>🌊 Rill (Wadi Researcher / Combat Aide)</h3>
        <ul>
          <li><strong>Description:</strong> Clever innovator with dark braided hair and a leather field coat with glowing teal Wadi-flow conduits. Publicly Mizizi, secretly Wadi.</li>
          <li><strong>Role:</strong> First-responder combat aide sent to field-test tech and recruit Squad 907 for <strong>Professor Ink's Scrivener Guild Expedition</strong>.</li>
          <li><strong>HP / Armor Slots:</strong> 8 Armor Slots | <strong>Stress:</strong> 6 | <strong>Difficulty:</strong> 13 | <strong>Evasion:</strong> 13</li>
          <li><strong>Primary Attack:</strong> <strong>Wadi Resonator Burst</strong> (Far Range, +4 to Hit | <strong>1d8+3</strong> Energy Damage).</li>
          <li><strong>Special (Aether Signal Jammer):</strong> Emits a 30ft pulse that cancels Mwaza-Chui's +2 Signal Lock bonus vs Britt & Aggie for 2 rounds.</li>
          <li><strong>Special (Wadi Flow Buff):</strong> Allies within 15ft gain +1 to Attack rolls and Advantage on Agility checks.</li>
        </ul>

        <h3>🪵 Bramble (Plant-Kin Ally - Squad 06)</h3>
        <ul>
          <li><strong>Description:</strong> Broad-shouldered plant-kin male with mossy pine bark skin and a heavy wool cloak. Study buddy of Aggie & Pip.</li>
          <li><strong>Goal:</strong> Protect Dr. Rose Halloway and hold the defensive line against aerial predators.</li>
          <li><strong>HP / Armor Slots:</strong> 9 Armor Slots | <strong>Stress:</strong> 7 | <strong>Difficulty:</strong> 12 | <strong>Evasion:</strong> 10</li>
          <li><strong>Primary Attack:</strong> <strong>Gnarled Pine Entanglement</strong> (Melee, +3 to Hit | <strong>1d10+4</strong> Physical Damage).</li>
          <li><strong>Special (Root Wall):</strong> Summons a pine-root barrier providing +2 Evasion cover (absorbs 2 hits).</li>
        </ul>

        <h3>🩺 Dr. Rose Halloway (Lead Field Medic)</h3>
        <ul>
          <li><strong>Role:</strong> Treating injured candidates under a temporary wooden longhouse lean-to in Zone 5.</li>
          <li><strong>Mechanic:</strong> PCs can escort wounded candidates to Dr. Halloway to clear 2 Stress or restore 1 Armor Slot.</li>
        </ul>

        <hr/>

        <h3>🛠️ Session 9 Scrap Crafting Matrix</h3>
        <table border="1" cellpadding="5">
          <tr><th>Scrap Component</th><th>Crafted Trap / Fortification</th><th>Combat Effect</th></tr>
          <tr><td>Bungee Cords + Wire</td><td>Bungee Tripwire Trap</td><td>Restrains Mwaza-Chui / Cats (DC 13 Finesse to set; DC 14 Agility escape).</td></tr>
          <tr><td>Sticky Tar Buckets</td><td>Tar Perimeter Moat</td><td>Halves movement speed; ignites for 1d8 Fire damage if lit by torch.</td></tr>
          <tr><td>Lead Weights + Rope</td><td>Weighted Entangling Net</td><td>Pins Gale-Wyrm to ground for 1 round (DC 13 Strength check to throw).</td></tr>
          <tr><td>Sponge Boom + Tar</td><td>Absorbent Barrier Wall</td><td>Blocks Dagger Shark pressure waves & electrical arcs.</td></tr>
        </table>
    `;

    // Page 4: Master Zone Encounter Matrix & GM Fear Spend Options
    const p4_content = `
        <h2>🗺️ Master Zone Encounter Matrix, GM Fear Spend Options & Biomes</h2>
        <p><em>Quick-reference matrix for GM encounter triggers, creature counts per zone, GM Fear costs, and Daggerheart biome effects across all 3 active zones.</em></p>

        <table border="1" cellpadding="6" style="border-collapse: collapse; width: 100%; font-size: 13px;">
          <tr style="background-color: #2a2a38; color: #ffffff;">
            <th style="width: 18%;">Zone & Biome</th>
            <th style="width: 22%;">Encounter & Threat Level</th>
            <th style="width: 22%;">Creature Roster & Counts</th>
            <th style="width: 20%;">GM Fear Spend Options</th>
            <th style="width: 18%;">Biome Effect & Hazard</th>
          </tr>
          <tr>
            <td><strong>Zone 0 & 8</strong><br><em>Nordic Pine Resonator Ridge</em></td>
            <td><strong>⚡ Core Breach Ambush</strong><br><span style="color: #d9534f; font-weight: bold;">Deadly Boss Stalk</span></td>
            <td>
              • <strong>Mwaza-Chui</strong> (Tier 2 Boss) ×1<br>
              • <strong>Stunted Canopy Cats</strong> (Minions) ×2
            </td>
            <td>
              • <strong>1 Fear:</strong> <em>Aether Decoy Burst</em> (15ft, DC 14 Agility or 1d8 Psychic + 1 Stress)<br>
              • <strong>2 Fear:</strong> <em>Walker Core Arc</em> (2d10+4 Elec)
            </td>
            <td><strong>Violet Voltage Canopy:</strong> Resonator sparks flicker. Mind-links/Spells trigger Mwaza-Chui Signal Lock (+2 to Hit).</td>
          </tr>
          <tr>
            <td><strong>Zone 1 & 3</strong><br><em>Petrified Granite Canopy</em></td>
            <td><strong>🐲 Aerostatic Tempest</strong><br><span style="color: #d9534f; font-weight: bold;">Deadly Aerial Raid</span></td>
            <td>
              • <strong>Gale-Wyrm</strong> (Tier 2 Heavy) ×1<br>
              • <strong>Stunted Canopy Cats</strong> (Minions) ×3
            </td>
            <td>
              • <strong>1 Fear:</strong> <em>Gravity Shift</em> (30ft radius, float 20ft up, Disadvantage on ground attacks)<br>
              • <strong>1 Fear:</strong> <em>Boulder Hurl</em> (2d10+6)
            </td>
            <td><strong>Low Visibility Rain:</strong> Heavy mist reduces sight >40ft. Ranged attacks beyond 40ft have Disadvantage unless lit.</td>
          </tr>
          <tr>
            <td><strong>Zone 5</strong><br><em>Flooded Silt Estuary Camp</em></td>
            <td><strong>🦈 Estuary Mud Siege</strong><br><span style="color: #d9534f; font-weight: bold;">Deadly Multi-Wave Siege</span></td>
            <td>
              • <strong>Mwaza-Chui</strong> (Stalker) ×1<br>
              • <strong>Dagger Sharks</strong> (Shock Troops) ×4<br>
              • <strong>Stunted Canopy Cats</strong> ×3
            </td>
            <td>
              • <strong>1 Fear:</strong> <em>Silt Flash Flood</em> (Mud pools expand; DC 13 Str or Restrained)<br>
              • <strong>1 Fear:</strong> <em>Death Roll</em> (Extra Bite + 1 Stress)
            </td>
            <td><strong>Flooded Mud Basins:</strong> Speed halved in mud. Dagger Sharks get Advantage (+2 to Hit). Elec attacks +1d6 splash.</td>
          </tr>
        </table>
    `;

    // Page 5: Official Daggerheart Environment Rules & Mechanics
    const p5_content = `
        <h2>🏰 Official Daggerheart Environment Rules & Mechanics</h2>
        <p><em>Full Daggerheart Environment design framework for running scenes with baseline Tier, Type, room Difficulty, Impulses, Passives, Reactions, Actions, Prompts, and Countdowns.</em></p>

        <hr/>
        <h3>📋 Daggerheart Environment Quick Creation Rules</h3>
        <ul>
          <li><strong>Tier:</strong> Match party level (Tier 1: Levels 1–4). Target numbers & damage scale accordingly.</li>
          <li><strong>Type:</strong> Define scene drama (Exploration, Social, Traversal, Event, or Hybrid).</li>
          <li><strong>Difficulty:</strong> Room target DC for player action rolls (Tier 1 Standard: 13–15).</li>
          <li><strong>Impulses:</strong> 1–3 behavioral cues dictating how the space naturally pushes/reacts to PCs.</li>
          <li><strong>Passives (Continuous):</strong> Always active baseline landscape rules (0 Fear cost).</li>
          <li><strong>Reactions (Triggered Exploits):</strong> Triggered by player failure or rolling with Fear (Costs 1 Fear).</li>
          <li><strong>Actions (Active Hazards):</strong> Active GM hazards when holding spotlight (Costs 1 Fear).</li>
          <li><strong>Prompts & Questions:</strong> 1–2 open-ended italicized questions under features to engage players.</li>
          <li><strong>Countdowns (Clocks):</strong> Progress clocks (tick up on success) or Consequence clocks (tick down on failure/Fear).</li>
        </ul>
    `;

    // Page 6: Scene 1 DM Guide — Walker Core Breach (Zone 0 & 8)
    const p6_content = `
        <h2>⚡ Scene 1 DM Guide: Walker Core Breach (Resonator Ridge)</h2>
        <p><strong>Zone:</strong> Zone 0 & 8 (Nordic Pine Resonator Ridge) | <strong>Tier 1 Event / Traversal Hybrid</strong> | <strong>Room Difficulty: 14</strong></p>

        <hr/>
        <h3>🗣️ Establishing Shot (Read-Aloud to Set Scene)</h3>
        <blockquote>
          "A deafening hum shatters the forest air as the Walker Core’s high-voltage resonator coils spark violet lightning into the dark sky. The glowing barrier wall flickers, cracks, and vanishes. Rain begins to pour through the tall pine canopy, turning the ground into a roaring muddy surge. Fleeing candidates scramble blindly down the slippery ridge as high-frequency static fills your ears."
        </blockquote>

        <hr/>
        <h3>🐾 Beast Roster & Exact Counts</h3>
        <ul>
          <li><strong>1× Mwaza-Chui</strong> (Memory Jaguar — Tier 2 Solo Boss Stalker)<br/>
              <em>Stats: HP 8 | Stress 6 | Evasion 14 | Difficulty 14 | <strong>Thresholds: Minor 8 | Major 16 | Severe 24</strong></em></li>
          <li><strong>2× Stunted Canopy Cats</strong> (Tier 1 Minion Swarm)<br/>
              <em>Stats: HP 2 | Stress 2 | Evasion 12 | Difficulty 12 | <strong>Thresholds: Minor 4 | Major 8 | Severe 12</strong></em></li>
        </ul>

        <hr/>
        <h3>👁️ Beast Descriptions to Read/Say to Players</h3>
        <ul>
          <li><strong>Mwaza-Chui:</strong> <em>"A massive, broad-shouldered feline predator woven from translucent dark violet energy and shifting Aether. Its fur glimmers like static electricity, and its glowing silver eyes mirror the exact frequency of your telepathic mind-link."</em></li>
          <li><strong>Stunted Canopy Cats:</strong> <em>"Small, feral tree-cats with mottled moss-green fur and coiled, wiry muscles. Their ears are tufted, their amber eyes gleam in the dark, and razor-sharp claws click against the wet pine bark as they stalk you from above."</em></li>
        </ul>

        <hr/>
        <h3>⚔️ Cool Combat Moments & Narrative Triggers to Describe</h3>
        <ul>
          <li><strong>Signal Lock Pounce:</strong> <em>"Mwaza-Chui vanishes into a flash of violet static, reappearing behind [Target PC] with claws charged in raw Aether energy!"</em></li>
          <li><strong>Decoy Mirror-Step:</strong> <em>"As your blade strikes the jaguar, its body shatters into a cloud of glowing purple sparks—it was a decoy! The real beast leaps down from a high branch behind you!"</em></li>
          <li><strong>Canopy Cat Ambush Shred:</strong> <em>"The two canopy cats drop simultaneously from the branches, pinning [Target PC] to the mud as their claws shred through leather and canvas!"</em></li>
        </ul>

        <hr/>
        <h3>🏰 Environment Mechanics & GM Fear Expenditure</h3>
        <ul>
          <li><strong>Passive (Violet Voltage Arc Field):</strong> Continuous (0 Fear). Mind-links or spells emit a violet flash; Mwaza-Chui gains +2 to Hit (<em>Signal Lock</em>).<br/><em>• What does the air smell like right before a coil discharges over your head?</em></li>
          <li><strong>Reaction (Overloaded Coil — 1 Fear):</strong> Triggered on failed Agility or roll with Fear. Coil explodes in a 20ft arc (DC 14 Agility check or 2d8 Lightning damage).<br/><em>• What piece of metal on your belt hums dangerously in response to the arc?</em></li>
          <li><strong>Action (Canopy Pine Needle Surge — 1 Fear):</strong> Pine needles catch fire in a 15ft radius (Difficult Terrain + 1 Stress/round).<br/><em>• How do you shelter your eyes as burning needles rain down around you?</em></li>
        </ul>

        <hr/>
        <h3>⏰ Scene 1 Tracker</h3>
        <p><strong>Consequence Clock (4 Segments — Walker Core Collapse):</strong> Tick down 1 segment on failed rolls or Fear. At 0, the barrier shatters completely, sweeping PCs and beasts into Zone 1.</p>
    `;

    // Page 7: Scene 2 DM Guide — Nordic Pine Forest Rescue (Zone 1 & 3)
    const p7_content = `
        <h2>🌲 Scene 2 DM Guide: Nordic Pine Forest Rescue</h2>
        <p><strong>Zone:</strong> Zone 1 & 3 (Petrified Granite Canopy) | <strong>Tier 1 Exploration / Traversal Hybrid</strong> | <strong>Room Difficulty: 14</strong></p>

        <hr/>
        <h3>🗣️ Establishing Shot (Read-Aloud to Set Scene)</h3>
        <blockquote>
          "Tall evergreen pines loom overhead, their dark needles dripping with glowing turquoise condensation. Among the mossy granite boulders, you hear Bramble’s voice shouting over the gale: 'Hold the beam, Doctor!' Above them, a colossal silhouette with aerostatic wings drifts through the mist, lifting a 500-pound granite boulder into the air with a pulse of localized gravity."
        </blockquote>

        <hr/>
        <h3>🐾 Beast Roster & Exact Counts</h3>
        <ul>
          <li><strong>1× Gale-Wyrm</strong> (Apex Aerostatic Dragon — Tier 2 Heavy)<br/>
              <em>Stats: HP 7 | Stress 5 | Evasion 13 | Difficulty 15 | <strong>Thresholds: Minor 9 | Major 17 | Severe 25</strong></em></li>
          <li><strong>3× Stunted Canopy Cats</strong> (Tier 1 Minion Swarm)<br/>
              <em>Stats: HP 2 | Stress 2 | Evasion 12 | Difficulty 12 | <strong>Thresholds: Minor 4 | Major 8 | Severe 12</strong></em></li>
        </ul>

        <hr/>
        <h3>👁️ Beast Descriptions to Read/Say to Players</h3>
        <ul>
          <li><strong>Gale-Wyrm:</strong> <em>"A serpentine dragon with translucent, iridescent scales that shimmer like oil on water. A glowing gravity core hums inside its chest, creating a swirling vortex of air that lifts rocks and debris into orbit around its wings."</em></li>
          <li><strong>Stunted Canopy Cats:</strong> <em>"Three moss-backed tree-cats leap seamlessly between floating granite boulders, using low gravity to bound 30 feet through the air with unsheathed talons."</em></li>
        </ul>

        <hr/>
        <h3>⚔️ Cool Combat Moments & Narrative Triggers to Describe</h3>
        <ul>
          <li><strong>Gravity Core Cataclysm:</strong> <em>"The Gale-Wyrm opens its maw, unleashing a localized gravitational pulse. Boulders shatter, and the earth beneath your feet bulges outward as gravity reverses!"</em></li>
          <li><strong>Aerostatic Boulder Drop:</strong> <em>"With a sweep of its wings, the Gale-Wyrm hurls a suspended 500-pound granite slab down at [Target PC], crushing the earth into a crater!"</em></li>
          <li><strong>Root Wall Defense:</strong> <em>"Bramble slams his wood-kin fists into the soil, causing thick pine roots to erupt around Dr. Halloway, forming a solid wooden barrier!"</em></li>
        </ul>

        <hr/>
        <h3>🏰 Environment Mechanics & GM Fear Expenditure</h3>
        <ul>
          <li><strong>Passive (Low Visibility Pine Rain):</strong> Continuous (0 Fear). Sight reduced beyond 40ft; ranged attacks >40ft at Disadvantage.<br/><em>• What memory does the cold pine rain bring to mind as it drenches your cloak?</em></li>
          <li><strong>Reaction (Tectonic Gravity Shift — 1 Fear):</strong> 30ft radius gravity inversion; PCs float 20ft (Disadvantage on ground melee attacks for 1 round).<br/><em>• What item slips from your pouch and floats away as gravity inverts?</em></li>
          <li><strong>Action (Aerostatic Boulder Drop — 1 Fear):</strong> Hurls 500lb boulder (DC 14 Agility check or 2d10+6 Physical damage and Pinned).<br/><em>• Where do you dive to avoid being crushed against the mossy granite floor?</em></li>
        </ul>

        <hr/>
        <h3>⏰ Scene 2 Tracker</h3>
        <p><strong>Progress Clock (6 Segments — Squad 06 Evacuation):</strong> Tick up 1 segment on successful checks against DC 14 (clearing boulders, guiding wounded, holding defensive line). At 6, Squad 06 is safely evacuated to Zone 5.</p>
    `;

    // Page 8: Scene 3 DM Guide — Fortified Canyon Camp Siege (Zone 5)
    const p8_content = `
        <h2>🦈 Scene 3 DM Guide: Fortified Canyon Camp Siege</h2>
        <p><strong>Zone:</strong> Zone 5 (Flooded Silt Estuary) | <strong>Tier 1 Event / Social Hybrid</strong> | <strong>Room Difficulty: 13</strong></p>

        <hr/>
        <h3>🗣️ Establishing Shot (Read-Aloud to Set Scene)</h3>
        <blockquote>
          "Nestled against a cliff wall under a weathered timber longhouse overhang, the camp fire crackles warmly against the cold Nordic wind. Rill adjusts her bio-resonance scanner: 'Ink wants you three in the Scrivener Guild for his forest expedition, but first we survive tonight.' As Britt and Aggie open their mind-link, a low, rhythmic purring echoes from the high pine ridge—and the swollen estuary waters begin to churn with dark shapes."
        </blockquote>

        <hr/>
        <h3>🐾 Beast Roster & Exact Counts</h3>
        <ul>
          <li><strong>1× Mwaza-Chui</strong> (Memory Jaguar — Boss Stalker)<br/>
              <em>Stats: HP 8 | Stress 6 | Evasion 14 | Difficulty 14 | <strong>Thresholds: Minor 8 | Major 16 | Severe 24</strong></em></li>
          <li><strong>4× Dagger Sharks</strong> (Aquatic Shock Troops — Tier 1)<br/>
              <em>Stats: HP 3 | Stress 3 | Evasion 13 | Difficulty 13 | <strong>Thresholds: Minor 6 | Major 12 | Severe 18</strong></em></li>
          <li><strong>3× Stunted Canopy Cats</strong> (Tier 1 Minion Swarm)<br/>
              <em>Stats: HP 2 | Stress 2 | Evasion 12 | Difficulty 12 | <strong>Thresholds: Minor 4 | Major 8 | Severe 12</strong></em></li>
        </ul>

        <hr/>
        <h3>👁️ Beast Descriptions to Read/Say to Players</h3>
        <ul>
          <li><strong>Dagger Sharks:</strong> <em>"Eight-foot-long sleek predators with hardened slate-grey skin and rows of serrated copper teeth. They surge through the knee-deep estuary mud as if it were open sea, thrashing violently toward the barricades."</em></li>
        </ul>

        <hr/>
        <h3>⚔️ Cool Combat Moments & Narrative Triggers to Describe</h3>
        <ul>
          <li><strong>Vortical Pressure Snap:</strong> <em>"A Dagger Shark explodes out of the silt mud, locking its jaw onto [Target PC]'s leg and dragging them into the rushing estuary current!"</em></li>
          <li><strong>Tar Moat Ignition:</strong> <em>"Rill fires a flare into the scrap tar moat—a 20-foot wall of roaring orange fire bursts upward, incinerating incoming beasts!"</em></li>
          <li><strong>Shadowfang Signal Pounce:</strong> <em>"Mwaza-Chui leaps from the longhouse roof timbers directly onto [Target PC], its Aether claws crackling as it locks onto your telepathic thoughts!"</em></li>
        </ul>

        <hr/>
        <h3>🏰 Environment Mechanics & GM Fear Expenditure</h3>
        <ul>
          <li><strong>Passive (Flooded Silt Estuary):</strong> Continuous (0 Fear). Speed halved in mud. Dagger Sharks get Advantage (+2 to Hit). Lightning attacks deal +1d6 splash.<br/><em>• How does heavy silt mud cling to your boots as you brace against the wave?</em></li>
          <li><strong>Reaction (Silt Flash Flood — 1 Fear):</strong> Estuary water surges (DC 13 Strength check or become Restrained in mud).<br/><em>• Who reaches out a hand to pull you out as the current sweeps you off your feet?</em></li>
          <li><strong>Action (Tar Moat Flare-Up — 1 Fear):</strong> Tar moats ignite into a 20ft fire wall (1d8 Fire damage to any beast crossing).<br/><em>• What shadow looms through the smoke as the flames roar to life?</em></li>
        </ul>

        <hr/>
        <h3>⏰ Scene 3 Tracker</h3>
        <p><strong>Progress Clock (8 Segments — Siege Defense Victory):</strong> Tick up 1 segment whenever a beast is slain, a trap is triggered, or a PC holds the line. At 8, the siege is broken!</p>
    `;

    // Page 9: Scene 2B DM Guide — Granite Canyon Basin (Zone 1 & 3 Generic)
    const p9_content = `
        <h2>⛰️ Scene 2B DM Guide: Granite Canyon Basin (Generic Canyon)</h2>
        <p><strong>Zone:</strong> Zone 1 & 3 (Petrified Granite Canyon Basin) | <strong>Tier 1 Exploration / Traversal Hybrid</strong> | <strong>Room Difficulty: 14</strong></p>

        <hr/>
        <h3>🗣️ Establishing Shot (Read-Aloud to Set Scene)</h3>
        <blockquote>
          "High, weathered granite canyon walls rise abruptly from the pine forest floor, boxing in the misty basin. Chiseled stone ledges and giant petrified tree stumps form natural terraced steps leading down to a roaring mountain stream. Above the canyon rim, dark clouds churn as localized gravity anomalies cause loose slate and mossy boulders to hum and levitate."
        </blockquote>

        <hr/>
        <h3>🐾 Beast Roster & Exact Counts</h3>
        <ul>
          <li><strong>1× Gale-Wyrm</strong> (Apex Aerostatic Dragon — Tier 2 Heavy)<br/>
              <em>Stats: HP 7 | Stress 5 | Evasion 13 | Difficulty 15 | <strong>Thresholds: Minor 9 | Major 17 | Severe 25</strong></em></li>
          <li><strong>3× Stunted Canopy Cats</strong> (Tier 1 Minion Swarm)<br/>
              <em>Stats: HP 2 | Stress 2 | Evasion 12 | Difficulty 12 | <strong>Thresholds: Minor 4 | Major 8 | Severe 12</strong></em></li>
        </ul>

        <hr/>
        <h3>👁️ Beast Descriptions to Read/Say to Players</h3>
        <ul>
          <li><strong>Gale-Wyrm:</strong> <em>"A serpentine dragon circling high between the narrow canyon walls, its gravity core casting shimmering distortion waves over the granite cliffs below."</em></li>
          <li><strong>Stunted Canopy Cats:</strong> <em>"Three agile tree-cats prowling along the narrow canyon cliff ledges, ready to pounce on anyone crossing the stone stream."</em></li>
        </ul>

        <hr/>
        <h3>⚔️ Cool Combat Moments & Narrative Triggers to Describe</h3>
        <ul>
          <li><strong>Canyon Boulder Collapse:</strong> <em>"Gale-Wyrm’s gravity pulse dislodges a massive granite slab from the upper canyon wall, sending it crashing into the narrow bottleneck!"</em></li>
          <li><strong>Cliff-Edge Pounce:</strong> <em>"A canopy cat leaps from a high granite shelf, using the narrow canyon walls to ricochet down onto [Target PC]!"</em></li>
        </ul>

        <hr/>
        <h3>🏰 Environment Mechanics & GM Fear Expenditure</h3>
        <ul>
          <li><strong>Passive (Canyon Echo & Low Visibility Mist):</strong> Sound amplifies in the canyon bottleneck; ranged attacks >40ft suffer Disadvantage.<br/><em>• How does your voice ring out as you call out target positions across the gorge?</em></li>
          <li><strong>Reaction (Granite Rockfall — 1 Fear):</strong> Dislodges loose cliff stones (DC 14 Agility check or 2d8 Physical damage).<br/><em>• Where do you dive for cover as shattered slate rains down from above?</em></li>
          <li><strong>Action (Gravity Choke — 1 Fear):</strong> Reverses gravity in the canyon bottleneck, lifting PCs 20ft off their feet.<br/><em>• What object slips from your grasp as gravity vanishes beneath you?</em></li>
        </ul>
    `;

    // Page 10: Scene 3B DM Guide — Basalt Canyon Defiles (Zone 5 Generic)
    const p10_content = `
        <h2>🏜️ Scene 3B DM Guide: Basalt Canyon Defiles (Generic Canyon)</h2>
        <p><strong>Zone:</strong> Zone 5 (Flooded Basalt Canyon Defiles) | <strong>Tier 1 Event / Combat Siege</strong> | <strong>Room Difficulty: 14</strong></p>

        <hr/>
        <h3>🗣️ Establishing Shot (Read-Aloud to Set Scene)</h3>
        <blockquote>
          "Knee-deep dark silt water surges through a tight basalt canyon defile, flanked by steep black rock walls and timber longhouse palisades. Thunder rumbles as rain cascades off the cliff overhangs, turning the rocky riverbed into a swirling mud trap. At the end of the defile, heavy wooden gates hold back the floodwaters—but beneath the murky surface, dorsal fins cut through the rushing current."
        </blockquote>

        <hr/>
        <h3>🐾 Beast Roster & Exact Counts</h3>
        <ul>
          <li><strong>1× Mwaza-Chui</strong> (Memory Jaguar — Tier 2 Solo Boss Stalker)<br/>
              <em>Stats: HP 8 | Stress 6 | Evasion 14 | Difficulty 14 | <strong>Thresholds: Minor 8 | Major 16 | Severe 24</strong></em></li>
          <li><strong>4× Dagger Sharks</strong> (Aquatic Shock Troops — Tier 1)<br/>
              <em>Stats: HP 3 | Stress 3 | Evasion 12 | Difficulty 13 | <strong>Thresholds: Minor 6 | Major 12 | Severe 18</strong></em></li>
          <li><strong>3× Stunted Canopy Cats</strong> (Tier 1 Minion Swarm)<br/>
              <em>Stats: HP 2 | Stress 2 | Evasion 12 | Difficulty 12 | <strong>Thresholds: Minor 4 | Major 8 | Severe 12</strong></em></li>
        </ul>

        <hr/>
        <h3>👁️ Beast Descriptions to Read/Say to Players</h3>
        <ul>
          <li><strong>Mwaza-Chui:</strong> <em>"Prowls the high basalt canyon rims above the defile, its violet Aether form silhouetted against the stormy sky as it locks onto your telepathic frequency."</em></li>
          <li><strong>Dagger Sharks:</strong> <em>"Four slate-grey aquatic predators thrashing through the flooded canyon trench, targeting anyone wading near the palisades."</em></li>
        </ul>

        <hr/>
        <h3>⚔️ Cool Combat Moments & Narrative Triggers to Describe</h3>
        <ul>
          <li><strong>Defile Mud Drag:</strong> <em>"A Dagger Shark bursts from the murky canyon water, grabbing [Target PC] by the armor and dragging them into the deep silt pool!"</em></li>
          <li><strong>Ridgetop Shadow Leap:</strong> <em>"Mwaza-Chui drops 30 feet from the basalt cliff top directly onto the barricade deck!"</em></li>
        </ul>

        <hr/>
        <h3>🏰 Environment Mechanics & GM Fear Expenditure</h3>
        <ul>
          <li><strong>Passive (Flooded Canyon Choke):</strong> Speed halved in silt mud. Dagger Sharks get Advantage on attack rolls in water. Lightning attacks deal +1d6 splash.<br/><em>• How do you maintain your footing in the narrow defile as water surges past your knees?</em></li>
          <li><strong>Reaction (Flash Surge — 1 Fear):</strong> Silt water level rises in the canyon defile (DC 13 Strength or Restrained).<br/><em>• What scrap timber barrier do you grab onto to keep from being swept downstream?</em></li>
          <li><strong>Action (Palisade Collapse — 1 Fear):</strong> Timber barricade takes 2d10 Structural damage, spilling debris into the mud.<br/><em>• Which way do you leap as the wooden palisade splinters under the impact?</em></li>
        </ul>
    `;

    const masterPages = [
        {{ name: "🌲 Session 10 Narrative Arc & Nordic Lore", type: "text", text: {{ content: p1_content, format: 1 }} }},
        {{ name: "🐆 Adversary Stat Blocks & Damage Thresholds", type: "text", text: {{ content: p2_content, format: 1 }} }},
        {{ name: "🪵 Ally NPCs, Rill & Scrap Rules", type: "text", text: {{ content: p3_content, format: 1 }} }},
        {{ name: "🗺️ Master Zone Encounter Matrix & Fear Options", type: "text", text: {{ content: p4_content, format: 1 }} }},
        {{ name: "🏰 Daggerheart Environment Rules & Mechanics", type: "text", text: {{ content: p5_content, format: 1 }} }},
        {{ name: "⚡ Scene 1 DM Guide — Walker Core Breach", type: "text", text: {{ content: p6_content, format: 1 }} }},
        {{ name: "🌲 Scene 2 DM Guide — Nordic Pine Rescue", type: "text", text: {{ content: p7_content, format: 1 }} }},
        {{ name: "🦈 Scene 3 DM Guide — Canyon Camp Siege", type: "text", text: {{ content: p8_content, format: 1 }} }},
        {{ name: "⛰️ Scene 2B DM Guide — Granite Canyon Basin", type: "text", text: {{ content: p9_content, format: 1 }} }},
        {{ name: "🏜️ Scene 3B DM Guide — Basalt Canyon Defiles", type: "text", text: {{ content: p10_content, format: 1 }} }}
    ];

    let dmJournal = game.journal.find(j => j.name === "Session 10 Master DM Guide" && j.folder?.id === journalFolder.id);
    if (!dmJournal) {{
        dmJournal = await JournalEntry.create({{
            name: "Session 10 Master DM Guide",
            folder: journalFolder.id,
            pages: masterPages
        }});
    }} else {{
        // Journal exists — add any missing pages only, never overwrite GM edits on existing pages
        for (let pData of masterPages) {{
            let existingP = dmJournal.pages.find(p => p.name === pData.name);
            if (!existingP) {{
                await dmJournal.createEmbeddedDocuments("JournalEntryPage", [pData]).catch(e => console.warn("Page creation note:", e));
                console.log(`Daggerheart Macro: Added new journal page '${{pData.name}}'.`);
            }} else {{
                console.log(`Daggerheart Macro: Journal page '${{pData.name}}' already exists, skipping.`);
            }}
        }}
    }}

    const pages = dmJournal.pages.contents || dmJournal.pages;
    const p1_id = pages[0]?.id || dmJournal.id;
    const p2_id = pages[1]?.id || dmJournal.id;
    const p3_id = pages[2]?.id || dmJournal.id;
    const p4_id = pages[3]?.id || dmJournal.id;
    const p5_id = pages[4]?.id || dmJournal.id;
    const p6_id = pages[5]?.id || dmJournal.id;
    const p7_id = pages[6]?.id || dmJournal.id;
    const p8_id = pages[7]?.id || dmJournal.id;
    const p9_id = pages[8]?.id || dmJournal.id;
    const p10_id = pages[9]?.id || dmJournal.id;

    // ── 2. Create Dedicated Actor Folder, Features & Active Effects ─────────────
    let actorFolder = game.folders.find(f => f.name === "Session 10 - Adversaries & Allies" && f.type === "Actor");
    if (!actorFolder) {{
        actorFolder = await Folder.create({{ name: "Session 10 - Adversaries & Allies", type: "Actor" }});
    }}

    let defaultActorType = "adversary";
    try {{
        const rawTypes = game.system?.documentTypes?.Actor || game.documentTypes?.Actor || CONFIG?.Actor?.typeLabels;
        if (rawTypes) {{
            const typeArray = Array.isArray(rawTypes) ? rawTypes : Object.keys(rawTypes);
            if (typeArray.includes("adversary")) defaultActorType = "adversary";
            else if (typeArray.includes("character")) defaultActorType = "character";
            else if (typeArray.length > 0) defaultActorType = typeArray[0];
        }}
    }} catch (e) {{
        console.warn("Daggerheart Actor Type Detection Note:", e);
    }}

    let defaultItemType = "feature";
    try {{
        const rawItemTypes = game.system?.documentTypes?.Item || game.documentTypes?.Item || CONFIG?.Item?.typeLabels;
        if (rawItemTypes) {{
            const itemTypeArray = Array.isArray(rawItemTypes) ? rawItemTypes : Object.keys(rawItemTypes);
            if (itemTypeArray.includes("feature")) defaultItemType = "feature";
            else if (itemTypeArray.includes("action")) defaultItemType = "action";
            else if (itemTypeArray.includes("ability")) defaultItemType = "ability";
            else if (itemTypeArray.length > 0) defaultItemType = itemTypeArray[0];
        }}
    }} catch (e) {{
        console.warn("Daggerheart Item Type Detection Note:", e);
    }}

    const actorDefinitions = [
        {{
            name: "Mwaza-Chui (Memory Jaguar)",
            type: defaultActorType,
            folder: actorFolder.id,
            img: TOKEN_CHUI,
            system: {{
                traits: {{ agility: {{ value: 3 }}, instinct: {{ value: 4 }}, strength: {{ value: 2 }}, presence: {{ value: 1 }}, finesse: {{ value: 3 }}, knowledge: {{ value: 2 }} }},
                resources: {{
                    hitPoints: {{ value: 0, max: 8 }},
                    stress: {{ value: 0, max: 6, isReversed: true }}
                }},
                evasion: 14,
                difficulty: 14,
                thresholds: {{ minor: 8, major: 16, severe: 24 }},
                damageThresholds: {{ minor: 8, major: 16, severe: 24 }},
                biography: `
                    <h3>🐆 Mwaza-Chui — Tier 2 Solo Boss (Memory Jaguar)</h3>
                    <p><strong>Primary Attack:</strong> <strong>Shadowfang Signal Pounce</strong> (Melee, +4 to Hit / +6 vs Mind-Links | <strong>2d8+5</strong> Physical/Psychic Damage)</p>
                    <p><strong>Damage Thresholds:</strong> <strong>Minor 8 | Major 16 | Severe 24</strong></p>
                    
                    <hr/>
                    <h4>🗺️ Zone Encounter & Creature Count Matrix</h4>
                    <table border="1" cellpadding="4" style="width:100%; border-collapse:collapse; font-size:12px;">
                      <tr style="background:#2a2a38; color:#fff;"><th>Zone / Biome</th><th>Encounter Title</th><th>Creature Count</th><th>GM Fear Costs</th></tr>
                      <tr><td>Zone 0 & 8 (Resonator Ridge)</td><td>⚡ Core Breach Ambush</td><td><strong>Mwaza-Chui ×1</strong> + Canopy Cats ×2</td><td>1 Fear: Decoy Burst | 2 Fear: Core Arc</td></tr>
                      <tr><td>Zone 5 (Estuary Camp)</td><td>🦈 Estuary Mud Siege</td><td><strong>Mwaza-Chui ×1</strong> + Dagger Sharks ×4</td><td>1 Fear: Silt Flood | 1 Fear: Frenzy Strike</td></tr>
                    </table>

                    <hr/>
                    <h4>🔥 GM Fear Expenditure Options</h4>
                    <ul>
                      <li><strong>1 Fear (Aether Decoy Burst):</strong> Decoy explodes in a 15ft radius (DC 14 Agility or 1d8 Psychic + 1 Stress).</li>
                      <li><strong>2 Fear (Frequency Overload):</strong> Emits a sonic roar disrupting all spellcasting and mind-links for 1 round.</li>
                    </ul>

                    <hr/>
                    <h4>⚔️ Tactical AI Loop ("Monsters Know What They're Doing")</h4>
                    <ol>
                      <li><strong>Shadow Stalking:</strong> Circles 40ft out in pine canopy. Strikes when a mind-link or spell is activated.</li>
                      <li><strong>Signal Lock Strike:</strong> Pounces onto mind-link user (Britt/Aggie) with +2 to Hit bonus.</li>
                      <li><strong>Mirror-Step Evasion:</strong> Teleports 40ft into tree shadows, leaving a purring Aether decoy.</li>
                    </ol>
                `,
                notes: `
                    <h3>🐆 Mwaza-Chui — Tier 2 Solo Boss</h3>
                    <p><strong>Primary Attack:</strong> <strong>Shadowfang Signal Pounce</strong> (+4 to Hit | 2d8+5 Damage)</p>
                    <p><strong>Damage Thresholds:</strong> Minor 8 | Major 16 | Severe 24</p>
                    <h4>🗺️ Encounter Counts & GM Fear Options</h4>
                    <p><strong>Zone 0 & 8:</strong> Count = 1 (with 2 Canopy Cats) | <strong>1 Fear:</strong> Decoy Burst (1d8 Psychic) | <strong>2 Fear:</strong> Core Arc (2d10+4 Elec)</p>
                    <p><strong>Zone 5:</strong> Count = 1 (with 4 Dagger Sharks & 3 Cats) | <strong>1 Fear:</strong> Silt Flood (DC 13 Str or Restrained)</p>
                `,
                motives: `High-Frequency Stealth Assassin / Boss Stalker targeting mind-link frequencies.`,
                tactics: `Circles 40ft out in canopy. Strikes with Signal Lock (+2 to Hit). Mirror-Steps 40ft away into shadows.`,
                description: `<h3>🐆 Mwaza-Chui — Tier 2 Solo Boss Stalker</h3>`
            }},
            attack: {{
                name: "Shadowfang Signal Pounce",
                type: "Melee",
                damage: "2d8+5",
                modifier: 4,
                img: "icons/skills/violet/mage-charge-buff-purple.webp",
                description: "Locks onto an active mind-link signal, then detonates from canopy shadow — Aether-laced claws shred psyche and flesh in the same stroke."
            }},
            features: [
                {{ name: "Signal Lock", img: "icons/svg/target.svg", description: "Gains +2 to Hit vs targets maintaining active telepathic mind-links (Britt & Aggie)." }},
                {{ name: "Mirror-Step Evasion", img: "icons/svg/eye.svg", description: "Teleports 40ft instantly into tree shadows upon striking, leaving a purring Aether decoy (1 Armor Slot to destroy)." }},
                {{ name: "Memory Surge", img: "icons/svg/lightning.svg", description: "When taking Severe damage, forces all nearby PCs to make a DC 14 Presence Check or gain 1 Stress from psychic feedback." }}
            ],
            effects: [
                {{ name: "Signal Lock Active (+2 to Hit vs Mind-Links)", icon: "icons/svg/target.svg", description: "Signal lock targeted on telepathic mind-link frequency." }},
                {{ name: "Mirror-Step Decoy Active", icon: "icons/svg/eye.svg", description: "Illusionary Aether decoy active 40ft away." }}
            ]
        }},
        {{
            name: "Gale-Wyrm",
            type: defaultActorType,
            folder: actorFolder.id,
            img: TOKEN_WYRM,
            system: {{
                traits: {{ agility: {{ value: 4 }}, instinct: {{ value: 3 }}, strength: {{ value: 3 }}, presence: {{ value: 1 }}, finesse: {{ value: 2 }}, knowledge: {{ value: 1 }} }},
                resources: {{
                    hitPoints: {{ value: 0, max: 7 }},
                    stress: {{ value: 0, max: 5, isReversed: true }}
                }},
                evasion: 13,
                difficulty: 15,
                thresholds: {{ minor: 9, major: 17, severe: 25 }},
                damageThresholds: {{ minor: 9, major: 17, severe: 25 }},
                biography: `
                    <h3>🐲 Gale-Wyrm — Tier 2 Apex Heavy (Aerostatic Dragon)</h3>
                    <p><strong>Primary Attack:</strong> <strong>Gravity Core Cataclysm</strong> (Very Far Range, +3 to Hit | <strong>2d10+6</strong> Physical/Impact Damage)</p>
                    <p><strong>Damage Thresholds:</strong> <strong>Minor 9 | Major 17 | Severe 25</strong></p>
                    
                    <hr/>
                    <h4>🗺️ Zone Encounter & Creature Count Matrix</h4>
                    <table border="1" cellpadding="4" style="width:100%; border-collapse:collapse; font-size:12px;">
                      <tr style="background:#2a2a38; color:#fff;"><th>Zone / Biome</th><th>Encounter Title</th><th>Creature Count</th><th>GM Fear Costs</th></tr>
                      <tr><td>Zone 1 & 3 (Petrified Granite)</td><td>🐲 Aerostatic Tempest</td><td><strong>Gale-Wyrm ×1</strong> + Canopy Cats ×3</td><td>1 Fear: Gravity Shift | 1 Fear: Boulder Drop</td></tr>
                    </table>

                    <hr/>
                    <h4>🔥 GM Fear Expenditure Options</h4>
                    <ul>
                      <li><strong>1 Fear (Tectonic Gravity Shift):</strong> Reverses local gravity in a 30ft radius; grounded PCs float 20ft up (Disadvantage on ground attacks).</li>
                      <li><strong>1 Fear (Aerostatic Gale Blast):</strong> Wing buffet pushes PCs back 20ft and knocks Prone (DC 13 Strength to resist).</li>
                    </ul>

                    <hr/>
                    <h4>⚔️ Tactical AI Loop ("Monsters Know What They're Doing")</h4>
                    <ol>
                      <li><strong>Aerial Harvesting:</strong> Hovers 50-60ft up in pine canopy out of melee reach.</li>
                      <li><strong>Gravity Drop:</strong> Lifts 500lb granite boulders and hurls them down (2d10+6 Severe damage).</li>
                      <li><strong>Gravity Reversal:</strong> Reverses local gravity when targeted by ranged attacks (Ranged Disadvantage).</li>
                    </ol>
                `,
                notes: `
                    <h3>🐲 Gale-Wyrm — Tier 2 Apex Heavy</h3>
                    <p><strong>Primary Attack:</strong> <strong>Gravity Core Cataclysm</strong> (+3 to Hit | 2d10+6 Damage)</p>
                    <p><strong>Damage Thresholds:</strong> Minor 9 | Major 17 | Severe 25</p>
                    <h4>🗺️ Encounter Counts & GM Fear Options</h4>
                    <p><strong>Zone 1 & 3:</strong> Count = 1 (with 3 Canopy Cats) | <strong>1 Fear:</strong> Gravity Shift (float 20ft) | <strong>1 Fear:</strong> Gale Blast (Knock Prone)</p>
                `,
                motives: `Ranged Heavy Artillery & Air Superiority.`,
                tactics: `Hovers 60ft up. Hurls 500lb boulders. Reverses gravity when targeted by ranged attacks.`,
                description: `<h3>🐲 Gale-Wyrm — Tier 2 Apex Heavy</h3>`
            }},
            attack: {{
                name: "Gravity Core Cataclysm",
                type: "Ranged",
                damage: "2d10+6",
                modifier: 3,
                img: "icons/skills/green/wave-crashing-stone.webp",
                description: "A half-tonne petrified granite boulder wreathed in violet gravity distortion tears free from the canyon wall and plummets from sixty feet above — the only warning is a low subsonic hum."
            }},
            features: [
                {{ name: "Gravity Drop", img: "icons/svg/hazard.svg", description: "Lifts 500lb petrified granite boulder with gravity aura and hurls it down (2d10+6 Severe damage, DC 14 Agility dodge)." }},
                {{ name: "Gravity Reversal", img: "icons/svg/upgrade.svg", description: "Reverses local gravity when targeted by ranged attacks. Ranged attacks made at Disadvantage; melee jumpers float 15ft in the air." }}
            ],
            effects: [
                {{ name: "Aerial Flight & High Canopy (60ft)", icon: "icons/svg/aura.svg", description: "Hovering 50-60ft up in the pine canopy out of melee reach." }},
                {{ name: "Gravity Reversal Field (Ranged Disadvantage)", icon: "icons/svg/upgrade.svg", description: "All ranged attacks targeting Gale-Wyrm suffer Disadvantage." }}
            ]
        }},
        {{
            name: "Stunted Canopy Cat",
            type: defaultActorType,
            folder: actorFolder.id,
            img: TOKEN_CAT,
            system: {{
                traits: {{ agility: {{ value: 3 }}, instinct: {{ value: 2 }}, strength: {{ value: 1 }}, presence: {{ value: 0 }}, finesse: {{ value: 2 }}, knowledge: {{ value: 0 }} }},
                resources: {{
                    hitPoints: {{ value: 0, max: 2 }},
                    stress: {{ value: 0, max: 2, isReversed: true }}
                }},
                evasion: 12,
                difficulty: 12,
                thresholds: {{ minor: 4, major: 8, severe: 12 }},
                damageThresholds: {{ minor: 4, major: 8, severe: 12 }},
                biography: `
                    <h3>🐱 Stunted Canopy Cat — Tier 1 Minion Swarm</h3>
                    <p><strong>Primary Attack:</strong> <strong>Canopy Ambush Shred</strong> (Melee, +3 to Hit / +5 vs Pinned | <strong>1d8+3</strong> Physical Damage)</p>
                    <p><strong>Damage Thresholds:</strong> <strong>Minor 4 | Major 8 | Severe 12</strong></p>
                    
                    <hr/>
                    <h4>🗺️ Zone Encounter & Creature Count Matrix</h4>
                    <table border="1" cellpadding="4" style="width:100%; border-collapse:collapse; font-size:12px;">
                      <tr style="background:#2a2a38; color:#fff;"><th>Zone / Biome</th><th>Encounter Title</th><th>Creature Count</th><th>GM Fear Costs</th></tr>
                      <tr><td>Zone 0 & 8 (Resonator Ridge)</td><td>⚡ Core Breach Ambush</td><td>Count = <strong>2 Cats</strong> (with Mwaza-Chui)</td><td>1 Fear: Swarm Drop</td></tr>
                      <tr><td>Zone 1 & 3 (Petrified Granite)</td><td>🐲 Aerostatic Tempest</td><td>Count = <strong>3 Cats</strong> (with Gale-Wyrm)</td><td>1 Fear: Synchronized Pounce</td></tr>
                      <tr><td>Zone 5 (Estuary Camp)</td><td>🦈 Estuary Mud Siege</td><td>Count = <strong>3 Cats</strong> (with Dagger Sharks)</td><td>1 Fear: Canopy Ambush</td></tr>
                    </table>

                    <hr/>
                    <h4>🔥 GM Fear Expenditure Options</h4>
                    <ul>
                      <li><strong>1 Fear (Swarm Drop):</strong> Spawn 2 additional Canopy Cats dropping from pine branches onto backline PCs.</li>
                      <li><strong>1 Fear (Synchronized Pounce):</strong> If 2+ cats attack the same target, target is knocked Prone and Restrained.</li>
                    </ul>
                `,
                notes: `
                    <h3>🐱 Stunted Canopy Cat — Minion Swarm</h3>
                    <p><strong>Primary Attack:</strong> <strong>Canopy Ambush Shred</strong> (+3 to Hit | 1d8+3 Damage)</p>
                    <p><strong>Damage Thresholds:</strong> Minor 4 | Major 8 | Severe 12</p>
                    <p><strong>Zone Counts:</strong> Zone 0/8 = 2 | Zone 1/3 = 3 | Zone 5 = 3</p>
                    <p><strong>1 Fear:</strong> Swarm Drop (+2 Cats) | <strong>1 Fear:</strong> Synchronized Pounce (Knock Prone & Restrain)</p>
                `,
                motives: `Skirmisher & Pinned-Target Finisher (Minion Swarm).`,
                tactics: `Flank through pine branches. Pounce on pinned or prone targets in groups of 3.`,
                description: `<h3>🐱 Stunted Canopy Cat — Minion Swarm</h3>`
            }},
            attack: {{
                name: "Canopy Ambush Shred",
                type: "Melee",
                damage: "1d6+2",
                modifier: 3,
                img: "icons/skills/red/claw-grasp.webp",
                description: "Drops without a sound from the upper canopy — three curved talons rake in a single fluid arc across any exposed skin or gap in armour."
            }},
            features: [
                {{ name: "Mizizi Pinned-Target Instinct", img: "icons/svg/combat.svg", description: "+2 to Hit vs targets pinned under timber or boulders, caught in tar moats, or prone." }},
                {{ name: "Canopy Flanking", img: "icons/svg/oak.svg", description: "Bypasses frontline defenders by leaping through upper pine canopy." }}
            ],
            effects: [
                {{ name: "Mizizi Pinned Target Bonus (+2 to Hit)", icon: "icons/svg/combat.svg", description: "+2 attack bonus against vulnerable or pinned targets." }}
            ]
        }},
        {{
            name: "Dagger Shark",
            type: defaultActorType,
            folder: actorFolder.id,
            img: TOKEN_SHARK,
            system: {{
                traits: {{ agility: {{ value: 3 }}, instinct: {{ value: 2 }}, strength: {{ value: 2 }}, presence: {{ value: 0 }}, finesse: {{ value: 2 }}, knowledge: {{ value: 0 }} }},
                resources: {{
                    hitPoints: {{ value: 0, max: 3 }},
                    stress: {{ value: 0, max: 3, isReversed: true }}
                }},
                evasion: 12,
                difficulty: 13,
                thresholds: {{ minor: 6, major: 12, severe: 18 }},
                damageThresholds: {{ minor: 6, major: 12, severe: 18 }},
                biography: `
                    <h3>🦈 Dagger Shark — Tier 1 Aquatic Shock Troop</h3>
                    <p><strong>Primary Attack:</strong> <strong>Vortical Pressure Snap</strong> (Melee, +3 to Hit / Advantage in Mud | <strong>1d10+4</strong> Physical Damage)</p>
                    <p><strong>Damage Thresholds:</strong> <strong>Minor 6 | Major 12 | Severe 18</strong></p>
                    
                    <hr/>
                    <h4>🗺️ Zone Encounter & Creature Count Matrix</h4>
                    <table border="1" cellpadding="4" style="width:100%; border-collapse:collapse; font-size:12px;">
                      <tr style="background:#2a2a38; color:#fff;"><th>Zone / Biome</th><th>Encounter Title</th><th>Creature Count</th><th>GM Fear Costs</th></tr>
                      <tr><td>Zone 5 (Flooded Estuary Camp)</td><td>🦈 Estuary Mud Siege</td><td>Count = <strong>4 Dagger Sharks</strong></td><td>1 Fear: Silt Flood | 1 Fear: Death Roll</td></tr>
                    </table>

                    <hr/>
                    <h4>🔥 GM Fear Expenditure Options</h4>
                    <ul>
                      <li><strong>1 Fear (Silt-Flash Surge):</strong> Rushing water expands mud pools; PCs in mud must pass DC 13 Strength check or become Restrained.</li>
                      <li><strong>1 Fear (Death Roll):</strong> On a successful hit, Dagger Shark inflicts 1 Stress and drags target 15ft into deep estuary water.</li>
                    </ul>
                `,
                notes: `
                    <h3>🦈 Dagger Shark — Aquatic Shock Troop</h3>
                    <p><strong>Primary Attack:</strong> <strong>Vortical Pressure Snap</strong> (+3 to Hit | 1d10+4 Damage)</p>
                    <p><strong>Damage Thresholds:</strong> Minor 6 | Major 12 | Severe 18</p>
                    <p><strong>Zone 5 Count:</strong> 4 Dagger Sharks</p>
                    <p><strong>1 Fear:</strong> Silt Flood (DC 13 Str or Restrained) | <strong>1 Fear:</strong> Death Roll (+1 Stress & Drag 15ft)</p>
                `,
                motives: `Aquatic Shock Troop & Pressure Interceptor.`,
                tactics: `Attack from water or mud with Pressure Scent Advantage. Execute drive-by bites.`,
                description: `<h3>🦈 Dagger Shark — Aquatic Shock Troop</h3>`
            }},
            attack: {{
                name: "Vortical Pressure Snap",
                type: "Melee",
                damage: "1d10+3",
                modifier: 3,
                img: "icons/skills/blue/shark-jaws-blue.webp",
                description: "Surges up through the knee-deep silt in total silence, mouth gaping at full torque — serrated copper-tinged teeth close around a limb with bone-fracturing hydraulic pressure."
            }},
            features: [
                {{ name: "Pressure Scent Tracking", img: "icons/svg/skull.svg", description: "Advantage on attack rolls against Iggy (emitting Leviathan engine hum) and targets standing in flooded mud." }},
                {{ name: "Drive-By Drag", img: "icons/svg/hazard.svg", description: "Executes rapid drive-by bites (1d10+4 Physical damage) and attempts to drag targets into deep mud." }}
            ],
            effects: [
                {{ name: "Pressure Scent (Advantage in Mud/Water)", icon: "icons/svg/skull.svg", description: "Advantage on attacks in aquatic or flooded mud terrain." }}
            ]
        }},
        {{
            name: "Rill (Combat Aide)",
            type: defaultActorType,
            folder: actorFolder.id,
            img: TOKEN_RILL,
            system: {{
                traits: {{ agility: {{ value: 3 }}, instinct: {{ value: 3 }}, strength: {{ value: 1 }}, presence: {{ value: 2 }}, finesse: {{ value: 4 }}, knowledge: {{ value: 3 }} }},
                resources: {{
                    hitPoints: {{ value: 0, max: 8 }},
                    stress: {{ value: 0, max: 6, isReversed: true }}
                }},
                evasion: 13,
                difficulty: 13,
                thresholds: {{ minor: 7, major: 14, severe: 21 }},
                damageThresholds: {{ minor: 7, major: 14, severe: 21 }},
                biography: `
                    <h3>🌊 Rill (Wadi Researcher / Combat Aide)</h3>
                    <p><strong>Primary Attack:</strong> <strong>Wadi Resonator Burst</strong> (Far Range, +4 to Hit | <strong>1d8+3</strong> Energy Damage)</p>
                    <p><strong>Damage Thresholds:</strong> <strong>Minor 7 | Major 14 | Severe 21</strong></p>
                    <p><strong>Role:</strong> Tactical Support Buffer & Disruptor</p>
                    <p>Positions within 15ft of Squad 907 (Britt, Aggie, Iggy) to grant <em>Wadi Flow</em> buffs (+1 Attack / Agility Advantage).</p>
                `,
                notes: `
                    <h3>🌊 Rill — Tactical Support Aide</h3>
                    <p><strong>Primary Attack:</strong> <strong>Wadi Resonator Burst</strong> (+4 to Hit | 1d8+3 Energy)</p>
                    <p><strong>Damage Thresholds:</strong> Minor 7 | Major 14 | Severe 21</p>
                    <p><strong>Aura:</strong> Allies within 15ft get +1 Attack & Agility Advantage.</p>
                `,
                motives: `Tactical Support Buffer & Disruptor. Field testing tech and recruiting candidates for Professor Ink.`,
                tactics: `Positions within 15ft of allies to grant Wadi Flow. Uses Aether Signal Jammer to block Mwaza-Chui.`,
                description: `<h3>🌊 Rill — Tactical Support & Recruitment</h3>`
            }},
            attack: {{
                name: "Wadi Resonator Burst",
                type: "Ranged",
                damage: "1d8+2",
                modifier: 4,
                img: "icons/skills/blue/freezing-burst.webp",
                description: "A crackling arc of compressed wadi-water energy discharged from the resonator bracer on Rill's forearm — calibrated precisely enough to disrupt a beast's nervous system without harming the candidate beside them."
            }},
            features: [
                {{ name: "Aether Signal Jammer", img: "icons/svg/shield.svg", description: "Emits a 30ft pulse that cancels Mwaza-Chui's +2 Signal Lock bonus vs Britt & Aggie for 2 rounds." }},
                {{ name: "Wadi Flow Tactical Aura", img: "icons/svg/aura.svg", description: "Allies within 15ft gain +1 to Attack rolls and Advantage on Agility checks." }},
                {{ name: "Scrivener Recruitment Pitch", img: "icons/svg/book.svg", description: "Pitches Professor Ink's Mizizi Forest Memory Expedition between combat waves." }}
            ],
            effects: [
                {{ name: "Wadi Flow Buff Aura (+1 Attack / Agility Advantage)", icon: "icons/svg/aura.svg", description: "+1 to Attack rolls and Advantage on Agility checks for nearby allies within 15ft." }},
                {{ name: "Aether Signal Jammer Active (30ft Radius)", icon: "icons/svg/shield.svg", description: "Cancels Mwaza-Chui's Signal Lock bonus." }}
            ]
        }},
        {{
            name: "Bramble",
            type: defaultActorType,
            folder: actorFolder.id,
            img: TOKEN_BRAMBLE,
            system: {{
                traits: {{ agility: {{ value: -1 }}, instinct: {{ value: 3 }}, strength: {{ value: 3 }}, presence: {{ value: 2 }}, finesse: {{ value: 0 }}, knowledge: {{ value: 2 }} }},
                resources: {{
                    hitPoints: {{ value: 0, max: 9 }},
                    stress: {{ value: 0, max: 7, isReversed: true }}
                }},
                evasion: 10,
                difficulty: 12,
                thresholds: {{ minor: 8, major: 15, severe: 22 }},
                damageThresholds: {{ minor: 8, major: 15, severe: 22 }},
                biography: `
                    <h3>🪵 Bramble (Plant-Kin Ally - Squad 06)</h3>
                    <p><strong>Primary Attack:</strong> <strong>Gnarled Pine Entanglement</strong> (Melee, +3 to Hit | <strong>1d10+4</strong> Physical Damage)</p>
                    <p><strong>Damage Thresholds:</strong> <strong>Minor 8 | Major 15 | Severe 22</strong></p>
                    <p><strong>Role:</strong> Frontline Tank & Chokepoint Anchor</p>
                    <p>Places himself directly between Dr. Rose Halloway / injured candidates and advancing beasts.</p>
                `,
                notes: `
                    <h3>🪵 Bramble — Frontline Tank Ally</h3>
                    <p><strong>Primary Attack:</strong> <strong>Gnarled Pine Entanglement</strong> (+3 to Hit | 1d10+4 Damage)</p>
                    <p><strong>Damage Thresholds:</strong> Minor 8 | Major 15 | Severe 22</p>
                    <p><strong>Defense:</strong> Summons Root Walls (+2 Evasion cover).</p>
                `,
                motives: `Frontline Tank & Chokepoint Anchor. Protecting Dr. Rose Halloway.`,
                tactics: `Positions between medics/allies and beasts. Summons Root Walls for cover.`,
                description: `<h3>🪵 Bramble — Frontline Tank</h3>`
            }},
            attack: {{
                name: "Gnarled Root Slam",
                type: "Melee",
                damage: "1d10+4",
                modifier: 2,
                img: "icons/skills/green/leaf-blade-wind.webp",
                description: "Massive root-knotted fists driven by centuries of packed-soil mass slam forward — thorned pine-root tendrils erupt from the impact point and coil around the target's legs, anchoring them in place."
            }},
            features: [
                {{ name: "Root Wall Defense", img: "icons/svg/shield.svg", description: "Summons a pine-root barrier providing +2 Evasion cover (absorbs 2 hits)." }},
                {{ name: "Chokepoint Anchor", img: "icons/svg/oak.svg", description: "Places himself directly between Dr. Rose Halloway / injured candidates and advancing beasts." }}
            ],
            effects: [
                {{ name: "Root Wall Cover (+2 Evasion)", icon: "icons/svg/shield.svg", description: "Grants +2 Evasion cover to adjacent allies." }}
            ]
        }}
    ];

    for (let data of actorDefinitions) {{
        let existing = game.actors.find(a => a.name === data.name);
        if (!existing) {{
            try {{
                existing = await Actor.create({{
                    name: data.name,
                    type: data.type,
                    folder: data.folder,
                    img: data.img,
                    system: data.system,
                    prototypeToken: {{
                        bar1: {{ attribute: "resources.hitPoints" }},
                        bar2: {{ attribute: "resources.stress" }},
                        displayBars: 40,
                        displayName: 20
                    }}
                }});
            }} catch (err) {{
                console.warn(`Daggerheart Macro: Secondary attempt creating '${{data.name}}'...`, err);
                existing = await Actor.create({{
                    name: data.name,
                    type: data.type,
                    folder: data.folder,
                    img: data.img
                }});
                if (existing && data.system) {{
                    await existing.update({{ system: data.system }}).catch(e => console.warn("System update note:", e));
                }}
            }}
        }} else {{
            // Actor already exists — update system data (HP/stress) and refresh items + effects
            console.log(`Daggerheart Macro: '${{data.name}}' already exists — refreshing system data and combat items.`);
            await existing.update({{
                img: data.img,
                system: data.system,
                "prototypeToken.bar1": {{ attribute: "resources.hitPoints" }},
                "prototypeToken.bar2": {{ attribute: "resources.stress" }},
                "prototypeToken.displayBars": 40,
                "prototypeToken.displayName": 20
            }}).catch(e => console.warn("Actor update note:", e));

            // Purge old items & effects so attacks/features always reflect latest macro data
            const oldItemIds = existing.items.map(i => i.id);
            if (oldItemIds.length > 0) {{
                await existing.deleteEmbeddedDocuments("Item", oldItemIds).catch(e => console.warn("Item deletion note:", e));
            }}
            const oldEffectIds = existing.effects.map(e => e.id);
            if (oldEffectIds.length > 0) {{
                await existing.deleteEmbeddedDocuments("ActiveEffect", oldEffectIds).catch(e => console.warn("Effect deletion note:", e));
            }}
        }}

        // Populates Daggerheart Features Tab (Item Documents), Attacks & Effects Tab (ActiveEffects)
        if (existing) {{
            const itemsToCreate = [];

            // 1. Primary Attack — use Daggerheart "feature" type (weapon schema incompatible; feature confirmed working)
            if (data.attack) {{
                itemsToCreate.push({{
                    name: data.attack.name,
                    type: "feature",
                    img: data.attack.img,
                    system: {{
                        description: `<p><strong>⚔️ Attack:</strong> ${{data.attack.type}} | <strong>${{data.attack.damage}}</strong> damage (${{data.attack.modifier >= 0 ? '+' : ''}}${{data.attack.modifier}} to Hit)</p><p>${{data.attack.description}}</p>`
                    }}
                }});
            }}

            // 2. Features
            if (data.features && data.features.length > 0) {{
                for (let f of data.features) {{
                    itemsToCreate.push({{
                        name: f.name,
                        type: defaultItemType,
                        img: f.img,
                        system: {{ description: f.description }}
                    }});
                }}
            }}

            if (itemsToCreate.length > 0) {{
                await existing.createEmbeddedDocuments("Item", itemsToCreate).catch(e => console.warn("Item creation note:", e));
            }}

            // 3. Active Effects
            if (data.effects && data.effects.length > 0) {{
                const effectsToCreate = data.effects.map(e => ({{
                    name: e.name,
                    label: e.name,
                    icon: e.icon,
                    disabled: false,
                    description: e.description
                }}));
                await existing.createEmbeddedDocuments("ActiveEffect", effectsToCreate).catch(e => console.warn("ActiveEffect creation note:", e));
            }}
        }}
    }}

    // ── 3. Create Dedicated Scene Folder & 3 Battle Map Scenes ────────────────
    let sceneFolder = game.folders.find(f => f.name === "Session 10 - Battle Maps" && f.type === "Scene");
    if (!sceneFolder) {{
        sceneFolder = await Folder.create({{ name: "Session 10 - Battle Maps", type: "Scene" }});
    }}

    // Fetch Actor document IDs so we can pin exact creature notes/sheets onto each map scene!
    const actorChui = game.actors.find(a => a.name === "Mwaza-Chui (Memory Jaguar)");
    const actorWyrm = game.actors.find(a => a.name === "Gale-Wyrm");
    const actorCat = game.actors.find(a => a.name === "Stunted Canopy Cat");
    const actorShark = game.actors.find(a => a.name === "Dagger Shark");
    const actorRill = game.actors.find(a => a.name === "Rill (Combat Aide)");
    const actorBramble = game.actors.find(a => a.name === "Bramble");

    const scenesToCreate = [
        {{
            name: "Zone 0 & 8 - Walker Core Breach (Nordic Pine Ridge)",
            folder: sceneFolder.id,
            imgPath: MAP_WALKER,
            width: 2000,
            height: 2000,
            grid: {{ size: 100, type: 1 }},
            tokenVision: true,
            globalLight: false,
            darkness: 0.65,
            lights: [
                {{
                    x: 1000,
                    y: 400,
                    config: {{ dim: 80, bright: 25, color: "#7722cc", alpha: 0.15, animation: {{ type: "pulse", speed: 2, intensity: 2 }} }}
                }},
                {{
                    x: 400,
                    y: 500,
                    config: {{ dim: 60, bright: 20, color: "#4477ee", alpha: 0.12, animation: {{ type: "swirling", speed: 2, intensity: 2 }} }}
                }},
                {{
                    x: 1500,
                    y: 1400,
                    config: {{ dim: 70, bright: 20, color: "#0088bb", alpha: 0.12, animation: {{ type: "pulse", speed: 2, intensity: 2 }} }}
                }}
            ],
            notes: [
                {{
                    x: 600,
                    y: 300,
                    entryId: dmJournal.id,
                    pageId: p6_id,
                    texture: {{ src: "icons/svg/book.svg" }},
                    icon: "icons/svg/book.svg",
                    iconSize: 44,
                    text: "⚡ Scene 1 DM Guide: Establishing Shot, Beast Descriptions & Counts (1x Mwaza-Chui, 2x Cats)"
                }},
                {{
                    x: 800,
                    y: 400,
                    entryId: dmJournal.id,
                    pageId: p4_id,
                    texture: {{ src: "icons/svg/hazard.svg" }},
                    icon: "icons/svg/hazard.svg",
                    iconSize: 44,
                    text: "🗺️ Zone 0/8 Encounter Table: Mwaza-Chui (x1) + Canopy Cats (x2) | GM Fear Options"
                }},
                {{
                    x: 1000,
                    y: 400,
                    entryId: actorChui ? actorChui.id : dmJournal.id,
                    pageId: actorChui ? null : p2_id,
                    texture: {{ src: "icons/svg/target.svg" }},
                    icon: "icons/svg/target.svg",
                    iconSize: 48,
                    text: "🐆 Mwaza-Chui (Memory Jaguar Boss x1): Shadowfang Signal Pounce & Decoy Tactics"
                }},
                {{
                    x: 1300,
                    y: 550,
                    entryId: actorCat ? actorCat.id : dmJournal.id,
                    pageId: actorCat ? null : p2_id,
                    texture: {{ src: "icons/svg/combat.svg" }},
                    icon: "icons/svg/combat.svg",
                    iconSize: 40,
                    text: "🐱 Stunted Canopy Cats (Minion Swarm x2): Canopy Ambush Shred"
                }}
            ]
        }},
        {{
            name: "Zone 1 & 3 - Nordic Pine Forest Rescue",
            folder: sceneFolder.id,
            imgPath: MAP_PINE,
            width: 2000,
            height: 2000,
            grid: {{ size: 100, type: 1 }},
            tokenVision: true,
            globalLight: false,
            darkness: 0.35,
            lights: [
                {{
                    x: 1000,
                    y: 1000,
                    config: {{ dim: 80, bright: 25, color: "#1a4d4d", alpha: 0.12, animation: {{ type: "pulse", speed: 2, intensity: 2 }} }}
                }},
                {{
                    x: 600,
                    y: 500,
                    config: {{ dim: 60, bright: 20, color: "#2d6666", alpha: 0.12, animation: {{ type: "sunburst", speed: 2, intensity: 2 }} }}
                }},
                {{
                    x: 1400,
                    y: 1300,
                    config: {{ dim: 60, bright: 20, color: "#ffaa33", alpha: 0.15, animation: {{ type: "torch", speed: 2, intensity: 2 }} }}
                }}
            ],
            notes: [
                {{
                    x: 500,
                    y: 500,
                    entryId: dmJournal.id,
                    pageId: p7_id,
                    texture: {{ src: "icons/svg/book.svg" }},
                    icon: "icons/svg/book.svg",
                    iconSize: 44,
                    text: "🌲 Scene 2 DM Guide: Establishing Shot, Beast Descriptions & Counts (1x Gale-Wyrm, 3x Cats)"
                }},
                {{
                    x: 700,
                    y: 500,
                    entryId: dmJournal.id,
                    pageId: p4_id,
                    texture: {{ src: "icons/svg/hazard.svg" }},
                    icon: "icons/svg/hazard.svg",
                    iconSize: 44,
                    text: "🗺️ Zone 1/3 Encounter Table: Gale-Wyrm (x1) + Canopy Cats (x3) | Low Visibility Rain"
                }},
                {{
                    x: 1000,
                    y: 600,
                    entryId: actorWyrm ? actorWyrm.id : dmJournal.id,
                    pageId: actorWyrm ? null : p2_id,
                    texture: {{ src: "icons/svg/upgrade.svg" }},
                    icon: "icons/svg/upgrade.svg",
                    iconSize: 48,
                    text: "🐲 Gale-Wyrm (Apex Aerostatic Dragon x1): Gravity Core Cataclysm & Gravity Reversal"
                }},
                {{
                    x: 1300,
                    y: 750,
                    entryId: actorCat ? actorCat.id : dmJournal.id,
                    pageId: actorCat ? null : p2_id,
                    texture: {{ src: "icons/svg/combat.svg" }},
                    icon: "icons/svg/combat.svg",
                    iconSize: 40,
                    text: "🐱 Stunted Canopy Cats (Minion Swarm x3): Canopy Ambush Shred"
                }},
                {{
                    x: 1200,
                    y: 1400,
                    entryId: actorBramble ? actorBramble.id : dmJournal.id,
                    pageId: actorBramble ? null : p3_id,
                    texture: {{ src: "icons/svg/oak.svg" }},
                    icon: "icons/svg/oak.svg",
                    iconSize: 40,
                    text: "🪵 Squad 06 Rescue: Bramble (Root Wall Tank) & Rill Support"
                }}
            ]
        }},
        {{
            name: "Zone 5 - Fortified Canyon Camp (Estuary Siege)",
            folder: sceneFolder.id,
            imgPath: MAP_CAMP,
            width: 2000,
            height: 2000,
            grid: {{ size: 100, type: 1 }},
            tokenVision: true,
            globalLight: false,
            darkness: 0.55,
            lights: [
                {{
                    x: 1000,
                    y: 1000,
                    config: {{ dim: 80, bright: 25, color: "#ff7722", alpha: 0.15, animation: {{ type: "torch", speed: 2, intensity: 2 }} }}
                }},
                {{
                    x: 500,
                    y: 1500,
                    config: {{ dim: 60, bright: 20, color: "#cc4400", alpha: 0.12, animation: {{ type: "pulse", speed: 2, intensity: 2 }} }}
                }},
                {{
                    x: 1600,
                    y: 500,
                    config: {{ dim: 60, bright: 20, color: "#009999", alpha: 0.12, animation: {{ type: "ghostly", speed: 2, intensity: 2 }} }}
                }}
            ],
            notes: [
                {{
                    x: 700,
                    y: 800,
                    entryId: dmJournal.id,
                    pageId: p8_id,
                    texture: {{ src: "icons/svg/book.svg" }},
                    icon: "icons/svg/book.svg",
                    iconSize: 44,
                    text: "🦈 Scene 3 DM Guide: Establishing Shot, Beast Descriptions & Counts (1x Chui, 4x Sharks, 3x Cats)"
                }},
                {{
                    x: 900,
                    y: 800,
                    entryId: dmJournal.id,
                    pageId: p5_id,
                    texture: {{ src: "icons/svg/hazard.svg" }},
                    icon: "icons/svg/hazard.svg",
                    iconSize: 44,
                    text: "🗺️ Zone 5 Encounter Table: Mwaza-Chui (x1) + Dagger Sharks (x4) + Cats (x3) | Estuary Siege"
                }},
                {{
                    x: 1400,
                    y: 600,
                    entryId: actorChui ? actorChui.id : dmJournal.id,
                    pageId: actorChui ? null : p2_id,
                    texture: {{ src: "icons/svg/target.svg" }},
                    icon: "icons/svg/target.svg",
                    iconSize: 48,
                    text: "🐆 Mwaza-Chui (Memory Jaguar Boss x1): Relentless Mind-Link Hunt"
                }},
                {{
                    x: 600,
                    y: 1400,
                    entryId: actorShark ? actorShark.id : dmJournal.id,
                    pageId: actorShark ? null : p2_id,
                    texture: {{ src: "icons/svg/skull.svg" }},
                    icon: "icons/svg/skull.svg",
                    iconSize: 44,
                    text: "🦈 Dagger Sharks (Aquatic Shock Troops x4): Vortical Pressure Snap & Mud Drag"
                }},
                {{
                    x: 1000,
                    y: 1100,
                    entryId: actorRill ? actorRill.id : dmJournal.id,
                    pageId: actorRill ? null : p3_id,
                    texture: {{ src: "icons/svg/shield.svg" }},
                    icon: "icons/svg/shield.svg",
                    iconSize: 40,
                    text: "🌊 Rill's Aether Jammer & Session 9 Scrap Fortification Matrix"
                }}
            ]
        }},
        {{
            name: "Zone 1 & 3 - Granite Canyon Basin (Generic)",
            folder: sceneFolder.id,
            imgPath: MAP_WETLAND,
            width: 2000,
            height: 2000,
            grid: {{ size: 100, type: 1 }},
            tokenVision: true,
            globalLight: false,
            darkness: 0.40,
            lights: [
                {{
                    x: 1000,
                    y: 1000,
                    config: {{ dim: 80, bright: 25, color: "#1a4d4d", alpha: 0.12, animation: {{ type: "pulse", speed: 2, intensity: 2 }} }}
                }},
                {{
                    x: 500,
                    y: 1400,
                    config: {{ dim: 60, bright: 20, color: "#2d6666", alpha: 0.12, animation: {{ type: "sunburst", speed: 2, intensity: 2 }} }}
                }}
            ],
            notes: [
                {{
                    x: 500,
                    y: 500,
                    entryId: dmJournal.id,
                    pageId: p9_id,
                    texture: {{ src: "icons/svg/book.svg" }},
                    icon: "icons/svg/book.svg",
                    iconSize: 44,
                    text: "⛰️ Scene 2B DM Guide: Granite Canyon Basin — Establishing Shot, Beast Descriptions & Counts (1x Gale-Wyrm, 3x Cats)"
                }},
                {{
                    x: 700,
                    y: 500,
                    entryId: dmJournal.id,
                    pageId: p4_id,
                    texture: {{ src: "icons/svg/hazard.svg" }},
                    icon: "icons/svg/hazard.svg",
                    iconSize: 44,
                    text: "🗺️ Zone 1/3 Encounter Table: Gale-Wyrm (x1) + Canopy Cats (x3) | Low Visibility Mist"
                }},
                {{
                    x: 1000,
                    y: 600,
                    entryId: actorWyrm ? actorWyrm.id : dmJournal.id,
                    pageId: actorWyrm ? null : p2_id,
                    texture: {{ src: "icons/svg/upgrade.svg" }},
                    icon: "icons/svg/upgrade.svg",
                    iconSize: 48,
                    text: "🐲 Gale-Wyrm (Apex Aerostatic Dragon x1): Gravity Core Cataclysm & Rockfall"
                }},
                {{
                    x: 1300,
                    y: 750,
                    entryId: actorCat ? actorCat.id : dmJournal.id,
                    pageId: actorCat ? null : p2_id,
                    texture: {{ src: "icons/svg/combat.svg" }},
                    icon: "icons/svg/combat.svg",
                    iconSize: 40,
                    text: "🐱 Stunted Canopy Cats (Minion Swarm x3): Cliff-Edge Pounce"
                }},
                {{
                    x: 1200,
                    y: 1400,
                    entryId: actorBramble ? actorBramble.id : dmJournal.id,
                    pageId: actorBramble ? null : p3_id,
                    texture: {{ src: "icons/svg/oak.svg" }},
                    icon: "icons/svg/oak.svg",
                    iconSize: 40,
                    text: "🪵 Squad 06 Rescue: Bramble (Root Wall Tank) & Rill Support"
                }}
            ]
        }},
        {{
            name: "Zone 5 - Basalt Canyon Defiles (Generic)",
            folder: sceneFolder.id,
            imgPath: MAP_CAMP,
            width: 2000,
            height: 2000,
            grid: {{ size: 100, type: 1 }},
            tokenVision: true,
            globalLight: false,
            darkness: 0.55,
            lights: [
                {{
                    x: 1000,
                    y: 1000,
                    config: {{ dim: 80, bright: 25, color: "#ff7722", alpha: 0.15, animation: {{ type: "torch", speed: 2, intensity: 2 }} }}
                }},
                {{
                    x: 600,
                    y: 1400,
                    config: {{ dim: 60, bright: 20, color: "#009999", alpha: 0.12, animation: {{ type: "ghostly", speed: 2, intensity: 2 }} }}
                }}
            ],
            notes: [
                {{
                    x: 700,
                    y: 800,
                    entryId: dmJournal.id,
                    pageId: p10_id,
                    texture: {{ src: "icons/svg/book.svg" }},
                    icon: "icons/svg/book.svg",
                    iconSize: 44,
                    text: "🏜️ Scene 3B DM Guide: Basalt Canyon Defiles — Establishing Shot, Beast Descriptions & Counts (1x Chui, 4x Sharks, 3x Cats)"
                }},
                {{
                    x: 900,
                    y: 800,
                    entryId: dmJournal.id,
                    pageId: p5_id,
                    texture: {{ src: "icons/svg/hazard.svg" }},
                    icon: "icons/svg/hazard.svg",
                    iconSize: 44,
                    text: "🗺️ Zone 5 Encounter Table: Mwaza-Chui (x1) + Dagger Sharks (x4) + Cats (x3) | Canyon Siege"
                }},
                {{
                    x: 1400,
                    y: 600,
                    entryId: actorChui ? actorChui.id : dmJournal.id,
                    pageId: actorChui ? null : p2_id,
                    texture: {{ src: "icons/svg/target.svg" }},
                    icon: "icons/svg/target.svg",
                    iconSize: 48,
                    text: "🐆 Mwaza-Chui (Memory Jaguar Boss x1): Canyon Rim Stalker"
                }},
                {{
                    x: 600,
                    y: 1400,
                    entryId: actorShark ? actorShark.id : dmJournal.id,
                    pageId: actorShark ? null : p2_id,
                    texture: {{ src: "icons/svg/skull.svg" }},
                    icon: "icons/svg/skull.svg",
                    iconSize: 44,
                    text: "🦈 Dagger Sharks (Aquatic Shock Troops x4): Silt Trench Snap & Mud Drag"
                }},
                {{
                    x: 1000,
                    y: 1100,
                    entryId: actorRill ? actorRill.id : dmJournal.id,
                    pageId: actorRill ? null : p3_id,
                    texture: {{ src: "icons/svg/shield.svg" }},
                    icon: "icons/svg/shield.svg",
                    iconSize: 40,
                    text: "🌊 Rill's Aether Jammer & Canyon Palisade Defenses"
                }}
            ]
        }}
    ];

    for (let sData of scenesToCreate) {{
        let existing = game.scenes.find(s => s.name === sData.name);
        const sceneData = {{
            name: sData.name,
            folder: sData.folder,
            background: {{ src: sData.imgPath }},
            img: sData.imgPath,
            width: sData.width,
            height: sData.height,
            grid: sData.grid,
            tokenVision: sData.tokenVision,
            globalLight: sData.globalLight,
            darkness: sData.darkness
        }};

        if (!existing) {{
            existing = await Scene.create(sceneData);
        }} else {{
            await existing.update(sceneData).catch(e => console.warn("Scene update note:", e));

            // Clean purge of old lights & note pins to guarantee updated creature pins
            const oldLightIds = existing.lights.map(l => l.id);
            if (oldLightIds.length > 0) {{
                await existing.deleteEmbeddedDocuments("AmbientLight", oldLightIds).catch(e => console.warn("Light deletion note:", e));
            }}
            const oldNoteIds = existing.notes.map(n => n.id);
            if (oldNoteIds.length > 0) {{
                await existing.deleteEmbeddedDocuments("Note", oldNoteIds).catch(e => console.warn("Note deletion note:", e));
            }}
        }}

        // Add Ambient Lighting if specified
        if (sData.lights) {{
            await existing.createEmbeddedDocuments("AmbientLight", sData.lights).catch(e => console.warn("Lighting note:", e));
        }}

        // Add Journal Notes Pins & Creature Actor Pins to Scene
        if (sData.notes) {{
            const noteDocs = sData.notes.map(n => ({{
                x: n.x,
                y: n.y,
                entryId: n.entryId,
                pageId: n.pageId,
                texture: n.texture,
                icon: n.icon,
                iconSize: n.iconSize,
                text: n.text
            }}));
            await existing.createEmbeddedDocuments("Note", noteDocs).catch(e => console.warn("Notes note:", e));
        }}
    }}

    ui.notifications.info(`🚀 Vumbua Session 10: Features, Active Effects, Notes, Battle Maps & Actors fully loaded into Daggerheart!`);
}})();
"""

with open(OUT_JS_1, 'w', encoding='utf-8') as f:
    f.write(js_template)

with open(OUT_JS_2, 'w', encoding='utf-8') as f:
    f.write(js_template)

print("Macro with Daggerheart Features, Active Effects, and Notes compiled successfully!")
