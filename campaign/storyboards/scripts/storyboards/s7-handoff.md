# Handoff Document: Session 7 Graphic Novel (Vertical Scroll Format)

This document is a handoff for the downstream agent or developer tasked with compiling the final graphic novel for **Session 7: Race Day**. It specifies the 15-page layout sequence, details of Kante's lore drop, the pre-made assets in the repository, and the design rules for vertical scrolling on mobile devices.

---

## 📱 Mobile-First Vertical Scroll Specifications

Instead of a traditional print layout, this session will be rendered as a **continuous vertical scroll**:
1.  **Format:** One panel per screen width/height, flowing vertically.
2.  **Gutters:** Eliminate thick margins. Use continuous vertical panels or gutterless transitions (`#### 🖤 Gutter Transition:`) to guide the viewer's eyes down the screen.
3.  **Aesthetics:** High-contrast color flats, smooth gradients (daylight to warm sunset to purple twilight), and clean linework.
4.  **Speech Bubbles:** Speech bubbles and narration boxes must be baked directly into the image files (or overlaid cleanly by the rendering engine). Do not use separate HTML floating elements.

---

## 🎨 Shared Visual Assets

The following pre-made assets must be integrated directly into the final render:

1.  **Chalkboard 1 (Panda 5 Battery):**
    *   **Path:** [s7_chalkboard1.png](file:///d:/Code/vumbua/sessions/storyboards/assets/s7_chalkboard1.png)
    *   **Usage:** Integrated on **Page 11 (Flashback Part 1)** as Professor Kante's board.
2.  **Chalkboard 2 (Declining Amplitude Sync-Ledgers):**
    *   **Path:** [s7_chalkboard2.png](file:///d:/Code/vumbua/sessions/storyboards/assets/s7_chalkboard2.png)
    *   **Usage:** Integrated on **Page 12 (Flashback Part 2)** as Professor Kante's board.
3.  **Zephyr Airship Blueprint:**
    *   **Path:** [s7_zephyr_layout.png](file:///d:/Code/vumbua/sessions/storyboards/assets/s7_zephyr_layout.png)
    *   **Usage:** Integrated on **Page 5 (Zephyr Cutaway)** as the establishing stage.
4.  **Reszo Race Basin Map:**
    *   **Path:** [s7_reso_race_map.png](file:///d:/Code/vumbua/sessions/storyboards/assets/s7_reso_race_map.png)
    *   **Usage:** Guides the visual geometry of **Page 14 (Apex Ring Climax)**.

---

## 👤 Correct Character Prompt Tokens

To ensure character art is consistent and never defaults to "generic fantasy," the downstream agent must replace character names in the generation engine with these exact descriptions:

*   **Loami:** `A rugged, broad-shouldered humanoid male mechanic with short brown hair, a short beard, wearing a brown woolen flat cap with a tiny Italian flag ribbon and a heavy canvas working collar, smudged with dark engine grease.`
*   **Ignatious:** `A young male Islander with literal burning flames for hair forming an orange crown around dark hair, glowing yellow-orange eyes, wearing a dark hooded traveler's cloak, soot-dusted face.`
*   **Iggy:** `A small, clay-and-soil-kin mole-like creature with packed dirt skin, green moss and small plant sprouts growing on his head, wearing oversized round copper goggles and a dark oversized heavy wool trench coat.`
*   **Cade Ashveil:** `A smooth, charismatic young male with deep crimson-tinged skin, wearing fine charcoal silks with gold ember trims and a warm diplomatic smile.`

---

## 📖 The 15-Page Sequence & Pacing

### Page 1: Side Gigs (The Campus Ground)
*   **Visual Content:** Loami knocking on his Block 99 dorm balcony door to wake up his Nordic-build roommate at 8 a.m., followed by Loami meeting Lucky with the custom backpack grog dispensers.
*   **Pre-made Assets:** None (New assets to be generated: `s7_page1.png`).
*   **Dialogue Highlights:**
    *   Loami: *"Rise and shine! It's Reszo race day!"*
    *   Lucky: *"Lucky knows how to do stuff. Why you sound so surprised?"*

### Page 2: Waking Iggy & The Colonnade Crowd
*   **Visual Content:** Ignatious waking up Iggy in Block 12. Iggy popping out of his coat, asking *"Are you mad?"* followed by a transition to the massive crowd flowing through the pillared Colonnade walkway. Pip sitting on Bramble's shoulders, throwing almonds at Iggy.
*   **Pre-made Assets:** None (New assets to be generated: `s7_page2.png`).
*   **Dialogue Highlights:**
    *   Ignatious: *"Hey, Gate. Hey, are you alive?"*
    *   Iggy: *"Are you mad?"*
    *   Pip: *"Hey, Iggy, jump higher! That one was on you!"*

### Page 3: Lawn Meeting & The Balloon
*   **Visual Content:** Loami and Lucky meeting Ignatious and Iggy. Ignatious pulling Loami aside in the courtyard to discuss the corrupted resonator he fixed the night before. Ignatious ties a bright red balloon to Iggy's wrist so they don't lose him; Iggy immediately ties it to a kid with a propeller hat and crawls away.
*   **Pre-made Assets:** None (New assets to be generated: `s7_page3.png`).
*   **Dialogue Highlights:**
    *   Ignatious: *"I helped one of the teams with a last-minute fix... their backup resonator failed because the node wasn't powerful enough."*
    *   Ignatious: *"Iggy, keep this on so I don't lose you... wait, where are you going?!"*

### Page 4: Mooring Mast Con (The Sprint)
*   **Visual Content:** Loami and Ignatious running at full speed along the stone gantry, carrying a heavy wooden grease barrel between them as the Zephyr prepares to untie. Loami lying to the gantry crew (*"Val's special recipe!"*) while Ignatious slips past. DM facepalm cameo in the corner.
*   **Pre-made Assets:** None (New assets to be generated: `s7_page4.png`).
*   **Dialogue Highlights:**
    *   Loami: *"This is a special request from Val himself! Val has a special recipe he likes, and we were late on it!"*
    *   Gantry Crew: *"Wait — what? You can't come on."*

### Page 5: The Sky-Haven Gondola (Splash Page)
*   **Visual Content:** Full architectural cutaway drawing showing Deck 1 (Mahogany Study Rooms), Deck 2 (Dining Salon), and Deck 3 (Observatory Amphitheater).
*   **Pre-made Assets:** Embed [s7_zephyr_layout.png](file:///d:/Code/vumbua/sessions/storyboards/assets/s7_zephyr_layout.png).

### Page 6: Loami's Server Debut & Iggy's Looming Glass
*   **Visual Content:** Left side/panel: Loami behind the cocktail bar, blowing a huge breath of fire over a lighter to excite the sportsbook crowd. Right side/panel: Iggy crawling on all fours across the looming glass magnifying floor, clutching his stomach in motion sickness as the ground below pans and zooms.
*   **Pre-made Assets:** None (New assets to be generated: `s7_page6.png`).
*   **Dialogue Highlights:**
    *   Loami: *"All right, baby. Let's go. It's Reszo day!"*
    *   Iggy: *"GROAN... too close... too fast..."*

### Page 7: Ambassador Cade Ashveil
*   **Visual Content:** Ignatious approaching Cade Ashveil and Ember inside the opulent wood-and-brass Sky-Haven cocktail lounge with large viewing windows, handing them glasses of grog. Cade introducing himself as the new ambassador from Lady Ignis. Cade pointing toward Mizizi elder Angela Galaspora sitting in a green moss-weave robe in a plush armchair.
*   **Pre-made Assets:** None (New assets to be generated: `s7_page7.png`).
*   **Dialogue Highlights:**
    *   Cade: *"Lady Ignis wants us established as a long-term Harmony faction... the bet she has is that if we can help the Mizizi, it will help us."*

### Page 8: Node Grading & Thematic Shift
*   **Visual Content:** Cade pointing down at the canyon below, explaining node grading (e.g. Nstyl's silence sand spires). Ignatious looking out over the sunset-lit canyon, experiencing an internal realization that the future of the Ash-Bloods lies with Harmony, not isolation.
*   **Pre-made Assets:** None (New assets to be generated: `s7_page8.png`).
*   **Dialogue Highlights:**
    *   Cade: *"Our fire influences our culture just as much as that sand. Why is it not having the same impact?"*
    *   Ignatious: *"I came here thinking isolation was something I'd push for. But seeing everything Harmony has to offer... I think the future of the Ash-Bloods is with Harmony."*

### Page 9: Engine Room Break-in
*   **Visual Content:** Ignatious and Loami convincing Val Jr. to take them to the core. Val Junior typing the passcode on the steel door. The door sliding open to reveal the humming, blue-white light of the engine room with stacked Panda 5 cells.
*   **Pre-made Assets:** None (New assets to be generated: `s7_page9.png`).
*   **Dialogue Highlights:**
    *   Val: *"Yeah, this is where the magic happens. Don't literally throw a wrench into it. We are literally flying."*

### Page 10: Night of Sparks & Grog Siphon
*   **Visual Content:** Val Jr. pointing at the battery packs, explaining the wireless electrical current. Showing the dark red Umbra crystals that act as resistor caps to prevent another overload (referencing the Night of Sparks catastrophe). Loami siphoning grog with a copper pipe and feeding it to Iggy, who is hiding behind the barrels.
*   **Pre-made Assets:** None (New assets to be generated: `s7_page10.png`).
*   **Dialogue Highlights:**
    *   Val: *"Ever since the Night of Sparks, we've had Umbra crystals. They act as resistors against the flow, keeping the surge below the threshold."*
    *   Iggy: *"You know... *hic*... I learned a lot about this stuff..."*

### Page 11: Flashback: Kante's Accidental Lesson (Part 1 — The Battery)
*   **Visual Content:** Flashback to Professor Kante's dark stone workshop. Kante pointing his wooden walking cane to Chalkboard 1 (`s7_chalkboard1.png`). Iggy sitting below, sketching in his notebook.
*   **Pre-made Assets:** Overlay Kante's chalkboard [s7_chalkboard1.png](file:///d:/Code/vumbua/sessions/storyboards/assets/s7_chalkboard1.png) on the wall.
*   **Dialogue Highlights:**
    *   Kante: *"The Panda 5 is our standard battery. Stored in Vox-hex, it lasts three days before running dry. But it only works when the network stays stable!"*

### Page 12: Flashback: Kante's Accidental Lesson (Part 2 — The Declining Aether)
*   **Visual Content:** Kante gesturing to Chalkboard 2 (`s7_chalkboard2.png`), showing the declining global amplitude graph and the scrapped APEX line. Kante placing a raw red Umbra crystal in Iggy's hand, warning him about connection vs. extraction.
*   **Pre-made Assets:** Overlay Kante's chalkboard [s7_chalkboard2.png](file:///d:/Code/vumbua/sessions/storyboards/assets/s7_chalkboard2.png) on the wall.
*   **Dialogue Highlights:**
    *   Kante: *"The APEX line is scrapped! If the Global Amplitude drops under the surge-line, our next-gen resonators will fail. Take this crystal—remember, integration is connection, not extraction!"*

### Page 13: Snap Back & Apron Blanket
*   **Visual Content:** Snap back to the Zephyr engine room. Drunk Iggy standing on a crate, shouting Kante's equations. Val Jr. looking terrified with his mouth wide open. Iggy staggers back to the storage room, curls up next to the barrel, and Loami tucks him in by covering his shell with his white Sterling apron.
*   **Pre-made Assets:** None (New assets to be generated: `s7_page13.png`).
*   **Dialogue Highlights:**
    *   Iggy: *"Next line of batteries has massive fluctuations because the amplitude didn't rise! Kante said so!"*
    *   Val: *"Shh! Keep your voice down! If this leaks, the Castellans are toast!"*

### Page 14: The Reszo Race Climax
*   **Visual Content:** Panoramic view of the half-mile-wide canyon of the Apex Ring. The stands are carved into basalt walls, and a train runs along the top rim. Pudge on his Griffin strikes the central spire, unleashing blue and orange fireworks. The Shatter Stamper lies stalled halfway across the canyon floor.
*   **Pre-made Assets:** Guided by [s7_reso_race_map.png](file:///d:/Code/vumbua/sessions/planning/s7/reso-race-map.png).
*   **Dialogue Highlights:**
    *   Pip: *"I don't really like the guy riding it, but his Griffin? Cool. I approve."*

### Page 15: Bartender Dispute & Walk Home
*   **Visual Content:** Loami and Ignatious asking the bartender for their coin, only to be told they were just considered "good party guests" and got exposure. The group walking back to the dorm blocks in the purple twilight, carrying heavy textbooks, ready to study for their exam.
*   **Pre-made Assets:** None (New assets to be generated: `s7_page15.png`).
*   **Dialogue Highlights:**
    *   Ignatious: *"I know this is a bad time, but you owe us a bushel of coins."*
    *   Bartender: *"I didn't order any drinks. I thought y'all were just good party guests!"*
    *   Loami: *"Next time's for pay, though."*
