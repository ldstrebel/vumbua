"""Seed inline spoken-turn markers (<!-- Lxxxx -->) into an existing clean-story file.

Fuzzy-matches each manifest dialogue-ledger turn against the prose paragraphs of
its scene and appends the marker to the best-matching paragraph. Anything below
the confidence threshold is left unmarked and listed in the report, so a human
(or an LLM pass) can place it manually.

Output: sessions/transcripts/clean/<sid>-clean-story.annotated.md  (never
overwrites the original) plus a per-scene report on stdout.

Usage: python seed_markers.py s12 [--threshold 0.55]
"""

import argparse
import difflib
import json
import os
import re
import sys


def norm(text):
    """Lowercase, strip punctuation/markup for fuzzy comparison."""
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"[^a-z0-9' ]+", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip()


def score(gist, paragraph):
    """Similarity between a ledger gist and a prose paragraph.

    Combines token containment (how much of the gist survives in the
    paragraph) with sequence similarity against the paragraph's best window.
    """
    g, p = norm(gist), norm(paragraph)
    if not g or not p:
        return 0.0
    g_tokens, p_tokens = g.split(), p.split()
    contained = sum(1 for t in g_tokens if t in p_tokens) / len(g_tokens)
    ratio = difflib.SequenceMatcher(None, g, p).ratio()
    return 0.7 * contained + 0.3 * ratio


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("session_id")
    ap.add_argument("--threshold", type=float, default=0.55)
    ap.add_argument("--force", action="store_true",
                    help="Strip pre-existing <!-- Lxxxx --> markers before re-seeding")
    args = ap.parse_args()
    sid = args.session_id

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manifest_path = os.path.join(base, "transcripts", "index", f"{sid}-manifest.json")
    story_path = os.path.join(base, "transcripts", "clean", f"{sid}-clean-story.md")
    out_path = os.path.join(base, "transcripts", "clean", f"{sid}-clean-story.annotated.md")

    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)
    with open(story_path, encoding="utf-8") as f:
        story = f.read()

    # Idempotence guard: never stack markers on an already-annotated draft.
    if re.search(r"<!--\s*L\d+\s*-->", story):
        if args.force:
            story = re.sub(r"\s*<!--\s*L\d+\s*-->", "", story)
        else:
            print("ERROR: story already contains <!-- Lxxxx --> markers. "
                  "Re-run with --force to strip and re-seed.")
            sys.exit(1)

    scene_re = re.compile(
        r"(<!--\s*RAW_RANGE:\s*\[\d+,\s*\d+\]\s*\|\s*SCENE_ID:\s*(\d+)\s*(?:\|\s*OOC)?\s*-->)"
    )
    parts = scene_re.split(story)
    # parts = [preamble, header1, id1, body1, header2, id2, body2, ...]
    ledgers = {
        b["scene_id"]: b.get("dialogue_ledger", [])
        for b in manifest.get("scene_blocks", [])
        if not b.get("ooc", False)
    }

    total_placed, total_unmatched = 0, []
    out = [parts[0]]
    for i in range(1, len(parts), 3):
        header, scene_id, body = parts[i], int(parts[i + 1]), parts[i + 2]
        turns = ledgers.get(scene_id, [])
        if turns:
            # Split body into paragraphs, keep separators for reassembly.
            paragraphs = body.split("\n\n")
            placements = {}  # paragraph index -> list of line numbers
            unmatched = []
            for turn in turns:
                line_no, gist = turn["line"], turn.get("gist", "")
                speaker = turn.get("speaker", "")
                best_idx, best_score = None, 0.0
                for idx, para in enumerate(paragraphs):
                    if "LEDGER:" in para or not para.strip():
                        continue
                    s = score(gist, para)
                    # small bonus if the speaker's name appears in the paragraph
                    if speaker and speaker.lower() in norm(para):
                        s += 0.05
                    if s > best_score:
                        best_idx, best_score = idx, s
                if best_idx is not None and best_score >= args.threshold:
                    placements.setdefault(best_idx, []).append(line_no)
                    total_placed += 1
                else:
                    unmatched.append((line_no, speaker, gist, round(best_score, 2)))

            for idx, lines in placements.items():
                if len(lines) > 3:
                    print(f"  [suspicious] Scene {scene_id}: {len(lines)} turns fuzzy-matched "
                          f"to one paragraph ({sorted(lines)}) — review placement manually.")
                markers = " ".join(f"<!-- L{n:04d} -->" for n in sorted(lines))
                paragraphs[idx] = paragraphs[idx].rstrip() + " " + markers
            body = "\n\n".join(paragraphs)

            if unmatched:
                total_unmatched.extend((scene_id, *u) for u in unmatched)
        out.extend([header, body])

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("".join(out))

    print(f"Wrote {out_path}")
    print(f"Placed {total_placed} markers; {len(total_unmatched)} turns unmatched.")
    if total_unmatched:
        print("\nUNMATCHED TURNS (need manual/LLM placement):")
        for scene_id, line_no, speaker, gist, sc in total_unmatched:
            print(f"  Scene {scene_id} L{line_no:04d} [{speaker}] (best {sc}): {gist[:80]}")
        sys.exit(2)


if __name__ == "__main__":
    main()
