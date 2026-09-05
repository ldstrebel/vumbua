import os

# Clean core Foundry SVG icon path for Mwaza-Kasa
IMG_TORTOISE = "icons/svg/shield.svg"

macro_js_content = f"""/**
 * MWAZA-KASA (SPIRIT TORTOISE) - MULTI-PAGE FOUNDRY VTT SETUP MACRO
 * 
 * Campaign: Vumbua (Daggerheart System 1.6.1 Compatible)
 * Entity: Mwaza-Kasa (Spirit Tortoise) — Ancient Aetheric Guardian
 */

(async () => {{
    console.log("Initializing Multi-Page Mwaza-Kasa (Spirit Tortoise) Setup Macro...");

    // ── 1. EMBEDDED ARTWORK / CORE ICON ──
    const IMG_TORTOISE = "{IMG_TORTOISE}";

    // ── 2. DETERMINE SYSTEM ACTOR TYPE ──
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

    // ── 3. CREATE / GET FOLDERS ──
    let actorFolder = game.folders.find(f => f.name === "NPCs" && f.type === "Actor");
    if (!actorFolder) {{
        actorFolder = await Folder.create({{ name: "NPCs", type: "Actor", color: "#2e7d32" }});
    }}

    let journalFolder = game.folders.find(f => f.name === "Vumbua Campaign Guides" && f.type === "JournalEntry");
    if (!journalFolder) {{
        journalFolder = await Folder.create({{ name: "Vumbua Campaign Guides", type: "JournalEntry", color: "#1b5e20" }});
    }}

    // ── 4. ACTOR DATA DEFINITION ──
    const tortoiseData = {{
        name: "Mwaza-Kasa",
        type: defaultActorType,
        folder: actorFolder.id,
        img: IMG_TORTOISE,
        system: {{
            tier: "3",
            type: "support",
            traits: {{
                agility: {{ value: 0 }},
                instinct: {{ value: 4 }},
                strength: {{ value: 4 }},
                presence: {{ value: 3 }},
                finesse: {{ value: 0 }},
                knowledge: {{ value: 3 }}
            }},
            resources: {{
                hitPoints: {{ value: 0, max: 10 }},
                stress: {{ value: 0, max: 6, isReversed: true }}
            }},
            evasion: 12,
            difficulty: 12,
            damageThresholds: {{ major: 20, severe: 40 }},
            biography: `<p><strong>Mwaza-Kasa (Spirit Tortoise) — Tier 3 Guardian</strong></p>
<p>A colossal, ancient spirit-creature native to the petrified forest. Revered as an aetheric anchor, Mwaza-Kasa stabilizes localized node networks, filters Death-Fungus spores, and projects the indestructible <strong>Aetheric Shell-Wall dome</strong> during storm surges and eyewall catastrophes.</p>`,
            notes: `<p><strong>Tactics & Behavior:</strong> Passive and non-aggressive. Absorbs environmental stress. When commune rolls complete the Sync Clock (4 ticks), locks into tree nodes and projects the Aetheric Shell-Wall.</p>`,
            attack: {{
                name: "Pacifying Harmonic Pulse",
                img: "icons/creatures/magical/spirit-fire-orange.webp",
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
                    parts: [{{
                        type: ["magical"],
                        value: {{ multiplier: "flat", flatMultiplier: 2, dice: "d6", bonus: 4, custom: {{ enabled: false, formula: "" }} }},
                        applyTo: "hitPoints",
                        resultBased: false,
                        base: false
                    }}],
                    includeBase: false,
                    direct: false
                }},
                description: "Emits a low-frequency harmonic pulse pushing hostile feral beasts back to Far range."
            }}
        }},
        prototypeToken: {{
            bar1: {{ attribute: "resources.hitPoints" }},
            bar2: {{ attribute: "resources.stress" }},
            displayBars: 40,
            displayName: 20
        }},
        features: [
            {{
                name: "Aetheric Hum (Passive)",
                img: "icons/magic/lightning/barrier-shield-orb-pink.webp",
                description: "Feral beasts cannot enter Close range of Mwaza-Kasa unless driven by extreme primal frenzy."
            }},
            {{
                name: "Resonance Symbiosis (Passive)",
                img: "icons/skills/melee/shield-block-gray-yellow.webp",
                description: "Humanoids in Close range gain +1 Evasion and +1 Armor. Spore-based toxins and Death-Fungus feedback are filtered out."
            }},
            {{
                name: "The Taboo (Reaction)",
                img: "icons/magic/unholy/silhouette-light-fire-blue.webp",
                description: "Staring or touching without attunement triggers a DC 15 Presence Check or 2 Mental Stress + Vulnerable."
            }},
            {{
                name: "Sheltering Sentinel Protocol (Action)",
                img: "icons/magic/unholy/barrier-fire-pink.webp",
                description: "When the Sync Clock (4 ticks) completes, Mwaza-Kasa anchors into the petrified tree node and projects an indestructible Aetheric Shell-Wall dome, rendering all allies completely immune to storm damage and beast assaults."
            }}
        ]
    }};

    // ── 5. ACTOR CREATION / UPDATE ──
    let tortoiseActor = game.actors.find(a => a.name === tortoiseData.name);
    if (!tortoiseActor) {{
        const res = await Actor.create(tortoiseData);
        tortoiseActor = Array.isArray(res) ? res[0] : res;
        console.log("Created Actor:", tortoiseActor?.name || tortoiseData.name);
    }} else {{
        await tortoiseActor.update({{
            system: tortoiseData.system,
            "prototypeToken.bar1": {{ attribute: "resources.hitPoints" }},
            "prototypeToken.bar2": {{ attribute: "resources.stress" }},
            "prototypeToken.displayBars": 40,
            "prototypeToken.displayName": 20
        }});
        
        const oldItemIds = tortoiseActor.items.map(i => i.id);
        if (oldItemIds.length > 0) {{
            await tortoiseActor.deleteEmbeddedDocuments("Item", oldItemIds);
        }}
        console.log("Updated Actor:", tortoiseActor.name);
    }}

    // Create embedded items for native attack and features
    const itemsToCreate = [];
    if (tortoiseData.system.attack) {{
        itemsToCreate.push({{
            name: tortoiseData.system.attack.name,
            type: "attack",
            img: tortoiseData.system.attack.img,
            system: tortoiseData.system.attack
        }});
    }}
    if (tortoiseData.features) {{
        for (let f of tortoiseData.features) {{
            itemsToCreate.push({{
                name: f.name,
                type: "feature",
                img: f.img,
                system: {{ description: f.description, actions: f.actions || {{}} }},
                effects: f.effects || []
            }});
        }}
    }}
    if (itemsToCreate.length > 0 && tortoiseActor) {{
        await tortoiseActor.createEmbeddedDocuments("Item", itemsToCreate);
    }}

    // ── 6. MULTI-PAGE JOURNAL DEFINITIONS ──
    const page1HTML = `
    <div style="font-family: 'Signika', sans-serif; color: #111; line-height: 1.5;">
      <h1 style="color: #1b5e20; border-bottom: 2px solid #2e7d32; margin-bottom: 8px;">Mwaza-Kasa — Overview & Visual Profile</h1>
      <p style="font-style: italic; background: #e8f5e9; padding: 8px 12px; border-left: 4px solid #2e7d32; margin-top: 4px;">
        "The forest does not speak in words, but in the slow shift of ancient shells."
      </p>
      <h2 style="color: #2e7d32; margin-top: 14px;">📜 General Description</h2>
      <p><strong>Mwaza-Kasa</strong> is a colossal, ancient Spirit Tortoise native to the petrified forest of Mizizi.</p>
    </div>
    `;

    const page2HTML = `
    <div style="font-family: 'Signika', sans-serif; color: #111; line-height: 1.5;">
      <h1 style="color: #b71c1c; border-bottom: 2px solid #d32f2f; margin-bottom: 8px;">The Taboo & Bio-Barrier</h1>
      <p><strong>Taboo:</strong> Touch or gaze requires DC 15 Presence check or 2 Stress + Vulnerable.</p>
    </div>
    `;

    const page3HTML = `
    <div style="font-family: 'Signika', sans-serif; color: #111; line-height: 1.5;">
      <h1 style="color: #f57f17; border-bottom: 2px solid #fbc02d; margin-bottom: 8px;">Sync Clock & Table Mechanics</h1>
      <p><strong>Commune Action:</strong> DC 16 Instinct/Presence roll adds 1 tick to 4-tick Sync Clock.</p>
    </div>
    `;

    const page4HTML = `
    <div style="font-family: 'Signika', sans-serif; color: #111; line-height: 1.5;">
      <h1 style="color: #0277bd; border-bottom: 2px solid #0288d1; margin-bottom: 8px;">Sheltering Sentinel Protocol</h1>
      <p>Projects impenetrable Aetheric Shell-Wall dome on clock completion.</p>
    </div>
    `;

    const pagesData = [
        {{ name: "1. Overview & Visual Profile", type: "text", text: {{ content: page1HTML, format: 1 }} }},
        {{ name: "2. The Taboo & Bio-Barrier", type: "text", text: {{ content: page2HTML, format: 1 }} }},
        {{ name: "3. Sync Clock & Table Mechanics", type: "text", text: {{ content: page3HTML, format: 1 }} }},
        {{ name: "4. Sheltering Sentinel & Storm Defense", type: "text", text: {{ content: page4HTML, format: 1 }} }}
    ];

    let journal = game.journal.find(j => j.name === "Mwaza-Kasa (Spirit Tortoise) Guide");
    if (!journal) {{
        journal = await JournalEntry.create({{
            name: "Mwaza-Kasa (Spirit Tortoise) Guide",
            folder: journalFolder.id,
            pages: pagesData
        }});
    }} else {{
        const oldPageIds = journal.pages.contents.map(p => p.id);
        if (oldPageIds.length > 0) {{
            await journal.deleteEmbeddedDocuments("JournalEntryPage", oldPageIds);
        }}
        await journal.createEmbeddedDocuments("JournalEntryPage", pagesData);
    }}

    ui.notifications.info("Mwaza-Kasa Actor & 4 Sub-Page Map Note Journal created/updated successfully!");
}})();
"""

out_file = r"d:\Code\vumbua\meta\foundry-exports\mwaza_kasa_macro.js"
with open(out_file, "w", encoding="utf-8") as f:
    f.write(macro_js_content.strip())

print(f"Generated {out_file} successfully.")