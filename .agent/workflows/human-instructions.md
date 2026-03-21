---
description: User guide — what to do and what to tell the AI
aliases:
- Human Instructions
---

# Vumbua Campaign — How to Use This Vault

Two flows cover 90% of ongoing work. Everything else is referenced below.

---

## Flow 1 — Adding a New NPC (minimal, live-session ready)

**Goal:** Get an NPC into Foundry with their portrait and name before or during the session they appear.

### What you do

1. **Tell the AI:**
   ```
   Add a stub NPC for [Name]. They appear in Session N.
   Here's a portrait: [attach image or describe what to generate]
   ```

2. **AI will:**
   - Create `characters/npcs/[name].md` with just name, role, and First Appearance tag
   - Generate or save the portrait to `meta/foundry-exports/portraits/[name]_portrait.png`
   - Run `python build_codex.py` (or delta mode for just that session)
   - Tell you when `vumbua-codex.json` is ready

3. **You do in Foundry:**
   - Open `meta/foundry-exports/vumbua-codex.json` → Select All → Copy
   - In Foundry, open the `Vumbua Codex Import` macro → Paste → Run
   - The NPC page appears in the **NPCs** journal with their portrait

4. **After the session:** run Flow 2 to fill in what the players actually learned.

---

## Flow 2 — Post-Session Recap

**Goal:** Process a session transcript → update the vault → update Foundry journals.

### What you prepare

- Raw transcript dropped at `sessions/transcripts/raw/sN-raw.md`
  (Granola export, Otter, manual notes — any format works)
- Know the session number

### What you tell the AI

```
/add-session
Process Session N. Raw transcript is at sessions/transcripts/raw/sN-raw.md.
Players: Sophie (Britt), Kristina (Aggie), John (Ignatius), Luke (Lomi), Holly (Iggy).
Date: [session date]
```

### What the AI will do

1. **Clean the transcript** → saves to `sessions/transcripts/clean/sN-clean.md`
   - Organizes into scenes, attributes dialogue, flags uncertain speakers
   - Zero detail loss — nothing is summarized or cut

2. **Update `sessions/index.md`** — adds a curated prose summary entry for Session N
   - This is what appears in Foundry's Chronicle journal

3. **Update character files** — for every new NPC that appeared:
   - Creates a profile in `characters/npcs/` if it doesn't exist
   - Adds session appearance notes to existing profiles

4. **Generate missing portraits** — for any new NPCs without a portrait file

5. **Rebuild the Foundry codex:**
   ```bash
   python build_codex.py N   # delta: only Session N + new NPCs
   ```

6. **Tells you:** "Ready — paste `vumbua-codex.json` into the Foundry macro"

### Three points where the AI will stop and ask you

The AI pauses at three checkpoints — don't skip these, they prevent spoilers and wrong names from reaching Foundry:

**Checkpoint 1 — Session Delta review** (before any files are created)
- You'll see a list of new NPCs, proposed canonical names, and a draft session title
- Confirm the names, correct any misidentified characters, approve or rename the title

**Checkpoint 2 — Chronicle prose review** (before the rebuild)
- You'll see the 2–4 sentence player-facing summary that will appear in Foundry's Chronicle journal
- Read it as a player: does it say what you want them to know? No spoilers? Right voice?
- Edit freely — this is YOUR text, not the AI's

**Checkpoint 3 — Portrait review** (before the rebuild)
- New NPC portraits are shown for approval
- Ask for regeneration if they don't match your vision or the transcript's description

After all three checkpoints are cleared, the AI runs the Foundry rebuild.

### You do in Foundry

1. Open `meta/foundry-exports/vumbua-codex.json` → Select All → Copy
2. Open the `Vumbua Codex Import` macro → Paste → Run
3. The macro updates Chronicle, NPCs, PCs, and Locations journals in two passes
4. Review: click a few cross-links to verify they navigate correctly

---

## Other workflows

### `/add-lore` — Add or update world lore

```
/add-lore
Add a location page for the Resonance Raceway. It appeared in Session 5.
[paste description or attach notes]
```

All files in `locations/` are auto-included in the next Foundry rebuild.

### `/export-to-foundry` — Manual rebuild without a new session

```
/export-to-foundry
Rebuild the full codex — no new session, just need to refresh Foundry.
```

Or for delta:
```
/export-to-foundry
Delta rebuild for Session 5 only.
```

---

## How the Foundry import works

The macro runs in **two passes** so all cross-links always resolve correctly:

- **Pass 1:** Creates or updates every journal page with placeholder tokens (`{{page:Azor}}`)
- **Pass 2:** Replaces all tokens with live `@UUID[...]` links and embeds portrait images

**It is additive-only** — existing pages are updated, nothing is ever deleted.

The JSON is currently ~1 MB (down from 13 MB after portrait compression). Paste works reliably in any modern browser.

---

## Spoiler safety

The pipeline automatically strips:
- Sections whose headings contain: `GM`, `DM`, `Secret`, `Hidden`, `Not Yet Revealed`, `GM Narration`, `GM Notes`
- All Obsidian callout blocks (`> [!warning]`, `> [!note]`, etc.)
- YAML front matter

**Rule for your vault:** Put anything the players shouldn't see under `## GM Narration` or inside a `> [!warning]-` block. Everything else in a player-facing heading will appear in Foundry.

---

## File quick reference

| What | Where |
|------|-------|
| Raw transcripts | `sessions/transcripts/raw/sN-raw.md` |
| Cleaned transcripts | `sessions/transcripts/clean/sN-clean.md` |
| Curated session summaries | `sessions/index.md` |
| NPC profiles | `characters/npcs/` |
| PC profiles | `characters/player-characters/` |
| Location pages | `locations/` |
| Portrait sources | `meta/foundry-exports/portraits/` |
| Build script | `meta/foundry-exports/build_codex.py` |
| Foundry codex JSON | `meta/foundry-exports/vumbua-codex.json` |
| Foundry import macro | `meta/foundry-exports/foundry-macro.js` |
| Lore reference (AI) | `.agent/workflows/lore-index.md` |
| Character index | `characters/index.md` |
| Knowledge tracker | `knowledge-tracker.md` |
| Timeline | `timeline.md` |

---

## Tips

### Portraits
- Any image format, any resolution — the build script resizes to 400 px and compresses to ~40 KB JPEG automatically
- Filename must be `[snake_case_name]_portrait.png` — see `add-character.md` for the slug rule
- To regenerate a portrait: delete the old file, ask the AI to generate a new one, rebuild

### Transcript quality
- More context is better — include table talk; the AI filters IC vs OOC
- Identify who the GM is in the transcript so the AI can separate narration from player speech
- Any format works (Granola export, raw text, bullet notes)

### Iterating on session summaries
- The curated entry in `sessions/index.md` is what players read in Foundry's Chronicle
- You can edit it freely — it's just markdown prose
- After editing, just run `python build_codex.py` to rebuild (no session number needed)

### Correcting the AI
- Be specific: *"Change all instances of 'Lasidian' to 'lavsidian'"*
- The AI will show you every change it makes
- For speaker corrections: *"Line 47 was Serra, not unidentified"*
