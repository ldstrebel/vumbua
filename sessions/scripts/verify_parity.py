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

    # 4. Read story content from intermediate block files in blocks_dir
    blocks_dir = os.path.join(base_dir, "transcripts", "clean", "blocks")
    parts = []
    for b in manifest.get("scene_blocks", []):
        scene_id = b["scene_id"]
        start, end = b["line_range"]
        if b.get("ooc", False):
            parts.append(f"<!-- RAW_RANGE: [{start}, {end}] | SCENE_ID: {scene_id} | OOC -->\n")
        else:
            b_path = os.path.join(blocks_dir, f"{session_id}-scene-{scene_id:02d}.md")
            if os.path.exists(b_path):
                with open(b_path, "r", encoding="utf-8") as bf:
                    parts.append(bf.read().strip() + "\n")
    story_content = "\n".join(parts)

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

            # Footer partition contract: rendered and skipped must be disjoint,
            # and their union must equal the manifest ledger exactly.
            double_counted = set(rendered_lines) & set(skipped_lines)
            if double_counted:
                errors.append(f"LEDGER PARTITION VIOLATION in Scene {scene_id}: lines listed as both rendered and skipped: {sorted(double_counted)}")

            story_ledger = set(rendered_lines) | set(skipped_lines)
            for expected_line in expected_ledger:
                if expected_line not in story_ledger:
                    errors.append(f"DIALOGUE TURN DROP in Scene {scene_id}: Line L{expected_line:04d} from manifest is not accounted for in story ledger.")
            phantom = story_ledger - set(expected_ledger)
            if phantom:
                errors.append(f"PHANTOM LEDGER ENTRIES in Scene {scene_id}: footer lists lines not in manifest dialogue ledger: {sorted(phantom)}")

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

            # 6a-2. Inline spoken-turn marker gate (dialogue ordering)
            # Every dialogue paragraph must END with <!-- Lxxxx --> marker(s).
            # Strip the ledger footer first so it can't be picked up.
            content_no_ledger = re.sub(
                r"<!--\s*LEDGER:.*?-->", "", s_block["content"], flags=re.DOTALL
            )
            marker_re = re.compile(r"<!--\s*L(\d+)\s*-->")

            # Walk paragraphs in document order so ordering reflects the prose.
            inline_markers = []
            for para in content_no_ledger.split("\n\n"):
                para = para.strip()
                if not para:
                    continue
                para_markers = [int(x) for x in marker_re.findall(para)]
                if not para_markers:
                    continue
                # Markers must form a trailing cluster at paragraph end —
                # a marker buried mid-paragraph can't be position-audited.
                tail = para
                trailing = 0
                while True:
                    m = re.search(r"<!--\s*L\d+\s*-->\s*$", tail)
                    if not m:
                        break
                    trailing += 1
                    tail = tail[: m.start()].rstrip()
                if trailing != len(para_markers):
                    errors.append(f"MID-PARAGRAPH MARKER in Scene {scene_id}: markers must be a trailing cluster at paragraph end (found {len(para_markers)} markers, only {trailing} trailing): '{para[:60]}...'")
                if len(para_markers) > 3:
                    warnings.append(f"MARKER PILE-UP in Scene {scene_id}: one paragraph carries {len(para_markers)} turn markers — verify these turns are genuinely fused: '{para[:60]}...'")
                inline_markers.extend(para_markers)

            # The footer's rendered list is the authoritative expectation
            # (it has already been reconciled against the manifest above).
            expected_rendered = rendered_lines

            if expected_rendered and not inline_markers:
                errors.append(
                    f"MISSING INLINE MARKERS in Scene {scene_id}: manifest expects "
                    f"{len(expected_rendered)} rendered dialogue turns but the prose "
                    f"contains no <!-- Lxxxx --> markers."
                )
            else:
                # Strict ascending order = prose follows transcript chronology
                for i in range(len(inline_markers) - 1):
                    if inline_markers[i] >= inline_markers[i + 1]:
                        errors.append(
                            f"DIALOGUE ORDER VIOLATION in Scene {scene_id}: "
                            f"L{inline_markers[i]:04d} appears in prose before "
                            f"L{inline_markers[i + 1]:04d} (raw order is reversed or duplicated)."
                        )

                # Set equivalence with the manifest's rendered turns
                missing = set(expected_rendered) - set(inline_markers)
                extra = set(inline_markers) - set(expected_rendered)
                if missing:
                    errors.append(
                        f"INLINE MARKER GAP in Scene {scene_id}: rendered turns missing "
                        f"markers in prose: {sorted(missing)}"
                    )
                if extra:
                    errors.append(
                        f"INLINE MARKER EXCESS in Scene {scene_id}: prose markers not in "
                        f"manifest rendered set: {sorted(extra)}"
                    )

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
