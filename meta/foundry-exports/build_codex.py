import json
import base64
import os
import re
import sys
from datetime import datetime

# Reconfigure stdout to use utf-8 to prevent encoding errors when printing to console
sys.stdout.reconfigure(encoding='utf-8')

# Paths
BASE_DIR = r'd:\Code\vumbua'
PORTRAITS_DIR = os.path.join(BASE_DIR, 'meta', 'foundry-exports', 'portraits')
OUTPUT = os.path.join(BASE_DIR, 'meta', 'foundry-exports', 'vumbua-codex.json')
NPC_DIR = os.path.join(BASE_DIR, 'characters', 'npcs')
PC_DIR = os.path.join(BASE_DIR, 'characters', 'player-characters')
SESSION_DIR = os.path.join(BASE_DIR, 'sessions', 'transcripts', 'clean')
LOCATION_DIR = os.path.join(BASE_DIR, 'locations')
FACTION_DIR = os.path.join(BASE_DIR, 'factions')
WORLD_DIR = os.path.join(BASE_DIR, 'world')

# Parse command line for delta export
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
    "greek row": "The Spire-Scape",
    "industrial zone": "The Spire-Scape",
    "great library": "The Spire-Scape",
    "power plant": "Block 99",
}

def register_link(slug, display_name):
    """Registers a mapping from a slug or alias (e.g. 'vumbua-academy') to a display name ('Vumbua Academy')."""
    if slug and display_name:
        LINK_MAP[slug.lower()] = display_name
        LINK_MAP[slug.lower().replace("-", " ")] = display_name
        LINK_MAP[slug.lower().replace(" ", "_")] = display_name

def extract_aliases(content):
    """Extracts aliases from a file's YAML frontmatter."""
    aliases = []
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        # Check for list style with indented or non-indented dashes:
        # aliases:
        #   - Val
        # aliases:
        # - Val
        list_match = re.search(r"aliases:\s*\n(([ \t]*-\s+[^\n]*\n?)+)", fm_text)
        if list_match:
            for line in list_match.group(1).split("\n"):
                line = line.strip()
                if line.startswith("-"):
                    aliases.append(line[1:].strip().strip('"').strip("'"))
        else:
            # Check for inline list style: aliases: [Val, Valentine]
            inline_match = re.search(r"aliases:\s*\[(.*?)\]", fm_text)
            if inline_match:
                for item in inline_match.group(1).split(","):
                    aliases.append(item.strip().strip('"').strip("'"))
            else:
                # Check for single string style: aliases: Val
                single_match = re.search(r"aliases:\s*([^\n]+)", fm_text)
                if single_match:
                    val = single_match.group(1).strip().strip('"').strip("'")
                    if not val.startswith("["):
                        aliases.append(val)
    return aliases

def get_player_facing_content(content):
    """Strips frontmatter, H1 headers, and GM secrets/narration to extract player-facing content."""
    # 1. Strip YAML frontmatter
    content = re.sub(r'^---.*?---\s*\n', '', content, flags=re.DOTALL)
    
    # 2. Strip top H1 title
    content = re.sub(r'^# .*?\n', '', content)
    
    # 3. Strip GM secrets and GM narration (non-greedy, stopping at next header or end of file)
    content = re.sub(r'## GM Secrets.*?(?=\n## |\n---|\Z)', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'## GM Narration.*?(?=\n## |\n---|\Z)', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    return content.strip()

def safe_split_cells(line):
    """Splits a markdown table row by pipes '|', ignoring pipes inside [[wikilinks]]."""
    def replace_pipe(match):
        return match.group(0).replace('|', '__PIPE__')
    
    # Temporarily hide pipes inside wikilinks
    temp_line = re.sub(r'\[\[.*?\]\]', replace_pipe, line)
    
    cells = [c.strip() for c in temp_line.split('|')]
    if line.strip().startswith('|'):
        cells = cells[1:]
    if line.strip().endswith('|') and len(cells) > 0:
        cells = cells[:-1]
        
    # Restore hidden pipes
    restored_cells = [c.replace('__PIPE__', '|').strip() for c in cells]
    return restored_cells

def markdown_to_html(text):
    """Enhanced markdown to HTML conversion for Foundry."""
    if not text: return ""
    
    # Pre-processing: Strip GM Secrets
    text = re.sub(r'## GM Secrets.*?(?=\n## |\n---|\Z)', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'## GM Narration.*?(?=\n## |\n---|\Z)', '', text, flags=re.DOTALL | re.IGNORECASE)

    # Tables: Improved parsing using safe split
    lines = text.split('\n')
    new_lines = []
    in_table = False
    for line in lines:
        if line.strip().startswith('|') and '|' in line:
            if not in_table:
                new_lines.append('<table style="border-collapse: collapse; width: 100%;">')
                in_table = True
            cells = safe_split_cells(line)
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

    # 1. Image/File Embeds: ![[target]] or ![[target|alias]]
    def resolve_embed(match):
        raw_content = match.group(1).strip()
        parts = re.split(r'\\?\|', raw_content, 1)
        target = parts[0].strip()
        target_clean = target.replace('\\', '/').split('/')[-1].strip()
        ext = os.path.splitext(target_clean.lower())[1]
        
        if ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']:
            return f"<img src='{target_clean}' alt='{target_clean}' />"
        else:
            return f"<span>Embed: {target_clean}</span>"

    text = re.sub(r'!\[\[([^\]\n]+?)\]\]', resolve_embed, text)

    # 2. Links [[target|alias]] or [[target]]
    def resolve_link(match):
        raw_content = match.group(1).strip()
        parts = re.split(r'\\?\|', raw_content, 1)
        target = parts[0].strip()
        alias = parts[1].strip() if len(parts) > 1 else target
        
        # Clean backslashes and folder prefixes from target
        target = target.replace('\\', '/').split('/')[-1].strip()
        alias = alias.replace('\\', '').strip()
        
        # Split headers (e.g., [[file#header]])
        if "#" in target:
            target = target.split("#", 1)[0].strip()
            
        # Check canonical map
        resolved = LINK_MAP.get(target.lower()) or LINK_MAP.get(target.lower().replace(" ", "-")) or LINK_MAP.get(target.lower().replace(" ", "_")) or target
        return f"{{{{page:{resolved}|{alias}}}}}"

    text = re.sub(r'\[\[([^\]\n]+?)\]\]', resolve_link, text)
    
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

# Global tracker for NPC/PC/Location/Faction updates
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
    """Extracts a section starting with #+ section_name until the next header of same or higher level, or ---."""
    escaped_name = re.escape(section_name)
    header_pattern = rf'(?:^|[\n])(#+)\s*{escaped_name}\b[^\n]*\n'
    header_match = re.search(header_pattern, content, re.IGNORECASE)
    if not header_match:
        return ""
        
    header_level = len(header_match.group(1))
    start_pos = header_match.end()
    
    remaining = content[start_pos:]
    next_header_pattern = rf'\n(#{{1,{header_level}}})\s+[^\n]*\n|\n---'
    next_match = re.search(next_header_pattern, remaining)
    if next_match:
        return remaining[:next_match.start()].strip()
    else:
        divider_match = re.search(r'\n---', remaining)
        if divider_match:
            return remaining[:divider_match.start()].strip()
        return remaining.strip()

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
                
                delta_text = extract_section(content, "Session Delta") or extract_section(content, "Entity Delta")
                if delta_text:
                    lines = delta_text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line: continue
                        m = re.search(r'(?:^[-*]\s+)(?:\*\*|)?\[\[(.*?)(?:\|.*?)?\]\](?:\*\*|)?(?:\s*[:—-]\s*)(.*)', line)
                        if m:
                            entity_name, update_text = m.groups()
                            register_update(entity_name, sess_id, update_text)

# Discover active sessions
active_sessions = []
if os.path.exists(SESSION_DIR):
    for fname in os.listdir(SESSION_DIR):
        match = re.search(r's(\d+\.?\d*)-clean\.md', fname)
        if match:
            sid = match.group(1).lstrip('0')
            if sid == "" or sid.startswith('.'): sid = "0" + sid
            active_sessions.append(sid)

active_sessions = sorted(list(set(active_sessions)), key=float)
print(f"Active Sessions (Normalized): {active_sessions}")

if target_session:
    print(f"Running DELTA export for Session {target_session}")

# Pass 0: Register all links dynamically from file names, H1s, and frontmatter aliases
def register_file_links(fpath, default_slug):
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract H1 name
        h1_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
        display_name = h1_match.group(1).strip() if h1_match else default_slug
        
        # Register slug
        register_link(default_slug, display_name)
        
        # Register aliases
        aliases = extract_aliases(content)
        for alias in aliases:
            register_link(alias, display_name)
    except Exception as e:
        print(f"Error registering links for {fpath}: {e}")

def populate_link_map():
    print("Pass 0: Registering all entity links...")
    
    # 1. Register Chronicle sessions (all variants)
    for sess_id in active_sessions:
        display_name = f"Session {sess_id}"
        variants = [
            f"session-{sess_id}",
            f"s{sess_id}",
            f"session-{sess_id}-clean",
            f"s{sess_id}-clean",
            f"session-{sess_id}-plan",
            f"s{sess_id}-plan"
        ]
        try:
            val = float(sess_id)
            is_int = val.is_integer()
            val_int = int(val)
        except ValueError:
            is_int = False
            val_int = None
            
        if val_int is not None:
            if is_int:
                variants.extend([
                    f"session-{val_int}",
                    f"session-{val_int:02d}",
                    f"s{val_int}",
                    f"s{val_int:02d}",
                    f"session-{val_int}-clean",
                    f"session-{val_int:02d}-clean",
                    f"s{val_int}-clean",
                    f"s{val_int:02d}-clean",
                    f"session-{val_int}-plan",
                    f"session-{val_int:02d}-plan",
                    f"s{val_int}-plan",
                    f"s{val_int:02d}-plan",
                ])
            else:
                variants.extend([
                    f"session-{val:04.1f}", # 02.5
                    f"session-{val}",      # 2.5
                    f"s{val:04.1f}",
                    f"s{val}",
                    f"session-{val:04.1f}-clean",
                    f"session-{val}-clean",
                    f"s{val:04.1f}-clean",
                    f"s{val}-clean",
                ])
        for var in variants:
            register_link(var, display_name)
        
    # 2. Scan PCs
    if os.path.exists(PC_DIR):
        for fname in os.listdir(PC_DIR):
            if fname.endswith('.md'):
                fpath = os.path.join(PC_DIR, fname)
                register_file_links(fpath, fname[:-3])
                
    # 3. Scan NPCs
    if os.path.exists(NPC_DIR):
        for fname in os.listdir(NPC_DIR):
            if fname.endswith('.md') and fname not in ['index.md', 'captains-dossier.md', 'lucky-timeline.md']:
                fpath = os.path.join(NPC_DIR, fname)
                register_file_links(fpath, fname[:-3])
                
    # 4. Scan Locations
    if os.path.exists(LOCATION_DIR):
        for fname in os.listdir(LOCATION_DIR):
            if fname.endswith('.md') and fname != 'index.md':
                fpath = os.path.join(LOCATION_DIR, fname)
                register_file_links(fpath, fname[:-3])
                
    # 5. Scan Factions
    if os.path.exists(FACTION_DIR):
        for root, dirs, files in os.walk(FACTION_DIR):
            for fname in files:
                if fname.endswith('.md') and fname != 'index.md':
                    fpath = os.path.join(root, fname)
                    register_file_links(fpath, fname[:-3])
                    
    # 6. Scan World Lore
    if os.path.exists(WORLD_DIR):
        for root, dirs, files in os.walk(WORLD_DIR):
            for fname in files:
                if fname.endswith('.md') and fname != 'index.md':
                    fpath = os.path.join(root, fname)
                    register_file_links(fpath, fname[:-3])

    # 7. Scan Bestiary
    bestiary_dir = os.path.join(BASE_DIR, 'bestiary')
    if os.path.exists(bestiary_dir):
        for fname in os.listdir(bestiary_dir):
            if fname.endswith('.md') and fname != 'index.md':
                fpath = os.path.join(bestiary_dir, fname)
                register_file_links(fpath, fname[:-3])

    # 8. Scan Glossary
    glossary_path = os.path.join(BASE_DIR, 'glossary.md')
    if os.path.exists(glossary_path):
        try:
            with open(glossary_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in lines:
                m = re.match(r'^\s*\*\*(.*?)\*\*', line)
                if m:
                    term_content = m.group(1).strip()
                    clean_term = re.sub(r'\[\[(.*?)(?:\|.*?)?\]\]', r'\1', term_content).strip()
                    clean_term = clean_term.split('(')[0].strip()
                    if clean_term:
                        term_lower = clean_term.lower()
                        if term_lower not in LINK_MAP and term_lower.replace(" ", "-") not in LINK_MAP:
                            register_link(clean_term, "Glossary")
        except Exception as e:
            print(f"Error parsing glossary links: {e}")

# Run Pass 0 & Pass 1
populate_link_map()
parse_deltas()

# Initialize data structure
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
        "locations": {"name": "Locations", "pages": []},
        "factions": {"name": "Factions", "pages": []},
        "world": {"name": "World Lore", "pages": []}
    },
    "portraits": {}
}

# 3. Process Chronicle
sort_idx = 0
for sess_id in active_sessions:
    if target_session and sess_id != target_session:
        sort_idx += 100
        continue

    found_sess = False
    patterns = [f"s{sess_id}-clean.md", f"s{float(sess_id):0>2g}-clean.md", f"s{int(float(sess_id)):02d}-clean.md"]
    for pattern in patterns:
        fpath = os.path.join(SESSION_DIR, pattern)
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            summary = extract_section(content, "Quick Summary") or extract_section(content, "Session Summary")
            delta = extract_section(content, "Session Delta") or extract_section(content, "Entity Delta")
            knowledge = extract_section(content, "Player Knowledge Changes")
            
            full_content = f"## Session {sess_id}\n"
            if summary: full_content += f"### Summary\n{summary}\n"
            if delta: full_content += f"### Changes & Updates\n{delta}\n"
            if knowledge: full_content += f"### Knowledge Acquired\n{knowledge}\n"
            
            if not summary and not delta:
                player_facing = get_player_facing_content(content)
                if player_facing:
                    full_content += f"{player_facing}\n"
            
            if summary or delta or "## Session" in full_content and len(full_content.strip()) > len(f"## Session {sess_id}"):
                page_name = f"Session {sess_id}"
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
            h1_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
            name = h1_match.group(1) if h1_match else fname[:-3]
            
            player_content = get_player_facing_content(content)
            
            # Add Recent Activity
            updates = GLOBAL_UPDATES.get(name) or GLOBAL_UPDATES.get(fname[:-3])
            if updates:
                activity_content = "\n### Recent Activity\n"
                for sess, text in updates:
                    activity_content += f"- **{sess}**: {text}\n"
                player_content += activity_content
            
            pc_content = f"## {name}\n{player_content}"
            
            data["journals"]["pcs"]["pages"].append({
                "name": name,
                "sort": sort_idx,
                "content": markdown_to_html(pc_content)
            })
            sort_idx += 100

# 5. Process NPCs
sort_idx = 100
for fname in sorted(os.listdir(NPC_DIR)):
    if fname.endswith('.md') and fname not in ['index.md', 'captains-dossier.md', 'lucky-timeline.md']:
        fpath = os.path.join(NPC_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            h1_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
            name = h1_match.group(1) if h1_match else fname[:-3]
        
        # Check First Appearance
        should_include = not target_session
        app_sess = "unknown"
        app_match = re.search(r'First Appearance.*?\s*\|\s*\[\[session-(.*?)[\\|\]]', content, re.IGNORECASE)
        if app_match:
            app_sess = app_match.group(1).strip().lstrip('0')
            if app_sess == "" or app_sess.startswith('.'): app_sess = "0" + app_sess
            should_include = (not target_session and app_sess in active_sessions) or (target_session and app_sess == target_session)
            
        if should_include:
            print(f"  Found NPC: {name} (First: {app_sess})")
            
            # Extract Daggerheart stats for Actor creation
            stats_section = extract_section(content, "Daggerheart Stats")
            stats = {}
            if stats_section:
                for m in re.finditer(r'\|\s*\*\*(.*?)\*\*\s*\|\s*([+-]?\d+)\s*\|', stats_section):
                    stat_key = m.group(1).lower()[:3]
                    stats[stat_key] = int(m.group(2))
                
                m_thresh = re.search(r'Minor\s*(\d+)\s*/\s*Major\s*(\d+)', stats_section)
                if m_thresh:
                    stats['thresholds'] = {'minor': int(m_thresh.group(1)), 'major': int(m_thresh.group(2))}
                
                for m in re.finditer(r'\|\s*\*\*(HP|Stress|Evasion)\*\*\s*\|\s*(\d+)\s*\|', stats_section):
                    stats[m.group(1).lower()] = int(m.group(2))

            portrait_fname = f"{slugify(name)}_portrait.png"
            img_tag = ""
            if os.path.exists(os.path.join(PORTRAITS_DIR, portrait_fname)):
                data["portraits"][portrait_fname] = load_portrait(portrait_fname)
                img_tag = f"<img src='portraits/{portrait_fname}' width='200' style='float:right;margin:0 0 10px 10px;border-radius:8px;'/>"
            
            overview = extract_section(content, "Overview")
            if stats:
                if "actors" not in data: data["actors"] = []
                data["actors"].append({
                    "name": name,
                    "img": f"portraits/{portrait_fname}",
                    "stats": stats,
                    "biography": markdown_to_html(overview)
                })

            player_content = get_player_facing_content(content)
            
            # Add Recent Activity
            updates = GLOBAL_UPDATES.get(name) or GLOBAL_UPDATES.get(fname[:-3])
            if updates:
                activity_content = "\n### Recent Activity\n"
                for sess, text in updates:
                    activity_content += f"- **{sess}**: {text}\n"
                player_content += activity_content
            
            npc_content = f"## {name}\n{img_tag}\n{player_content}"
            
            data["journals"]["npcs"]["pages"].append({
                "name": name,
                "sort": sort_idx,
                "content": markdown_to_html(npc_content)
            })
            sort_idx += 100

# 6. Process Locations (Dynamically processing all files)
sort_idx = 100
for fname in sorted(os.listdir(LOCATION_DIR)):
    if fname.endswith('.md') and fname != 'index.md':
        fpath = os.path.join(LOCATION_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
            h1_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
            name = h1_match.group(1) if h1_match else fname[:-3]
            
            player_content = get_player_facing_content(content)
            
            # Add Recent Activity
            updates = GLOBAL_UPDATES.get(name) or GLOBAL_UPDATES.get(fname[:-3])
            if updates:
                activity_content = "\n### Recent Activity\n"
                for sess, text in updates:
                    activity_content += f"- **{sess}**: {text}\n"
                player_content += activity_content
            
            loc_content = f"## {name}\n{player_content}"
            
            data["journals"]["locations"]["pages"].append({
                "name": name,
                "sort": sort_idx,
                "content": markdown_to_html(loc_content)
            })
            sort_idx += 100

# 7. Process Factions (Dynamically processing all clans and harmony groups)
sort_idx = 100
if os.path.exists(FACTION_DIR):
    for root, dirs, files in os.walk(FACTION_DIR):
        for fname in sorted(files):
            if fname.endswith('.md') and fname != 'index.md':
                fpath = os.path.join(root, fname)
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    h1_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
                    name = h1_match.group(1) if h1_match else fname[:-3]
                    
                    player_content = get_player_facing_content(content)
                    
                    # Add Recent Activity
                    updates = GLOBAL_UPDATES.get(name) or GLOBAL_UPDATES.get(fname[:-3])
                    if updates:
                        activity_content = "\n### Recent Activity\n"
                        for sess, text in updates:
                            activity_content += f"- **{sess}**: {text}\n"
                        player_content += activity_content
                        
                    faction_content = f"## {name}\n{player_content}"
                    
                    data["journals"]["factions"]["pages"].append({
                        "name": name,
                        "sort": sort_idx,
                        "content": markdown_to_html(faction_content)
                    })
                    sort_idx += 100

# 8. Process World Lore (Dynamically processing all files in world/)
sort_idx = 100
if os.path.exists(WORLD_DIR):
    for root, dirs, files in os.walk(WORLD_DIR):
        for fname in sorted(files):
            # Include all .md files in world except index.md and the survey json/exam files if nested
            if fname.endswith('.md') and fname != 'index.md':
                fpath = os.path.join(root, fname)
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    h1_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
                    name = h1_match.group(1) if h1_match else fname[:-3]
                    
                    player_content = get_player_facing_content(content)
                    
                    # Add Recent Activity
                    updates = GLOBAL_UPDATES.get(name) or GLOBAL_UPDATES.get(fname[:-3])
                    if updates:
                        activity_content = "\n### Recent Activity\n"
                        for sess, text in updates:
                            activity_content += f"- **{sess}**: {text}\n"
                        player_content += activity_content
                        
                    world_content = f"## {name}\n{player_content}"
                    
                    data["journals"]["world"]["pages"].append({
                        "name": name,
                        "sort": sort_idx,
                        "content": markdown_to_html(world_content)
                    })
                    sort_idx += 100

# 9. Process Bestiary (Dynamically processing all files in bestiary/ and adding them to world)
bestiary_dir = os.path.join(BASE_DIR, 'bestiary')
if os.path.exists(bestiary_dir):
    for fname in sorted(os.listdir(bestiary_dir)):
        if fname.endswith('.md') and fname != 'index.md':
            fpath = os.path.join(bestiary_dir, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
                h1_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
                name = h1_match.group(1) if h1_match else fname[:-3]
                
                player_content = get_player_facing_content(content)
                
                # Add Recent Activity
                updates = GLOBAL_UPDATES.get(name) or GLOBAL_UPDATES.get(fname[:-3])
                if updates:
                    activity_content = "\n### Recent Activity\n"
                    for sess, text in updates:
                        activity_content += f"- **{sess}**: {text}\n"
                    player_content += activity_content
                    
                world_content = f"## {name}\n{player_content}"
                
                data["journals"]["world"]["pages"].append({
                    "name": name,
                    "sort": sort_idx,
                    "content": markdown_to_html(world_content)
                })
                sort_idx += 100

# 10. Process Glossary (Processing glossary.md from root and adding to world)
glossary_path = os.path.join(BASE_DIR, 'glossary.md')
if os.path.exists(glossary_path):
    with open(glossary_path, 'r', encoding='utf-8') as f:
        content = f.read()
    h1_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
    name = h1_match.group(1) if h1_match else "Glossary"
    
    player_content = get_player_facing_content(content)
    world_content = f"## {name}\n{player_content}"
    
    data["journals"]["world"]["pages"].append({
        "name": name,
        "sort": sort_idx,
        "content": markdown_to_html(world_content)
    })
    sort_idx += 100

# 11. Final Save
with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

size_mb = os.path.getsize(OUTPUT) / (1024*1024)
print(f"\nFinal Codex Size: {size_mb:.2f} MB")
print(f"NPCs: {len(data['journals']['npcs']['pages'])}")
print(f"Locations: {len(data['journals']['locations']['pages'])}")
print(f"Factions: {len(data['journals']['factions']['pages'])}")
print(f"World Lore: {len(data['journals']['world']['pages'])}")
print(f"Total Pages: {sum(len(j['pages']) for j in data['journals'].values())}")
