"""Batch & Nightly Scheduling Manager for the Vumbua Ebook Engine.

Tracks block completion status, generates queued batches of unrendered scenes,
enforces rate-limit delays, and supports background execution loops.
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from typing import Dict, Any, List

from .config import get_sessions_dir
from .leak_detector import LeakDetector
from .lore_guardian import LoreGuardian


class BatchScheduler:
    def __init__(self, sessions_dir: Path = None):
        self.sessions_dir = sessions_dir or get_sessions_dir()
        self.transcripts_dir = self.sessions_dir / "data"
        self.index_dir = self.transcripts_dir / "index"
        self.blocks_dir = self.transcripts_dir / "clean" / "blocks"

    def get_manifest_path(self, session_id: str) -> Path:
        return self.index_dir / f"{session_id}-manifest.json"

    def load_manifest(self, session_id: str) -> Dict[str, Any]:
        path = self.get_manifest_path(session_id)
        if not path.exists():
            raise FileNotFoundError(f"Manifest not found for session {session_id} at {path}")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Inspects all scenes in the manifest against existing block files."""
        manifest = self.load_manifest(session_id)
        blocks = manifest.get("scene_blocks", [])

        completed_blocks = []
        pending_blocks = []
        ooc_blocks = []

        leak_det = LeakDetector()
        lore_grd = LoreGuardian()

        for b in blocks:
            scene_id = b["scene_id"]
            start, end = b["line_range"]
            title = b.get("title", f"Scene {scene_id}")
            is_ooc = b.get("ooc", False)

            if is_ooc:
                ooc_blocks.append({
                    "scene_id": scene_id,
                    "title": title,
                    "range": [start, end],
                    "status": "OOC_SKIPPED"
                })
                continue

            block_file = self.blocks_dir / f"{session_id}-scene-{scene_id:02d}.md"
            if not block_file.exists():
                pending_blocks.append({
                    "scene_id": scene_id,
                    "title": title,
                    "range": [start, end],
                    "status": "MISSING"
                })
            else:
                # Check for validity
                with open(block_file, "r", encoding="utf-8") as f:
                    content = f.read()

                leak_res = leak_det.scan_text(content, filename=block_file.name)
                lore_res = lore_grd.scan_text(content, filename=block_file.name)
                has_ledger = "LEDGER:" in content

                errors = leak_res["violations"] + lore_res["errors"]
                if not has_ledger:
                    errors.append({"message": "Missing LEDGER footer"})

                if errors:
                    pending_blocks.append({
                        "scene_id": scene_id,
                        "title": title,
                        "range": [start, end],
                        "status": "INVALID",
                        "errors": errors
                    })
                else:
                    word_count = len(content.split())
                    completed_blocks.append({
                        "scene_id": scene_id,
                        "title": title,
                        "range": [start, end],
                        "status": "VALID",
                        "words": word_count
                    })

        total_scenes = len(blocks)
        non_ooc_total = total_scenes - len(ooc_blocks)
        progress_pct = round((len(completed_blocks) / max(1, non_ooc_total)) * 100, 1)

        return {
            "session_id": session_id,
            "total_scenes": total_scenes,
            "ooc_scenes": len(ooc_blocks),
            "completed_scenes": len(completed_blocks),
            "pending_scenes": len(pending_blocks),
            "progress_percent": progress_pct,
            "completed": completed_blocks,
            "pending": pending_blocks,
            "ooc": ooc_blocks
        }

    def print_status(self, session_id: str):
        status = self.get_session_status(session_id)
        print("=" * 70)
        print(f"  BATCH SCHEDULER STATUS: {session_id.upper()}")
        print(f"  PROGRESS: {status['completed_scenes']} / {status['total_scenes'] - status['ooc_scenes']} Active Scenes ({status['progress_percent']}%)")
        print(f"  OOC (Skipped): {status['ooc_scenes']} | PENDING: {status['pending_scenes']}")
        print("=" * 70)

        if status["pending"]:
            print("\n[PENDING SCENE QUEUE]")
            for p in status["pending"]:
                reason = p["status"]
                err_str = f" ({len(p.get('errors', []))} errors)" if reason == "INVALID" else ""
                print(f"  - Scene {p['scene_id']:02d}: {p['title']} [{p['range'][0]} - {p['range'][1]}] -> [{reason}{err_str}]")
        else:
            print("\n[ALL SCENES COMPLETED AND VALIDATED]")

        print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Batch Scheduler CLI")
    parser.add_argument("session_id", help="Session ID (e.g. s12)")
    args = parser.parse_args()

    scheduler = BatchScheduler()
    scheduler.print_status(args.session_id)


if __name__ == "__main__":
    main()
