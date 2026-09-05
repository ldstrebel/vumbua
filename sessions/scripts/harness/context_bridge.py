"""Context Bridge & Micro-State Ledger.

Tracks narrative state across scene blocks (setting, active characters,
physical statuses, carried props, and immediate preceding action) so each
LLM generation step requires only a ~200-token continuity prompt rather than
the entire past manuscript.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ContextBridge:
    def __init__(self, blocks_dir: Optional[Path] = None):
        self.blocks_dir = blocks_dir or (Path(__file__).resolve().parent.parent.parent / "transcripts" / "clean" / "blocks")

    def get_state_file_path(self, session_id: str, scene_id: int) -> Path:
        return self.blocks_dir / f"{session_id}-scene-{scene_id:02d}-state.json"

    def save_scene_state(self, session_id: str, scene_id: int, state_data: Dict[str, Any]) -> Path:
        """Saves state output after a scene has been novelized."""
        os.makedirs(self.blocks_dir, exist_ok=True)
        path = self.get_state_file_path(session_id, scene_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=2)
        return path

    def load_scene_state(self, session_id: str, scene_id: int) -> Optional[Dict[str, Any]]:
        """Loads state from a previous scene."""
        path = self.get_state_file_path(session_id, scene_id)
        if not path.exists():
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def format_bridge_prompt(self, previous_state: Dict[str, Any]) -> str:
        """Formats the compact context bridge block for injecting into an LLM prompt."""
        if not previous_state:
            return ""

        setting = previous_state.get("location_and_environment", "Unspecified setting")
        chars = previous_state.get("characters_present", [])
        char_lines = []
        for c in chars:
            if isinstance(c, dict):
                name = c.get("name", "Unknown")
                status = c.get("status", "")
                char_lines.append(f"  - **{name}**: {status}" if status else f"  - **{name}**")
            else:
                char_lines.append(f"  - **{c}**")

        items = previous_state.get("key_items_or_props", [])
        action = previous_state.get("immediate_preceding_action", "")
        emotional_tone = previous_state.get("emotional_tone_or_tension", "")

        lines = [
            "### 🌉 Preceding Scene Context Bridge (Preserve Continuity)",
            f"- **Setting & Environment**: {setting}",
            "- **Active Characters & Physical State**:",
        ]
        lines.extend(char_lines or ["  - None recorded"])

        if items:
            lines.append(f"- **Key Carried Props / Active Tech**: {', '.join(items)}")
        if action:
            lines.append(f"- **Immediate Preceding Action**: {action}")
        if emotional_tone:
            lines.append(f"- **Emotional Tone / Stakes**: {emotional_tone}")

        lines.append("")
        return "\n".join(lines)
