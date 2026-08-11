#!/usr/bin/env python3
"""Build a human review dossier for a session's novelization assumptions.

Enriches sN-assumptions.json in place:
  - rendered_as: the exact prose paragraph(s) from sN-clean-story.md whose
    trailing marker cluster contains the assumption's raw line(s), or
    "(not rendered as dialogue...)" when the line was skipped/narration.
  - review: {"status": "pending", "correction": ""} — edit status to
    "approved" or "corrected" (put the fix in correction) and hand it back.

Also writes sessions/review/sN-dossier.md: raw vs rendered side by side for every
low/medium confidence entry, with a fill-in verdict line per item.

Usage: python3 build_dossier.py s12 [--all-confidences]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def paragraph_map(story_text: str) -> dict[int, str]:
    """Map raw line number -> prose paragraph that renders it.

    Markers are trailing clusters at paragraph ends, so every marker in a
    paragraph maps to that paragraph's prose (markers stripped).
    """
    out: dict[int, str] = {}
    for para in re.split(r"\n\s*\n", story_text):
        para = para.strip()
        if not para or para.startswith("<!-- RAW_RANGE") or para.startswith("<!-- LEDGER"):
            continue
        lines = [int(m) for m in re.findall(r"<!--\s*L(\d+)\s*-->", para)]
        if not lines:
            continue
        prose = re.sub(r"\s*<!--\s*L\d+\s*-->", "", para).strip()
        for n in lines:
            out[n] = prose
    return out


def main() -> None:
    session = sys.argv[1] if len(sys.argv) > 1 else "s12"
    all_conf = "--all-confidences" in sys.argv

    assumptions_path = ROOT / "transcripts" / "index" / f"{session}-assumptions.json"
    story_path = ROOT / "transcripts" / "clean" / f"{session}-clean-story.md"
    dossier_path = ROOT / "review" / f"{session}-dossier.md"
    dossier_path.parent.mkdir(exist_ok=True)

    assumptions = json.loads(assumptions_path.read_text())
    para_of = paragraph_map(story_path.read_text())

    for entry in assumptions:
        paras: list[str] = []
        for n in entry.get("raw_lines", []):
            p = para_of.get(n)
            if p and p not in paras:
                paras.append(p)
        entry["rendered_as"] = (
            "\n\n".join(paras)
            if paras
            else "(not rendered as dialogue — omitted, fused into narration, or covered by a ledger skip)"
        )
        entry.setdefault("review", {"status": "pending", "correction": ""})

    assumptions_path.write_text(json.dumps(assumptions, indent=2) + "\n")

    wanted = {"low", "medium"} if not all_conf else {"low", "medium", "high"}
    items = [a for a in assumptions if a.get("confidence") in wanted]
    order = {"low": 0, "medium": 1, "high": 2}
    items.sort(key=lambda a: (order.get(a.get("confidence"), 9), a.get("scene_id", 0)))

    lines = [
        f"# {session.upper()} Novelization — Assumption Review Dossier",
        "",
        f"{len(items)} items needing your eyes ({sum(1 for a in items if a['confidence']=='low')} low, "
        f"{sum(1 for a in items if a['confidence']=='medium')} medium confidence). "
        "For each: fill in the **Verdict** line — `OK` to approve, or write the correction "
        "(what was actually said / who actually spoke / how it should read). "
        "Anything left blank stays pending.",
        "",
        "---",
        "",
    ]
    for a in items:
        raw_ref = ", ".join(f"L{n}" for n in a.get("raw_lines", []))
        lines += [
            f"## {a['id']} — scene {a['scene_id']}, {raw_ref} ({a['confidence']} confidence, {a['type']})",
            "",
            f"**Raw transcript said:**",
            f"> {a.get('raw_text', '(raw text not captured)')}",
            "",
            f"**Interpreted as:** {a['assumption']}",
            "",
            "**Rendered in prose:**",
        ]
        lines += [f"> {ln}" if ln else ">" for ln in a["rendered_as"].splitlines()]
        lines += ["", "**Verdict:** ", "", "---", ""]

    dossier_path.write_text("\n".join(lines))
    print(f"[OK] Enriched {assumptions_path.name} (rendered_as + review fields)")
    print(f"[OK] Wrote {dossier_path} ({len(items)} review items)")


if __name__ == "__main__":
    main()
