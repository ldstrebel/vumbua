# Update Foundry Journals

Use this workflow to (re)build `vumbua-codex.json` and import it into Foundry VTT.
Run it after every session or whenever new NPCs / locations are added.

---

## How the pipeline works

```
sessions/index.md          ← curated session titles + prose summaries (primary)
sessions/transcripts/clean/sN-clean.md  ← raw scene prose (secondary / Part content)
characters/npcs/*.md       ← NPC pages (only if First Appearance tag present)
characters/player-characters/*.md
locations/*.md
meta/foundry-exports/portraits/[name]_portrait.png  ← source portraits
        ↓
python build_codex.py
        ↓
meta/foundry-exports/vumbua-codex.json  (~1 MB)
        ↓
Paste JSON into Foundry macro dialog → two-pass import
```

**Content priority for session pages:**
1. Subtitle → `sessions/index.md` entry title (falls back to transcript `# H1`)
2. Summary paragraph → transcript `## Quick Summary` / `## Session Summary` (falls back to index prose)
3. Additional prose → `## Part N` opening paragraphs (s4-style) or `## Play-by-Play` scenes (s3-style)

---

## Full rebuild (all sessions)

```bash
cd vumbua/meta/foundry-exports
python build_codex.py
```

Output: `vumbua-codex.json` — contains all chronicle pages, all tagged NPCs, all PCs, all locations, and portrait data URIs.

## Delta rebuild (new session only)

```bash
python build_codex.py 5          # generates only Session 5 page + NPCs first appearing in Session 5
```

Use delta mode for live-session reveals — much faster, smaller JSON.

---

## Steps

### 1. Session content is ready
- Clean transcript exists at `sessions/transcripts/clean/sN-clean.md`
- A curated entry exists in `sessions/index.md` under `### [[Session 0N|Session N: Title]]`
  - If missing, add a 2–4 sentence prose summary under that heading (no bullet points)

### 2. New NPCs have their files and tags
- Each new NPC has a file at `characters/npcs/[name].md`
- The Overview table contains: `| **First Appearance** | [[session-N\|Session N]] |`
- This tag is the only gate — without it, the NPC is silently skipped
- Minimal stub is fine; the script strips GM content automatically

### 3. New NPCs have portraits (optional but recommended)
- Portrait file: `meta/foundry-exports/portraits/[slugified_name]_portrait.png`
- Slug rule: lowercase → remove all quotes and punctuation → spaces to underscores
  - "Professor Kante" → `professor_kante_portrait.png`
  - `Seraphina "Serra" Vox` → `seraphina_serra_vox_portrait.png`
- The build script auto-compresses to JPEG 400px / ~40 KB — use any resolution source

### 4. New locations are in the right folder
- All `*.md` files in `locations/` are auto-included — no manual registration needed
- GM-content sections (`## GM Narration`, `## GM Notes`, etc.) are stripped automatically

### 5. Run the build

```bash
python build_codex.py        # full
python build_codex.py N      # delta for session N
```

The script prints `✓ / ✗` for every page. Any `✗` with "file not found" means a session transcript is missing.

### 6. Import into Foundry VTT

1. Open `meta/foundry-exports/vumbua-codex.json` — **select all → copy**
2. In Foundry, open the macro `Vumbua Codex Import`
3. Paste the JSON into the input field → **Run**
4. The macro runs in two passes:
   - Pass 1: creates / updates all journal pages with raw content
   - Pass 2: resolves all `{{page:Name}}` cross-links to `@UUID[...]` and embeds portrait data URIs
5. A summary dialog reports pages created / updated and any unresolved links

**Import is additive-only.** Existing pages are updated; nothing is deleted.

---

## Spoiler safety

The pipeline automatically strips:
- YAML front matter
- Obsidian callout blocks (`> [!...]`)
- Any section whose heading contains: `gm`, `dm`, `secret`, `hidden`, `not yet revealed`, `source references`, `planning`, `future plot`, `gm narration`, `gm description`, `gm notes`, `gm reflections`

Never put GM-only information in player-facing heading sections. Use `## GM Narration` or a `> [!warning]-` callout.

---

## Spoiler audit (run occasionally)

```bash
python build_codex.py
python - <<'EOF'
import json, re
data = json.load(open("vumbua-codex.json"))
pat = re.compile(r'\bGM\b|\bthe players\b|posing as|secretly\b|true identity|not yet reveal', re.I)
for sec, j in data["journals"].items():
    for p in j["pages"]:
        plain = re.sub(r'<[^>]+>', ' ', p["content"])
        for line in plain.splitlines():
            if pat.search(line):
                print(f"[{sec}] {p['name']}: {line.strip()[:100]}")
EOF
```

Any hit that isn't a false positive should be fixed in the source file, not in the script.

---

## Naming conventions

| Thing | Convention |
|---|---|
| Session transcript | `sessions/transcripts/clean/sN-clean.md` (e.g. `s5-clean.md`) |
| Session index entry | `### [[Session 0N\|Session N: Title]]` in `sessions/index.md` |
| NPC file | `characters/npcs/[kebab-name].md` |
| Portrait source | `meta/foundry-exports/portraits/[snake_name]_portrait.png` |
| Chronicle page name | `Session N` (plain — no subtitle — so `{{page:Session N}}` links resolve) |
