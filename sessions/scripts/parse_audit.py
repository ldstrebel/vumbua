#!/usr/bin/env python3
"""
Parse Audit Tool — Vumbua Audiobook Generator
Outputs a complete human-readable audit report of every audio block
the parser would generate, with the raw source line alongside it.
Zero API credits used.
"""
import re
import sys
from pathlib import Path

def parse_with_audit(story_path):
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
    warnings = []

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("---") or line.startswith("title:") or line.startswith("author:") or line.startswith("campaign:") or line.startswith("genre:"):
            continue

        if line.startswith("# ") and not line.startswith("## "):
            continue

        if line.startswith("## CHAPTER"):
            current_chapter = line.replace("##", "").strip()
            continue

def detect_quote_speaker_audit(pre_tag, post_tag, speakers, last_speaking_character):
    dialogue_verbs = r'(?:said|asked|screamed|replied|gasped|yelled|announced|noted|shouted|exclaimed|muttered|offered|shrugged|grunted|grinned|whispered|recalled|snarled|hissed|roared|cried|spat|mused|complained|corrected|warned|countered|admitted|laughed|groaned|sighed|breathed|confirmed|interrupted|finished|added|continued|insisted|pleaded|stated|declared|demanded|urged|agreed|protested|objected|called|bellowed|chortled|chimed|snickered|exulted|whimpered|scolded|grumbled|mumbled|rasped|quipped|sputtered|retorted|gushed|beamed|barked|snapped|howled|chirped)'

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
                return closest_spk, f"pre-quote verb '{last_verb.group(0)}' -> {closest_spk}"

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
                return closest_spk, f"post-quote verb '{first_verb.group(0)}' -> {closest_spk}"

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
        return candidates[0][1], f"proximity '{candidates[0][1]}' (dist {candidates[0][0]})"

    combined_tag = pre_tag + " " + post_tag
    if re.search(r'\b(he|his|him)\b', combined_tag, re.IGNORECASE) and last_speaking_character in ["Loami", "Ignatious", "Iggy"]:
        return last_speaking_character, f"pronoun 'he/his/him' -> {last_speaking_character}"
    elif re.search(r'\b(she|her)\b', combined_tag, re.IGNORECASE) and last_speaking_character in ["Britt", "Aggie", "Pip"]:
        return last_speaking_character, f"pronoun 'she/her' -> {last_speaking_character}"

    spk = last_speaking_character if last_speaking_character else "Loami"
    return spk, f"FALLBACK -> {spk}"


def parse_with_audit(story_path):
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
    warnings = []

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
                "text": line,
                "source": line,
                "method": "pure narration"
            })
            continue

        curr_idx = 0
        for idx, match in enumerate(match_quotes):
            start, end = match.span()
            pre_tag = line[curr_idx:start]
            post_tag = line[end:match_quotes[idx+1].start()] if idx + 1 < len(match_quotes) else line[end:]

            detected_speaker, method = detect_quote_speaker_audit(pre_tag, post_tag, speakers, last_speaking_character)
            if method.startswith("FALLBACK"):
                warnings.append({
                    "line_num": line_num,
                    "text": line[:80],
                    "assigned_to": detected_speaker,
                    "narration_tag": (pre_tag + " " + post_tag)[:60]
                })

            last_speaking_character = detected_speaker

            # Narration before quote
            if start > curr_idx:
                narr_text = line[curr_idx:start].strip()
                if narr_text.strip(" *_\t\n"):
                    blocks.append({
                        "line_num": line_num,
                        "chapter": current_chapter,
                        "speaker": "Narrator",
                        "text": narr_text,
                        "source": line,
                        "method": "narration segment"
                    })

            # Quote segment
            quote_text = f'"{match.group(1).strip()}"'
            blocks.append({
                "line_num": line_num,
                "chapter": current_chapter,
                "speaker": detected_speaker,
                "text": quote_text,
                "source": line,
                "method": method
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
                    "text": narr_text,
                    "source": line,
                    "method": "narration segment"
                })

    return blocks, warnings


def write_audit_report(blocks, warnings, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("=" * 100 + "\n")
        f.write("VUMBUA AUDIOBOOK PARSER AUDIT REPORT\n")
        f.write("Source: sessions/transcripts/clean/s11-clean-story.md\n")
        f.write(f"Total Blocks: {len(blocks)}\n")
        f.write(f"Warnings (fallback assignments): {len(warnings)}\n")
        f.write("=" * 100 + "\n\n")

        current_chapter = None
        for b in blocks:
            if b["chapter"] != current_chapter:
                current_chapter = b["chapter"]
                f.write(f"\n{'=' * 80}\n")
                f.write(f"  CHAPTER: {current_chapter}\n")
                f.write(f"{'=' * 80}\n\n")

            speaker_label = f"[{b['speaker'].upper():<10}]"
            method_note = f"  ({b['method']})"
            flag = " <<< FALLBACK WARNING" if b["method"].startswith("FALLBACK") else ""

            f.write(f"L{b['line_num']:<4} {speaker_label}{flag}\n")
            f.write(f"       Source  : {b['text'][:95]}\n")
            f.write(f"       Method  : {b['method']}\n")
            f.write("\n")

        if warnings:
            f.write("\n" + "=" * 100 + "\n")
            f.write("FALLBACK WARNINGS — PLEASE VERIFY THESE BLOCKS MANUALLY\n")
            f.write("=" * 100 + "\n")
            for w in warnings:
                f.write(f"\n  L{w['line_num']}: Assigned to [{w['assigned_to']}] via fallback\n")
                f.write(f"     Text      : {w['text']}\n")
                f.write(f"     Narr Tag  : '{w['narration_tag']}'\n")
        else:
            f.write("\n[OK] ZERO FALLBACK WARNINGS - All speakers explicitly detected!\n")


if __name__ == "__main__":
    story_path = "sessions/transcripts/clean/s11-clean-story.md"
    out_path = "sessions/scripts/parse_audit_report.txt"

    print(f"Running full parse audit on: {story_path}")
    blocks, warnings = parse_with_audit(story_path)
    write_audit_report(blocks, warnings, out_path)

    print(f"[OK] Parse audit complete!")
    print(f"     Total blocks : {len(blocks)}")
    print(f"     Warnings     : {len(warnings)} fallback assignment(s)")
    print(f"     Report saved : {out_path}")

    if warnings:
        print("\n[WARNINGS] Lines that used fallback speaker detection:")
        for w in warnings:
            print(f"  L{w['line_num']}: -> [{w['assigned_to']}] (narration tag: '{w['narration_tag']}')")
            print(f"     '{w['text']}'")
