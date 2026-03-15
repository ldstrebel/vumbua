/**
 * Vumbua Codex — Foundry VTT Journal Importer v4
 * 
 * - Portraits embedded as base64 data URIs (no file upload needed)
 * - 3-pass: create pages → resolve links + portraits in memory → write final HTML
 */

const CODEX_FOLDER_NAME = "Vumbua Codex";

(async () => {
    // ── Step 1: Get JSON ────────────────────────────────────────────
    const jsonText = await new Promise((resolve) => {
        new Dialog({
            title: "Vumbua Codex Importer v4",
            content: `
        <form>
          <div class="form-group stacked">
            <label>Paste the contents of <strong>vumbua-codex.json</strong>:</label>
            <textarea id="vumbua-json-input" 
                      style="width:100%;height:300px;font-family:monospace;font-size:11px;" 
                      placeholder="Paste JSON here..."></textarea>
          </div>
          <p style="font-size:11px;color:#888;">
            🖼️ Portraits are embedded — no file uploads needed.<br/>
            ⚠️ This will DELETE existing Vumbua Codex journals and recreate them fresh.
          </p>
        </form>
      `,
            buttons: {
                import: {
                    icon: '<i class="fas fa-file-import"></i>',
                    label: "Import Fresh",
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

    if (!jsonText) { ui.notifications.warn("Import cancelled."); return; }

    let data;
    try { data = JSON.parse(jsonText); }
    catch (e) { ui.notifications.error(`JSON parse error: ${e.message}`); return; }

    ui.notifications.info("Vumbua Codex: Starting import...");

    // ── Step 2: Build portrait data URI map ─────────────────────────
    const portraitDataURIs = {};
    if (data.portraits) {
        for (const [filename, base64Data] of Object.entries(data.portraits)) {
            portraitDataURIs[filename] = `data:image/png;base64,${base64Data}`;
        }
        console.log(`Prepared ${Object.keys(portraitDataURIs).length} portrait data URIs.`);
    }

    // ── Step 3: Clean up existing Codex ─────────────────────────────
    let codexFolder = game.folders.find(
        f => f.name === CODEX_FOLDER_NAME && f.type === "JournalEntry"
    );
    if (codexFolder) {
        const existing = game.journal.filter(j => j.folder?.id === codexFolder.id);
        for (const j of existing) await j.delete();
        console.log(`Deleted ${existing.length} existing journals.`);
    } else {
        codexFolder = await Folder.create({
            name: CODEX_FOLDER_NAME,
            type: "JournalEntry",
            parent: null
        });
    }

    // ── Step 4: Pass 1 — Create empty placeholder pages ─────────────
    const pageMap = new Map();
    const pageUpdateQueue = [];

    for (const [key, journalData] of Object.entries(data.journals)) {
        const journal = await JournalEntry.create({
            name: journalData.name,
            folder: codexFolder.id,
            ownership: { default: CONST.DOCUMENT_OWNERSHIP_LEVELS.OBSERVER }
        });

        for (const pageData of journalData.pages) {
            const page = await JournalEntryPage.create({
                name: pageData.name,
                type: "text",
                text: { content: "<p>Loading...</p>" },
                sort: pageData.sort ?? 0
            }, { parent: journal });

            const pageUUID = `JournalEntry.${journal.id}.JournalEntryPage.${page.id}`;
            pageMap.set(pageData.name, pageUUID);
            pageUpdateQueue.push({
                journalId: journal.id,
                pageId: page.id,
                originalContent: pageData.content
            });
        }
    }

    console.log(`Pass 1: ${pageMap.size} pages created.`);

    // ── Step 5: Pass 2 — Resolve links + embed portraits in memory ──
    const linkPattern = /\{\{page:([^|}]+)(?:\|([^}]+))?\}\}/g;
    let linksResolved = 0;
    let linksUnresolved = 0;
    let imagesResolved = 0;

    for (const item of pageUpdateQueue) {
        let content = item.originalContent;

        // Resolve {{page:Name}} links → @UUID references
        content = content.replace(linkPattern, (match, pageName, displayText) => {
            const uuid = pageMap.get(pageName);
            const label = displayText || pageName;
            if (uuid) {
                linksResolved++;
                return `@UUID[${uuid}]{${label}}`;
            } else {
                linksUnresolved++;
                console.warn(`  Unresolved link: ${match}`);
                return `<em>${label}</em>`;
            }
        });

        // Replace portrait src paths with base64 data URIs
        content = content.replace(/src='portraits\/([^']+)'/g, (match, filename) => {
            const dataURI = portraitDataURIs[filename];
            if (dataURI) {
                imagesResolved++;
                return `src='${dataURI}'`;
            }
            console.warn(`  No portrait data for: ${filename}`);
            return match;
        });

        item.resolvedContent = content;
    }

    console.log(`Pass 2: ${linksResolved} links, ${imagesResolved} images resolved.`);

    // ── Step 6: Pass 3 — Write final content ────────────────────────
    for (const item of pageUpdateQueue) {
        const journal = game.journal.get(item.journalId);
        const page = journal.pages.get(item.pageId);
        await page.update({ "text.content": item.resolvedContent });
    }

    console.log(`Pass 3: ${pageUpdateQueue.length} pages finalized.`);

    // ── Step 7: Summary ─────────────────────────────────────────────
    const totalPages = pageMap.size;
    const journalNames = Object.values(data.journals).map(j => j.name);

    new Dialog({
        title: "✅ Vumbua Codex Import Complete",
        content: `
      <h3>Import Successful!</h3>
      <table style="width:100%; border-collapse:collapse; margin:8px 0;">
        <tr><td style="padding:4px;">📖 Journals</td><td><strong>${journalNames.length}</strong></td></tr>
        <tr><td style="padding:4px;">📄 Pages</td><td><strong>${totalPages}</strong></td></tr>
        <tr><td style="padding:4px;">🔗 Links resolved</td><td><strong>${linksResolved}</strong></td></tr>
        <tr><td style="padding:4px;">🖼️ Portraits embedded</td><td><strong>${imagesResolved}</strong></td></tr>
        ${linksUnresolved > 0 ? `<tr><td style="padding:4px;">⚠️ Unresolved</td><td><strong>${linksUnresolved}</strong></td></tr>` : ''}
      </table>
      <p><strong>Journals:</strong> ${journalNames.join(", ")}</p>
    `,
        buttons: { ok: { label: "Done", icon: '<i class="fas fa-check"></i>' } },
        default: "ok"
    }).render(true);

    ui.notifications.info(`Vumbua Codex: ${totalPages} pages, ${linksResolved} links, ${imagesResolved} portraits.`);
})();
