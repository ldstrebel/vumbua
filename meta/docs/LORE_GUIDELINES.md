# Lore Documentation Guidelines

## 1. Linking Convention (CRITICAL)

**Rule:** Always use the **filename (kebab-case)** as the link target, with the display text piped.

*   **CORRECT:** `[[vumbua-academy|Vumbua Academy]]`
*   **INCORRECT:** `[[Vumbua Academy]]`
*   **INCORRECT:** `[[Vumbua_Academy]]`

**Why?**
Wiki-links (`[[Link]]`) look for a file named `Link.md`. If it doesn't exist, some tools create it at the root. Our files are organized in subfolders with kebab-case names (e.g., `lore/locations/vumbua-academy.md`). Using the filename ensures the link resolves correctly to the existing file.

## 2. File Organization

*   **Locations:** `lore/locations/`
*   **Factions:** `lore/factions/` (or `lore/factions/clans/` for specific clans)
*   **NPCs:** `lore/characters/npcs/`
*   **World Key Terms:** `lore/world/`

## 3. Creating New Lore

1.  **Check Indices:** Before creating a new file, check `index.md` or the relevant subfolder to see if it exists.
2.  **Naming:** Use `kebab-case` for filenames (lowercase, hyphens instead of spaces).
3.  **Frontmatter:** Always include `aliases` and `tags`.

```markdown
---
aliases:
- Display Name
- Alternate Name
tags:
- type
- subtype
---
```
