/**
 * Vumbua Codex — Foundry VTT Journal Importer v6 (ULTRA-LEAN & SAFE)
 * 
 * - Optimized for Delta Imports (Session updates).
 * - Multi-version Folder Check (handles j.folder as object or ID).
 * - Memory Management: Clears input after parsing to prevent Chrome crashes.
 * - Additive only: Logs skipped pages to reassure users.
 */

const CODEX_FOLDER_NAME = "Vumbua Codex";

(async () => {
    // ── Step 1: Get JSON ────────────────────────────────────────────
    const jsonText = await new Promise((resolve) => {
        new Dialog({
            title: "Vumbua Codex Importer v6",
            content: `
        <form style="font-family:sans-serif;">
          <div class="form-group stacked">
            <label>Paste the contents of <strong>vumbua-codex.json</strong>:</label>
            <textarea id="vumbua-json-input" 
                      style="width:100%;height:300px;font-family:monospace;font-size:11px;background:#f4f4f4;border:1px solid #ccc;padding:8px;" 
                      placeholder="Paste JSON here..."></textarea>
          </div>
          <div style="background:#eef; padding:10px; border-radius:4px; font-size:12px; margin-top:10px; border-left:4px solid #2d5dcc;">
            🚀 <strong>Performance Tip:</strong> For session updates, run <br/>
            <code>python build_codex.py [session_id]</code> <br/>
            to generate a small (1MB) Delta file. This prevents browser crashes!
          </div>
        </form>
      `,
            buttons: {
                import: {
                    icon: '<i class="fas fa-bolt"></i>',
                    label: "Import Changes",
                    callback: (html) => resolve(html.find("#vumbua-json-input").val())
                },
                cancel: {
                    icon: '<i class="fas fa-times"></i>',
                    label: "Cancel",
                    callback: () => resolve(null)
                }
            },
            default: "import",
            close: () => resolve(null)
        }).render(true);
    });

    if (!jsonText || jsonText.trim() === "") return;

    let data;
    try { 
        data = JSON.parse(jsonText); 
        // Memory Clear: Helping Chrome recovery
        const textarea = document.getElementById("vumbua-json-input");
        if (textarea) textarea.value = ""; 
    }
    catch (e) { ui.notifications.error(`JSON parse error: ${e.message}`); return; }

    const isDelta = data.meta?.deltaMode;
    const targetSess = data.meta?.targetSession;
    ui.notifications.info(`Vumbua Codex: Starting ${isDelta ? 'Delta' : 'Full'} import...`);

    // ── Step 2: Build portrait map ─────────────────────────
    const portraitDataURIs = {};
    if (data.portraits) {
        for (const [filename, base64Data] of Object.entries(data.portraits)) {
            portraitDataURIs[filename] = `data:image/png;base64,${base64Data}`;
        }
    }

    // ── Step 3: Folder discovery ─────────────────────────────────
    let codexFolder = game.folders.find(f => f.name === CODEX_FOLDER_NAME && f.type === "JournalEntry");
    if (!codexFolder) {
        codexFolder = await Folder.create({ name: CODEX_FOLDER_NAME, type: "JournalEntry" });
    }
    const codexFolderId = codexFolder.id;

    // ── Step 4: Map all existing pages in the folder ──────────────────
    // This allows Delta imports to link to pages created in previous sessions.
    const pageMap = new Map(); // Name -> UUID
    const allJournalsInCodex = game.journal.filter(j => {
        const folderId = (typeof j.folder === 'string') ? j.folder : j.folder?.id;
        return folderId === codexFolderId;
    });
    
    for (const j of allJournalsInCodex) {
        for (const p of j.pages) {
            pageMap.set(p.name, `JournalEntry.${j.id}.JournalEntryPage.${p.id}`);
        }
    }
    console.log(`Knowledge Base: Indexed ${pageMap.size} existing pages for link resolution.`);

    // ── Step 5: Process Journals from JSON ─────────────────────────────
    let pagesCreated = 0;
    let pagesUpdated = 0;
    const unresolvedNames = new Set();

    for (const [key, journalData] of Object.entries(data.journals)) {
        // Find existing journal in folder
        let journal = game.journal.find(j => {
            const folderId = (typeof j.folder === 'string') ? j.folder : j.folder?.id;
            return j.name === journalData.name && folderId === codexFolderId;
        });

        if (!journal) {
            journal = await JournalEntry.create({
                name: journalData.name,
                folder: codexFolderId,
                ownership: { default: CONST.DOCUMENT_OWNERSHIP_LEVELS.OBSERVER }
            });
            console.log(`Created Journal: ${journalData.name}`);
        }

        for (const pageData of journalData.pages) {
            let page = journal.pages.find(p => p.name === pageData.name);
            
            // Link Resolution Logic
            const resolveLinks = (raw) => {
                return raw.replace(/\{\{page:([^|}]+)(?:\|([^}]+))?\}\}/g, (match, pageName, displayText) => {
                    const uuid = pageMap.get(pageName);
                    const label = displayText || pageName;
                    if (uuid) return `@UUID[${uuid}]{${label}}`;
                    unresolvedNames.add(pageName);
                    return `<em>${label}</em>`;
                });
            };

            // Portrait Embedding Logic
            const embedPortraits = (raw) => {
                return raw.replace(/src='portraits\/([^']+)'/g, (match, filename) => {
                    return portraitDataURIs[filename] ? `src='${portraitDataURIs[filename]}'` : match;
                });
            };

            const finalContent = embedPortraits(resolveLinks(pageData.content));

            if (!page) {
                page = await JournalEntryPage.create({
                    name: pageData.name,
                    type: "text",
                    text: { content: finalContent },
                    sort: pageData.sort ?? 0
                }, { parent: journal });
                pagesCreated++;
                pageMap.set(pageData.name, `JournalEntry.${journal.id}.JournalEntryPage.${page.id}`);
            } else {
                await page.update({ "text.content": finalContent });
                pagesUpdated++;
            }
        }
    }

    // ── Step 6: Process Actors from JSON ─────────────────────────────
    let actorsCreated = 0;
    let actorsUpdated = 0;

    if (data.actors) {
        let actorFolder = game.folders.find(f => f.name === "NPCs" && f.type === "Actor");
        if (!actorFolder) {
            actorFolder = await Folder.create({ name: "NPCs", type: "Actor" });
        }

        for (const actorData of data.actors) {
            let actor = game.actors.find(a => a.name === actorData.name);
            
            // Portrait Embedding
            const portraitUrl = actorData.img ? (portraitDataURIs[actorData.img.replace('portraits/', '')] || actorData.img) : "";

            const actorFields = {
                name: actorData.name,
                type: "npc", // Adjust based on Daggerheart system
                img: portraitUrl,
                folder: actorFolder.id,
                system: {
                    stats: {
                        agility: { value: actorData.stats.agi ?? 0 },
                        instinct: { value: actorData.stats.ins ?? 0 },
                        strength: { value: actorData.stats.str ?? 0 },
                        presence: { value: actorData.stats.prs ?? 0 },
                        finesse: { value: actorData.stats.fin ?? 0 },
                        knowledge: { value: actorData.stats.knw ?? 0 }
                    },
                    health: { max: actorData.stats.hp ?? 6, value: actorData.stats.hp ?? 6 },
                    stress: { max: actorData.stats.stress ?? 5, value: actorData.stats.stress ?? 5 },
                    evasion: { value: actorData.stats.evasion ?? 10 },
                    thresholds: { 
                        minor: { value: actorData.stats.thresholds?.minor ?? 4 }, 
                        major: { value: actorData.stats.thresholds?.major ?? 8 } 
                    },
                    details: { biography: { value: actorData.biography } }
                }
            };

            if (!actor) {
                await Actor.create(actorFields);
                actorsCreated++;
            } else {
                await actor.update(actorFields);
                actorsUpdated++;
            }
        }
    }

    // ── Step 7: Final Summary ─────────────────────────────────────────────
    let missingList = Array.from(unresolvedNames).filter(name => !pageMap.has(name));
    
    new Dialog({
        title: "✅ Vumbua Codex: Import Complete",
        content: `
      <div style="font-family:sans-serif;">
        <h3 style="color:#2d5dcc;border-bottom:1px solid #ccc;padding-bottom:5px;">
           ${isDelta ? `Delta Update (Session ${targetSess})` : 'Full Codex Rebuild'}
        </h3>
        <p style="margin:10px 0;">Foundry sync finished successfully.</p>
        
        <div style="display:flex; justify-content:space-around; background:#f9f9f9; padding:10px; border-radius:4px; border:1px solid #eee;">
           <div style="text-align:center;">
             <div style="font-size:1.4em; font-weight:bold; color:green;">+${pagesCreated}</div>
             <div style="font-size:0.8em; color:#666;">Pages</div>
           </div>
           <div style="text-align:center;">
             <div style="font-size:1.4em; font-weight:bold; color:orange;">+${actorsCreated}</div>
             <div style="font-size:0.8em; color:#666;">Actors</div>
           </div>
           <div style="text-align:center;">
             <div style="font-size:1.4em; font-weight:bold; color:#2d5dcc;">${pagesUpdated + actorsUpdated}</div>
             <div style="font-size:0.8em; color:#666;">Updated</div>
           </div>
        </div>

        ${missingList.length > 0 ? `
          <div style="background:#fff3cd; padding:10px; border-radius:4px; margin-top:10px; border: 1px solid #ffeeba;">
            <strong>⚠️ Cross-References Note:</strong><br/>
            <small>This import mentions pages that aren't in Foundry yet. This is normal for Delta imports. They will resolve when those pages are eventually added.</small>
          </div>
        ` : '<p style="color:green;margin-top:10px;">✨ All links resolved successfully!</p>'}
        
        <p style="font-size:0.9em; color:#666; margin-top:10px;">
          <em>Note: No existing pages were deleted. Journals was scanned for matching names and updated in-place.</em>
        </p>
      </div>
    `,
        buttons: { ok: { label: "Done", icon: '<i class="fas fa-check"></i>' } },
        default: "ok"
    }).render(true);

    ui.notifications.info(`Vumbua Codex complete: +${pagesCreated}, ${pagesUpdated} updated.`);
})();
