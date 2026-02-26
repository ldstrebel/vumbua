# Export to Foundry

Use this workflow to prep the Vumbua wiki for Foundry VTT ingestion via the Lava Flow module.

## Prerequisites
- A recent session was completed or bulk wiki edits were made.

## Steps

1. **Clear the Old Vault**
   - Delete the `meta/foundry-export-vault` directory to start fresh.
   ```bash
   Remove-Item -Recurse -Force meta/foundry-export-vault -ErrorAction SilentlyContinue
   ```

2. **Run the AI Generator Script**
   // turbo
   - This script creates a fresh `meta/foundry-export-vault` folder. It dynamically generates the spoiler-free `Party Overview.md` and synthesizes the `Known NPCs.md` file using `sessions/index.md` as the source of truth. Finally, it securely copies the `characters/player-characters/` directory over, stripping out all `## GM Notes`.
   ```bash
   python meta/scripts/generate_player_vault.py
   ```

3. **Verify Security**
   - Ensure the scrubbing worked perfectly by searching across the vault.
   ```bash
   grep -ri "GM Notes" meta/foundry-export-vault/ || true
   ```
   // turbo
   
4. **Commit changes**
   ```bash
   git add meta/foundry-export-vault/ meta/scripts/
   git commit -m "docs: Generate Foundry Export Vault"
   ```

5. **Notify the User**
   - Tell the user the player vault has been dynamically generated and is ready for Lava Flow import.
