import json
import hashlib

def main():
    raw_path = "sessions/data/index/s7.5-raw-indexed.md"
    sha = hashlib.sha256(open(raw_path, "rb").read()).hexdigest()
    total_lines = sum(1 for _ in open(raw_path, "r", encoding="utf-8"))

    manifest = {
        "session_id": "s7.5",
        "raw_file": "sessions/data/index/s7.5-raw-indexed.md",
        "raw_file_hash": sha,
        "total_raw_lines": total_lines,
        "target_word_budget": 2500,
        "scene_blocks": [
            {
                "scene_id": 1,
                "title": "Aggie's VIP Day & The Spore Recipe",
                "line_range": [1, 111],
                "raw_line_count": 111,
                "speakers_present": ["Aggie", "Angela Galaspora", "Valentine Sterling Sr.", "Cade Ashveil", "Pip", "Bramble", "Valentine Sterling Jr."],
                "dialogue_ledger": [
                    {"line": 27, "speaker": "Angela Galaspora", "gist": "Hey girls! Just the Mizizi I was looking for. Come with me—we have a day ahead!", "covers": [1, 35]},
                    {"line": 45, "speaker": "Angela Galaspora", "gist": "Is Britt okay, child? She looks... slouched. Out of breath.", "covers": [36, 50]},
                    {"line": 56, "speaker": "Angela Galaspora", "gist": "I thought she looked strange. She does not look too bad, but I get a strange feeling of deja vu...", "covers": [51, 60]},
                    {"line": 63, "speaker": "Angela Galaspora", "gist": "Ah Mr. Cade, thank you thank you for arranging this adventure and pass my thanks along to Lady Ignis!", "covers": [61, 65]},
                    {"line": 68, "speaker": "Valentine Sterling Sr.", "gist": "Hello Elder Angela, welcome to the Zephyr, please note it is a Reso race not resy...", "covers": [66, 70]},
                    {"line": 72, "speaker": "Angela Galaspora", "gist": "Well I think our fellow Mycelium Circle member Rill had something to do with one of the teams...", "covers": [71, 74]},
                    {"line": 76, "speaker": "Cade Ashveil", "gist": "Well these ferns are great, almost as cool as the rocks out in the race.", "covers": [75, 83]},
                    {"line": 90, "speaker": "Valentine Sterling Jr.", "gist": "I'm glad you're here. I wanted to pick you guys up from the dorms myself...", "covers": [84, 92]},
                    {"line": 95, "speaker": "Valentine Sterling Jr.", "gist": "Look, you need to be ready. I plan to lock myself in my room to study tonight...", "covers": [93, 111]}
                ],
                "ooc": False
            },
            {
                "scene_id": 2,
                "title": "Britt's VIP Day & The Basalt Wager",
                "line_range": [112, 207],
                "raw_line_count": 96,
                "speakers_present": ["Britt", "Angela Galaspora", "Valentine Sterling Sr.", "Cade Ashveil", "Valerius Sterling", "Valentine Sterling Jr."],
                "dialogue_ledger": [
                    {"line": 119, "speaker": "Angela Galaspora", "gist": "Hey girls! Just the Mizizi I was looking for. Come with me—we have a day ahead!", "covers": [112, 132]},
                    {"line": 146, "speaker": "Angela Galaspora", "gist": "Ah Mr. Cade, thank you thank you for arranging this adventure and pass my thanks along to Lady Ignis!", "covers": [133, 148]},
                    {"line": 151, "speaker": "Valentine Sterling Sr.", "gist": "Hello Elder Angela, welcome to the Zephyr, please note it is a Reso race not resy...", "covers": [149, 153]},
                    {"line": 155, "speaker": "Angela Galaspora", "gist": "Well I think our fellow Mycelium Circle member Rill had something to do with one of the teams...", "covers": [154, 157]},
                    {"line": 159, "speaker": "Cade Ashveil", "gist": "Well these ferns are great, almost as cool as the rocks out in the race.", "covers": [158, 172]},
                    {"line": 187, "speaker": "Valentine Sterling Jr.", "gist": "I'm glad you're here. I wanted to pick you guys up from the dorms myself...", "covers": [173, 189]},
                    {"line": 192, "speaker": "Valentine Sterling Jr.", "gist": "Look, you need to be ready. I plan to lock myself in my room to study tonight...", "covers": [190, 207]}
                ],
                "ooc": False
            }
        ]
    }

    out_path = "sessions/data/index/s7.5-manifest.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote {out_path} with {len(manifest['scene_blocks'])} blocks.")

if __name__ == "__main__":
    main()
