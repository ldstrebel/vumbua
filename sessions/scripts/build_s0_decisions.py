"""Build canonical s0-attribution-decisions.json deterministically.

Session 0 is a pure session-zero: collaborative worldbuilding + character creation.
There is no in-fiction play, so "OOC" here means non-canon table talk
(logistics, social outro, date artifacts) vs canon creation material (which gets
the prologue treatment downstream).

Shared mic: 'Luke S' carries Luke S (GM) and Kristina. Evidence for Kristina
lines: she is addressed as "Christina"/"Christina's character" and the Luke S
stream answers in first person about her character's design/relationship.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEXED = ROOT / "transcripts" / "index" / "s0-raw-indexed.md"
OUT = ROOT / "transcripts" / "index" / "s0-attribution-decisions.json"

# --- OOC declarations (non-canon: logistics/social/artifacts) ---------------
OOC_RANGES = [
    {"from": 1, "to": 3,
     "note": "Transcript header/date artifacts."},
    {"from": 615, "to": 631,
     "note": "Survey-link logistics: sending the trials link, screenshot "
             "instructions, 'send just to you or the group'."},
    {"from": 653, "to": 671,
     "note": "Screenshot-cropping + survey-tool meta: 'need the bottom', dice "
             "roll didn't work, tree-building UI, 'didn't play test the "
             "balance'."},
    {"from": 731, "to": 772,
     "note": "Social outro: sick baby, Puerto Rico trip, pina coladas; "
             "transcription footer."},
]
OOC_LINES = {
    # scattered admin inside canon flow
    683: "Admin: 'at this point you'll have enough to create your character.'",
}

# --- Shared-mic decomposition -----------------------------------------------
# Luke S stream lines attributed to Kristina (player, pre-Aggie naming).
KRISTINA = {
    78: "Answers Sophie's 'Christina, what do you think?' in first person "
        "(distant relatives / cousins / same year).",
    80: "Continuation of her answer.",
    82: "Continuation of her answer.",
    90: "'we go to school but we're very different groups' — elaborating the "
        "cousins-but-not-close dynamic.",
    349: "Sophie says 'correct me if you think I'm wrong here, Christina' — "
         "softening 'aggressive' to 'passionate' is her reply.",
    365: "Ack bridging into her character description.",
    367: "'I was thinking mine was going to be pretty skeptical in like a "
         "more quiet like' — describing HER character.",
    369: "Continuation: 'suspicious but'.",
    372: "Continuation ack.",
    383: "'mine... she's a little bit quieter... wary of Harmony... going to "
         "uncover the conspiracy' — defining her character's worldview.",
    388: "low-confidence: 'Hell yeah' to Sophie's shared-backstory proposal.",
    407: "'Um, not officially yet' — answering 'does your character have a "
         "name?'",
    409: "'We're waiting for the names to come to' (continues into 411).",
    411: "'us.' — end of the names answer.",
    413: "'my character would be kind of like looking for... a darker corner' "
         "— describing her character's arrival reaction.",
    416: "Continuation: darker/safe spot, 'she like kind of waddles off'.",
    418: "'spot.' — tail of her answer.",
    420: "'Uh, shapewise turtle,' — answering 'more turtle or more fungus?'",
    422: "mushroom-side colors/textures + 'the only thing that I've really "
         "decided on my character is... the red and'.",
    424: "'white spotted mushroom.'",
    428: "'that you drop into when you get I can turtle and like suck into'.",
    430: "'the paci.' — shell detail continuation.",
    433: "'Is it soft? Is it like a harder shell? I don't know.' — "
         "self-questioning design talk.",
    437: "'I'm kind of leaning on the mushroom side...' — design lean.",
    439: "'We'll see what your classes are...' — deferring design to class "
         "choice.",
    443: "'the only other character detail I need is like do we have huge "
         "eyes... Medium small.' — self-answering design riff.",
    445: "'Okay.' — closing the design beat.",
}

def load_lines():
    pat = re.compile(r"^L(\d+): \*\*([^*]+):\*\*\s*(.*)$")
    out = []
    for raw in open(INDEXED, encoding="utf-8"):
        m = pat.match(raw.rstrip("\n"))
        if m:
            out.append((int(m.group(1)), m.group(2).strip(), m.group(3)))
    return out

def main():
    lines = load_lines()
    mics = {"Luke S": {"lines": {}}}
    kristina = luke = 0
    for n, stream, _text in lines:
        if stream != "Luke S":
            continue
        if n in KRISTINA:
            mics["Luke S"]["lines"][str(n)] = [
                {"identity": "Kristina", "note": KRISTINA[n]}]
            kristina += 1
        else:
            mics["Luke S"]["lines"][str(n)] = [{"identity": "GM"}]
            luke += 1
    decisions = {
        "session_id": "s0",
        "_note": "s0 is pure session-zero creation talk; 'ooc' marks "
                 "non-canon social/logistics, NOT non-fiction. All creation "
                 "talk is prologue material downstream.",
        "ooc_ranges": OOC_RANGES,
        "ooc_lines": {str(k): v for k, v in OOC_LINES.items()},
        "mics": mics,
    }
    OUT.write_text(json.dumps(decisions, indent=2), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"  Luke S stream: {luke} GM, {kristina} Kristina")

if __name__ == "__main__":
    main()
