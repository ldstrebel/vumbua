#!/usr/bin/env python3
"""
Storyboard Prompt Validator
===========================
Validates image prompts in storyboard markdown files against the AGENTS.md rules.
Catches the four failure modes identified in the S8 postmortem:

1. Name leaks in visual descriptors (outside quoted text)
2. Proper nouns stripped from quoted speech/narration text
3. Abbreviated character tokens (e.g. "the nurse" instead of full description)
4. Missing speech bubbles in prompts that should have them

Usage:
    python validate_prompts.py <storyboard-file.md> [--transcript <clean-transcript.md>]
"""

import re
import sys
import argparse
from pathlib import Path

# Fix Windows terminal encoding
sys.stdout.reconfigure(encoding="utf-8", errors="replace")



# Known character names that should NOT appear in visual descriptor context
CHARACTER_NAMES = [
    "Loami", "Iggy", "Ignatious", "Britt", "Aggie",
    "Remmy", "Bjorn", "Lyra", "Ludo", "Isolde", "Vane",
    "Pip", "Bramble", "Kante",
]

# Abbreviated tokens that indicate incomplete character descriptions
ABBREVIATED_TOKENS = [
    r"\bthe nurse\b",
    r"\bthe halfling nurse\b",
    r"\bthe mechanic\b",
    r"\bthe dean\b",
    r"\bthe cousin\b",
    r"\bthe clay creature\b",
    r"\bthe fire-haired\b",
    r"\ba halfling\b(?! female nurse with kind)",
    r"\ba nurse\b(?! with kind)",
]


# Minimum character description length (chars) to consider "complete"
MIN_TOKEN_LENGTH = 40


def extract_prompts(md_text: str) -> list[dict]:
    """Extract all image prompts from the storyboard markdown."""
    prompts = []
    lines = md_text.split("\n")
    
    for i, line in enumerate(lines):
        if "#### 🎨 Image Prompt:" in line:
            # The prompt is on the next line(s) inside backticks
            prompt_text = ""
            # Check if prompt is on same line
            if "`" in line:
                match = re.search(r"`(.+?)`", line, re.DOTALL)
                if match:
                    prompt_text = match.group(1)
            
            # If not found, scan subsequent lines
            if not prompt_text:
                for j in range(i + 1, min(i + 10, len(lines))):
                    match = re.search(r"`(.+?)`", lines[j], re.DOTALL)
                    if match:
                        prompt_text = match.group(1)
                        break
            
            if prompt_text:
                # Find the page header above this prompt
                page_title = "Unknown"
                for k in range(i, max(i - 20, 0), -1):
                    if lines[k].startswith("### Page"):
                        page_title = lines[k].strip("# ").strip()
                        break
                
                prompts.append({
                    "line": i + 1,
                    "page_title": page_title,
                    "text": prompt_text,
                })
    
    return prompts


def extract_quoted_text(prompt: str) -> list[str]:
    """Extract all quoted strings from a prompt (speech bubble / narration text)."""
    # Match text inside double quotes preceded by "text:" or similar context
    return re.findall(r'"([^"]+)"', prompt)


def get_descriptor_text(prompt: str) -> str:
    """Return the prompt text with all quoted strings removed (visual descriptor only)."""
    return re.sub(r'"[^"]*"', '""', prompt)


def check_name_leaks_in_descriptors(prompt_data: dict) -> list[str]:
    """Check for character names in visual descriptor portions (outside quotes)."""
    issues = []
    descriptor_text = get_descriptor_text(prompt_data["text"])
    
    for name in CHARACTER_NAMES:
        # Case-insensitive search in descriptor text
        pattern = rf"\b{re.escape(name)}\b"
        matches = re.findall(pattern, descriptor_text, re.IGNORECASE)
        if matches:
            issues.append(
                f"❌ NAME LEAK: '{name}' found in visual descriptor text "
                f"(outside quotes). Replace with physical description token."
            )
    
    return issues


def check_names_preserved_in_quotes(prompt_data: dict) -> list[str]:
    """
    Check that proper nouns in quoted text haven't been replaced with descriptions.
    Flags suspicious patterns like 'the white-haired cousin' or 'the green-skinned female'
    appearing inside speech bubble quotes.
    """
    issues = []
    quoted_texts = extract_quoted_text(prompt_data["text"])
    
    suspicious_replacements = [
        (r"the white-haired (cousin|female|woman|girl)", "Aggie"),
        (r"the green-skinned (cousin|female|woman|girl)", "Britt"),
        (r"the clay (creature|kin|humanoid)", "Iggy"),
        (r"the fire-haired (male|boy|youth|young man)", "Ignatious"),
        (r"the broad-shouldered (male|man|humanoid)", "Loami"),
        (r"the halfling (nurse|female|woman)", "Remmy"),
    ]
    
    for quoted in quoted_texts:
        for pattern, likely_name in suspicious_replacements:
            if re.search(pattern, quoted, re.IGNORECASE):
                issues.append(
                    f"⚠️  STRIPPED NAME: '{quoted[:50]}...' contains a description "
                    f"('{pattern}') where the character name '{likely_name}' should "
                    f"probably appear verbatim per the transcript."
                )
    
    return issues


def check_abbreviated_tokens(prompt_data: dict) -> list[str]:
    """Check for abbreviated character references that should be full tokens."""
    issues = []
    descriptor_text = get_descriptor_text(prompt_data["text"])
    
    for pattern in ABBREVIATED_TOKENS:
        matches = re.findall(pattern, descriptor_text, re.IGNORECASE)
        if matches:
            issues.append(
                f"⚠️  ABBREVIATED TOKEN: '{matches[0]}' found. Use the full "
                f"visual description token (>{MIN_TOKEN_LENGTH} chars) instead."
            )
    
    return issues


def check_speech_bubbles_present(prompt_data: dict) -> list[str]:
    """Check that prompts contain speech bubble instructions."""
    issues = []
    text = prompt_data["text"]
    
    # Check if there are speech bubble descriptions in the panel section above
    # (This is a heuristic — we flag if the prompt has no quoted text at all)
    quoted = extract_quoted_text(text)
    has_bubble_instruction = (
        "speech bubble" in text.lower() or
        "narration box" in text.lower() or
        "caption" in text.lower()
    )
    
    if not has_bubble_instruction and not quoted:
        issues.append(
            f"⚠️  NO TEXT ELEMENTS: Prompt has no speech bubbles, narration boxes, "
            f"or quoted text. Per AGENTS.md Rule 2, text must be baked into the art."
        )
    
    return issues


def check_bubble_attribution(prompt_data: dict) -> list[str]:
    """Check that speech bubbles specify which character (by description) they point from."""
    issues = []
    # Strip quoted text first so character names inside dialogue/narration are ignored
    descriptor_text = get_descriptor_text(prompt_data["text"])
    
    # Find speech bubble instructions
    bubble_pattern = r"speech bubble.*?(?:containing|with|reads|says|points)"
    bubbles = re.findall(bubble_pattern, descriptor_text, re.IGNORECASE)
    
    for bubble in bubbles:
        # Check for attribution by name instead of description
        for name in CHARACTER_NAMES:
            if re.search(rf"\b{re.escape(name)}\b", bubble, re.IGNORECASE):
                issues.append(
                    f"❌ BUBBLE ATTRIBUTION BY NAME: Speech bubble attributed to "
                    f"'{name}' by name. Use physical description instead."
                )
    
    return issues



def validate_storyboard(filepath: str, transcript_path: str = None) -> dict:
    """Run all validation checks on a storyboard file."""
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    
    md_text = path.read_text(encoding="utf-8")
    prompts = extract_prompts(md_text)
    
    results = {
        "file": str(path),
        "total_prompts": len(prompts),
        "pages_with_issues": 0,
        "total_issues": 0,
        "issues_by_page": {},
    }
    
    for prompt_data in prompts:
        page_issues = []
        
        page_issues.extend(check_name_leaks_in_descriptors(prompt_data))
        page_issues.extend(check_names_preserved_in_quotes(prompt_data))
        page_issues.extend(check_abbreviated_tokens(prompt_data))
        page_issues.extend(check_speech_bubbles_present(prompt_data))
        page_issues.extend(check_bubble_attribution(prompt_data))
        
        if page_issues:
            results["pages_with_issues"] += 1
            results["total_issues"] += len(page_issues)
            results["issues_by_page"][prompt_data["page_title"]] = {
                "line": prompt_data["line"],
                "issues": page_issues,
            }
    
    return results


def print_report(results: dict):
    """Print a human-readable validation report."""
    print("=" * 70)
    print(f"📋 Storyboard Prompt Validation Report")
    print(f"   File: {results['file']}")
    print(f"   Prompts scanned: {results['total_prompts']}")
    print("=" * 70)
    
    if results["total_issues"] == 0:
        print("\n✅ All prompts passed validation. No issues found.\n")
        return
    
    print(f"\n🚨 Found {results['total_issues']} issue(s) across "
          f"{results['pages_with_issues']} page(s):\n")
    
    for page_title, data in results["issues_by_page"].items():
        print(f"--- {page_title} (line {data['line']}) ---")
        for issue in data["issues"]:
            print(f"  {issue}")
        print()
    
    print("=" * 70)
    print(f"Summary: {results['total_issues']} issues, "
          f"{results['pages_with_issues']}/{results['total_prompts']} pages affected.")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Validate storyboard prompts against AGENTS.md rules"
    )
    parser.add_argument(
        "storyboard",
        help="Path to the storyboard markdown file"
    )
    parser.add_argument(
        "--transcript", "-t",
        help="Path to the clean transcript for cross-referencing dialogue",
        default=None,
    )
    
    args = parser.parse_args()
    results = validate_storyboard(args.storyboard, args.transcript)
    print_report(results)
    
    # Exit with error code if issues found
    sys.exit(1 if results["total_issues"] > 0 else 0)


if __name__ == "__main__":
    main()
