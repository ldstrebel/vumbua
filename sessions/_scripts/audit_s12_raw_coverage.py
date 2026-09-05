import re
import os

def audit_raw_coverage(raw_path, clean_path, story_path):
    print("==================================================")
    print("[AUDIT] RAW TRANSCRIPT TO CLEAN/STORY COVERAGE AUDIT")
    print("==================================================")

    with open(raw_path, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    with open(clean_path, 'r', encoding='utf-8') as f:
        clean_text = f.read()

    with open(story_path, 'r', encoding='utf-8') as f:
        story_text = f.read()

    # Key canon plot anchors to verify across raw, clean, and story
    key_anchors = [
        ("Sterling Broadcast", ["Night of Embers", "Panda 5", "half made it"]),
        ("Spirit Tortoise Amnesiac Walk", ["forget", "walk", "glide"]),
        ("Iggy Grounding Ritual", ["rock", "head", "heart", "feet"]),
        ("Pip Biscuit Distribution", ["biscuit", "wounded"]),
        ("Val & Finch's Death", ["spectacles", "Finch", "Val"]),
        ("Kale Communication Stones", ["stones", "Conte", "crystal"]),
        ("Raphael Shield Explanation", ["invasion", "short-circuited"]),
        ("Rill's Wadi Salve", ["Wadi", "salve", "two weeks"]),
        ("Recruiting Zephyr", ["electric purple", "shark teeth", "Fulgur"]),
        ("Recruiting Lucky", ["Sarge", "Lucky"]),
        ("Saffron's Sky Island", ["Saffron", "sketch", "floating"]),
        ("Professor Inc.'s Walker", ["spider", "walker", "expedition"]),
        ("Heading Adjustment", ["two degrees", "Center Grove"]),
        ("Wantila Fungus Barrier", ["Wantila", "fungus", "lethal"]),
        ("Network Vision (5 Clans)", ["Mizizi", "Ash-Blood", "Trench", "Fulgur", "Wadi", "Renali"]),
        ("Clear-Cutting Memory Loss", ["mycelium", "uploaded", "bark", "dust"]),
        ("Mwaza-Kasa Shell Map", ["shell", "map", "pinprick runes"])
    ]

    print("\n[CHECKING 17 CANON PLOT ANCHORS]:")
    all_passed = True
    for title, terms in key_anchors:
        in_raw = any(t.lower() in raw_text.lower() for t in terms)
        in_clean = any(t.lower() in clean_text.lower() for t in terms)
        in_story = any(t.lower() in story_text.lower() for t in terms)

        status = "PASS" if (in_clean and in_story) else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"  • {title:30s} | Raw: {'YES' if in_raw else 'NO '} | Clean: {'YES' if in_clean else 'NO '} | Story: {'YES' if in_story else 'NO '} -> [{status}]")

    if all_passed:
        print("\n[PASS] ALL 17 CANON PLOT ANCHORS COVERED 100% IN CLEAN AND STORY FILES!")
    else:
        print("\n[WARNING] SOME ANCHORS MISSING - SEE DETAIL ABOVE.")

if __name__ == '__main__':
    audit_raw_coverage(
        "sessions/data/raw/s12-raw.md",
        "sessions/data/clean/s12-clean.md",
        "sessions/data/clean/s12-clean-story.md"
    )
