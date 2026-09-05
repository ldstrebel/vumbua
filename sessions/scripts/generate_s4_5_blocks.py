"""Generates canonical markdown block files for Session 4.5 scenes 02-05."""

import os
import json
import re

def main():
    blocks_dir = os.path.join("sessions", "transcripts", "clean", "blocks")
    os.makedirs(blocks_dir, exist_ok=True)
    
    manifest = json.load(open("sessions/transcripts/index/s4.5-manifest.json", encoding="utf-8"))
    
    scenes_data = {
        2: {
            "ch_num": 43,
            "title": "Roots, Karma, and Morning Bells",
            "prose": """The quiet of the freshman residential quarters was thick and heavy, punctuated only by the distant hiss of academy steam conduits and the muted breathing of sleeping cadets. <!-- L0123 -->

Britt and Aggie walked together down the dimly lit corridor of Block 12. Britt's fingers curled tightly around the carved wooden charm of her necklace, her knuckles pale beneath her olivaceous skin. The violence of the alleyway encounter still reverberated through her core like an unnatural harmonic hum. Back among the Mazizi clan, the deep fungal passage network and the ancient canopy bound everyone together. In a community where every life was tethered by shared roots, person-to-person cruelty was practically unthinkable. If you harmed another, the injury echoed across the whole network and returned to you with the relentless inevitability of rot feeding the soil. <!-- L0125 --> <!-- L0128 --> <!-- L0129 --> <!-- L0131 -->

"I just don't understand why that happened," Britt whispered as they reached their cubicle door, her voice trembling with lingering shock. "I was just talking to them." <!-- L0133 --> <!-- L0135 -->

Aggie squeezed her cousin's hand, her own sharp gaze steady in the gloom. "It's so weird. Like, why? I don't get it either. But his karma came quickly. Death comes to us all, one way or another." <!-- L0136 --> <!-- L0138 --> <!-- L0139 -->

The Mazizi perspective was grounded in the great natural cycles: life fed into death, decay nourished new growth, and traveling solo through the mycelial paths risked losing one's grounding to the outer world. To lash out without reason was the mark of someone whose spirit had severed its roots. Outside the cubicle, Britt paused, drawing a deep, stabilizing breath of cool air before stepping inside. She squeezed Aggie's hand once more, slid beneath her coarse woolen blanket, and let exhaustion claim her. <!-- L0140 --> <!-- L0142 --> <!-- L0145 --> <!-- L0147 --> <!-- L0157 --> <!-- L0159 --> <!-- L0164 -->

When the great brass horns blared at dawn, the sound vibrated straight through the stone floorboards. Block 12 was a sprawling, repurposed green room where open floor spans and tiered plant-potting benches had been hastily partitioned into cubicles. Light filtered through high clerestory windows, illuminating lush fern growth and creeping moss that still clung to the stone walls. Stamped onto the heavy double doors of their hall was the day's curriculum slate: Reality Anchoring in the third amphitheater, followed by Aetheric Defense. <!-- L0170 --> <!-- L0173 --> <!-- L0175 --> <!-- L0177 -->

Aggie had already been awake for an hour, perched alertly on the edge of her bunk and listening to the excited chatter of waking students as they prepared for breakfast. Britt sat up in a quiet meditative pose among the green leaves, centering her spirit against the unfamiliar pressures of the academy. <!-- L0179 --> <!-- L0181 --> <!-- L0185 --> <!-- L0194 --> <!-- L0196 --> <!-- L0206 --> <!-- L0219 -->"""
        },
        3: {
            "ch_num": 44,
            "title": "The Talking Stones & The Breakfast Line",
            "prose": """Aggie held Britt's hand, guiding her out of Block 12 and into the vibrant sunlight of the quad. "Brace yourself," Aggie murmured with a conspiratorial grin, "because I definitely found someone who is eating her way through the entire pantry." <!-- L0221 --> <!-- L0223 -->

A small, energetic girl with wild curls bounded toward them, practically vibrating with excitement. "Hi! Hi! Are you Aggie's cousin?" Pip chirped, bouncing on the balls of her feet. "Are you ready to get food? I hear they've been cooking all night for us! The biscuits! The fresh churned butter!" <!-- L0225 --> <!-- L0227 --> <!-- L0229 -->

Beside Pip stood Bramble, a towering, gentle youth whose skin was textured like seasoned ironwood, with delicate cedar needles sprouting from his shoulders. Bramble pulled a flask of cool water from his satchel, offering it to Britt with a slow, courtly incline of his leafy head. Peeling off toward the tables was Saffron, a quiet girl with charcoal smudges on her wrists who was already immersed in a sketchbook. <!-- L0231 --> <!-- L0233 --> <!-- L0237 --> <!-- L0239 -->

Walking alongside them was Kale, a slender, bespectacled boy with ink-stained cuffs who was balancing three carved slate stones in his palms. Britt tilted her head, watching the stones hum with faint resonant energy. "What are those?" she asked. <!-- L0241 --> <!-- L0243 -->

Kale pushed his spectacles up his nose, looking sheepish yet impassioned. "It sounds silly, but I really think rocks can talk. Back home, my family works the crystal veins. Resonance is like an underground river of power flowing through the world. If I can tune these resonators to the same harmonic frequency, we can bridge voice vibrations across miles—like a handheld radio, but powered purely by stone." <!-- L0245 --> <!-- L0247 --> <!-- L0281 --> <!-- L0313 -->

In the dining pavilion, the aroma of roasted foods filled the vaulted ceiling. While Pip piled her tray high with warm biscuits, honey, and strips of sizzling salt-pork, Britt selected only a handful of steamed berries, roasted squash seeds, and wild tubers—the traditional gatherer sustenance of her people. <!-- L0323 --> <!-- L0325 --> <!-- L0327 --> <!-- L0335 -->

"Wait," Britt asked, pointing a cautious finger at Pip's plate. "What is that crispy strip?" <!-- L0337 --> <!-- L0341 -->

"Bacon!" Pip beamed proudly, taking a massive crunchy bite. "It's a little pig. Roasted with brown sugar!" <!-- L0346 --> <!-- L0370 -->

Britt froze, her dark eyes widening in unvarnished horror. To eat a dead creature simply because it tasted sweet—without ritual prayer, without offering its bones back to the earth—was an entirely alien concept. "You... you like the dead thing?" Britt murmured, gently setting her berries down as the warning bell began to chime above the hall. <!-- L0376 --> <!-- L0399 --> <!-- L0407 -->"""
        },
        4: {
            "ch_num": 45,
            "title": "Professor Thorne & The Dead Island",
            "prose": """The third amphitheater was an imposing bowl of dark slate benches, tiered steeply around a central dais. Professor Silas Thorne stood before a massive brass orrery, his dusty traveler's cloak still stained with red clay from distant expeditions. His pale blonde hair hung loose over a sharp, weathered face that held none of the academic softness of his peers. <!-- L0409 --> <!-- L0411 --> <!-- L0419 --> <!-- L0421 --> <!-- L0425 -->

"Reality Anchoring," Thorne began without preamble, his gravelly voice cutting through the whispering freshmen like an axe through kindling. "Most of you think this academy is teaching you to conquer the sky. You are wrong. This institution exists for one solemn duty: to ensure that the end of the world does not catch us unawares." <!-- L0437 --> <!-- L0452 --> <!-- L0470 -->

He unrolled a broad charcoal map depicting a desolate archipelago far beyond the civilized charts. "Sixty years ago, our expedition surveyed an uncharted landmass sixty leagues past the barrier currents. We found cities of stone, aqueducts, and plazas. But there were no birds. No insects. No grass. Nothing lived. Every creature had died where it stood, leaving only dry skeletons bleached white under an empty sky. The energy had been vacuumed out of the land, leaving inert, dead matter behind." <!-- L0470 --> <!-- L0500 -->

Britt leaned forward, a chill racing down her spine. The phenomenon Thorne described sounded like an apocalyptic inversion of the crisis facing her own Mazizi homeland. In the petrified groves of her home, the forest had refused to die; here, an entire island had been stripped of the very spark of vitality. <!-- L0504 --> <!-- L0517 -->

In the front row, several noble cadets giggled nervously, whispering among themselves about party rumors. Professor Thorne's jaw tightened. He glanced at the chattering students, his eyes flashing with sudden, cold contempt. Without uttering another syllable, he snapped his heavy lecture tome shut with a thunderous clap, turned sharply on his heel, and walked straight out the side doors into the corridor. <!-- L0525 --> <!-- L0531 --> <!-- L0541 -->"""
        },
        5: {
            "ch_num": 46,
            "title": "The Edge of the World & Sterling Hall",
            "prose": """The lecture hall fell dead silent as the heavy door swung shut behind the professor. Cadets looked at each other in bewildered amusement, unsure whether class was officially dismissed or if this was an eccentric test. <!-- L0494 -->

"He ran away!" Pip gasped, her eyes snapping wide as she sprang to her feet. "We have to follow him!" <!-- L0494 --> <!-- L0500 -->

Pip vaulted onto Bramble's broad wooden shoulders, clutching his cedar-needle boughs like reins. From her elevated perch, she pointed toward the crowded central colonnade. "There! His blonde hair is turning toward the faculty stairwell!" <!-- L0504 --> <!-- L0517 -->

Britt, Aggie, and Kale sprinted after them, weaving through clusters of bewildered students. They cornered Professor Thorne at the landing of a stone spiral staircase. Thorne paused, turning to face the panting freshmen with an assessing, begrudging look of respect. <!-- L0525 --> <!-- L0531 -->

"You followed," Thorne murmured, leaning against the cold balustrade. "Perhaps you actually care to understand. When an island loses its anchor, the edge of the world catches up to it. Reality collapses. The resonance fields we generate in Harmony are not luxury power grids; they are life-support shields holding back an encroaching void. In the dead zones, our tech fails instantly, and the air itself feels like a vacuum pulling at your soul." <!-- L0541 --> <!-- L0557 --> <!-- L0563 --> <!-- L0579 --> <!-- L0583 -->

The bell for second period echoed through the arches, breaking the spell. Thorne nodded curtly, turning up the stairs. "Read chapter four. If you survive Friday, we'll discuss resonance shields." <!-- L0600 -->

Following their afternoon seminar on Aetheric Defense—where naval tacticians demonstrated heavy steel plating designed to repel colossal atmospheric beasts—Aggie and Britt bid farewell to their new friends. Before departing, Kale handed Aggie one of his experimental communication stones, its amber crystal glowing with steady warmth. "Click the bezel twice if you need to reach us," he smiled warmly. <!-- L0601 --> <!-- L0602 --> <!-- L0604 --> <!-- L0605 --> <!-- L0607 --> <!-- L0608 -->

As the sun began to dip behind the western spires, casting long violet shadows across the quad, Aggie and Britt made their way toward the upper terraces. Following the rumors of student gatherings, Aggie spotted Val walking toward Sterling Hall, surrounded by a noisy entourage of admirers. At the entrance stood two dark-haired sentinels who glared at the crowd with lethal intensity. Welcoming Val inside with a quiet greeting, the female sentinel leveled a stony, warning glare at the lingering students and slammed the heavy iron-reinforced doors shut, sealing the secrets of Sterling Hall within. <!-- L0614 --> <!-- L0616 --> <!-- L0618 --> <!-- L0620 -->"""
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
        
        out_file = os.path.join(blocks_dir, f"s4.5-scene-{sid:02d}.md")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(full_content)
        print(f"Wrote {out_file} ({len(prose.split())} words, range [{start}, {end}])")

if __name__ == "__main__":
    main()
