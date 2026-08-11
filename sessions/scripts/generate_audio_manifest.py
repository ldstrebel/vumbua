#!/usr/bin/env python3
"""
Vumbua LLM Audio Manifest Generator
-----------------------------------
Parses novelized session story files (e.g. s11-clean-story.md) and generates a 100%
verbatim Audio Manifest JSON with character-specific accent & phonetic tts_text tuning.

Usage:
  python sessions/scripts/generate_audio_manifest.py \
    --story sessions/transcripts/clean/s11-clean-story.md \
    --transcript sessions/transcripts/clean/s11-clean.md \
    --output sessions/audio/s11/s11_audio_manifest.json
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

VALID_SPEAKERS = ["Narrator", "Loami", "Pip", "Ignatious", "Britt", "Aggie", "Iggy", "Bramble"]

# Global proper noun and fantasy term phonetic dictionary
GLOBAL_PHONETIC_MAP = {
    "Mwaza-Kasa": "Mwahzah Kahsah",
    "Mwaza-Chui": "Mwahzah Cheewee",
    "Mizizi": "Meezeezee",
    "Lazizi": "Lahzeezee",
    "Cazito": "Kahzeetoh",
    "coyobi": "coy-oh-bee",
    "Coyobi": "Coy-oh-bee",
    "Aether": "Ether",
    "aether": "ether",
    "Meowders": "Meow-ders",
}

def apply_phonetics(text, speaker):
    """
    Generates TTS-optimized phonetic text for ElevenLabs speech synthesis
    for fantasy terms and proper nouns without altering character voice models.
    """
    tts_text = text

    # Apply Global Fantasy & Proper Noun Phonetics
    for word, phonetic in GLOBAL_PHONETIC_MAP.items():
        pattern = r'(?<![A-Za-z0-9])' + re.escape(word) + r'(?![A-Za-z0-9])'
        tts_text = re.sub(pattern, phonetic, tts_text)

    return tts_text


def detect_quote_speaker(pre_tag, post_tag, speakers, last_speaking_character):
    dialogue_verbs = r'(?:said|asked|screamed|replied|gasped|yelled|announced|noted|shouted|exclaimed|muttered|offered|shrugged|grunted|grinned|whispered|recalled|snarled|hissed|roared|cried|spat|mused|complained|corrected|warned|countered|admitted|laughed|groaned|sighed|breathed|confirmed|interrupted|finished|added|continued|insisted|pleaded|stated|declared|demanded|urged|agreed|protested|objected|called|bellowed|chortled|chimed|snickered|exulted|whimpered|scolded|grumbled|mumbled|rasped|quipped|sputtered|retorted|gushed|beamed|barked|snapped|howled|chirped)'

    # 1a. Check pre_tag for immediate speech verb
    pre_verbs = list(re.finditer(dialogue_verbs, pre_tag, re.IGNORECASE))
    if pre_verbs:
        last_verb = pre_verbs[-1]
        dist_to_quote = len(pre_tag) - last_verb.end()
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
            if closest_spk and min_dist <= 45:
                return closest_spk

    # 1b. Check post_tag for immediate speech verb
    post_verbs = list(re.finditer(dialogue_verbs, post_tag, re.IGNORECASE))
    if post_verbs:
        first_verb = post_verbs[0]
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
            if closest_spk and min_dist <= 30:
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
        return candidates[0][1]

    # 3. PRONOUN TRACKING
    combined_tag = pre_tag + " " + post_tag
    if re.search(r'\b(he|his|him)\b', combined_tag, re.IGNORECASE) and last_speaking_character in ["Loami", "Ignatious", "Iggy"]:
        return last_speaking_character
    elif re.search(r'\b(she|her)\b', combined_tag, re.IGNORECASE) and last_speaking_character in ["Britt", "Aggie", "Pip"]:
        return last_speaking_character

    # 4. FALLBACK
    return last_speaking_character if last_speaking_character else "Loami"


def parse_line_into_manifest_blocks(line, line_num, current_chapter, quote_context, last_speaking_character):
    """
    Parses a single line of novelized story prose into sequential audio manifest blocks.
    Ensures 100% verbatim text preservation of the source line and generates phonetic tts_text.
    """
    match_quotes = list(re.finditer(r'"([^"]+)"', line))
    if not match_quotes:
        return [{
            "line_num": line_num,
            "chapter": current_chapter,
            "speaker": "Narrator",
            "text": line,
            "tts_text": apply_phonetics(line, "Narrator")
        }], last_speaking_character

    blocks = []
    curr_idx = 0

    for idx, match in enumerate(match_quotes):
        start, end = match.span()
        pre_tag = line[curr_idx:start]
        post_tag = line[end:match_quotes[idx+1].start()] if idx + 1 < len(match_quotes) else line[end:]

        detected_speaker = detect_quote_speaker(pre_tag, post_tag, VALID_SPEAKERS, last_speaking_character)
        last_speaking_character = detected_speaker

        # Emitting Narration before quote
        if start > curr_idx:
            narr_text = line[curr_idx:start]
            if narr_text:
                blocks.append({
                    "line_num": line_num,
                    "chapter": current_chapter,
                    "speaker": "Narrator",
                    "text": narr_text,
                    "tts_text": apply_phonetics(narr_text, "Narrator")
                })

        # Emitting Dialogue Quote (Exact slice with quotes)
        quote_text = line[start:end]
        blocks.append({
            "line_num": line_num,
            "chapter": current_chapter,
            "speaker": detected_speaker,
            "text": quote_text,
            "tts_text": apply_phonetics(quote_text, detected_speaker)
        })
        curr_idx = end

    # Emitting Trailing Narration after last quote
    if curr_idx < len(line):
        narr_text = line[curr_idx:]
        if narr_text:
            blocks.append({
                "line_num": line_num,
                "chapter": current_chapter,
                "speaker": "Narrator",
                "text": narr_text,
                "tts_text": apply_phonetics(narr_text, "Narrator")
            })

    return blocks, last_speaking_character


def generate_manifest(story_path, transcript_path, output_path):
    print(f"\n📖 Loading story file: {story_path}")
    with open(story_path, "r", encoding="utf-8") as f:
        text = f.read()

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2]

    lines = text.splitlines()
    current_chapter = "CHAPTER 1: THE NIGHT OF EMBERS"
    manifest_blocks = []
    block_id = 1
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

        line_blocks, last_speaking_character = parse_line_into_manifest_blocks(
            line, line_num, current_chapter, {}, last_speaking_character
        )

        for b in line_blocks:
            b["id"] = block_id
            block_id += 1
            manifest_blocks.append(b)

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(manifest_blocks, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully generated Audio Manifest JSON!")
    print(f"   • Total Blocks Extracted : {len(manifest_blocks)}")
    print(f"   • Output File            : {out_file.resolve()}\n")

    return manifest_blocks


def main():
    parser = argparse.ArgumentParser(description="Vumbua LLM Audio Manifest Generator")
    parser.add_argument("--story", required=True, help="Path to story markdown file (e.g. s11-clean-story.md)")
    parser.add_argument("--transcript", help="Path to clean transcript file (e.g. s11-clean.md) for ground-truth lookup")
    parser.add_argument("--output", required=True, help="Path to output manifest JSON file")

    args = parser.parse_args()
    generate_manifest(args.story, args.transcript, args.output)

if __name__ == "__main__":
    main()
