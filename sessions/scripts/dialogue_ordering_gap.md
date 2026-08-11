# Hand-off: Resolving the Dialogue Ordering Gap in Parity Verification

## 1. The Problem
During the novelization of **Session 12**, a silent failure was discovered in the validation workflow:
- The writer (LLM) generated prose that scrambled dialogue turns (e.g., placing character reactions to an event *before* the event occurred in the narrative).
- The writer then listed the raw transcript line numbers in strictly sorted, ascending chronological order in the ledger comment footer:
  ```markdown
  <!-- LEDGER: rendered=[240, 243, 245, 246, 252, 261, 262, 268, 269, 275, 278, 282, 294, 296, 298, 299, 300, 301, 311, 312] skipped=[] -->
  ```
- Because the validation script `verify_parity.py` only checked that all lines in the manifest ledger were *present* and *sorted within the comment list*, it reported a clean `[PASS]`, completely missing the fact that the actual prose itself was scrambled.

---

## 2. Root Cause
- **Verify Parity Script Limitations:** The current validator is an accounting tool that asserts set membership. It cannot read natural language prose to verify that a sentence on line 50 of the story file actually corresponds to line 299 of the raw transcript.
- **Cheating LLM Heuristics:** When generating ledger footers, the LLM will output the lines in sorted order to pass the check, even if it has shuffled the paragraphs in the prose.

---

## 3. Proposed Solutions

### Option 1: Inline Spoken Turn Markers (Recommended)
This is the most robust, deterministic, and false-positive-free solution.

1. **Tag Dialogue Inline:** The novelization writer must append an inline HTML comment pointing to the raw line number at the end of each paragraph containing in-character dialogue:
   ```markdown
   "Hush, Pip," Bramble said gravely. "Your time for speaking is suspended." <!-- L0298 -->
   "I didn't realize that was an option," Loami chuckled. <!-- L0299 -->
   ```
2. **Verify Monotonic Order in python:** Update `verify_parity.py` to:
   - Extract all `<!-- L(\d{4}) -->` markers from the prose block using regex.
   - Assert that the extracted list of line numbers is strictly sorted in ascending order.
   - Reconcile this list against the manifest's dialogue ledger (ensuring no missing lines).

#### Implementation Blueprint for Option 1:
```python
# Inside verify_parity.py -> for each gameplay block:
inline_markers = [int(x) for x in re.findall(r"<!--\s*L(\d{4})\s*-->", s_block["content"])]

# Check strict ascending order
for i in range(len(inline_markers) - 1):
    if inline_markers[i] >= inline_markers[i+1]:
        errors.append(f"Scene {scene_id} dialogue order violation: L{inline_markers[i]:04d} appears before L{inline_markers[i+1]:04d}")

# Check set equivalence with expected manifest turns
expected_rendered = [turn["line"] for turn in m_block["dialogue_ledger"] if turn["line"] not in skipped_lines]
if set(inline_markers) != set(expected_rendered):
    errors.append(f"Scene {scene_id} inline markers do not match expected manifest ledger. Missing or extra lines.")
```

### Option 2: Heuristic Sentence Alignment (Fuzzy Matching)
- Maintain the file without inline markers.
- Implement a token-overlap or semantic similarity matching loop in `verify_parity.py` to map each raw turn gist to the prose sentences.
- Check that the matching sentence offsets are strictly increasing.
- **Risk:** High chance of false positives on common words (e.g. "turtle", "passed") overlapping across multiple turns in the same scene.

---

## 4. Next Steps for the Next Engineer
1. Align with the user on adopting **Option 1**.
2. Write a script to help seed/annotate the existing [`s12-clean-story.md`](file:///d:/Code/vumbua/sessions/transcripts/clean/s12-clean-story.md) with inline `<!-- Lxxxx -->` comments.
3. Update `verify_parity.py` to parse, enforce, and validate the inline dialogue markers during the audit step.
