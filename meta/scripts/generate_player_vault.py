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
        
    # 2. Extract facts for Known NPCs
    npc_knowledge = defaultdict(list)
    current_session = "Unknown Session"
    
    # We want to iterate line by line to track which session we are in
    for line in overview_content.split('\n'):
        # Track session headers like `### [[Session 00|Session 0: The Trials]]`
        session_match = re.match(r'^###\s+(\[\[.*?\]\])', line)
        if session_match:
            current_session = session_match.group(1)
            continue
            
        # Look for bullet points
        if line.strip().startswith('-'):
            # Find all links
            for link_match in re.finditer(r'\[\[(.*?)(?:\|.*?)?\]\]', line):
                target = link_match.group(1).strip()
                kebab_target = target.lower().replace(' ', '-')
                
                # Check if this target is an NPC
                npc_path = os.path.join(PROJECT_ROOT, "characters", "npcs", f"{kebab_target}.md")
                if os.path.exists(npc_path):
                    # Clean up the bullet point parsing slightly
                    clean_fact = re.sub(r'^-', '', line).strip()
                    npc_knowledge[kebab_target].append((current_session, clean_fact))
                    
    # Write Known NPCs
    known_npcs_lines = [
        "# Known NPCs",
        "> A compendium of individuals the party has encountered, and exactly what is known about them so far.\n"
    ]
    
    for npc_kebab, facts in sorted(npc_knowledge.items()):
        npc_path = os.path.join(PROJECT_ROOT, "characters", "npcs", f"{npc_kebab}.md")
        npc_name = npc_kebab.replace('-', ' ').title()
        
        # Pull actual display name from the NPC file
        if os.path.exists(npc_path):
            with open(npc_path, 'r', encoding='utf-8') as f:
                content = f.read()
                title_match = re.search(r'^#\s+(.*?)$', content, re.MULTILINE)
                if title_match:
                    npc_name = title_match.group(1)
                    
        # Remove duplicates while preserving order
        unique_facts = []
        seen = set()
        for session_link, fact in facts:
            sig = (session_link, fact)
            if sig not in seen:
                seen.add(sig)
                unique_facts.append(sig)
                
        if unique_facts:
            known_npcs_lines.append(f"## [[{npc_kebab}|{npc_name}]]")
            for session_link, fact in unique_facts:
                known_npcs_lines.append(f"- {fact} *(Source: {session_link})*")
            known_npcs_lines.append("")
        
    npcs_path = os.path.join(EXPORT_VAULT_DIR, "Known NPCs.md")
    with open(npcs_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(known_npcs_lines))

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
