#!/usr/bin/env python3
"""
Vumbua Audio Manifest Auditor
-----------------------------
Audits sN_audio_manifest.json against sN-clean-story.md for 100% word-for-word parity
and speaker assignment integrity.

Zero fake warnings. Full empirical verification.

Usage:
  python sessions/_scripts/audit_manifest.py \
    --manifest campaign/audio/s11/s11_audio_manifest.json \
    --story sessions/data/clean/s11-clean-story.md \
    --report campaign/audio/s11/manifest_audit_report.md
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path

# Ensure UTF-8 output formatting for Windows terminals
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

VALID_SPEAKERS = {"Narrator", "Loami", "Pip", "Ignatious", "Britt", "Aggie", "Iggy", "Bramble"}

def audit_manifest(manifest_path, story_path, report_path):
    print(f"\n🔍 Auditing Audio Manifest: {manifest_path}")
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        blocks = json.load(f)

    with open(story_path, "r", encoding="utf-8") as f:
        story_text = f.read()

    # Strip YAML frontmatter if present
    if story_text.startswith("---"):
        parts = story_text.split("---", 2)
        if len(parts) >= 3:
            story_text = parts[2]

    # Reconstitute source story lines from manifest blocks
    line_reconstitution = {}
    speaker_counts = {}
    invalid_speakers = []
    formatting_issues = []

    for b in blocks:
        line_num = b["line_num"]
        spk = b["speaker"]
        txt = b["text"]

        # Track speaker counts
        speaker_counts[spk] = speaker_counts.get(spk, 0) + 1

        # Check speaker validity
        if spk not in VALID_SPEAKERS:
            invalid_speakers.append((b["id"], line_num, spk, txt))

        # Check for orphan quote formatting
        if spk != "Narrator" and not (txt.startswith('"') or txt.endswith('"')):
            formatting_issues.append((b["id"], line_num, spk, f"Character voice block without quotes: '{txt}'"))

        # Reconstruct line text
        if line_num not in line_reconstitution:
            line_reconstitution[line_num] = []
        line_reconstitution[line_num].append(txt)

    # Verify 100% Word-for-Word Parity against sN-clean-story.md
    story_lines = story_text.splitlines()
    parity_errors = []
    total_parsed_lines = 0

    for line_num, raw_line in enumerate(story_lines, 1):
        line = raw_line.strip()
        if not line or line.startswith("---") or line.startswith("title:") or line.startswith("author:") or line.startswith("campaign:") or line.startswith("genre:"):
            continue
        if line.startswith("# ") and not line.startswith("## "):
            continue
        if line.startswith("## CHAPTER") or line.startswith("#"):
            continue

        total_parsed_lines += 1
        if line_num not in line_reconstitution:
            parity_errors.append(f"Line {line_num} missing from manifest: '{line[:60]}...'")
            continue

        # Join reconstituted sub-blocks for this line
        reconstituted = "".join(line_reconstitution[line_num])

        if line != reconstituted:
            parity_errors.append(f"L{line_num} Parity Mismatch:\n  Original     : '{line}'\n  Reconstituted: '{reconstituted}'")

    # Generate Audit Report Markdown File
    report_file = Path(report_path)
    report_file.parent.mkdir(parents=True, exist_ok=True)

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# Audio Manifest Parity & Integrity Audit Report\n\n")
        f.write(f"- **Manifest File:** `{manifest_path}`\n")
        f.write(f"- **Story Source File:** `{story_path}`\n")
        f.write(f"- **Total Audio Blocks:** {len(blocks)}\n")
        f.write(f"- **Total Parsed Prose Lines:** {total_parsed_lines}\n\n")

        f.write("## 🗣️ Voice Cast Breakdown\n\n")
        f.write("| Speaker | Block Count | Percentage |\n")
        f.write("|---|---|---|\n")
        for spk, count in sorted(speaker_counts.items(), key=lambda x: x[1], reverse=True):
            pct = (count / len(blocks)) * 100
            f.write(f"| **{spk}** | {count} | {pct:.1f}% |\n")

        f.write("\n## 🎯 Audit Verification Results\n\n")
        
        if not parity_errors and not invalid_speakers and not formatting_issues:
            f.write("> [!NOTE]\n")
            f.write("> ✅ **PASSED 100% PARITY & INTEGRITY AUDIT!**\n")
            f.write("> All story text reconstituted 100% verbatim. Zero dropped words, zero invalid speakers.\n")
        else:
            if parity_errors:
                f.write(f"> [!CAUTION]\n> **Found {len(parity_errors)} Text Parity Mismatch(es):**\n\n")
                for err in parity_errors:
                    f.write(f"```text\n{err}\n```\n")

            if invalid_speakers:
                f.write(f"\n> [!WARNING]\n> **Found {len(invalid_speakers)} Invalid Speaker(s):**\n\n")
                for item in invalid_speakers:
                    f.write(f"- Block #{item[0]} (Line {item[1]}): Unknown Speaker `{item[2]}`\n")

            if formatting_issues:
                f.write(f"\n> [!WARNING]\n> **Found {len(formatting_issues)} Formatting Issue(s):**\n\n")
                for item in formatting_issues:
                    f.write(f"- Block #{item[0]} (Line {item[1]}): {item[3]}\n")

    print(f"📊 Audit Complete!")
    print(f"   • Total Blocks Audited : {len(blocks)}")
    print(f"   • Parity Status        : {'✅ 100% VERBATIM MATCH' if not parity_errors else '❌ PARITY ERRORS FOUND'}")
    print(f"   • Audit Report Saved   : {report_file.resolve()}\n")

    if parity_errors:
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vumbua Audio Manifest Auditor")
    parser.add_argument("--manifest", required=True, help="Path to sN_audio_manifest.json")
    parser.add_argument("--story", required=True, help="Path to sN-clean-story.md")
    parser.add_argument("--report", default="campaign/audio/s11/manifest_audit_report.md", help="Path to audit report markdown file")

    args = parser.parse_args()
    audit_manifest(args.manifest, args.story, args.report)
