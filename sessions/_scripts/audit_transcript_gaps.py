#!/usr/bin/env python3
"""Audit transcript dialogue turns against novelization prose to detect omitted interjections,
turn order discrepancies, and dropped character beats.

Usage: python3 audit_transcript_gaps.py [session_id]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

def main() -> None:
    session = sys.argv[1] if len(sys.argv) > 1 else "s12"
    raw_path = ROOT / "sessions" / "data" / "index" / f"{session}-raw-indexed.md"
    manifest_path = ROOT / "sessions" / "data" / "index" / f"{session}-manifest.json"
    
    if not raw_path.exists() or not manifest_path.exists():
        print(f"[ERROR] Missing raw index or manifest for {session}")
        sys.exit(1)
        
    raw_lines = {}
    for line in raw_path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^L(\d+):\s*(.*)", line)
        if m:
            l_num = int(m.group(1))
            raw_lines[l_num] = m.group(2)
            
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    
    print(f"==================================================")
    print(f"[AUDIT] DIALOGUE TURN GAP AUDIT: {session.upper()}")
    print(f"==================================================")
    
    total_gaps = 0
    for scene in manifest.get("scene_blocks", []):
        scene_id = scene["scene_id"]
        ledger = scene.get("dialogue_ledger", [])
        if not ledger or scene.get("ooc", False):
            continue
            
        rendered_nums = sorted([item["line"] if isinstance(item, dict) else item for item in ledger])
        if not rendered_nums:
            continue
            
        min_l, max_l = min(rendered_nums), max(rendered_nums)
        
        skipped_player_turns = []
        for l_num in range(min_l, max_l + 1):
            if l_num not in rendered_nums and l_num in raw_lines:
                txt = raw_lines[l_num]
                # Flag lines spoken by PCs/NPCs that contain dialogue
                if any(spk in txt for spk in ["**Ignatius**", "**Lomi**", "**Britt**", "**Iggy**", "**Aggie**"]):
                    skipped_player_turns.append((l_num, txt))
                    
        if skipped_player_turns:
            print(f"\n[SCENE {scene_id}: {scene['title']}] Potential Omitted Turns:")
            for l_num, txt in skipped_player_turns:
                print(f"  - L{l_num:04d}: {txt[:90]}")
                total_gaps += 1
                
    if total_gaps == 0:
        print("\n[PASS] ZERO OMITTED PLAYER DIALOGUE TURNS DETECTED!")
    else:
        print(f"\n[WARNING] {total_gaps} player dialogue turns skipped between rendered bounds.")

if __name__ == "__main__":
    main()
