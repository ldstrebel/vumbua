import os
import re
import shutil
from collections import defaultdict

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
INDEX_FILE = os.path.join(PROJECT_ROOT, "sessions", "index.md")
EXPORT_VAULT_DIR = os.path.join(PROJECT_ROOT, "meta", "foundry-export-vault")

def generate_vault():
    os.makedirs(EXPORT_VAULT_DIR, exist_ok=True)
    
    # 1. Generate Party Overview by copying sessions/index.md
    overview_path = os.path.join(EXPORT_VAULT_DIR, "Party Overview.md")
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        index_content = f.read()

    # Rename the top header
    overview_content = index_content.replace("# Session Recaps", "# Party Overview\n> A chronicle of the party's journey and accumulated knowledge.\n\n## Session Recaps", 1)
    
    with open(overview_path, 'w', encoding='utf-8') as f:
        f.write(overview_content)
        
    # 2. Extract facts for Known NPCs and Locations
    knowledge = {
        "npcs": defaultdict(list),
        "locations": defaultdict(list)
    }
    current_session = "Unknown Session"
    
    for line in overview_content.split('\n'):
        # Track session headers like `### [[Session 00|Session 0: The Trials]]`
        session_match = re.match(r'^###\s+(\[\[.*?\]\])', line)
        if session_match:
            current_session = session_match.group(1)
            continue
            
        if line.strip().startswith('-'):
            for link_match in re.finditer(r'\[\[(.*?)(?:\|.*?)?\]\]', line):
                target = link_match.group(1).strip()
                kebab_target = target.lower().replace(' ', '-')
                
                # Check entity type
                npc_path = os.path.join(PROJECT_ROOT, "characters", "npcs", f"{kebab_target}.md")
                loc_path = os.path.join(PROJECT_ROOT, "locations", f"{kebab_target}.md")
                
                entity_type = None
                if os.path.exists(npc_path):
                    entity_type = "npcs"
                elif os.path.exists(loc_path):
                    entity_type = "locations"
                    
                if entity_type:
                    clean_fact = re.sub(r'^-', '', line).strip()
                    knowledge[entity_type][kebab_target].append((current_session, clean_fact))
                    
    # Write individual entity files
    for entity_type, entities in knowledge.items():
        base_dir = "characters/npcs" if entity_type == "npcs" else "locations"
        out_dir = os.path.join(EXPORT_VAULT_DIR, base_dir.replace("/", os.sep))
        os.makedirs(out_dir, exist_ok=True)
        
        for kebab_name, facts in entities.items():
            source_path = os.path.join(PROJECT_ROOT, base_dir.replace("/", os.sep), f"{kebab_name}.md")
            display_name = kebab_name.replace('-', ' ').title()
            
            # Extract actual display name
            if os.path.exists(source_path):
                with open(source_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    title_match = re.search(r'^#\s+(.*?)$', content, re.MULTILINE)
                    if title_match:
                        display_name = title_match.group(1).strip()
                        
            # Remove duplicate facts
            unique_facts = []
            seen = set()
            for session_link, fact in facts:
                sig = (session_link, fact)
                if sig not in seen:
                    seen.add(sig)
                    unique_facts.append(sig)
                    
            if unique_facts:
                out_lines = [
                    f"# {display_name}",
                    "",
                    "## Known Information"
                ]
                for session_link, fact in unique_facts:
                    out_lines.append(f"- {fact} *(Source: {session_link})*")
                    
                out_path = os.path.join(out_dir, f"{kebab_name}.md")
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write("\n".join(out_lines))

    # 3. Securely copy PCs and scrub GM Notes
    pcs_src = os.path.join(PROJECT_ROOT, "characters", "player-characters")
    pcs_dest = os.path.join(EXPORT_VAULT_DIR, "characters", "player-characters")
    
    if os.path.exists(pcs_src):
        shutil.copytree(pcs_src, pcs_dest, dirs_exist_ok=True)
        # Scrub GM Notes from cloned markdown files
        for root, _, files in os.walk(pcs_dest):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    gm_notes_idx = content.find("## GM Notes")
                    if gm_notes_idx != -1:
                        content = content[:gm_notes_idx].strip() + "\n"
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                            
if __name__ == "__main__":
    print(f"Generating spoiler-free player vault at: {EXPORT_VAULT_DIR}")
    generate_vault()
    print("Done! Party Overview, Known NPCs, and Player Characters generated.")
