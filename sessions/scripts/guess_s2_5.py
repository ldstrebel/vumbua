"""Heuristic speaker guesses for s2.5 (undiarized two-person session).

Session 2.5 is a one-on-one between Luke S (GM) and Holly (Iggy).
Voice model built from s1's attributed transcript:
  - Luke S: long narration, world description, "what Iggy sees",
    questions directed at the player ("What would Iggy do?").
  - Holly: short intent statements ("I think Iggy would..."),
    backchannels, answers; names 'Luke' in third person.

Output: index/s2.5-speaker-guesses.json — per-line {guess, confidence, reason}.
Every guess is low-confidence scaffolding for a human/LLM attribution pass;
nothing here is canonical.
"""
import json, re
from pathlib import Path

IDX = Path('sessions/transcripts/index/s2.5-raw-indexed.md')
OUT = Path('sessions/transcripts/index/s2.5-speaker-guesses.json')

LINE = re.compile(r"^L(\d+): \[undiarized\](?: \[TURN\?\])?\s*(.*)$")

GM_CUES = [
    r"\bwhat (?:does|would|do|did|can) iggy\b", r"\biggy (?:sees|knows|hears|"
    r"notices|gets|might|can|would have|hasn't|is getting)\b",
    r"^so\b", r"^and so\b", r"^um\b", r"^okay\b", r"\?$",
    r"\byou (?:see|hear|notice|can|would|could|are|were|get|have)\b",
    r"\ba couple of\b", r"\bbasically\b", r"\bthe thing is\b",
    r"\bwhat i (?:would|think|imagine)\b", r"\bthe (?:map|board|fire|campfire|"
    r"guards|captain|professor|node|ship|battery)\b",
]
HOLLY_CUES = [
    r"\bi think (?:that )?iggy\b", r"\biggy (?:just|just sort|probably|"
    r"would|wants|goes|does|is gonna|gonna|tries)\b",
    r"^yeah\b", r"^no\b", r"^mhm\b", r"^oh\b", r"^wait\b", r"^nice\b",
    r"^i (?:don't|do|did|was|am|feel|guess|mean|like|love|hate)\b",
    r"\bluke\b",  # naming the GM in third person
    r"\bmy (?:character|guy|dude|man)\b",
]

def score(body):
    g = sum(1 for p in GM_CUES if re.search(p, body, re.I))
    h = sum(1 for p in HOLLY_CUES if re.search(p, body, re.I))
    if g == h:
        return None, 0.0
    who = "Luke S" if g > h else "Holly"
    conf = min(0.9, 0.4 + 0.15 * abs(g - h))
    return who, conf

guesses = {}
counts = {"Luke S": 0, "Holly": 0, "unknown": 0}
for raw in open(IDX, encoding="utf-8"):
    m = LINE.match(raw.rstrip("\n"))
    if not m:
        continue
    n, body = int(m.group(1)), m.group(2)
    who, conf = score(body)
    if who:
        guesses[str(n)] = {"guess": who, "confidence": round(conf, 2),
                           "reason": f"cue match (gm-vs-holly differential)"}
        counts[who] += 1
    else:
        counts["unknown"] += 1

OUT.write_text(json.dumps({
    "session_id": "s2.5",
    "_note": "Heuristic guesses ONLY — undiarized single-mic transcript. "
             "Treat as scaffolding for an attribution pass, never as canon. "
             "All confidences are capped at 0.9 and most sit at 0.4-0.55.",
    "counts": counts,
    "lines": guesses,
}, indent=2), encoding="utf-8")
print(counts, "->", OUT)
