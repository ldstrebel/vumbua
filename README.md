# Vumbua Campaign Repository

A **Daggerheart campaign** set in a Magitek-Steampunk world inspired by *Atlantis: The Lost Empire*.

**[📖 View the Campaign Wiki](https://ldstrebel.github.io/vumbua/)** *(once deployed to GitHub Pages)*

---

## What Is This?

This repository contains all the lore, session recaps, and character information for the **Vumbua campaign**—an ongoing tabletop RPG adventure that meets every 2 weeks.

### The Setting

**The Great Stitching** is a process where isolated civilizations and their reality-Nodes are physically integrated into a growing empire called **Harmony**. Vumbua Academy is a mobile city-state that has just relocated to a new frontier after 80 years of stagnation.

Our party of five unlikely students must navigate:
- Political intrigue between Harmony's houses
- Cultural tensions with newly integrated clans
- The mystery of why integration sometimes fails
- Personal quests for identity, power, and truth

---

## Repository Structure

```
docs/                    # GitHub Pages content (THE PUBLIC WIKI)
├── index.md            # Campaign homepage
├── lore/               # World-building
│   ├── world/          # Stitching mechanics, integration physics
│   ├── locations/      # Vumbua Academy, Harmony Prime, frontier
│   ├── factions/       # All 8 Harmony houses + 5 clans
│   └── bestiary/       # Creatures and phenomena
├── characters/         # PC and NPC profiles
├── sessions/           # Scene-by-scene recaps
└── mechanics/          # Daggerheart system info

Vumbua/                 # Original source documents
├── Lore/              # Raw lore notes (being migrated)
└── Sessions/          # Original session scripts
```

---

## Dual-Track Documentation

**Important:** Lore pages include both **player-facing information** and **GM secrets**.

- **"What Players Know"** sections are safe to share
- **"GM Secrets"** sections are clearly marked with red caution boxes
- The Knowledge Tracker keeps track of what's been revealed

This allows us to maintain a single source of truth while preserving mysteries.

---

## For Players

### Catching Up on Sessions
Start here: [📚 Session Index](docs/sessions/index.md)

### Learning About the World
Browse: [🌍 Lore Hub](docs/lore/index.md)

### Quick Reference
- [Glossary](docs/lore/glossary.md) - Terms and definitions
- [Timeline](docs/lore/timeline.md) - When things happened
- [Characters](docs/characters/index.md) - Who's who

---

## For the GM (Me)

### After Each Session Workflow

1. **Copy the template**
   ```bash
   cp docs/sessions/_template.md docs/sessions/session-XX.md
   ```

2. **Fill in the session recap** (scene-by-scene)

3. **Update affected lore pages**
   - Add newly revealed information to "What Players Know"
   - Update GM Secrets if needed

4. **Update trackers**
   - [Knowledge Tracker](docs/lore/knowledge-tracker.md) - Mark new discoveries
   - [Timeline](docs/lore/timeline.md) - Add session date and events
   - [Character profiles](docs/characters/) - Update relationships and growth

5. **Update Session Index**
   - Add new session to [docs/sessions/index.md](docs/sessions/index.md)

### GM Notes Location
Private prep notes go in `docs/gm-notes/` (excluded from GitHub Pages)

---

## GitHub Pages Deployment

To deploy changes:

```bash
git add docs/
git commit -m "Session XX recap and lore updates"
git push origin main
```

GitHub Pages will automatically rebuild from the `docs/` folder.

### Local Preview

To preview the site locally:
```bash
# Install Jekyll (once)
gem install bundler jekyll

# Serve locally
cd docs
jekyll serve

# View at http://localhost:4000
```

---

## Content Guidelines

### Session Recaps
- **Keep story-relevant dialogue** in screenplay format
- **Cut non-story table talk** (unless it's really funny)
- **Scene-by-scene structure** for easy reference
- **Include Player Discoveries** bullets
- **Add GM Notes** for behind-the-scenes info

### Lore Pages
- **Always include both sections**: "What Players Know" and "GM Secrets"
- **Use clear section headers** and markdown formatting
- **Link between related pages** for easy navigation
- **Update Knowledge Tracker** when players learn something

### Character Profiles
- **Update after each session** with new developments
- **Track relationships** between characters
- **Note personal goals** and how they evolve

---

## Campaign Status

**System:** Daggerheart (v1.5/1.6)  
**Current Session:** 1  
**Schedule:** Every 2 weeks  
**Party Size:** 5 players

### The Party
- **Britt** (Sophie) - Mizizi, Gold Rank
- **Aggie** (Kristina) - Mizizi, Silver Rank
- **Ignatius** (John) - Ash-Blood, Silver Rank
- **Lomi** (Luke F) - Harmony-born, Copper Rank
- **Iggy** (Holly) - "Earthkin," Gold Rank

---

## Contributing

This is a personal campaign repository, but if you're a player and spot an error or want to suggest an update:

1. **Create an issue** describing what needs fixing
2. **Or submit a PR** with the correction

Please maintain the dual-track documentation format when editing lore pages!

---

## License

Campaign content © 2026 ldstrebel

*This is a personal campaign wiki. Content may reference Daggerheart rules (Darrington Press) but all lore, characters, and story are original.*
