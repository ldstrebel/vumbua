import sys
import os
import re
import hashlib
import json

def load_aliases():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    aliases_path = os.path.join(script_dir, "speaker_aliases.json")
    if os.path.exists(aliases_path):
        with open(aliases_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def prep_raw(session_id):
    # Path setup
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # under vumbua/sessions/
    raw_path = os.path.join(base_dir, "transcripts", "raw", f"{session_id}-raw.md")
    index_dir = os.path.join(base_dir, "transcripts", "index")
    os.makedirs(index_dir, exist_ok=True)
    indexed_path = os.path.join(index_dir, f"{session_id}-raw-indexed.md")

    if not os.path.exists(raw_path):
        print(f"Error: Raw transcript file not found at {raw_path}")
        sys.exit(1)

    aliases = load_aliases()
    processed_lines = []

    with open(raw_path, "r", encoding="utf-8") as f:
        for line in f:
            # 1. Normalize line endings & strip trailing whitespace
            line = line.replace("\r\n", "\n").replace("\r", "\n").rstrip()
            
            # 2. Skip empty lines
            if not line:
                continue

            # 3. Apply canonical speaker alias mapping to speaker labels only
            # Look for lines starting with **Speaker Name:**
            match = re.match(r"^\*\*([^*]+):\*\*\s*(.*)$", line)
            if match:
                speaker = match.group(1).strip()
                dialogue = match.group(2)
                if speaker in aliases:
                    canonical = aliases[speaker]
                    line = f"**{canonical}:** {dialogue}"

            processed_lines.append(line)

    # 4. Prefix with immutable line numbers (L0001: )
    final_lines = []
    for idx, line in enumerate(processed_lines, 1):
        final_lines.append(f"L{idx:04d}: {line}\n")

    # Write output file
    with open(indexed_path, "w", encoding="utf-8") as f:
        f.writelines(final_lines)

    # 5. Compute SHA-256 of the INDEXED file
    sha256 = hashlib.sha256()
    with open(indexed_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    file_hash = sha256.hexdigest()

    print(f"Indexed file created: {indexed_path}")
    print(f"SHA-256: {file_hash}")
    return file_hash

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prep_raw.py <session_id> (e.g. s12)")
        sys.exit(1)
    prep_raw(sys.argv[1])
