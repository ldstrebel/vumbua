import json

def build_decisions():
    decisions = {
        "session_id": "s7.5",
        "_note": "Attribution decisions for s7.5 survey source on shared mic Luke S (carries GM, Britt, Aggie).",
        "ooc_ranges": [],
        "ooc_lines": {},
        "mics": {
            "Luke S": {
                "lines": {}
            }
        }
    }

    # Lines 1 to 102: Aggie's VIP Day
    # Lines 103 to 198: Britt's VIP Day

    aggie_decision_lines = {22, 27, 32, 40, 43, 48, 55, 68, 71, 74, 77, 82, 87, 101}
    britt_decision_lines = {114, 119, 124, 128, 131, 138, 151, 154, 161, 164, 171, 174, 179, 184, 198}

    for line_no in range(1, 199):
        if line_no in aggie_decision_lines:
            identity = "Aggie"
        elif line_no in britt_decision_lines:
            identity = "Britt"
        else:
            identity = "GM"

        decisions["mics"]["Luke S"]["lines"][str(line_no)] = [{"identity": identity}]

    with open("sessions/transcripts/index/s7.5-attribution-decisions.json", "w", encoding="utf-8") as f:
        json.dump(decisions, f, indent=2)
    print("Generated s7.5-attribution-decisions.json with 198 lines.")

if __name__ == "__main__":
    build_decisions()
