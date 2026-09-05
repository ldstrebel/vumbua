"""Generates canonical markdown block files for Session 4 scenes 12-22."""

import os
import json
import re

def main():
    blocks_dir = os.path.join("sessions", "data", "clean", "blocks")
    os.makedirs(blocks_dir, exist_ok=True)
    
    manifest = json.load(open("sessions/data/index/s4-manifest.json", encoding="utf-8"))
    
    scenes_data = {
        12: {
            "ch_num": 32,
            "title": "The Heavy Sleeper & The Morning Rush",
            "prose": """Dawn broke over the high basalt towers of the Zephyr Academy, throwing sharp angled shadows across the cobblestones and stirring the barracks from a fitful, heavy rest. <!-- L1094 -->

In the corner bunk of Room 42, Ignatius shook himself awake. His hair flickered with low embers of crimson and amber flame, snapping him into alertness as he threw on his traveler's cloak and looked across the cramped quarters for his roommate. <!-- L1102 --> <!-- L1103 -->

Iggy was still dead to the world. The little packed-clay humanoid was buried beneath three layers of heavy woolen blankets, snoring with a rhythmic sound like grinding river stones. Faint translucent bubbles drifted up from his snout with every subterranean breath. Iggy had absolutely no concept of academy schedules, morning bells, or academic standing. To the soil-kin, the entire institution was an incomprehensible puzzle. Until someone physically dislodged him, sleep was the only sensible state of existence. <!-- L1104 --> <!-- L1106 --> <!-- L1107 --> <!-- L1109 -->

Ignatius paced the cold stone floor, stomping into his boots. He was accustomed to being the last cadet sprinting toward roll call, but he was completely unaccustomed to having a companion who was later than he was. He leaned over the mound of blankets and nudged the heavy clay shoulder. "Iggy, we got to go. We literally have class, do you know where you are?" <!-- L1112 --> <!-- L1115 --> <!-- L1124 --> <!-- L1128 --> <!-- L1130 -->

"Go away sleeping," a muffled voice grumbled from beneath the mattress. "Huh? No idea." <!-- L1127 --> <!-- L1129 --> <!-- L1131 -->

"Oh, just follow me. It's fine. You have to get out of bed!" Ignatius urged, shaking his hands. <!-- L1132 --> <!-- L1134 -->

With an agonizing groan, Iggy staged the most dramatic tumble possible out of the bunk. Sheets, pillows, and moss sprouts cascaded over the edge in a tangled avalanche as the soil-kin landed on the floorboards with a dull thud. He crawled out on all fours, sloth-crawling across the planks with zero intention of hurrying. <!-- L1137 --> <!-- L1139 --> <!-- L1141 --> <!-- L1143 -->

Meanwhile, across the courtyard in Room 99, Lomi's morning was an entirely different machine. Waking with the first hint of daylight like a veteran shipyard hand on the morning shift, Lomi had already shaved his thick jaw, tossed down a bowl of plain, unadorned oatmeal, and buttoned his heavy work collar. By the time he stepped into the hallway, a stubborn five-o'clock shadow was already clawing its way through his rugged skin. <!-- L1153 --> <!-- L1156 --> <!-- L1158 --> <!-- L1162 --> <!-- L1164 -->

He passed Sarge in the corridor. No unnecessary words were exchanged—just a mutual nod, a grunt of understanding, and a firm fist bump. Lomi could tell the older veteran was nervous about the academic test battery, but Lomi kept his composure. Back in the boiler rooms and engine bays of the lower rings, Lomi had handled immense pressure—steam pressure, structural load, hydraulic strain. But mental classroom pressure? That was an uncharted frontier. <!-- L1171 --> <!-- L1177 --> <!-- L1179 --> <!-- L1180 --> <!-- L1186 --> <!-- L1194 --> <!-- L1198 -->

Outside, the bells began their rhythmic chime. Ignatius dragged Iggy out into the brisk morning air, watching the little soil-kin squint against the morning sun until the distant aroma of baking bread and roasting meats drifted from the dining pavilion. <!-- L1208 --> <!-- L1212 -->

"Hell yeah," Ignatius grinned, his flame-hair brightening with anticipation. "Food for sure. You can't adventure on an empty stomach." <!-- L1211 --> <!-- L1213 --> <!-- L1215 --> <!-- L1217 -->"""
        },
        13: {
            "ch_num": 33,
            "title": "The Grand Dining Pavilion & The Hallway Follower",
            "prose": """The scent hit Iggy's packed-earth senses like a physical blast wave. In all his underground years among soil and subterranean caverns, he had never experienced the concentrated olfactory assault of an academy dining pavilion at peak service: sizzled sausage, molasses-glazed rolls, spiced oats, and roasted tubers all mingling in a glorious cloud. His round copper goggles widened as his feet carried him forward on auto-pilot. <!-- L1218 --> <!-- L1221 --> <!-- L1223 -->

Hundreds of cadets from across the archipelago swarmed the arched entryways. Uniformed scions of noble airship lineages rubbed shoulders with soot-stained grease monkeys, quiet scouts, and grim mercenaries. The grand dining hall echoed with the clatter of iron spoons against ceramic bowls, the hiss of steaming cauldrons, and the low roar of nervous conversation about the morning's schedule. Ignatius and Iggy weaved through the bustling morning throng, scanning the long wooden benches for a familiar woolen flat cap. <!-- L1238 --> <!-- L1248 --> <!-- L1258 -->

Lomi had secured a bench near the perimeter wall. For Lomi, breakfast was a matter of union discipline—fifteen minutes, caloric efficiency, and situational awareness. A mechanic who didn't fuel himself properly before a shift was a mechanic who made fatal mistakes when torqueing down high-pressure bolts. He was chewing methodically through a slab of dense rye bread when his peripheral vision caught something out of place. <!-- L1278 --> <!-- L1288 -->

A nervous cadet with ink-stained cuffs was hovering awkwardly three paces away, clearly tracking Lomi's movements. Every time Lomi reached for a cup of chicory tea, the boy shifted his weight, pretending to inspect a ceiling beam while sneaking glances at Lomi's tool belt and work collar. <!-- L1318 --> <!-- L1328 -->

Lomi didn't scare easily, but he appreciated good intelligence. In the yards, you learned quickly to watch the shadows; a curious spectator was usually looking for an easy mark or an open toolbox. Lomi loved a good working-class story, yet this shadow possessed none of the easy charm of an honest rogue. He had the pinched, desperate look of an academic cheat who was drowning before the first bell had even struck. When the shadow realized Lomi was staring directly at him, he melted back into the crowd of cadets rushing between tables. <!-- L1338 --> <!-- L1340 --> <!-- L1348 -->

"Morning," Lomi greeted as Ignatius and Iggy slid onto the bench opposite him, the wooden planks groaning slightly under their collective weight. Ignatius was grinning eagerly, while Iggy was practically vibrating with culinary fixation, his nose twitching toward the steaming food line. <!-- L1349 --> <!-- L1350 -->"""
        },
        14: {
            "ch_num": 34,
            "title": "The Buffet Connoisseur",
            "prose": """The dining hall buffet stretched eighty feet across the northern wall, laden with heated iron platters, bubbling tureens of barley stew, and overflowing baskets of hot flatbread. Ignatius shoved a heavy brass tray into Iggy's hands. "Grab this tray, Iggy. Grab whatever you want. We got to move before the first bell!" <!-- L1433 -->

Iggy did not understand the concept of taking a standard portion. To the soil-kin, the buffet line was not a meal—it was an exhaustive geological field survey. He marched down the gleaming silver counter, picking up individual food items with muddy fingertips, taking a deliberate, evaluative bite, and chewing with intense philosophical contemplation before deciding whether the item merited addition to his tray. <!-- L1469 --> <!-- L1474 -->

He sampled a wedge of sharp sheep's curd, chewed it thoughtfully, and set it down. He took a single bite of a peppered pork sausage, nodded with slow satisfaction, and dropped three links onto his brass platter. Next came a steamed dumpling, which he dissected with his thumbnail to examine the inner cabbage filling before devouring it in one swift motion. <!-- L1478 --> <!-- L1480 --> <!-- L1481 --> <!-- L1482 -->

A massive, tusker orc cadet standing in line behind them froze, eyes bugging out in horrified fascination as Iggy took a small nibble out of a sweet melon pastry, nodded solemnly to himself, and moved down to sample a grilled salt-pork strip. <!-- L1483 --> <!-- L1484 --> <!-- L1485 -->

"Do you know this person?" the orc whispered to Ignatius in a strained, deeply bewildered voice, gesturing with his ladle at the small creature methodically taste-testing the academy's food supply. <!-- L1485 -->

"He's a guy that likes to try things once," Ignatius replied smoothly, leaning on the counter without an ounce of embarrassment. "He has his priorities sorted. Why commit to an entire plate until you know the quality of the harvest?" <!-- L1497 --> <!-- L1533 -->

Lomi watched from the table, taking another slow bite of his bread and chuckling under his breath. The sheer chaos of their squad was rapidly making them the most watched table in the entire freshman cohort. But breakfast could not last forever; high above the quad, the third brass bell rang with deafening clarity, echoing off the basalt colonnades and signaling the immediate start of freshmen lectures. <!-- L1557 --> <!-- L1569 --> <!-- L1581 -->"""
        },
        15: {
            "ch_num": 35,
            "title": "Aerial Dynamics & The Chalk Throw",
            "prose": """The lecture amphitheater was a colossal structure of stepped basalt rows carved directly into the bedrock of the academy's central spire. Hundreds of wooden desks were bolted to the curving stone floor, descending in dizzying concentric rings toward a central stage dominated by three colossal slate chalkboards mounted on brass rails. <!-- L1581 -->

Lomi, Ignatius, and Iggy filed into the middle tier—close enough to see the diagrams, far enough back to avoid volunteering for demonstrations. At the podium stood Professor Hollow, a severe, hawk-nosed scholar with wire spectacles and black sleeves dusted white with gypsum. Without a word of greeting or introductory welcome, Hollow spun on his heel and began attacking the chalkboard with furious sweeps of chalk, scribbling complex formulas of differential calculus, air resistance vectors, and buoyant lift equations. <!-- L1590 --> <!-- L1593 --> <!-- L1603 -->

Lomi stared at the blackboard in mounting horror. Back in the lower rings of Octoumba, lift was simple: you fed power into the coil, checked the pressure gauges, and kept the manifold from blowing out. If the ship rose, your math was right; if it dipped, you threw more coal into the firebox. Here, Hollow was lecturing on fluid shear, atmospheric density gradients, and angular lift coefficients. In the front row, a pristine noble cadet raised his hand and fluently debated the third derivative of drift velocity. <!-- L1604 --> <!-- L1606 --> <!-- L1608 -->

Lomi's heart hammered against his ribs. Day one, fifteen minutes into their very first class, and he was already completely out of his depth. He leaned forward frantically, his quill scratching violently into his parchment as he attempted to copy down every single squiggle, glyph, and vector, desperate not to fall behind on the very first morning. <!-- L1610 --> <!-- L1612 --> <!-- L1614 --> <!-- L1615 -->"""
        },
        16: {
            "ch_num": 36,
            "title": "Panic at the Desks",
            "prose": """As Professor Hollow's harsh voice droned on like a circular saw cutting through green timber, the amphitheater grew stiflingly hot. The chalk dust hung thick in the air, catching the sunlight in hazy shafts. To Lomi's left, an exhausted cadet slumped forward against his desk, his chin resting on his forearm as his eyes rolled shut in exhaustion. <!-- L1627 --> <!-- L1639 -->

*Crack!* <!-- L1651 -->

With terrifying pinpoint accuracy, a two-inch chunk of hard chalk whipped across the tiered room and struck the sleeping student squarely between the shoulder blades. The cadet gasped, bolting upright with wide, terrified eyes. Professor Hollow didn't even pause his lecture or break his stride, his hand already dipping into a wooden tray for another missile. <!-- L1663 --> <!-- L1675 --> <!-- L1687 -->

Beside Lomi, Iggy took one look at the ballistic chalk strike and immediately made an executive decision. The little soil-kin slid out of his chair, tucked his knees to his chin, and curled into a dense, packed-dirt ball underneath the wooden desk, pulling his moss sprouts flat against his stony crown. To anyone glancing down the aisle, he looked like an ornamental garden boulder that someone had carelessly dropped under the furniture. <!-- L1711 --> <!-- L1723 --> <!-- L1728 -->

Ignatius rested his boot lightly against Iggy's shell-less back, a silent reassuring presence to let the soil-kin know he was safe. Lomi, meanwhile, was peering shamelessly at his neighbor's parchment, trying to decipher whether the symbol on the board was a Greek theta or a stylized valve diagram. The academic reality of Zephyr was a brutal wake-up call: the academy wasn't here to nurture them; it was designed to weed out the weak before they ever set foot on an airship deck. <!-- L1729 --> <!-- L1731 --> <!-- L1734 -->"""
        },
        17: {
            "ch_num": 37,
            "title": "The Ink-Stained Cadet",
            "prose": """When the dismissal bell finally tolled, the collective sigh of relief in the amphitheater was loud enough to rattle the windowpanes. Cadets groaned, rubbing cramped fingers, massaging stiff necks, and gathering scattered papers. Iggy uncurled from under the desk, shaking loose dust from his trench coat, while Ignatius stretched his arms until his knuckles popped. <!-- L1735 --> <!-- L1741 --> <!-- L1750 --> <!-- L1752 -->

"Priorities," Ignatius muttered, shaking his head with a wry grin. "That man could weaponize bedtime. If he throws chalk like that, imagine what he does with an artillery cannon." <!-- L1753 --> <!-- L1755 -->

As they gathered their satchels and joined the stream of students pushing toward the daylight of the colonnade, a tall, lanky human cadet sidled up alongside Lomi. His fingers were heavily smeared with dark printer's ink, contrasting sharply with the engine soot on Lomi's forearms. He leaned in close, his voice dropped to a conspiratorial whisper. "You know these formulas? Heavy stuff for day one." <!-- L1756 --> <!-- L1758 --> <!-- L1765 -->

Lomi eyed him warily, keeping his hands near his tool pouch. "Sorry, what was that?" <!-- L1759 --> <!-- L1777 -->

"I'm talking about survival," the ink-stained cadet murmured, casting a nervous look over his shoulder toward the faculty offices. "Hollow writes the hardest exams in the entire academy. Half the class fails the Friday Basalt Run theory slate. But there are ways around the grind. There's a guy named Lucky. If you've got the currency, Lucky's got Val's notes. The actual study guides. The questions before they ever hit the slate." <!-- L1789 --> <!-- L1801 --> <!-- L1813 --> <!-- L1825 --> <!-- L1837 --> <!-- L1849 -->

Before Lomi could press for details, the student melted away into the midday throng, leaving the trio standing at the edge of the sunlit courtyard with a dangerous new lead. <!-- L1850 --> <!-- L1857 -->"""
        },
        18: {
            "ch_num": 38,
            "title": "The Bulletin Board & The Resonance Race",
            "prose": """Ignatius gestured across the courtyard toward a massive crowd gathered in front of the academy's grand announcement board. "I will follow Lomi's good example," he said, pushing through the cluster of chattering freshmen. "Let's see what else they're threatening to throw at us this week." <!-- L1858 --> <!-- L1862 --> <!-- L1870 -->

Nailed to the cedar timbers of the board were official parchment notices bearing the academy's gilded wax seals. Cadets were jostling for position, whispering furiously about rig requirements, faculty rosters, and time trials. Lomi leaned over the heads of two shorter students, his mechanic's eyes scanning the dense schedule of upcoming freshman trials. <!-- L1882 --> <!-- L1894 -->

"You can't theory your way through life," Lomi grunted, tapping a heavy finger against the parchment. "You build things, you fix things, you fly things. Look at this schedule." <!-- L1894 --> <!-- L1900 --> <!-- L1906 -->

The official parchment laid out the grueling freshman calendar in stark, unyielding terms:
- **Wednesday Afternoon:** The Upperclassman Resonance Race in the Apex Ring.
- **Thursday Morning:** First-Year Rig Inspection & Team Sorting.
- **Friday Dawn:** The Basalt Run entrance trial and written exam battery. <!-- L1908 --> <!-- L1918 --> <!-- L1930 --> <!-- L1942 -->

"We know we got to find Lucky at some point," Ignatius pointed out, crossing his arms over his chest as he studied the dates. "If Friday's exam is anything like Hollow's lecture, we're going to need every edge we can find. But look at Wednesday—that race is going to draw every mechanic and pilot on the island." <!-- L1954 --> <!-- L1966 --> <!-- L1978 --> <!-- L1987 -->"""
        },
        19: {
            "ch_num": 39,
            "title": "Memories of Spires & Gliders",
            "prose": """As they walked toward the outer stone terraces overlooking the great drop into the lower basin, Lomi's eyes gleamed with an unfamiliar fire. The mention of the Apex Ring had struck a deep, nostalgic chord within the mechanic. The weariness from Hollow's classroom evaporated, replaced by the fierce, focused energy of a craftsman in his element. <!-- L1988 --> <!-- L1994 --> <!-- L2000 -->

"The Apex Race," Lomi said, his voice full of genuine reverence. "The Reso Race. We have got to get a team together for this!" <!-- L2030 --> <!-- L2032 --> <!-- L2034 -->

Ignatius looked surprised, matching Lomi's brisk stride. "You've seen it?" <!-- L2034 -->

"Ever since I was a kid," Lomi nodded eagerly, gesturing with both hands as memories flooded back. "When my dad retired from the yard, he bought tickets way up in the basalt grandstands where you could see the entire track layout across the canyon. But later, when I started working for the union, I was down in the undercroft beneath the floor. Our crew had to crawl through the maintenance tunnels to make sure the resonance spires were drawing power correctly." <!-- L2034 -->

He paused by the balustrade, looking out over the clouds and sketching the aerial arena in empty air. "Each city has its own spire, its own harmonic frequency. You build a rig, launch it into the ring, and hit the energy nodes as they light up. You don't know when a spire is going to erupt with power, and when it does, three rigs dive for it simultaneously, scraping hulls and trading paint. You collect the charge, race to the center pillar, and discharge it to score." <!-- L2034 --> <!-- L2036 -->

Lomi shook his head with a wide grin. "One season I was up on the glider launch platform fixing a stuck pneumatic ram. Looking out over that stadium with thirty thousand people screaming... I think folks take to the sky just for the view. It made me queasy, but man, it was a sight to behold. If we build a rig and finish in the top tier, we can write our own ticket." <!-- L2036 --> <!-- L2038 --> <!-- L2108 --> <!-- L2117 -->"""
        },
        20: {
            "ch_num": 40,
            "title": "Rigs, Bets, and Skipping Class",
            "prose": """The temptation was overwhelming. To their left lay the stone corridors leading back to the classrooms where theoretical navigation was about to begin; to their right lay the workshops, the alleyways, and the rumor of Lucky. <!-- L2118 --> <!-- L2120 --> <!-- L2124 --> <!-- L2130 -->

Iggy was currently in the throes of an epic food coma from his morning buffet rampage. The soil-kin blinked sleepily through his goggles, perfectly content to wander wherever the group went so long as nobody forced him to do long division or memorize wind vectors. "I'd rather explore than sit in a classroom," his muffled posture communicated clearly, his little hands buried deep in the pockets of his heavy trench coat. <!-- L2150 --> <!-- L2153 --> <!-- L2156 --> <!-- L2158 -->

"Look," Ignatius said, tapping his chin thoughtfully. "Class is going to be there tomorrow. The lecture notes can be copied, but Lucky moves around, and the rig workshop opens early for registered teams. If we're going to compete in the race and survive Friday, we need parts, and we need those exam notes." <!-- L2166 --> <!-- L2178 --> <!-- L2190 -->

They pooled their effort, ducking beneath the covered arches of the old cloister and asking discreet questions among the grease monkeys, apprentices, and dispatch runners. It cost them two points of collective Hope and forty minutes of dodging academy proctors, but finally, a tip pointed them down an isolated maintenance alleyway behind the cartography archives. <!-- L2202 --> <!-- L2214 --> <!-- L2226 -->

"One thing you ought to know," a passing courier warned them before vanishing around a corner into the steam vents. "Val told Lucky he wasn't allowed to take coin for the notes. Val wrote the test and forbade cash sales. If you want Lucky's goods, money won't do it." <!-- L2230 --> <!-- L2238 --> <!-- L2241 --> <!-- L2243 -->"""
        },
        21: {
            "ch_num": 41,
            "title": "The Sky Dragon & The Sea Dragon",
            "prose": """In the shadow of a rusted steam conduit at the end of the blind alley, they found him. Lucky was an wiry, sharp-eyed upperclassman leaning against a crate of copper tubing, tossing a brass coin into the air and catching it with practiced ease. <!-- L2244 --> <!-- L2254 --> <!-- L2264 -->

"You're late," Lucky said without looking up from his coin. "And don't bother reaching for your coin purse. Val made me swear on my mother's grave: no gold. I only trade in secrets. Genuine secrets. The kind you don't tell your bunkmates." <!-- L2274 --> <!-- L2284 --> <!-- L2294 -->

Lomi and Ignatius exchanged a glance. Ignatius stepped forward, adjusting the folds of his dark cloak as the embers around his brow flared softly into bright gold. <!-- L2300 --> <!-- L2302 -->

"Well, when I was a child," Ignatius began, his voice dropping into the deep, resonant cadence of a seasoned fire-teller, "what I was told about the birth of the Ashwood Islands goes back millennia. Millennia. In those days, there was a great dragon of the sky and a great dragon of the sea. They respected each other, but they were separated by the horizon. They could see each other from afar, and they were lonely. Year after year, the sky dragon passed above the swells, longing to meet." <!-- L2304 --> <!-- L2306 --> <!-- L2308 -->

Lucky stopped tossing his coin, his gaze locked on Ignatius as the flame-haired cadet spoke. <!-- L2308 -->

"Then came a trickster demon," Ignatius continued softly. "He told the sky dragon that all he had to do was fly to the very zenith of the heavens—as high as wings could carry him—and dive straight down. 'Break the horizon,' the demon promised, 'and you will meet.' And so the sky dragon climbed into the black vacuum and dived like a falling star. He struck the ocean with apocalyptic force, shattering the horizon, fracturing the world, and throwing up the volcanic pillars that became our islands." <!-- L2308 --> <!-- L2314 --> <!-- L2324 -->

Lucky let out a slow, appreciative whistle, giving Ignatius a crisp nod. "That's a hell of a story, fire-boy. But ancient myths don't pay the butcher. I need something raw. Something personal." <!-- L2334 --> <!-- L2338 --> <!-- L2342 --> <!-- L2345 -->"""
        },
        22: {
            "ch_num": 42,
            "title": "The Golden Receipt & The Secret Chamber",
            "prose": """Ignatius and Lomi turned in unison, looking down at Iggy. <!-- L2338 --> <!-- L2340 -->

"Iggy," Ignatius nudged gently. "Share something with our pal Lucky. Tell him about when you cracked Britt's ribs back among the tangled greenhouse roots, or show him what you've got in your coat." <!-- L2340 --> <!-- L2342 --> <!-- L2344 -->

Iggy looked up with his round copper goggles, utterly bewildered by the transaction. "I don't even know what test we're taking. What is the test? I don't even know why we're here. All I know is I'm here." <!-- L2406 --> <!-- L2408 --> <!-- L2410 --> <!-- L2411 --> <!-- L2413 -->

Lucky raised an eyebrow, smirking down at the small clay figure. "You might be the second most interesting person I've met today. The other one almost electrocuted me. But you got to have something worth trading." <!-- L2414 --> <!-- L2415 --> <!-- L2419 --> <!-- L2421 -->

Iggy patted down the oversized pockets of his heavy wool trench coat. Past the damp moss clumps, past the dried soil rations and the flexible copper goggle straw, his fingers closed around a stiff piece of vellum he had been carrying since the entrance trials. <!-- L2422 --> <!-- L2424 --> <!-- L2426 -->

"I don't know what this means," Iggy said simply, holding out his official exam receipt. <!-- L2427 -->

Lucky casually took the paper, glanced at it—and froze. Across the header of the slate receipt was a heavy, embossed seal in pure, shimmering auric gold leaf, pulsing with an untraceable resonant signature. <!-- L2428 -->

Lucky's face drained of color, his smirk vanishing instantly. "You don't... you don't know what this is?" he whispered, his swagger completely evaporating. "She didn't know what hers meant either. She wasn't damn gold..." <!-- L2428 --> <!-- L2430 -->

He grabbed the edge of Iggy's sleeve, glancing sharply left and right down the empty corridor. "Get out of the main road. Right now. In here." <!-- L2430 --> <!-- L2432 -->

Lucky threw open a heavy iron-banded doorway leading into a secluded storage vault, ushering Ignatius, Lomi, and Iggy inside and slamming the heavy latch shut behind them. <!-- L2436 --> <!-- L2440 --> <!-- L2445 --> <!-- L2448 --> <!-- L2451 -->"""
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
        
        out_file = os.path.join(blocks_dir, f"s4-scene-{sid:02d}.md")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(full_content)
        print(f"Wrote {out_file} ({len(prose.split())} words, range [{start}, {end}])")

if __name__ == "__main__":
    main()
