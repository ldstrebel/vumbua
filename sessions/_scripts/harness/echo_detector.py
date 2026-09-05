"""Fuzzy Echo and Repetition Detector.

Finds proximity phrase echoes, repetitive sentence structures,
and overused filter words / weak fiction crutches.
"""

import re
from collections import defaultdict, deque
from typing import List, Dict, Any, Tuple
from .config import FILTER_WORDS


STOP_PHRASES = {
    "in front of", "out of the", "at the end", "as well as",
    "on top of", "one of the", "part of the", "the edge of",
    "the side of", "the rest of", "into the air", "a couple of",
    "back to the", "down to the", "shook his head", "shook her head",
    "took a breath", "took a deep", "deep breath and"
}


class EchoDetector:
    def __init__(self, proximity_window_words: int = 400, min_ngram_len: int = 3, max_ngram_len: int = 5):
        self.window_size = proximity_window_words
        self.min_ngram = min_ngram_len
        self.max_ngram = max_ngram_len
        self.filter_regexes = [(p, re.compile(p, re.IGNORECASE)) for p in FILTER_WORDS]

    def _tokenize(self, text: str) -> List[Tuple[str, int, int]]:
        """Tokenizes text into (word, line_number, char_offset) tuples."""
        tokens = []
        lines = text.splitlines()
        for line_num, line in enumerate(lines, start=1):
            # Ignore markdown comments and headers
            if line.strip().startswith("<!--") or line.strip().startswith("#"):
                continue
            for match in re.finditer(r"\b[A-Za-z0-9'-]+\b", line):
                tokens.append((match.group(0), line_num, match.start()))
        return tokens

    def _extract_sentences(self, text: str) -> List[Tuple[str, int]]:
        """Extracts sentences with their line numbers."""
        sentences = []
        lines = text.splitlines()
        current_sentence = []
        start_line = 1

        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith("<!--") or stripped.startswith("#"):
                continue
            if not stripped:
                continue

            # Split line on punctuation (. ! ?)
            parts = re.split(r"(?<=[.!?])\s+", line)
            for p in parts:
                p_clean = p.strip()
                if p_clean:
                    sentences.append((p_clean, line_num))

        return sentences

    def find_phrase_echoes(self, text: str) -> List[Dict[str, Any]]:
        """Finds repeated multi-word phrases occurring close to each other."""
        tokens = self._tokenize(text)
        echoes = []
        n_tokens = len(tokens)

        # Map phrase -> list of token indices
        seen_phrases = defaultdict(list)

        for n in range(self.min_ngram, self.max_ngram + 1):
            for i in range(n_tokens - n + 1):
                window = tokens[i:i + n]
                words = [w[0].lower() for w in window]
                phrase = " ".join(words)

                # Skip common stop phrases
                if phrase in STOP_PHRASES:
                    continue

                line_num = window[0][1]

                # Check if this phrase was seen within the proximity window
                if phrase in seen_phrases:
                    prev_indices = seen_phrases[phrase]
                    for prev_idx, prev_line in prev_indices:
                        distance = i - prev_idx
                        if 0 < distance <= self.window_size:
                            echoes.append({
                                "phrase": phrase,
                                "first_line": prev_line,
                                "repeat_line": line_num,
                                "distance_words": distance,
                                "message": f"Phrase echo: '{phrase}' repeated {distance} words later (lines {prev_line} & {line_num})."
                            })
                            break
                seen_phrases[phrase].append((i, line_num))

        # Deduplicate overlapping sub-phrases
        unique_echoes = []
        seen_spans = set()
        for echo in sorted(echoes, key=lambda e: (e["first_line"], -len(e["phrase"]))):
            key = (echo["first_line"], echo["repeat_line"])
            if key not in seen_spans:
                seen_spans.add(key)
                unique_echoes.append(echo)

        return unique_echoes

    def find_monotone_starters(self, text: str, threshold: int = 3) -> List[Dict[str, Any]]:
        """Detects 3+ consecutive sentences starting with the same words."""
        sentences = self._extract_sentences(text)
        monotones = []
        if len(sentences) < threshold:
            return monotones

        streak = []
        prev_starter = None

        for s_text, line_num in sentences:
            # Strip dialogue quotes if needed
            s_clean = re.sub(r'^["\']+', '', s_text).strip()
            words = s_clean.split()
            if len(words) < 2:
                continue

            starter = f"{words[0].lower()} {words[1].lower()}"
            # Normalize pronouns e.g. "he looked" vs "he stepped" -> "he"
            single_starter = words[0].lower()

            if single_starter in {"he", "she", "they", "it"} and prev_starter in {"he", "she", "they", "it"} and single_starter == prev_starter:
                streak.append((s_text, line_num, single_starter))
            elif starter == prev_starter:
                streak.append((s_text, line_num, starter))
            else:
                if len(streak) >= threshold:
                    monotones.append({
                        "starter": streak[0][2],
                        "count": len(streak),
                        "start_line": streak[0][1],
                        "end_line": streak[-1][1],
                        "samples": [s[0][:60] for s in streak[:3]],
                        "message": f"Repetitive sentence rhythm: {len(streak)} consecutive sentences start with '{streak[0][2]}'."
                    })
                streak = [(s_text, line_num, starter)]
                prev_starter = starter

        if len(streak) >= threshold:
            monotones.append({
                "starter": streak[0][2],
                "count": len(streak),
                "start_line": streak[0][1],
                "end_line": streak[-1][1],
                "samples": [s[0][:60] for s in streak[:3]],
                "message": f"Repetitive sentence rhythm: {len(streak)} consecutive sentences start with '{streak[0][2]}'."
            })

        return monotones

    def count_filter_words(self, text: str) -> Dict[str, Any]:
        """Counts occurrences of weak filter words and computes frequency per 1,000 words."""
        tokens = self._tokenize(text)
        word_count = len(tokens)
        counts = {}
        total_filters = 0
        matches_by_line = []

        for line_num, line in enumerate(text.splitlines(), start=1):
            if line.strip().startswith("<!--") or line.strip().startswith("#"):
                continue
            for pattern, regex in self.filter_regexes:
                for match in regex.finditer(line):
                    matched_term = match.group(0).lower()
                    counts[matched_term] = counts.get(matched_term, 0) + 1
                    total_filters += 1
                    matches_by_line.append((line_num, matched_term))

        freq_per_1000 = (total_filters / max(1, word_count)) * 1000

        return {
            "word_count": word_count,
            "total_filter_words": total_filters,
            "frequency_per_1000": round(freq_per_1000, 2),
            "counts": counts,
            "high_density": freq_per_1000 > 12.0
        }

    def scan_text(self, text: str, filename: str = "text") -> Dict[str, Any]:
        echoes = self.find_phrase_echoes(text)
        monotones = self.find_monotone_starters(text)
        filter_report = self.count_filter_words(text)

        warnings = []
        for e in echoes[:10]:  # Cap to top 10 to keep reports clean
            warnings.append({
                "type": "PHRASE_ECHO",
                "severity": "WARN",
                "line": e["repeat_line"],
                "message": e["message"]
            })

        for m in monotones:
            warnings.append({
                "type": "MONOTONE_RHYTHM",
                "severity": "WARN",
                "line": m["start_line"],
                "message": m["message"]
            })

        if filter_report["high_density"]:
            warnings.append({
                "type": "FILTER_WORD_DENSITY",
                "severity": "WARN",
                "line": 1,
                "message": f"High filter-word density ({filter_report['frequency_per_1000']} / 1k words). Consider trimming 'felt like', 'seemed to', 'suddenly'."
            })

        return {
            "filename": filename,
            "passed": True,  # Echoes are stylistic warnings, not hard build blockers
            "echoes_found": len(echoes),
            "monotone_streaks": len(monotones),
            "filter_word_stats": filter_report,
            "warnings": warnings
        }
