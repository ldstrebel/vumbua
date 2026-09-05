import re
import os
import sys

def grade_scene_cluster(clean_attributed_path, scene_block_paths, start_line, end_line):
    with open(clean_attributed_path, 'r', encoding='utf-8') as f:
        clean_text = f.read()

    # Parse clean attributed transcript in line range
    turns = []
    for block in clean_text.split('\n\n'):
        block = block.strip()
        if not block:
            continue
        m = re.match(r'^\*\*\[\[(.*?)\]\]\s*(.*?)\*\*\s*\[(.*?)\]:\s*(.*)', block, re.DOTALL)
        if m:
            spk, role, anchor, text = m.groups()
            if 'out of character' not in role:
                # check anchor range
                anch_nums = [int(x) for x in re.findall(r'L(\d+)', anchor)]
                if anch_nums:
                    if any(start_line <= n <= end_line for n in anch_nums):
                        turns.append({'speaker': spk, 'role': role, 'anchor': anchor, 'text': text.strip()})

    # Read combined scene block text
    combined_story = ""
    for p in scene_block_paths:
        with open(p, 'r', encoding='utf-8') as f:
            combined_story += f.read() + "\n\n"

    # 1. Check for forbidden italicized embedded dialogue patterns
    # Pattern: *Dialogue fragment,* character said or *fragment* —
    italic_dialogue_matches = re.findall(r'\*([A-Z][^\*\n]{3,}?[,\.\?!])\*\s*(?:said|whispered|screamed|gasped|cried|yelled|murmured|replied|—)', combined_story)
    embedded_dialogue_penalty = len(italic_dialogue_matches) * 10

    # 2. Check for entity name spelling errors
    mispellings = {
        'Real': 'Rill',
        'Professor Inc': 'Professor Ink',
        'Professor Inc.': 'Professor Ink',
        'Lazizi': 'Mizizi',
        'Lassi Zizi': 'Mizizi',
        'Brian Nagy': 'Britt and Aggie',
        'Kim': 'Pip',
    }
    found_misspellings = []
    for bad, good in mispellings.items():
        if re.search(r'\b' + re.escape(bad) + r'\b', combined_story):
            found_misspellings.append((bad, good))
    spelling_penalty = len(found_misspellings) * 5

    # 3. Check line anchor coverage
    referenced_lines = set([int(x) for x in re.findall(r'<!--\s*L(\d+)\s*-->', combined_story)])
    expected_line_coverage = 0
    covered_turns = []
    uncovered_turns = []

    story_lower = combined_story.lower()
    for t in turns:
        # Check text presence
        words = re.findall(r'\b\w{4,}\b', t['text'].lower())
        found = False
        if len(words) >= 2:
            for i in range(len(words)-1):
                pair = words[i] + " " + words[i+1]
                if pair in story_lower:
                    found = True
                    break
        elif len(words) == 1:
            if words[0] in story_lower:
                found = True
        else:
            found = True

        if found:
            covered_turns.append(t)
        else:
            uncovered_turns.append(t)

    coverage_rate = len(covered_turns) / len(turns) if turns else 1.0
    coverage_score = coverage_rate * 70.0 # 70 max pts for coverage

    # 4. Standard Dialogue Formatting (30 max pts)
    dialogue_quotes = re.findall(r'"([^"\n]{4,})"', combined_story)
    dialogue_score = 30.0 if len(dialogue_quotes) >= max(5, len(turns) * 0.4) else (len(dialogue_quotes) / (len(turns)*0.4)) * 30.0

    total_score = max(0, min(100, (coverage_score + dialogue_score) - embedded_dialogue_penalty - spelling_penalty))

    return {
        'total_score': total_score,
        'turns_count': len(turns),
        'covered_count': len(covered_turns),
        'uncovered_count': len(uncovered_turns),
        'coverage_rate': coverage_rate,
        'dialogue_quotes_count': len(dialogue_quotes),
        'italic_dialogue_penalties': len(italic_dialogue_matches),
        'found_misspellings': found_misspellings,
        'uncovered_turns': uncovered_turns,
        'sample_quotes': dialogue_quotes[:5] if dialogue_quotes else []
    }

if __name__ == '__main__':
    # test on Scene 18
    res = grade_scene_cluster(
        'sessions/data/clean/s12-clean-attributed.md',
        ['sessions/data/clean/blocks/s12-scene-18.md'],
        1601, 1650
    )
    print("Test result for Scene 18:", res)
