import re
import os
import sys

def audit_completeness(clean_path, story_path):
    print(f"==================================================")
    print(f"[AUDIT] DEEP SCENE-BY-SCENE PARITY & AUDIT REPORT")
    print(f"==================================================")
    
    if not os.path.exists(clean_path):
        print(f"[ERROR] Clean file not found at {clean_path}")
        return
    if not os.path.exists(story_path):
        print(f"[ERROR] Story file not found at {story_path}")
        return

    with open(clean_path, 'r', encoding='utf-8') as f:
        clean_text = f.read()

    with open(story_path, 'r', encoding='utf-8') as f:
        story_text = f.read()

    # Extract all dialogue lines from s12-clean.md
    # Lines formatted like: **[[Speaker]] (PC/NPC):** "Dialogue..." or **Speaker:** "Dialogue..."
    dialogue_pattern = re.compile(r'\*\*(?:\[\[)?([^\]\:\*]+)(?:\]\])?\s*\((?:PC|NPC|Radio Broadcast)\)\:\*\*\s*["“]([^"”]+)["”]')
    clean_quotes = dialogue_pattern.findall(clean_text)

    print(f"\n[TOTAL] Spoken Dialogue Quotes in Clean Transcript: {len(clean_quotes)}")

    missing_quotes = []
    found_quotes = 0

    for speaker, quote in clean_quotes:
        quote_clean = quote.strip()
        # Split quote into sentences to handle dialogue split by speech tags
        sentences = [s.strip() for s in re.split(r'[\.\!\?]', quote_clean) if len(s.strip()) > 5]
        
        all_sentences_found = True
        for sentence in sentences:
            if sentence.lower() not in story_text.lower():
                all_sentences_found = False
                break

        if all_sentences_found and len(sentences) > 0:
            found_quotes += 1
        else:
            missing_quotes.append((speaker, quote))

    print(f"[MATCHED] Quotes in Story File: {found_quotes} / {len(clean_quotes)}")
    
    if missing_quotes:
        print(f"\n[MISSING] MISSING OR ALTERED DIALOGUE QUOTES ({len(missing_quotes)} items):")
        for idx, (spk, q) in enumerate(missing_quotes, 1):
            print(f"  {idx}. [{spk}]: \"{q}\"")
    else:
        print("[PASS] ALL DIALOGUE QUOTES ARE 100% PRESENT IN STORY FILE!")

    # Check key scene beats in clean transcript
    scenes_pattern = re.compile(r'### (Scene \d+\: [^\n]+)')
    scenes = scenes_pattern.findall(clean_text)
    print(f"\n[SCENES] Scene Structure Audit ({len(scenes)} scenes in clean transcript):")
    for s in scenes:
        print(f"  • {s}")

if __name__ == '__main__':
    clean_file = "sessions/data/clean/s12-clean.md"
    story_file = "sessions/data/clean/s12-clean-story.md"
    audit_completeness(clean_file, story_file)
