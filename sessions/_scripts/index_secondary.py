"""Index non-diarized session sources (ai-summary, survey) into the standard
artifact shape: hash-locked L####-stamped index file.

Unlike prep_raw.py (which requires a config-declared GM and parses
`**Speaker:**` turns), this handles sources with no diarized turns:
  - ai-summary: meeting summaries / monologue dumps (s2.5, s3)
  - survey:     async choose-your-own-adventure docs (s7.5)

The artifact is shape-compatible with sN-raw-indexed.md but every line carries
a source-class tag instead of a speaker label, so downstream tooling can
measure coverage while knowing the provenance is secondhand.

Usage: python sessions/_scripts/index_secondary.py s2.5 --source-class ai-summary
"""
import argparse, hashlib, json, os, re, sys

NOTE = {
    "ai-summary": "no diarized transcript exists; every line is secondhand "
                  "AI-summarized content.",
    "survey": "primary async-survey source; verbatim by construction.",
    "undiarized": "real full transcript from a single undiarized audio "
                  "source; no speaker labels exist. [TURN?] marks heuristic "
                  "turn-boundary guesses only.",
}
CONTENT_LINE = re.compile(r"^\s*$")          # skip blank lines only
HEADER_LINE = re.compile(r"^(#+\s|>?\s*\[!)")  # markdown headers/callouts kept but tagged


def _mark_turn_boundaries(lines):
    """Heuristic turn-boundary scaffold for undiarized audio: mark lines that
    look like a speaker change (short backchannel after a long turn, vocatives,
    question->answer). Low confidence — a scaffold for the attribution stage,
    not a claim about who spoke."""
    voc = re.compile(r"^(?:hey\s+)?(sophie|kristina|christina|john|holly|"
                     r"luke|britt|aggie|iggy|ignatius|lomi)\b", re.I)
    out = []
    prev_q = False
    for ln in lines:
        body = ln.split("] ", 1)[-1]
        # only two reliable text signals: a question just asked (answer
        # follows = likely new speaker) or an explicit vocative name
        boundary = prev_q or bool(voc.match(body))
        out.append(ln.replace("] ", "] [TURN?] ", 1) if boundary else ln)
        prev_q = body.rstrip().endswith("?")
    return out


def index_secondary(session_id, source_class, out_dir=None, raw_path=None,
                    sessions_dir=None):
    base_dir = sessions_dir or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    raw_path = raw_path or os.path.join(
        base_dir, "data", "raw", f"{session_id}-raw.md")
    if not os.path.exists(raw_path):
        # survey sessions may live in clean/ directly
        alt = os.path.join(base_dir, "data", "clean",
                           f"{session_id}-clean.md")
        raw_path = alt if os.path.exists(alt) else raw_path
    if not os.path.exists(raw_path):
        print(f"[ERROR] no source found for {session_id}", file=sys.stderr)
        sys.exit(1)

    out_dir = out_dir or os.path.join(base_dir, "data", "index")
    os.makedirs(out_dir, exist_ok=True)
    indexed_path = os.path.join(out_dir, f"{session_id}-raw-indexed.md")
    provenance_path = os.path.join(out_dir, f"{session_id}-provenance.json")

    with open(raw_path, "rb") as fh:
        blob = fh.read()
    sha = hashlib.sha256(blob).hexdigest()
    text = blob.decode("utf-8-sig")

    lines = []
    n = 0
    for raw in text.splitlines():
        if CONTENT_LINE.match(raw):
            continue
        chunks = [raw]
        # ai-summary/undiarized blobs are giant unwrapped paragraphs — split
        # into sentence-level lines so beats can be anchored meaningfully
        if source_class in ("ai-summary", "undiarized") and len(raw) > 400:
            sents = re.split(r"(?<=[.!?])\s+", raw)
            if source_class == "undiarized":
                # keep sentence granularity so turn-boundary heuristics work
                chunks = sents
            else:
                chunks, buf = [], ""
                for s in sents:
                    buf = (buf + " " + s).strip()
                    if len(buf) >= 400:
                        chunks.append(buf); buf = ""
                if buf:
                    chunks.append(buf)
        for chunk in chunks:
            n += 1
            lines.append(f"L{n:04d}: [{source_class}] {chunk}")

    if source_class == "undiarized":
        lines = _mark_turn_boundaries(lines)

    header = (
        f"# {session_id} — SECONDARY-SOURCE INDEX\n"
        f"# source_class: {source_class}\n"
        f"# source_file: {os.path.relpath(raw_path, base_dir)}\n"
        f"# sha256: {sha}\n"
        f"# NOTE: {NOTE[source_class]}\n"
        f"# Parity coverage still applies, but 'attribution' here is structural\n"
        f"# (which doc section a beat came from), not speaker identity.\n\n")
    with open(indexed_path, "w", encoding="utf-8") as fh:
        fh.write(header + "\n".join(lines) + "\n")

    prov = {
        "session_id": session_id,
        "source_class": source_class,
        "source_file": os.path.relpath(raw_path, base_dir).replace("\\", "/"),
        "sha256": sha,
        "content_lines": n,
        "diarized": False,
        "needs_generation": source_class == "ai-summary",
        "needs_diarization": source_class == "undiarized",
        "note": NOTE[source_class],
    }
    with open(provenance_path, "w", encoding="utf-8") as fh:
        json.dump(prov, fh, indent=2)

    print(f"Indexed {session_id} ({source_class}): {n} content lines")
    print(f"  -> {indexed_path}")
    print(f"  sha256: {sha[:16]}…")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("session_id")
    p.add_argument("--source-class", required=True,
                   choices=["ai-summary", "survey", "undiarized"])
    p.add_argument("--out-dir")
    p.add_argument("--raw")
    a = p.parse_args()
    index_secondary(a.session_id, a.source_class, out_dir=a.out_dir,
                    raw_path=a.raw)
