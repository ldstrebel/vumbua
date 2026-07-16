---
name: storyboard-audit
description: Audit generated storyboard images against visual profiles, log feedback, and perform root-cause analysis on failures.
---

# Storyboard Quality Auditing & Feedback Protocol

Use this skill when generating comic book pages, reviewing visual storyboard assets, or resolving user feedback regarding character design, visual errors, or scene continuity issues.

---

## 📋 Step-by-Step Audit Workflow

### Step 1: Visual Pre-Screening (Proactive Check)
Whenever a storyboard page or batch of panels is generated:
1. **Never assume the output is correct.** You must visually inspect the staged PNG files.
2. Call the `view_file` tool on the absolute path of the generated PNG file (e.g., `d:\Code\vumbua\sessions\storyboards\assets\sN_pageNN.png`).
3. Compare the visual details in the image against the **Ground-Truth Character Profiles**:
   * **Loami:** Humanoid male, flat cap with Italian flag ribbon, canvas working collar, grease smudges.
   * **Iggy:** Clay-kin creature of packed dirt/clay, moss and plant sprouts on head, round copper goggles, oversized trench coat. **No shell, no fur, no snout, no animal claws.**
   * **Ignatious:** Young male Islander, burning orange flames for hair, glowing yellow eyes, hooded traveler's cloak.
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
   * Did a name leak into the prompt?
   * Was an outdated token (like "mole-like") used?
   * Was a key physical token (like "moss sprouts" or "trench coat") omitted from a panel prompt?
   * Did the generator collapse a multi-panel layout?
3. **Document the RCA:** Record the symptom, the root cause, and the planned resolution in the evaluation markdown file.
4. **Rewrite the Prompt:** **DO NOT PATCH OR EDIT** the failing prompt. Rewrite it from scratch, pulling the exact physical tokens verbatim from the characters' markdown files.
5. **Regenerate & Re-Audit:** Generate the new image, copy it to assets, call `view_file` to verify the fix, and present it for final human review.
