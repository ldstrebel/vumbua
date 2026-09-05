import os
from PIL import Image, ImageDraw
import base64
import io

def get_compressed_b64(path, border_color=(129, 199, 132), border_width=6):
    if not os.path.exists(path):
        print(f"Warning: {path} not found.")
        return None
    try:
        im = Image.open(path).convert("RGBA")
        width, height = im.size
        min_dim = min(width, height)
        left = (width - min_dim) // 2
        top = (height - min_dim) // 2
        right = (width + min_dim) // 2
        bottom = (height + min_dim) // 2
        im = im.crop((left, top, right, bottom))
        
        size = (150, 150)
        im = im.resize(size, Image.Resampling.LANCZOS)
        
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        
        output = Image.new("RGBA", size, (0, 0, 0, 0))
        output.paste(im, (0, 0), mask=mask)
        
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
        return None

base_dir = r"d:\Code\vumbua\meta\foundry-exports"

path_raptor   = os.path.join(base_dir, "portraits", "storm_raptor_portrait.png")
path_jaguar   = os.path.join(base_dir, "tokens", "token_mwaza_chui.png")
path_bobcat   = os.path.join(base_dir, "tokens", "token_canopy_cat.png")
path_tortoise = os.path.join(base_dir, "portraits", "mwaza_kasa_portrait.png")
path_pip      = os.path.join(base_dir, "portraits", "pip_portrait.png")
path_bramble  = os.path.join(base_dir, "portraits", "bramble_portrait.png")
path_kael     = os.path.join(base_dir, "portraits", "kael_portrait.png")
path_saffron  = os.path.join(base_dir, "portraits", "saffron_portrait.png")

b64_raptor   = get_compressed_b64(path_raptor,   border_color=(255, 183, 77))   # Amber / Lightning
b64_jaguar   = get_compressed_b64(path_jaguar,   border_color=(229, 115, 115))  # Crimson / Shadow
b64_bobcat   = get_compressed_b64(path_bobcat,   border_color=(255, 138, 128))  # Coral Swarm
b64_tortoise = get_compressed_b64(path_tortoise, border_color=(79, 195, 247))   # Cyan Aetheric Shell
b64_pip      = get_compressed_b64(path_pip,      border_color=(255, 183, 77))   # Warm Pastry Gold
b64_bramble  = get_compressed_b64(path_bramble,  border_color=(129, 199, 132))  # Forest Green
b64_kael     = get_compressed_b64(path_kael,     border_color=(79, 195, 247))   # Sky Blue Tech
b64_saffron  = get_compressed_b64(path_saffron,  border_color=(186, 104, 200))  # Purple Scout

IMG_RAPTOR   = b64_raptor   or "icons/creatures/claws/claw-talons-glowing-orange.webp"
IMG_JAGUAR   = b64_jaguar   or "icons/magic/unholy/strike-hand-glow-pink.webp"
IMG_BOBCAT   = b64_bobcat   or "icons/skills/melee/blood-slash-foam-red.webp"
IMG_TORTOISE = b64_tortoise or "icons/magic/unholy/barrier-fire-pink.webp"
IMG_PIP      = b64_pip      or "icons/weapons/wands/wand-carved-fire.webp"
IMG_BRAMBLE  = b64_bramble  or "icons/skills/melee/strike-blade-hooked-orange-blue.webp"
IMG_KAEL     = b64_kael     or "icons/weapons/swords/sword-flanged-lightning.webp"
IMG_SAFFRON  = b64_saffron  or "icons/skills/melee/strike-dagger-skull-white.webp"

getP_code = 'const getP = (name) => pageUUIDMap[name] ? "@UUID[" + pageUUIDMap[name] + "]{" + name + "}" : "<strong>" + name + "</strong>";'
getA_code = 'const getA = (name) => actorUUIDMap[name] ? "@UUID[" + actorUUIDMap[name] + "]{" + name + "}" : "<strong>" + name + "</strong>";'

macro_js_content = f"""/**
 * 🌪️ TEMPEST CLEARING & TREE FORTRESS ENCOUNTER - MASTER SETUP MACRO
 * 
 * Campaign: Vumbua (Daggerheart System 1.6.1 SRD Balanced)
 * Location: Sector 3 High-Altitude Canopy Clearing & Tree Fortress
 * Theme: Dark Mode Native + Master Prep & SRD Reaction Rolls / Saves
 * 
 * Features:
 *  - Prototype Tokens set `prependAdjective: true` so dragging tokens onto the canvas generates unique names (e.g., "Snarling Bobcat", "Fierce Raptor").
 *  - Full Base64 WebP circular token artwork.
 *  - Preserves custom user-assigned actor artwork on refresh.
 */

(async () => {{
    console.log("🌪️ Executing Tempest Clearing & Tree Fortress Macro with Squad 06 Allies...");

    const IMG_RAPTOR   = "{IMG_RAPTOR}";
    const IMG_JAGUAR   = "{IMG_JAGUAR}";
    const IMG_BOBCAT   = "{IMG_BOBCAT}";
    const IMG_TORTOISE = "{IMG_TORTOISE}";
    const IMG_PIP      = "{IMG_PIP}";
    const IMG_BRAMBLE  = "{IMG_BRAMBLE}";
    const IMG_KAEL     = "{IMG_KAEL}";
    const IMG_SAFFRON  = "{IMG_SAFFRON}";

    // ── 1. Create Dedicated Journal Folder & Master Journal Entry ─────────────
    let journalFolder = game.folders.find(f => f.name === "Encounter DM Guides" && f.type === "JournalEntry");
    if (!journalFolder) {{
        journalFolder = await Folder.create({{ name: "Encounter DM Guides", type: "JournalEntry" }});
    }}

    // ── CATEGORY HEADER HTML TEMPLATES (LEVEL 1) ──
    const overviewPlaceholderHTML = `<p>Generating Master Prep Overview with dynamic UUID links...</p>`;
    const cat1HTML = `<h1 style="color: #81c784; border-bottom: 2px solid #81c784; padding-bottom: 4px; margin-bottom: 8px;">🌲 Environment & Setup</h1><p style="color: #e0e0e0;">Master tactical environment notes for Sector 3 Canopy Raft and Tree Fortress encounter.</p>`;
    const cat2HTML = `<h1 style="color: #ffd54f; border-bottom: 2px solid #ffd54f; padding-bottom: 4px; margin-bottom: 8px;">⏱️ Encounter Clocks</h1><p style="color: #e0e0e0;">Individual progress & hazard clocks for quick DM reference.</p>`;
    const cat3HTML = `<h1 style="color: #ba68c8; border-bottom: 2px solid #ba68c8; padding-bottom: 4px; margin-bottom: 8px;">🔥 GM Reaction Options</h1><p style="color: #e0e0e0;">Fear spending & environmental reaction options for dynamic GM combat control.</p>`;
    const cat4HTML = `<h1 style="color: #4fc3f7; border-bottom: 2px solid #4fc3f7; padding-bottom: 4px; margin-bottom: 8px;">🦅 Events & Battle Waves</h1><p style="color: #e0e0e0;">Narrative triggers, emergency pastry rescues, and wave escalation benchmarks.</p>`;
    const cat5HTML = `<h1 style="color: #e57373; border-bottom: 2px solid #e57373; padding-bottom: 4px; margin-bottom: 8px;">⚔️ Adversary Quick-Refs</h1><p style="color: #e0e0e0;">Stat blocks and tactical abilities for Storm Raptors, Mwaza-Chui, and Bobcat swarms.</p>`;
    const cat6HTML = `<h1 style="color: #81c784; border-bottom: 2px solid #81c784; padding-bottom: 4px; margin-bottom: 8px;">🤝 Squad 06 Ally Quick-Refs</h1><p style="color: #e0e0e0;">Level 3 support ally stat blocks and passive aura abilities.</p>`;

    // ── NARROW SUB-PAGES FOR DARK THEME (LEVEL 2) ──
    const page1Env = `
        <h2 style="color: #81c784; border-bottom: 1px solid rgba(129,199,132,0.3); padding-bottom: 4px;">🌲 ENVIRONMENT: THE TEMPEST CLEARING & TREE FORTRESS</h2>
        <p style="color: #e0e0e0;"><strong style="color: #81c784;">Tier:</strong> 3 (Traversal / Event) | <strong style="color: #81c784;">Difficulty Benchmark:</strong> 17</p>
        <p style="color: #e0e0e0;"><strong style="color: #81c784;">Description:</strong> A high-altitude basalt clearing above the high canopy where storm winds batter Squad 907's Canopy Raft and Squad 06's living Tree Fortress.</p>
        <p style="color: #e0e0e0;"><strong style="color: #81c784;">Vertical Line of Sight:</strong> Airborne beasts at Far Range vertically. Forest floor at Very Far Range below. Shifting raft height closer to treetops brings deck within Close Range of climbing beasts.</p>
    `;

    const pageClockDawn = `
        <h2 style="color: #ffd54f; border-bottom: 1px solid rgba(255,213,79,0.3); padding-bottom: 4px;">⏱️ DAWN SURVIVAL (COUNTDOWN 8)</h2>
        <div style="background: rgba(251,192,45,0.12); border-left: 4px solid #ffd54f; padding: 10px 14px; border-radius: 4px; margin: 10px 0;">
          <p style="color: #fffde7; margin: 0 0 6px 0;"><strong>Goal:</strong> Hold the Tree Fortress until dawn extraction arrives.</p>
          <ul style="color: #fffde7; margin: 0; padding-left: 20px;">
            <li><strong>Advance (Tick Down) on PC Rolls:</strong></li>
            <li>• <strong style="color: #81c784;">Critical Success:</strong> Tick down 3.</li>
            <li>• <strong style="color: #4fc3f7;">Success with Hope:</strong> Tick down 2.</li>
            <li>• <strong style="color: #ffd54f;">Success with Fear:</strong> Tick down 1.</li>
            <li>• <strong style="color: #e57373;">Failure:</strong> 0 ticks.</li>
          </ul>
        </div>
    `;

    const pageClockSurge = `
        <h2 style="color: #e57373; border-bottom: 1px solid rgba(229,115,115,0.3); padding-bottom: 4px;">⏱️ EYEWALL STORM SURGE (COUNTDOWN 6)</h2>
        <div style="background: rgba(211,47,47,0.15); border-left: 4px solid #e57373; padding: 10px 14px; border-radius: 4px; margin: 10px 0;">
          <p style="color: #ffebee; margin: 0 0 6px 0;"><strong>Hazard Progress:</strong> Ticks <strong>UP</strong> whenever a player rolls Failure with Fear, or when GM spends 1 Fear.</p>
          <p style="color: #ffebee; margin: 0;"><strong>Trigger at 6 (Catastrophic Eyewall Surge):</strong> Storm eyewall rips across the deck, dealing <strong style="color: #ff8a80;">[[/r 3d10+8 # Physical/Lightning Damage]]</strong> to all unshielded PCs and knocking them <strong>Vulnerable</strong>. Reset clock to 0.</p>
        </div>
    `;

    const pageClockSync = `
        <h2 style="color: #81c784; border-bottom: 1px solid rgba(129,199,132,0.3); padding-bottom: 4px;">⏱️ MWAZA-KASA SYNC (COUNTDOWN 4)</h2>
        <div style="background: rgba(46,125,50,0.15); border-left: 4px solid #81c784; padding: 10px 14px; border-radius: 4px; margin: 10px 0;">
          <p style="color: #e8f5e9; margin: 0 0 6px 0;"><strong>Goal:</strong> Commune with Mwaza-Kasa to activate storm dome.</p>
          <ul style="color: #e8f5e9; margin: 0; padding-left: 20px;">
            <li><strong>Commune Action:</strong> Spend an action to commune (<strong style="color: #81c784;">Instinct or Presence Roll - DC 16</strong>). Success adds 1 tick (Hope adds +1 extra tick).</li>
            <li><strong>Completion at 4 (Sheltering Sentinel Activation):</strong> Mwaza-Kasa anchors into tree node and projects an <strong style="color: #a5d6a7;">indestructible Aetheric Shell-Wall dome</strong> around the Tree Fortress & Canopy Raft, rendering all allies completely immune to Storm Surges and beast assaults!</li>
          </ul>
        </div>
    `;

    const pageClockEquil = `
        <h2 style="color: #ffb74d; border-bottom: 1px solid rgba(255,183,77,0.3); padding-bottom: 4px;">⏱️ GONDOLA EQUILIBRIUM (COUNTDOWN 8)</h2>
        <div style="background: rgba(239,108,0,0.15); border-left: 4px solid #ffb74d; padding: 10px 14px; border-radius: 4px; margin: 10px 0;">
          <p style="color: #fff3e0; margin: 0 0 6px 0;"><strong>Raft Balance Hazard:</strong> Every action roll with Fear ticks this DOWN by 1.</p>
          <ul style="color: #fff3e0; margin: 0; padding-left: 20px;">
            <li><strong>Trigger at 0 (Deck Pitch):</strong> Deck pitches violently into the eyewall. All PCs make an <strong style="color: #ffb74d;">Agility Reaction Roll (17)</strong> or take <strong style="color: #ff8a80;">[[/r 3d8+5 # Physical Damage]]</strong> and become <strong>Vulnerable</strong> as they hang over the edge.</li>
            <li><strong>Stabilize Action:</strong> Spend action with <strong style="color: #ffb74d;">Agility or Finesse Roll (17)</strong> to stabilize ropes and tick countdown back UP by 2 (or <strong style="color: #a5d6a7;">+4</strong> if Bramble is lashing lines).</li>
          </ul>
        </div>
    `;

    const pageGMFear = `
        <h2 style="color: #ba68c8; border-bottom: 1px solid rgba(186,104,200,0.3); padding-bottom: 4px;">🔥 GM FEAR SPENDING & REACTION OPTIONS</h2>
        <div style="background: rgba(142,36,170,0.15); border-left: 4px solid #ba68c8; padding: 10px 14px; border-radius: 4px; margin: 10px 0;">
          <ul style="color: #f3e5f5; margin: 0; padding-left: 20px;">
            <li><strong style="color: #ce93d8;">Hurricane Gale (1 Fear):</strong> Gust sweeps deck. All raft creatures make <strong>Strength Reaction Roll (17)</strong> or become <strong>Restrained</strong> in rigging / pushed to edge.</li>
            <li><strong style="color: #ce93d8;">Advance Surge Clock (1 Fear):</strong> Tick Eyewall Storm Surge clock UP by +1.</li>
            <li><strong style="color: #ce93d8;">Snagged Anchor (Triggered on Fail w/ Fear):</strong> Raft cable snags petrified treetops. Unanchored targets take <strong style="color: #ff8a80;">[[/r 2 # Stress]]</strong> and drop held items.</li>
            <li><strong style="color: #ce93d8;">Raptor Snatch & Pitch (1 Fear on hit):</strong> Target makes an <strong>Agility or Strength Reaction Roll (DC 15)</strong>. Fail = Dragged over edge (Restrained in open air); Pass = Catches deck edge.</li>
            <li><strong style="color: #ce93d8;">Jaguar Mirror-Step (1 Fear after attack):</strong> Teleport 40ft into shadows leaving decoy.</li>
            <li><strong style="color: #ce93d8;">Jaguar Frequency Overload (1 Fear):</strong> Deal <strong style="color: #ff8a80;">[[/r 3d6+4 # Magical Damage]]</strong> in a line; targets make an <strong>Instinct Reaction Roll (DC 17)</strong> or have spellcasting & mind-links suppressed 1 round.</li>
            <li><strong style="color: #ce93d8;">Bobcat Group Swarm (1 Fear):</strong> Swarm up cables for a shared attack roll. On hit, deal <strong style="color: #ff8a80;">[[/r 5 # Physical Damage]]</strong> + 2 damage per active minion.</li>
          </ul>
        </div>
    `;

    const pageEventHawk = `
        <h2 style="color: #ffb74d; border-bottom: 1px solid rgba(255,183,77,0.3); padding-bottom: 4px;">🦅 PIP & THE STORM HAWK PASTRY RESCUE</h2>
        <div style="background: rgba(239,108,0,0.15); border-left: 4px solid #ffb74d; padding: 10px 14px; border-radius: 4px; margin: 10px 0;">
          <p style="color: #fff3e0; margin: 0 0 6px 0;">Pip is snatched while clutching bacon pastries shouting: <strong style="color: #ff8a80;">"LET ME GO YOU STUPID BIRD!!!"</strong></p>
          <ul style="color: #fff3e0; margin: 0; padding-left: 20px;">
            <li><strong>Persuade Pip to Drop Sack:</strong> <strong style="color: #ffd54f;">DC 15 Presence Check</strong>. Pip hurls sack down; bird drops Pip to chase food.</li>
            <li><strong>Shoot Bird's Talons:</strong> <strong style="color: #e57373;">DC 17 Ranged Attack</strong>. Forces Raptor to drop Pip.</li>
            <li><strong>Catch Pip:</strong> <strong style="color: #81c784;">DC 14 Agility/Finesse Reaction Roll</strong> to catch Pip safely.</li>
          </ul>
        </div>
    `;

    const pageEventRadio = `
        <h2 style="color: #4fc3f7; border-bottom: 1px solid rgba(79,195,247,0.3); padding-bottom: 4px;">📻 RADIO & SPEAKING STONE RELAY</h2>
        <div style="background: rgba(2,136,209,0.15); border-left: 4px solid #4fc3f7; padding: 10px 14px; border-radius: 4px; margin: 10px 0;">
          <p style="color: #e1f5fe; margin: 0 0 6px 0;">Bramble activates Kael's Speaking Stone to relay Aggie's voice across the forest.</p>
          <p style="color: #e1f5fe; margin: 0;"><strong>Frequency Relay Effect:</strong> While Kael operates the relay un-restrained, all PCs gain <strong style="color: #81c784;">+1 to Mwaza-Kasa Sync rolls</strong>.</p>
        </div>
    `;

    const pageWave1 = `
        <h2 style="color: #ba68c8; border-bottom: 1px solid rgba(186,104,200,0.3); padding-bottom: 4px;">⚔️ WAVE 1: AERIAL & CANOPY SWARM</h2>
        <div style="background: rgba(142,36,170,0.15); border-left: 4px solid #ba68c8; padding: 10px 14px; border-radius: 4px; margin: 10px 0;">
          <p style="color: #f3e5f5; margin: 0;">Radio screeches on. Storm Raptors dive from eyewall. One snatches Pip. Bobcats swarm cables toward Kael & Saffron.</p>
        </div>
    `;

    const pageWave2 = `
        <h2 style="color: #ba68c8; border-bottom: 1px solid rgba(186,104,200,0.3); padding-bottom: 4px;">⚔️ WAVE 2: JAGUAR ASSAULT & MID-AIR RESCUE</h2>
        <div style="background: rgba(142,36,170,0.15); border-left: 4px solid #ba68c8; padding: 10px 14px; border-radius: 4px; margin: 10px 0;">
          <p style="color: #f3e5f5; margin: 0;">Mwaza-Chui pounce. PCs must split focus between mid-air Pip rescue and hauling Mwaza-Kasa onto the Tree Fortress.</p>
        </div>
    `;

    const pageWave3 = `
        <h2 style="color: #ba68c8; border-bottom: 1px solid rgba(186,104,200,0.3); padding-bottom: 4px;">⚔️ WAVE 3: EYEWALL PEAK & SHELTERING SENTINEL</h2>
        <div style="background: rgba(142,36,170,0.15); border-left: 4px solid #ba68c8; padding: 10px 14px; border-radius: 4px; margin: 10px 0;">
          <p style="color: #f3e5f5; margin: 0;">Surge clock hits peak. Completing Mwaza-Kasa Sync (4 ticks) projects the indestructible Sheltering Sentinel dome over raft & fortress!</p>
        </div>
    `;

    // ── ADVERSARY & ALLY PAGES WITH DETAILED REACTION NOTES ──
    const pageNPCRaptor = `
        <h2 style="color: #e57373; border-bottom: 1px solid rgba(229,115,115,0.3); padding-bottom: 4px;">🦅 STORM RAPTOR (SKULK)</h2>
        <p style="color: #e0e0e0;"><strong style="color: #e57373;">Difficulty:</strong> 14 (17 flying) | <strong style="color: #e57373;">Evasion:</strong> 14 | <strong style="color: #e57373;">HP:</strong> 5 | <strong style="color: #e57373;">Stress:</strong> 3 | <strong style="color: #e57373;">Thresholds:</strong> Major 16 | Severe 30</p>
        <p style="color: #e0e0e0;"><strong style="color: #e57373;">Attack:</strong> <strong>Claws & Beak</strong> (Melee, +2 to Hit | <strong style="color: #ff8a80;">[[/r 2d6+7 # Physical Damage]]</strong>)</p>
        <p style="color: #e0e0e0;"><strong style="color: #e57373;">Abilities:</strong> Flying (Diff 17), Screech (Presence DC 14 Reaction -> 1d4 Stress), Snatch & Pitch (1 Fear on hit -> Agility/Strength DC 15 Reaction Roll).</p>
        <div style="background: rgba(211,47,47,0.15); border-left: 4px solid #e57373; padding: 10px 14px; border-radius: 4px; margin-top: 10px;">
          <h4 style="color: #ff8a80; margin: 0 0 6px 0;">🧠 DM Tactical Reactions & Behaviors</h4>
          <ul style="color: #ffebee; margin: 0; padding-left: 20px; font-size: 0.95em;">
            <li><strong>Opening Ambush:</strong> Swoops out of eyewall fog, targeting unanchored characters or food sacks (Pip's bacon pastries!).</li>
            <li><strong>Snatch & Pitch Trigger:</strong> On a successful hit, spending 1 Fear forces the target to make an <strong>Agility or Strength Reaction Roll (DC 15)</strong>. On failure, target is dragged over the edge (Restrained in open air); on success, target catches the deck edge.</li>
            <li><strong>Screech Reaction:</strong> Spending 1 Stress forces all Close targets to make a <strong>Presence Reaction Roll (DC 14)</strong> or take 1d4 Stress.</li>
          </ul>
        </div>
    `;

    const pageNPCJaguar = `
        <h2 style="color: #e57373; border-bottom: 1px solid rgba(229,115,115,0.3); padding-bottom: 4px;">🐆 MWAZA-CHUI (BRUISER)</h2>
        <p style="color: #e0e0e0;"><strong style="color: #e57373;">Difficulty:</strong> 17 | <strong style="color: #e57373;">Evasion:</strong> 17 | <strong style="color: #e57373;">HP:</strong> 6 | <strong style="color: #e57373;">Stress:</strong> 4 | <strong style="color: #e57373;">Thresholds:</strong> Major 18 | Severe 35</p>
        <p style="color: #e0e0e0;"><strong style="color: #e57373;">Attack:</strong> <strong>Frequency Bite</strong> (Close, +4 to Hit / +6 vs mind-links | <strong style="color: #ff8a80;">[[/r 3d8+3 # Physical/Psychic Damage]]</strong>)</p>
        <p style="color: #e0e0e0;"><strong style="color: #e57373;">Abilities:</strong> Mirror-Step (1 Fear teleport), Frequency Overload (1 Fear line -> Instinct DC 17 Reaction Roll).</p>
        <div style="background: rgba(211,47,47,0.15); border-left: 4px solid #e57373; padding: 10px 14px; border-radius: 4px; margin-top: 10px;">
          <h4 style="color: #ff8a80; margin: 0 0 6px 0;">🧠 DM Tactical Reactions & Behaviors</h4>
          <ul style="color: #ffebee; margin: 0; padding-left: 20px; font-size: 0.95em;">
            <li><strong>Mind-Link Hunter:</strong> Drawn directly to telepathic links and Speaking Stone broadcasts (+2 to Hit vs mind-link users).</li>
            <li><strong>Mirror-Step Decoy:</strong> Spends 1 Fear after taking damage or attacking to teleport 40ft into shadow, leaving an Aetheric static image.</li>
            <li><strong>Frequency Overload:</strong> Spends 1 Fear to spew static embers in a Close line (3d6+4 Magic). Targets make an <strong>Instinct Reaction Roll (DC 17)</strong> or have spellcasting & mind-links suppressed 1 round.</li>
          </ul>
        </div>
    `;

    const pageNPCBobcat = `
        <h2 style="color: #e57373; border-bottom: 1px solid rgba(229,115,115,0.3); padding-bottom: 4px;">🐱 MWAZA-BOBCAT SWARM (MINION)</h2>
        <p style="color: #e0e0e0;"><strong style="color: #e57373;">Difficulty:</strong> 15 | <strong style="color: #e57373;">Evasion:</strong> 15 | <strong style="color: #e57373;">HP:</strong> 1 | <strong style="color: #e57373;">Stress:</strong> 1</p>
        <p style="color: #e0e0e0;"><strong style="color: #e57373;">Attack:</strong> <strong>Canopy Pounce</strong> (Melee, +0 to Hit | <strong style="color: #ff8a80;">[[/r 5 # Physical Damage]]</strong>)</p>
        <p style="color: #e0e0e0;"><strong style="color: #e57373;">Abilities:</strong> Minion (9) (Defeated on hit; every 9 damage defeats extra minion), Group Attack (1 Fear -> shared attack roll).</p>
        <div style="background: rgba(211,47,47,0.15); border-left: 4px solid #e57373; padding: 10px 14px; border-radius: 4px; margin-top: 10px;">
          <h4 style="color: #ff8a80; margin: 0 0 6px 0;">🧠 DM Tactical Reactions & Behaviors</h4>
          <ul style="color: #ffebee; margin: 0; padding-left: 20px; font-size: 0.95em;">
            <li><strong>Cable Swarmer:</strong> Scrambles up tension cables toward Kael's Speaking Stone array to chew signal wires.</li>
            <li><strong>Group Pounce:</strong> Spends 1 Fear to combine all active minions into a single high-damage pounce (5 + 2 per minion).</li>
            <li><strong>Sonic Panic:</strong> Scatters or drops from cables if Mwaza-Kasa releases a Pacifying Pulse or Kael fires a shockwave.</li>
          </ul>
        </div>
    `;

    const pageNPCTortoise = `
        <h2 style="color: #81c784; border-bottom: 1px solid rgba(129,199,132,0.3); padding-bottom: 4px;">🐢 MWAZA-KASA (SPIRIT TORTOISE)</h2>
        <p style="color: #e0e0e0;"><strong style="color: #81c784;">Difficulty:</strong> 12 | <strong style="color: #81c784;">Evasion:</strong> 12 | <strong style="color: #81c784;">HP:</strong> 10 | <strong style="color: #81c784;">Stress:</strong> 6 | <strong style="color: #81c784;">Thresholds:</strong> Major 20 | Severe 40</p>
        <p style="color: #e0e0e0;"><strong style="color: #81c784;">Attack:</strong> <strong>Pacifying Pulse</strong> (Close, +4 to Hit | <strong style="color: #81c784;">[[/r 2d6+4 # Magical Damage]]</strong>)</p>
        <p style="color: #e0e0e0;"><strong style="color: #81c784;">Abilities:</strong> Aetheric Hum, Resonance Symbiosis (+1 Evasion & Armor to nearby allies), The Taboo reaction (Presence DC 15 Reaction Roll).</p>
        <div style="background: rgba(46,125,50,0.15); border-left: 4px solid #81c784; padding: 10px 14px; border-radius: 4px; margin-top: 10px;">
          <h4 style="color: #a5d6a7; margin: 0 0 6px 0;">🧠 DM Tactical Reactions & Behaviors</h4>
          <ul style="color: #e8f5e9; margin: 0; padding-left: 20px; font-size: 0.95em;">
            <li><strong>Commune Response:</strong> Ticks UP on the Sync Clock whenever PCs succeed on Instinct or Presence commune checks (DC 16).</li>
            <li><strong>Aetheric Aura:</strong> Feral beasts refuse to step into Close range. Nearby humanoids gain +1 Evasion and +1 Armor.</li>
            <li><strong>The Taboo Trigger:</strong> Staring directly into its eyes or striking its shell triggers a <strong>Presence Reaction Roll (DC 15)</strong>. Fail = 2 Stress + Vulnerable.</li>
          </ul>
        </div>
    `;

    const pageNPCPip = `
        <h2 style="color: #81c784; border-bottom: 1px solid rgba(129,199,132,0.3); padding-bottom: 4px;">🌸 PIP (SUPPORT / QUARTERMASTER)</h2>
        <p style="color: #e0e0e0;"><strong style="color: #81c784;">Evasion:</strong> 13 | <strong style="color: #81c784;">HP:</strong> 4 | <strong style="color: #81c784;">Stress:</strong> 4 | <strong style="color: #81c784;">Thresholds:</strong> Major 12 | Severe 22</p>
        <p style="color: #e0e0e0;"><strong style="color: #81c784;">Attack:</strong> <strong>Pastry Tossing & Flare</strong> (Close, +3 to Hit | <strong style="color: #81c784;">[[/r 1d6+3 # Magical Damage]]</strong>)</p>
        <p style="color: #e0e0e0;"><strong style="color: #81c784;">Abilities:</strong> Emergency Pastry Supply (Clear 1 Stress), Hysterical Distraction (Disadvantage to attacker).</p>
        <div style="background: rgba(46,125,50,0.15); border-left: 4px solid #81c784; padding: 10px 14px; border-radius: 4px; margin-top: 10px;">
          <h4 style="color: #a5d6a7; margin: 0 0 6px 0;">🧠 DM Tactical Reactions & Behaviors</h4>
          <ul style="color: #e8f5e9; margin: 0; padding-left: 20px; font-size: 0.95em;">
            <li><strong>Mid-Air Screaming:</strong> Starts Wave 1 snatched by a Storm Raptor shouting <em style="color: #ff8a80;">"LET ME GO YOU STUPID BIRD!"</em></li>
            <li><strong>Pastry Supply Reaction:</strong> When an ally takes Stress, Pip hurls a dense bacon pastry to clear 1 Stress.</li>
            <li><strong>Hysterical Scream:</strong> Screams hysterically when an ally is targeted, giving the attacker Disadvantage.</li>
          </ul>
        </div>
    `;

    const pageNPCBramble = `
        <h2 style="color: #81c784; border-bottom: 1px solid rgba(129,199,132,0.3); padding-bottom: 4px;">🌿 BRAMBLE (SUPPORT / DEFENDER)</h2>
        <p style="color: #e0e0e0;"><strong style="color: #81c784;">Evasion:</strong> 11 | <strong style="color: #81c784;">HP:</strong> 7 | <strong style="color: #81c784;">Stress:</strong> 5 | <strong style="color: #81c784;">Thresholds:</strong> Major 16 | Severe 28</p>
        <p style="color: #e0e0e0;"><strong style="color: #81c784;">Attack:</strong> <strong>Root-Vine Slam</strong> (Melee, +4 to Hit | <strong style="color: #81c784;">[[/r 2d8+4 # Physical Damage]]</strong>)</p>
        <p style="color: #e0e0e0;"><strong style="color: #81c784;">Abilities:</strong> Tree Fortress Anchor (+2 Equilibrium stabilization), Root Rampart (+2 Armor Slots to ally).</p>
        <div style="background: rgba(46,125,50,0.15); border-left: 4px solid #81c784; padding: 10px 14px; border-radius: 4px; margin-top: 10px;">
          <h4 style="color: #a5d6a7; margin: 0 0 6px 0;">🧠 DM Tactical Reactions & Behaviors</h4>
          <ul style="color: #e8f5e9; margin: 0; padding-left: 20px; font-size: 0.95em;">
            <li><strong>Anchor Defense:</strong> Lashes root-vines into deck winch cables (+2 bonus to all Gondola Equilibrium stabilization rolls).</li>
            <li><strong>Root Rampart Shield:</strong> When an ally takes heavy damage, weaves living timber around them (+2 Armor Slots & Vanguard Protection).</li>
            <li><strong>Deck Pitch Response:</strong> Immediately drops to all fours when the deck tilts, anchoring unseated allies.</li>
          </ul>
        </div>
    `;

    const pageNPCKael = `
        <h2 style="color: #81c784; border-bottom: 1px solid rgba(129,199,132,0.3); padding-bottom: 4px;">⚙️ KAEL (SUPPORT / SIGNAL TECH)</h2>
        <p style="color: #e0e0e0;"><strong style="color: #81c784;">Evasion:</strong> 12 | <strong style="color: #81c784;">HP:</strong> 4 | <strong style="color: #81c784;">Stress:</strong> 4 | <strong style="color: #81c784;">Thresholds:</strong> Major 13 | Severe 24</p>
        <p style="color: #e0e0e0;"><strong style="color: #81c784;">Attack:</strong> <strong>Acoustic Shockwave</strong> (Close, +3 to Hit | <strong style="color: #81c784;">[[/r 2d6+2 # Magical Damage]]</strong>)</p>
        <p style="color: #e0e0e0;"><strong style="color: #81c784;">Abilities:</strong> Speaking Stone Frequency Relay (+1 Sync bonus), Tension Calibration (Reduce hazard dmg by 3).</p>
        <div style="background: rgba(46,125,50,0.15); border-left: 4px solid #81c784; padding: 10px 14px; border-radius: 4px; margin-top: 10px;">
          <h4 style="color: #a5d6a7; margin: 0 0 6px 0;">🧠 DM Tactical Reactions & Behaviors</h4>
          <ul style="color: #e8f5e9; margin: 0; padding-left: 20px; font-size: 0.95em;">
            <li><strong>Frequency Tuning:</strong> Tunes the Speaking Stone array to Mwaza-Kasa (+1 bonus to all Mwaza-Kasa Sync rolls while un-restrained).</li>
            <li><strong>Dampener Shield:</strong> Crystal dampeners reduce storm hazard damage to Tree Fortress allies by 3.</li>
            <li><strong>Panicked Defense:</strong> If Bobcats reach his rig, fires an Acoustic Shockwave and calls for Bramble or PC cover.</li>
          </ul>
        </div>
    `;

    const pageNPCSaffron = `
        <h2 style="color: #81c784; border-bottom: 1px solid rgba(129,199,132,0.3); padding-bottom: 4px;">🎨 SAFFRON (SUPPORT / SCOUT)</h2>
        <p style="color: #e0e0e0;"><strong style="color: #81c784;">Evasion:</strong> 14 | <strong style="color: #81c784;">HP:</strong> 4 | <strong style="color: #81c784;">Stress:</strong> 3 | <strong style="color: #81c784;">Thresholds:</strong> Major 13 | Severe 23</p>
        <p style="color: #e0e0e0;"><strong style="color: #81c784;">Attack:</strong> <strong>Precision Stylus Strike</strong> (Melee, +3 to Hit | <strong style="color: #81c784;">[[/r 1d8+3 # Physical Damage]]</strong>)</p>
        <p style="color: #e0e0e0;"><strong style="color: #81c784;">Abilities:</strong> Anatomical Sketch (Advantage on damage vs sketched beasts), Unbothered Focus.</p>
        <div style="background: rgba(46,125,50,0.15); border-left: 4px solid #81c784; padding: 10px 14px; border-radius: 4px; margin-top: 10px;">
          <h4 style="color: #a5d6a7; margin: 0 0 6px 0;">🧠 DM Tactical Reactions & Behaviors</h4>
          <ul style="color: #e8f5e9; margin: 0; padding-left: 20px; font-size: 0.95em;">
            <li><strong>Anatomical Sketching:</strong> Rapidly sketches target beast weak points; all attacks against that target gain Advantage for 1 round.</li>
            <li><strong>Unbothered Focus:</strong> Completely ignores wind shear and deck pitch while sketching.</li>
            <li><strong>Jaguar Counter:</strong> Sketches Mwaza-Chui's static aura to reveal its true position through telepathic decoys.</li>
          </ul>
        </div>
    `;

    // ── HIERARCHICAL LEVEL-1 & LEVEL-2 PAGES ARRAY ──
    const masterPages = [
        // ── MASTER PREP OVERVIEW (LEVEL 1 PAGE 1) ──
        {{ name: "⚔️ Master Tactical Overview & Prep Guide", type: "text", title: {{ show: true, level: 1 }}, text: {{ content: overviewPlaceholderHTML, format: 1 }} }},

        // ── ENVIRONMENT ──
        {{ name: "🌲 Environment & Setup", type: "text", title: {{ show: true, level: 1 }}, text: {{ content: cat1HTML, format: 1 }} }},
        {{ name: "Canopy Clearing & Tree Fortress", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: page1Env, format: 1 }} }},

        // ── ENCOUNTER CLOCKS ──
        {{ name: "⏱️ Encounter Clocks", type: "text", title: {{ show: true, level: 1 }}, text: {{ content: cat2HTML, format: 1 }} }},
        {{ name: "Dawn Survival (Countdown 8)", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: pageClockDawn, format: 1 }} }},
        {{ name: "Eyewall Storm Surge (Countdown 6)", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: pageClockSurge, format: 1 }} }},
        {{ name: "Mwaza-Kasa Sync (Countdown 4)", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: pageClockSync, format: 1 }} }},
        {{ name: "Gondola Equilibrium (Countdown 8)", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: pageClockEquil, format: 1 }} }},

        // ── GM REACTION OPTIONS ──
        {{ name: "🔥 GM Reaction Options", type: "text", title: {{ show: true, level: 1 }}, text: {{ content: cat3HTML, format: 1 }} }},
        {{ name: "Fear Spending & Reaction Options", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: pageGMFear, format: 1 }} }},

        // ── EVENTS & BATTLE WAVES ──
        {{ name: "🦅 Events & Battle Waves", type: "text", title: {{ show: true, level: 1 }}, text: {{ content: cat4HTML, format: 1 }} }},
        {{ name: "Pip & Storm Hawk Pastry Rescue", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: pageEventHawk, format: 1 }} }},
        {{ name: "Radio & Speaking Stone Relay", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: pageEventRadio, format: 1 }} }},
        {{ name: "Wave 1: Aerial & Canopy Swarm", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: pageWave1, format: 1 }} }},
        {{ name: "Wave 2: Jaguar Assault & Mid-Air Rescue", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: pageWave2, format: 1 }} }},
        {{ name: "Wave 3: Eyewall Peak & Sheltering Sentinel", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: pageWave3, format: 1 }} }},

        // ── ADVERSARY QUICK-REFS ──
        {{ name: "⚔️ Adversary Quick-Refs", type: "text", title: {{ show: true, level: 1 }}, text: {{ content: cat5HTML, format: 1 }} }},
        {{ name: "Storm Raptor (Skulk)", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: pageNPCRaptor, format: 1 }} }},
        {{ name: "Mwaza-Chui (Bruiser)", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: pageNPCJaguar, format: 1 }} }},
        {{ name: "Mwaza-Bobcat Swarm (Minion)", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: pageNPCBobcat, format: 1 }} }},
        {{ name: "Mwaza-Kasa (Support)", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: pageNPCTortoise, format: 1 }} }},

        // ── SQUAD 06 ALLY QUICK-REFS ──
        {{ name: "🤝 Squad 06 Ally Quick-Refs", type: "text", title: {{ show: true, level: 1 }}, text: {{ content: cat6HTML, format: 1 }} }},
        {{ name: "Pip (Support)", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: pageNPCPip, format: 1 }} }},
        {{ name: "Bramble (Support)", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: pageNPCBramble, format: 1 }} }},
        {{ name: "Kael (Support)", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: pageNPCKael, format: 1 }} }},
        {{ name: "Saffron (Support)", type: "text", title: {{ show: true, level: 2 }}, text: {{ content: pageNPCSaffron, format: 1 }} }}
    ];

    let dmJournal = game.journal.find(j => j.name === "The Tempest Clearing & Tree Fortress Encounter" && (j.folder?.id === journalFolder.id || j.folder === journalFolder.id));
    if (!dmJournal) {{
        dmJournal = await JournalEntry.create({{
            name: "The Tempest Clearing & Tree Fortress Encounter",
            folder: journalFolder.id,
            pages: masterPages
        }});
        ui.notifications.info("Created Journal Entry: The Tempest Clearing & Tree Fortress Encounter");
    }} else {{
        const oldPageIds = dmJournal.pages.contents.map(p => p.id);
        if (oldPageIds.length > 0) {{
            await dmJournal.deleteEmbeddedDocuments("JournalEntryPage", oldPageIds);
        }}
        await dmJournal.createEmbeddedDocuments("JournalEntryPage", masterPages);
        ui.notifications.info("Updated Journal Entry: The Tempest Clearing & Tree Fortress Encounter");
    }}

    // ── 2. Create Dedicated Actor Folder & Daggerheart Actors ──────────────────
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

    // Map legacy names to migrate old actors cleanly
    const legacyActorNames = {{
        "Mwaza-Bobcat Swarm": ["Bobcat", "Mizizi Bobcat", "Mizizi Bobcat Swarm"],
        "Storm Raptor": ["Storm Hawk", "Raptor"],
        "Mwaza-Chui": ["Mizizi Jaguar", "Memory Jaguar", "Jaguar"],
        "Mwaza-Kasa": ["Spirit Tortoise", "Mwaza-Kasa (Spirit Tortoise)"],
        "Pip": ["Pip"],
        "Bramble": ["Bramble"],
        "Kael": ["Kael"],
        "Saffron": ["Saffron"]
    }};

    const actorDefinitions = [
        // ── 1. STORM RAPTOR ──
        {{
            name: "Storm Raptor",
            type: defaultActorType,
            folder: actorFolder.id,
            img: IMG_RAPTOR,
            prototypeToken: {{
                bar1: {{ attribute: "resources.hitPoints" }},
                bar2: {{ attribute: "resources.stress" }},
                displayBars: 40,
                displayName: 20,
                prependAdjective: true
            }},
            system: {{
                tier: "3",
                type: "skulk",
                traits: {{ agility: {{ value: 3 }}, instinct: {{ value: 2 }}, strength: {{ value: 2 }}, presence: {{ value: 1 }}, finesse: {{ value: 3 }}, knowledge: {{ value: 0 }} }},
                resources: {{ hitPoints: {{ value: 0, max: 5 }}, stress: {{ value: 0, max: 3, isReversed: true }} }},
                evasion: 14,
                difficulty: 14,
                damageThresholds: {{ major: 16, severe: 30 }},
                motives: "Swoops from eyewall fog to snatch carrying items or unanchored prey.",
                notes: pageNPCRaptor,
                biography: pageNPCRaptor,
                attack: {{
                    name: "Claws & Beak",
                    img: "icons/creatures/claws/claw-talons-glowing-orange.webp",
                    type: "attack",
                    range: "melee",
                    roll: {{ type: "attack", trait: null, difficulty: null, bonus: 2, advState: "neutral", diceRolling: {{ multiplier: "flat", flatMultiplier: 1, dice: "d6", compare: null, treshold: null }}, useDefault: false }},
                    damage: {{ parts: [{{ type: ["physical"], value: {{ multiplier: "flat", flatMultiplier: 2, dice: "d6", bonus: 7, custom: {{ enabled: false, formula: "" }} }}, applyTo: "hitPoints", resultBased: false, base: false }}], includeBase: false, direct: false }},
                    description: "Vicious talons coated in storm lightning."
                }}
            }},
            features: [
                {{ name: "Flying (Passive)", img: "icons/magic/fire/elemental-fire-flying.webp", description: "Difficulty becomes 17 while airborne in eyewall gusts." }},
                {{ name: "Screech (Action)", img: "icons/creatures/abilities/bear-roar-bite-brown-green.webp", description: "Mark 1 Stress -> Target makes a Presence Reaction Roll (DC 14) or takes 1d4 Stress." }},
                {{ name: "Snatch & Pitch (Action)", img: "icons/skills/movement/feet-bladed-boots-fire.webp", description: "Spend 1 Fear on hit -> Target makes an Agility or Strength Reaction Roll (DC 15). Fail = Dragged over edge (Restrained in open air); Pass = Catches deck edge." }}
            ]
        }},
        // ── 2. MWAZA-CHUI ──
        {{
            name: "Mwaza-Chui",
            type: defaultActorType,
            folder: actorFolder.id,
            img: IMG_JAGUAR,
            prototypeToken: {{
                bar1: {{ attribute: "resources.hitPoints" }},
                bar2: {{ attribute: "resources.stress" }},
                displayBars: 40,
                displayName: 20,
                prependAdjective: true
            }},
            system: {{
                tier: "3",
                type: "bruiser",
                traits: {{ agility: {{ value: 3 }}, instinct: {{ value: 4 }}, strength: {{ value: 2 }}, presence: {{ value: 1 }}, finesse: {{ value: 3 }}, knowledge: {{ value: 2 }} }},
                resources: {{ hitPoints: {{ value: 0, max: 6 }}, stress: {{ value: 0, max: 4, isReversed: true }} }},
                evasion: 17,
                difficulty: 17,
                damageThresholds: {{ major: 18, severe: 35 }},
                motives: "Hunts telepathic mind-links and spellcasters. Teleports into shadow decoys.",
                notes: pageNPCJaguar,
                biography: pageNPCJaguar,
                attack: {{
                    name: "Frequency Bite",
                    img: "icons/magic/unholy/strike-hand-glow-pink.webp",
                    type: "attack",
                    range: "close",
                    roll: {{ type: "attack", trait: null, difficulty: null, bonus: 4, advState: "neutral", diceRolling: {{ multiplier: "flat", flatMultiplier: 1, dice: "d6", compare: null, treshold: null }}, useDefault: false }},
                    damage: {{ parts: [{{ type: ["physical", "magical"], value: {{ multiplier: "flat", flatMultiplier: 3, dice: "d8", bonus: 3, custom: {{ enabled: false, formula: "" }} }}, applyTo: "hitPoints", resultBased: false, base: false }}], includeBase: false, direct: false }},
                    description: "Aetheric bite targeting active mind-links (+2 to Hit vs links)."
                }}
            }},
            features: [
                {{ name: "Mirror-Step (Action)", img: "icons/magic/unholy/silhouette-light-fire-blue.webp", description: "Spend 1 Fear after attack -> teleport 40ft into shadows leaving decoy." }},
                {{ name: "Frequency Overload (Action)", img: "icons/magic/unholy/strike-body-explode-disintegrate.webp", description: "Spend 1 Fear -> spew static embers in a Close line (3d6+4 Magic). Targets make an Instinct Reaction Roll (DC 17) or have spellcasting & mind-links suppressed 1 round." }}
            ]
        }},
        // ── 3. MWAZA-BOBCAT SWARM ──
        {{
            name: "Mwaza-Bobcat Swarm",
            type: defaultActorType,
            folder: actorFolder.id,
            img: IMG_BOBCAT,
            prototypeToken: {{
                bar1: {{ attribute: "resources.hitPoints" }},
                bar2: {{ attribute: "resources.stress" }},
                displayBars: 40,
                displayName: 20,
                prependAdjective: true
            }},
            system: {{
                tier: "3",
                type: "minion",
                traits: {{ agility: {{ value: 3 }}, instinct: {{ value: 2 }}, strength: {{ value: 1 }}, presence: {{ value: 1 }}, finesse: {{ value: 2 }}, knowledge: {{ value: 0 }} }},
                resources: {{ hitPoints: {{ value: 0, max: 1 }}, stress: {{ value: 0, max: 1, isReversed: true }} }},
                evasion: 15,
                difficulty: 15,
                damageThresholds: {{ major: 0, severe: 0 }},
                motives: "Cable Swarmer: Scrambles up cables to chew signal wires. Combines for group pounce.",
                notes: pageNPCBobcat,
                biography: pageNPCBobcat,
                attack: {{
                    name: "Canopy Pounce",
                    img: "icons/skills/melee/blood-slash-foam-red.webp",
                    type: "attack",
                    range: "melee",
                    roll: {{ type: "attack", trait: null, difficulty: null, bonus: 0, advState: "neutral", diceRolling: {{ multiplier: "flat", flatMultiplier: 1, dice: "d6", compare: null, treshold: null }}, useDefault: false }},
                    damage: {{ parts: [{{ type: ["physical"], value: {{ multiplier: "flat", flatMultiplier: 0, dice: "d6", bonus: 5, custom: {{ enabled: false, formula: "" }} }}, applyTo: "hitPoints", resultBased: false, base: false }}], includeBase: false, direct: false }},
                    description: "Swarm pounce on cables."
                }}
            }},
            features: [
                {{ name: "Minion (9) (Passive)", img: "icons/skills/melee/shield-damaged-broken-gold.webp", description: "Defeated on taking damage. Every 9 damage defeats an extra minion." }},
                {{ name: "Group Attack (Action)", img: "icons/skills/melee/blade-tips-triple-steel.webp", description: "Spend 1 Fear -> swarm up ropes for shared attack (5 + 2 per active minion)." }}
            ]
        }},
        // ── 4. MWAZA-KASA ──
        {{
            name: "Mwaza-Kasa",
            type: defaultActorType,
            folder: actorFolder.id,
            img: IMG_TORTOISE,
            prototypeToken: {{
                bar1: {{ attribute: "resources.hitPoints" }},
                bar2: {{ attribute: "resources.stress" }},
                displayBars: 40,
                displayName: 20,
                prependAdjective: true
            }},
            system: {{
                tier: "3",
                type: "support",
                traits: {{ agility: {{ value: 0 }}, instinct: {{ value: 4 }}, strength: {{ value: 4 }}, presence: {{ value: 3 }}, finesse: {{ value: 0 }}, knowledge: {{ value: 3 }} }},
                resources: {{ hitPoints: {{ value: 0, max: 10 }}, stress: {{ value: 0, max: 6, isReversed: true }} }},
                evasion: 12,
                difficulty: 12,
                damageThresholds: {{ major: 20, severe: 40 }},
                motives: "Communes to anchor Sheltering Sentinel dome. Repels feral beasts.",
                notes: pageNPCTortoise,
                biography: pageNPCTortoise,
                attack: {{
                    name: "Pacifying Pulse",
                    img: "icons/magic/unholy/barrier-fire-pink.webp",
                    type: "attack",
                    range: "close",
                    roll: {{ type: "attack", trait: null, difficulty: null, bonus: 4, advState: "neutral", diceRolling: {{ multiplier: "flat", flatMultiplier: 1, dice: "d6", compare: null, treshold: null }}, useDefault: false }},
                    damage: {{ parts: [{{ type: ["magical"], value: {{ multiplier: "flat", flatMultiplier: 2, dice: "d6", bonus: 4, custom: {{ enabled: false, formula: "" }} }}, applyTo: "hitPoints", resultBased: false, base: false }}], includeBase: false, direct: false }},
                    description: "Pacifying pulse pushing targets to Far range (Strength/Presence DC 16 Reaction Roll)."
                }}
            }},
            features: [
                {{ name: "Aetheric Hum (Passive)", img: "icons/magic/fire/flame-burning-hand-white.webp", description: "Feral beasts cannot enter Close range of Mwaza-Kasa." }},
                {{ name: "Resonance Symbiosis (Passive)", img: "icons/skills/melee/shield-block-gray-yellow.webp", description: "Humanoids in Close range gain +1 Evasion and +1 Armor." }},
                {{ name: "The Taboo (Reaction)", img: "icons/magic/fire/flame-burning-hand-purple.webp", description: "Staring/touching triggers a Presence Reaction Roll (DC 15). Fail = 2 Stress + Vulnerable." }}
            ]
        }},
        // ── 5. PIP ──
        {{
            name: "Pip",
            type: defaultActorType,
            folder: actorFolder.id,
            img: IMG_PIP,
            prototypeToken: {{
                bar1: {{ attribute: "resources.hitPoints" }},
                bar2: {{ attribute: "resources.stress" }},
                displayBars: 40,
                displayName: 20,
                prependAdjective: false
            }},
            system: {{
                tier: "1",
                type: "support",
                traits: {{ agility: {{ value: 3 }}, instinct: {{ value: 1 }}, strength: {{ value: 0 }}, presence: {{ value: 3 }}, finesse: {{ value: 2 }}, knowledge: {{ value: 1 }} }},
                resources: {{ hitPoints: {{ value: 0, max: 4 }}, stress: {{ value: 0, max: 4, isReversed: true }} }},
                evasion: 13,
                difficulty: 13,
                damageThresholds: {{ major: 12, severe: 22 }},
                motives: "Quartermaster & bacon pastry supplier. Screams to distract attackers.",
                notes: pageNPCPip,
                biography: pageNPCPip,
                attack: {{
                    name: "Pastry Tossing & Flare",
                    img: "icons/weapons/wands/wand-carved-fire.webp",
                    type: "attack",
                    range: "close",
                    roll: {{ type: "attack", trait: null, difficulty: null, bonus: 3, advState: "neutral", diceRolling: {{ multiplier: "flat", flatMultiplier: 1, dice: "d6", compare: null, treshold: null }}, useDefault: false }},
                    damage: {{ parts: [{{ type: ["magical"], value: {{ multiplier: "flat", flatMultiplier: 1, dice: "d6", bonus: 3, custom: {{ enabled: false, formula: "" }} }}, applyTo: "hitPoints", resultBased: false, base: false }}], includeBase: false, direct: false }},
                    description: "Fires Kael's speaking-stone flare or hurls dense hardtack pastries."
                }}
            }},
            features: [
                {{ name: "Emergency Pastry Supply (Action)", img: "icons/skills/melee/sword-winged-holy-orange.webp", description: "Spend 1 Hope -> Share a saved bacon pastry with a Close ally to clear 1 Stress." }},
                {{ name: "Hysterical Distraction (Reaction)", img: "icons/creatures/abilities/bear-roar-bite-brown-green.webp", description: "When an ally is attacked, Pip screams at the top of her lungs ('LET ME GO YOU STUPID BIRD!'), giving the attacker Disadvantage." }}
            ]
        }},
        // ── 6. BRAMBLE ──
        {{
            name: "Bramble",
            type: defaultActorType,
            folder: actorFolder.id,
            img: IMG_BRAMBLE,
            prototypeToken: {{
                bar1: {{ attribute: "resources.hitPoints" }},
                bar2: {{ attribute: "resources.stress" }},
                displayBars: 40,
                displayName: 20,
                prependAdjective: false
            }},
            system: {{
                tier: "1",
                type: "support",
                traits: {{ agility: {{ value: 1 }}, instinct: {{ value: 3 }}, strength: {{ value: 4 }}, presence: {{ value: 2 }}, finesse: {{ value: 0 }}, knowledge: {{ value: 2 }} }},
                resources: {{ hitPoints: {{ value: 0, max: 7 }}, stress: {{ value: 0, max: 5, isReversed: true }} }},
                evasion: 11,
                difficulty: 15,
                damageThresholds: {{ major: 16, severe: 28 }},
                motives: "Tree Fortress tank. Anchors cables & projects Root Ramparts around allies.",
                notes: pageNPCBramble,
                biography: pageNPCBramble,
                attack: {{
                    name: "Root-Vine Slam",
                    img: "icons/skills/melee/strike-blade-hooked-orange-blue.webp",
                    type: "attack",
                    range: "melee",
                    roll: {{ type: "attack", trait: null, difficulty: null, bonus: 4, advState: "neutral", diceRolling: {{ multiplier: "flat", flatMultiplier: 1, dice: "d6", compare: null, treshold: null }}, useDefault: false }},
                    damage: {{ parts: [{{ type: ["physical"], value: {{ multiplier: "flat", flatMultiplier: 2, dice: "d8", bonus: 4, custom: {{ enabled: false, formula: "" }} }}, applyTo: "hitPoints", resultBased: false, base: false }}], includeBase: false, direct: false }},
                    description: "Heavy slam with petrified root-vines."
                }}
            }},
            features: [
                {{ name: "Tree Fortress Anchor (Passive)", img: "icons/skills/melee/shield-block-gray-yellow.webp", description: "Grants +2 bonus to all Gondola Equilibrium stabilization rolls while anchored." }},
                {{ name: "Root Rampart (Action)", img: "icons/magic/lightning/barrier-shield-orb-pink.webp", description: "Mark 1 Stress -> Wove instant timber shields around a Close ally (+2 Armor Slots & Vanguard Protection for 1 round)." }}
            ]
        }},
        // ── 7. KAEL ──
        {{
            name: "Kael",
            type: defaultActorType,
            folder: actorFolder.id,
            img: IMG_KAEL,
            prototypeToken: {{
                bar1: {{ attribute: "resources.hitPoints" }},
                bar2: {{ attribute: "resources.stress" }},
                displayBars: 40,
                displayName: 20,
                prependAdjective: false
            }},
            system: {{
                tier: "1",
                type: "support",
                traits: {{ agility: {{ value: 1 }}, instinct: {{ value: 2 }}, strength: {{ value: 0 }}, presence: {{ value: 1 }}, finesse: {{ value: 3 }}, knowledge: {{ value: 4 }} }},
                resources: {{ hitPoints: {{ value: 0, max: 4 }}, stress: {{ value: 0, max: 4, isReversed: true }} }},
                evasion: 12,
                difficulty: 14,
                damageThresholds: {{ major: 13, severe: 24 }},
                motives: "Signal Tech genius. Tunes Speaking Stones to boost Mwaza-Kasa Sync.",
                notes: pageNPCKael,
                biography: pageNPCKael,
                attack: {{
                    name: "Acoustic Shockwave",
                    img: "icons/weapons/swords/sword-flanged-lightning.webp",
                    type: "attack",
                    range: "close",
                    roll: {{ type: "attack", trait: null, difficulty: null, bonus: 3, advState: "neutral", diceRolling: {{ multiplier: "flat", flatMultiplier: 1, dice: "d6", compare: null, treshold: null }}, useDefault: false }},
                    damage: {{ parts: [{{ type: ["magical"], value: {{ multiplier: "flat", flatMultiplier: 2, dice: "d6", bonus: 2, custom: {{ enabled: false, formula: "" }} }}, applyTo: "hitPoints", resultBased: false, base: false }}], includeBase: false, direct: false }},
                    description: "Discharges acoustic feedback through Speaking Stone resonators."
                }}
            }},
            features: [
                {{ name: "Speaking Stone Frequency Relay (Action)", img: "icons/magic/lightning/barrier-shield-orb-pink.webp", description: "Tune Speaking Stone to Mwaza-Kasa's frequency (+1 bonus to all Mwaza-Kasa Sync rolls)." }},
                {{ name: "Tension Calibration (Passive)", img: "icons/skills/melee/shield-damaged-broken-gold.webp", description: "Umber crystal anchors absorb wind shear, reducing environmental hazard damage to Tree Fortress allies by 3." }}
            ]
        }},
        // ── 8. SAFFRON ──
        {{
            name: "Saffron",
            type: defaultActorType,
            folder: actorFolder.id,
            img: IMG_SAFFRON,
            prototypeToken: {{
                bar1: {{ attribute: "resources.hitPoints" }},
                bar2: {{ attribute: "resources.stress" }},
                displayBars: 40,
                displayName: 20,
                prependAdjective: false
            }},
            system: {{
                tier: "1",
                type: "support",
                traits: {{ agility: {{ value: 2 }}, instinct: {{ value: 3 }}, strength: {{ value: 1 }}, presence: {{ value: 1 }}, finesse: {{ value: 4 }}, knowledge: {{ value: 2 }} }},
                resources: {{ hitPoints: {{ value: 0, max: 4 }}, stress: {{ value: 0, max: 3, isReversed: true }} }},
                evasion: 14,
                difficulty: 13,
                damageThresholds: {{ major: 13, severe: 23 }},
                motives: "Scout & cartographer. Sketches beast weak points to grant Advantage.",
                notes: pageNPCSaffron,
                biography: pageNPCSaffron,
                attack: {{
                    name: "Precision Stylus Strike",
                    img: "icons/skills/melee/strike-dagger-skull-white.webp",
                    type: "attack",
                    range: "melee",
                    roll: {{ type: "attack", trait: null, difficulty: null, bonus: 3, advState: "neutral", diceRolling: {{ multiplier: "flat", flatMultiplier: 1, dice: "d6", compare: null, treshold: null }}, useDefault: false }},
                    damage: {{ parts: [{{ type: ["physical"], value: {{ multiplier: "flat", flatMultiplier: 1, dice: "d8", bonus: 3, custom: {{ enabled: false, formula: "" }} }}, applyTo: "hitPoints", resultBased: false, base: false }}], includeBase: false, direct: false }},
                    description: "Targeted strike on anatomical weak points."
                }}
            }},
            features: [
                {{ name: "Anatomical Sketch (Action)", img: "icons/skills/melee/blade-tip-chipped-blood-red.webp", description: "Spend 1 Hope -> Sketch a target creature. All Squad 907/06 attacks against it gain Advantage for 1 round." }},
                {{ name: "Unbothered Focus (Passive)", img: "icons/magic/fire/flame-burning-hand-white.webp", description: "Saffron ignores environmental storm hazards and pitch instability while sketching." }}
            ]
        }}
    ];

    for (let data of actorDefinitions) {{
        let actor = game.actors.find(a => a.name === data.name || (legacyActorNames[data.name] && legacyActorNames[data.name].includes(a.name)));
        if (!actor) {{
            console.log("Creating new Actor & Primary Attack:", data.name);
            const res = await Actor.create(data);
            actor = Array.isArray(res) ? res[0] : res;
            if (actor) {{
                ui.notifications.info("Created Actor: " + actor.name);
            }}
        }} else {{
            console.log("Refreshing existing Actor & Primary Attack:", data.name);
            
            // SMART ARTWORK PRESERVATION:
            const isDefaultIcon = !actor.img || actor.img.startsWith("icons/svg/") || 
                                  actor.img.includes("blood-slash-foam-red") || 
                                  actor.img.includes("claw-talons") || 
                                  actor.img.includes("strike-hand-glow") || 
                                  actor.img.includes("barrier-fire-pink");
            const finalImg = (actor.img && !isDefaultIcon) ? actor.img : data.img;

            await actor.update({{
                name: data.name,
                img: finalImg,
                system: data.system,
                "prototypeToken.bar1": {{ attribute: "resources.hitPoints" }},
                "prototypeToken.bar2": {{ attribute: "resources.stress" }},
                "prototypeToken.displayBars": 40,
                "prototypeToken.displayName": 20,
                "prototypeToken.prependAdjective": data.prototypeToken?.prependAdjective ?? false
            }});
            
            const oldItemIds = actor.items.map(i => i.id);
            if (oldItemIds.length > 0) {{
                await actor.deleteEmbeddedDocuments("Item", oldItemIds);
            }}
            ui.notifications.info("Refreshed Actor & Native Attack: " + actor.name);
        }}

        if (actor) {{
            const itemsToCreate = [];
            if (data.system.attack) {{
                itemsToCreate.push({{
                    name: data.system.attack.name,
                    type: "attack",
                    img: data.system.attack.img,
                    system: data.system.attack
                }});
            }}
            if (data.features) {{
                for (let f of data.features) {{
                    itemsToCreate.push({{
                        name: f.name,
                        type: "feature",
                        img: f.img,
                        system: {{ description: f.description, actions: f.actions || {{}} }},
                        effects: f.effects || []
                    }});
                }}
            }}
            if (itemsToCreate.length > 0) {{
                await actor.createEmbeddedDocuments("Item", itemsToCreate);
            }}
        }}
    }}

    // ── 3. DYNAMICALLY BUILD MASTER PREP & TACTICAL OVERVIEW WITH @UUID LINKS ──
    const pageUUIDMap = {{}};
    for (let page of dmJournal.pages) {{
        pageUUIDMap[page.name] = page.uuid;
    }}

    const actorUUIDMap = {{}};
    for (let actorDef of actorDefinitions) {{
        const act = game.actors.find(a => a.name === actorDef.name);
        if (act) actorUUIDMap[act.name] = act.uuid;
    }}

    {getP_code}
    {getA_code}

    const masterOverviewHTML = `
      <div style="font-family: 'Signika', sans-serif; color: #e0e0e0; line-height: 1.6;">
        <h1 style="color: #81c784; border-bottom: 3px solid #81c784; padding-bottom: 6px; margin-bottom: 12px;">
          ⚔️ TEMPEST CLEARING & TREE FORTRESS — MASTER TACTICAL OVERVIEW
        </h1>

        <div style="background: rgba(46, 125, 50, 0.15); border-left: 4px solid #81c784; padding: 12px 16px; border-radius: 6px; margin-bottom: 16px;">
          <h3 style="color: #a5d6a7; margin: 0 0 6px 0;">🎯 DM Prep Brief & Scenario Objective</h3>
          <p style="margin: 0; color: #e8f5e9;">
            Squad 907 and Squad 06 are trapped atop the living Tree Fortress and Canopy Raft as an Eyewall Storm Surge sweeps across Sector 3.
            The PCs must defend the fortress, manage gondola pitch equilibrium, rescue Pip from a Storm Raptor, and commune with <strong>` + getA("Mwaza-Kasa") + `</strong> to activate the <em>Sheltering Sentinel</em> dome before dawn extraction arrives.
          </p>
        </div>

        <h2 style="color: #ffd54f; border-bottom: 1px solid rgba(255,213,79,0.3); padding-bottom: 4px; margin-top: 20px;">
          📜 Woven Battle Flow & Scene Escalation
        </h2>

        <!-- PHASE 1 -->
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); padding: 12px 16px; border-radius: 6px; margin-bottom: 12px;">
          <h3 style="color: #ba68c8; margin: 0 0 8px 0;">Phase 1: Eyewall Opening & Pastry Rescue</h3>
          <p style="margin: 0 0 8px 0;">
            As 80-knot eyewall gusts tear across the canopy clearing, airborne ` + getA("Storm Raptor") + ` beasts dive from the fog. One snatches <strong>Pip</strong> off the deck while she clutches her hardtack bacon pastries.
            Simultaneously, a swarm of ` + getA("Mwaza-Bobcat Swarm") + ` minions scrambles up the winch cables toward Kael's communication rig.
          </p>
          <p style="margin: 0; font-size: 0.95em; color: #b388ff;">
            🔗 <strong>Interactive Links:</strong> ` + getP("Pip & Storm Hawk Pastry Rescue") + ` | ` + getP("Wave 1: Aerial & Canopy Swarm") + ` | ` + getP("Gondola Equilibrium (Countdown 8)") + `
          </p>
        </div>

        <!-- PHASE 2 -->
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); padding: 12px 16px; border-radius: 6px; margin-bottom: 12px;">
          <h3 style="color: #ffb74d; margin: 0 0 8px 0;">Phase 2: Jaguar Assault & Mid-Air Chaos</h3>
          <p style="margin: 0 0 8px 0;">
            A telepathic ` + getA("Mwaza-Chui") + ` (Memory Jaguar) pounces onto the deck, hunting active mind-links and spellcasters.
            The PCs must split focus between rescuing Pip in mid-air, stabilizing deck pitch, and hauling ` + getA("Mwaza-Kasa") + ` onto the tree node while ` + getA("Bramble") + ` anchors the winch cables and ` + getA("Kael") + ` operates the radio relay.
          </p>
          <p style="margin: 0; font-size: 0.95em; color: #ffcc80;">
            🔗 <strong>Interactive Links:</strong> ` + getP("Wave 2: Jaguar Assault & Mid-Air Rescue") + ` | ` + getP("Radio & Speaking Stone Relay") + ` | ` + getP("Eyewall Storm Surge (Countdown 6)") + `
          </p>
        </div>

        <!-- PHASE 3 -->
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); padding: 12px 16px; border-radius: 6px; margin-bottom: 12px;">
          <h3 style="color: #4fc3f7; margin: 0 0 8px 0;">Phase 3: Eyewall Peak & Sheltering Sentinel Climax</h3>
          <p style="margin: 0 0 8px 0;">
            The eyewall storm surge hits peak intensity. Completing 4 ticks on the ` + getP("Mwaza-Kasa Sync (Countdown 4)") + ` anchors the Spirit Tortoise into the petrified tree node, projecting an impenetrable <em>Aetheric Shell-Wall dome</em> around the raft and tree fortress to guarantee survival until extraction.
          </p>
          <p style="margin: 0; font-size: 0.95em; color: #81d4fa;">
            🔗 <strong>Interactive Links:</strong> ` + getP("Wave 3: Eyewall Peak & Sheltering Sentinel") + ` | ` + getP("Dawn Survival (Countdown 8)") + ` | ` + getP("Mwaza-Kasa (Support)") + `
          </p>
        </div>

        <!-- SQUAD 06 ALLY ACTION MATRIX -->
        <h2 style="color: #81c784; border-bottom: 1px solid rgba(129,199,132,0.3); padding-bottom: 4px; margin-top: 20px;">
          🤝 Squad 06 Support & Reaction Matrix
        </h2>
        <table style="width: 100%; border-collapse: collapse; margin-top: 8px; font-size: 0.95em;">
          <thead>
            <tr style="background: rgba(255,255,255,0.08); text-align: left; color: #81c784;">
              <th style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);">Ally</th>
              <th style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);">Tactical Role & Reaction Trigger</th>
              <th style="padding: 8px; border-bottom: 1px solid rgba(255,255,255,0.2);">Mechanic & Direct Link</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 8px;">🌸 <strong>Pip</strong></td>
              <td style="padding: 8px;">Quartermaster / Mid-Air Rescue Trigger (Screams give Disadvantage to attackers)</td>
              <td style="padding: 8px;">Clears 1 Stress (Bacon Pastry) & Distraction. ` + getP("Pip (Support)") + ` | ` + getA("Pip") + `</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 8px;">🌿 <strong>Bramble</strong></td>
              <td style="padding: 8px;">Defender Tank (Triggers Root Rampart when allies take major damage)</td>
              <td style="padding: 8px;">Lashes winch lines (+2 Equilibrium) & Root Rampart (+2 Armor Slots). ` + getP("Bramble (Support)") + ` | ` + getA("Bramble") + `</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 8px;">⚙️ <strong>Kael</strong></td>
              <td style="padding: 8px;">Signal Tech (Operates Speaking Stones; panics if Bobcats chew cables)</td>
              <td style="padding: 8px;">Relays Aggie's voice (+1 Sync rolls) & Acoustic Shockwave. ` + getP("Kael (Support)") + ` | ` + getA("Kael") + `</td>
            </tr>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
              <td style="padding: 8px;">🎨 <strong>Saffron</strong></td>
              <td style="padding: 8px;">Scout / Cartographer (Sketches beast weak points & telepathic decoys)</td>
              <td style="padding: 8px;">Anatomical Sketch (Advantage on PC damage) & Unbothered Focus. ` + getP("Saffron (Support)") + ` | ` + getA("Saffron") + `</td>
            </tr>
          </tbody>
        </table>

        <!-- GM FEAR & HAZARD QUICK-LOOK -->
        <h2 style="color: #ba68c8; border-bottom: 1px solid rgba(186,104,200,0.3); padding-bottom: 4px; margin-top: 20px;">
          🔥 GM Fear Spending & Reaction Quick-Look
        </h2>
        <p style="margin-top: 6px;">
          Keep <strong>` + getP("Fear Spending & Reaction Options") + `</strong> open on your GM screen during combat to trigger Hurricane Gales, Raptor Snatches, or Mwaza-Chui Mirror-Steps!
        </p>
      </div>
    `;

    const overviewPage = dmJournal.pages.contents.find(p => p.name.includes("Master Tactical Overview"));
    if (overviewPage) {{
        await overviewPage.update({{ text: {{ content: masterOverviewHTML, format: 1 }} }});
    }}

    ui.notifications.info("🎉 Tempest Clearing Setup Complete! Prototype tokens configured to prepend random adjectives for Adversaries!");
}})();
"""

out_file = r"d:\Code\vumbua\meta\foundry-exports\tempest_clearing_macro.js"
with open(out_file, "w", encoding="utf-8") as f:
    f.write(macro_js_content.strip())

print(f"Generated {out_file} successfully.")
