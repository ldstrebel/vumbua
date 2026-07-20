# Vumbua Comic Book Generation Guidelines

Always follow these rules when writing comic book storyboards or generating page images for Vumbua:

---

## 1. Page Budget, Panel Layout & Presentation

*   **Never truncate the page budget:** Scale pages to the number of major scenes in the clean transcript — typically 3–5 pages per major scene, 10–20 pages per full session. Do not compress.
*   **Dynamic Panel Layouts & Overlay Panels:** Vary panel layouts dynamically across pages. Do not rely exclusively on standard grids. Mix single splash panels, vertical/horizontal splits, and **full-page splash backgrounds with stylized inset panels overlayed on top** for dramatic action or focus effects.
*   **Environmental Transitions:** Always include explicit gutter transition descriptions (`#### 🖤 Gutter Transition:`) between panels to guide spatial and temporal shifts.
*   **Global Black Gutters:** All session storyboards must use a consistent black background and black gutter design (`Black gutters.`). Flashback sequences use dark gray (`#333`) gutter color. Specify this explicitly in every panel prompt.

---

## 2. Visual Style & Prompts

*   **Style tokens:** Use exactly this string as the opening of every image prompt:
    `Detailed 2D graphic novel style, clean expressive manga-style linework, crisp black ink outlines, cel-shaded color flats, cinematic volumetric lighting`
*   **No artist names:** Do not use "Carey Pietsch" or any other specific artist name.
*   **No HTML overlays:** All text, speech bubbles, narration boxes, and sound effects must be baked directly into the generated page art in the prompt. Do not use HTML/CSS overlays.
*   **Mandatory Explicit Skin Color & Full Physical Tokens:** Every character description token MUST specify a complete physical description including explicit skin tone/color (e.g., Caucasian/fair skin, dark brown skin, olivaceous green skin, light grey reptilian skin, packed-dirt clay brown skin, white fur). Never leave skin tone or physical ancestry ambiguous, or the image generator will drift between panels.
*   **No name leaks in visual descriptors:** Never use character names as visual descriptors for the image generator (e.g., "Loami stands in the doorway"). Always replace names with their exact physical description tokens as pulled from their profile files in that same turn. **EXCEPTION: Quoted text inside speech bubbles and narration boxes is PRINTED TEXT, not a visual descriptor. Character names inside quoted dialogue and narration MUST be preserved verbatim from the clean transcript.** The image generator renders quoted text as printed characters — it does not use names inside quotes to influence visual rendering of the character.


---

## 3. MANDATORY Pre-Generation & Planning Gate (DO NOT SKIP)

**Before writing any panel prompt, generating implementation plans, or calling `generate_image`, the following steps are REQUIRED:**

1.  **Read the clean transcript.** Call `view_file` on `sessions/transcripts/clean/sN-clean.md` for the session being storyboarded. Do not rely on memory or session summaries.
2.  **Read every character profile and location file** for entities in the scene. Call `view_file` on each relevant file.
3.  **Extract character and location tokens verbatim.** Copy the physical description lines directly into both the `implementation_plan.md` and the storyboard file.
4.  **Include Tokens in `implementation_plan.md` & STOP for Approval:** When planning a storyboard task, include the full proposed `## 👤 Character Reference Prompt Tokens` and `## 🏛️ Location Reference Prompt Tokens` sections in `implementation_plan.md`. **Stop execution and wait for explicit user approval of the tokens before proceeding to prompt writing or image generation.** Do not auto-approve or bypass this gate.
5.  **Check for reference images.** Call `list_dir` on `sessions/storyboards/assets/` to confirm existing assets.


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

## 6. Location & World-Tech Consistency

Every storyboard MUST include a **`## 🏛️ Location Reference Prompt Tokens`** section at the top alongside character tokens. Do not accept generic AI backgrounds or modern tech tropes for named locations:

*   **Mandatory Location Tokens in Every Prompt:** Every prompt set in a named location must explicitly inject the full location reference token. Never rely on generic terms like "at the harbor" or "in the arena."
*   **Campus Harbor:** Low-profile grassy harbor islands with stone features connected by elegant stone walkways and bridges across a 1,700-foot-deep dark turquoise basin. The permanently moored Deep-Hull (a colossal Titanic-like iron steamship with brass fittings and glass canopies) is anchored in the background bay.
*   **Apex Arena:** A colossal half-mile-wide basalt canyon carved into natural cliff walls. Steep, terraced stone grandstands wrap around the canyon. Rows of heavy wooden desks are mounted directly onto the stone row below.
*   **Exam Slates (World Tech):** Exam slates are heavy copper-lined stone slabs with self-writing glowing text across their surfaces, weighted by a glowing copper-and-crystal paperweight. Never draw modern plastic/glass digital tablets.
*   **Zephyr interior bar/lounge:** Wood-paneled walls, polished brass fixtures, leather seating, warm amber lighting from gas lamps. NOT a generic balcony or outdoor terrace.
*   **The Colonnade:** Pillared marble hallway leading to airship berths. Crisp white stone with brass fixtures.

---

## 7. Dialogue Locking (Zero-Tolerance for Hallucinated Text)

**All speech bubbles and narration boxes baked into panel art must come verbatim from the clean transcript.** The image generator will invent plausible-sounding dialogue if not constrained — including fake character names, invented confrontations, and dramatic fabrications that never happened.

Rules:

*   **No improvised dialogue.** Every line in a speech bubble must be an exact quote from `sessions/transcripts/clean/sN-clean.md`. If a line is paraphrased or not present in the transcript, it is a hard fail.
*   **Names ARE allowed inside quoted text.** The "no name leaks" rule (Section 2) applies to visual descriptors only. Speech bubble text like `"Aggie, where were you?"` must retain the name `Aggie` exactly as spoken in the transcript. The image generator renders quoted text as printed characters — it does not use names inside quotes to influence visual rendering. However, the image generator may INVENT fantasy names (e.g. "Kip", "Iñigo", "Alistair") if character identities are left ambiguous in the visual descriptor portion of the prompt. Always attribute speech bubbles to a character by physical description, not by name.
*   **No invented characters.** If a name appears in the generated image that does not appear in any character file or the clean transcript (e.g. "Alistair"), that page is an automatic hard fail. Rewrite the prompt from scratch.
*   **No escalated drama.** Do not describe scene dynamics as "confrontation", "argument", or "angry" if the transcript tone is casual or amicable. The generator will amplify the described tone — a "dispute" becomes a brawl, a "chat" becomes a standoff.
*   **Narration boxes must be present.** Every panel must include at least one narration box paraphrasing the GM's narration from the clean transcript. Dialogue alone is insufficient to carry story continuity across panels.

---

## 8. Standalone Prompt Completeness

Every image prompt must be **fully self-contained.** The image generator has zero memory between calls. Rules:

*   **Full visual token required:** Every character visible in the panel must have their FULL visual description token repeated in that specific prompt. Do not use abbreviated references like "the nurse" or "the mechanic" — always include the complete physical description token from the character profile.
*   **Explicit Skin Color/Tone Required:** Every visual token MUST explicitly specify skin tone/color (e.g., Caucasian/fair skin, dark brown skin, olivaceous green skin, light grey reptilian skin, earthy clay skin, white fur) to prevent skin tone drift between panels.
*   **Speech bubble attribution by description:** Every speech bubble must include the full quoted text AND specify which character (by physical description, not name) it points from.

*   **No cross-page assumptions:** Never assume the generator will "remember" a character from a previous page. Each prompt is an island.
*   **Prompt validation before generation:** Before calling `generate_image`, verify each prompt against these rules. Use the `sessions/storyboards/scripts/validate_prompts.py` script if available.
