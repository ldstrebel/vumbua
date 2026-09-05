// ══════════════════════════════════════════════════════════════════════════════
// Daggerheart System Diagnostic Macro
// PASTE THIS INTO FOUNDRY VTT CONSOLE (F12 → Console tab)
// Run BEFORE re-running the main session macro.
// ══════════════════════════════════════════════════════════════════════════════
(async () => {
    // ── 1. Print the full system data of the first existing actor ────────────
    const actor = game.actors.contents[0];
    if (!actor) {
        console.error("No actors found in world. Run the s10 macro first to create them.");
        return;
    }

    console.group(`📋 Actor: "${actor.name}"  (type: "${actor.type}")`);
    console.log("actor.system →", JSON.parse(JSON.stringify(actor.system)));
    console.groupEnd();

    // ── 2. Print the exact HP / stress paths ─────────────────────────────────
    const sys = actor.system;
    const candidates = [
        "hp", "health", "stress", "hitPoints",
        "attributes.hp", "attributes.health", "attributes.stress",
        "resources.hp", "resources.stress"
    ];

    console.group("🔍 Resource field probe");
    for (const path of candidates) {
        const parts = path.split(".");
        let val = sys;
        for (const p of parts) val = val?.[p];
        if (val !== undefined) {
            console.log(`✅  system.${path} =`, JSON.parse(JSON.stringify(val)));
        } else {
            console.log(`❌  system.${path} → undefined`);
        }
    }
    console.groupEnd();

    // ── 3. Print all Item types registered in this system ────────────────────
    console.group("🗡️ Valid Item types in this system");
    const validTypes = game.system.documentTypes?.Item ?? [];
    console.log("Item types:", validTypes);
    console.groupEnd();

    // ── 4. Print the prototypeToken bar attributes of the actor ──────────────
    console.group("🎯 Token bar configuration");
    console.log("bar1:", actor.prototypeToken?.bar1);
    console.log("bar2:", actor.prototypeToken?.bar2);
    console.log("displayBars:", actor.prototypeToken?.displayBars);
    console.groupEnd();

    // ── 5. Print items on the actor (attacks, features) ──────────────────────
    console.group("⚔️ Embedded Items on actor");
    for (const item of actor.items) {
        console.log(`  [${item.type}] "${item.name}"`, JSON.parse(JSON.stringify(item.system)));
    }
    if (actor.items.size === 0) console.warn("No items found on this actor.");
    console.groupEnd();

    ui.notifications.info(`Diagnostic complete for "${actor.name}" — check the F12 Console.`);
})();
