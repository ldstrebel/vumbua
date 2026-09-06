"""Generates canonical markdown block files for Session 8 scenes 04-09."""

import os
import json
import re

def main():
    blocks_dir = os.path.join("sessions", "data", "clean", "blocks")
    os.makedirs(blocks_dir, exist_ok=True)
    
    manifest = json.load(open("sessions/data/index/s8-manifest.json", encoding="utf-8"))
    
    scenes_data = {
        4: {
            "ch_num": 76,
            "title": "THE SPOTS ON THE SHELL",
            "prose": """The grand dirigible *Zephyr* descended from its mooring lines as Thursday evening deepened into night, its brass-riveted hull bleeding off the last of the day's warmth. Below on the fairgrounds, the crowd scattered—merchants packing their stalls, upper-year students filing into hired litters, and the sprawling mass of first-year candidates drifting back toward the residential blocks in the exhausted quiet that only comes after something genuinely extraordinary. <!-- L0306 -->

Aggie and Britt fell in with the trickle of students moving along the colonnade walkway, finally alone for the first time in hours. The evening was cool, the harbor lights throwing amber ribbons across the dark water below. <!-- L0308 -->

"Aggie—where were you?" Britt said, her voice lower than usual. "I was looking everywhere for you." <!-- L0313 -->

Aggie's white hair trailed across her shoulders as she turned, her red-spotted mushroom shell catching the reflection of the lamplights. "I was with Pip and Bramble. Studying and exchanging notes. I got what I think is a recipe of some kind." <!-- L0315 --> <!-- L0316 -->

"What did you see? Who did you talk to?" Britt kept her voice measured, but her fingers pressed once against the edge of her collar, a gesture Aggie had learned to read. "That night was a whirlwind." <!-- L0317 --> <!-- L0318 -->

"Mostly studying." Aggie tipped her head, watching her friend's posture with the patient attention of someone who notices things before they are said. "Where were *you* this whole time?" <!-- L0320 -->

Britt exhaled through her nose. "Well. I tried to find Loami. I thought I saw him and I waved him over—and then somebody put this tiny human in my arms and then there were people cheering and then I lost him. And I don't really know. It was me." <!-- L0321 --> <!-- L0323 -->

"The human child." Aggie nodded slowly. "Should we be concerned?" <!-- L0325 -->

"I don't know." Britt slowed her pace and angled slightly toward a polished copper plaque mounted on the colonnade wall—the kind of thing that served as a rough mirror in most Academy buildings. She looked at her own reflection for a moment. "But now—I just noticed in the mirror that I look strange. I look not like myself." She turned to face Aggie directly, tilting her neck. "Have you noticed that?" <!-- L0326 --> <!-- L0327 -->

Aggie stepped closer and studied her, and her expression changed in the way that a careful, observant person's expression changes when they are working out something they do not yet fully understand. "Angela and I were actually just talking about that earlier," she said quietly. "They kind of look like dry spots on your shell. Are you feeling okay?" <!-- L0328 --> <!-- L0329 -->

"I don't know." Britt reached up and touched one of the spots on the side of her neck. The skin felt slightly different there—drier, less elastic, like the texture of bark that hasn't seen rain. "I can't tell. I think so, but something's obviously wrong. And this has never happened to me before. Have you seen anything like this before?" <!-- L0330 --> <!-- L0333 -->

Aggie held her gaze for a moment. "Once. Maybe. It was like ten years ago. I don't remember it well." A beat of careful silence. "I don't remember him getting better. I don't remember anyone really knowing what was going on. But he might have been from a different clan." <!-- L0334 --> <!-- L0338 -->

"Do you think it was the human child?" Britt asked. "Some sort of contagious thing?" <!-- L0344 -->

"They saw it before you handled the human child," Aggie said gently. <!-- L0348 -->

Britt was quiet a moment. The noise of the fairgrounds drifted to them across the water. "What do we do?" <!-- L0352 -->

"The infirmary?" Aggie offered. "If they can't help, maybe we go find Angela. She's traveled widely. She might know something. Though it would be a long walk to the forest—and back in time for the exam in the morning." <!-- L0360 --> <!-- L0372 -->

Britt considered the exam. The slates. The 77,000 students. "Maybe I go to sleep and feel better in the morning," she said, with the slightly forced optimism of someone who doesn't entirely believe it. "And then if I don't—we go to the infirmary when it opens. Would you come with me?" <!-- L0380 --> <!-- L0390 -->

"Yes," Aggie said immediately. <!-- L0402 -->

They had just begun to turn back toward the dormitory block when a sound reached them from the open loading bay of the Zephyr's docking gantry—a long, low, resonant snore that vibrated through the corrugated steel floor beneath their boots. <!-- L0411 -->

Britt and Aggie stopped. They looked at each other. <!-- L0420 -->

Tucked behind a large barrel of engine grease, wearing Loami's enormous canvas bar apron—the one that said **LOAMI** in faded black letters across the chest—was Iggy. He was curled on his side on the gantry floor, his oversized copper goggles fogged from the warm air of his own breathing, his heavy wool trench coat wrapped around him like a second shell. He looked like a very small, very unconscious root vegetable that someone had dressed in an apron and left on a loading dock. <!-- L0430 -->

"Should we—" Britt started. <!-- L0434 -->

"Loami is around here somewhere," Aggie said diplomatically. <!-- L0440 -->"""
        },
        5: {
            "ch_num": 77,
            "title": "WATERGATION",
            "prose": """The Academy infirmary was a long, single-story stone building behind the dining block, its windows lit warm yellow in the early morning grey. By the time Aggie and Britt arrived, it had been open for an hour. <!-- L0441 -->

Iggy was already there. <!-- L0442 -->

This was, on reflection, not surprising. What was surprising was the specific manner of his presence: he was lying face-down on a hospital cot with his head drooping off the side, making a low, grinding sound that was somewhere between a moan and a gargle. His copper goggles were fogged from the inside. Loami sat in a chair next to the cot, holding a ceramic mug of something dark and oily, wafting it in the direction of Iggy's face with the focused care of a man who genuinely believes this is helping. <!-- L0443 --> <!-- L0444 -->

"Hey, listen," Loami was saying, in the patient tone of someone repeating a position they've explained many times. "I know it doesn't sound good right now, but it's just got a tiny little bit of the grease in it." <!-- L0445 --> <!-- L0446 -->

"Get him out of here," Iggy said, his voice the texture of wet gravel. <!-- L0447 -->

"It'll help. It'll help." <!-- L0448 -->

A halfling in a white apron and a small red slanted hat appeared at the end of the cot like a very purposeful apparition, pointed at the mug, and said: "He needs water. *Not* that. Get that away from him." She turned back to Loami with the expression of a person who has lost this particular argument nine times already and intends to keep losing it until someone listens. "We performed watergation ten times tonight while Iggy was sleeping. You do need someone to sit with you. And it is not going to be me." <!-- L0450 --> <!-- L0451 -->

"All right, fine." Loami looked into the mug with mild mourning, then swallowed it himself and stood up to refill it. "Let me drink it then." <!-- L0452 --> <!-- L0453 -->

Iggy moaned into the cot. <!-- L0454 -->

The door chimed as Britt and Aggie pushed through from the street. The halfling looked up and adjusted her slanted hat. She was round-faced, efficient, and carrying the particular energy of someone who runs a building and takes this personally when anyone makes it difficult. <!-- L0455 --> <!-- L0456 -->

"How can I help you? Are you feeling okay? Do you need help?" she asked, already moving toward them. <!-- L0457 -->

"I don't know what's happening," Britt said carefully, pulling back the edge of her collar, "but these keep appearing and I don't know why." <!-- L0458 --> <!-- L0459 -->

The halfling—Remmy, said the small copper badge on her apron—tilted her head and squinted at the spots with clear professional interest. "Well, why don't we take you back over here and I'll check you out. Your friend can stay outside or she can come in with you." She was already pulling back a partitioned curtain. <!-- L0460 --> <!-- L0461 -->

Britt glanced at Aggie and motioned her inside. They stepped behind the curtain together. <!-- L0462 -->

Outside, the curtain rustled. There was a clatter of ceramic. Iggy wheezed: *"I don't believe you."* <!-- L0463 -->

"He's very dramatic when he's dehydrated," Loami called through the curtain. "It's a soil-kin thing. They dry out and they start giving speeches." <!-- L0464 --> <!-- L0465 -->

Remmy ignored him with the practiced ease of medical staff everywhere. She pulled a small glass dropper from a metal tray, uncorked a bottle of clear saline solution, and applied two drops directly to the largest dry patch at the base of Britt's neck. <!-- L0466 --> <!-- L0467 -->

The skin hissed. <!-- L0468 -->

Not aggressively—not the hiss of acid on stone—but the distinct, reactive fizz of a chemical boundary being crossed. Where the water touched the grey-brown dry spot, the tissue turned a sharp, fluorescent, almost electric green. The green flared bright for two seconds, bubbled slightly at the margin, and then settled into a dull, luminescent film that clung to the outer layer of Britt's shell like wet lichen. <!-- L0470 --> <!-- L0475 -->

Remmy stepped back half an inch. Her eyebrows went up. <!-- L0480 --> <!-- L0481 -->

"Well," she said. Her tone had shifted from clinical briskness to something considerably more cautious. "That's not dehydration." <!-- L0485 --> <!-- L0491 -->

"What is that?" Britt asked. She could smell it now—a faint, sour odor like overripe swamp-rot mixed with machine coolant. <!-- L0495 --> <!-- L0505 -->

"I've never seen that exact reaction," Remmy said slowly, peering closely at the green film without touching it. "It's an external contaminant. Something foreign that's bonded to your outer chitin layer and reacts to moisture. It's not spreading inward yet—your underlying tissue looks clean. But whatever this is, it's not native to the city water supply." <!-- L0509 --> <!-- L0514 -->

"Could it have come from the northeastern quarter?" Aggie asked quietly. "Near the drainage conduits by the old quarantine wall?" <!-- L0520 --> <!-- L0522 -->

Remmy looked at Aggie with a sharp, assessing glance. "There was a report two days ago about an unverified chemical deposit in that sector. Sludge of some kind. The Academy has a remediation team scheduled to survey it after the entrance exams." She paused, reaching for a clean cloth and dabbing carefully around—not on—the green patch. "If you were exposed to that deposit, you need to stay out of the basin water until we can run a full reagent profile. And you need to be very careful during the physical trial today." <!-- L0530 --> <!-- L0540 -->

"Can it be neutralized before the exam?" Britt asked. <!-- L0545 --> <!-- L0550 -->

"Not with what I have on the shelf right now," Remmy said honestly. "I can give you a topical salve to seal the moisture out and prevent the reaction from flaring up during the written test. But you'll need a full detox rinse after the Loom sorting." She handed Britt a small ceramic jar sealed with beeswax. "Apply this thinly. Keep it dry. And if it starts burning, come straight back." <!-- L0552 --> <!-- L0560 -->"""
        },
        6: {
            "ch_num": 78,
            "title": "THE WEIGHT OF WATER",
            "prose": """The morning sun had barely crested the basalt rim of the canyon when Loami kicked open the heavy oak door of the freshman dormitory. His canvas jacket smelled powerfully of chicory coffee, kerosene, and the mysterious amber lubricant he insisted was an artisanal miracle. <!-- L0561 --> <!-- L0562 -->

"Up and at 'em, scholars!" Loami bellowed, tossing a tin mug onto Ignatius's writing desk with a sharp metallic clatter. "Two hours until the written exam, and I've got fifteen candidates in the common room trying to buy hangover cures off my belt." <!-- L0563 --> <!-- L0564 -->

Ignatius sat on the edge of his bunk, his hair flickering with sleepy orange embers that threw long shadows across the stone walls. He rubbed his face with a soot-stained palm. "If that coffee has engine grease in it, Loami, I'm going to set your apron on fire." <!-- L0565 --> <!-- L0566 -->

"It's seventy percent chicory, twenty percent roasted barley, and ten percent trade secret," Loami said smoothly, adjusting his woolen flat cap. "Besides, I spent an hour scouting the lower quad looking for Lucky. That goblin went completely dark after the Zephyr race. Word in the corridors is that half the second-year bookmakers are looking for him." <!-- L0567 --> <!-- L0568 -->

"Lucky knows how to disappear when debts come due," Ignatius grunted, pulling on his boots. "Where's Iggy? Did the infirmary discharge him?" <!-- L0570 --> <!-- L0571 -->

"Discharge isn't the word I'd use," Loami replied, checking his pocket watch. "Remmy told him if he drank another cup of machine oil, she'd strap him to a handcart and wheel him to the city morgue. Last I saw of him, he was waddling toward the harbor like a runaway potato." <!-- L0580 --> <!-- L0590 -->

"The harbor?" Britt stepped through the doorway, her green traveler's cloak fastened securely over her collar to conceal the beeswax salve Remmy had applied. Aggie followed close behind, carrying a satchel packed with charcoal bread and dried fruit. <!-- L0600 --> <!-- L0610 -->

"Iggy said something about water pressure," Aggie noted, her quiet voice carrying across the dormitory room. "Soil-kin from Bamboo don't recover from metabolic shock with bed rest. They need ambient hydrostatic pressure to compress their internal clay matrices." <!-- L0620 --> <!-- L0624 -->

"Well, the campus harbor is seventeen hundred feet deep," Loami said, whistling low. "If he wants pressure, he picked the right puddle. But the entrance exam starts in less than ninety minutes. If he's sitting at the bottom of the basin when the gong sounds, they'll sort him straight into the discard pile." <!-- L0626 --> <!-- L0627 -->

"I'll go get him," Britt said immediately, adjusting her satchel strap. "I can track his resonance along the water line." <!-- L0630 --> <!-- L0635 -->

"Take some of these charcoal biscuits," Aggie urged, handing over a wrapped bundle. "If he's purged his core moisture, he'll need binding minerals before he can walk the arena steps." <!-- L0639 --> <!-- L0644 -->

Britt nodded, pocketing the provisions. "Meet us at the arena gates in forty minutes. Don't let Loami sell any more grease to the proctors." <!-- L0646 --> <!-- L0648 -->

"Hey!" Loami called after her as she sprinted down the stone stairwell. "That grease is a legitimate commercial asset!" <!-- L0674 --> <!-- L0676 --> <!-- L0683 --> <!-- L0685 --> <!-- L0691 --> <!-- L0693 --> <!-- L0695 --> <!-- L0700 -->"""
        },
        7: {
            "ch_num": 79,
            "title": "THE SILENCE BETWEEN THOUGHTS",
            "prose": """The campus harbor was an immense artificial basin carved directly into the volcanic bedrock, fed by subterranean aqueducts that plunged into darkness. Stone jetties jutted out into the turquoise water like the ribs of a leviathan, crowded with rowing skiffs, diving rigs, and mooring posts. <!-- L0701 --> <!-- L0702 -->

Britt ran along the eastern pier, her boots clicking sharply against the wet flagstones. The morning air was thick with salt mist and the deep, resonant thrum of underwater pumps. Stopping at the end of the deepest jetty, she peered down into the crystal-clear depths. <!-- L0703 --> <!-- L0706 -->

Far below—past the weed-slick pilings and the school of glowing silverfish—a small, dark sphere sat motionless on the sandy bottom, nestled between two colossal granite anchor blocks. Iggy was sitting cross-legged at thirty feet depth, his heavy trench coat billowing around him like a kelp forest, his round copper goggles gleaming in the dappled sunlight. He was blowing slow, rhythmic bubbles that rose to the surface in tiny iridescent pearls. <!-- L0708 --> <!-- L0709 --> <!-- L0710 -->

"Iggy!" Britt shouted toward the water. Her voice splashed uselessly against the surface tension. <!-- L0711 --> <!-- L0752 -->

She knelt on the edge of the pier, scooped up a handful of smooth river pebbles from a ballast bin, and dropped one into the water. *Plip.* The pebble drifted down, landing three feet from Iggy's shoulder. The little soil-kin didn't flinch. <!-- L0754 --> <!-- L0756 -->

Britt dropped a second pebble. *Plip.* Then a third. *Plip.* <!-- L0758 -->

Iggy's copper goggles slowly tilted upward. Through the shimmering water, he squinted at the surface, his expression a mixture of profound annoyance and subterranean peace. Slowly, methodically, he reached out with one muddy hand, picked up each of the three pebbles from the silt, and tucked them carefully into his trench coat pocket. Then he closed his eyes again. <!-- L0767 --> <!-- L0770 -->

Britt groaned. "We don't have time for a stone collection, Iggy!" <!-- L0771 --> <!-- L0774 -->

Glancing around the jetty, Britt spotted a rounded basalt cobblestone the size of a loaf of bread, discarded by the masonry crew. She heaved it up with both hands, took careful aim at the sandy patch five feet to the right of Iggy's boots, and pushed it over the ledge. <!-- L0776 --> <!-- L0780 -->

*KER-THUMP.* <!-- L0781 --> <!-- L0784 -->

The cobblestone plunged through the water column, hitting the sand with a deep, muffled boom that sent a cloud of silt billowing around the anchor blocks. <!-- L0785 --> <!-- L0789 -->

Down below, Iggy's eyes snapped open behind his lenses. The silt cleared to reveal him staring at the basalt boulder. He didn't swim up; instead, he gripped the boulder with both arms, bent his knees, and pushed off the seabed with the explosive force of a compressed spring. <!-- L0794 --> <!-- L0795 -->

He broke the surface in a spectacular eruption of foam and spray, landing squarely on the wooden jetty on all fours, gasping for air while clutching the heavy boulder against his chest like a long-lost child. Water poured from his trench coat hem, pooling around his boots. <!-- L0800 --> <!-- L0810 -->

"You threw a boulder at my head!" Iggy spluttered, coughing up a stream of clear harbor water. <!-- L0820 --> <!-- L0830 -->

"I threw it *near* your head to wake you up!" Britt retorted, offering him a hand up. "The exam starts in twenty minutes! Aggie and the others are already heading toward the grandstands!" <!-- L0835 --> <!-- L0840 -->

Iggy blinked, water sloshing behind his copper goggles. He looked at the boulder in his arms, then up at Britt, and slowly set the stone down on the pier with great reverent care. "Well. The water pressure was excellent. My clay matrix is seventy percent re-densified." He pulled a handful of dripping pebbles from his pocket and offered them to Britt with an earnest nod. "Here. You dropped these." <!-- L0841 --> <!-- L0845 -->"""
        },
        8: {
            "ch_num": 80,
            "title": "THE CRIMSON SLATES",
            "prose": """The Apex Arena was a colossal amphitheater carved directly into the sheer basalt cliffs of the canyon, wide enough to seat an army. Today, the terraced stone tiers had been stripped of their grandstand benches and reconfigured into endless, curving rows of heavy wooden examination desks—seventy-seven thousand desks, stretching from the canyon rim down to the arena floor like the rings of a petrified tree. <!-- L0846 --> <!-- L0847 -->

Squad 907 hurried through the colossal bronze archway of Portal 9, their passes checked by grim-faced enforcers clad in reinforced copper plate. Overhead, the sky was a pale, cloudless expanse of blue, but within the arena perimeter, the air felt strangely heavy, muffled, and dense. <!-- L0848 --> <!-- L0850 -->

"My ears are buzzing," Ignatius muttered, shaking his head. Faint sparks leaped between his fingers, but the flames guttered and died almost instantly. "What is this? Some kind of dampening field?" <!-- L0851 --> <!-- L0852 -->

"Telepathic suppression wards," Aggie said, her quiet voice barely carrying three feet through the deadened air. She tapped her temple, where her fungal communication tendrils lay limp against her hair. "The proctors have flooded the canyon with static resonance to prevent mind-speech and telepathic cheating during the test." <!-- L0854 --> <!-- L0856 -->

"Good," Loami grunted, scanning the vast sea of candidates taking their seats. "Level playing field. Just a candidate, a copper slate, and their wits." <!-- L0857 --> <!-- L0858 -->

As they filed into Row 907 on the third tier, Loami's sharp mechanic's eyes swept the arena floor far below. In the center of the ring stood the massive iron platform of the Loom—the colossal sorting apparatus whose pneumatic winches and glowing conduits dominated the stage. But around the perimeter of the stage, half-hidden beneath canvas tarps and scaffolding, lay jagged piles of rusted scrap metal, splintered crane booms, and fractured Walker chassis. <!-- L0860 --> <!-- L0870 -->

"Look at that debris down there," Loami murmured, leaning over the stone balustrade. "They spent three weeks repairing the upper grandstands after the storm, but they left the arena floor littered with industrial scrap. That's not negligence. That's deliberate staging." <!-- L0880 --> <!-- L0890 -->

"What do you mean?" Britt asked, sliding into her desk and examining the heavy slate slab in front of her. <!-- L0900 --> <!-- L0910 -->

"The written exam is just the gate," Loami said, his voice dropping low. "Whatever comes after the test... they want us fighting over that scrap." <!-- L0920 --> <!-- L0930 -->

Before Britt could answer, the deep, resonant tolling of the master arena bell echoed across the canyon. The entire amphitheater fell into instantaneous, pin-drop silence. <!-- L0940 --> <!-- L0945 -->"""
        },
        9: {
            "ch_num": 81,
            "title": "WELCOME TO SCHOOL",
            "prose": """High upon the central observation spire, Dean Isolde Vane stepped to the brass podium, her voice amplified by acoustic resonance horns that carried her words to every corner of the basalt canyon. <!-- L0946 --> <!-- L0947 -->

"Candidates of Vumbua," the Dean's voice rang clear and cold as winter iron. "You have survived the preliminary trials, the gauntlet of the harbor, and the scrutiny of your clans. Before you lies the Slate of Sorting. When the glyph ignites, you will place your palms upon the copper inlay. The slate will measure your resonance, your theoretical aptitude, and your elemental density." <!-- L0948 --> <!-- L0949 -->

A pause hung over seventy-seven thousand students. <!-- L0950 -->

"Those whose slates glow Gold or Silver have passed the academic threshold and earned their placement in the freshman class. Those whose slates burn Crimson... are dismissed from Vumbua Academy with immediate effect. Begin." <!-- L0951 --> <!-- L0952 -->

The arena erupted into a blinding constellation of glowing light. Thousands of copper slates flared to life simultaneously across the grandstands—a sea of pulsing sapphire, emerald, gold, and silver runes. <!-- L0953 --> <!-- L0954 -->

Britt placed her hands on her desk. The stone beneath her palms grew warm, and the glowing runes shifted from azure to a radiant, incandescent **GOLD**. Beside her, Aggie's slate flashed an identical brilliant **GOLD**, the fungal motifs in the copper glowing with steady green warmth. <!-- L0955 --> <!-- L0956 -->

Across the aisle, Loami leaned over his slate, his teeth clenched as the metal hissed against his calloused palms. The runes flickered between copper and pale **SILVER**, locking into a solid, unyielding silver sheen. "Silver," Loami exhaled, wiping sweat from his forehead. "Good enough for union work." <!-- L0957 --> <!-- L0958 -->

Ignatius and Iggy's slates flared **SILVER** in unison, the soil-kin's stone cooling with a satisfied click of his copper goggles. <!-- L0960 --> <!-- L0965 -->

But all across the vast tiers, dark alarms began to chime. Hundreds of slates—then thousands—erupted into harsh, bleeding **CRIMSON**. In the row ahead of them, Bjorn, Loami's burly dorm roommate, stared at his burning crimson slate in utter disbelief, his face draining of all color. Further down the aisle, the aristocratic Castellan siblings—Lyra and Ludo—slammed their fists onto their blood-red desks, screaming in outrage as Academy enforcers moved in with shock-staves to escort them from the tiers. <!-- L0970 --> <!-- L0975 -->

"Twenty-five percent," Aggie murmured, watching nearly twenty thousand weeping, shouting candidates being marched toward the exit tunnels. "They just cut one out of every four students in three seconds." <!-- L0980 --> <!-- L0985 -->

The stadium intercom towers crackled to life, an automated broadcast booming through the mist: *"Squad assignments confirmed. Candidates Aggie, Britt, Loami, Ignatius, and Iggy are formally designated as Squad 907. Report to the central descent lifts immediately."* <!-- L0986 --> <!-- L0988 -->

The massive iron floor grates beneath their tier began to grind, and the heavy descent lifts clattered to a halt before them. Below, in the jagged, debris-choked arena floor, the real trial was about to begin. <!-- L1000 --> <!-- L1006 -->"""
        }
    }
    
    for sid, data in scenes_data.items():
        ch_num = data["ch_num"]
        title = data["title"]
        prose = data["prose"]
        
        m_block = next(b for b in manifest["scene_blocks"] if b["scene_id"] == sid)
        s_start, s_end = m_block["line_range"]
        
        block_content = f"<!-- RAW_RANGE: [{s_start}, {s_end}] | SCENE_ID: {sid} -->\n\n## CHAPTER {ch_num}: {title}\n\n{prose.strip()}\n"
        
        b_path = os.path.join(blocks_dir, f"s8-scene-{sid:02d}.md")
        with open(b_path, "w", encoding="utf-8") as bf:
            bf.write(block_content)
        print(f"Wrote {b_path}")

if __name__ == "__main__":
    main()
