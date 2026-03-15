import json, base64, os, re, sys
from datetime import datetime

# Paths
BASE_DIR = r'd:\Code\vumbua'
PORTRAITS_DIR = os.path.join(BASE_DIR, 'meta', 'foundry-exports', 'portraits')
OUTPUT = os.path.join(BASE_DIR, 'meta', 'foundry-exports', 'vumbua-codex.json')
NPC_DIR = os.path.join(BASE_DIR, 'characters', 'npcs')
PC_DIR = os.path.join(BASE_DIR, 'characters', 'player-characters')
SESSION_DIR = os.path.join(BASE_DIR, 'sessions', 'transcripts', 'clean')
LOCATION_DIR = os.path.join(BASE_DIR, 'locations')

# NEW: Parse command line for delta export
# Usage: python build_codex.py [session_id]
# Example: python build_codex.py 4  (Only exports Session 4 and its new NPCs)
target_session = sys.argv[1] if len(sys.argv) > 1 else None
if target_session:
    target_session = str(target_session).lstrip('0')
    if target_session == "" or target_session.startswith('.'): target_session = "0" + target_session

# Helper to load portrait as base64
def load_portrait(filename):
    path = os.path.join(PORTRAITS_DIR, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return base64.b64encode(f.read()).decode('ascii')
    return None

# Link Mapping (Canonical lookup)
# Mapping of file slugs/aliases to their Foundry Page Names
LINK_MAP = {
    "session-00": "Session 0",
    "session-01": "Session 1",
    "session-02": "Session 2",
    "session-03": "Session 3",
    "session-04": "Session 4",
    "session-0.5": "Session 0.5",
    "session-1": "Session 1",
    "session-2": "Session 2",
    "session-3": "Session 3",
    "session-4": "Session 4",
    "s0": "Session 0",
    "s1": "Session 1",
    "s2": "Session 2",
    "s3": "Session 3",
    "s4": "Session 4",
    "mizizi": "Mizizi Petrified Forest",
    "academy": "Vumbua Academy",
    "lucky": "Lucky",
    "val": "Valentine \"Val\" Sterling",
}

def register_link(slug, display_name):
    """Registers a mapping from a slug (e.g. 'vumbua-academy') to a display name ('Vumbua Academy')."""
    if slug and display_name:
        LINK_MAP[slug.lower()] = display_name
        LINK_MAP[slug.lower().replace("-", " ")] = display_name
        LINK_MAP[slug.lower().replace(" ", "_")] = display_name

def markdown_to_html(text):
    """Enhanced markdown to HTML conversion for Foundry."""
    if not text: return ""
    
    # Pre-processing: Strip GM Secrets
    text = re.sub(r'## GM Secrets.*?(?=\n## |\n---|\Z)', '', text, flags=re.DOTALL | re.IGNORECASE)

    # Tables: Improved parsing
    lines = text.split('\n')
    new_lines = []
    in_table = False
    for line in lines:
        if line.strip().startswith('|') and '|' in line:
            if not in_table:
                new_lines.append('<table style="border-collapse: collapse; width: 100%;">')
                in_table = True
            cells = [c.strip() for c in line.split('|') if c.strip() or line.count('|') > 1]
            if not cells: continue 
            if all(re.match(r'^[\s:-]+$', c) for c in cells): continue # Skip separator
            
            row_style = "border: 1px solid #ccc; padding: 8px;"
            row_html = "<tr>"
            for cell in cells:
                tag = "th" if not any(l.startswith('<tr>') for l in new_lines[-2:]) and len(new_lines) > 0 and 'table' in new_lines[-1] else "td"
                row_html += f"<{tag} style='{row_style}'>{cell}</{tag}>"
            row_html += "</tr>"
            new_lines.append(row_html)
        else:
            if in_table:
                new_lines.append('</table>')
                in_table = False
            new_lines.append(line)
    if in_table: new_lines.append('</table>')
    text = '\n'.join(new_lines)

    # Links [[target|alias]] or [[target]]
    def resolve_link(match):
        groups = match.groups()
        target = groups[0].strip()
        alias = groups[1].strip() if len(groups) > 1 and groups[1] else target
        
        # Check canonical map
        resolved = LINK_MAP.get(target.lower()) or LINK_MAP.get(target.lower().replace(" ", "-")) or target
        return f"{{{{page:{resolved}|{alias}}}}}"

    # Combined regex to avoid multiple passes and index errors
    text = re.sub(r'\[\[([^|\]]+?)(?:\|([^\]]+?))?\]\]', resolve_link, text)
    
    # Bold/Italic
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    
    # Headings
    text = re.sub(r'^### (.*?)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    
    # Lists: Cleaner wrapping
    def wrap_list(m):
        items = m.group(0).strip().split('\n')
        list_html = "<ul>"
        for item in items:
            list_html += f"<li>{re.sub(r'^- ', '', item)}</li>"
        list_html += "</ul>"
        return list_html

    text = re.sub(r'(^- .*(\n|$))+', wrap_list, text, flags=re.MULTILINE)
    
    # Paragraphs and line breaks
    text = text.replace('\r\n', '\n')
    # Protect existing tags from being wrapped in <p>
    blocks = re.split(r'(<table.*?</table>|<ul.*?</ul>|<h\d.*?>.*?</h\d>|<img.*?>)', text, flags=re.DOTALL)
    new_blocks = []
    for block in blocks:
        if block.startswith('<'):
            new_blocks.append(block)
        else:
            p_block = block.strip()
            if p_block:
                p_block = p_block.replace('\n\n', '</p><p>')
                p_block = p_block.replace('\n', '<br/>')
                new_blocks.append(f"<p>{p_block}</p>")
    
    text = "".join(new_blocks)
    
    # Final cleanup
    text = text.replace('<p></p>', '')
    text = re.sub(r'<p>\s*</p>', '', text)
    
    return text

# Global tracker for NPC/PC/Location updates
GLOBAL_UPDATES = {} # { "Entity Name": [ ("Session 1", "Update text"), ... ] }

def register_update(entity_name, session_id, text):
    """Stores an update for an entity to be appended to their page later."""
    if not entity_name or not text: return
    # Clean entity name from [[ ]] if present
    clean_name = re.sub(r'\[\[(.*?)(?:\|.*?)?\]\]', r'\1', entity_name).strip()
    if clean_name not in GLOBAL_UPDATES:
        GLOBAL_UPDATES[clean_name] = []
    GLOBAL_UPDATES[clean_name].append((f"Session {session_id}", text))

def slugify(text):
    return text.lower().replace(' ', '_').replace('-', '_').replace('.', '_')

def extract_section(content, section_name):
    """Extracts a section starting with ## section_name until the next ## or ---."""
    # Handle multiple possible header levels for the section
    pattern = rf'(?:^|[\n])(?:#+)\s*{section_name}\s*[\n](.*?)(?=\n#+ |\n---|\Z)'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE | re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""

def parse_deltas():
    """First pass: Scan all session files for Entity/Session Deltas."""
    print("Pass 1: Parsing Entity Deltas...")
    for sess_id in active_sessions:
        patterns = [f"s{sess_id}-clean.md", f"s{float(sess_id):0>2g}-clean.md", f"s{int(float(sess_id)):02d}-clean.md"]
        for pattern in patterns:
            fpath = os.path.join(SESSION_DIR, pattern)
            if os.path.exists(fpath):
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Look for "Session Delta" or "Entity Delta" (Session 3 uses Entity Delta)
                delta_text = extract_section(content, "Session Delta") or extract_section(content, "Entity Delta")
                if delta_text:
                    # Parse bullet points: - [[Name]] — Update
                    # Or: * **[[Name]]**: Update
                    lines = delta_text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line: continue
                        # Regex to catch: - [[Name]] — Text OR * **[[Name]]**: Text
                        m = re.search(r'(?:^[-*]\s+)(?:\*\*|)?\[\[(.*?)(?:\|.*?)?\]\](?:\*\*|)?(?:\s*[:—-]\s*)(.*)', line)
                        if m:
                            entity_name, update_text = m.groups()
                            register_update(entity_name, sess_id, update_text)

# 1. Discover active sessions
active_sessions = []
if os.path.exists(SESSION_DIR):
    for fname in os.listdir(SESSION_DIR):
        match = re.search(r's(\d+\.?\d*)-clean\.md', fname)
        if match:
            # Normalize: "00" -> "0", "02.5" -> "2.5"
            sid = match.group(1).lstrip('0')
            if sid == "" or sid.startswith('.'): sid = "0" + sid # Handle "0" or "0.5"
            active_sessions.append(sid)

active_sessions = sorted(list(set(active_sessions)), key=float)
print(f"Active Sessions (Normalized): {active_sessions}")

if target_session:
    print(f"Running DELTA export for Session {target_session}")

# Run Pass 1
parse_deltas()

# 2. Build Codex
data = {
    "meta": {
        "sessions": active_sessions,
        "deltaMode": target_session is not None,
        "targetSession": target_session,
        "generated": datetime.now().strftime("%Y-%m-%d"),
        "spoilerAudit": "Dynamic filtering based on First Appearance tags. GM-only sections stripped."
    },
    "journals": {
        "chronicle": {"name": "Campaign Chronicle", "pages": []},
        "pcs": {"name": "Player Characters", "pages": []},
        "npcs": {"name": "NPCs", "pages": []},
        "locations": {"name": "Locations", "pages": []}
    },
    "portraits": {}
}

# 3. Process Chronicle
sort_idx = 0
for sess_id in active_sessions:
    # If delta mode, skip other sessions
    if target_session and sess_id != target_session:
        sort_idx += 100
        continue

    found_sess = False
    # Check multiple patterns
    patterns = [f"s{sess_id}-clean.md", f"s{float(sess_id):0>2g}-clean.md", f"s{int(float(sess_id)):02d}-clean.md"]
    for pattern in patterns:
        fpath = os.path.join(SESSION_DIR, pattern)
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Combine Summary + Delta (Ensuring Session 3 looks better)
            summary = extract_section(content, "Quick Summary") or extract_section(content, "Session Summary")
            delta = extract_section(content, "Session Delta") or extract_section(content, "Entity Delta")
            knowledge = extract_section(content, "Player Knowledge Changes")
            
            full_content = f"## Session {sess_id}\n"
            if summary: full_content += f"### Summary\n{summary}\n"
            if delta: full_content += f"### Changes & Updates\n{delta}\n"
            if knowledge: full_content += f"### Knowledge Acquired\n{knowledge}\n"
            
            if summary or delta:
                page_name = f"Session {sess_id}"
                register_link(f"session-{sess_id}", page_name)
                data["journals"]["chronicle"]["pages"].append({
                    "name": page_name,
                    "sort": sort_idx,
                    "content": markdown_to_html(full_content)
                })
                sort_idx += 100
                found_sess = True
                break

# 4. Process PCs
sort_idx = 100
for fname in sorted(os.listdir(PC_DIR)):
    if fname.endswith('.md'):
        with open(os.path.join(PC_DIR, fname), 'r', encoding='utf-8') as f:
            content = f.read()
            name = fname[:-3].capitalize()
            h1_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
            if h1_match: name = h1_match.group(1)
            
            register_link(fname[:-3], name)
            overview = extract_section(content, "Overview")
            quest = extract_section(content, "Quest Tracker")
            
            pc_content = f"## {name}\n{overview}\n"
            
            # Add Recent Activity
            updates = GLOBAL_UPDATES.get(name) or GLOBAL_UPDATES.get(fname[:-3])
            if updates:
                pc_content += "### Recent Activity\n"
                for sess, text in updates:
                    pc_content += f"- **{sess}**: {text}\n"
            
            pc_content += f"\n### Quest Tracker\n{quest}"
            
            data["journals"]["pcs"]["pages"].append({
                "name": name,
                "sort": sort_idx,
                "content": markdown_to_html(pc_content)
            })
            sort_idx += 100

# 5. Process NPCs
sort_idx = 100
for fname in sorted(os.listdir(NPC_DIR)):
    if fname.endswith('.md') and fname != 'index.md':
        fpath = os.path.join(NPC_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            h1_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
            name = h1_match.group(1) if h1_match else fname[:-3]
            register_link(fname[:-3], name)
        
        # Check First Appearance
        app_match = re.search(r'First Appearance.*?\s*\|\s*\[\[session-(.*?)[\\|\]]', content, re.IGNORECASE)
        if app_match:
            app_sess = app_match.group(1).lstrip('0')
            if app_sess == "" or app_sess.startswith('.'): app_sess = "0" + app_sess
            
            # Target logic: Include if session matches, OR if no target session (Full mode)
            should_include = (not target_session and app_sess in active_sessions) or (target_session and app_sess == target_session)
            
            if should_include:
                print(f"  Found NPC: {name} (First: {app_sess})")
                
                overview = extract_section(content, "Overview")
                known = extract_section(content, "What Players Know")
                
                # Look for portrait
                portrait_fname = f"{slugify(name)}_portrait.png"
                img_tag = ""
                if os.path.exists(os.path.join(PORTRAITS_DIR, portrait_fname)):
                    # Important: Loaded into Base64 only if we are exporting this NPC
                    data["portraits"][portrait_fname] = load_portrait(portrait_fname)
                    img_tag = f"<img src='portraits/{portrait_fname}' width='200' style='float:right;margin:0 0 10px 10px;border-radius:8px;'/>"
                
                npc_content = f"## {name}\n{img_tag}\n{overview}\n"
                
                # Add Recent Activity
                updates = GLOBAL_UPDATES.get(name) or GLOBAL_UPDATES.get(fname[:-3])
                if updates:
                    npc_content += "### Recent Activity\n"
                    for sess, text in updates:
                        npc_content += f"- **{sess}**: {text}\n"
                
                npc_content += f"\n### What Players Know\n{known}"
                
                data["journals"]["npcs"]["pages"].append({
                    "name": name,
                    "sort": sort_idx,
                    "content": markdown_to_html(npc_content)
                })
                sort_idx += 100

# 6. Process Locations
sort_idx = 100
key_locations = ["Vumbua Academy", "Mizizi Petrified Forest", "Block 04", "Block 12", "Block 99", "Celestial Lounge", "Walker-Core", "Lucky's Supply Room"]

for loc_name in key_locations:
    slug = loc_name.lower().replace(" ", "-").replace("'", "")
    fname = slug + ".md"
    fpath = os.path.join(LOCATION_DIR, fname)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            h1_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
            name = h1_match.group(1) if h1_match else loc_name
            register_link(slug, name)
            
            overview = extract_section(content, "Overview")
            known = extract_section(content, "What Players Know")
            
            loc_content = f"## {name}\n{overview}\n"
            
            # Add Recent Activity
            updates = GLOBAL_UPDATES.get(name) or GLOBAL_UPDATES.get(slug)
            if updates:
                loc_content += "### Recent Activity\n"
                for sess, text in updates:
                    loc_content += f"- **{sess}**: {text}\n"

            loc_content += f"\n### What Players Know\n{known}"
            
            data["journals"]["locations"]["pages"].append({
                "name": name,
                "sort": sort_idx,
                "content": markdown_to_html(loc_content)
            })
            sort_idx += 100

# 7. Final Save
with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

size_mb = os.path.getsize(OUTPUT) / (1024*1024)
print(f"\nFinal Codex Size: {size_mb:.2f} MB")
print(f"NPCs: {len(data['journals']['npcs']['pages'])}")
print(f"Locations: {len(data['journals']['locations']['pages'])}")
print(f"Total Pages: {sum(len(j['pages']) for j in data['journals'].values())}")
