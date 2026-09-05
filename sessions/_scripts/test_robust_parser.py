#!/usr/bin/env python3
import re
import json
from pathlib import Path

def test_robust_parser():
    story_path = Path("sessions/data/clean/s11-clean-story.md")
    with open(story_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    speakers = ["Loami", "Pip", "Ignatious", "Britt", "Aggie", "Iggy", "Bramble"]
    
    blocks = []
    current_chapter = "Prologue"
    last_speaking_character = None

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("---") or line.startswith("# Session") or line.startswith("title:") or line.startswith("author:") or line.startswith("campaign:") or line.startswith("genre:"):
            continue

        if line.startswith("## CHAPTER"):
            current_chapter = line.replace("##", "").strip()
            continue

        match_quotes = list(re.finditer(r'"([^"]+)"', line))

        if not match_quotes:
            # Pure narration block
            blocks.append({
                "line_num": line_num,
                "chapter": current_chapter,
                "speaker": "Narrator",
                "text": line
            })
            continue

        # Keep dialogue paragraphs smooth by attributing the full line to the character if it contains dialogue!
        narration_text = re.sub(r'"[^"]+"', '', line).strip()
        
        detected_speaker = None
        
        dialogue_verbs = r'(?:said|asked|screamed|replied|gasped|yelled|announced|noted|shouted|exclaimed|muttered|offered|shrugged|grunted|grinned|whispered|recalled|snarled|hissed|roared|cried|spat|mused|complained|corrected|warned|countered|admitted|laughed|groaned|sighed|breathed|confirmed|interrupted|finished|added|continued|insisted|pleaded|stated|declared|demanded|urged|agreed|protested|objected|called|bellowed|chortled|chimed|snickered)'

        # 1. PRIMARY: NAME immediately followed by a speech verb within 5 chars (e.g. 'Aggie gasped', 'Loami said,')
        for spk in speakers:
            if re.search(r'\b' + spk + r'\b.{0,5}\b' + dialogue_verbs + r'\b', narration_text, re.IGNORECASE):
                detected_speaker = spk
                break

        if not detected_speaker and re.search(r'\bNatty\b.{0,5}\b' + dialogue_verbs + r'\b', narration_text, re.IGNORECASE):
            detected_speaker = "Ignatious"

        # 2. SECONDARY: Find earliest occurring character name in narration tag (by string position)
        if not detected_speaker:
            name_positions = []
            for spk in speakers:
                m = re.search(r'\b' + spk + r'\b', narration_text, re.IGNORECASE)
                if m:
                    name_positions.append((m.start(), spk))
            m_natty = re.search(r'\bNatty\b', narration_text, re.IGNORECASE)
            if m_natty:
                name_positions.append((m_natty.start(), "Ignatious"))
            
            if name_positions:
                name_positions.sort(key=lambda x: x[0])
                detected_speaker = name_positions[0][1]

        # 3. Check pronouns in narration tag
        if not detected_speaker:
            if re.search(r'\b(he|his|him)\b', narration_text, re.IGNORECASE) and last_speaking_character in ["Loami", "Ignatious", "Iggy"]:
                detected_speaker = last_speaking_character
            elif re.search(r'\b(she|her)\b', narration_text, re.IGNORECASE) and last_speaking_character in ["Britt", "Aggie", "Pip"]:
                detected_speaker = last_speaking_character

        # 4. Fallback
        if not detected_speaker:
            detected_speaker = last_speaking_character if last_speaking_character else "Loami"

        last_speaking_character = detected_speaker

        # Tokenize line into sequential narration (Narrator) and quote (character) blocks
        curr_idx = 0
        for match in match_quotes:
            start, end = match.span()
            # Narration before quote
            if start > curr_idx:
                narr_text = line[curr_idx:start].strip()
                if narr_text:
                    blocks.append({
                        "line_num": line_num,
                        "chapter": current_chapter,
                        "speaker": "Narrator",
                        "text": narr_text
                    })
            
            # Quote segment assigned to detected character voice
            quote_text = f'"{match.group(1).strip()}"'
            blocks.append({
                "line_num": line_num,
                "chapter": current_chapter,
                "speaker": detected_speaker,
                "text": quote_text
            })
            curr_idx = end

        # Trailing narration after last quote
        if curr_idx < len(line):
            narr_text = line[curr_idx:].strip()
            if narr_text:
                blocks.append({
                    "line_num": line_num,
                    "chapter": current_chapter,
                    "speaker": "Narrator",
                    "text": narr_text
                })

    print("\n--- SPECIFIC CHECK FOR LINE 89 (THE USER SCREENSHOT ISSUE) ---")
    for b in blocks:
        if "speed you up" in b["text"] or "Channeling his hearthfire" in b["text"] or "Try again" in b["text"]:
            print(f"L{b['line_num']:<3} | [{b['speaker']:<10}] in {b['chapter'][:20]:<20}: \"{b['text']}\"")

if __name__ == "__main__":
    test_robust_parser()
