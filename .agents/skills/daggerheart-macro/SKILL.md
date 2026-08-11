---
name: daggerheart-macro
description: Guidelines for generating and updating Foundry VTT macros for Daggerheart, including creating NPC Adversaries with native rollable attacks and compressed embedded artwork.
---

# Daggerheart Macro & NPC Generation Guidelines

Use this skill when creating or updating Foundry VTT macros that set up Daggerheart campaign sessions, NPC Adversaries, and DM journal guides.

---

## 1. Native Rollable Primary Attacks

To create premium, clean NPC sheets, avoid cluttering the **Features** tab with basic attacks. Instead, Daggerheart supports a native, rollable **Primary Attack** card displayed on the left panel of the adversary sheet. This is wired directly under the `system.attack` object.

### ⚔️ Primary Attack Schema
The JS object structure for `system.attack` on a Daggerheart Adversary is as follows:

```javascript
attack: {
    name: "Claws & Beak",
    img: "icons/skills/melee/blood-slash-foam-red.webp", // Core icon guaranteed to exist in Foundry
    type: "attack",
    range: "melee", // "melee", "close", "far", etc.
    roll: {
        type: "attack",
        trait: null,
        difficulty: null,
        bonus: 2, // The hit modifier (+2 to Hit)
        advState: "neutral",
        diceRolling: { multiplier: "flat", flatMultiplier: 1, dice: "d6", compare: null, treshold: null },
        useDefault: false
    },
    damage: {
        parts: [
            {
                type: ["physical"], // Damage type: "physical", "magical", etc.
                // Value formula: (multiplier * dice) + bonus
                value: { 
                    multiplier: "flat", 
                    flatMultiplier: 2, // Number of dice (e.g., 2d6)
                    dice: "d6",        // Dice type
                    bonus: 7,          // Flat damage bonus (+7)
                    custom: { enabled: false, formula: "" } 
                },
                applyTo: "hitPoints",
                resultBased: false,
                base: false
            }
        ],
        includeBase: false,
        direct: false
    },
    description: "Vicious talons and hooked beak coated in lightning residue."
}
```

### 🧹 Cleaning Duplicate Features
When native attacks are populated, ensure any duplicate attack entries (e.g., manual text features or action cards mimicking the attack name) are removed from the `features` array. Keep the **Features** list clean for actual special actions, passives, and reactions (e.g., *Flying*, *Screech*, *Leaping Ambush*).

### ⚠️ Core Icon Hard Requirement
To prevent broken image placeholders on NPC sheets, you **MUST** configure `attack.img` using one of the following 36 verified core icon paths. Do not guess filenames or invent paths.

| Verified Core Path | Description / Theme |
| :--- | :--- |
| `icons/commodities/claws/talon-grey.webp` | Standard claws / talons |
| `icons/creatures/abilities/bear-roar-bite-brown-green.webp` | Beast bite / roar |
| `icons/creatures/abilities/dragon-fire-breath-orange.webp` | Fire breath |
| `icons/creatures/abilities/fang-tooth-blood-red.webp` | Bloody fangs / teeth |
| `icons/creatures/abilities/fang-tooth-poison-green.webp` | Poisonous fangs / teeth |
| `icons/creatures/claws/claw-bear-paw-swipe-red.webp` | Red claw swipe |
| `icons/creatures/claws/claw-straight-orange.webp` | Orange claw strike |
| `icons/creatures/claws/claw-talons-glowing-orange.webp` | Glowing/fiery claws |
| `icons/creatures/magical/spirit-fire-orange.webp` | Fiery spirit |
| `icons/creatures/reptiles/snake-fangs-bite-green-yellow.webp` | Snake bite |
| `icons/magic/death/hand-undead-skeleton-fire-green.webp` | Green fire undead hand |
| `icons/magic/fire/dagger-rune-enchant-flame-strong-blue.webp` | Blue flame dagger |
| `icons/magic/fire/elemental-fire-flying.webp` | Flying fire elemental |
| `icons/magic/fire/flame-burning-hand-purple.webp` | Purple burning hand |
| `icons/magic/fire/flame-burning-hand-white.webp` | White burning hand |
| `icons/magic/lightning/barrier-shield-orb-pink.webp` | Pink lightning shield |
| `icons/magic/unholy/barrier-fire-pink.webp` | Pink fire barrier |
| `icons/magic/unholy/silhouette-light-fire-blue.webp` | Blue fire silhouette |
| `icons/magic/unholy/strike-body-explode-disintegrate.webp` | Body explosion / disintegrate |
| `icons/magic/unholy/strike-hand-glow-pink.webp` | Pink glowing hand strike |
| `icons/skills/melee/blade-tip-chipped-blood-red.webp` | Chipped bloody blade |
| `icons/skills/melee/blade-tips-triple-steel.webp` | Triple steel blades |
| `icons/skills/melee/blood-slash-foam-red.webp` | Red bloody slash |
| `icons/skills/melee/hand-grip-sword-red.webp` | Red sword grip |
| `icons/skills/melee/shield-block-gray-yellow.webp` | Shield block |
| `icons/skills/melee/shield-damaged-broken-gold.webp` | Broken gold shield |
| `icons/skills/melee/strike-axe-red.webp` | Red axe strike |
| `icons/skills/melee/strike-blade-hooked-orange-blue.webp` | Hooked orange-blue blade |
| `icons/skills/melee/strike-dagger-skull-white.webp` | White skull dagger strike |
| `icons/skills/melee/strike-sword-slashing-red.webp` | Red slashing sword |
| `icons/skills/melee/sword-winged-holy-orange.webp` | Winged holy sword |
| `icons/skills/melee/weapons-crossed-swords-yellow.webp` | Crossed yellow swords |
| `icons/skills/movement/feet-bladed-boots-fire.webp` | Fire bladed boots |
| `icons/weapons/sickles/scythe-bone-green-fire.webp` | Green fire bone scythe |
| `icons/weapons/swords/sword-flanged-lightning.webp` | Lightning sword |
| `icons/weapons/wands/wand-carved-fire.webp` | Carved fire wand |

---

## 2. Embedded Artwork & Size Optimization

Foundry VTT macros are stored in a database (such as NeDB or LevelDB) and edited via browser textareas. Including raw, uncompressed images (such as multi-megabyte PNG or JPEG portraits) directly as base64 strings will inflate macro sizes to several megabytes (e.g., 4 MB to 16 MB+). 

This triggers browser pasting overflows or database field limits, resulting in truncation and syntax errors like:
* `SyntaxError: must be valid JavaScript for an asynchronous scope: Unexpected token ':'` (caused by truncation in the middle of a base64 header like `data:image/png;base64...`)
* `Cannot use import statement outside a module`

### ⚡ The WebP Circular Token Pattern
Always compress, resize, and crop all embedded actor portraits into circular tokens with transparent backgrounds using Python's `PIL` library before base64 encoding.

To make high-contrast, premium tokens:
1. **Center-crop** the image to a square.
2. **Resize** to `150x150` pixels.
3. **Apply a circular mask** and save as WebP with alpha transparency support.
4. **Draw a colored border ring** matching the creature's thematic aesthetic (e.g. blue for storm, red/orange for fire, gold/yellow for pyre) to create strong visual contrast.

#### Python Compression & Token Utility:
```python
from PIL import Image, ImageDraw
import base64
import io

def get_compressed_b64(path, border_color=(255, 255, 255), border_width=6):
    try:
        im = Image.open(path).convert("RGBA")
        
        # Center-crop to a square
        width, height = im.size
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        right = (width + min_dim) // 2
        bottom = (height + min_dim) // 2
        im = im.crop((left, top, right, bottom))
        
        size = (150, 150)
        im = im.resize(size, Image.Resampling.LANCZOS)
        
        # Circular mask
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        
        # Output with transparency
        output = Image.new("RGBA", size, (0, 0, 0, 0))
        output.paste(im, (0, 0), mask=mask)
        
        # Colored ring border
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
```

---

## 3. Macro Reference Example

Refer to [embed_images.py](file:///d:/Code/vumbua/meta/foundry-exports/embed_images.py) and the generated [tempest_clearing_macro.js](file:///d:/Code/vumbua/meta/foundry-exports/tempest_clearing_macro.js) as the primary working template for generating Daggerheart Adversaries.

### Key Macro Steps:
1. **Define base64 portraits** as constants at the top.
2. **Setup Journal Folder & Entries** using `JournalEntry.create`.
3. **Setup Actor Folder & Actor Documents** using `Folder.create` and `Actor.create`.
4. **Determine System Document Types** dynamically:
   ```javascript
   let defaultActorType = "adversary";
   try {
       const rawTypes = game.system?.documentTypes?.Actor || game.documentTypes?.Actor;
       if (rawTypes && Object.keys(rawTypes).includes("adversary")) {
           defaultActorType = "adversary";
       }
   } catch (e) { console.warn(e); }
   ```
5. **Populate features, actions, and active effects** inside the actor creation loop using `createEmbeddedDocuments("Item", ...)` and `createEmbeddedDocuments("ActiveEffect", ...)`.
6. **Support Refreshing/Updating** existing documents instead of creating duplicates:
   ```javascript
   let existing = game.actors.find(a => a.name === data.name);
   if (!existing) {
       existing = await Actor.create(data);
   } else {
       await existing.update({ system: data.system, img: data.img });
       // Purge old embedded items/effects and recreate them
       await existing.deleteEmbeddedDocuments("Item", existing.items.map(i => i.id));
       await existing.deleteEmbeddedDocuments("ActiveEffect", existing.effects.map(e => e.id));
   }
   ```

---

## 4. Advanced Features: Interactive Actions & Active Effects

To build high-fidelity custom monsters (Adversaries), features should not be flat HTML descriptions. Instead, configure them with **Active Effects** (passive changes) and **Actions** (clickable roll and damage triggers, metacurrency costs, and reaction rolls).

### ⚔️ Feature Actions Schema (system.actions)
Feature actions are stored under the `system.actions` object, keyed by a random 16-character string.

```javascript
actions: {
    "random16CharKeyA": {
        _id: "random16CharKeyA",
        name: "Flame Breath",
        type: "attack", // "attack", "damage", "healing", "effect"
        actionType: "action", // "action", "passive", "reaction"
        systemPath: "actions",
        chatDisplay: true,
        img: "icons/svg/fire.svg",
        range: "close",
        cost: [
            {
                scalable: false,
                key: "fear", // Resource spent: "fear" (GM), "stress", "hope" (Player)
                value: 1,
                consumeOnSuccess: false
            }
        ],
        roll: {
            type: "attack",
            bonus: 4, // Hit modifier (+4 to Hit)
            advState: "neutral",
            useDefault: false
        },
        damage: {
            parts: [
                {
                    value: {
                        multiplier: "flat", // "flat" is required for flat adversary damage, NOT "prof"
                        flatMultiplier: 3, // Number of dice (e.g. 3d6)
                        dice: "d6",
                        bonus: 4,
                        custom: { enabled: false, formula: "" }
                    },
                    applyTo: "hitPoints", // "hitPoints", "stress", "armor"
                    type: ["magical"], // ["physical"] or ["magical"]
                    base: false,
                    resultBased: false
                }
            ],
            includeBase: false,
            direct: false // Set true to bypass Armor Slots (Direct Damage)
        },
        save: {
            trait: "agility", // The targeted reaction roll trait (e.g. "agility", "strength")
            difficulty: 17, // The target difficulty DC
            damageMod: "none" // "none", "half"
        },
        effects: [],
        triggers: []
    }
}
```

### 🧬 Feature Active Effects Schema (effects)
Embedded passive adjustments (like adding dice to damage rolls or modifying thresholds) are stored under the item's root `effects` array.

Set `"transfer": true` to automatically bind the effect to the Actor when the feature is created.

```javascript
effects: [
    {
        name: "Sneak Attack Passive",
        img: "icons/skills/melee/strike-dagger-skull-white.webp",
        transfer: true, // Crucial: transfers effect to Actor automatically
        type: "base",
        disabled: false,
        changes: [
            {
                key: "system.bonuses.damage.physical.dice", // Stat key to modify
                mode: 2, // MODE_ADD (adds the value to the base stat)
                value: "1d6", // E.g., adds 1d6 damage
                priority: null
            }
        ],
        duration: {
            startTime: null,
            combat: null,
            seconds: null,
            rounds: null,
            turns: null
        }
    }
]
```

---

## 5. Full Database Schema & Creation Lifecycle

To create or refresh an NPC adversary, follow this precise execution loop. This avoids validation errors and prevents document duplication.

### 📋 Complete Adversary Actor Schema
```javascript
{
    name: "Storm Raptor",
    type: "adversary", // Validated against game.system.documentTypes.Actor
    folder: "folderIdString",
    img: "data:image/webp;base64,...", // Compressed 150x150 circular token
    system: {
        tier: "3", // Must be a string choice matching ["1", "2", "3", "4"]. Passing a number or non-matching string throws NaN validation errors.
        type: "skulk", // "bruiser", "minion", "horde", "leader", "ranged", "social", "solo", "standard", "support"
        traits: {
            agility: { value: 3 },
            instinct: { value: 2 },
            strength: { value: 2 },
            presence: { value: 1 },
            finesse: { value: 3 },
            knowledge: { value: 0 }
        },
        resources: {
            hitPoints: { value: 0, max: 5 }, // value (current), max (maximum), isReversed (boolean)
            stress: { value: 0, max: 3, isReversed: true }
        },
        evasion: 14,
        difficulty: 14,
        damageThresholds: {
            major: 16, // NPC Adversaries only use major and severe damage thresholds (default 0), NOT minor/major.
            severe: 30
        },
        biography: "HTML biography string...",
        notes: "HTML tactics/motives notes...",
        resistance: {
            physical: { resistance: false, immunity: false, reduction: 0 }, // optional physical DR
            magical: { resistance: false, immunity: false, reduction: 0 }  // optional magical DR
        },
        rules: {
            conditionImmunities: { hidden: false, restrained: false, vulnerable: false }, // optional status immunities
            damageReduction: { thresholdImmunities: false, reduceSeverity: false },
            attack: { damage: null }
        },
        bonuses: {
            roll: { attack: 0, action: 0, reaction: 0 }, // optional passive roll modifier bonuses
            damage: { physical: 0, magical: 0 }        // optional passive damage bonuses
        },
        attack: {
            // Native rollable attack structure (see Section 1)
        }
    },
    prototypeToken: {
        bar1: { attribute: "resources.hitPoints" },
        bar2: { attribute: "resources.stress" },
        displayBars: 40, // Always Show Owner
        displayName: 20, // Hovered Owner
        prependAdjective: true // Prepend random adjective when spawned on canvas (e.g. "Snarling Bobcat")
    }
}
```

### 🔨 Database Update Lifecycle
When re-running a setup macro, avoid generating duplicate actors. Use this flow to delete stale embedded sub-items (attacks, actions, active effects) and recreate them fresh:

```javascript
let existing = game.actors.find(a => a.name === data.name);
if (!existing) {
    // Create new actor
    existing = await Actor.create(data);
} else {
    // Update basic stats and properties
    await existing.update({
        img: data.img,
        system: data.system,
        "prototypeToken.bar1": { attribute: "resources.hitPoints" },
        "prototypeToken.bar2": { attribute: "resources.stress" },
        "prototypeToken.displayBars": 40,
        "prototypeToken.displayName": 20
    });
    
    // Purge old embedded features & active effects to prevent duplicates
    const oldItemIds = existing.items.map(i => i.id);
    if (oldItemIds.length > 0) {
        await existing.deleteEmbeddedDocuments("Item", oldItemIds);
    }
    const oldEffectIds = existing.effects.map(e => e.id);
    if (oldEffectIds.length > 0) {
        await existing.deleteEmbeddedDocuments("ActiveEffect", oldEffectIds);
    }
}

// Batch create new features/attacks
const itemsToCreate = [];
if (data.attack) {
    itemsToCreate.push({
        name: data.attack.name,
        type: "attack",
        img: data.attack.img,
        system: data.attack
    });
}
if (data.features) {
    for (let f of data.features) {
        itemsToCreate.push({
            name: f.name,
            type: "feature",
            img: f.img,
            system: { description: f.description, actions: f.actions || {} },
            effects: f.effects || []
        });
    }
}
if (itemsToCreate.length > 0) {
    await existing.createEmbeddedDocuments("Item", itemsToCreate);
}
```

---

## 6. Adversary Schema Dumper Command

Use this console utility command to extract the complete, validated database schema of any NPC in your world. Paste this into the F12 console to dump the exact structure for copy-pasting back into macro templates:

```javascript
(async () => {
    const actorName = "Storm Raptor"; // Change to target actor
    const actor = game.actors.getName(actorName);
    if (!actor) {
        console.error(`Actor '${actorName}' not found in world.`);
        return;
    }

    const payload = {
        name: actor.name,
        type: actor.type,
        img: actor.img,
        system: {
            tier: actor.system.tier,
            type: actor.system.type,
            traits: actor.system.traits,
            resources: actor.system.resources,
            evasion: actor.system.evasion,
            difficulty: actor.system.difficulty,
            thresholds: actor.system.thresholds,
            damageThresholds: actor.system.damageThresholds,
            biography: actor.system.biography,
            attack: actor.system.attack
        },
        features: actor.items.filter(i => i.type === "feature").map(i => ({
            name: i.name,
            img: i.img,
            description: i.system.description,
            actions: i.system.actions || {},
            effects: i.effects.map(e => ({
                name: e.name,
                disabled: e.disabled,
                changes: e.changes
            }))
        }))
    };

    console.group(`📋 Validated Schema Dump for '${actorName}'`);
    console.log(JSON.stringify(payload, null, 2));
    console.groupEnd();
    ui.notifications.info(`Logged schema payload for '${actorName}' to F12 Console.`);
})();
```

