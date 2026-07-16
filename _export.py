
import os, shutil, zipfile

base = r'D:\Code\vumbua'
out  = os.path.join(base, '_notebooklm-export')
os.makedirs(out, exist_ok=True)

def merge(src_dir, pattern, out_name, recursive=False):
    parts = []
    walk = os.walk(src_dir) if recursive else [(src_dir, [], os.listdir(src_dir))]
    for root, dirs, files in walk:
        for fn in sorted(files):
            if fn.endswith('.md'):
                fp = os.path.join(root, fn)
                if os.path.getsize(fp) < 100:
                    continue
                rel = fp.replace(base + os.sep, '')
                parts.append('')
                parts.append('---')
                parts.append(f'## FILE: {rel}')
                parts.append('---')
                parts.append('')
                with open(fp, encoding='utf-8', errors='ignore') as f:
                    parts.append(f.read())
    out_path = os.path.join(out, out_name)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(parts))
    kb = os.path.getsize(out_path) // 1024
    print(f'  Written {out_name}: {kb} KB')

print('Building NotebookLM export...')

# 1. Transcripts (pre-aggregated)
src = os.path.join(base, 'sessions', 'transcripts', 'Aggregated Sessions.md')
dst = os.path.join(out, 'all-transcripts.md')
shutil.copy2(src, dst)
print(f'  Copied all-transcripts.md: {os.path.getsize(dst)//1024} KB')

# 2. World lore
merge(os.path.join(base, 'world'), '*.md', 'all-world-lore.md', recursive=True)

# 3. Locations
merge(os.path.join(base, 'locations'), '*.md', 'all-locations.md')

# 4. NPCs
merge(os.path.join(base, 'characters', 'npcs'), '*.md', 'all-npcs.md')

# 5. Player Characters
merge(os.path.join(base, 'characters', 'player-characters'), '*.md', 'all-player-characters.md')

# 6. Planning
merge(os.path.join(base, 'sessions', 'planning'), '*.md', 'all-planning.md', recursive=True)

# 6.5. Storyboards
merge(os.path.join(base, 'sessions', 'storyboards'), '*.md', 'all-storyboards.md', recursive=True)

# 7. Reference (glossary + timeline + knowledge-tracker)
ref_parts = []
for fn in ['glossary.md', 'timeline.md', 'knowledge-tracker.md']:
    fp = os.path.join(base, fn)
    ref_parts.append('')
    ref_parts.append('---')
    ref_parts.append(f'## FILE: {fn}')
    ref_parts.append('---')
    ref_parts.append('')
    with open(fp, encoding='utf-8', errors='ignore') as f:
        ref_parts.append(f.read())
ref_path = os.path.join(out, 'reference.md')
with open(ref_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(ref_parts))
print(f'  Written reference.md: {os.path.getsize(ref_path)//1024} KB')

# Zip
zip_path = os.path.join(base, 'vumbua-notebooklm.zip')
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for fn in os.listdir(out):
        zf.write(os.path.join(out, fn), fn)
total_kb = os.path.getsize(zip_path) // 1024
print(f'\nDone! ZIP: {zip_path} ({total_kb} KB)')
print('Files:')
for fn in sorted(os.listdir(out)):
    kb = os.path.getsize(os.path.join(out, fn)) // 1024
    print(f'  {fn}: {kb} KB')
