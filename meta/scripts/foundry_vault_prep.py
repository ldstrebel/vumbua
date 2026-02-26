import os
import re
import shutil

# Ensure paths are relative to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
EXPORT_VAULT_DIR = os.path.join(PROJECT_ROOT, "meta", "foundry-export-vault")

# Directories to copy
TARGET_DIRS = [
    "characters",
    "locations",
    "factions"
]

# Supported image extensions
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}

def clean_vault():
    """Wipe the existing export vault to ensure a clean slate."""
    if os.path.exists(EXPORT_VAULT_DIR):
        shutil.rmtree(EXPORT_VAULT_DIR)
    os.makedirs(EXPORT_VAULT_DIR)

def scrub_markdown(content):
    """
    Search for the GM Notes header. If found, truncate the string right before it.
    Matches variations like:
    ## GM Notes
    ## GM Notes [HIDDEN FROM PLAYERS]
    """
    match = re.search(r'(^|\n)(#+\s*GM Notes.*)(\n|$)', content, re.IGNORECASE)
    if match:
        return content[:match.start()]
    return content

def extract_links_from_markdown(content):
    """Extract all [[wiki-links]] from markdown text, returning their normalized kebab-case targets."""
    links = set()
    for match in re.finditer(r'\[\[(.*?)(?:\|.*?)?\]\]', content):
        target = match.group(1).strip()
        # Normalize to the expected filename format (e.g. "Percival Vane-Smythe III" -> "percival-vane-smythe-iii")
        target_kebab = target.lower().replace(' ', '-')
        links.add(target_kebab)
    return links

def build_known_links_whitelist():
    """Scan non-NPC files (sessions, PCs, locations, factions) to build a whitelist of known entities."""
    whitelist = set()
    source_dirs = [
        "sessions/transcripts/clean",
        "sessions",  # for index.md
        "characters/player-characters",
        "locations",
        "factions"
    ]
    
    for relative_dir in source_dirs:
        dir_path = os.path.join(PROJECT_ROOT, relative_dir.replace("/", os.sep))
        if not os.path.exists(dir_path):
            continue
            
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.md'):
                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        content = f.read()
                    whitelist.update(extract_links_from_markdown(content))
                    
    return whitelist

def process_and_copy_file(src_path, dest_path):
    """Copy a file. If it's markdown, scrub it first. Ensure directories exist."""
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    ext = os.path.splitext(src_path)[1].lower()
    
    if ext == '.md':
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        scrubbed_content = scrub_markdown(content)
        
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(scrubbed_content)
    elif ext in IMAGE_EXTENSIONS:
        shutil.copy2(src_path, dest_path)

def build_vault():
    """Copy over all targeted locations, scrubbing secrets and filtering NPCs."""
    known_links = build_known_links_whitelist()
    print(f"Found {len(known_links)} unique wiki-links to use as an NPC whitelist.")
    
    for dirname in TARGET_DIRS:
        src_dir = os.path.join(PROJECT_ROOT, dirname)
        if not os.path.exists(src_dir):
            continue
            
        for root, _, files in os.walk(src_dir):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                base_name = os.path.splitext(file)[0].lower()
                
                # NPC Filtering Logic
                is_npc_file = "characters" in root and "npcs" in root
                if is_npc_file and ext == '.md' and base_name not in known_links:
                    # Skip unmet NPCs
                    continue
                
                if ext == '.md' or ext in IMAGE_EXTENSIONS:
                    src_path = os.path.join(root, file)
                    rel_path = os.path.relpath(src_path, PROJECT_ROOT)
                    dest_path = os.path.join(EXPORT_VAULT_DIR, rel_path)
                    process_and_copy_file(src_path, dest_path)

def generate_party_overview():
    """Generate the 'Party Overview.md' from the sessions/index.md file."""
    session_index_path = os.path.join(PROJECT_ROOT, "sessions", "index.md")
    dest_path = os.path.join(EXPORT_VAULT_DIR, "Party Overview.md")
    
    if not os.path.exists(session_index_path):
        print("Warning: sessions/index.md not found. Skipping Party Overview generation.")
        return
        
    with open(session_index_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Standardize the document for Foundry players
    header = "# Party Overview\n\n> A chronicle of the party's journey through Vumbua.\n\n"
    
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(header + content)

if __name__ == "__main__":
    print(f"Building sanitized Foundry VTT export vault at: {EXPORT_VAULT_DIR}")
    clean_vault()
    build_vault()
    generate_party_overview()
    print("Done! Ready for Lava Flow import.")
