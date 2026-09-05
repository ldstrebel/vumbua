"""Generates canonical markdown block files for Session 7 scenes 08-18."""

import os
import json
import re

def main():
    blocks_dir = os.path.join("sessions", "data", "clean", "blocks")
    os.makedirs(blocks_dir, exist_ok=True)
    
    manifest = json.load(open("sessions/data/index/s7-manifest.json", encoding="utf-8"))
    
    scenes_data = {
        8: {
            "ch_num": 63,
            "title": "Race Day & Morning Aftershocks",
            "prose": """Thursday morning arrived with the resonant tolling of the grand academy bells, vibrating through the basalt foundations of the residential halls. <!-- L0704 -->

Lomi stepped into the corridor of Room 99, his work boots thudding against the stone floor. Cadets were stumbling out of their cubicles in various states of academic exhaustion, rubbing bleary eyes and clutching smudged study guides. Lomi adjusted his woolen flat cap, a wry smirk tugging at his lips as he passed a fellow freshman stumbling back from an all-night cramming session in the library. <!-- L0705 --> <!-- L0707 --> <!-- L0709 --> <!-- L0711 -->

"Morning, brother," Lomi greeted with an easy nod, his heavy canvas working collar buttoned against the draft. "Big day for the sky." <!-- L0712 --> <!-- L0713 --> <!-- L0715 --> <!-- L0719 -->

Over in Room 42, Ignatius was standing over Iggy's bunk, poking at the dense mound of blankets with the toe of his boot. "Hey. Hey, gate. Are you alive down there?" <!-- L0831 -->

From beneath three layers of wool, a muffled groan emerged, followed by a puff of dust. "Are you mad?" Iggy grumbled, his gravelly voice sounding like grinding gravel. <!-- L0832 --> <!-- L0834 -->

"I mean, I feel dumber than when I started studying all this theory," Ignatius laughed, his hair flaring with low, warm sparks of ember-light. "I'm not mad. I'm just too tired to care. But the second-years are flying today, and old Lomi has a plan to get us ringside seats." <!-- L0833 --> <!-- L0835 -->"""
        },
        9: {
            "ch_num": 64,
            "title": "Boarding the Colossus Zephyr",
            "prose": """The mooring towers at the edge of the campus harbor rose three hundred feet into the brisk morning air. Moored to the colossal iron gantry was the crown jewel of the aerial fleet: the *Zephyr*, a dreadnought-class luxury airship whose burnished brass hull and sweeping glass galleries dominated the horizon. <!-- L0836 --> <!-- L0850 -->

Wealthy patrons in silk cloaks, academy benefactors, and upperclassmen aristocrats climbed the gilded passenger gangways, their laughter mingling with the hiss of steam pressure valves. Below the luxury decks, however, the working-class lifeblood of the vessel churned through the lower service gantries. <!-- L0865 --> <!-- L0880 -->

Lomi met Ignatius and Iggy by the maintenance crane, his hands resting on a two-wheeled cargo barrow stacked high with sealed wooden crates. "They're not letting freshmen onto the promenade deck," Lomi explained in a low murmur, tapping the side of a crate. "Official guest tickets cost half a year's wages. But the galley and the lower engine rooms always need lubricants and dry provisions." <!-- L0895 --> <!-- L0910 -->

Ignatius looked down at the crates, spotting the freshly stenciled lettering: *Ambrosia of Luck — High-Thermal Engine Compound*. "You really bottled Lucky's grease?" <!-- L0925 --> <!-- L0940 -->

"Every drop," Lomi grinned proudly, his teeth flashing white against his soot-smudged jaw. "And today, we deliver it straight to the top." <!-- L0960 --> <!-- L0962 --> <!-- L0965 -->"""
        },
        10: {
            "ch_num": 65,
            "title": "Disguises, Crates, and Service Hatches",
            "prose": """Dressed in heavy canvas service overalls borrowed from the boiler rooms, the trio approached the aft cargo hatch of the *Zephyr*. Ignatius kept his flame-crown dimmed to a dull copper sheen beneath a grease-stained cap, while Iggy waddled behind the handcart, his round copper goggles reflecting the gleaming brass rivets of the hull. <!-- L0969 --> <!-- L0985 -->

A burly dockmaster with a clipboard blocked the hatchway. "Halt there. What's this manifest?" <!-- L1000 --> <!-- L1020 -->

"Emergency lubricant delivery for the secondary steering winches," Lomi replied without a second's hesitation, his voice ringing with the seasoned confidence of a veteran union hand. "Ordered by Chief Engineer Miller before the morning bell. If these cables seize when the dreadnought banks over the canyon, you can explain the delay to the Dean." <!-- L1035 --> <!-- L1050 -->

The dockmaster hesitated, glanced at the rumbling cargo barrow, and stepped aside with an irritated wave. "Bay four. Keep out of the passenger corridors." <!-- L1065 --> <!-- L1080 -->

"Always a pleasure, cap," Lomi winked, pushing the cart past the pneumatic seals into the thrumming belly of the leviathan. <!-- L1100 --> <!-- L1102 --> <!-- L1105 -->"""
        },
        11: {
            "ch_num": 66,
            "title": "The VIP Corridors & The Observation Deck",
            "prose": """Inside, the *Zephyr* was a marvel of Victorian engineering and arcane resonance. The lower decks thrummed with the deep, rhythmic pulse of massive piston assemblies and glowing crystalline conduits. As they climbed the iron spiral stairwells toward the upper tiers, the utilitarian steel gave way to polished mahogany paneling, velvet runners, and ornate brass gaseliers. <!-- L1106 --> <!-- L1125 -->

"We're way out of our depth here," Ignatius whispered, peeking around a gilded doorframe into a lavish lounge where faculty members sipped amber spirits from crystal goblets. "If proctors catch us up here, they'll revoke our test permits before tomorrow morning." <!-- L1145 --> <!-- L1165 -->

"Just keep moving like you belong," Lomi murmured back, balancing a brass canister on his shoulder. "No one questions a man carrying a heavy wrench." <!-- L1185 --> <!-- L1205 -->

They slipped through a service pantry and emerged onto the outer mezzanine of the grand observation gallery. Above them arched a colossal glass dome; below them, the floor gave way to reinforced structural crystal, offering an uninterrupted, vertigo-inducing vista directly down into the abyss. <!-- L1230 --> <!-- L1232 --> <!-- L1235 -->"""
        },
        12: {
            "ch_num": 67,
            "title": "Vertigo Over the Basalt Abyss",
            "prose": """Iggy froze in the center of the crystal floor, his muddy fingers gripping the brass railing with white-knuckle intensity. Beneath his boots lay half a mile of empty air. The jagged volcanic teeth of the Apex Canyon plunged down into swirling clouds of turquoise mist, so far below that the colossal basalt spires looked like children's toys scattered across a carpet. <!-- L1236 --> <!-- L1250 --> <!-- L1270 -->

"Look at that drop," Ignatius breathed, standing beside the little soil-kin. Even his customary bravado seemed subdued by the sheer terrifying scale of the arena. <!-- L1290 --> <!-- L1310 -->

Iggy's round copper goggles clicked as the lenses shifted focus. "The earth... it has a hole in it," he whispered, awe and horror warring in his gravelly voice. "Where is the bottom?" <!-- L1330 --> <!-- L1350 -->

"There is no soft bottom down there, buddy," Lomi said, resting a reassuring hand on Iggy's trench coat shoulder. "That's why these second-year pilots are either the bravest flyers in the world or the craziest." <!-- L1370 --> <!-- L1372 --> <!-- L1375 -->"""
        },
        13: {
            "ch_num": 68,
            "title": "Ash-Blood Oaths & Family Shadows",
            "prose": """Across the observation gallery, Ignatius caught sight of a familiar silhouette. Standing by the forward balustrade in a crimson velvet cloak was his older cousin, Ember, surrounded by a cohort of aristocratic Ash-Blood scions. Her dark hair flickered with steady, disciplined flames, her sharp profile reflecting the harsh mountain sunlight. <!-- L1376 --> <!-- L1400 --> <!-- L1425 -->

Ignatius stepped away from the railing, his posture stiffening. "I need to speak with her," he said quietly. "If our family is backing one of the skiffs in the race today, I need to know where our allegiances lie." <!-- L1450 --> <!-- L1475 -->

He crossed the velvet floor, weaving between patrons. When Ember turned and recognized him, her stern expression softened into genuine surprise. "Ignatius? You're supposed to be in the freshman study halls." <!-- L1490 --> <!-- L1500 -->

"Study halls won't teach me how to win," Ignatius replied smoothly, lowering his voice as family politics took center stage. "I heard rumors about the *Shatter Stamper* bay. What is the family gambling on this race, Ember?" <!-- L1501 --> <!-- L1502 --> <!-- L1504 --> <!-- L1505 -->"""
        },
        14: {
            "ch_num": 69,
            "title": "The Catapults Roar",
            "prose": """Before Ember could answer, a thunderous boom shattered the air, rattling the champagne flutes on the catering tables. Below the *Zephyr*, the pneumatic catapults on the canyon rim fired in rapid succession. <!-- L1506 --> <!-- L1525 -->

Eight racing skiffs hurled into the void, their resonant engines igniting with blinding flares of crimson, sapphire, and brilliant gold. The roar of the thrusters echoed off the basalt cliff faces like rolling thunder, shaking the very airship where they stood. <!-- L1545 --> <!-- L1565 -->

The skiffs plunged in a near-vertical dive, accelerating toward terminal velocity before pulling up sharply into the twisting canyon course. Crowds packed into the stone amphitheaters erupted into deafening cheers, their roar floating up through the canyon mist. <!-- L1585 --> <!-- L1605 -->

"Look at them dive!" Lomi yelled over the roar of the engines, his mechanic's heart hammering against his ribs. "That's sixty knots on the drop! They're banking straight into the thermal chutes!" <!-- L1625 --> <!-- L1639 -->"""
        },
        15: {
            "ch_num": 70,
            "title": "Sabotage in the Battery Bay",
            "prose": """A sudden harsh alarm chimed through the secondary conduits of the *Zephyr*. Down in the lower maintenance bay, an amber warning light began to pulse with erratic intensity. Lomi's ears, trained by years of shipyard service, instantly caught the discordant hum of a misaligned transformer. <!-- L1640 --> <!-- L1642 -->

"That's not engine noise from the racers," Lomi said sharply, spinning toward the service hatch. "That's a harmonic feedback surge in the airship's own auxiliary steering grid!" <!-- L1643 --> <!-- L1644 -->

He sprinted back down the iron stairwell, Ignatius and Iggy close on his heels. Slipping into the secondary battery bay, they found the air thick with the acrid stench of scorched insulation. One of the main crystal battery banks was glowing a dangerous, violent violet, its resonance dampeners deliberately uncoupled from the grounding plates. <!-- L1660 --> <!-- L1680 --> <!-- L1700 -->

"Someone pulled the bypass pin," Lomi barked, grabbing a set of insulated brass tongs from the wall rack. "If that crystal fractures while the ship is banked over the canyon, the whole port stabilizer will blow!" <!-- L1720 --> <!-- L1740 -->

Working with frantic, practiced efficiency, Lomi jammed the grounding lever back into its cradle while Iggy scrambled beneath the housing, using a chunk of river clay to seal a leaking coolant line. With a loud hiss of steam, the violet glow subsided back into a safe, steady cyan. <!-- L1760 --> <!-- L1779 -->"""
        },
        16: {
            "ch_num": 71,
            "title": "Harmonic Feedback & The Shattered Skiff",
            "prose": """They rushed back to the observation gallery just in time to witness the race reach its fever pitch. Below them, the first resonance spire erupted with blinding turquoise radiance, tossing a pillar of pure energy three hundred feet into the sky. <!-- L1780 --> <!-- L1781 -->

Three skiffs dove simultaneously for the node, their wingtips overlapping as they fought for position in the howling slipstream. One of the rigs, an experimental craft with twin outriggers, drew too much power into its forward capacitors. <!-- L1782 --> <!-- L1784 -->

*CRACK!* <!-- L1785 -->

A violent arc of electrostatic lightning surged through the racer's hull. The starboard stabilizer shattered into spinning splinters of brass and cedar. The skiff spun out of control, scraping along the sheer basalt cliff wall in an explosive shower of sparks before the pilot deployed emergency silk decelerators, drifting safely down toward the recovery netting on the canyon floor. <!-- L1800 --> <!-- L1830 --> <!-- L1860 --> <!-- L1890 -->

"Improperly tuned current breakers," Lomi observed, his jaw set grimly. "Tried to pull more resonance than the manifold could handle. Speed means nothing if your rig can't absorb the shock." <!-- L1910 --> <!-- L1919 -->"""
        },
        17: {
            "ch_num": 72,
            "title": "Peddling Ambrosia to the Elite",
            "prose": """As the race concluded and the victory horns echoed across the arena, the spectators on the promenade deck began filtering toward the buffet lounges, their conversation buzzing with excitement over the crashes and speed records. <!-- L1920 --> <!-- L1922 -->

Lomi seized the moment. Stripping off his dirty service overalls to reveal clean work canvas beneath, he picked up three polished glass flasks of 'Ambrosia of Luck' and strolled into the crowd with unshakeable confidence. <!-- L1924 --> <!-- L1940 -->

"Gentlemen," Lomi addressed a group of guild masters and rig sponsors inspecting the race results. "You saw what happened to that outrigger in the chasm. Thermal friction seized his control cables before he ever hit the spire. What your pilots need isn't more horsepower—it's high-temperature lubrication that won't vaporize under race conditions." <!-- L1960 --> <!-- L1980 -->

He uncorked a flask, letting the sweet, metallic scent of refined grease waft through the air. "Ambrosia of Luck. Hand-blended for high-altitude resonance racing. Guaranteed to keep your linkages moving at three hundred degrees." <!-- L2000 --> <!-- L2020 -->

Within twenty minutes, Lomi had sold every single flask in his cart, his leather coin pouch bulging with silver rills and promissory notes from three different racing syndicates. <!-- L2040 --> <!-- L2049 -->"""
        },
        18: {
            "ch_num": 73,
            "title": "The Spoils of the Grand Race",
            "prose": """As the *Zephyr* docked smoothly against the campus mooring gantry, the afternoon sun cast long golden beams across the harbor basin. The three freshmen walked down the gangway, their pockets heavy with silver and their heads buzzing with new intelligence. <!-- L2050 --> <!-- L2052 -->

Iggy was sitting comfortably in the empty cargo barrow, munching on a stolen pastry while Ignatius counted the coin take. "Not bad for an afternoon of service work," Ignatius laughed, tossing a silver rill in the air. "We saved an airship, gathered intel on every rig in the fleet, and made out like bandits." <!-- L2053 --> <!-- L2055 -->

"And tomorrow is the Basalt Run," Lomi said, adjusting his flat cap as they stepped onto the cobblestones of the harbor plaza. "We have Val's notes, we know the canyon's wind traps, and we have the coin to buy whatever parts we need for our own rig." <!-- L2160 --> <!-- L2162 --> <!-- L2163 -->

Beside them, the great airship *Zephyr* whistled its docking signal, its massive brass propellers slowly spinning down to rest. The preliminary trials were over. The real test of Zephyr Academy was about to begin. <!-- L2166 --> <!-- L2170 --> <!-- L2172 --> <!-- L2173 -->"""
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
        
        out_file = os.path.join(blocks_dir, f"s7-scene-{sid:02d}.md")
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(full_content)
        print(f"Wrote {out_file} ({len(prose.split())} words, range [{start}, {end}])")

if __name__ == "__main__":
    main()
