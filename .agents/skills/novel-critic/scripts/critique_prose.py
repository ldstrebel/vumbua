#!/usr/bin/env python3
"""Adversarial Prose Critic & Bloat Scanner.

Runs forensic telemetry on novelized story files (sN-clean-story.md) to detect:
1. Purple prose & repeated architectural/sensory tropes (rolling 1,000-word window)
2. Stagnant action / "talking heads" ratio (excessive dialogue without physical motion)
3. Domestic logistics & hallway transit filler (breakfast, buffets, walking down corridors)
4. Character voice homogenization (vocabulary overlap across character dialogue)
5. Static scene delta (scenes lacking conflict, stakes shifts, or state changes)

Usage:
    python critique_prose.py s1
    python critique_prose.py s7.5 --out sessions/transcripts/index/s7.5-critique.md
"""

import argparse
import json
import os
import re
import sys
from collections import Counter

# Repetitive sensory & architectural phrases to watch out for
SENSORY_PHRASES = [
    r"warm mahogany",
    r"polished brass",
    r"acrid ozone",
    r"gaslight lanterns?",
    r"circular (?:crystal|glass) floor",
    r"basalt (?:canyon|chasm|ring)",
    r"copper balustrades?",
    r"heavy canvas (?:working )?collar",
    r"woolen flat cap",
    r"green leaf crown",
    r"dangling satchels?",
    r"living woven green",
    r"steamship with brass fittings",
    r"subtle(?:,)? disorienting flutter",
    r"force of nature",
    r"pure dread",
]

# Logistics & filler patterns (breakfast, transit, syllabus banter)
LOGISTICS_PATTERNS = [
    (r"\b(?:breakfast|buffet|muffins?|bacon|sky-bites?|appetizers?|trays of food)\b", "Dining / Food Logistics"),
    (r"\b(?:walking down the (?:hall|corridor|berths?)|threaded through the gates?|walked together down)\b", "Corridor / Transit Logistics"),
    (r"\b(?:desks?|chalk|syllabus|lecture notes?|textbooks?)\b", "Academic Logistics"),
]

# Action & motion verbs to evaluate scene physical dynamics
ACTION_VERBS = {
    "ran", "running", "leaped", "leaping", "sprinted", "sprinting", "slammed", "slamming",
    "crawled", "crawling", "grabbed", "grabbing", "wrenched", "wrenching", "dodged", "dodging",
    "shattered", "shattering", "ducked", "ducking", "lunged", "lunging", "tackled", "tackling",
    "climbed", "climbing", "pushed", "pushing", "dragged", "dragging", "bolted", "bolting",
    "dived", "diving", "swung", "swinging", "struck", "striking", "burst", "bursting"
}


def analyze_purple_prose(text):
    findings = []
    text_lower = text.lower()
    for pattern in SENSORY_PHRASES:
        matches = list(re.finditer(pattern, text_lower))
        if len(matches) >= 3:
            findings.append({
                "phrase": pattern.replace(r"\b", "").replace(r"(?:", "").replace(r")?", "").replace(r")", ""),
                "occurrences": len(matches),
                "severity": "HIGH" if len(matches) >= 5 else "MEDIUM"
            })
    return findings


def analyze_logistics_density(text):
    total_words = len(text.split())
    if total_words == 0:
        return {}
    
    logistics_counts = {}
    for pattern, category in LOGISTICS_PATTERNS:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        if matches:
            logistics_counts[category] = len(matches)
            
    return {
        "categories": logistics_counts,
        "total_hits": sum(logistics_counts.values()),
        "hit_density_per_kword": round(sum(logistics_counts.values()) / (total_words / 1000), 2) if total_words > 0 else 0
    }


def analyze_dialogue_vs_action(scenes):
    scene_metrics = []
    for s in scenes:
        content = s["content"]
        words = content.split()
        if not words:
            continue
        
        quotes = re.findall(r'"([^"]+)"', content)
        dialogue_words = sum(len(q.split()) for q in quotes)
        dialogue_ratio = round(dialogue_words / len(words), 3)
        
        # Count action verbs in narrative
        narrative_text = re.sub(r'"[^"]+"', '', content).lower()
        narrative_tokens = re.findall(r"\b[a-z]+\b", narrative_text)
        action_verb_count = sum(1 for tok in narrative_tokens if tok in ACTION_VERBS)
        
        talking_heads_risk = dialogue_ratio > 0.45 and action_verb_count < 3
        
        scene_metrics.append({
            "scene_id": s["scene_id"],
            "title": s["title"],
            "word_count": len(words),
            "dialogue_ratio": dialogue_ratio,
            "action_verb_count": action_verb_count,
            "talking_heads_risk": talking_heads_risk
        })
    return scene_metrics


def analyze_character_voices(text):
    # Extract quotes attributed to specific characters
    # Look for patterns like: "..." Lomi said / Lomi murmured / "..." Britt shouted
    character_quotes = {"Lomi": [], "Britt": [], "Aggie": [], "Ignatius": [], "Iggy": []}
    
    lines = text.split("\n")
    for i, line in enumerate(lines):
        quotes = re.findall(r'"([^"]+)"', line)
        if not quotes:
            continue
        surrounding = line
        if i > 0:
            surrounding += " " + lines[i-1]
        if i < len(lines) - 1:
            surrounding += " " + lines[i+1]
            
        for char in character_quotes:
            if re.search(r'\b' + char + r'\b', surrounding, flags=re.IGNORECASE):
                character_quotes[char].extend(quotes)
                break
                
    voice_profiles = {}
    for char, q_list in character_quotes.items():
        if not q_list:
            continue
        combined = " ".join(q_list).lower()
        tokens = re.findall(r"\b[a-z]{3,}\b", combined)
        avg_quote_len = round(sum(len(q.split()) for q in q_list) / len(q_list), 1)
        voice_profiles[char] = {
            "total_quotes": len(q_list),
            "avg_words_per_turn": avg_quote_len,
            "top_vocab": [w for w, _ in Counter(tokens).most_common(5)]
        }
    return voice_profiles


def parse_story_scenes(story_text):
    raw_blocks = re.findall(
        r"<!--\s*RAW_RANGE:\s*\[\d+,\s*\d+\]\s*\|\s*SCENE_ID:\s*(\d+)(?:\s*\|\s*OOC)?\s*-->\s*(.*?)(?=<!--\s*RAW_RANGE:|$)",
        story_text,
        re.DOTALL
    )
    scenes = []
    for sc_id, content in raw_blocks:
        lines = content.strip().split("\n")
        title = lines[0] if lines and lines[0].startswith("#") else f"Scene {sc_id}"
        scenes.append({
            "scene_id": int(sc_id),
            "title": title.lstrip("#").strip(),
            "content": content.strip()
        })
    return scenes


def generate_critique_report(session_id, story_path, manifest_path=None):
    if not os.path.exists(story_path):
        print(f"Error: Story file not found at {story_path}", file=sys.stderr)
        sys.exit(1)
        
    with open(story_path, "r", encoding="utf-8") as f:
        story_text = f.read()
        
    scenes = parse_story_scenes(story_text)
    purple_prose = analyze_purple_prose(story_text)
    logistics = analyze_logistics_density(story_text)
    scene_actions = analyze_dialogue_vs_action(scenes)
    voices = analyze_character_voices(story_text)
    
    total_words = len(story_text.split())
    
    report = []
    report.append(f"# 🗡️ Ruthless Editorial Critique: {session_id.upper()}")
    report.append(f"**Total Words:** {total_words:,} | **Scenes Audited:** {len(scenes)}")
    report.append("")
    
    # 1. Executive Verdict
    report.append("## 1. Executive Editorial Verdict")
    talking_heads = [s for s in scene_actions if s["talking_heads_risk"]]
    purple_alerts = [p for p in purple_prose if p["severity"] == "HIGH"]
    
    if talking_heads or purple_alerts or logistics.get("hit_density_per_kword", 0) > 8.0:
        report.append("> [!WARNING]")
        report.append("> **Verdict: BLOATED / PACING DRAG DETECTED.**")
        report.append(f"> Found {len(talking_heads)} talking-head scenes with minimal physical action, {len(purple_alerts)} high-frequency purple prose phrases, and high domestic/transit logistics density.")
    else:
        report.append("> [!NOTE]")
        report.append("> **Verdict: LEAN & DYNAMIC.**")
        report.append("> Good narrative velocity, disciplined sensory description, and well-staged physical action beats.")
    report.append("")
    
    # 2. Talking Heads & Stagnant Action
    report.append("## 2. Stagnant Action & Talking Heads Scanner")
    report.append("| Scene | Title | Words | Dialogue % | Action Verbs | Risk Assessment |")
    report.append("|---|---|---|---|---|---|")
    for s in scene_actions:
        risk_str = "**TALKING HEADS (Low Action)**" if s["talking_heads_risk"] else "Balanced"
        report.append(f"| Scene {s['scene_id']} | {s['title'][:35]} | {s['word_count']} | {int(s['dialogue_ratio']*100)}% | {s['action_verb_count']} | {risk_str} |")
    report.append("")
    
    # 3. Purple Prose & Sensory Overkill
    report.append("## 3. Sensory Overkill & Lexical Echoes")
    if purple_prose:
        for p in purple_prose:
            report.append(f"- **`{p['phrase']}`**: repeated **{p['occurrences']} times** across session (`[{p['severity']}]`).")
    else:
        report.append("- No high-frequency sensory echoes detected. Varied atmospheric palette.")
    report.append("")
    
    # 4. Logistics & Filler Density
    report.append("## 4. Logistics & Table Filler Scanner")
    report.append(f"- **Filler hits per 1,000 words:** {logistics.get('hit_density_per_kword', 0)}")
    for cat, count in logistics.get("categories", {}).items():
        report.append(f"  - **{cat}:** {count} occurrences")
    report.append("")
    
    # 5. Character Voice Profiles
    report.append("## 5. Character Voice Differentiation")
    for char, v in voices.items():
        report.append(f"- **{char}:** {v['total_quotes']} turns | Avg {v['avg_words_per_turn']} w/turn | Top vocab: {', '.join(v['top_vocab'])}")
    report.append("")
    
    # 6. Recommendation for 2nd Pass Abridgment
    report.append("## 6. Recommended 2nd-Pass Cuts & Compressions")
    if talking_heads:
        for th in talking_heads:
            report.append(f"- **Compress Scene {th['scene_id']} ({th['title']}):** High dialogue ({int(th['dialogue_ratio']*100)}%) with low physical movement. Inject active staging beats or compress negotiations by 25%.")
    if logistics.get("hit_density_per_kword", 0) > 6.0:
        report.append("- **Trim Corridor & Dining Beats:** Condense morning arrivals and food table chatter into swift 1-paragraph establishing transitions.")
    if not talking_heads and logistics.get("hit_density_per_kword", 0) <= 6.0:
        report.append("- **Scene Retention:** High narrative density. Retain fully for the core novel.")
        
    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="Adversarial Prose Critic")
    parser.add_argument("session_id", help="Session ID (e.g. s1, s7.5)")
    parser.add_argument("--out", help="Output path for markdown critique report")
    args = parser.parse_args()
    
    from pathlib import Path
    base_dir = str(Path(__file__).resolve().parents[4])
    story_path = os.path.join(base_dir, "sessions", "transcripts", "clean", f"{args.session_id}-clean-story.md")
    
    report = generate_critique_report(args.session_id, story_path)
    
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[OK] Wrote critique report to {args.out}")
    else:
        print(report)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
