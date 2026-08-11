import re

def search_stadium_announcement():
    with open("sessions/transcripts/raw/s12-raw.md", "r", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"Total lines in s12-raw.md: {len(lines)}")
    
    keywords = ["speaker", "announc", "intercom", "stadium", "passed", "arena", "voice", "crackl", "PA ", "system", "broadcast", "microph", "audio", "trial"]

    matching_lines = []
    for idx, line in enumerate(lines, 1):
        for kw in keywords:
            if kw.lower() in line.lower():
                matching_lines.append((idx, line.strip()))
                break

    print(f"\nFound {len(matching_lines)} matching lines in s12-raw.md:\n")
    for idx, content in matching_lines[:40]:
        print(f"Line {idx}: {content[:120]}")

if __name__ == '__main__':
    search_stadium_announcement()
