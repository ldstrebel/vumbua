"""Generates canonical markdown block files for Session 10 scenes 05-41."""

import os
import json
import re

def main():
    blocks_dir = os.path.join("sessions", "data", "clean", "blocks")
    os.makedirs(blocks_dir, exist_ok=True)
    
    manifest = json.load(open("sessions/data/index/s10-manifest.json", encoding="utf-8"))
    
    # Text mapping per scene
    scenes_data = {
        5: {"ch_num": 89, "title": "MAGNETIC SAND SURFING", "prose": """Sector 1's canyon sands moved in sudden vertical cliffs that solidified in seconds from loose grain to sheer packed stone, fifty-foot swells of compressed mineral matter that reared up without warning and slammed flat again before you could account for them. <!-- L0503 --> <!-- L0505 --> <!-- L0625 -->"""},
        6: {"ch_num": 89, "title": "MAGNETIC SAND SURFING (PART 2)", "prose": """Loami worked the calculation with salvaged copper-wound industrial anchors and magnetic clamps. The friction of the sand against the canyon walls generated static electricity—slow-building, diffuse, but real—and the magnetic clamps could be temporarily charged by contact with the moving sands, creating brief bursts of polarity that could be exploited for traction, momentum, or, if you were good at the timing, something closer to surfing. <!-- L0650 --> <!-- L0700 --> <!-- L0750 -->"""},
        7: {"ch_num": 89, "title": "MAGNETIC SAND SURFING (PART 3)", "prose": """Ignatius had attempted to hold the magnets overhead as a flying spotter. The magnetic surge yanked him downward with considerably more force than anticipated and planted him face-first into a forty-foot sand wave. He emerged from this intact, if substantially coated in mineral dust. <!-- L0780 --> <!-- L0820 --> <!-- L0870 -->"""},
        8: {"ch_num": 89, "title": "MAGNETIC SAND SURFING (PART 4)", "prose": """They adapted. Loami mounted a sheet of scrap metal and used polarity flips—alternating the charge on the clamps every thirty to forty seconds as the sand-wave geometry changed—to skate across the canyon floor while Ignatius tracked from ten feet overhead, calling out the locations of embedded hardware as it became visible between wave crests: iron-hooped barrels, steel cables, and copper fittings. Loami harvested them all before the sand closed back over. <!-- L0920 --> <!-- L0980 --> <!-- L1020 -->"""},
        
        9: {"ch_num": 90, "title": "IGGY'S FIRST TREE", "prose": """Sector 3 was where the Apex Ring stored its forest—a wall of petrified giants, ninety-foot trunks of compressed mineral-wood with root systems sunk deep into the bedrock and branches interlaced at forty to sixty feet. Iggy had never seen a tree, having grown up in Bamboo with its manicured urban medians. He stood at the tree line, looked up, and simply stopped moving. <!-- L1051 --> <!-- L1064 --> <!-- L1078 -->"""},
        10: {"ch_num": 90, "title": "IGGY'S FIRST TREE (PART 2)", "prose": """He set down his gear, pulled out his journal, and began to sketch. He peeled bark samples from the lower trunk with careful, methodical hands, pressing them flat into the pages of his knapsack for later study. <!-- L1100 --> <!-- L1150 -->"""},
        11: {"ch_num": 90, "title": "IGGY'S FIRST TREE (PART 3)", "prose": """A frustrated roar rolled through the steam-vented clearing behind him. Sam the Cyclops Troll, still resentful about both the crystal and the bite, was closing the distance across Sector 3 at a very committed pace. <!-- L1200 --> <!-- L1201 --> <!-- L1205 -->"""},
        12: {"ch_num": 90, "title": "IGGY'S FIRST TREE (PART 4)", "prose": """\"Let's go, let's go!\" Iggy said to himself, packing his samples. He attempted to navigate southwest through the dense woods, but after twenty minutes of walking, the canopy brightened and he stepped out of the tree line directly back into the clearing he'd started from. Sam was now three-quarters of the distance closed. <!-- L1262 --> <!-- L1341 -->"""},
        13: {"ch_num": 90, "title": "IGGY'S FIRST TREE (PART 5)", "prose": """He tried again, bouncing off stone trunks like a pinball machine. He emerged from the forest line a second time—directly in front of Sam, Sarah the female Cyclops (arms crossed, smirking), and a young elf girl. Sarah extended her open hand with elaborate patience, demanding the crystal back. <!-- L1399 --> <!-- L1403 --> <!-- L1450 -->"""},
        14: {"ch_num": 90, "title": "IGGY'S FIRST TREE (PART 6)", "prose": """\"Hold please!\" Iggy said. He drank a stamina potion, dropped into his rolling ball form, and bolted for the basin water 100 yards away, scattering bark samples behind him as a peace offering. Sam hurled a twenty-foot petrified tree trunk that slammed into the mud six inches from Iggy, exploding dirt and shockwaves into his side for 6 damage. Iggy leaped into the 1,700-foot deep water basin, earning a permanent traumatic phobia of trees. <!-- L1525 --> <!-- L1536 --> <!-- L1546 -->"""},
        
        15: {"ch_num": 91, "title": "THE SOULLESS FOREST", "prose": """Along the Sector 3 shoreline, Aggie and Britt held the rendezvous point and waited. Aggie had walked through the forest already, scouting the mycelium maze. \"It looks like home,\" Aggie said, \"but it's missing the soul. A master artist created this place knowing nothing about what it feels like to live in it.\" <!-- L1802 --> <!-- L1811 --> <!-- L1850 -->"""},
        16: {"ch_num": 91, "title": "THE SOULLESS FOREST (PART 2)", "prose": """Aggie walked to an ancient petrified tree at the edge of the clearing and placed her palms flat against the bark, channeling her Mizizi instinct. \"Tell me where our people are,\" she whispered. <!-- L1920 --> <!-- L1926 -->"""},
        17: {"ch_num": 91, "title": "THE SOULLESS FOREST (PART 3)", "prose": """The forest answered in mental impressions: *We were told not to tell you where your people were... but one of yours tried to enter the forest twice and got lost. We lost track after one of our brethren was felled and thrown at him.* <!-- L2015 --> <!-- L2050 -->"""},
        18: {"ch_num": 91, "title": "THE SOULLESS FOREST (PART 4)", "prose": """\"Someone threw a tree?!\" Aggie gasped, pulling her hands back from the rough stone bark. <!-- L2115 --> <!-- L2150 -->"""},
        19: {"ch_num": 91, "title": "THE SOULLESS FOREST (PART 5)", "prose": """Aggie went to the shoreline and tapped river stones rhythmically over the water—a steady, repeating acoustic signal. Submerged thirty feet below, Iggy heard the clacking and oriented toward the sound. <!-- L2190 --> <!-- L2250 -->"""},
        20: {"ch_num": 91, "title": "THE SOULLESS FOREST (PART 6)", "prose": """Iggy collected every dropped river stone as he rose, crawling up the muddy shore covered in sediment and glaring at the tree line. \"The trees... they're hostile. They threw themselves at me.\" \"The trees didn't throw themselves, Iggy! The cyclops threw them!\" <!-- L2400 --> <!-- L2472 --> <!-- L2534 -->"""},
        
        21: {"ch_num": 92, "title": "THE NATTY RENAMING", "prose": """Midnight in Sector 3. The Canopy Raft was a collection of intentions and raw materials spread across the shoreline: six iron-hooped buoyancy barrels, steel cables, high-tension bungee cords, two canvas tarps, fuel bladders sealed with dark tar, coolant hoses, and a raw sulfur energy crystal. <!-- L2650 --> <!-- L2700 -->"""},
        22: {"ch_num": 92, "title": "THE NATTY RENAMING (PART 2)", "prose": """Loami arrived hauling the barrel collection from Sector 1. He tossed Ignatius a wineskin as he dropped the load. \"First of all, your name is great and all. But we already have an Iggy. We have an Aggie. So, you're now Natty. I'm calling you Natty.\" <!-- L2780 --> <!-- L2850 -->"""},
        23: {"ch_num": 92, "title": "THE NATTY RENAMING (PART 3)", "prose": """Ignatius looked at him. His flame hair flickered with mild outrage before he calculated that this was not a fight worth having. \"Alright, crew,\" Loami said, surveying the haul. \"Phase 1 is done. Now we build.\" <!-- L2940 --> <!-- L3000 -->"""},
        24: {"ch_num": 92, "title": "THE NATTY RENAMING (PART 4)", "prose": """They built through the night. The hull was assembled from six iron-hooped barrels bound with steel cables and bungee cords, topped with a canvas deck and four heavy shovels for steering oars. <!-- L3063 --> <!-- L3065 -->"""},
        25: {"ch_num": 92, "title": "THE NATTY RENAMING (PART 5)", "prose": """The balloon canopy was stitched from tar-sealed fuel bladders painted with mottled forest camouflage, with a central burner fixture designed to hold the raw sulfur crystal. <!-- L3193 --> <!-- L3250 -->"""},
        26: {"ch_num": 92, "title": "THE NATTY RENAMING (PART 6)", "prose": """For defense, they mounted two coolant-hose slingshots loaded with petrified seed pods wrapped in glowing bioluminescent moss as tracer rounds, along with bamboo blow-dart tubes. <!-- L3327 --> <!-- L3400 -->"""},
        27: {"ch_num": 92, "title": "THE NATTY RENAMING (PART 7)", "prose": """At 2:00 AM, Loami stepped back and inspected the craft. \"She's airtight, buoyant, and hidden,\" he confirmed. \"She is,\" Natty agreed with pride. <!-- L3452 --> <!-- L3459 -->"""},
        
        28: {"ch_num": 93, "title": "RILL AT FOUR IN THE MORNING", "prose": """At 4:00 AM, silver river fog rolled across the Sector 3 shoreline. Squad 907 was resting near the camouflaged raft when a figure stepped quietly out of the mist. <!-- L3550 --> <!-- L3600 -->"""},
        29: {"ch_num": 93, "title": "RILL AT FOUR IN THE MORNING (PART 2)", "prose": """Her blue hair was damp with fog and her canvas captain's coat was dark with moisture. Rill paused at the shoreline, looking at the Canopy Raft with warm approval. \"You've built something impressive out of scrap, candidates.\" <!-- L3626 --> <!-- L3636 -->"""},
        30: {"ch_num": 93, "title": "RILL AT FOUR IN THE MORNING (PART 3)", "prose": """\"Rill!\" Aggie stepped forward. \"What are you doing out here?\" <!-- L3651 --> <!-- L3652 -->"""},
        31: {"ch_num": 93, "title": "RILL AT FOUR IN THE MORNING (PART 4)", "prose": """\"Warning you,\" Rill said quietly. \"The 8:00 challenge isn't a standard run. The Dean and the Logistics Officers are dropping the sector suppression barriers. Whatever is inside these sectors is coming out.\" <!-- L3654 --> <!-- L3700 -->"""},
        32: {"ch_num": 93, "title": "RILL AT FOUR IN THE MORNING (PART 5)", "prose": """She reached into her coat and held out a heavy brass-bound flare gun. Aggie took it gratefully. \"If the storm takes the sky or you get pinned in the basin, fire this straight up. Don't die out here.\" <!-- L3777 --> <!-- L3778 -->"""},
        33: {"ch_num": 93, "title": "RILL AT FOUR IN THE MORNING (PART 6)", "prose": """She vanished into the fog. Across the basin, the 5:00 AM evacuation bell rang, sending most candidates heading for the exits. Squad 907 stayed. <!-- L3783 --> <!-- L3790 --> <!-- L3804 -->"""},
        
        34: {"ch_num": 94, "title": "THE DAGGER SHARKS", "prose": """8:00 AM arrived with a sustained siren drone from the arena towers. Across five sectors, the massive Walker-Core suppression barriers released with a canyon-splitting crack, discharging violet static arcs down their colossal iron legs. <!-- L4301 --> <!-- L4350 -->"""},
        35: {"ch_num": 94, "title": "THE DAGGER SHARKS (PART 2)", "prose": """\"Push!\" Loami ordered. The Canopy Raft slid into the basin water with a solid thud and floated cleanly. They were 100 yards into open water when the first chitinous, bioluminescent fins sliced through the foam. <!-- L4401 --> <!-- L4411 -->"""},
        36: {"ch_num": 94, "title": "THE DAGGER SHARKS (PART 3)", "prose": """Twelve-foot Dagger Sharks with glowing violet lateral lines circled the hull. \"Dagger sharks!\" Iggy screamed in terror. \"They track living energy signatures—they took my friends in the lower trenches! We have to get off the water NOW!\" <!-- L4516 --> <!-- L4523 -->"""},
        37: {"ch_num": 94, "title": "THE DAGGER SHARKS (PART 4)", "prose": """\"I'm lighting the sulfur crystal!\" Natty shouted, activating Sparking Engines. The burner ignited, sending superheated gas into the balloon envelope. <!-- L4611 --> <!-- L4650 -->"""},
        38: {"ch_num": 94, "title": "THE DAGGER SHARKS (PART 5)", "prose": """A Dagger Shark leaped out of the water, its armored jaws clamping onto Natty's shoulder. Natty gritted his teeth, his inner furnace flaring as his heavy leather pauldron absorbed the crushing bite, refusing to let go of the burner. <!-- L4709 --> <!-- L4750 -->"""},
        39: {"ch_num": 94, "title": "THE DAGGER SHARKS (PART 6)", "prose": """\"Hold steady, Natty!\" Aggie placed her hands on the burner frame and channeled Wild Touch, supercharging the sulfur burn. The balloon filled in a roaring rush, lifting the raft fifteen feet into the air! <!-- L4789 --> <!-- L4850 -->"""},
        40: {"ch_num": 94, "title": "THE DAGGER SHARKS (PART 7)", "prose": """\"Distraction tactic!\" Iggy called out. Aggie and Britt loaded the slingshots with glowing moss-wrapped seed pods, firing them toward the distant shore to lure the sharks away with false bio-signatures. <!-- L5003 --> <!-- L5076 -->"""},
        41: {"ch_num": 94, "title": "THE DAGGER SHARKS (PART 8)", "prose": """Loami swung the grappling hook and anchored the raft into an eighty-foot petrified bough overhead. The camouflaged raft swung into the high canopy and vanished against the foliage, safe and hidden above the chaos below. <!-- L5134 --> <!-- L5138 --> <!-- L5200 -->"""}
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
        
        b_path = os.path.join(blocks_dir, f"s10-scene-{sid:02d}.md")
        with open(b_path, "w", encoding="utf-8") as bf:
            bf.write(block_content)
        print(f"Wrote {b_path}")

if __name__ == "__main__":
    main()
