---
description: Generate image and video prompts for animating a Vumbua scene
---

# Storyboard & Animation Workflow (Slash Command: /storyboard)

Use this workflow when the user requests a storyboard prompt, a scene visualization, or an animation setup. 
The goal is to translate a campaign scene into a strict 2-part prompt system:
1. An **Image Prompt** (to generate the base storyboard frame / aesthetic reference).
2. A **Video Animation Prompt** (to feed into an AI video generator alongside that image).

---

## 1. The Vumbua Aesthetic (CRITICAL)

When writing image prompts, you must override default "fantasy" biases. The style of Vumbua is **NOT** dark, grim, medieval, or muddy. It is a bright, optimistic, and highly detailed fusion of eras. 

**Always enforce these core visual pillars:**
- **Lighting & Tone:** Bright, vibrant daylight, high contrast, cinematic volumetric lighting. Clear skies with dramatic clouds.
- **Architecture:** "Oxford meets Steampunk, built into the Wild." Pristine, bright white marble facades, grandstands, and sweeping arches are **carved directly into or bolted onto massive, rugged natural cliff faces and jagged mountains**. There is a sharp, beautiful contrast between the manicured academic stone and the raw, weathered textures of nature.
- **Scale & Composition:** Sweeping wide shots, massive scale, deep depth of field. 
- **Atmosphere:** Clean, manicured green gardens and white marble structures integrated with heavy industrial brass machinery, all nestled within a vast, unyielding natural landscape. A world of grounded exploration. Students in crisp, uniform attire.
- **Technology:** Gaslamp fantasy. Steam, brass, umber crystals, and gears. Do not use generic "glowing magical auras" unless specifically requested by the node physics.

## 2. Step 1: The 3x3 Narrative Key-Frame Grid Prompt

You must instruct the image generator to create a **single image containing a 3x3 grid**. The 9 panels must represent **sequential key-frames of a narrative scene**. The video AI will fill in the gaps between these major key moments. 

Write an excruciatingly detailed, expert-level image prompt optimized for tools like Midjourney v6/Niji 6. 

**Rules for the Image Prompt:**
- **The Anime/Ghibli Style:** We are abandoning "video gamey" 3D render styles. The style must explicitly invoke high-budget anime movies (Studio Ghibli, Makoto Shinkai). Words to use: *vibrant painterly environments, lush cel-shaded anime style, incredibly detailed 2D animation frame, breathtaking anime cinematography.*
- **The Vumbua Baseline (Anti-Tropes & Aesthetics):** Defend against generic biases across ALL eras! 
  - **No Generic Steampunk:** NO standard trains, literal gears, clock-faces glued to pipes, or top hats. 
  - **Transit & Spectator Vehicles:** Describe spectator vehicles as *ornate, steam-pulled observation cars with vast glass windows and outward-facing bleacher seating, reminiscent of Oxford rowing races*. **CRITICAL ARCHITECTURE:** The tracks run elevated *behind* the grandstands, so the train looks over the tops of the audience's heads, providing an unobstructed view of the basin and allowing easy hop-on/hop-off access. It NEVER runs between the crowd and the view.
  - **The Starting Grid (Geography):** If generating the basin starting line, the ground is exactly half solid earth and half turquoise water so boats and heavy dirt crawlers can idle side-by-side. The colossal, four-legged Walker-Core crane is set *far back* behind the line. NEVER generate a purely aquatic regatta and NEVER generate a mass crane-drop.
  - **Ships & Airships (The Exception):** If there is one area that *does* lean heavily into high-fantasy steampunk, it is the ships and racing crafts! Describe them as *Treasure Planet-style solar galleons or heavy brass ironclads held aloft by massive, silk-textured golden dirigible balloons*. They should feature ornate golden solar sails and thick brass cabling connecting the hull to the shimmering balloon. Do NOT just ask for "hover crafts" or it will draw boring sailboats. Avoid generic blimps.
  - **No Sci-Fi / Modern:** Explicitly describe engines as *vented brass steam engines glowing warmly with crystal resonance energy, NO jet engines, NO rockets*.
  - **No Text/Subtitles:** Anime styles often add Japanese subtitles. Explicitly ban text.
- **Setting Consistency (Object Permanence):** Midjourney forgets the background by the end of the grid. In panels 7, 8, and 9, you MUST explicitly re-describe the specific background biome established in earlier panels.
- **CRITICAL: "Thick" Panel Descriptions (NO SUMMARIES):** You must never regress into writing "thin" summaries. If you write "Top left: emerging into the blinding sunlight," the AI will hallucinate. You must write **THICK** micro-descriptions for *every single panel*, detailing exact materials, lighting, background elements, and specific character clothing. Every panel description must feel overwhelmingly dense (e.g., "Top Left: Dense crowds of students wearing crisp, tailored blue and gold uniforms walking casually through pristine, manicured white marble gardens with blooming crimson flora under volumetric sunlight.")

**Structure the prompt strictly like this (Enforcing THICK Descriptions):**
```text
A 3x3 grid of sequential narrative anime key-frames showing [Scene Narrative]. Top left is [THICK description: lighting, material, specific clothing, background architecture of Moment 1], top middle is [THICK description: lighting, material, specific action, foreground elements of Moment 2...], top right is [THICK description: lighting, material, camera angle, specific weather of Moment 3...], middle left is [THICK description...], middle is [THICK description...], middle right is [THICK description...], bottom left is [THICK description...], bottom middle is [THICK description...], bottom right is [THICK description...]. [Vumbua Academy Aesthetic: pristine Oxford-style white stone academia blending flawlessly with elegant, massive brass high-fantasy technology]. [Anime Style: Studio Ghibli meets Makoto Shinkai, breathtaking vibrant 2D anime cinematography, lush painterly environments, beautifully stylized cel-shaded animation, crisp linework]. --no text, typography, lettering, subtitles, watermarks, generic steampunk, clock faces, modern vehicles, modern trains, bullet trains, jet engines, rockets, sci-fi thrusters, top hats, dirt arenas
```

---

## 3. Step 2: The Video Animation Prompts

## 3. Step 2: The Video Animation Prompts

The reason video models often return jagged, graceless cuts between frames is because the prompt lacks transitional "meat". If you just tell the AI to "transition from the gardens to the arches," it will slightly shift the frame and hard-cut. 

You must design the camera path in tandem with the storyboard. In the Stitching Prompt, you must explicitly describe **HOW** the camera physically moves from the composition of one panel into the next. Use **structural wipes, match-cuts, or extreme spatial camera sweeps** to bridge the gaps. 

**CRITICAL: The "Double Tap" Rule**
Video AI suffers from extreme amnesia. When transitioning to a new panel, you must **"double tap"** the key design elements (scale, material, aesthetic) to ensure it doesn't drift. Do not just say "reveal the stadium"; explicitly say "reveal the *colossal, blinding white marble* stadium."

You will generate **TWO separate video prompts**:
1. **The Stitching Prompt (Image-to-Video):** Uses the 3x3 grid. Explicitly describes the physical camera sweeps, foreground wipes, and double-taps the key aesthetic keywords for every panel.
2. **The Direct One-Shot Prompt (Text-to-Video):** Designed to generate the exact same scene entirely from text, skipping the storyboard grid.

**Structure the verbose Stitching Prompt like this (Focusing on the "Meat" & Double Taps):**
```text
A seamless, continuous cinematic sequence. We begin on Panel 1, tracking left-to-right over the pristine, manicured gardens and blue uniforms. The camera then pushes rapidly forward, using the passing back of a student's uniform (Panel 1) to completely wipe the frame, seamlessly revealing the massive, sweeping brass structural arches of high-fantasy resonance tech (Panel 2). The camera tilts sharply up the brass supports (Panel 2) until the sun flares the lens, match-cutting brilliantly into the colossal, blindingly bright white marble stadium (Panel 3). We dolly backward from the stadium edge (Panel 3), dropping over the rim into a breathtaking aerial dive over the massive, turquoise river canyon basin (Panel 4). [Continue explicitly describing the foreground wipes, flares, or camera sweeps that bridge every single panel, ensuring you "double tap" the visual scale and aesthetic for each]. The AI generates perfectly fluid, high-budget 2D anime motion between these key moments with no graceless cuts, maintaining breathtaking Ghibli lighting throughout.
```

**Structure the verbose One-Shot (Text-to-Video) Prompt like this:**
```text
A seamless, continuous continuous tracking shot in a breathtaking Studio Ghibli/Makoto Shinkai anime style. The camera begins by [detailed camera movement through Phase 1]. It then flows seamlessly into [continuous camera movement through Phase 2], sweeping past [details]. The sequence culminates as the camera [final cinematic move resolving on Phase 3/Climax]. [Insert Vumbua Visual Rules and Anti-Tropes here].
```

---

## 4. Output Format

When executing this workflow, output the results to the user in this exact markdown format:

### 🖼️ 3x3 Narrative Key-Frame Grid Prompt (Midjourney --niji 6)
```text
[Your highly detailed, Anime-styled 3x3 Sequential Grid Image Prompt Here]
```

### 🎬 Image-to-Video Sequence Stitching Prompt (Runway/Luma Gen-3)
```text
[Your verbose, camera-directed stitching Video Prompt Here]
```

### 🎥 Direct Text-to-Video Prompt (Skipping Grid)
```text
[Your highly detailed, continuous one-shot Video Prompt Here]
```  
