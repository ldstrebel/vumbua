import json, base64, os, re, sys
from datetime import datetime

# Paths — auto-detect repo root from this script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..'))
PORTRAITS_DIR = os.path.join(SCRIPT_DIR, 'portraits')
OUTPUT = os.path.join(SCRIPT_DIR, 'vumbua-codex.json')
NPC_DIR = os.path.join(BASE_DIR, 'characters', 'npcs')
PC_DIR = os.path.join(BASE_DIR, 'characters', 'player-characters')
SESSION_DIR = os.path.join(BASE_DIR, 'sessions', 'transcripts', 'clean')
LOCATION_DIR = os.path.join(BASE_DIR, 'locations')

# Parse command line for delta export
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
LINK_MAP = {
    "session-00": "Session 0",
    "session-01": "Session 1",
    "session-02": "Session 2",
    "session-02.5": "Session 2.5",
    "session-03": "Session 3",
    "session-04": "Session 4",
    "session-0": "Session 0",
    "session-0.5": "Session 0.5",
    "session-1": "Session 1",
    "session-2": "Session 2",
    "session-2.5": "Session 2.5",
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
    "valerius sterling": "Valentine \"Val\" Sterling",
    "valerius-sterling": "Valentine \"Val\" Sterling",
}

def register_link(slug, display_name):
    """Registers a mapping from a slug to a display name."""
    if slug and display_name:
        LINK_MAP[slug.lower()] = display_name
        LINK_MAP[slug.lower().replace("-", " ")] = display_name
        LINK_MAP[slug.lower().replace(" ", "_")] = display_name

def markdown_to_html(text):
    """Enhanced markdown to HTML conversion for Foundry."""
    if not text: return ""

    # Pre-processing: Strip GM Secrets and GM Notes
    text = re.sub(r'## GM Secrets.*?(?=\n## |\n---|\Z)', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'## GM Notes.*?(?=\n## |\n---|\Z)', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'\*\*GM Notes?:?\*\*.*?(?=\n## |\n---|\n\n|\Z)', '', text, flags=re.DOTALL | re.IGNORECASE)
    # Strip callout blocks (GM secrets, notes, etc.)
    text = re.sub(r'> \[!CAUTION\].*?(?=\n[^>]|\Z)', '', text, flags=re.DOTALL)
    text = re.sub(r'> \[!WARNING\].*?NOT YET REVEALED.*?(?=\n[^>]|\Z)', '', text, flags=re.DOTALL)
    text = re.sub(r'> \[!NOTE\].*?(?=\n[^>]|\Z)', '', text, flags=re.DOTALL)

    # Strip backslash before pipe/bracket in wiki links (Obsidian artifact)
    # Must happen BEFORE table parsing so [[link\|alias]] doesn't split on |
    text = re.sub(r'\\([|\]])', r'\1', text)

    # Resolve wiki links BEFORE table parsing to avoid | conflicts
    def resolve_link(match):
        groups = match.groups()
        target = groups[0].strip()
        alias = groups[1].strip() if len(groups) > 1 and groups[1] else target
        resolved = LINK_MAP.get(target.lower()) or LINK_MAP.get(target.lower().replace(" ", "-")) or target
        return f"{{{{page:{resolved}|{alias}}}}}"

    text = re.sub(r'\[\[([^|\]]+?)(?:\|([^\]]+?))?\]\]', resolve_link, text)

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
            if all(re.match(r'^[\s:-]+$', c) for c in cells): continue
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

    # Bold/Italic
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)

    # Headings
    text = re.sub(r'^#### (.*?)$', r'<h5>\1</h5>', text, flags=re.MULTILINE)
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
    text = text.replace('<p></p>', '')
    text = re.sub(r'<p>\s*</p>', '', text)

    return text

# Global tracker for NPC/PC/Location updates from session deltas
GLOBAL_UPDATES = {}

def register_update(entity_name, session_id, text):
    """Stores an update for an entity to be appended to their page later."""
    if not entity_name or not text: return
    clean_name = re.sub(r'\[\[(.*?)(?:\|.*?)?\]\]', r'\1', entity_name).strip()
    if clean_name not in GLOBAL_UPDATES:
        GLOBAL_UPDATES[clean_name] = []
    GLOBAL_UPDATES[clean_name].append((f"Session {session_id}", text))

def slugify(text):
    return text.lower().replace(' ', '_').replace('-', '_').replace('.', '_')

def extract_section(content, section_name):
    """Extracts a section starting with ## section_name until the next ## or ---."""
    pattern = rf'(?:^|[\n])(?:#+)\s*{re.escape(section_name)}\s*[\n](.*?)(?=\n#+ |\n---|\Z)'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE | re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""

def extract_session_title(content):
    """Extracts a descriptive session title from frontmatter or H1 header."""
    # Try frontmatter title: field
    fm_match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', content, re.MULTILINE)
    if fm_match:
        title = fm_match.group(1).strip()
        subtitle = re.sub(r'^Session\s+\d+[\.\d]*\s*:\s*', '', title)
        if subtitle and subtitle != title:
            return subtitle
        return title

    # Try H1 header: # Session N: Subtitle
    h1_match = re.search(r'^# .*?:\s*(.+)$', content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()

    # Try H1 with dash: # Session N - Subtitle
    h1_dash = re.search(r'^# .*?-\s*(.+)$', content, re.MULTILINE)
    if h1_dash:
        return h1_dash.group(1).strip()

    return None

def extract_narrative(content):
    """Extracts the full narrative content from a session file.

    Looks for rich content in this priority order:
    1. Named Parts (## Part 1: ..., ## Part 2: ...) -- used in Session 4
    2. Named Scenes (## Scenes / ### Scene 1: ...) -- used in Sessions 0-2.5
    3. Play-by-Play section (## Play-by-Play) -- used in Session 3
    4. Falls back to Summary if no narrative found
    """
    # Strategy 1: Extract ## Part N sections (Session 4 style)
    parts = re.findall(r'(^## Part \d+:.*?)(?=\n## |\Z)', content, re.DOTALL | re.MULTILINE)
    if parts:
        return '\n\n'.join(p.strip() for p in parts)

    # Strategy 2: Extract Scenes section (Sessions 0-2.5 style)
    scenes_section = extract_section(content, "Scenes")
    if scenes_section:
        return scenes_section

    # Strategy 3: Extract Play-by-Play section (Session 3 style)
    play_by_play = extract_section(content, "Play-by-Play")
    if play_by_play:
        return play_by_play

    # Strategy 4: Fallback -- summary
    summary = extract_section(content, "Quick Summary") or extract_section(content, "Session Summary")
    if summary:
        return summary

    return ""

def extract_npc_session(content):
    """Extracts the first-appearance session ID from an NPC file.
    Checks both 'First Appearance' and 'First Mentioned' fields."""
    for field in ['First Appearance', 'First Mentioned']:
        pattern = rf'{field}.*?\[\[session-(.*?)[\\\||\]]'
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            sess = match.group(1).lstrip('0')
            if sess == "" or sess.startswith('.'): sess = "0" + sess
            return sess
    return None

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
                        m = re.search(r'(?:^[-*]\s+)(?:\*\*|)?\[\[(.*?)(?:\|.*?)?\]\](?:\*\*|)?(?:\s*[:\u2014-]\s*)(.*)', line)
                        if m:
                            entity_name, update_text = m.groups()
                            register_update(entity_name, sess_id, update_text)

# -----------------------------------------------------------------------
# 1. Discover active sessions
# -----------------------------------------------------------------------
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

# Run Pass 1: Parse deltas for GLOBAL_UPDATES
parse_deltas()

# -----------------------------------------------------------------------
# 2. Build Codex structure
# -----------------------------------------------------------------------
data = {
    "meta": {
        "sessions": active_sessions,
        "deltaMode": target_session is not None,
        "targetSession": target_session,
        "generated": datetime.now().strftime("%Y-%m-%d"),
        "spoilerAudit": "Player-known facts only. No GM Notes, no hidden backstory, no planned content. Iggy race=Earthkin. Zephyr race=Unknown. Rill=Mizizi exchange student. NPC ranks removed \u2014 private info."
    },
    "journals": {
        "chronicle": {"name": "Campaign Chronicle", "pages": []},
        "pcs": {"name": "Player Characters", "pages": []},
        "npcs": {"name": "NPCs", "pages": []},
        "locations": {"name": "Locations", "pages": []}
    },
    "portraits": {}
}

# -----------------------------------------------------------------------
# 3. Process Chronicle -- full narrative play-by-play
# -----------------------------------------------------------------------

# Add arc overview page (not in delta mode)
if not target_session:
    max_sess = active_sessions[-1] if active_sessions else "0"
    data["journals"]["chronicle"]["pages"].append({
        "name": "The Intake",
        "sort": 0,
        "content": markdown_to_html(
            f"## Arc 1: The Intake\n"
            f"*Sessions 0\u2013{max_sess} cover the party's arrival at Vumbua Academy, "
            f"their first night, and the events leading up to their first day of class.*"
        )
    })

sort_idx = 100
for sess_id in active_sessions:
    if target_session and sess_id != target_session:
        sort_idx += 100
        continue

    # Find the session file
    patterns = [f"s{sess_id}-clean.md", f"s{float(sess_id):0>2g}-clean.md", f"s{int(float(sess_id)):02d}-clean.md"]
    for pattern in patterns:
        fpath = os.path.join(SESSION_DIR, pattern)
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract descriptive title
            subtitle = extract_session_title(content)
            if subtitle:
                page_name = f"Session {sess_id}: {subtitle}"
            else:
                page_name = f"Session {sess_id}"

            register_link(f"session-{sess_id}", page_name)
            register_link(f"session-{int(float(sess_id)):02d}", page_name)

            # Extract full narrative content
            narrative = extract_narrative(content)

            # Also grab summary for a lead-in
            summary = extract_section(content, "Quick Summary") or extract_section(content, "Session Summary")

            full_content = f"## {page_name}\n"
            if summary and narrative and summary != narrative:
                full_content += f"{summary}\n\n"
            if narrative:
                full_content += f"{narrative}\n"

            # Add key moments from Session Outcomes if available
            outcomes = extract_section(content, "Session Outcomes")
            if outcomes:
                full_content += f"\n### Session Outcomes\n{outcomes}\n"

            if narrative or summary:
                data["journals"]["chronicle"]["pages"].append({
                    "name": page_name,
                    "sort": sort_idx,
                    "content": markdown_to_html(full_content)
                })
                sort_idx += 100
                break

# -----------------------------------------------------------------------
# 4. Process PCs
# -----------------------------------------------------------------------
sort_idx = 100
for fname in sorted(os.listdir(PC_DIR)):
    # Skip non-markdown and excalidraw files
    if not fname.endswith('.md') or '.excalidraw' in fname:
        continue

    with open(os.path.join(PC_DIR, fname), 'r', encoding='utf-8') as f:
        content = f.read()
        name = fname[:-3].capitalize()
        h1_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
        if h1_match: name = h1_match.group(1)

        register_link(fname[:-3], name)
        overview = extract_section(content, "Overview")
        quest = extract_section(content, "Quest Tracker")
        key_moments = extract_section(content, "Key Moments")

        pc_content = f"## {name}\n"

        # Look for portrait
        portrait_fname = f"{slugify(name)}_portrait.png"
        if os.path.exists(os.path.join(PORTRAITS_DIR, portrait_fname)):
            data["portraits"][portrait_fname] = load_portrait(portrait_fname)
            pc_content += f"<img src='portraits/{portrait_fname}' width='200' style='float:right;margin:0 0 10px 10px;border-radius:8px;'/>\n"

        if overview:
            pc_content += f"{overview}\n"

        # Add Recent Activity from deltas
        updates = GLOBAL_UPDATES.get(name) or GLOBAL_UPDATES.get(fname[:-3])
        if updates:
            pc_content += "### Recent Activity\n"
            for sess, text in updates:
                pc_content += f"- **{sess}**: {text}\n"

        if key_moments:
            pc_content += f"\n### Key Moments\n{key_moments}\n"
        if quest:
            pc_content += f"\n### Quest Tracker\n{quest}"

        data["journals"]["pcs"]["pages"].append({
            "name": name,
            "sort": sort_idx,
            "content": markdown_to_html(pc_content)
        })
        sort_idx += 100

# -----------------------------------------------------------------------
# 5. Process NPCs -- include all that have appeared in active sessions
# -----------------------------------------------------------------------
SKIP_NPC_FILES = {'index.md', 'captains-dossier.md', 'resonance-racers.md'}

sort_idx = 100
for fname in sorted(os.listdir(NPC_DIR)):
    if not fname.endswith('.md') or fname in SKIP_NPC_FILES:
        continue

    fpath = os.path.join(NPC_DIR, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
        h1_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
        name = h1_match.group(1) if h1_match else fname[:-3].replace('-', ' ').title()
        register_link(fname[:-3], name)

    # Determine first appearance session
    app_sess = extract_npc_session(content)

    # Inclusion logic:
    # - In delta mode: only include NPCs whose first appearance matches target session
    # - In full mode: include all NPCs that have a first appearance in any active session,
    #   OR NPCs with no session data but that reference sessions (include for completeness)
    if target_session:
        should_include = (app_sess == target_session)
    else:
        if app_sess:
            should_include = app_sess in active_sessions
        else:
            has_session_content = bool(re.search(r'Session \d', content, re.IGNORECASE))
            should_include = has_session_content

    if not should_include:
        continue

    print(f"  Found NPC: {name} (First: {app_sess or 'unknown'})")

    overview = extract_section(content, "Overview")
    known = extract_section(content, "What Players Know")
    interactions = extract_section(content, "Interactions") or extract_section(content, "Session Appearances")

    # Look for portrait
    portrait_fname = f"{slugify(name)}_portrait.png"
    img_tag = ""
    if os.path.exists(os.path.join(PORTRAITS_DIR, portrait_fname)):
        data["portraits"][portrait_fname] = load_portrait(portrait_fname)
        img_tag = f"<img src='portraits/{portrait_fname}' width='200' style='float:right;margin:0 0 10px 10px;border-radius:8px;'/>"

    # Build NPC page
    role_match = re.search(r'\*\*Role\*\*.*?\|\s*(.*?)\s*\|', content)
    first_seen_label = f"Session {app_sess}" if app_sess else "Background"

    npc_content = f"## {name}\n{img_tag}\n"

    # Add overview table
    role_text = role_match.group(1).strip() if role_match else ""
    if role_text or app_sess:
        npc_content += "<table>"
        if role_text:
            npc_content += f"<tr><td><strong>Role</strong></td><td>{role_text}</td></tr>"
        npc_content += f"<tr><td><strong>First Seen</strong></td><td>{first_seen_label}</td></tr>"
        npc_content += "</table>\n"

    if overview:
        short_name = name.split('(')[0].strip().split('"')[0].strip()
        npc_content += f"### Who Is {short_name}?\n{overview}\n"

    # Add Recent Activity from deltas
    updates = GLOBAL_UPDATES.get(name) or GLOBAL_UPDATES.get(fname[:-3])
    if updates:
        npc_content += "### Recent Activity\n"
        for sess, text in updates:
            npc_content += f"- **{sess}**: {text}\n"

    if interactions:
        npc_content += f"\n### Interactions\n{interactions}\n"
    elif known:
        npc_content += f"\n### What Players Know\n{known}\n"

    data["journals"]["npcs"]["pages"].append({
        "name": name,
        "sort": sort_idx,
        "content": markdown_to_html(npc_content)
    })
    sort_idx += 100

# -----------------------------------------------------------------------
# 6. Process Locations
# -----------------------------------------------------------------------
key_locations = [
    "Vumbua Academy", "Mizizi Petrified Forest",
    "Block 04", "Block 12", "Block 99",
    "Celestial Lounge", "Walker-Core",
    "Apex Ring", "Lucky's Supply Room",
]

sort_idx = 100
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

            # Add Recent Activity from deltas
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

# -----------------------------------------------------------------------
# 7. Embed portrait images
# -----------------------------------------------------------------------
for fname in sorted(os.listdir(PORTRAITS_DIR)):
    if fname.endswith('.png') and '_portrait.png' in fname and fname not in data['portraits']:
        if re.match(r'^[a-z_]+_portrait\.png$', fname):
            b64 = load_portrait(fname)
            if b64:
                data['portraits'][fname] = b64

# -----------------------------------------------------------------------
# 8. Save output
# -----------------------------------------------------------------------
with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

size_mb = os.path.getsize(OUTPUT) / (1024*1024)
print(f"\nOutput: {size_mb:.1f} MB")

# -----------------------------------------------------------------------
# 9. Validation
# -----------------------------------------------------------------------
pages = []
for j in data['journals'].values():
    pages.extend(j['pages'])
names = set(p['name'] for p in pages)
all_content = ' '.join(p['content'] for p in pages)
links = re.findall(r'\{\{page:([^|}]+)', all_content)
missing = [l for l in links if l not in names]
img_refs = set(re.findall(r"src='portraits/([^']+)'", all_content))
missing_imgs = img_refs - set(data['portraits'].keys())

print(f"Pages: {len(pages)}")
print(f"  Chronicle: {len(data['journals']['chronicle']['pages'])}")
print(f"  PCs: {len(data['journals']['pcs']['pages'])}")
print(f"  NPCs: {len(data['journals']['npcs']['pages'])}")
print(f"  Locations: {len(data['journals']['locations']['pages'])}")
print(f"Portraits: {len(data['portraits'])}")
print(f"Links: {len(links)} ({len(set(links))} unique)")
print(f"Unresolvable: {missing if missing else 'None'}")
print(f"Image refs: {len(img_refs)}, missing: {missing_imgs if missing_imgs else 'None'}")

# Spoiler audit
for term in ['gold-rank', 'silver-rank', 'copper-rank', 'trench-kin', 'GM Note', 'GM SECRET']:
    found = [p['name'] for p in pages if term.lower() in p['content'].lower()]
    if found:
        print(f"SPOILER WARNING: '{term}' found in: {found}")
