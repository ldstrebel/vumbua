---
name: storyboard-audit
description: Audit generated storyboard images against visual profiles, log feedback, and perform root-cause analysis on failures.
---

# Storyboard Quality Auditing & Feedback Protocol

Use this skill when generating comic book pages, reviewing visual storyboard assets, or resolving user feedback regarding character design, visual errors, or scene continuity issues.

---

## 📋 Step-by-Step Audit Workflow

### Step 0: Prompt Validation (Pre-Generation Gate)
**Before calling `generate_image` or writing any panel prompt, validate each prompt against these rules:**

1. **Token Completeness:** Every character visible in the panel has their FULL visual description token from the character profile — not an abbreviation like "the nurse" or "the mechanic." The image generator has zero memory between calls; each prompt must be self-contained.
2. **Location Token Completeness:** Every prompt set in a named location must explicitly inject the full location token (e.g. stone walkways, grassy islands, and Deep-Hull for Harbor; mounted wooden desks in basalt canyon for Apex Arena). Never rely on generic location names like "the harbor."
3. **Quoted Text Integrity:** All text inside `"..."` (speech bubbles and narration boxes) matches the clean transcript verbatim, **including proper nouns and character names.** The "no name leaks" rule applies to visual descriptors only, NOT to printed dialogue/narration text.
4. **No Name Leaks in Descriptors:** Character names appear ONLY inside quoted speech/narration text. The visual descriptor portions of the prompt (scene descriptions, character positioning, shot type) must use physical description tokens, never names.
5. **Speech Bubble Attribution:** Every speech bubble specifies which character (by physical description, not name) it points from.
6. **Script Check:** If `sessions/storyboards/scripts/validate_prompts.py` exists, run it before generation to catch violations automatically.


### Step 1: Visual Pre-Screening (Proactive Check)
Whenever a storyboard page or batch of panels is generated:
1. **Never assume the output is correct.** You must visually inspect the staged PNG files.
2. Call the `view_file` tool on the absolute path of the generated PNG file (e.g., `d:\Code\vumbua\sessions\storyboards\assets\sN_pageNN.png`).
3. Compare the visual details in the image against the **Ground-Truth Character Profiles**:
   * **Loami:** Humanoid male, flat cap with Italian flag ribbon, canvas working collar, grease smudges.
   * **Iggy:** Clay-kin creature of packed dirt/clay, moss and plant sprouts on head, round copper goggles, oversized trench coat. **No shell, no fur, no snout, no animal claws.**
   * **Ignatious:** Young male Islander, burning orange flames for hair, glowing yellow eyes, hooded traveler's cloak.
   * **Britt:** Slender green-skinned turtle-mushroom hybrid, pointed elven ears, root-like dreadlocks, lumpy leaf-strewn turtle shell. **NOT an octopus, NOT shell-less.**
   * **Aggie:** Grey-skinned turtle-mushroom hybrid, white hair, green leaf crown, red-and-white spotted amanita mushroom cap shell. **ONE mushroom shell only, not two.**
   * **Remmy:** Caucasian halfling female nurse, short wavy brown hair, crooked red cloth cap, white linen apron. **Must be consistent across all panels she appears in.**
4. Check layout: Verify that the panel structure (single panel vs. vertical split diptych/triptych) matches the narrative pacing and does not have collapsed scenes.

### Step 2: Visual Log Logging & Verification
Create or update the session evaluation file at `sessions/storyboards/evaluations/sN-evaluation.md`:
1. Log the visual findings for each page/panel in the visual grades table.
2. If there are typos, minor drifts, or errors, note them down in the audit comments.

### Step 3: Presenting to User for Final Approval
Present the staged images and your visual audit report to the user.
> [!IMPORTANT]
> Do not proceed to the next page or batch of generations until the user explicitly confirms that the characters and layout look correct. Human approval is the final gate.

### Step 4: Feedback Ingestion & Root Cause Analysis (RCA)
If the user rejects a panel or notes a character consistency error (e.g., "Iggy has a shell," "Iggy is a mole," "Ignatious has normal hair"):
1. **Log the Failure:** Open `sessions/storyboards/evaluations/sN-evaluation.md` and add a new entry under the **Root Cause Analysis (RCA) & Revision History** section.
2. **Perform RCA:** Check the prompt history and trace back the failure:
   * Did a name leak into the visual descriptor portion of the prompt?
   * Was an outdated token (like "mole-like") used?
   * Was a key physical token (like "moss sprouts" or "trench coat") omitted from a panel prompt?
   * Did the generator collapse a multi-panel layout?
   * Was a recurring NPC (like a nurse) described with an abbreviated token, causing visual drift across panels?
   * Were proper nouns incorrectly stripped from quoted speech bubble or narration text?
   * Was dialogue improvised or paraphrased instead of pulled verbatim from the clean transcript?
3. **Document the RCA:** Record the symptom, the root cause, and the planned resolution in the evaluation markdown file.
4. **Rewrite the Prompt:** **DO NOT PATCH OR EDIT** the failing prompt. Rewrite it from scratch, pulling the exact physical tokens verbatim from the characters' markdown files.
5. **Regenerate & Re-Audit:** Generate the new image, copy it to assets, call `view_file` to verify the fix, and present it for final human review.
