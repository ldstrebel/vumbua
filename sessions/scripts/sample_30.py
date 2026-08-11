import random
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from generate_audiobook import parse_story_into_blocks

def main():
    random.seed(42)
    story_path = "sessions/transcripts/clean/s11-clean-story.md"
    blocks = parse_story_into_blocks(story_path)

    # Group blocks by line number
    line_map = {}
    for b in blocks:
        l = b["line_num"]
        if l not in line_map:
            line_map[l] = []
        line_map[l].append(b)

    unique_lines = sorted(line_map.keys())
    sample_lines = sorted(random.sample(unique_lines, 30))

    print(f"Total unique lines sampled: {len(sample_lines)} (from {len(blocks)} total audio blocks)\n")

    for i, line_num in enumerate(sample_lines, 1):
        line_blocks = line_map[line_num]
        ch = line_blocks[0]["chapter"].replace("## ", "")
        print(f"{'='*100}")
        print(f"SAMPLE #{i:02d} | Line {line_num} ({ch}) | Sub-blocks: {len(line_blocks)}")
        print(f"{'='*100}")
        for sub_i, b in enumerate(line_blocks, 1):
            spk = f"[{b['speaker']}]"
            print(f"  Sub-block {sub_i}: {spk:<14} -> {b['text']}")
        print()

if __name__ == "__main__":
    main()
