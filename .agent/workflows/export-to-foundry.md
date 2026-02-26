# Export to Foundry

Use this workflow to prep the Vumbua wiki for Foundry VTT ingestion via the Lava Flow module.

## Prerequisites
- A recent session was completed or bulk wiki edits were made.

## Steps

1. **Run the Vault Prep script**
   - The script creates a sanitized clone of the wiki at `meta/foundry-export-vault`
   ```bash
   python meta/scripts/foundry_vault_prep.py
   ```
   // turbo
   
2. **The Verification Audit**
   - Run a strict grep search across the export directory to guarantee no secrets bled through the truncator.
   - If this command outputs *anything*, the workflow has failed. Stop and fix the python script logic before proceeding.
   ```bash
   grep -ri "GM Notes" meta/foundry-export-vault/ || true
   ```
   // turbo
   
3. **Commit changes**
   ```bash
   git add meta/foundry-export-vault/ .agent/workflows/
   git commit -m "docs: Update Foundry Export Vault"
   ```

4. **Notify the User**
   - Tell the user the vault has been successfully built and audited.
   - Instruct the user to open Foundry, run the **Lava Flow** macro/tool, and point it to the generic `meta/foundry-export-vault` folder.
   - Remind the user to ensure "Import non-markdown files" is checked in Lava Flow if any character portraits or maps were updated!
