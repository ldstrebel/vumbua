---
description: Generate a graphic novel storyboard for a Vumbua campaign session
---

# Storyboard Workflow (Slash Command: /storyboard)

Use this workflow when generating comic book pages for a Vumbua session.

> **Cross-reference:** All rules in `.agent/AGENTS.md` apply to every step of this workflow. Read them before starting.

---

## Step 0 — MANDATORY Ground-Truth Verification (DO NOT SKIP)

This step is not optional. Do not write a single panel description until it is complete.

### 0a. Read the clean transcript
Call `view_file` on `sessions/transcripts/clean/sN-clean.md` for the session being storyboarded.
- Identify every major scene (a scene = a distinct location or narrative beat)
- Note the exact dialogue lines that need to appear as speech bubbles
- Note the order of events — do not rely on memory of the session

### 0b. Read every character profile for characters in this session
Call `view_file` on each file for characters who appear:
- `characters/player-characters/loami.md`
- `characters/player-characters/iggy.md`
- `characters/player-characters/ignatious.md`
- `characters/player-characters/aggie.md`
- `characters/player-characters/britt.md`
- Any relevant NPC file in `characters/npcs/`

**For each character, copy the physical description lines into a working token block.** Do not write tokens from memory.

### 0c. Check which reference assets exist
Call `list_dir` on `sessions/storyboards/assets/` to see what source images are available (blueprints, chalkboards, maps). Only reference files that actually exist.

### 0d. Build the scene outline — show it to the user before generating anything

Write a scene list in this format and **stop here for user review**:

```markdown
## Scene Outline: Session N

| # | Scene | Location | Key Characters | Proposed Pages |
|---|---|---|---|---|
| 1 | [Scene name] | [Location] | [Characters] | [e.g. 2] |
...

**Total proposed pages: [N]**
```

**Wait for user confirmation** on the scene count and page budget before proceeding. If the user requests changes, revise the outline before any generation.

---

## Step 1 — Write the Full Storyboard Document

Only begin this step after the user approves the scene outline.

Write the complete storyboard to `sessions/storyboards/sN-storyboard.md` before generating any images. The storyboard is the ground-truth specification — images must match it, not the other way around.

### Page budget guidance

Scale page count to the session's actual content:
- **1–2 short scenes:** 4–6 pages
- **3–4 scenes:** 8–12 pages
- **5+ scenes or complex mechanics:** 12–20 pages

Never compress multiple major scenes onto a single page unless they are directly continuous (e.g., a two-line exchange).

### Panel format (per page)

Each page must include:

```markdown
## Page N: [Scene Title]

**Scene:** [Location description — match AGENTS.md location rules]
**Color palette:** [Specific palette: warm amber, steel grey, etc.]
**Lighting:** [Direction and quality of light]

### Panel 1
**Shot:** [Wide / Medium / Close-up / Splash]
**Description:** [THICK description — characters with full token strings, background elements, foreground details, action]
**Speech bubble:** "[Exact quote from clean transcript]" — [Character token description, not name]
**Sound effect:** [e.g., KA-CLANK! in bold hand-lettered style — if applicable]

### Panel 2
...

#### 🖤 Gutter Transition:
[Describe the spatial or temporal shift between this page and the next]
```

### Dialogue rules
- **Exact quotes only** — lifted verbatim from the clean transcript. Never paraphrase.
- **25-word maximum** per speech bubble. If a quote is longer, split across two bubbles or two panels.
- **Dialect preservation** — Iggy's dropped letters (`'S nice`, `'course`), Kante's broken English. Do not "fix" these.

### Character description tokens
Never use a character's name in a panel prompt. Use the tokens extracted in Step 0b. Example structure:
```
[rugged broad-shouldered humanoid male, short brown hair, short beard, brown woolen flat cap with tiny Italian flag ribbon, heavy canvas working collar, dark engine grease smudges on hands and collar]
```

---

## Step 2 — Generate Images (2–3 Pages at a Time)

Only begin generation after the full storyboard document is written and the user has had the opportunity to review the outline.

### Generation rules

- Generate **2–3 pages per batch**, then stop
- After each batch, **call `view_file` on the generated PNGs to visually audit character details and scene consistency. Document your findings, then present the images and your audit to the user for explicit confirmation** before continuing.
- If the user (or the visual audit) identifies any character error, treat it as a hard fail — rewrite the prompt from scratch using the ground-truth token from the profile file.
- Do not patch prompts. Rewrite them.

### Image prompt structure (for `generate_image` tool)

Each page = one `generate_image` call. Structure the prompt as:

```
[Style token: Detailed 2D graphic novel style, clean expressive manga-style linework, crisp black ink outlines, cel-shaded color flats, cinematic volumetric lighting]

[Page layout description: e.g. "A three-panel comic book page"]

Panel 1: [THICK description — shot type, character tokens, background, lighting, action, speech bubble text, sound effects]

Panel 2: [THICK description]

Panel 3: [THICK description]

[Color palette note: e.g. "Warm amber gas-lamp interior lighting throughout, mahogany and brass textures"]

--no text artifacts, no subtitles, no watermarks, no generic fantasy backgrounds
```

### Mandatory pause points

| After | Action |
|---|---|
| Scene outline (Step 0d) | ⏸ Stop — wait for user approval of page budget |
| Pages 1–3 | ⏸ Stop — show images, wait for character confirmation |
| Pages 4–6 | ⏸ Stop — show images, wait for confirmation |
| Every 3 pages thereafter | ⏸ Stop — show images, wait for confirmation |
| Final page | ⏸ Stop — ask user if any pages need regeneration |

---

## Step 3 — Save Assets and Update Storyboard

After all pages are approved by the user:

1. Copy each approved image to `sessions/storyboards/assets/sN_pageNN.png`
2. Update the storyboard document to reference the asset paths
3. Run `python _export.py` to rebuild the NotebookLM export

---

## The Vumbua Visual Style (Anti-Trope Rules)

Apply these rules to every panel prompt.

### Architecture
"Oxford meets Steampunk, built into the Wild." Pristine white marble facades and sweeping arches are **carved directly into rugged natural cliff faces**. Sharp contrast between manicured academic stone and raw natural textures.

### Technology
Gaslamp fantasy. Steam, brass, umber crystals, gears. Do NOT use generic glowing magical auras or sci-fi thrusters.

### Airships
Treasure Planet-style solar galleons or heavy brass ironclads held aloft by massive silk-textured golden dirigible balloons with ornate golden solar sails. Do NOT generate generic blimps or sailboats.

### The Apex Ring
Half-mile-wide basalt canyon. Grandstands cut directly into the canyon walls. Ground is exactly half solid earth and half turquoise water. NEVER a floating stadium or a flat arena.

### Spectator vehicles
Ornate steam-pulled observation cars with vast glass windows and outward-facing bleacher seating. Tracks run elevated **behind** the grandstands, never between the crowd and the view.

### Anti-tropes (ban from all prompts)
`--no generic steampunk, clock faces, top hats, modern vehicles, bullet trains, jet engines, rockets, sci-fi thrusters, dirt arenas, generic fantasy castles, Japanese subtitles, watermarks`

---

## Video Prompt Output (Optional — for external tools)

If the user requests video prompts for Runway/Luma after the graphic novel is approved, generate these separately using the approved images as reference:

### Image-to-Video Stitching Prompt
Describe the physical camera path between panels using structural wipes and match-cuts. **"Double tap"** key design elements at every transition (e.g., "revealing the *colossal, blinding white marble* stadium" not just "revealing the stadium").

### Direct Text-to-Video Prompt
Write a continuous tracking shot description in Studio Ghibli/Makoto Shinkai anime style, describing all three phases of the scene in a single unbroken camera movement.
