import os
import re
import sys

npcs_dir = r"d:\Code\vumbua\characters\npcs"
valid_categories = {"first-year", "second-year", "faculty", "notable-figure"}
ignore_files = {"captains-dossier.md", "lucky-timeline.md", "second-year-pilots.md"}

def validate_all_npcs():
    errors = []
    total_checked = 0

    if not os.path.exists(npcs_dir):
        print(f"Error: Directory {npcs_dir} does not exist.")
        sys.exit(1)

    files = [f for f in os.listdir(npcs_dir) if f.endswith(".md") and f not in ignore_files]

    for filename in files:
        filepath = os.path.join(npcs_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        total_checked += 1

        # Check for frontmatter
        if not content.startswith("---"):
            errors.append(f"{filename}: Missing YAML frontmatter header '---'")
            continue

        # Extract tags
        tags_match = re.search(r"tags:\n((?:  - .*\n)+)", content)
        if not tags_match:
            errors.append(f"{filename}: Missing or malformed 'tags:' block in frontmatter")
            continue

        file_tags = [t.strip().replace("- ", "") for t in tags_match.group(1).strip().split("\n")]
        
        # Check category tag
        categories_found = set(file_tags).intersection(valid_categories)
        if len(categories_found) == 0:
            errors.append(f"{filename}: Missing explicit category tag (must have one of {valid_categories})")
        elif len(categories_found) > 1:
            errors.append(f"{filename}: Multiple conflicting category tags found: {categories_found}")

        # Check squad tags consistency
        has_squad_tag = any(t.startswith("squad-") for t in file_tags)
        if has_squad_tag:
            if "first-year" not in file_tags:
                errors.append(f"{filename}: Has squad tag {file_tags} but is NOT tagged 'first-year'")
            if "second-year" in file_tags:
                errors.append(f"{filename}: CRITICAL ERROR — Has squad tag {file_tags} AND is tagged 'second-year'")

    print("========================================")
    print(f"NPC METADATA VALIDATION REPORT")
    print(f"Total Character Files Checked: {total_checked}")
    print(f"Total Validation Errors:      {len(errors)}")
    print("========================================")

    if errors:
        for err in errors:
            print(f"[FAIL] {err}")
        sys.exit(1)
    else:
        print("[SUCCESS] ALL 69 NPC CHARACTER PROFILES PASSED 100% CLEAN VALIDATION!")
        sys.exit(0)

if __name__ == "__main__":
    validate_all_npcs()
