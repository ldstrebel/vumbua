"""Style and Pacing Analyzer (ProWritingAid & AutoCrit Model).

Calculates sentence length variance, pacing distribution, dialogue ratios,
dialogue tag adverbs, and sensory palette coverage.
"""

import re
import math
from typing import List, Dict, Any, Tuple
from .config import SENSORY_KEYWORDS


class StyleAnalyzer:
    def __init__(self):
        # Regex to extract quoted dialogue
        self.dialogue_regex = re.compile(r'"([^"]*)"|“([^”]*)”')
        # Regex for adverb-heavy dialogue tags e.g. 'said quickly', 'asked quietly'
        self.adverb_tag_regex = re.compile(
            r'\b(said|asked|shouted|whispered|murmured|replied|yelled|groaned|laughed)\s+([a-z]+ly)\b',
            re.IGNORECASE
        )

    def _split_sentences(self, text: str) -> List[Tuple[str, int, int]]:
        """Extracts (sentence_text, line_number, word_count)."""
        sentences = []
        lines = text.splitlines()

        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith("<!--") or stripped.startswith("#"):
                continue
            if not stripped:
                continue

            # Split on sentence terminals
            raw_sentences = re.split(r'(?<=[.!?])\s+', line)
            for s in raw_sentences:
                clean_s = s.strip()
                words = re.findall(r'\b[A-Za-z0-9\'-]+\b', clean_s)
                if words:
                    sentences.append((clean_s, line_num, len(words)))
        return sentences

    def analyze_pacing(self, text: str) -> Dict[str, Any]:
        """Calculates sentence length distribution and pacing variance."""
        sentences = self._split_sentences(text)
        if not sentences:
            return {"sentence_count": 0, "mean_length": 0, "std_dev": 0, "distribution": {}}

        lengths = [s[2] for s in sentences]
        total_sentences = len(lengths)
        mean_len = sum(lengths) / total_sentences

        variance = sum((l - mean_len) ** 2 for l in lengths) / total_sentences
        std_dev = math.sqrt(variance)

        # Categorize sentence lengths
        # Short: 1-8 words (punchy, action)
        # Medium: 9-20 words (standard rhythmic prose)
        # Long: 21-35 words (complex scenic description)
        # Very Long: 36+ words (intricate worldbuilding / rolling thought)
        dist = {
            "short (1-8 words)": sum(1 for l in lengths if l <= 8),
            "medium (9-20 words)": sum(1 for l in lengths if 9 <= l <= 20),
            "long (21-35 words)": sum(1 for l in lengths if 21 <= l <= 35),
            "very_long (36+ words)": sum(1 for l in lengths if l >= 36)
        }

        # Percentage breakdown
        dist_pct = {k: round((v / total_sentences) * 100, 1) for k, v in dist.items()}

        return {
            "sentence_count": total_sentences,
            "mean_length": round(mean_len, 1),
            "std_dev": round(std_dev, 1),
            "pacing_dynamic": std_dev >= 7.0,  # Good variance indicates musical rhythm
            "counts": dist,
            "percentages": dist_pct
        }

    def analyze_dialogue_ratio(self, text: str) -> Dict[str, Any]:
        """Measures the balance between spoken dialogue and narrative prose."""
        total_words = len(re.findall(r'\b[A-Za-z0-9\'-]+\b', text))
        if total_words == 0:
            return {"total_words": 0, "dialogue_words": 0, "narrative_words": 0, "dialogue_pct": 0}

        dialogue_words = 0
        for match in self.dialogue_regex.finditer(text):
            quoted = match.group(1) or match.group(2) or ""
            dialogue_words += len(re.findall(r'\b[A-Za-z0-9\'-]+\b', quoted))

        narrative_words = max(0, total_words - dialogue_words)
        dialogue_pct = round((dialogue_words / total_words) * 100, 1)
        narrative_pct = round((narrative_words / total_words) * 100, 1)

        return {
            "total_words": total_words,
            "dialogue_words": dialogue_words,
            "narrative_words": narrative_words,
            "dialogue_pct": dialogue_pct,
            "narrative_pct": narrative_pct,
            "balanced": 25.0 <= dialogue_pct <= 65.0
        }

    def audit_dialogue_tags(self, text: str) -> List[Dict[str, Any]]:
        """Finds dialogue tags relying on -ly adverbs."""
        issues = []
        for line_num, line in enumerate(text.splitlines(), start=1):
            if line.strip().startswith("<!--"):
                continue
            for match in self.adverb_tag_regex.finditer(line):
                verb = match.group(1)
                adverb = match.group(2)
                # Ignore benign adverbs like 'only', 'simply'
                if adverb.lower() in {"only", "simply", "barely", "hardly"}:
                    continue
                issues.append({
                    "line": line_num,
                    "verb": verb,
                    "adverb": adverb,
                    "snippet": line[:100],
                    "message": f"Adverb in dialogue tag: '{verb} {adverb}'. Replace with character action beat."
                })
        return issues

    def audit_sensory_palette(self, text: str) -> Dict[str, Any]:
        """Measures presence of the 5 sensory registers + arcanatech."""
        text_lower = text.lower()
        palette_counts = {}

        for register, keywords in SENSORY_KEYWORDS.items():
            count = 0
            for kw in keywords:
                # Count word occurrences
                count += len(re.findall(rf'\b{re.escape(kw)}\b', text_lower))
            palette_counts[register] = count

        total_sensory_hits = sum(palette_counts.values())
        covered_registers = sum(1 for count in palette_counts.values() if count > 0)

        return {
            "total_hits": total_sensory_hits,
            "covered_registers": covered_registers,
            "palette_counts": palette_counts,
            "rich_sensory": covered_registers >= 4
        }

    def generate_style_report(self, text: str, filename: str = "text") -> Dict[str, Any]:
        pacing = self.analyze_pacing(text)
        ratio = self.analyze_dialogue_ratio(text)
        tag_adverbs = self.audit_dialogue_tags(text)
        sensory = self.audit_sensory_palette(text)

        warnings = []
        if pacing.get("sentence_count", 0) > 10 and not pacing.get("pacing_dynamic", False):
            warnings.append({
                "type": "MONOTONE_PACING",
                "severity": "INFO",
                "message": f"Sentence length std-dev is low ({pacing['std_dev']}). Mix short punchy lines with longer descriptive sentences."
            })

        for tag_issue in tag_adverbs[:5]:
            warnings.append({
                "type": "ADVERB_DIALOGUE_TAG",
                "severity": "WARN",
                "line": tag_issue["line"],
                "message": tag_issue["message"]
            })

        if sensory["covered_registers"] < 3 and ratio["total_words"] > 500:
            warnings.append({
                "type": "SENSORY_DEFICIT",
                "severity": "WARN",
                "line": 1,
                "message": f"Low sensory register diversity ({sensory['covered_registers']}/5). Add tactile, olfactory, or ambient energy cues."
            })

        return {
            "filename": filename,
            "pacing": pacing,
            "dialogue_ratio": ratio,
            "sensory_palette": sensory,
            "tag_adverb_count": len(tag_adverbs),
            "warnings": warnings
        }
