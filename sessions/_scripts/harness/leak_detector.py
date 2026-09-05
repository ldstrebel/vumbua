"""Leak and Table-Talk Sanitizer.

Deterministically detects real player names, TTRPG mechanics jargon,
OOC technical audio artifacts, and embedded italic dialogue anti-patterns.
"""

import re
from typing import List, Dict, Any
from .config import DENY_LIST_PLAYERS, DENY_LIST_MECHANICS, DENY_LIST_OOC_REALIA


class LeakDetector:
    def __init__(self, extra_player_names: List[str] = None):
        self.player_names = set(DENY_LIST_PLAYERS)
        if extra_player_names:
            self.player_names.update(name.lower() for name in extra_player_names)

        # Build regex patterns for players
        # Note: Luke should not match lukewarm. Use word boundaries.
        self.player_regexes = [
            (name, re.compile(rf"\b{re.escape(name)}\b", re.IGNORECASE))
            for name in sorted(self.player_names, key=lambda x: -len(x))
        ]

        # Build regex patterns for mechanics
        self.mechanics_regexes = [
            (term, re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE))
            for term in sorted(DENY_LIST_MECHANICS, key=lambda x: -len(x))
        ]

        # Build regex patterns for OOC realia
        self.realia_regexes = [
            (term, re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE))
            for term in sorted(DENY_LIST_OOC_REALIA, key=lambda x: -len(x))
        ]

        # Embedded italic dialogue pattern: *Dialogue text here,* Pip said...
        self.embedded_italic_regex = re.compile(
            r"\*([^*]{6,}[,.]?)\*[,.]?\s+(?:[A-Za-z'-]+\s+)?(?:said|asked|shouted|murmured|replied|yelled|groaned|laughed|whispered|muttered)\b",
            re.IGNORECASE
        )

    def scan_text(self, text: str, filename: str = "text") -> Dict[str, Any]:
        """Scans text line by line and returns violations."""
        lines = text.splitlines()
        violations = []
        warnings = []
        in_frontmatter = False
        in_codeblock = False

        for line_idx, line in enumerate(lines, start=1):
            stripped = line.strip()

            # Handle frontmatter
            if stripped == "---":
                if line_idx == 1:
                    in_frontmatter = True
                    continue
                elif in_frontmatter:
                    in_frontmatter = False
                    continue

            if in_frontmatter:
                continue

            # Handle code blocks
            if stripped.startswith("```"):
                in_codeblock = not in_codeblock
                continue
            if in_codeblock:
                continue

            # Skip pure comment / ledger lines
            if stripped.startswith("<!--") and stripped.endswith("-->"):
                continue

            # 1. Player Name Leaks (Strict Violation)
            for name, regex in self.player_regexes:
                # Avoid false positives for "Luke" if part of "Luke S" in ledger or metadata
                if regex.search(line):
                    violations.append({
                        "line": line_idx,
                        "type": "PLAYER_NAME_LEAK",
                        "severity": "ERROR",
                        "matched": name,
                        "snippet": line[:120],
                        "message": f"Real player name '{name}' detected in manuscript."
                    })

            # 2. TTRPG Mechanics Leaks (Strict Violation)
            for term, regex in self.mechanics_regexes:
                if regex.search(line):
                    violations.append({
                        "line": line_idx,
                        "type": "MECHANICS_LEAK",
                        "severity": "ERROR",
                        "matched": term,
                        "snippet": line[:120],
                        "message": f"Game mechanics jargon '{term}' detected in manuscript."
                    })

            # 3. OOC Realia Leaks (Strict Violation)
            for term, regex in self.realia_regexes:
                if regex.search(line):
                    violations.append({
                        "line": line_idx,
                        "type": "OOC_REALIA_LEAK",
                        "severity": "ERROR",
                        "matched": term,
                        "snippet": line[:120],
                        "message": f"Real-world audio/technical term '{term}' detected in manuscript."
                    })

            # 4. Embedded Italic Dialogue Anti-Pattern
            m_italic = self.embedded_italic_regex.search(line)
            if m_italic:
                violations.append({
                    "line": line_idx,
                    "type": "EMBEDDED_ITALIC_DIALOGUE",
                    "severity": "ERROR",
                    "matched": m_italic.group(0),
                    "snippet": line[:120],
                    "message": "Anti-Pattern: Embedded italic dialogue detected. Must use standard quotes (\"...\")."
                })

        return {
            "filename": filename,
            "passed": len(violations) == 0,
            "error_count": len(violations),
            "warning_count": len(warnings),
            "violations": violations,
            "warnings": warnings
        }

    def scan_file(self, filepath: str) -> Dict[str, Any]:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return self.scan_text(content, filename=filepath)
