import base64
import os
import io
from PIL import Image, ImageDraw

def get_b64(path, border_color=(255, 255, 255), border_width=6):
    try:
        im = Image.open(path).convert("RGBA")
        
        # Center-crop to a perfect square to prevent squishing
        width, height = im.size
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        right = (width + min_dim) // 2
        bottom = (height + min_dim) // 2
        im = im.crop((left, top, right, bottom))
        
        # Resize to 150x150
        size = (150, 150)
        im = im.resize(size, Image.Resampling.LANCZOS)
        
        # Create circular mask
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        
        # Create new image with transparent background
        output = Image.new("RGBA", size, (0, 0, 0, 0))
        output.paste(im, (0, 0), mask=mask)
        
        # Draw the colored border ring inside the circular edge
        if border_width > 0:
            draw_border = ImageDraw.Draw(output)
            offset = border_width // 2
            draw_border.ellipse(
                (offset, offset, size[0] - offset, size[1] - offset),
                outline=border_color,
                width=border_width
            )
        
        buffer = io.BytesIO()
        output.save(buffer, format='WEBP', quality=85)
        return 'data:image/webp;base64,' + base64.b64encode(buffer.getvalue()).decode('ascii')
    except Exception as e:
        print(f"Error compressing {path}: {e}")
        with open(path, 'rb') as f:
            return 'data:image/png;base64,' + base64.b64encode(f.read()).decode('ascii')

p1 = r'C:\Users\ldstr\.gemini\antigravity-ide\brain\206a4965-28e5-4ab2-9975-e76d89eded50\storm_raptor_portrait_1785601052423.png'
p2 = r'C:\Users\ldstr\.gemini\antigravity-ide\brain\206a4965-28e5-4ab2-9975-e76d89eded50\ember_warg_portrait_1785601061667.png'
p3 = r'C:\Users\ldstr\.gemini\antigravity-ide\brain\206a4965-28e5-4ab2-9975-e76d89eded50\pyre_lynx_portrait_1785601071956.png'

b1 = get_b64(p1, border_color=(51, 102, 204), border_width=6)   # Cyan-Blue ring for Storm Raptor
b2 = get_b64(p2, border_color=(204, 51, 51), border_width=6)    # Red ring for Ember Warg
b3 = get_b64(p3, border_color=(255, 153, 0), border_width=6)    # Gold/Amber ring for Pyre Lynx

macro_template = f"""/**
 * Foundry VTT Macro: The Tempest Clearing & Gondola Encounter (WITH EMBEDDED ARTWORK & WORKING ATTACKS)
 * System Compatibility: Daggerheart (1.6.1+) & Foundry VTT v10 / v11 / v12
 * 
 * INCLUDES:
 * 1. Native Clickable Primary Attack Cards (Targetable & Rollable directly on the Adversary Sheet)!
 * 2. Embedded Base64 Portrait Art for all 3 NPCs!
 * 3. Master DM Journal Entry ("The Tempest Clearing & Gondola Encounter") with 3 Pages:
 *    - Environment Stat Block (Tier 3 Traversal/Event, Dynamic Countdown 8, Passives, Actions & Reactions)
 *    - Adversary Roster & Stat Sheets Summary with Embedded Artwork
 *    - 3-Phase Tactical DM Running Guide (The Descent, Rope Swarm, Warg Snare)
 * 4. 3 Fully Formatted Daggerheart NPC Actors in "Adversaries & Allies" folder:
 *    - Storm Raptor (Tier 3 Skulk)
 *    - Ember Warg (Tier 3 Standard / Bruiser)
 *    - Pyre Lynx (Tier 3 Minion)
 */

(async () => {{
    ui.notifications.info("Executing Tempest Clearing & Gondola Macro with Native Attacks...");

    const IMG_RAPTOR = "{b1}";
    const IMG_WARG = "{b2}";
    const IMG_LYNX = "{b3}";

    // ── 1. Create Dedicated Journal Folder & Master Journal Entry ─────────────
    let journalFolder = game.folders.find(f => f.name === "Encounter DM Guides" && f.type === "JournalEntry");
    if (!journalFolder) {{
        journalFolder = await Folder.create({{ name: "Encounter DM Guides", type: "JournalEntry" }});
    }}

    const envPageContent = `
        <h2>🌪️ ENVIRONMENT: THE TEMPEST CLEARING</h2>
        <p><strong>Tier:</strong> 3 (Traversal) | <strong>Difficulty Benchmark:</strong> 17</p>
        <p><strong>Description:</strong> A high-altitude basalt clearing above the Mizizi canopy where storm winds batter Squad 907's Canopy Raft.</p>
        <p><strong>Impulses:</strong> Pitch the deck, pull targets overboard, snap tethers.</p>
        <p><strong>Potential Adversaries:</strong> Storm Raptors (Skulks), Ember Wargs (Bruisers), Pyre Lynxes (Minions).</p>
        
        <hr/>

        <h3>⚙️ Passive Features</h3>
        <ul>
          <li><strong>Gondola Equilibrium (Dynamic Countdown 8):</strong> 
            <br/>The Canopy Raft must stay centered in the clear eye. Every action roll with Fear ticks this down by 1. 
            <br/>When it reaches 0, the deck pitches violently into the violent eyewall: all PCs must make an <strong>Agility Reaction Roll (17)</strong> or take <strong>3d8+5 physical damage</strong> and become <strong>Vulnerable</strong> as they hang over the buoyancy barrels. 
            <br/>A PC can spend an action with an <strong>Agility or Finesse Roll (17)</strong> to stabilize the ropes and tick the countdown back up by 2.
          </li>
          <li style="margin-top:8px;"><strong>Vertical Line of Sight:</strong> 
            <br/>Enemies in the air are at <strong>Far Range</strong> vertically. Enemies on the forest floor are at <strong>Very Far Range</strong> below. 
            <br/>Shifting the raft's height closer to the treetops puts the deck within <strong>Close Range</strong> of ground attacks.
          </li>
        </ul>

        <hr/>

        <h3>🔥 GM Actions & Reactions</h3>
        <ul>
          <li><strong>Hurricane Gale (Action — 1 Fear):</strong> 
            <br/>Spend a Fear. A gust of wind sweeps across the deck. All creatures on the raft must make a <strong>Strength Reaction Roll (17)</strong>. On a failure, they are knocked <strong>Restrained</strong> in the rigging or pushed to the edge.
          </li>
          <li style="margin-top:8px;"><strong>Snagged Anchor (Reaction — Triggered on Failure w/ Fear):</strong> 
            <br/>When a player rolls a Failure with Fear, the raft's trailing steel cable snags on the petrified treetops, jerking the platform. Anyone not anchored takes <strong>2 Stress</strong> and drops whatever they are holding.
          </li>
        </ul>

        <hr/>

        <h3>⏱️ Progress Tracking: The Dawn Survival Clock</h3>
        <ul>
          <li><strong>Dawn Survival Clock (Countdown 8):</strong>
            <br/>A progress clock tracking the hours remaining until dawn. Tick down (advance) this clock when PCs make action rolls to defend or stabilize:
            <br/>• <strong>Critical Success</strong>: Tick down 3.
            <br/>• <strong>Success with Hope</strong>: Tick down 2.
            <br/>• <strong>Success with Fear</strong>: Tick down 1.
            <br/>• <strong>Failure</strong>: No progress ticks.
            <br/>Dawn arrives and the storm subsides when the countdown reaches 0, signaling the arrival of the sector evac vessel.
          </li>
        </ul>

        <hr/>

        <h3>⚠️ Complications & Hooks</h3>
        <ul>
          <li><strong>Miz-Tortoise Rescue (Active Event):</strong>
            <br/>A sacred moss-backed tortoise is trapped on a canopy branch below, getting attacked by Ember Wargs. A PC can spend an action to pull it onto the deck with a <strong>Strength or Finesse roll (17)</strong>. Rescuing it grants the raft a permanent <strong>+1 Evasion/Armor blessing</strong>.
          </li>
          <li style="margin-top:8px;"><strong>Bramble's Cry (Triggered Event):</strong>
            <br/>At the start of Wave 2, Bramble (the giant ancient tree-man) reaches out telepathically to Aggie (or whoever spoke to the forest), trapped by Pyre Lynxes in the canopy foliage. Rescuing him requires a <strong>Finesse/Agility roll (17)</strong> to swat the minions. Rescuing Bramble secures his aid in lashing the cables (+2 to Gondola Equilibrium stabilization rolls).
          </li>
        </ul>

        <hr/>

        <h3>❓ Feature Questions</h3>
        <ol>
          <li>How does the rain slicking the deck affect the characters' grip on their weapons?</li>
          <li>What cargo inside the gondola shifts and breaks loose as the deck tilts?</li>
          <li>Whose personal keepsake falls over the edge into the abyss during the first wind shear?</li>
        </ol>
    `;

    const rosterPageContent = `
        <h2>⚔️ Adversary Roster & Stat Sheets (Tier 3 / 17 Battle Points)</h2>
        <p><em>Balanced for a Tier 3 / Level 5 hard encounter (5 PCs).</em></p>

        <hr/>

        <div style="display:flex; gap:12px; margin-bottom:15px;">
          <img src="${{IMG_RAPTOR}}" style="width:120px; height:120px; border-radius:8px; object-fit:cover; border:2px solid #3366cc;"/>
          <div>
            <h3>🦅 Storm Raptor (2x Aerial Skulks — 4 BP Total)</h3>
            <ul>
              <li><strong>Role:</strong> Tier 3 Skulk (2 Points each) | <strong>Difficulty:</strong> 14 (17 while flying) | <strong>Evasion:</strong> 14</li>
              <li><strong>HP:</strong> 5 | <strong>Stress:</strong> 3 | <strong>Damage Thresholds:</strong> Minor 16 | Major 30</li>
              <li><strong>Attack:</strong> <strong>Claws & Beak</strong> (Melee, +2 to Hit | <strong>2d6+7</strong> physical damage)</li>
              <li><strong>Flying (Passive)</strong>: Difficulty is 17 while flying.</li>
              <li><strong>Screech (Action)</strong>: Mark 1 Stress to force 1d4 Stress on all targets in front up to Far range.</li>
              <li><strong>Snatch & Pitch (Action)</strong>: Spend 1 Fear on hit to drag a PC over the edge (Restrained over open air).</li>
            </ul>
          </div>
        </div>

        <hr/>

        <div style="display:flex; gap:12px; margin-bottom:15px;">
          <img src="${{IMG_WARG}}" style="width:120px; height:120px; border-radius:8px; object-fit:cover; border:2px solid #cc3333;"/>
          <div>
            <h3>🐺 Ember Warg (3x Forest Floor Heavy Hitters — 12 BP Total)</h3>
            <ul>
              <li><strong>Role:</strong> Tier 3 Bruiser (4 Points each) | <strong>Difficulty:</strong> 17 | <strong>Evasion:</strong> 17</li>
              <li><strong>HP:</strong> 6 | <strong>Stress:</strong> 4 | <strong>Damage Thresholds:</strong> Minor 18 | Major 35</li>
              <li><strong>Attack:</strong> <strong>Fiery Jaws</strong> (Close, +4 to Hit | <strong>3d8+3</strong> physical/magic damage)</li>
              <li><strong>Leaping Ambush (Action)</strong>: If raft drops to Close range of canopy, leap onto rim, deal attack damage and make target Vulnerable.</li>
              <li><strong>Flame Breath (Action)</strong>: Spend 1 Fear to spew embers upward at balloon (Close line, 3d6+4 magic damage; envelope hit reduces Gondola Equilibrium by 2).</li>
            </ul>
          </div>
        </div>

        <hr/>

        <div style="display:flex; gap:12px; margin-bottom:15px;">
          <img src="${{IMG_LYNX}}" style="width:120px; height:120px; border-radius:8px; object-fit:cover; border:2px solid #ff9900;"/>
          <div>
            <h3>🐱 Pack of Pyre Lynxes (1x Ground Swarm — 1 BP Total)</h3>
            <ul>
              <li><strong>Role:</strong> Tier 3 Minions (1 Point for a group of 5) | <strong>Difficulty:</strong> 15 | <strong>Evasion:</strong> 15</li>
              <li><strong>HP:</strong> 1 | <strong>Stress:</strong> 1 | <strong>Damage Thresholds:</strong> None</li>
              <li><strong>Attack:</strong> <strong>Infernal Pounce</strong> (Melee, +0 to Hit | <strong>5</strong> magic damage)</li>
              <li><strong>Minion (9) (Passive)</strong>: Defeated on taking any damage. Every 9 damage dealt by AoE/multi-target attack defeats an additional Lynx in range.</li>
              <li><strong>Group Attack (Action)</strong>: Spend 1 Fear to spotlight all Pyre Lynxes. They swarm up the ropes and make one shared attack roll. On success, deal 5 magic damage each (combined).</li>
            </ul>
          </div>
        </div>
    `;

    const guidePageContent = `
        <h2>🧭 How to Run the Scene (The Tactical Loop)</h2>
        
        <blockquote>
          <strong>Sight</strong>: Churning indigo static clouds arcing violet lightning across walker-core legs. The Canopy Raft tilts precariously, anchored by steel cable to a towering 80-foot petrified branch.<br/>
          <strong>Sound</strong>: The shriek of gale-force winds shearing the canvas; the low, supercharged roar of Natty's sulfur burner; splash of fins snapping in the basin below.<br/>
          <strong>Smell</strong>: Ozone, wet stone-bark, and the sharp scent of raw sulfur crystals.<br/>
          <strong>Atmosphere</strong>: A freezing rain slicking the wooden deck; the adrenaline-spiked realization that the sector barriers are gone.<br/><br/>
          <em>"Huddled in the canopy raft, you hear a screech rip through the wind from above. Two metal-feathered Storm Raptors dive out of the eyewall, while below, shadow-like Ember Wargs begin bounding up the stone trunk toward your anchor lines..."</em>
        </blockquote>

        <h3>⚔️ Wave Breakdown & Flow</h3>
        <ol style="line-height:1.6;">
          <li>
            <strong>Wave 1: The Canopy Ambush (Range: Far/Close)</strong>
            <br/>The <strong>Storm Raptors</strong> hit first from the sky (Far range), attempting to drag players over the side, while a pack of <strong>Pyre Lynxes</strong> scrambles up the tethers. 
            <br/><em>Complication</em>: The <strong>Miz-Tortoise</strong> is spotted on a canopy branch below. The Wargs are attacking it.
          </li>
          <li style="margin-top:12px;">
            <strong>Wave 2: The Heavy Assault (Range: Melee)</strong>
            <br/>The raft sways closer to the branches as the burner fluctuates. 3x <strong>Ember Wargs</strong> leap onto the buoyancy-barrel deck.
            <br/><em>Complication</em>: <strong>Bramble</strong> reaches out telepathically to Aggie, overwhelmed by minions in the foliage.
          </li>
        </ol>

        <hr/>

        <h3>🧠 Tactics & GM Running Advice</h3>
        <ul>
          <li><strong>Storm Raptors</strong>: Hover at Far range, diving to use <em>Snatch & Pitch</em>. Target high-Evasion PCs to isolate them. Morale: Flee if reduced to 1 HP.</li>
          <li><strong>Ember Wargs</strong>: Scale the petrified trunks. Leap onto the deck and target the burner. Morale: Retreat down the trunk if reduced to 1 HP.</li>
          <li><strong>Pyre Lynxes</strong>: Minion swarms, climbing anchor lines. Use <em>Group Attack</em> to swarm and distract.</li>
        </ul>

        <hr/>

        <h3>⚠️ Campaign-Specific Hazards & Traumas</h3>
        <ul>
          <li><strong>Iggy's Tree Phobia</strong>: Iggy is terrified of the petrified forest. If Iggy makes an action roll to climb the rigging or look down, he has Disadvantage unless an ally spends 1 Hope to reassure him.</li>
          <li><strong>The Dagger Shark Fall</strong>: If a player is snatched and pitched overboard, they fall 30 feet into the water basin. Direct falling damage is 1d20+5 physical (SRD p. 69), and they enter Melee range of the tracking Dagger Sharks.</li>
        </ul>
    `;

    const remindersPageContent = `
        <h2>🧠 Running DM Reminders (SRD Quick Ref)</h2>
        
        <h3>🎲 Duality Action Roll Quick Reference</h3>
        <ul>
          <li><strong>Success with Hope</strong>: Action succeeds. Gain 1 Hope.</li>
          <li><strong>Success with Fear</strong>: Action succeeds with a cost/complication. GM gains 1 Fear.</li>
          <li><strong>Failure with Hope</strong>: Action fails. Gain 1 Hope. Spotlight swings to GM.</li>
          <li><strong>Failure with Fear</strong>: Action fails with a major consequence. GM gains 1 Fear. Spotlight swings to GM.</li>
          <li><strong>Critical Success (Matching Dice)</strong>: Automatic success with a bonus. Gain 1 Hope + clear 1 Stress. Deals critical damage.</li>
        </ul>

        <hr/>

        <h3>📢 GM Spotlight Shifting Triggers</h3>
        <ul>
          <li>Reminder that spotlight shifts to the GM on any PC action roll failure or when the narrative dictates.</li>
        </ul>

        <hr/>

        <h3>🔥 GM Fear Spent Cheat Sheet</h3>
        <ul>
          <li><strong>Spend 1 Fear to</strong>:
            <br/>• Interrupt players to steal the spotlight.
            <br/>• Make an additional GM move.
            <br/>• Activate an adversary's Fear feature (e.g. *Snatch & Pitch*, *Flame Breath*, *Group Attack*).
            <br/>• Activate an environment's Fear feature (e.g. *Hurricane Gale*).
            <br/>• Add an adversary's Experience to a roll.
          </li>
        </ul>
    `;

    const masterPages = [
        {{ name: "🌪️ Environment: The Tempest Clearing", type: "text", text: {{ content: envPageContent, format: 1 }} }},
        {{ name: "⚔️ Adversary Roster & Stat Sheets", type: "text", text: {{ content: rosterPageContent, format: 1 }} }},
        {{ name: "🧭 How to Run the Scene (Tactical Loop)", type: "text", text: {{ content: guidePageContent, format: 1 }} }},
        {{ name: "🧠 Running DM Reminders", type: "text", text: {{ content: remindersPageContent, format: 1 }} }}
    ];

    let dmJournal = game.journal.find(j => j.name === "The Tempest Clearing & Gondola Encounter" && (j.folder?.id === journalFolder.id || j.folder === journalFolder.id));
    if (!dmJournal) {{
        dmJournal = await JournalEntry.create({{
            name: "The Tempest Clearing & Gondola Encounter",
            folder: journalFolder.id,
            pages: masterPages
        }});
        ui.notifications.info("Created Journal Entry: The Tempest Clearing & Gondola Encounter");
    }} else {{
        for (let pData of masterPages) {{
            let existingP = dmJournal.pages.find(p => p.name === pData.name);
            if (!existingP) {{
                await dmJournal.createEmbeddedDocuments("JournalEntryPage", [pData]).catch(e => console.warn("Page note:", e));
            }} else {{
                await existingP.update({{ "text.content": pData.text.content }});
            }}
        }}
        ui.notifications.info("Updated Journal Entry: The Tempest Clearing & Gondola Encounter");
    }}

    // ── 2. Create Dedicated Actor Folder & Daggerheart NPC Actors ─────────────
    let actorFolder = game.folders.find(f => f.name === "Adversaries & Allies" && f.type === "Actor");
    if (!actorFolder) {{
        actorFolder = await Folder.create({{ name: "Adversaries & Allies", type: "Actor" }});
    }}

    let defaultActorType = "adversary";
    try {{
        const rawTypes = game.system?.documentTypes?.Actor || game.documentTypes?.Actor || CONFIG?.Actor?.typeLabels;
        if (rawTypes) {{
            const typeArray = Array.isArray(rawTypes) ? rawTypes : Object.keys(rawTypes);
            if (typeArray.includes("adversary")) defaultActorType = "adversary";
            else if (typeArray.includes("npc")) defaultActorType = "npc";
            else if (typeArray.includes("character")) defaultActorType = "character";
            else if (typeArray.length > 0) defaultActorType = typeArray[0];
        }}
    }} catch (e) {{
        console.warn("Actor Type Detection Note:", e);
    }}

    const actorDefinitions = [
        {{
            name: "Storm Raptor",
            type: defaultActorType,
            folder: actorFolder.id,
            img: IMG_RAPTOR,
            system: {{
                traits: {{ agility: {{ value: 3 }}, instinct: {{ value: 2 }}, strength: {{ value: 2 }}, presence: {{ value: 1 }}, finesse: {{ value: 3 }}, knowledge: {{ value: 0 }} }},
                resources: {{
                    hitPoints: {{ value: 0, max: 5 }},
                    stress: {{ value: 0, max: 3, isReversed: true }}
                }},
                evasion: 14,
                difficulty: 14,
                thresholds: {{ minor: 16, major: 30 }},
                damageThresholds: {{ minor: 16, major: 30 }},
                biography: `
                    <div style="display:flex; gap:12px; align-items:center; margin-bottom:10px;">
                      <img src="${{IMG_RAPTOR}}" style="width:80px; height:80px; border-radius:6px; border:2px solid #3366cc;"/>
                      <div>
                        <h3 style="margin:0;">🦅 Storm Raptor — Tier 3 Skulk</h3>
                        <p style="margin:2px 0;"><strong>Primary Attack:</strong> <strong>Claws & Beak</strong> (Melee, +2 to Hit | <strong>2d6+7</strong> physical damage)</p>
                        <p style="margin:2px 0;"><strong>Damage Thresholds:</strong> <strong>Minor 16 | Major 30</strong></p>
                      </div>
                    </div>
                    <p><strong>Motives & Tactics:</strong> Swoop from the fog, screech to disorient, drag PCs off the basket.</p>
                `,
                attack: {{
                    name: "Claws & Beak",
                    img: "icons/commodities/claws/talon-grey.webp",
                    type: "attack",
                    range: "melee",
                    roll: {{
                        type: "attack",
                        trait: null,
                        difficulty: null,
                        bonus: 2,
                        advState: "neutral",
                        diceRolling: {{ multiplier: "flat", flatMultiplier: 1, dice: "d6", compare: null, treshold: null }},
                        useDefault: false
                    }},
                    damage: {{
                        parts: [
                            {{
                                type: ["physical"],
                                value: {{ multiplier: "flat", flatMultiplier: 2, dice: "d6", bonus: 7, custom: {{ enabled: false, formula: "" }} }},
                                applyTo: "hitPoints",
                                resultBased: false,
                                base: false
                            }}
                        ],
                        includeBase: false,
                        direct: false
                    }},
                    description: "Vicious talons and hooked beak coated in lightning residue."
                }}
            }},
            features: [
                {{
                    name: "Flying (Passive)",
                    img: "icons/svg/aura.svg",
                    description: "While flying, the Raptor gains a +3 bonus to its Difficulty (Difficulty becomes 17).",
                    actions: {{}},
                    effects: [{{
                        name: "Airborne Evasion",
                        icon: "icons/svg/aura.svg",
                        transfer: true,
                        disabled: false,
                        description: "Difficulty increased to 17 while airborne.",
                        changes: [{{ key: "system.difficulty", mode: 2, value: "3", priority: null }}]
                    }}]
                }},
                {{
                    name: "Screech (Action)",
                    img: "icons/svg/sound.svg",
                    description: "Mark a Stress to blast a high-pitched screech at all targets in front up to Far range. Targets must mark 1d4 Stress.",
                    actions: {{
                        "raptorScreechActionKey": {{
                            _id: "raptorScreechActionKey",
                            name: "Screech",
                            type: "damage",
                            actionType: "action",
                            systemPath: "actions",
                            chatDisplay: true,
                            cost: [{{ scalable: false, key: "stress", value: 1, consumeOnSuccess: false }}],
                            damage: {{
                                parts: [{{
                                    value: {{ multiplier: "flat", flatMultiplier: 0, dice: "d6", bonus: 0, custom: {{ enabled: true, formula: "1d4" }} }},
                                    applyTo: "stress",
                                    type: [],
                                    base: false,
                                    resultBased: false
                                }}],
                                includeBase: false,
                                direct: true
                            }}
                        }}
                    }}
                }},
                {{
                    name: "Snatch & Pitch (Action)",
                    img: "icons/svg/target.svg",
                    description: "Spend a Fear on a successful attack to grab a target and drag them over the side. The target becomes Restrained over the open air.",
                    actions: {{
                        "raptorSnatchActionKey": {{
                            _id: "raptorSnatchActionKey",
                            name: "Snatch & Pitch",
                            type: "effect",
                            actionType: "action",
                            systemPath: "actions",
                            chatDisplay: true,
                            cost: [{{ scalable: false, key: "fear", value: 1, consumeOnSuccess: false }}]
                        }}
                    }}
                }}
            ],
            effects: []
        }},
        {{
            name: "Ember Warg",
            type: defaultActorType,
            folder: actorFolder.id,
            img: IMG_WARG,
            system: {{
                traits: {{ agility: {{ value: 3 }}, instinct: {{ value: 3 }}, strength: {{ value: 4 }}, presence: {{ value: 2 }}, finesse: {{ value: 1 }}, knowledge: {{ value: 1 }} }},
                resources: {{
                    hitPoints: {{ value: 0, max: 6 }},
                    stress: {{ value: 0, max: 4, isReversed: true }}
                }},
                evasion: 17,
                difficulty: 17,
                thresholds: {{ minor: 18, major: 35 }},
                damageThresholds: {{ minor: 18, major: 35 }},
                biography: `
                    <div style="display:flex; gap:12px; align-items:center; margin-bottom:10px;">
                      <img src="${{IMG_WARG}}" style="width:80px; height:80px; border-radius:6px; border:2px solid #cc3333;"/>
                      <div>
                        <h3 style="margin:0;">🐺 Ember Warg — Tier 3 Bruiser</h3>
                        <p style="margin:2px 0;"><strong>Primary Attack:</strong> <strong>Fiery Jaws</strong> (Close, +4 to Hit | <strong>3d8+3</strong> physical/magic damage)</p>
                        <p style="margin:2px 0;"><strong>Damage Thresholds:</strong> <strong>Minor 18 | Major 35</strong></p>
                      </div>
                    </div>
                    <p><strong>Motives & Tactics:</strong> Circle the falling balloon, leap onto lower tether ropes, breathe fire upward.</p>
                `,
                attack: {{
                    name: "Fiery Jaws",
                    img: "icons/creatures/abilities/fang-tooth-blood-red.webp",
                    type: "attack",
                    range: "close",
                    roll: {{
                        type: "attack",
                        trait: null,
                        difficulty: null,
                        bonus: 4,
                        advState: "neutral",
                        diceRolling: {{ multiplier: "flat", flatMultiplier: 1, dice: "d6", compare: null, treshold: null }},
                        useDefault: false
                    }},
                    damage: {{
                        parts: [
                            {{
                                type: ["physical", "magical"],
                                value: {{ multiplier: "flat", flatMultiplier: 3, dice: "d8", bonus: 3, custom: {{ enabled: false, formula: "" }} }},
                                applyTo: "hitPoints",
                                resultBased: false,
                                base: false
                            }}
                        ],
                        includeBase: false,
                        direct: false
                    }},
                    description: "Massive ember-coated jaws dripping liquid fire."
                }}
            }},
            features: [
                {{
                    name: "Flame Breath (Action — 3d6+4 Magic)",
                    img: "icons/svg/fire.svg",
                    description: "Spend a Fear to spew embers upward at the balloon's envelope or basket. Targets in a Close line take 3d6+4 magic damage. If the balloon envelope is hit, tick the Gondola Equilibrium countdown down by 2.",
                    actions: {{
                        "wargBreathActionKey": {{
                            _id: "wargBreathActionKey",
                            name: "Flame Breath",
                            type: "attack",
                            actionType: "action",
                            systemPath: "actions",
                            chatDisplay: true,
                            cost: [{{ scalable: false, key: "fear", value: 1, consumeOnSuccess: false }}],
                            roll: {{ type: "attack", bonus: 4, advState: "neutral", useDefault: false }},
                            damage: {{
                                parts: [{{
                                    value: {{ multiplier: "flat", flatMultiplier: 3, dice: "d6", bonus: 4, custom: {{ enabled: false, formula: "" }} }},
                                    applyTo: "hitPoints",
                                    type: ["magical"],
                                    base: false,
                                    resultBased: false
                                }}],
                                includeBase: false,
                                direct: false
                            }}
                        }}
                    }}
                }},
                {{
                    name: "Leaping Ambush (Action)",
                    img: "icons/svg/up.svg",
                    description: "If the balloon drops to Close range of the canopy, the Warg can leap onto the gondola's rim, dealing its attack damage and making the target Vulnerable.",
                    actions: {{
                        "wargLeapActionKey": {{
                            _id: "wargLeapActionKey",
                            name: "Leaping Ambush",
                            type: "attack",
                            actionType: "action",
                            systemPath: "actions",
                            chatDisplay: true,
                            roll: {{ type: "attack", bonus: 4, advState: "neutral", useDefault: false }},
                            damage: {{
                                parts: [{{
                                    value: {{ multiplier: "flat", flatMultiplier: 3, dice: "d8", bonus: 3, custom: {{ enabled: false, formula: "" }} }},
                                    applyTo: "hitPoints",
                                    type: ["physical"],
                                    base: false,
                                    resultBased: false
                                }}],
                                includeBase: false,
                                direct: false
                            }}
                        }}
                    }}
                }}
            ],
            effects: []
        }},
        {{
            name: "Pyre Lynx",
            type: defaultActorType,
            folder: actorFolder.id,
            img: IMG_LYNX,
            system: {{
                traits: {{ agility: {{ value: 4 }}, instinct: {{ value: 2 }}, strength: {{ value: 1 }}, presence: {{ value: 0 }}, finesse: {{ value: 3 }}, knowledge: {{ value: 0 }} }},
                resources: {{
                    hitPoints: {{ value: 0, max: 1 }},
                    stress: {{ value: 0, max: 1, isReversed: true }}
                }},
                evasion: 15,
                difficulty: 15,
                thresholds: {{ minor: 0, major: 0 }},
                damageThresholds: {{ minor: 0, major: 0 }},
                biography: `
                    <div style="display:flex; gap:12px; align-items:center; margin-bottom:10px;">
                      <img src="${{IMG_LYNX}}" style="width:80px; height:80px; border-radius:6px; border:2px solid #ff9900;"/>
                      <div>
                        <h3 style="margin:0;">🐱 Pack of Pyre Lynxes — Tier 3 Minion Swarm</h3>
                        <p style="margin:2px 0;"><strong>Primary Attack:</strong> <strong>Infernal Pounce</strong> (Melee, +0 to Hit | <strong>5</strong> magic damage)</p>
                        <p style="margin:2px 0;"><strong>Damage Thresholds:</strong> None (Defeated on any hit)</p>
                      </div>
                    </div>
                    <p><strong>Motives & Tactics:</strong> Swarm the ropes, bite through lines, distract the party.</p>
                `,
                attack: {{
                    name: "Infernal Pounce",
                    img: "icons/creatures/claws/claw-talons-glowing-orange.webp",
                    type: "attack",
                    range: "melee",
                    roll: {{
                        type: "attack",
                        trait: null,
                        difficulty: null,
                        bonus: 0,
                        advState: "neutral",
                        diceRolling: {{ multiplier: "flat", flatMultiplier: 1, dice: "d6", compare: null, treshold: null }},
                        useDefault: false
                    }},
                    damage: {{
                        parts: [
                            {{
                                type: ["magical"],
                                value: {{ multiplier: "flat", flatMultiplier: 0, dice: "d6", bonus: 5, custom: {{ enabled: false, formula: "" }} }},
                                applyTo: "hitPoints",
                                resultBased: false,
                                base: false
                            }}
                        ],
                        includeBase: false,
                        direct: false
                    }},
                    description: "Swarm pounce dealing 5 magic damage per active Lynx."
                }}
            }},
            features: [
                {{
                    name: "Minion (9) (Passive)",
                    img: "icons/svg/skull.svg",
                    description: "Defeated when taking any damage. For every 9 damage dealt by an AoE or multi-target attack, defeat an additional Lynx in range."
                }},
                {{
                    name: "Group Attack (Action)",
                    img: "icons/svg/combat.svg",
                    description: "Spend a Fear to spotlight all Pyre Lynxes near a target. They swarm up the ropes into Melee range and make one shared attack roll. On a success, they deal 5 magic damage each (combined).",
                    actions: {{
                        "lynxGroupAttackKey": {{
                            _id: "lynxGroupAttackKey",
                            name: "Group Attack",
                            type: "attack",
                            actionType: "action",
                            systemPath: "actions",
                            chatDisplay: true,
                            cost: [{{ scalable: false, key: "fear", value: 1, consumeOnSuccess: false }}],
                            roll: {{ type: "attack", bonus: 0, advState: "neutral", useDefault: false }},
                            damage: {{
                                parts: [{{
                                    value: {{ multiplier: "flat", flatMultiplier: 0, dice: "d6", bonus: 5, custom: {{ enabled: false, formula: "" }} }},
                                    applyTo: "hitPoints",
                                    type: ["magical"],
                                    base: false,
                                    resultBased: false
                                }}],
                                includeBase: false,
                                direct: false
                            }}
                        }}
                    }}
                }}
            ],
            effects: []
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
                ui.notifications.info(`Created NPC Actor with Attack: ${{data.name}}`);
            }} catch (err) {{
                console.warn(`Attempting fallback Actor creation for '${{data.name}}'...`, err);
                existing = await Actor.create({{
                    name: data.name,
                    type: data.type,
                    folder: data.folder,
                    img: data.img
                }});
                if (existing && data.system) {{
                    await existing.update({{ system: data.system }}).catch(e => console.warn("System update note:", e));
                }}
                ui.notifications.info(`Created NPC Actor (fallback): ${{data.name}}`);
            }}
        }} else {{
            console.log(`Refreshing existing Actor & Primary Attack: ${{data.name}}`);
            await existing.update({{
                img: data.img,
                system: data.system,
                "prototypeToken.bar1": {{ attribute: "resources.hitPoints" }},
                "prototypeToken.bar2": {{ attribute: "resources.stress" }},
                "prototypeToken.displayBars": 40,
                "prototypeToken.displayName": 20
            }}).catch(e => console.warn("Actor update note:", e));

            const oldItemIds = existing.items.map(i => i.id);
            if (oldItemIds.length > 0) {{
                await existing.deleteEmbeddedDocuments("Item", oldItemIds).catch(e => console.warn("Item deletion note:", e));
            }}
            const oldEffectIds = existing.effects.map(e => e.id);
            if (oldEffectIds.length > 0) {{
                await existing.deleteEmbeddedDocuments("ActiveEffect", oldEffectIds).catch(e => console.warn("Effect deletion note:", e));
            }}
            ui.notifications.info(`Refreshed NPC Actor & Native Attack: ${{data.name}}`);
        }}

        if (existing) {{
            const itemsToCreate = [];

            // Add Primary Attack as an item
            if (data.attack) {{
                itemsToCreate.push({{
                    name: data.attack.name,
                    type: "attack",
                    img: data.attack.img,
                    system: data.attack
                }});
            }}

            if (data.features && data.features.length > 0) {{
                for (let f of data.features) {{
                    itemsToCreate.push({{
                        name: f.name,
                        type: "feature",
                        img: f.img,
                        system: {{ 
                            description: f.description,
                            actions: f.actions || {{}}
                        }},
                        effects: f.effects || []
                    }});
                }}
            }}

            if (itemsToCreate.length > 0) {{
                await existing.createEmbeddedDocuments("Item", itemsToCreate).catch(e => console.warn("Item creation note:", e));
            }}

            if (data.effects && data.effects.length > 0) {{
                const effectsToCreate = data.effects.map(e => ({{
                    name: e.name,
                    label: e.name,
                    icon: e.icon,
                    disabled: false,
                    description: e.description,
                    changes: e.changes || []
                }}));
                await existing.createEmbeddedDocuments("ActiveEffect", effectsToCreate).catch(e => console.warn("ActiveEffect creation note:", e));
            }}
        }}
    }}

    ui.notifications.info("✅ Tempest Clearing Macro Complete! Journal & 3 NPCs with Native Working Attacks Created.");
}})();
"""

with open(r'd:\Code\vumbua\meta\foundry-exports\tempest_clearing_macro.js', 'w', encoding='utf-8') as out:
    out.write(macro_template)

print("Macro written with working native attack cards!")
