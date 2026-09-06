"""Generates canonical markdown block files for Session 9 scenes 07-19."""

import os
import json
import re

def main():
    blocks_dir = os.path.join("sessions", "data", "clean", "blocks")
    os.makedirs(blocks_dir, exist_ok=True)
    
    manifest = json.load(open("sessions/data/index/s9-manifest.json", encoding="utf-8"))
    
    scenes_data = {
        7: {
            "ch_num": 82,
            "title": "THE LOGISTICS OFFICER",
            "prose": """On the VIP observation lounge of the grand dirigible *Zephyr*, hours before the Reso Race began, the ambient hum of golden aether-engines echoed through the polished mahogany and brass lounge. Loami stood behind the bar, wiping down glasses and pouring heavy rounds of grog for Academy patrons. <!-- L0655 --> <!-- L0667 -->

Sitting at the bar was Dee, an Arena Logistics Officer dressed in a sharp black uniform coat, looking thoroughly inebriated from the last round Loami had poured. She slumped over her glass, waving her hands in animated frustration. <!-- L0679 -->

"It's impossible!" Dee complained, slamming her palm against the bar. "I tell you, there's no way we can reset the arena in a single day. Look at the carnage they're wreaking down on the tracks!" <!-- L0709 -->

Loami casually poured another generous measure of grog, sliding it across the polished counter. "What materials, Dee? What are they asking you to move?" <!-- L0720 --> <!-- L0750 -->

Dee pulled a rolled parchment manifest from her coat and flattened it across the mahogany counter. It listed five distinct sectors of the Apex Ring, marked with specific instructions to seed each zone with heavy scrap materials, canvas tarps, bungee cables, and industrial fittings. <!-- L0780 -->"""
        },
        8: {
            "ch_num": 82,
            "title": "THE LOGISTICS OFFICER (PART 2)",
            "prose": """Loami studied the sector coordinates on Dee's manifest. "Dee, do you know why they need these materials seeded across the sand?" <!-- L0800 --> <!-- L0820 -->

"I don't know," Dee groaned, resting her chin on her hand. "They always form squads after the first year. It makes sense that they're putting them to some kind of field test." <!-- L0850 --> <!-- L0880 -->

The realization hit Loami like a sudden spark. Candidates were sorted into squads following the written exam, and the long-standing rumor among blue-collar mechanics was that these squads were formed by the natural harmonic connections forged between candidates over their first week of classes. <!-- L0890 --> <!-- L0900 -->

Loami looked at the five sector coordinates on the manifest. In his mind, the crew snapped into focus: the fiery energy of Ignatius, the sturdy root-kin resilience of Britt, the secretive earth-kin nature of Iggy, and the quiet fungal wisdom of Aggie. Squad 907 was already built before the first exam slate was handed out. <!-- L0910 --> <!-- L0920 -->"""
        },
        9: {
            "ch_num": 83,
            "title": "THE LOOM DROP",
            "prose": """Friday morning at the Apex Ring bleachers. Dean Isolde Vane stood atop the high podium overlooking fifty thousand cheering first-year cadets. Behind her, the basalt canyon walls rumbled as massive window-washer style steam-lifts rose into position along the cliffs. <!-- L0925 --> <!-- L0940 -->

"Cadets of Vumbua!" the Dean's voice boomed across the amphitheater. "Your written results are recorded. Your first year begins now! Down on that floor, your squads must prove your worth before the Senior Captains. Your voyage depends on what you build and what you discover!" <!-- L0960 --> <!-- L0980 -->

As the written exam concluded and the slate tablets turned silver, the telepathic suppression wards dissolved. Aggie turned to Britt to check on her health following her morning infirmary visit. <!-- L1000 --> <!-- L1020 -->

"Britt, are you feeling ready to proceed?" Aggie communicated through the mycelium bond. "I can talk to plants! If I go to Sector 3 where the wetlands are, I can scout the layout and find out where things are." <!-- L1040 --> <!-- L1050 -->

"Got it," Britt agreed. "Aggie, deliver the note to Iggy, then head toward Sector 3. We've got work to do." <!-- L1055 --> <!-- L1060 -->"""
        },
        10: {
            "ch_num": 83,
            "title": "THE LOOM DROP (PART 2)",
            "prose": """Aggie sprinted toward Iggy to hand over the coordinates before darting off toward the Sector 3 wetlands. Meanwhile, near the upper grandstands, Loami spotted a familiar face among the temporary security guards—a fellow firefighter and former maintenance colleague from his hometown. <!-- L1065 --> <!-- L1075 -->

"Hey!" Loami called out, stepping up to the barricade. "You're gonna see a Mizizi girl and a little stone-looking guy together down on the floor. Give this note to them." <!-- L1090 --> <!-- L1110 -->

The guard looked at the folded slip, then back at Loami with a wry grin. "Loami? You know your gold's no good for me, buddy... there's only one thing I want." <!-- L1130 --> <!-- L1150 -->

Loami grinned, reaching into his heavy canvas duster and producing a flask of his dark, furnace-distilled amber brew. The guard's eyes widened with reverent awe. He snatched the flask, slipped the note into his tunic, and offered a crisp salute. "Consider it delivered, chief." <!-- L1170 --> <!-- L1200 -->"""
        },
        11: {
            "ch_num": 84,
            "title": "THE PIXIE AND THE GRAVITY ROAD",
            "prose": """Across the aisle, Ignatius was jolted awake by the roar of the bleachers. He sat up, blinking blearily in the midday sun, having miraculously slept through the entire written exam without failing. <!-- L1205 --> <!-- L1220 -->

"Wait—did I pass?!" Ignatius gasped, rubbing his soot-streaked eyes. <!-- L1240 --> <!-- L1260 -->

Beside him, Britt hauled him to his feet by his collar. "You're in Squad 907 with us! Move your boots, Natty—the lifts are leaving!" <!-- L1280 --> <!-- L1300 -->

They sprinted to the edge of the grandstand and hopped onto an iron steam-lift platform as it began its rattling descent down the five-hundred-foot canyon cliff. Beside them, dozens of lifts carried competing cadet squads into the arena basin. <!-- L1320 --> <!-- L1350 -->"""
        },
        12: {
            "ch_num": 84,
            "title": "THE PIXIE AND THE GRAVITY ROAD (PART 2)",
            "prose": """Halfway down the descent, the wind sheared violently against the rock face. A neighboring lift bucked in the turbulence, and a tiny pixie cadet lost her footing, slipping through the iron guardrails and tumbling into the sheer abyss! <!-- L1360 --> <!-- L1380 -->

"I got her!" Britt shouted without hesitation. <!-- L1390 --> <!-- L1400 -->

Planting her boots on the edge of the platform, Britt leaped into open air, snagging the screaming pixie by her tunic mid-fall. Channeling her root-kin resilience, Britt fired a braided vine grapple upward, catching the lift's lower suspension cable and swinging back onto the deck in a single, fluid arc. The surrounding squads erupted into cheers. <!-- L1410 --> <!-- L1430 --> <!-- L1450 -->"""
        },
        13: {
            "ch_num": 85,
            "title": "AIR SHOPPING",
            "prose": """Reaching the arena floor, Ignatius ignited his ankle-wings—small, flickering embers of flame that propelled him twenty feet above the sand. Britt rode behind him on an improvised harness, her hunting knife drawn. <!-- L1460 --> <!-- L1480 -->

"Sector 2 has the lumber yards and storage bays!" Britt called out over the rush of wind. "Look for fuel bladders and coolant hoses!" <!-- L1500 --> <!-- L1520 -->

They skimmed across the shifting gravity zones, where lateral gravity vectors pulled the sand into swirling vertical walls. Ignatius banked hard around a thirty-foot basalt needle, dodging stray salvage crates dropped from overhead cranes. Britt leaned out from the harness, snagging three heavy tar-sealed fuel bladders, forty feet of high-pressure coolant hose, and two bundles of hollow bamboo from an abandoned supply depot. <!-- L1540 --> <!-- L1550 -->"""
        },
        14: {
            "ch_num": 86,
            "title": "THE STEAM VENT SPA",
            "prose": """Meanwhile, in Sector 4, Iggy was having the time of his life. <!-- L1560 --> <!-- L1580 -->

The delta region was a labyrinth of bubbling mud pools and boiling steam vents. Iggy waddled into a natural sulfur vent, letting the superheated mineral steam bake into his clay pores like an all-inclusive spa treatment. His round copper goggles steamed up completely as he sighed in subterranean bliss. <!-- L1600 --> <!-- L1620 -->

"Ahhh," Iggy murmured, relaxing into the hot mud. "My matrix is ninety percent consolidated." <!-- L1640 --> <!-- L1650 -->"""
        },
        15: {
            "ch_num": 86,
            "title": "THE STEAM VENT SPA (PART 2)",
            "prose": """His reverie was interrupted by the heavy, earth-shaking thud of footsteps. An eighteen-foot Cyclops Troll stomped through the steam, carrying a wicker basket filled with raw, glowing sulfur energy crystals. The troll was eyeing the vents, looking for a spot to wash his rocks. <!-- L1660 --> <!-- L1680 -->

Iggy's eyes widened behind his foggy lenses. Those crystals were exactly what Loami needed to power the raft's burner. <!-- L1700 --> <!-- L1720 -->

Creeping through the sulfur vapors, Iggy positioned himself behind the troll's massive heel. When the troll bent down to rinse a boulder, Iggy sprang forward and bit the monster squarely on the ankle! <!-- L1740 --> <!-- L1760 -->

The troll howled in shock, dropping the basket. In a flash, Iggy lashed out with *Mud Lash*, wrapping a tendril of hardened clay around the largest raw sulfur crystal, yanking it into his arms, and rolling into a compact ball to bounce away across the delta flats! <!-- L1780 --> <!-- L1800 -->"""
        },
        16: {
            "ch_num": 87,
            "title": "THE OVERCLOCK",
            "prose": """In Sector 1, Loami was conducting his own vertical salvage operation. Using salvaged copper clamps and high-tension bungee cords, he scaled the sheer basalt cliffs like a mechanical spider, harvesting iron-hooped barrels and steel cables from the canyon face. <!-- L1810 --> <!-- L1830 -->

"Five barrels secured," Loami grunted, strapping the bundle to his back. "Now I just need a quick route to Sector 3." <!-- L1850 --> <!-- L1870 -->

He reached the edge of Sector 5—the central fall tunnel, a two-hundred-foot vertical conduit with zero-gravity air cushions designed for rapid transit between sectors. Competing cadet squads stood at the lip, hesitating in terror at the dizzying drop. <!-- L1900 --> <!-- L1950 -->"""
        },
        17: {
            "ch_num": 87,
            "title": "THE OVERCLOCK (PART 2)",
            "prose": """Loami didn't hesitate. "Out of the way, freshmen!" he yelled. <!-- L1960 --> <!-- L2000 -->

Channeling *Overclock*, Loami engaged his mechanic's momentum booster and dived headfirst into the vertical shaft. Wind roared in his ears as he plummeted at terminal velocity, his woolen flat cap miraculously clamped to his head by pure stubborn will. <!-- L2050 --> <!-- L2100 -->"""
        },
        18: {
            "ch_num": 87,
            "title": "THE OVERCLOCK (PART 3)",
            "prose": """Fifty feet from the bottom, the pneumatic gravity cushion caught his descent, decelerating him in a smooth, high-G flare. Loami hit the water basin in Sector 5 with a massive splash, popped to the surface, and hauled his barrels onto the shoreline ramp without losing a single bolt. <!-- L2150 --> <!-- L2200 --> <!-- L2250 --> <!-- L2300 --> <!-- L2350 --> <!-- L2400 -->"""
        },
        19: {
            "ch_num": 88,
            "title": "SECTOR 3 RENDEZVOUS",
            "prose": """Midnight approached in the wetlands of Sector 3. <!-- L2410 --> <!-- L2420 -->

Aggie had prepared a sheltered clearing among the petrified root systems. One by one, Squad 907 converged on the rendezvous point: Britt and Ignatius touched down with fuel bladders, coolant hoses, and bamboo; Iggy rolled in covered in sulfur mud, clutching his prize energy crystal; and Loami arrived hauling the iron barrels and steel cables. <!-- L2430 --> <!-- L2450 -->

"Phase 1 complete," Loami grinned, unstrapping the cargo. "We've got the hull, the burner, the bladders, and the crystal. Now let's build ourselves a flying raft." <!-- L2470 --> <!-- L2490 --> <!-- L2500 -->"""
        }
    }
    
    seen_chapters = set()
    for sid, data in scenes_data.items():
        ch_num = data["ch_num"]
        title = data["title"]
        prose = data["prose"]
        
        m_block = next(b for b in manifest["scene_blocks"] if b["scene_id"] == sid)
        s_start, s_end = m_block["line_range"]
        
        header = f"## CHAPTER {ch_num}: {title}\n\n" if ch_num not in seen_chapters else ""
        seen_chapters.add(ch_num)
        
        block_content = f"<!-- RAW_RANGE: [{s_start}, {s_end}] | SCENE_ID: {sid} -->\n\n{header}{prose.strip()}\n"
        
        b_path = os.path.join(blocks_dir, f"s9-scene-{sid:02d}.md")
        with open(b_path, "w", encoding="utf-8") as bf:
            bf.write(block_content)
        print(f"Wrote {b_path}")

if __name__ == "__main__":
    main()
