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

| # | Scene | Location | Key Characters | Proposed Pages | Layout Structure & Justification |
|---|---|---|---|---|---|
| 1 | [Scene name] | [Location] | [Characters] | [e.g. 2] | [e.g. 2-Panel Asymmetrical Split — establishes environment top, tight dialogue bottom] |
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

### Panel Format & Dynamic Layout Flexibility (Mandatory Anti-Grid & Justification Rule)

Do **NOT** default to a static 3-panel grid for every page. For EVERY page, you MUST explicitly justify the panel count, geometry, and layout approach:

- **1-Panel Splash / Overlay:** High-impact revelations, epic vistas, or grand battle scenes (with optional inset panels/narration overlays).
- **2-Panel Asymmetrical Vertical Split:** Establishing wide shot (65% top) transitioning into emotional reaction close-up (35% bottom).
- **2-Panel Dynamic High-Contrast Split:** Confrontations or presentation vs. explosive action transitions (50/50 split).
- **2-Panel Asymmetrical Diagonal / Side Split:** Parallel actions (e.g. 60% left action / 40% full-height right transition).
- **2-Panel Progression leading to Splash:** Top narrative return leading into a full-width bottom detailed splash (40/60 split).
- **3-Panel Tiered Grid:** Selectively used for multi-step conversations or fast step-by-step action sequences.
- **4-Panel Quad Grid:** Rapid multi-character reactions or fast combat exchanges.

**Mandatory Page Header Format:**
Every page in the storyboard markdown file MUST include:

```markdown
## Page N: [Scene Title]

**Scene Location:** [Location description — match AGENTS.md location rules]
**Color Palette:** [Specific palette: warm amber, steel grey, dark turquoise, etc.]
**Layout Structure:** [Specify layout: e.g., 2-Panel Asymmetrical Diagonal Split (65/35), 1-Panel Splash, etc.]
**Layout Justification:** [Explicitly justify WHY this panel count and geometry was chosen for this specific beat, and how it avoids formulaic grids]

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

[Page layout description: e.g. "An asymmetrical two-panel comic book page with black gutters divided by a sharp diagonal black gutter slash, top panel taking up 65% vertical height and bottom panel taking up 35% vertical height"]

Panel 1: [THICK description — shot type, character tokens, background, lighting, action, speech bubble text, sound effects]

Panel 2: [THICK description]

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
