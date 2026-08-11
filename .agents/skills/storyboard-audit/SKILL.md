---
name: storyboard-audit
description: Audit generated storyboard images against visual profiles, log feedback, and perform root-cause analysis on failures.
---

# Storyboard Quality Auditing & Feedback Protocol

Use this skill when generating comic book pages, reviewing visual storyboard assets, or resolving user feedback regarding character design, visual errors, or scene continuity issues.

> [!CAUTION]
> **ZERO SELF-BIAS RULE:** Prompts are requests to an unpredictable image generator. Never assume an image followed a prompt. Self-grading by assuming prompt compliance or rubber-stamping "PASS" checkmarks without exhaustive verification is strictly banned.

---

## 🤖 Adversarial Multi-Subagent Pipeline Architecture

To completely eliminate confirmation bias ("self-bias") during graphic novel creation, execution MUST follow a 3-tier adversarial subagent pipeline:

```
                  ┌─────────────────────────────────────┐
                  │        1. PROMPT ARCHITECT          │
                  │   Reads ground-truth profiles/rules │
                  │   Generates sanitized prompts       │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
                  ┌─────────────────────────────────────┐
                  │         2. ARTIST RENDERER          │
                  │   Calls generate_image tool         │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
                  ┌─────────────────────────────────────┐
                  │      3. ADVERSARIAL INSPECTOR       │
                  │   Blinded to prompt intent!         │
                  │   Calls view_file on raw PNG asset  │
                  │   Audits against canonical profile  │
                  │   Emits PASS or HARD FAIL report    │
                  └──────────────────┬──────────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    ▼                                 ▼
               [ HARD FAIL ]                       [ PASS ]
             Re-queue to Architect             Present to User
             with Error Diff                   for Final Approval
```

### Roles & Boundaries:
1. **Prompt Architect (Agent 1):** Takes clean transcripts & character profile files, extracts exact physical description tokens, strips all page numbers/headers, and formats clean visual prompts.
2. **Artist Renderer (Agent 2):** Calls `generate_image` with sanitized prompts and saves assets as `sX_pageY.png`.
3. **Adversarial Inspector (Agent 3 - BLINDED):** Reads ONLY the canonical character/location specs and calls `view_file` on the PNG. It has NO access to the prompt text so it cannot form self-bias. Its sole objective is to **find visual defects** (e.g. Iggy having a shell, page numbers on borders, floating umbrellas, wrong skin tone). If any defect is found → **HARD FAIL** with rewrite diff.

---


## 🛡️ Visual Continuity Protocol

1. **The Anti-Text Lockdown:** Strictly prohibit any text, numbers, page markers, titles, or corner captions from appearing inside the art or gutters. The visual space must remain 100% clean. Never include strings like `"Page 18"` or `"pg 18"` in the prompt sent to the image generator. Always include negative constraints: `--no text, typography, page numbers, page titles, corner captions, watermarks`.
2. **The Silhouette Check:**
   - **Britt:** Always verify she has her turtle shell ONLY on her back. (Zero backpacks allowed).
   - **Iggy:** Always verify he has NO SHELL. (Clay body + coat + water goggles only).
   - **Aggie:** Integrated Amanita mushroom carapace shell on her back ONLY. (No floating umbrella hats).
   - **Loami:** Mud/dirt accents on cap and gear. Right metallic shoulder pauldron, green fist emblem.
   - **Mwaza-Kasa:** Non-humanoid quadrupedal spirit tortoise walking on four legs with a petrified bark shell. (No human faces, no white hair, no goggles).
   - **Dean Isolde Vane:** Always a furry hamster/yordle-like female (dwarf-scale, white fur, bushy eyebrows, academic gear).
3. **The Era Anchor:** Every mechanical or human outfit must stay Oxfordian/Victorian/steampunk fantasy. No modern firefighter gear (no yellow plastic) and no generic medieval armor (no knights). Use canvas, brass, petrified wood, and dark wool.
4. **The Arena / Canopy Rule:** Never attempt to 'wrap' stadium walls or canopy foliage. Show one high-altitude cliff-top or branch slice with sheer vertical drops to the basin below.
5. **The Naming Hard-Rule:** Every image generation MUST be saved using the `sX_pageY` format (e.g. `s11_pg01`, `s11_pg18`) immediately after creation to maintain library organization.
6. **Dialogue Preservation:** Pass the user's dialogue through verbatim from the clean transcript. Do not summarize, 'improve', or edit the tone of speech bubbles.

---

## 🎨 Art Style Guide

* **Prompt Style Core:** `Detailed 2D graphic novel style, clean expressive manga-style linework, crisp black ink outlines, cel-shaded color flats, cinematic volumetric lighting`
* **Negatives / Bans:** `--no 3D render, realism, hyper-detailed, muddy colors, dark grit, muted tones, page numbers, page titles, corner captions, border labels, watermarks, margin text`

---

## 👤 Canonical Character Reference Tokens

Character names must **NEVER** appear in image generator prompts. Use these exact physical description tokens only:

1. **Britt (PC):** `A slender turtle-mushroom hybrid female with olivaceous, moss-green skin and prominent, pointed elven ears. Wild, long dreadlocks made of living green roots and thick vines cascade past her waist. She wears a simple, sleeveless charcoal grey tunic. She has a large turtle shell, lumpy, and leaf-strewn securely attached to her back.`
2. **Iggy (PC):** `A small, short clay-and-soil-kin humanoid creature with cracked, dry-earth skin texture and tiny green sprouts growing from the top of his head. He wears massive, oversized round brass goggles that are visibly half-filled with sloshing water. His diminutive body is wrapped in a heavy, dark grey wool coat/tunic. STRICTLY NO TURTLE SHELL, NO HUMAN SKIN.`
3. **Aggie (PC):** `A turtle-mushroom hybrid female with light grey, textured, reptilian skin and expressive, wide green eyes. She has neat, shoulder-length white hair adorned with a delicate green leaf crown. She wears a simple, sleeveless white linen dress featuring intricate green vine embroidery around the waist. Her back shell is a massive, vibrant red-and-white spotted amanita muscaria mushroom cap integrated onto her back. STRICTLY NO FLOATING UMBRELLA HATS.`
4. **Loami (PC):** `A rugged, heavily built Caucasian male with a wide, confident grin, one green eye and one blue, short brown hair, and a trimmed beard. His face, hat, and gear are prominently splattered with dark mud and dirt accents. He wears a brown flat cap featuring a distinct vertical red, white, and green striped ribbon on the side. His attire consists of a rugged working shirt under a heavy leather strap layout, a thick chain necklace, and a bulky, layered metallic mechanical shoulder pauldron on his right side. A round green emblem featuring a fist icon is pinned to his chest strap.`
5. **Ignatious (PC):** `A 17-year-old Ember Islander male with dark hair featuring flaming orange eyebrows and a subtle active fire crown through his hair, glowing yellow-orange eyes, soot-dusted dark hooded traveler's cloak over a dark leather vest, ember-trimmed cuffs, soot-dusted trousers. STRICTLY NO METAL TIARAS, NO DEMON FACES.`
6. **Pip (NPC):** `A hyperactive 12-year-old female gnome cadet with fair Caucasian skin, expressive wide hazel eyes, messy short reddish-copper pixie hair, wearing a brown canvas cadet jacket with golden brass buttons over a light grey shirt, brown trousers, carrying a greasy canvas sack spilling golden biscuit crumbs. STRICTLY NO BEARDS, NO MALE FEATURES.`
7. **Mwaza-Kasa (NPC):** `A non-humanoid quadrupedal spirit tortoise about 3–4 feet wide walking on four reptile legs, dark petrified bark carapace shell with subtle glowing blue lichen patterns, pale grey reptilian neck and beak snout, glassy ancient dark eyes looking with a sad, embarrassed gaze. STRICTLY NO HUMANOID FEMALE FEATURES, NO WHITE HAIR, NO CLOTHES, NO GOGGLES.`
8. **Remmy (NPC):** `Halfling female nurse, kind features, short wavy brown hair under a small, tilted red cloth hat, wearing a clean white linen apron over a dark grey tunic.`
9. **Bjorn (NPC):** `Tall, lean-muscled young male of Nordic build, with short blonde hair and simple candidate garments.`
10. **Lyra Castellan (NPC):** `Strikingly beautiful young dark-skinned female with severe, dark hair tied in a tight bun, wearing a high-collared uniform.`
11. **Ludo Castellan (NPC):** `Dark-skinned young male with similar facial features as Lyra, dark hair, wearing a slightly disheveled candidate uniform.`
12. **Dean Isolde Vane (NPC):** `Small furred hamster-like creature with infectious energy, a tiny frame, white fur, bushy eyebrows, wearing academic gear.`

---

## 📋 Step-by-Step Audit Workflow


### Step 0: Prompt Validation (Pre-Generation Gate)

Before calling `generate_image` or writing any panel prompt, validate each prompt against these rules:

1. **Token Completeness:** Every character visible in the panel has their FULL visual description token from the character profile — not an abbreviation like "the nurse" or "the mechanic." The image generator has zero memory between calls; each prompt must be self-contained.
2. **Location Token Completeness:** Every prompt set in a named location must explicitly inject the full location token (e.g., stone walkways, grassy islands, and Deep-Hull for Harbor; mounted wooden desks in basalt canyon for Apex Arena; 50ft high petrified tree boughs wedged between ancient trunks for Canopy). Never rely on generic location names.
3. **Quoted Text Integrity:** All text inside `"..."` (speech bubbles and narration boxes) matches the clean transcript verbatim, **including proper nouns and character names.**
4. **No Name Leaks in Descriptors:** Character names appear ONLY inside quoted speech/narration text. The visual descriptor portions of the prompt must use physical description tokens, never names.
5. **Mandatory Speaker Presence & Bubble Attribution:** If a character speaks in a panel, the prompt **MUST explicitly require their physical presence in that panel frame** and mandate: `"Speech bubble tail emerging directly from the mouth of [Character description]..."`.
6. **Single-Bubble & No-Duplicate Constraints:** Include explicit negative text constraints: `"STRICTLY ONE speech bubble for [Speaker 1], STRICTLY ONE speech bubble for [Speaker 2], no extra floating speech bubbles or duplicate text boxes on the deck."`
7. **No Border Page Numbers or Border Text:** Never include strings like "Page 18" or "pg 18" in the image prompt string sent to the generator. Include explicit negative text constraints: `"STRICTLY NO PAGE NUMBERS, NO PAGE TITLES, NO BORDER TEXT, NO WATERMARKS, NO BORDER LABELS, NO PRINTED CORNER CAPTIONS."`
8. **Mwaza-Kasa Non-Humanoid Isolation (Page 18/19):** Mwaza-Kasa is a **non-humanoid quadrupedal spirit tortoise walking on four legs with a petrified bark carapace shell**. Include explicit negative constraints to prevent drift into Aggie or Iggy: `"STRICTLY NO HUMANOID FEMALE FEATURES, NO WHITE HAIR, NO CLOTHES, NO AGGIE FEATURES, NO GOGGLES, NO IGGY FEATURES."`


---

### Step 1: Visual Pre-Screening (Mandatory 3-Layer Evidence-First Audit)

Whenever a storyboard page or batch of panels is generated:

1. Call the `view_file` tool on the absolute path of the generated PNG file.
2. Perform the **3-Layer Evidence-First Visual Inspection Protocol**:

#### Layer 1: Background & Environment Isolation Check
- **Location Terrain:** Is the background 100% compliant with the canonical setting?
- **Negative Checks:**
  - ❌ Is there any open water, ocean, sea, or piers in a high canopy forest scene?
  - ❌ Are there generic modern buildings, plastic tablets, or incorrect biomes?
  - *Failure Action:* If environment drifts (e.g. canopy turns into open ocean) → **AUTOMATIC HARD FAIL**.

#### Layer 2: Anatomical & Attachment Verification Check
Cross-check every character against ground-truth profiles:
- **Loami:** Humanoid male, brown flat cap with tiny red-white-green ribbon, canvas working collar, **dark engine grease smudges on hands, face, and collar**, leather pauldrons.
- **Iggy:** Clay-kin creature of packed dark dirt/clay, green moss and small plant sprouts growing on head, round copper water goggles, heavy wool trench coat. **STRICTLY NON-HUMAN. NO HUMAN SKIN. NO NORMAL HUMAN HEAD.**
- **Ignatious:** Young male Islander, **LITERAL roaring orange flames for hair** forming an active crown around dark hair, glowing yellow eyes, dark traveler's cloak. **STRICTLY NO METAL CROWNS, NO GOLDEN TIARAS.**
- **Britt:** Slender green-skinned turtle-mushroom hybrid, pointed ears, long dreadlocks of living green roots past waist, **lumpy grey-green turtle shell securely attached to her back**.
- **Aggie:** Grey-skinned turtle-mushroom hybrid, shoulder-length white hair with green leaf crown, **vibrant red-and-white spotted Amanita mushroom cap shell INTEGRATED onto her back**. **STRICTLY NO FLOATING MUSHROOM UMBRELLA HATS OR TOADSTOOL SUNSHADES OVER HER HEAD.**
- **Mewoders / Beasts:** Small furry tree-cats (bobcat size with bobcat ears), **STRICTLY NOT large panthers or mountain lions**.

#### Layer 3: Text Box & Speech Bubble Scan
- **Character Presence:** Is every speaking character physically drawn in the panel frame? (If speaker is off-screen or missing → **AUTOMATIC HARD FAIL**).
- **Bubble Tail Attribution:** Does the speech bubble tail emerge directly from the speaking character's mouth? (If tail points to wrong character, tree bark, or empty sky → **AUTOMATIC HARD FAIL**).
- **Bubble Count & Duplication:** Count every speech bubble in the panel. (If there are duplicate text boxes, floating text boxes, or repeated dialogue lines → **AUTOMATIC HARD FAIL**).
- **Text Artifact Scan:** Read every word line-by-line. Check for garbled text, mangled letters, or gibberish.

---

### Step 2: Visual Log Logging & Verification

Document the visual findings in `sessions/storyboards/evaluations/sN-evaluation.md` and `walkthrough.md`:
1. Write down an **Explicit Visual Inventory** describing *what is literally in the pixels* BEFORE assigning a grade.
2. Document every failed check, missing token, misattributed speech tail, or text artifact.
3. If ANY layer fails, mark the page as a **HARD FAIL** and lay out the exact prompt rewrite plan.

---

### Step 3: Presenting to User for Final Approval

Present the staged images and your unsparing visual audit report to the user.
> [!IMPORTANT]
> Do not proceed to the next page or batch of generations until the user explicitly confirms that the characters, dialogue attributions, and layout look correct. Human approval is the final gate.

---

### Step 4: Root Cause Analysis (RCA) & Prompt Rewrites

If a panel fails audit or the user identifies an error:
1. **Never patch or edit** a failing prompt. Rewrite it from scratch.
2. Trace the root cause (e.g., missing spatial positioning tokens, ambiguous shell attachment description, unconstrained text generation).
3. Inject rigid negative constraints (`STRICTLY NO...`) and explicit spatial attributions (`Speech bubble coming directly from the mouth of...`).
4. Regenerate and perform the full 3-Layer Evidence-First Audit again.
