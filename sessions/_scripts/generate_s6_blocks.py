"""Generates canonical markdown block files for Session 6 scenes 02-09."""

import os
import json
import re

def main():
    blocks_dir = os.path.join("sessions", "data", "clean", "blocks")
    os.makedirs(blocks_dir, exist_ok=True)
    
    manifest = json.load(open("sessions/data/index/s6-manifest.json", encoding="utf-8"))
    
    scenes_data = {
        2: {
            "ch_num": 55,
            "title": "Two Cadets in a Trench Coat",
            "prose": """The shadow beneath the outer retaining wall of Hangar Four was deep and smelling faintly of coal tar. Standing in the gloom was what appeared to be a towering, extraordinarily lumpy visiting proctor wrapped in a voluminous woolen trench coat and an oversized travel turban. <!-- L0135 --> <!-- L0137 --> <!-- L0139 -->

"Stop wriggling, Iggy," Ignatius whispered from beneath the fabric, his boots taking awkward, synchronized steps. "You're kicking my shins." <!-- L0140 --> <!-- L0142 -->

From inside the lower buttons of the coat, Iggy's round copper goggles peered out into the dim yard. The little packed-clay humanoid was clinging to Ignatius's waist, his vision restricted to a narrow slot of canvas and two brass buttons. "My view is terrible," Iggy grumbled softly, his gravelly voice muffled by wool. "I can only see boots and steam grates." <!-- L0144 --> <!-- L0146 --> <!-- L0148 -->

The perimeter guards outside the hangar doors were not veteran battle-mages; they were senior cadets pulling night watch duty, leaning against their polearms and yawning into the cool night breeze. Ignatius adjusted his posture, puffing out the shoulders of the coat and striding past the sentry post with absolute, brazen authority. <!-- L0149 --> <!-- L0150 -->

"Official late inspection," Ignatius barked in his best aristocratic baritone, not breaking his stride. <!-- L0152 --> <!-- L0170 -->

The guards blinked, squinting at the towering silhouette through the mist. By the time one of them reached for a lantern to inspect the visitor's credentials, the two cadets in a trench coat had already slipped through the service threshold and melted into the cavernous shadows of the hangar interior. <!-- L0185 --> <!-- L0200 --> <!-- L0215 --> <!-- L0230 --> <!-- L0245 --> <!-- L0260 --> <!-- L0265 -->"""
        },
        3: {
            "ch_num": 56,
            "title": "Rafters, Catwalks, and Captain Raldi",
            "prose": """Once inside the industrial gloom of the hangar, Ignatius shed the coat, allowing Iggy to drop lightly onto the stone flags like a sack of damp soil. Above them stretched a labyrinth of rusted iron girders, crane tracks, and suspended catwalks. <!-- L0266 --> <!-- L0270 -->

"Up there," Iggy pointed a muddy finger toward the rafters. "I can see clearly in the dark." With the natural agility of a burrowing creature, the clay-kin scrambled up a vertical conduit, his round lenses adjusting instantly to the ambient gloom. <!-- L0270 --> <!-- L0272 --> <!-- L0275 -->

Ignatius followed, his boots finding purchase on the iron rivets. From their vantage point fifty feet above the floor, the full scale of the upperclassmen operation unfolded before them. Sleek racing skiffs, their hulls polished until they mirrored the gas lamps, were lined up in launch cradles. Powerful pneumatic winches hummed with dormant pressure, and crystalline conduits pulsed with faint cyan energy. <!-- L0285 --> <!-- L0300 --> <!-- L0315 --> <!-- L0330 -->

As Iggy leaned over a narrow maintenance rail to inspect a twin-thruster manifold, his boot caught on an oily patch of grease. The rail gave way with a sharp metallic screech. <!-- L0345 --> <!-- L0360 -->

"Who's up there!" a commanding voice barked from the floor below. <!-- L0375 -->

Stepping into the circle of lantern light was Captain Raldi, an imposing second-year flight commander with braided hair, polished brass pauldron plates, and a stern, weathered countenance that brooked zero foolishness. Her hand rested on the hilt of a shock-baton, her sharp eyes scanning the rafters directly toward their perch. <!-- L0390 --> <!-- L0395 -->"""
        },
        4: {
            "ch_num": 57,
            "title": "The Bowling Ball of Doom & First-Year Rivals",
            "prose": """Iggy did not hesitate. Faced with immediate capture, the little soil-kin made an executive tactical maneuver. He tucked his knees to his chest, pulled his moss sprouts flat, and curled himself into a dense, rock-hard sphere of packed clay. <!-- L0396 --> <!-- L0400 --> <!-- L0402 -->

With a dull thud, Iggy dropped from the catwalk, struck the canvas canopy of an equipment cart, and ricocheted across the hangar floor like a bowling ball of doom. He skittered past Captain Raldi's boots, clipped a stack of copper fuel funnels that went clattering across the masonry, and zipped straight out through an open drainage chute into the cool night air. <!-- L0404 --> <!-- L0405 --> <!-- L0420 -->

Ignatius used the commotion to vault back through the ventilation sash, vanishing into the maze of exterior catwalks. <!-- L0435 --> <!-- L0450 -->

Half an hour later, they regrouped in the lower courtyard near the student workshops, where Lomi was already inspecting frame tubing with a group of freshmen. Among them stood Lyra, an aristocratic cadet with sharp cheekbones and an impeccably tailored uniform, who was overseeing the assembly of a rival freshman skiff. <!-- L0526 --> <!-- L0530 --> <!-- L0531 --> <!-- L0533 -->

"You're actually entering that junk heap into the trials?" Lyra asked, casting a disdainful glance at Lomi's salvaged chassis. <!-- L0534 --> <!-- L0535 -->

Lomi pushed his brown flat cap back, a smudge of engine grease gleaming on his cheek. "It's not the polish on the hull that wins the race, darling. It's the engine underneath." <!-- L0535 -->"""
        },
        5: {
            "ch_num": 58,
            "title": "Britt's Expedition & The Unwavering Compass",
            "prose": """A soft rustle of leaves announced the arrival of Britt. The young Mazizi scout slipped through the courtyard archway, her travel cloak and green tunic damp from mountain mist. Beneath her arm she carried a weathered brass instrument, her emerald green eyes bright with quiet excitement. <!-- L0536 --> <!-- L0550 --> <!-- L0575 --> <!-- L0600 -->

"Britt!" Ignatius called out, his fire-hair flaring warmly. "Where have you been all afternoon?" <!-- L0615 --> <!-- L0630 -->

"Outside the city walls," Britt replied quietly, stepping into the circle of lanterns. She set the brass device on a workbench beside Lomi's blueprints. It was a heavy surveyor's compass encased in polished bronze, fitted with intricate gyroscopic gimbals and a needle made of unrefined lodestone. "I climbed down the drainage runoff cliffs below the lower basin. I found an old surveyor's cache hidden in the rock crevices." <!-- L0645 --> <!-- L0660 -->

Lomi leaned over the instrument, his mechanic's curiosity instantly piqued. He tapped the glass bezel, expecting the needle to wobble or drift as all standard instruments did when carried far from Harmony Prime's central resonance towers. <!-- L0661 --> <!-- L0662 -->

The needle did not move. It remained locked in place, pointing with unyielding precision toward a bearing deep beneath the academy spires. <!-- L0663 --> <!-- L0665 -->"""
        },
        6: {
            "ch_num": 59,
            "title": "Harmonic Signatures & The Runoff Cliffs",
            "prose": """Lomi picked up the compass, turning it slowly in his calloused hands. No matter which way he rotated the bronze casing, the heavy needle remained rigidly oriented along its mysterious axis. <!-- L0666 --> <!-- L0680 --> <!-- L0700 -->

"This isn't tuning to Harmony Prime," Lomi murmured, his brow furrowing as he studied the etched runes around the circumference. "Standard resonant instruments fluctuate the further you get from the main spires. But this compass isn't reading city power. It's tuned to something subterranean. Something ancient." <!-- L0715 --> <!-- L0730 --> <!-- L0745 -->

Britt nodded, her hand resting on the living moss wrapped around her wrist. "Down along the runoff cliffs, the rock felt different. The moisture in the stone was alive. Even though we are thousands of feet in the air on a floating basalt plateau, the roots beneath this island are anchored to something deep. The compass led me straight to the cache like a voice calling through the mycelium." <!-- L0760 --> <!-- L0775 -->

Iggy waddled over, his copper goggles peering closely at the glass face. "It hums," the soil-kin observed, placing a dirt-caked finger against the brass base. "Like river water under ice." <!-- L0790 --> <!-- L0792 --> <!-- L0794 -->

"If this needle stays locked regardless of atmospheric interference," Lomi realized, looking up at his squad with growing excitement, "we can use it to navigate the thermal blind spots during the Basalt Run. While other pilots are flying blind through the canyon dust, we'll have an absolute bearing." <!-- L0795 -->"""
        },
        7: {
            "ch_num": 60,
            "title": "Courtyard Politics & The Charmed Mechanic",
            "prose": """As evening settled over the academy, the courtyard filled with cadets taking a break from late-night cramming. Second-year racers strutted between the benches, talking loudly about slipstream angles and engine horsepower. <!-- L0796 --> <!-- L0815 --> <!-- L0835 --> <!-- L0855 -->

A couple of aristocratic upperclassmen paused by their table, eyeing Lomi's working-class flat cap and grease-stained leather collar with smug amusement. "You look like you belong in a coal bunker, not an aerial cockpit," one sneered, tossing his silk scarf over his shoulder. <!-- L0875 --> <!-- L0895 --> <!-- L0915 -->

Lomi didn't even blink. He wiped his hands casually on an oily rag, flashed a slow, charming smile, and leaned back against the stone balustrade. "I'm sure you were charmed to meet me," Lomi drawled with easy confidence. "Save that pretty scarf for Wednesday, friend. You'll need something to wipe our exhaust off your goggles." <!-- L0920 --> <!-- L0922 --> <!-- L0923 --> <!-- L0924 --> <!-- L0925 -->

Ignatius burst into laughter, clinking his tin mug against Lomi's arm, while the aristocrat flushed crimson and stormed off toward the dining hall. <!-- L0925 -->"""
        },
        8: {
            "ch_num": 61,
            "title": "Pip's Grapevine & Sibling Rivalries",
            "prose": """A moment later, Pip came skipping across the cobblestones, a basket of warm berry tarts balanced precariously on her arm, with the towering, gentle frame of Bramble following behind like a leafy bodyguard. <!-- L0926 --> <!-- L0945 --> <!-- L0965 --> <!-- L0985 -->

"Food delivery!" Pip announced, plopping the basket onto the workbench. "Bramble and I have been listening to the grapevine all afternoon. The second-years are terrified of the wind shear in the southern chasm! Half of them are putting lead weights in their keels to avoid getting flipped." <!-- L1000 --> <!-- L1020 --> <!-- L1040 --> <!-- L1045 -->

"Lead weights?" Lomi chuckled, shaking his head. "Amateurs. That'll kill their climb rate off the first spire. What they need is proper lubrication to keep their control cables from seizing under heat." <!-- L1045 -->

Pip grabbed a tart, taking a huge bite and spraying crumbs as she grinned. "Which is why your little deal with Lucky is going to make you legendary before the first flag even drops!" <!-- L1045 -->"""
        },
        9: {
            "ch_num": 62,
            "title": "Two Days to the Basalt Run",
            "prose": """The quad grew quiet as the midnight bells echoed from the clock tower, tolling twelve deep strokes that reverberated across the floating city. Above them, the stars wheeled across the black expanse of the sky, cold and infinite. <!-- L1046 --> <!-- L1060 --> <!-- L1080 --> <!-- L1100 -->

They sat together on the stone steps: Lomi, Ignatius, Iggy, and Britt, joined by Pip and Bramble. On the flagstones before them lay their accumulated treasures: Val's annotated exam study guide, the mysterious unwavering surveyor's compass, the promise of Conte's amber power core, and the blueprint for a racing rig that would defy every convention in the academy playbook. <!-- L1120 --> <!-- L1140 --> <!-- L1160 -->

"Two days," Ignatius said quietly, the embers around his brow glowing with steady, resolute warmth. "Two days until the Resonance Race, and then the Basalt Run." <!-- L1180 --> <!-- L1182 --> <!-- L1184 -->

"We're ready," Britt said softly, her fingers brushing the green vines at her wrist as she looked out over the darkened horizon. <!-- L1184 -->

Lomi pulled his flat cap down tight, a wide, confident grin cutting through the engine soot on his face. "Let them bring their polished hulls and noble names. We're going to give this academy a lesson it won't ever forget." <!-- L1184 -->"""
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
        
        out_file = os.path.join(blocks_dir, f"s6-scene-{sid:02d}.md")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(full_content)
        print(f"Wrote {out_file} ({len(prose.split())} words, range [{start}, {end}])")

if __name__ == "__main__":
    main()
