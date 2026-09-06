"""Session completion gate — defines 'done' for a session.

A session's story is not accepted until this reports ALL PASS. The check
encodes the artifact chain: a clean story without a manifest/ledger is
UNVERIFIED PROSE, not a pipeline product (see the s8-s11 incident: stories
arrived with no manifests, so parity could not run).

Usage: python sessions/_scripts/session_status.py s8
       python sessions/_scripts/session_status.py        # all sessions
"""
import json, os, sys, glob

REQUIRED = [
    ("config",            "config/{sid}-session-config.json"),
    ("raw indexed",       "data/index/{sid}-raw-indexed.md"),
    ("attribution",       "data/index/{sid}-attribution.json"),
    ("manifest",          "data/index/{sid}-manifest.json"),
    ("blocks",            "data/clean/blocks/{sid}-scene-*.md"),
    ("clean attributed",  "data/clean/{sid}-clean-attributed.md"),
    ("clean story",       "data/clean/{sid}-clean-story.md"),
    ("assumptions",       "data/index/{sid}-assumptions.json"),
    ("novel mirror",      "../novel/sessions/{sid}-story.md"),
]

# sessions whose source class legitimately lacks some artifacts
EXEMPTIONS = {
    "survey":    {"config", "attribution"},   # s7.5: no audio, no speakers
    "ai-summary": {"config", "attribution"},  # s3: nothing to attribute
    "undiarized": {"config", "attribution"},  # s2.5 pending diarization
}

def provenance_class(sid, base):
    p = os.path.join(base, "data", "index", f"{sid}-provenance.json")
    if os.path.exists(p):
        try:
            return json.load(open(p, encoding="utf-8"))["source_class"]
        except Exception:
            pass
    return "diarized"

def check_session(sid, base):
    cls = provenance_class(sid, base)
    exempt = EXEMPTIONS.get(cls, set())
    results = []
    for label, pat in REQUIRED:
        if label in exempt:
            results.append((label, "EXEMPT", f"({cls})"))
            continue
        hits = glob.glob(os.path.join(base, pat.format(sid=sid)))
        results.append((label, "OK" if hits else "MISSING",
                        hits[0] if hits else pat.format(sid=sid)))
    return cls, results

def main():
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    sids = [sys.argv[1]] if len(sys.argv) > 1 else sorted(
        os.path.basename(f).split("-")[0]
        for f in glob.glob(os.path.join(base, "data/index/*-raw-indexed.md")))
    all_ok = True
    for sid in sids:
        cls, results = check_session(sid, base)
        missing = [r for r in results if r[1] == "MISSING"]
        status = "PASS" if not missing else "INCOMPLETE"
        if missing: all_ok = False
        print(f"\n=== {sid} [{cls}] -- {status} ===")
        for label, st, detail in results:
            mark = {"OK": "[OK]     ", "MISSING": "[MISSING]", "EXEMPT": "[-]      "}[st]
            print(f"  {mark}  {label}")
    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
