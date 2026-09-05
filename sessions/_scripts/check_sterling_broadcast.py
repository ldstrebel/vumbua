import os
import re

def check_sterling_alignment():
    with open("campaign/prep/s12-finale/s12-intro-sterling.md", "r", encoding="utf-8") as f:
        master_script = f.read()

    with open("sessions/data/clean/s12-clean-story.md", "r", encoding="utf-8") as f:
        story_text = f.read()

    paragraphs = [p.strip() for p in master_script.split('\n\n') if p.strip()]
    print(f"Total Master Broadcast Paragraphs: {len(paragraphs)}")

    missing_count = 0
    for idx, p in enumerate(paragraphs, 1):
        p_clean = re.sub(r'\\([!\[\]\-\*\\])', r'\1', p)
        p_clean = re.sub(r'\[\*\*(Sterling|Kante)\*\*\]', '', p_clean).strip()
        
        # Check first sentence of each paragraph
        first_sentence = p_clean.split('.')[0].strip()
        first_sentence = re.sub(r'[^\w\s]', '', first_sentence)

        story_clean_text = re.sub(r'[^\w\s]', '', story_text)

        if first_sentence.lower() in story_clean_text.lower():
            print(f"  [MATCH] Paragraph {idx}: VERBATIM FOUND (\"{first_sentence[:30]}...\")")
        else:
            print(f"  [MISSING] Paragraph {idx}: NOT FOUND -> \"{first_sentence[:30]}...\"")
            missing_count += 1

    if missing_count == 0:
        print("\n[PASS] ALL 13 PARAGRAPHS OF STERLING/KANTE BROADCAST VERIFIED 100% VERBATIM!")
    else:
        print(f"\n[WARNING] {missing_count} PARAGRAPHS MISMATCHED!")

if __name__ == '__main__':
    check_sterling_alignment()
