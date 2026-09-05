/**
 * Foundry VTT Macro: Create Castellan Twins
 * This macro creates NPC actors for Lyra and Ludo Castellan with their initial stats and portraits.
 */

async function createCastellans() {
    const castellanData = [
        {
            name: "Lyra Castellan",
            img: "meta/foundry-exports/portraits/lyra_ludo_castellan_portrait.png",
            stats: { agi: 0, ins: 0, str: -1, prs: 3, fin: 1, knw: 2 },
            hp: 6,
            stress: 5,
            evasion: 10,
            thresholds: { minor: 4, major: 8 },
            biography: "<p>Political Scion / Student / Hanger-on</p><p><i>'Val, darling, you look positively frayed. Surely House Sterling isn't working you this hard already?'</i></p>"
        },
        {
            name: "Ludo Castellan",
            img: "meta/foundry-exports/portraits/lyra_ludo_castellan_portrait.png",
            stats: { agi: -1, ins: 1, str: 0, prs: 2, fin: 0, knw: 3 },
            hp: 6,
            stress: 5,
            evasion: 9,
            thresholds: { minor: 4, major: 8 },
            biography: "<p>Political Scion / Student / Hanger-on</p><p><i>'We’ve saved you a seat at the High Table tonight. No sycophants, just... partners.'</i></p>"
        }
    ];

    for (let data of castellanData) {
        // Check if actor already exists to avoid duplicates
        let existing = game.actors.find(a => a.name === data.name);
        if (existing) {
            ui.notifications.warn(`Actor "${data.name}" already exists.`);
            continue;
        }

        // Create the Actor (Daggerheart System expected)
        await Actor.create({
            name: data.name,
            type: "npc", // Adjust to "adversary" or "npc" depending on your exact Daggerheart system implementation
            img: data.img,
            system: {
                stats: {
                    agility: { value: data.stats.agi },
                    instinct: { value: data.stats.ins },
                    strength: { value: data.stats.str },
                    presence: { value: data.stats.prs },
                    finesse: { value: data.stats.fin },
                    knowledge: { value: data.stats.knw }
                },
                health: { max: data.hp, value: data.hp },
                stress: { max: data.stress, value: data.stress },
                evasion: { value: data.evasion },
                thresholds: { 
                    minor: { value: data.thresholds.minor }, 
                    major: { value: data.thresholds.major } 
                },
                details: { biography: { value: data.biography } }
            }
        });
        
        ui.notifications.info(`Created NPC: ${data.name}`);
    }
}

createCastellans();
