import sys
import os
import re
import json
import hashlib

def get_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def clean_lines(filepath):
    # Reads the lines of the file, stripping standard prefixes like LXXXX:
    lines = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Strip LXXXX: prefix
            match = re.match(r"^L\d{4}:\s*(.*)$", line)
            if match:
                lines.append(match.group(1))
            else:
                lines.append(line)
    return lines

def parse_ledger_list(list_str):
    # Parses list of numbers like "[975, 1041]" or "[L0975, L1041]" or "[]"
    # Strips any non-digit chars before/after commas
    list_str = list_str.strip()
    if list_str == "[]" or not list_str:
        return []
    # Find all sequences of digits (optionally preceded by L)
    matches = re.findall(r"L?(\d+)", list_str)
    return [int(m) for m in matches]

def calculate_dialogue_words(lines, start_line, end_line):
    word_count = 0
    # Line ranges in manifest are 1-indexed
    for idx in range(start_line - 1, min(end_line, len(lines))):
        line = lines[idx]
        # Match dialogue format: **Speaker:** dialogue
        match = re.match(r"^\*\*([^*]+):\*\*\s*(.*)$", line)
        if match:
            dialogue_text = match.group(2)
            word_count += len(dialogue_text.split())
    return word_count

def verify_parity(session_id):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manifest_path = os.path.join(base_dir, "transcripts", "index", f"{session_id}-manifest.json")
    indexed_path = os.path.join(base_dir, "transcripts", "index", f"{session_id}-raw-indexed.md")
    story_path = os.path.join(base_dir, "transcripts", "clean", f"{session_id}-clean-story.md")

    errors = []
    warnings = []

    # 1. Load manifest and check file existence
    if not os.path.exists(manifest_path):
        print(f"Error: Manifest not found at {manifest_path}")
        sys.exit(1)
    if not os.path.exists(indexed_path):
        print(f"Error: Indexed file not found at {indexed_path}")
        sys.exit(1)
    if not os.path.exists(story_path):
        print(f"Error: Story file not found at {story_path}")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # 2. Hash lock check
    actual_hash = get_sha256(indexed_path)
    expected_hash = manifest.get("raw_file_hash")
    if actual_hash != expected_hash:
        errors.append(f"HASH LOCK MISMATCH: indexed file hash is '{actual_hash}', manifest expected '{expected_hash}'")

    # 3. Read raw indexed lines for word counting
    raw_lines = clean_lines(indexed_path)
    total_raw_lines = manifest.get("total_raw_lines")

    # 4. Read story file
    with open(story_path, "r", encoding="utf-8") as f:
        story_content = f.read()

    # 5. Extract RAW_RANGE sections from story file
    # Pattern matches: <!-- RAW_RANGE: [start, end] | SCENE_ID: N -->
    # followed by the block content
    # followed by the next RAW_RANGE or end of file
    sections = re.findall(
        r"<!--\s*RAW_RANGE:\s*\[(\d+),\s*(\d+)\]\s*\|\s*SCENE_ID:\s*(\d+)\s*(?:\|\s*(OOC))?\s*-->\s*(.*?)(?=<!--\s*RAW_RANGE:|$)", 
        story_content, 
        re.DOTALL
    )

    covered_lines = set()
    story_scenes = {}

    for start_str, end_str, scene_id_str, ooc_flag, block_content in sections:
        start, end = int(start_str), int(end_str)
        scene_id = int(scene_id_str)
        is_ooc = bool(ooc_flag)

        # Line ranges overlapping check in story
        block_lines = set(range(start, end + 1))
        overlap = block_lines.intersection(covered_lines)
        if overlap:
            errors.append(f"OVERLAP IN STORY: Scene {scene_id} range [{start}, {end}] overlaps with other scenes on lines: {sorted(list(overlap))[:10]}...")
        covered_lines.update(block_lines)

        story_scenes[scene_id] = {
            "range": (start, end),
            "content": block_content.strip(),
            "is_ooc": is_ooc
        }

    # Verify tiling of ranges in story matches total lines
    missing_lines = set(range(1, total_raw_lines + 1)) - covered_lines
    if missing_lines:
        errors.append(f"LINE LEAK DETECTED IN STORY: {len(missing_lines)} lines are not covered. Missing lines: {sorted(list(missing_lines))[:20]}...")

    # 6. Verify agreement with manifest blocks
    manifest_scenes = {b["scene_id"]: b for b in manifest.get("scene_blocks", [])}

    for scene_id, m_block in manifest_scenes.items():
        m_start, m_end = m_block["line_range"]
        m_ooc = m_block.get("ooc", False)

        if scene_id not in story_scenes:
            errors.append(f"MISSING SCENE IN STORY: Scene {scene_id} ('{m_block['title']}') is present in manifest but missing from story.")
            continue

        s_block = story_scenes[scene_id]
        s_start, s_end = s_block["range"]
        s_ooc = s_block["is_ooc"]

        # Range agreement check
        if s_start != m_start or s_end != m_end:
            errors.append(f"RANGE MISMATCH: Scene {scene_id} in story covers [{s_start}, {s_end}], but manifest expects [{m_start}, {m_end}]")

        # OOC agreement check
        if s_ooc != m_ooc:
            errors.append(f"OOC FLAGS MISMATCH: Scene {scene_id} OOC is {s_ooc} in story, but manifest expects {m_ooc}")

        # Non-OOC Block Auditing
        if not m_ooc:
            # 6a. Parse ledger footer
            # Pattern: <!-- LEDGER: rendered=[...] skipped=[...] -->
            ledger_match = re.search(
                r"<!--\s*LEDGER:\s*rendered=\[(.*?)\]\s*skipped=\[(.*?)\]\s*-->", 
                s_block["content"]
            )
            if not ledger_match:
                errors.append(f"MISSING LEDGER FOOTER: Scene {scene_id} does not contain a ledger footer block.")
                continue

            rendered_lines = parse_ledger_list(ledger_match.group(1))
            skipped_lines = parse_ledger_list(ledger_match.group(2))

            # Reconcile dialogue ledger lines
            expected_ledger = [turn["line"] for turn in m_block.get("dialogue_ledger", [])]
            story_ledger = rendered_lines + skipped_lines

            # Check that story covers all manifest turns
            for expected_line in expected_ledger:
                if expected_line not in story_ledger:
                    errors.append(f"DIALOGUE TURN DROP in Scene {scene_id}: Line L{expected_line:04d} from manifest is not accounted for in story ledger.")

            # Check for illegal skips or reason violations
            # Check skipped items in footer have valid parenthesized reasons in skipped text
            skipped_raw_str = ledger_match.group(2)
            # Find any skipped indices that don't have (ooc) or (duplicate)
            # e.g. L0980(ooc) or 980(duplicate)
            # Let's check skipped list for tags without approved reasons
            skipped_items = re.findall(r"(\d+)(?:\(([^)]+)\))?", skipped_raw_str)
            for num_str, reason in skipped_items:
                if not reason or reason not in ["ooc", "duplicate"]:
                    errors.append(f"ILLEGAL SKIP REASON in Scene {scene_id}: Line L{int(num_str):04d} has unapproved skip reason: '{reason}'")

            # 6b. Compression ratio guardrail (prose word count vs raw dialogue word count)
            prose_words = len(s_block["content"].split())
            dialogue_words = calculate_dialogue_words(raw_lines, m_start, m_end)

            if dialogue_words > 0:
                ratio = prose_words / dialogue_words
                if ratio < 0.35:
                    warnings.append(f"COMPRESSION WARNING: Scene {scene_id} prose word count is {prose_words} vs {dialogue_words} raw dialogue words (ratio {ratio:.2f} < 0.35)")

    # 7. Whitelist header validation
    # Whitelist is '# Title' and '## Chapter Name'. Reject any '### Subscene' or other subheadings
    forbidden_headers = re.findall(r"^(###\s+.*)$", story_content, re.MULTILINE)
    if forbidden_headers:
        errors.append(f"HEADER FORMAT VIOLATION: Whitelist breach. Forbidden headers found: {forbidden_headers}")

    # Output report
    if errors:
        print("[FAIL] PARITY AUDIT FAILED:")
        for err in errors:
            print(f"  - {err}")
        if warnings:
            print("Warnings:")
            for warn in warnings:
                print(f"  - {warn}")
        sys.exit(1)
    else:
        print("[PASS] PARITY AUDIT PASSED: 100% transcript coverage and dialogue ledger fidelity confirmed.")
        if warnings:
            print("Warnings during pass:")
            for warn in warnings:
                print(f"  - {warn}")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python verify_parity.py <session_id> (e.g. s12)")
        sys.exit(1)
    verify_parity(sys.argv[1])
