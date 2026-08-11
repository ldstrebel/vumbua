import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def detect_quote_speaker(pre_tag, post_tag, speakers, last_speaking_character):
    dialogue_verbs = r'(?:said|asked|screamed|replied|gasped|yelled|announced|noted|shouted|exclaimed|muttered|offered|shrugged|grunted|grinned|whispered|recalled|snarled|hissed|roared|cried|spat|mused|complained|corrected|warned|countered|admitted|laughed|groaned|sighed|breathed|confirmed|interrupted|finished|added|continued|insisted|pleaded|stated|declared|demanded|urged|agreed|protested|objected|called|bellowed|chortled|chimed|snickered|exulted|whimpered|scolded|grumbled|mumbled|rasped|quipped|sputtered|retorted|gushed|beamed|barked|snapped|howled|chirped)'

    is_323 = "My headdd" in post_tag or "carry Pip down" in pre_tag

    # 1a. Check pre_tag for immediate speech verb
    pre_verbs = list(re.finditer(dialogue_verbs, pre_tag, re.IGNORECASE))
    if pre_verbs:
        last_verb = pre_verbs[-1]
        dist_to_quote = len(pre_tag) - last_verb.end()
        if is_323:
            print(f"DEBUG pre_verb found: '{last_verb.group(0)}' at dist_to_quote {dist_to_quote}")
        if dist_to_quote <= 35:
            closest_spk = None
            min_dist = float('inf')
            for spk in speakers:
                for m in re.finditer(r'\b' + spk + r'\b', pre_tag, re.IGNORECASE):
                    dist = abs(last_verb.start() - m.start())
                    if dist < min_dist:
                        min_dist = dist
                        closest_spk = spk
            m_natty = list(re.finditer(r'\bNatty\b', pre_tag, re.IGNORECASE))
            for m in m_natty:
                dist = abs(last_verb.start() - m.start())
                if dist < min_dist:
                    min_dist = dist
                    closest_spk = "Ignatious"
            if is_323:
                print(f"DEBUG pre_verb closest_spk={closest_spk}, min_dist={min_dist}")
            if closest_spk and min_dist <= 45:
                if is_323:
                    print(f"DEBUG Step 1a returned {closest_spk}")
                return closest_spk

    # 1b. Check post_tag for immediate speech verb
    post_verbs = list(re.finditer(dialogue_verbs, post_tag, re.IGNORECASE))
    if post_verbs:
        first_verb = post_verbs[0]
        if is_323:
            print(f"DEBUG post_verb found: '{first_verb.group(0)}' at pos {first_verb.start()}")
        if first_verb.start() <= 35:
            closest_spk = None
            min_dist = float('inf')
            for spk in speakers:
                for m in re.finditer(r'\b' + spk + r'\b', post_tag[:first_verb.end() + 25], re.IGNORECASE):
                    dist = abs(first_verb.start() - m.start())
                    if dist < min_dist:
                        min_dist = dist
                        closest_spk = spk
            m_natty = list(re.finditer(r'\bNatty\b', post_tag[:first_verb.end() + 25], re.IGNORECASE))
            for m in m_natty:
                dist = abs(first_verb.start() - m.start())
                if dist < min_dist:
                    min_dist = dist
                    closest_spk = "Ignatious"
            if is_323:
                print(f"DEBUG post_verb closest_spk={closest_spk}, min_dist={min_dist}")
            if closest_spk and min_dist <= 30:
                if is_323:
                    print(f"DEBUG Step 1b returned {closest_spk}")
                return closest_spk

    # 2. PROXIMITY MATCHING
    candidates = []
    pre_len = len(pre_tag)
    for spk in speakers:
        for m in re.finditer(r'\b' + spk + r'\b', pre_tag, re.IGNORECASE):
            dist = pre_len - m.end()
            candidates.append((dist, spk))
        for m in re.finditer(r'\b' + spk + r'\b', post_tag, re.IGNORECASE):
            dist = m.start()
            candidates.append((dist, spk))

    m_natty_pre = list(re.finditer(r'\bNatty\b', pre_tag, re.IGNORECASE))
    for m in m_natty_pre:
        candidates.append((pre_len - m.end(), "Ignatious"))
    m_natty_post = list(re.finditer(r'\bNatty\b', post_tag, re.IGNORECASE))
    for m in m_natty_post:
        candidates.append((m.start(), "Ignatious"))

    if candidates:
        candidates.sort(key=lambda x: x[0])
        if is_323:
            print(f"DEBUG Step 2 returned {candidates[0][1]}")
        return candidates[0][1]

    # 3. PRONOUN TRACKING
    combined_tag = pre_tag + " " + post_tag
    if re.search(r'\b(he|his|him)\b', combined_tag, re.IGNORECASE) and last_speaking_character in ["Loami", "Ignatious", "Iggy"]:
        return last_speaking_character
    elif re.search(r'\b(she|her)\b', combined_tag, re.IGNORECASE) and last_speaking_character in ["Britt", "Aggie", "Pip"]:
        return last_speaking_character

    # 4. FALLBACK
    return last_speaking_character if last_speaking_character else "Loami"

def parse_story_into_blocks(story_path):
    with open(story_path, "r", encoding="utf-8") as f:
        text = f.read()

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2]

    lines = text.splitlines()
    current_chapter = "CHAPTER 1: THE NIGHT OF EMBERS"
    blocks = []
    speakers = ["Loami", "Pip", "Ignatious", "Britt", "Aggie", "Iggy", "Bramble"]
    last_speaking_character = None

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("---") or line.startswith("title:") or line.startswith("author:") or line.startswith("campaign:") or line.startswith("genre:"):
            continue

        if line.startswith("# ") and not line.startswith("## "):
            continue

        if line.startswith("## CHAPTER"):
            current_chapter = line.replace("##", "").strip()
            continue

        if line.startswith("#"):
            continue

        match_quotes = list(re.finditer(r'"([^"]+)"', line))
        if not match_quotes:
            blocks.append({
                "line_num": line_num,
                "chapter": current_chapter,
                "speaker": "Narrator",
                "text": line
            })
            continue

        curr_idx = 0
        for idx, match in enumerate(match_quotes):
            start, end = match.span()
            pre_tag = line[curr_idx:start]
            post_tag = line[end:match_quotes[idx+1].start()] if idx + 1 < len(match_quotes) else line[end:]

            detected_speaker = detect_quote_speaker(pre_tag, post_tag, speakers, last_speaking_character)
            last_speaking_character = detected_speaker

            # Narration before quote
            if start > curr_idx:
                narr_text = line[curr_idx:start].strip()
                if narr_text.strip(" *_\t\n"):
                    blocks.append({
                        "line_num": line_num,
                        "chapter": current_chapter,
                        "speaker": "Narrator",
                        "text": narr_text
                    })

            # Quote segment
            quote_text = f'"{match.group(1).strip()}"'
            blocks.append({
                "line_num": line_num,
                "chapter": current_chapter,
                "speaker": detected_speaker,
                "text": quote_text
            })
            curr_idx = end

        # Trailing narration
        if curr_idx < len(line):
            narr_text = line[curr_idx:].strip()
            if narr_text.strip(" *_\t\n"):
                blocks.append({
                    "line_num": line_num,
                    "chapter": current_chapter,
                    "speaker": "Narrator",
                    "text": narr_text
                })

    return blocks

if __name__ == "__main__":
    blocks = parse_story_into_blocks("sessions/transcripts/clean/s11-clean-story.md")
    print("\n--- SPECIFIC CHECK FOR LINE 323 ---")
    for b in blocks:
        if b["line_num"] == 323:
            print(f"L323 | [{b['speaker']:<10}] : {b['text']}")
