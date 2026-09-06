"""Generates canonical markdown block files for Session 11 scenes 03-23."""

import os
import json
import re

def main():
    blocks_dir = os.path.join("sessions", "data", "clean", "blocks")
    os.makedirs(blocks_dir, exist_ok=True)
    
    manifest = json.load(open("sessions/data/index/s11-manifest.json", encoding="utf-8"))
    
    scenes_data = {
        3: {"ch_num": 95, "title": "THE MEWODERS IN THE CANOPY", "prose": """Squad 907 hung suspended in the high petrified canopy of Sector 3, their camouflaged Canopy Raft wedged between four colossal ancient boughs sixty feet above the mossy forest floor. Torrential rain beat against the tar-sealed canvas balloon envelope overhead, and distant booms of static lightning shook the canyon obelisk. <!-- L0255 --> <!-- L0280 --> <!-- L0300 -->"""},
        4: {"ch_num": 95, "title": "THE MEWODERS IN THE CANOPY (PART 2)", "prose": """\"Well, the landing went better than I thought,\" Ignatius said, shaking rain from his dark cloak. <!-- L0350 --> <!-- L0400 -->

Loami checked the bungee lashing on the hull. \"Yeah, I'm shocked we got here at all. But here we are. Safe as we're going to get.\" <!-- L0450 --> <!-- L0480 -->"""},
        5: {"ch_num": 95, "title": "THE MEWODERS IN THE CANOPY (PART 3)", "prose": """A rustling in the boughs alerted Loami's low-light vision. Feline predators—Mewoders, vicious canopy tree-cats with mottled camouflage fur—were stalking along the branches! Iggy curled into a ball on the raft, trembling from his tree trauma: \"The trees have eyes! The trees have eyes!\" Britt stepped forward, casting *Hypnotic Shimmer* in a dazzling fan of light to stun the pack. <!-- L0500 --> <!-- L0520 --> <!-- L0550 -->"""},
        
        6: {"ch_num": 96, "title": "PIP AND THE STORM RAPTOR", "prose": """High above the canopy, a piercing predatory shriek cut through the thunder. A massive Storm Raptor, its wings crackling with static electricity, dove out of the tempest clouds carrying a screaming figure in its talons—Pip, clutching her bag of bacon biscuits for dear life! <!-- L0580 --> <!-- L0620 --> <!-- L0650 -->"""},
        7: {"ch_num": 96, "title": "PIP AND THE STORM RAPTOR (PART 2)", "prose": """\"Pip!\" Britt cried out. Ignatius fired his ember ankle-jets, soaring up toward the raptor's flight path, while Loami loaded the heavy coolant slingshot with petrified seed pods. <!-- L0700 --> <!-- L0750 --> <!-- L0780 -->"""},
        8: {"ch_num": 96, "title": "PIP AND THE STORM RAPTOR (PART 3)", "prose": """A direct hit from the slingshot broke the raptor's grip, and Ignatius caught Pip in mid-air, carrying her safely down onto the Canopy Raft deck. Pip landed, hugged her biscuit sack tight, and glared up at the clouds: \"Nobody touches my biscuits!\" <!-- L0800 --> <!-- L0820 --> <!-- L0850 -->"""},
        
        9: {"ch_num": 97, "title": "MWAZA-CHUI AND THE STATIC ROAR", "prose": """The celebration was cut short by a sound that vibrated through their teeth—a low, rhythmic static pulse echoing from the branch forks above. Through the foliage emerged two Mwaza-Chui—apex canopy jaguars whose dark fur crackled with violet bio-electrical frequency. <!-- L0880 --> <!-- L0920 --> <!-- L0950 -->"""},
        10: {"ch_num": 97, "title": "MWAZA-CHUI AND THE STATIC ROAR (PART 2)", "prose": """The alpha jaguar released a deafening, static-charged roar that short-circuited spellcasting links and dazed the squad with sharp electromagnetic feedback. \"They disrupt magical resonance!\" Aggie warned through ringing ears. <!-- L1000 --> <!-- L1050 --> <!-- L1100 -->"""},
        11: {"ch_num": 97, "title": "MWAZA-CHUI AND THE STATIC ROAR (PART 3)", "prose": """Aggie touched the ancient bough beneath her boots and channeled *Wild Fortress*, causing living petrified bark and timber to rapidly grow around Pip and Loami in a protective igloo barricade. Outside, Britt and Ignatius held the line with slingshot barrage and flame flares. <!-- L1120 --> <!-- L1140 --> <!-- L1150 -->"""},
        
        12: {"ch_num": 98, "title": "BRAMBLE IN THE TREES", "prose": """As the jaguars stalked the perimeter of the wooden igloo, the petrified leaves above began to rustle in synchronized patterns. Aggie felt a familiar resonance pulse through the root network—Bramble, using *Speak to Plants* from Squad 06's high tree fortress! <!-- L1180 --> <!-- L1220 --> <!-- L1250 -->"""},
        13: {"ch_num": 98, "title": "BRAMBLE IN THE TREES (PART 2)", "prose": """*\"Aggie! It's Bramble!\"* the tree whispered in her mind. *\"I apologize for misleading your signals earlier—we didn't know it was Squad 907 until we saw Iggy's shape in the canopy! We're holding the timber ramparts on the west bough!\"* <!-- L1300 --> <!-- L1350 --> <!-- L1400 -->"""},
        14: {"ch_num": 98, "title": "BRAMBLE IN THE TREES (PART 3)", "prose": """*\"Bramble, we've got Pip and we're pinned by Mwaza-Chui!\"* Aggie transmitted back. *\"Prepare your lines—we're bringing the fight to the floor!\"* <!-- L1420 --> <!-- L1440 --> <!-- L1450 -->"""},
        
        15: {"ch_num": 99, "title": "DON'T TOUCH MY BISCUITS", "prose": """To dislodge the apex jaguars from the raft platform, Loami concocted a high-stakes diversion. \"Mushroom bait on the deck!\" Loami shouted. Aggie and Britt piled glowing bioluminescent fungi across the raft planks, creating an irresistible bio-luminescent beacon. <!-- L1480 --> <!-- L1520 --> <!-- L1550 -->"""},
        16: {"ch_num": 99, "title": "DON'T TOUCH MY BISCUITS (PART 2)", "prose": """When the jaguars leaped onto the raft to investigate, Loami and Britt sliced the main bungee anchor cables with their hunting blades. The entire raft tilted sixty degrees, dumping the surprised jaguars down into the lower canopy abyss with a cacophony of snarls! <!-- L1600 --> <!-- L1650 --> <!-- L1700 -->"""},
        17: {"ch_num": 99, "title": "DON'T TOUCH MY BISCUITS (PART 3)", "prose": """Pip cheered, popping a warm bacon biscuit into her mouth, and handed one to the trembling Iggy: \"See? Told you biscuits solve everything.\" <!-- L1720 --> <!-- L1740 --> <!-- L1750 -->"""},
        
        18: {"ch_num": 100, "title": "THE SACRED MEMORY NETWORK", "prose": """A rustle in the central bough drew their eyes. Emerging slowly from the hollow of a sacred tree was a tortoise—larger than normal, with a shell resembling ancient petrified bark. Mwaza-Kasa, the sacred Spirit Tortoise of the Mizizi clan, had appeared. <!-- L1780 --> <!-- L1820 --> <!-- L1850 -->"""},
        19: {"ch_num": 100, "title": "THE SACRED MEMORY NETWORK (PART 2)", "prose": """Pip offered the tortoise a biscuit, which it accepted with slow, ancient dignity. Then Aggie and Britt reached out and laid their palms upon its weathered shell. In that instant, a tidal wave of ancestral memory flooded their minds. <!-- L1900 --> <!-- L1950 --> <!-- L2000 -->"""},
        20: {"ch_num": 100, "title": "THE SACRED MEMORY NETWORK (PART 3)", "prose": """They saw the sacred grove of their childhood, the ancient clan elders, and the terrifying onset of the green sludge rot that had claimed their ancestors. The vision revealed the truth: clan isolation was a manufactured lie, and the living network connected all six clans across the endless horizon. <!-- L2020 --> <!-- L2060 --> <!-- L2100 -->"""},
        
        21: {"ch_num": 101, "title": "THE SPIRIT TORTOISE DESCENDS", "prose": """The vision subsided, leaving Aggie and Britt weeping in shared revelation. Mwaza-Kasa collapsed into a catatonic trance, its heavy shell slipping from the wet bough. With a sudden creak of branches, the tortoise plummeted fifty feet toward the forest floor! <!-- L2150 --> <!-- L2200 --> <!-- L2250 -->"""},
        22: {"ch_num": 101, "title": "THE SPIRIT TORTOISE DESCENDS (PART 2)", "prose": """\"No!\" Britt gasped. Squad 907 rapidly rappelled down their vine lines, dropping to the mossy earth below. To their immense relief, Mwaza-Kasa was completely unhurt, standing calmly on the forest loam and blinking up at them. <!-- L2300 --> <!-- L2340 --> <!-- L2370 -->"""},
        23: {"ch_num": 101, "title": "THE SPIRIT TORTOISE DESCENDS (PART 3)", "prose": """The sacred tortoise turned and nodded toward the deep trail ahead, beginning its slow, deliberate march into the heart of the Mizizi grove. Squad 907 fell into step behind it, Level 5 and ready for the final trial of Session 12. <!-- L2380 --> <!-- L2390 --> <!-- L2400 -->"""}
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
        
        b_path = os.path.join(blocks_dir, f"s11-scene-{sid:02d}.md")
        with open(b_path, "w", encoding="utf-8") as bf:
            bf.write(block_content)
        print(f"Wrote {b_path}")

if __name__ == "__main__":
    main()
