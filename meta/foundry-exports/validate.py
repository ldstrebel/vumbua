import json, re

with open(r'd:\Code\vumbua\meta\foundry-exports\vumbua-codex.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Check NPC content for rank-like terms
for p in data['journals']['npcs']['pages']:
    content = p['content']
    # Search for rank terms
    matches = re.findall(r'(?i)(gold|silver|copper|bronze|rank|iron)[^<]{0,30}', content)
    if matches:
        print(f"\n{p['name']}:")
        for m in matches:
            print(f"  Found: ...{m}...")
    
    # Also print the table/header portion
    table_match = re.search(r'<table>.*?</table>', content, re.DOTALL)
    if table_match:
        print(f"\n{p['name']} TABLE:")
        print(f"  {table_match.group()[:300]}")
