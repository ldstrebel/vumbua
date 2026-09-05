#!/usr/bin/env python3
"""Extract the narration boxes and speech bubbles out of a storyboard document.

Purely mechanical: it reads page/panel headings, the explicit
`**Narration Box (...)**` / `**Speech Bubble N (Label)**` bullets, and — for the pages
that only carry their text inside the image prompt — the `Narration box ...: "…"` and
`Speech bubble ... : "…"` clauses of the prompt itself. Nothing is paraphrased, no
speaker is resolved to a campaign identity, and the panel's `Plain Language Fallback`
is carried along verbatim so a later pass can use it as narration.

Resolving a bubble's label ("moss leader", "Trench leader") to an actual NPC is a
semantic decision and lives in `sN-vision-inserts.json`, not here.

    python sessions/_scripts/extract_storyboard.py campaign/storyboards/clans-origin-storyboard.md
"""

import argparse
import json
import re
import sys

PAGE_RE = re.compile(r"^##\s*\S*\s*Page\s+([\d.]+):\s*(.+?)\s*$")
PANEL_RE = re.compile(r"^###\s*Panel\s+(\d+)\s*(?:\((.*)\))?\s*$")
BULLET_RE = re.compile(r"^\*\s+\*\*(.+?):\*\*\s*(.*)$")
SETTING_RE = re.compile(r"^\*\*Scene Location:\*\*\s*(.+?)\s*$")
NARRATION_BULLET_RE = re.compile(r"^Narration Box(?:\s*\d+)?(?:\s*\((.+?)\))?$", re.I)
BUBBLE_BULLET_RE = re.compile(r"^Speech Bubble(?:\s*\d+)?(?:\s*\((.+?)\))?$", re.I)
PROMPT_NARRATION_RE = re.compile(r"Narration box(?:\s*\d+)?\s*([a-z ]*?):\s*\"(.+?)\"", re.I)
PROMPT_BUBBLE_RE = re.compile(
    r"Speech bubble(?:\s*\d+)?\s*(?:from\s+)?([A-Za-z' -]*?):\s*\"(.+?)\"", re.I
)
SFX_RE = re.compile(r"Sound effect[^:]*:\s*\"(.+?)\"", re.I)


def strip_code(text):
    return text.strip().strip("`").strip()


def unquote(text):
    text = strip_code(text)
    if len(text) > 1 and text[0] == '"' and text[-1] == '"':
        text = text[1:-1]
    return text.strip()


def key(text):
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def parse(path):
    pages = []
    page = panel = None
    for raw in open(path, encoding="utf-8"):
        line = raw.rstrip("\n")

        match = PAGE_RE.match(line)
        if match:
            page = {"page": match.group(1), "title": match.group(2),
                    "scene_location": "", "panels": []}
            pages.append(page)
            panel = None
            continue

        match = SETTING_RE.match(line)
        if match and page is not None:
            page["scene_location"] = match.group(1).rstrip("  ").rstrip()
            continue

        match = PANEL_RE.match(line)
        if match and page is not None:
            panel = {
                "panel": int(match.group(1)),
                "layout": (match.group(2) or "").strip(),
                "fallback": "",
                "narration": [],
                "dialogue": [],
                "sfx": [],
            }
            page["panels"].append(panel)
            continue

        match = BULLET_RE.match(line)
        if not match or panel is None:
            continue
        field, value = match.group(1).strip(), match.group(2)

        if field.lower().startswith("plain language fallback"):
            panel["fallback"] = strip_code(value)
            continue
        if field.lower().startswith("sound effect"):
            panel["sfx"].append(unquote(value))
            continue

        found = NARRATION_BULLET_RE.match(field)
        if found:
            panel["narration"].append(
                {"position": (found.group(1) or "").strip(), "text": unquote(value)}
            )
            continue

        found = BUBBLE_BULLET_RE.match(field)
        if found:
            panel["dialogue"].append(
                {"label": (found.group(1) or "").strip(), "text": unquote(value)}
            )
            continue

        if field.lower() == "prompt":
            prompt = strip_code(value)
            seen = {key(item["text"]) for item in panel["narration"]}
            for position, text in PROMPT_NARRATION_RE.findall(prompt):
                if key(text) not in seen:
                    panel["narration"].append(
                        {"position": position.strip(), "text": text.strip()}
                    )
                    seen.add(key(text))
            seen = {key(item["text"]) for item in panel["dialogue"]}
            for label, text in PROMPT_BUBBLE_RE.findall(prompt):
                if key(text) not in seen:
                    panel["dialogue"].append(
                        {"label": label.strip(), "text": text.strip()}
                    )
                    seen.add(key(text))
            seen = {key(text) for text in panel["sfx"]}
            for text in SFX_RE.findall(prompt):
                if key(text) not in seen:
                    panel["sfx"].append(text.strip())
                    seen.add(key(text))
    return pages


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("storyboard")
    parser.add_argument("--out", help="write JSON here instead of stdout")
    parser.add_argument("--labels", action="store_true",
                        help="list every speech-bubble label with its page/panel")
    args = parser.parse_args(argv)

    pages = parse(args.storyboard)
    if args.labels:
        for page in pages:
            for panel in page["panels"]:
                for item in panel["dialogue"]:
                    print(f"p{page['page']}.{panel['panel']}\t{item['label']}\t{item['text'][:70]}")
        return 0

    payload = {"storyboard": args.storyboard, "pages": pages}
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(text + "\n")
        narration = sum(len(p["narration"]) for page in pages for p in page["panels"])
        dialogue = sum(len(p["dialogue"]) for page in pages for p in page["panels"])
        print(f"Extracted {len(pages)} pages: {narration} narration boxes, "
              f"{dialogue} speech bubbles → {args.out}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
