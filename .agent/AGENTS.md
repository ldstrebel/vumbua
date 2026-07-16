# Vumbua Comic Book Generation Guidelines

Always follow these rules when writing comic book storyboards or generating page images for Vumbua:

---

## 1. Page Budget & Narrative Pacing

*   **Never truncate the page budget:** Scale pages to the number of major scenes in the clean transcript — typically 3–5 pages per major scene, 10–20 pages per full session. Do not compress.
*   **Environmental Transitions:** Always include explicit gutter transition descriptions (`#### 🖤 Gutter Transition:`) between panels to guide spatial and temporal shifts.
*   **Flashback gutters:** Use dark gray (`#333`) gutter color for flashback sequences, black (`#000`) for present-day. Specify this explicitly in every panel prompt that shifts time.

---

## 2. Visual Style & Prompts

*   **Style tokens:** Use exactly this string as the opening of every image prompt:
    `Detailed 2D graphic novel style, clean expressive manga-style linework, crisp black ink outlines, cel-shaded color flats, cinematic volumetric lighting`
*   **No artist names:** Do not use "Carey Pietsch" or any other specific artist name.
*   **No HTML overlays:** All text, speech bubbles, narration boxes, and sound effects must be baked directly into the generated page art in the prompt. Do not use HTML/CSS overlays.
*   **No name leaks:** Never pass character names (e.g. "Loami", "Ignatious", "Iggy", "Britt", "Aggie") directly to the image generator. Always replace names with their exact physical description tokens as pulled from their profile files in that same turn.

---

## 3. MANDATORY Pre-Generation Gate (DO NOT SKIP)

**Before writing any panel prompt or calling `generate_image`, the following steps are REQUIRED in the same turn:**

1.  **Read the clean transcript.** Call `view_file` on `sessions/transcripts/clean/sN-clean.md` for the session being storyboarded. Do not rely on memory or session summaries.
2.  **Read every character profile** for characters who appear in the scene. Call `view_file` on each relevant file:
    - `characters/player-characters/loami.md`
    - `characters/player-characters/iggy.md`
    - `characters/player-characters/ignatious.md`
    - `characters/player-characters/aggie.md`
    - `characters/player-characters/britt.md`
    - Any NPC file in `characters/npcs/` for NPCs in the scene
3.  **Extract the physical description token** for each character directly from the file text in that same turn. Do not paraphrase or reconstruct from memory. Copy the relevant description lines verbatim into the prompt.
4.  **Check for reference images.** Before adding any file to `ImagePaths`, call `list_dir` on `sessions/storyboards/assets/` to confirm the file actually exists. Never assume a reference file exists.

> **Why this matters:** The model can inspect generated images using the `view_file` tool on the PNG paths to visually audit them inline, but it must never assume they are correct. The only protection against character drift is an accurate description pulled from ground-truth files in the same turn as generation, combined with a visual post-generation audit.

---

## 4. Visual Auditing and Human Approval Gate

**The model must visually audit all generated images.** Self-grading by merely reading back prompts is strictly banned. Instead, the model must call `view_file` on the generated PNG assets to visually inspect character features (e.g. Iggy's trench coat and moss sprouts, Loami's Cap and grease smudges) and panel structures before presenting them.

Rules:

*   **Pre-Screening Audit:** For every batch of images generated, the model must call `view_file` on the PNGs, perform a visual consistency check against the character profiles, and document any findings (such as missing sprouts or incorrect layout).
*   **Human Approval is the Final Gate:** After performing the visual audit, **stop and show the images and audit results to the user**. Do not proceed to the next page until the user explicitly confirms the characters look correct.
*   If the user (or the visual audit) identifies a character error, treat it as a **hard fail**. Rewrite the panel prompt from scratch using the ground-truth file text. Do not patch — rewrite.
*   **Do not run autonomous multi-page generation loops.** Generate 2–3 pages, visually audit, pause, show, confirm, then continue.

---

## 5. Zero-Tolerance for Hallucinated Features

Known character failure modes. Any page containing one of these is an automatic hard fail — rewrite the prompt and regenerate:

| Character | Common AI Failure | Correct Description |
|---|---|---|
| **Loami** | Drawn as a turquoise octopus creature | Rugged broad-shouldered humanoid male, short brown hair, short beard, brown woolen flat cap with tiny Italian flag ribbon, heavy canvas working collar, smudged with dark engine grease and soot |
| **Iggy** | Drawn as a turtle with a stone shell | Small clay-and-soil-kin humanoid-shaped creature of packed dirt and clay, packed dirt skin, green moss and small plant sprouts on head, oversized round copper goggles, dark oversized heavy wool trench coat. **NO SHELL.** |
| **Ignatious** | Drawn with generic red spiky hair or school uniform | Young male with literal burning flames for hair forming an orange crown around dark hair, glowing yellow-orange eyes, dark hooded traveler's cloak |
| **"Octoumba"** | Misread as Loami's species | Octoumba is a geographical region/continent. Loami is humanoid. |

---

## 6. Location Consistency

Check backgrounds against established concept art or blueprints before writing any panel prompt. Do not accept generic AI backgrounds for named locations:

*   **Zephyr interior bar/lounge:** Wood-paneled walls, polished brass fixtures, leather seating, warm amber lighting from gas lamps. NOT a generic balcony or outdoor terrace.
*   **Apex Ring:** A half-mile-wide basalt canyon carved into natural rock. Grandstands cut directly into canyon walls. NOT a floating stadium or flat arena.
*   **The Colonnade:** Pillared marble hallway leading to airship berths. Crisp white stone with brass fixtures.

---

## 7. Dialogue Locking (Zero-Tolerance for Hallucinated Text)

**All speech bubbles and narration boxes baked into panel art must come verbatim from the clean transcript.** The image generator will invent plausible-sounding dialogue if not constrained — including fake character names, invented confrontations, and dramatic fabrications that never happened.

Rules:

*   **No improvised dialogue.** Every line in a speech bubble must be an exact quote from `sessions/transcripts/clean/sN-clean.md`. If a line is paraphrased or not present in the transcript, it is a hard fail.
*   **No character names in speech bubbles.** The image generator invents fantasy names (e.g. "Kip", "Iñigo", "Alistair") to fill dialogue if character identities are ambiguous. Never include character names inside speech bubbles — the generator will hallucinate them.
*   **No invented characters.** If a name appears in the generated image that does not appear in any character file or the clean transcript (e.g. "Alistair"), that page is an automatic hard fail. Rewrite the prompt from scratch.
*   **No escalated drama.** Do not describe scene dynamics as "confrontation", "argument", or "angry" if the transcript tone is casual or amicable. The generator will amplify the described tone — a "dispute" becomes a brawl, a "chat" becomes a standoff.
*   **Narration boxes must be present.** Every panel must include at least one narration box paraphrasing the GM's narration from the clean transcript. Dialogue alone is insufficient to carry story continuity across panels.
