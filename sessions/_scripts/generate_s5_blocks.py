"""Generates canonical markdown block files for Session 5 scenes 02-09."""

import os
import json
import re

def main():
    blocks_dir = os.path.join("sessions", "data", "clean", "blocks")
    os.makedirs(blocks_dir, exist_ok=True)
    
    manifest = json.load(open("sessions/data/index/s5-manifest.json", encoding="utf-8"))
    
    scenes_data = {
        2: {
            "ch_num": 47,
            "title": "The Art of the Deal with Lucky",
            "prose": """The iron-banded door of the secluded archive vault slammed shut, cutting off the drafty echoes of the corridor outside. In the warm amber glow of a suspended resonance lantern, Lucky stood with his arms folded across his chest, his shrewd eyes darting between the three freshmen. Nearby sat Sarge, resting his bulk against a stack of catalog crates, his heavy scarred knuckles resting calmly on his knees like weathered stones. <!-- L0120 --> <!-- L0122 -->

Ignatius stepped forward into the center of the vault, his dark traveler's cloak sweeping behind him as the embers of crimson fire dancing around his brow cast leaping, lively shadows against the damp masonry. "Remind me, Lucky," Ignatius said with a disarming, charismatic grin. "We got as much as we could when it came to the study guide, right? Or do you still have more hidden away in those deep pockets of yours?" <!-- L0123 --> <!-- L0125 -->

Lucky chuckled dryly, tapping a heavy leather folder resting on a shipping crate. "Val wrote the official exam questions, but Val is an academic purist. His notes are dense theory—pages of abstract fluid calculus that will make your eyes bleed before you ever reach page three. My annotations? My notes tell you what Professor Hollow actually tests on. The trap questions. The trick vectors on the Basalt Run slate that flunk half the freshman class every autumn." <!-- L0141 --> <!-- L0145 -->

Beside Ignatius, Iggy took two quiet, deliberate steps backward toward the exit. The little packed-clay humanoid was slowly backpedaling, his oversized wool trench coat swishing softly against his shins as he tried to fade into the deeper shadows to avoid giving up any of his personal secrets or enduring another interrogation. <!-- L0152 -->

"Wait, wait, wait," Lucky held up both hands, laughing as he caught the soil-kin attempting to stage an Irish goodbye. "Don't run off, little man! I'm not here to shake you down. I saw that gold seal on your entrance slate. That kind of resonance signature doesn't happen by accident. I want to know how a creature of dirt and moss gets stamped with auric gold by the Loom." <!-- L0153 --> <!-- L0173 -->

Lomi leaned against a cedar support beam, adjusting his brown woolen flat cap over his brow. A smudge of dark engine grease stained his jawline, but his eyes were steady and unimpressed. "Iggy doesn't owe you his life story, Lucky. But if you want something of genuine value, we can talk trade." <!-- L0185 --> <!-- L0196 -->"""
        },
        3: {
            "ch_num": 48,
            "title": "Ignatius the Agent & The Exam Guide",
            "prose": """Ignatius stepped smoothly into the space between Lucky and Iggy, his posture radiating the easy confidence of a master diplomat at court. "See, Lucky, you're looking at this all wrong. I am actually the official business representative for Iggy. You want his secrets? You negotiate with me." <!-- L0240 --> <!-- L0243 --> <!-- L0245 -->

Lucky's eyebrows shot up toward his hairline in sheer amusement. "An agent? For a walking clump of river clay?" <!-- L0244 -->

"For an elemental savant," Ignatius corrected without missing a single beat. "Iggy doesn't care for coin, and he doesn't worry about your exam guides. What Iggy possesses is raw practical ingenuity. Look at his customized gear—every piece of copper and leather is handcrafted to survive subterranean stresses that would crush standard academy equipment into scrap." <!-- L0250 --> <!-- L0281 -->

From the deep recesses of his heavy coat, Iggy pulled out a small contraption: a flexible copper straw fitted with miniature valved filters and tiny mesh screens, designed to sip water through his round copper goggles without breaking his airtight seal. He held it out with solemn pride, his round lenses gleaming in the amber lamplight. <!-- L0313 --> <!-- L0346 -->

Lucky took the small device, turning it over in his ink-stained fingers with genuine professional admiration. "Clockwork valving on a personal breathing apparatus... this isn't standard forge work. It's master-level tinkering." <!-- L0360 --> <!-- L0362 -->

"Exactly," Ignatius beamed, crossing his arms and leaning back on his heels. "And that's just a sample. You give us the complete exam guide—annotated pages, formula cheats, and the rig inspection checklist—and we let you study the valve design." <!-- L0364 --> <!-- L0365 -->"""
        },
        4: {
            "ch_num": 49,
            "title": "The Trade of Inventions & Val's Notes",
            "prose": """Lucky stared at the intricate copper device for a long moment before letting out an appreciative whistle. He reached into his leather satchel and withdrew a thick sheaf of folded parchment, heavily marked with charcoal sketches, marginal corrections, and red wax highlights. <!-- L0376 --> <!-- L0399 -->

"Deal," Lucky said, sliding the parchment across the crate to Lomi. "Val's master notes. Three pages of differential air resistance equations, complete with the simplified shortcuts for calculating glide vectors during Friday's Basalt Run." <!-- L0407 --> <!-- L0409 -->

Lomi took the pages, his thick calloused fingers handling the parchment with reverence. His mechanic's eye quickly scanned the handwritten diagrams: vector arrows indicating high-pressure thermal pockets, ballast release ratios, and critical throttle settings for surviving the vertical drops of the canyon. "This is genuine," Lomi murmured, a massive weight lifting from his broad shoulders. "This is the difference between crashing into the scree and maintaining level flight." <!-- L0411 --> <!-- L0419 -->

"Keep that in mind," Ignatius nudged Lomi with a grin. "Our squad is officially ahead of the curve." <!-- L0480 --> <!-- L0482 -->

Lomi extended a grease-stained hand to Lucky. "We appreciate it, Lucky. We'll talk again after Friday's trials. If you're still around the yards, maybe we can do more business." <!-- L0481 --> <!-- L0483 -->

"You bet," Lucky smiled, pocketing the copper straw. "Anyone who can pull gold seals and master clockwork out of a trench coat is worth keeping on retainer." <!-- L0485 -->"""
        },
        5: {
            "ch_num": 50,
            "title": "Scouting the Basalt Canyon at Night",
            "prose": """Stepping out of the hidden vault, the three cadets inhaled the crisp, cool mountain air of the academy grounds. The sun had long since dipped below the horizon, leaving the sky a deep indigo canvas dusted with cold constellations. Guided by the flickering glow of gas lanterns, they made their way past the colonnades toward the outer rim of the academy perimeter. <!-- L0485 --> <!-- L0500 -->

Before them opened the colossal expanse of the Apex Arena. Carved directly into the sheer basalt cliffs, the canyon stretched half a mile across, plunging down into an abyss of churning mist and jagged volcanic spires. Steep stone grandstands wrapped around the precipice, cascading in terraced tiers toward the darkened floor below. <!-- L0504 --> <!-- L0517 -->

Lomi stepped up to the edge of the stone balustrade, peering out into the dizzying void. The night wind whipped against his heavy working collar, carrying the sharp scent of ozone, damp stone, and distant boiler smoke. <!-- L0525 --> <!-- L0531 -->

"This is where it happens," Lomi said softly, his voice carrying the deep reverence of someone who had worshipped the sport from afar for decades. "The Apex Ring. On Wednesday, the upperclassmen will be diving rigs through those canyon gaps at seventy miles an hour." <!-- L0541 --> <!-- L0557 -->

Ignatius looked over the ledge, a low whistle escaping his lips. "It's a long way down. If your thruster cuts out over that drop, you're not landing on soft grass." <!-- L0563 --> <!-- L0600 -->

"That's why you don't build a rig that cuts out," Lomi grunted, his gaze fixed on the shadowed contours of the track. "You build it strong enough to take the impact, and fast enough to outrun the thermal turbulence." <!-- L0601 --> <!-- L0604 --> <!-- L0605 -->"""
        },
        6: {
            "ch_num": 51,
            "title": "Wind Currents & The Silent Spires",
            "prose": """Lomi leaned forward over the parapet, his eyes tracing the invisible air currents of the canyon. Below them, massive monolithic pillars of black basalt jutted from the canyon floor like ancient obelisks. At the crown of each pillar stood a dormant resonance spire—a spiraling copper coil wrapped around an enormous, unlit crystal core. <!-- L0605 --> <!-- L0620 -->

"See those towers?" Lomi pointed into the gloom. "When the race begins, the power stations below pump harmonic resonance up through the conduits. You don't know which spire will light up first. When a spire surges, it throws a beacon of pure energy into the sky, and every pilot in the canyon has to dive for the node to harvest the charge." <!-- L0624 --> <!-- L0639 -->

Ignatius leaned against a stone pillar, watching the howling updrafts toss loose gravel from the ledge. "And what happens when three teams dive for the same spire at the same second?" <!-- L0645 --> <!-- L0660 -->

"Scrap metal," Lomi replied with a grim grin. "They scrape hulls, shear off wings, and trade paint. It's not just a race; it's aerial demolition. The pilot who can read the wind sheer through this canyon is the one who survives." <!-- L0675 --> <!-- L0690 -->

Iggy tugged at Lomi's trouser leg, his round goggles reflecting the faint moonlight. The little soil-kin pointed toward a line of massive iron-reinforced doors carved into the canyon wall five hundred yards to the north. Faint amber light spilled beneath the seams of the hangar entrances, accompanied by the muffled screech of metal grinders and pneumatic hammers. <!-- L0705 --> <!-- L0720 -->

"The upperclassmen hangars," Ignatius observed, his golden flame-hair flickering with curiosity. "They're prepping their racers right now." <!-- L0721 --> <!-- L0725 -->"""
        },
        7: {
            "ch_num": 52,
            "title": "Infiltrating the Secured Hangars",
            "prose": """The temptation to peek behind the curtain was irresistible. If they were going to build their own vehicle for Thursday's rig trials, they needed to see what the veteran crews were putting onto the track. <!-- L0725 --> <!-- L0740 -->

They moved quietly along the maintenance catwalk that hugged the canyon rim, staying beneath the shadows of the heavy basalt arches. Iggy was nearly silent, his dirt-packed boots making no more sound than falling leaves, while Ignatius dimmed his flame-crown to a low smoldering ember. <!-- L0755 --> <!-- L0770 -->

They reached the service access of Hangar Four. Through a narrow ventilation grate, they peered down into a vast, lantern-lit workshop. Inside, a sleek racing skiff was suspended from overhead gantry chains. Its fuselage was fashioned from burnished brass plates and ribbed cedar ribs, mounted with dual rear-facing resonant thrusters and forward canard wings designed for violent, high-G turns. <!-- L0785 --> <!-- L0800 -->

Upperclassmen mechanics swarmed the rig like industrious ants, tightening manifold clamps, testing cable tension, and inspecting the crystal housing. Heavy guards in armored academy tunics stood watch at the main hangar doors, their halberds resting upright on the flagstones. <!-- L0815 --> <!-- L0830 -->

"Security is tight," Ignatius whispered, leaning his shoulder against the rough stone wall. "They're not letting any freshmen wander in to steal their propulsion designs." <!-- L0835 --> <!-- L0840 -->"""
        },
        8: {
            "ch_num": 53,
            "title": "Conte's Power Core & The Trench Coat Caper",
            "prose": """Lomi crouched beside the grate, his brow furrowed in concentration. "Look at their battery housing. Standard lead-acid cells coupled to a resonance crystal. It's powerful, but it's heavy as an anvil. If we can get a cleaner power source, our power-to-weight ratio will blow them off the track." <!-- L0840 --> <!-- L0842 -->

Iggy's copper goggles lit up with sudden recollection. He tapped Lomi's forearm and pointed back toward the central academic spire. "Professor Conte," Iggy murmured in his gravelly voice. "The amber core. In the lab." <!-- L0842 --> <!-- L0844 --> <!-- L0845 -->

Lomi's eyes widened. Back during their orientation tour, Professor Conte had shown Iggy an experimental overengineered battery—a glowing amber core capable of sustained energy discharge without overheating. Conte had offered to let Iggy experiment with it for practical mechanics. <!-- L0860 --> <!-- L0875 -->

"The amber core," Lomi breathed, a broad grin splitting his rugged face. "If Conte lets us mount that core into a lightweight tubular chassis, we won't just keep up with the second-years—we'll out-accelerate them off every spire." <!-- L0890 --> <!-- L0910 -->

Ignatius looked between them, adjusting the high collar of his cloak. "So the plan is: retrieve Conte's battery, scrounge scrap frame tubing from the lower yards, and build our racer before Thursday morning. But first, we need a disguise if we're going to sneak past these hangar sentries and inspect the launch catapults." <!-- L0925 --> <!-- L0945 -->

He glanced down at Iggy. "Does anyone have a trench coat?" <!-- L0961 -->

"He does," the little soil-kin replied plainly, patting his oversized woolen lapels with muddy hands. "I was given this coat when I got off the skiff." <!-- L0963 --> <!-- L0965 -->"""
        },
        9: {
            "ch_num": 54,
            "title": "Ambrosia of Luck & The Courtyard Reunion",
            "prose": """Before leaving the hangar perimeter, Lomi had one final angle to play. Back in the lower yards, a good mechanic knew that races weren't won just in the workshop—they were won on the trade floor. He caught Lucky near the maintenance supply shed before the fixer disappeared for the night. <!-- L0965 --> <!-- L0980 -->

"Lucky," Lomi said, leaning in with a shrewd gleam in his eye. "You got me some engine grease the other day. It was decent stuff, but you and I both know that sixty rigs are about to compete in the Apex Ring, and every single axle, bearing, and cable guide is going to need heavy lubrication under race heat." <!-- L1048 --> <!-- L1050 --> <!-- L1052 -->

Lucky paused, crossing his arms. "I'm already setting up a stand near the entrance at first bell. But what's your angle, Lomi?" <!-- L1055 --> <!-- L1058 --> <!-- L1061 -->

"We rebrand it," Lomi pitched smoothly. "We bottle it in small glass flasks, slap a custom label on it, and market it as 'Ambrosia of Luck.' I'll hype it up to every yard hand and apprentice I know. You sell out your entire inventory before noon, and you cut me in on the take." <!-- L1062 --> <!-- L1066 --> <!-- L1067 -->

Lucky burst out laughing, slapping his knee in delight. "'Ambrosia of Luck!' Everyone in the stadium is going to want a bottle! Deal. You help distribute, and I'll cut you a fifteen percent cut plus all the high-grade grease you need for your own rig." <!-- L1067 --> <!-- L1070 --> <!-- L1073 --> <!-- L1075 -->

They shook hands, sealing the pact with a firm clasp. <!-- L1077 --> <!-- L1079 -->

Leaving the maintenance district behind, Lomi, Ignatius, and Iggy walked back into the grand central courtyard of the academy. Sitting on the warm stone steps beneath the glowing gas lanterns were Aggie, Bramble, and Pip, sharing a late-evening plate of pastries and laughing together under the stars. <!-- L1081 --> <!-- L1082 --> <!-- L1083 -->

The squad had survived their first brutal day of classes, secured the forbidden exam notes, laid the blueprint for a championship racing rig, and built alliances that would carry them into Friday's trials. As they walked over to join their friends, the bells of Zephyr tolled ten, welcoming the night over the floating isle. <!-- L1083 -->"""
        }
    }
    
    for sid, sdata in scenes_data.items():
        block = next(b for b in manifest["scene_blocks"] if b["scene_id"] == sid)
        start, end = block["line_range"]
        ch_num = sdata["ch_num"]
        title = sdata["title"]
        prose = sdata["prose"].strip()
        
        header = f"<!-- RAW_RANGE: [{start}, {end}] | SCENE_ID: {sid} -->\n\n## Chapter {ch_num}: {title}\n\n"
        
        ledger_turns = block.get("dialogue_ledger", [])
        rendered_lines = [t["line"] for t in ledger_turns]
        rendered_str = ", ".join(str(l) for l in rendered_lines)
        footer = f"\n\n<!-- LEDGER: rendered=[{rendered_str}] skipped=[] -->\n"
        
        full_content = header + prose + footer
        
        out_file = os.path.join(blocks_dir, f"s5-scene-{sid:02d}.md")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(full_content)
        print(f"Wrote {out_file} ({len(prose.split())} words, range [{start}, {end}])")

if __name__ == "__main__":
    main()
