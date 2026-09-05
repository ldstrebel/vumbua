import json
import os
import re

def reconcile():
    base_dir = "sessions"
    manifest_path = os.path.join(base_dir, "transcripts", "index", "s6-manifest.json")
    blocks_dir = os.path.join(base_dir, "transcripts", "clean", "blocks")

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    for block in manifest.get("scene_blocks", []):
        scene_id = block["scene_id"]
        if block.get("ooc", False):
            continue

        block_path = os.path.join(blocks_dir, f"s6-scene-{scene_id:02d}.md")
        if not os.path.exists(block_path):
            print(f"Scene {scene_id}: file missing {block_path}")
            continue

        with open(block_path, "r", encoding="utf-8") as bf:
            content = bf.read()

        expected_lines = [turn["line"] for turn in block.get("dialogue_ledger", [])]
        expected_set = set(expected_lines)

        content_no_ledger = re.sub(r"<!--\s*LEDGER:.*?-->", "", content, flags=re.DOTALL).strip()
        marker_re = re.compile(r"<!--\s*L(\d+)\s*-->")

        paragraphs = content_no_ledger.split("\n\n")
        new_paras = []
        seen_markers = set()
        last_marker_val = 0
        all_rendered_markers = []

        for para in paragraphs:
            para_markers = [int(m) for m in marker_re.findall(para)]
            clean_para = marker_re.sub("", para).strip()
            clean_para = re.sub(r"\s+([.,!?;])", r"\1", clean_para)
            clean_para = re.sub(r"\s{2,}", " ", clean_para)

            cur_para_markers = []
            for m in para_markers:
                if m in expected_set and m not in seen_markers and m > last_marker_val:
                    cur_para_markers.append(m)
                    seen_markers.add(m)
                    last_marker_val = m
                    all_rendered_markers.append(m)

            if cur_para_markers:
                tag_str = " ".join([f"<!-- L{m:04d} -->" for m in cur_para_markers])
                new_paras.append(f"{clean_para} {tag_str}")
            else:
                new_paras.append(clean_para)

        rebuilt_content = "\n\n".join(new_paras)

        rendered_sorted = sorted(list(seen_markers))
        skipped_sorted = [l for l in expected_lines if l not in seen_markers]

        rendered_str = ", ".join(str(l) for l in rendered_sorted)
        skipped_str = ", ".join(f"{l}(ooc)" for l in skipped_sorted)
        footer = f"\n\n<!-- LEDGER: rendered=[{rendered_str}] skipped=[{skipped_str}] -->\n"

        final_content = rebuilt_content + footer
        with open(block_path, "w", encoding="utf-8") as bf:
            bf.write(final_content)

        print(f"Scene {scene_id:02d}: {len(rendered_sorted)} rendered, {len(skipped_sorted)} skipped.")

if __name__ == "__main__":
    reconcile()
