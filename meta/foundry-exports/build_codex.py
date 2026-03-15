import json, base64, os, re

PORTRAITS_DIR = r'd:\Code\vumbua\meta\foundry-exports\portraits'
OUTPUT = r'd:\Code\vumbua\meta\foundry-exports\vumbua-codex.json'

# Helper to load portrait as base64
def load_portrait(filename):
    path = os.path.join(PORTRAITS_DIR, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return base64.b64encode(f.read()).decode('ascii')
    return None

# Build data structure
data = {
    "meta": {
        "sessions": ["00", "01", "02", "02.5", "03", "04"],
        "generated": "2026-03-09",
        "spoilerAudit": "Player-known facts only. No GM Notes, no hidden backstory, no planned content. Iggy race=Earthkin. Zephyr race=Unknown. Rill=Mizizi exchange student. NPC ranks removed — private info."
    },
    "journals": {
        "chronicle": {
            "name": "Campaign Chronicle",
            "pages": [
                {
                    "name": "The Intake",
                    "sort": 0,
                    "content": "<h2>Arc 1: The Intake</h2><p><em>Sessions 0–3 cover the party's arrival at Vumbua Academy, their first night, and the events leading up to their first day of class.</em></p>"
                },
                {
                    "name": "Session 0: The Trials",
                    "sort": 100,
                    "content": "<h2>Session 0: The Trials</h2><h3>The Opening</h3><p>Five students arrive at {{page:Vumbua Academy}} for the intake trials. They don't yet know each other — they're strangers from different corners of Harmony, united only by admissions letters and ambition.</p><h3>The Trial of Beasts</h3><p>The first trial pairs students in the {{page:Mizizi Petrified Forest}}, a haunted dead-land outside the Academy walls. {{page:Britt}} and {{page:Aggie}} — both Mizizi — are paired together and must survive hostile fauna. Meanwhile {{page:Ignatius}} and {{page:Lomi}} are paired, and {{page:Iggy}} works solo.</p><h3>The Pairing</h3><p>During the trial, {{page:Britt}} encounters a creature and freezes — but {{page:Aggie}} intervenes. Their bond begins here, forged in shared survival. {{page:Ignatius}} and {{page:Lomi}} clash on approach ({{page:Ignatius}} wants to charge; {{page:Lomi}} wants to plan) but discover complementary strengths.</p><h3>Dean Isolde's Welcome</h3><p>After the trials, {{page:Dean Isolde Vane}} addresses the incoming class. She is formal, commanding, and sets the tone: Vumbua is not a school — it is a proving ground. Students are sorted into ranks based on their trial performance.</p><h3>Key Moments</h3><ul><li>{{page:Britt}} and {{page:Aggie}} form a protective bond during the beast trial</li><li>{{page:Ignatius}} and {{page:Lomi}} clash but find mutual respect</li><li>{{page:Iggy}} completes his trial solo — quiet but effective</li><li>The Academy's competitive hierarchy is immediately established</li></ul>"
                },
                {
                    "name": "Session 1: The First Night",
                    "sort": 200,
                    "content": "<h2>Session 1: The First Night</h2><h3>Settling In</h3><p>The party finds their assigned rooms in {{page:Block 04}}, the student housing district. {{page:Britt}} and {{page:Aggie}} are roommates. {{page:Lomi}} meets his neighbours. {{page:Ignatius}} discovers the communal spaces. {{page:Iggy}} quietly observes from a crane perch above the block.</p><h3>The Bonfire Invitation</h3><p>{{page:Serra Vox}} approaches the group and invites them to an unofficial welcome event in {{page:Block 99}} — the older, more run-down district where upperclassmen throw parties. She's confident and direct, establishing herself as the social hub of the incoming class.</p><h3>At the Bonfire</h3><p>The {{page:Block 99}} bonfire is a mix of students from all backgrounds. Key encounters:</p><ul><li>{{page:Lucky}} runs a betting game and catches {{page:Lomi}}'s attention</li><li>{{page:Valentine Sterling}} holds court, discussing Academy politics and family legacy</li><li>{{page:Sarge}} — a gruff older student — provides blunt perspective on Academy life</li><li>{{page:Rill}} introduces herself as a Mizizi exchange student and bonds with {{page:Britt}} and {{page:Aggie}}</li></ul><h3>The Spark</h3><p>Late in the evening, a strange atmospheric pulse ripples through the Academy. Most students barely notice, but {{page:Ignatius}} feels it viscerally — a surge of heat connected to his Ash-Blood heritage. The night settles into uneasy quiet.</p>"
                },
                {
                    "name": "Session 2: The Bonfire & The Spark",
                    "sort": 300,
                    "content": "<h2>Session 2: The Bonfire & The Spark</h2><h3>The Bonfire Continues</h3><p>The social dynamic at {{page:Block 99}} deepens. New faces appear:</p><ul><li>{{page:Percy Vane-Smythe III}} holds forth on the <strong>Sixfold Theory</strong> — a fringe academic position arguing that more elemental clans exist beyond the known five. Most students dismiss it, but the debate draws a crowd.</li><li>{{page:Zephyr}} appears at the fire's edge — an androgynous figure of unknown origin who says little but watches everything.</li><li>{{page:Bramble}} — a quiet, plant-like student — gravitates toward {{page:Aggie}} and shares an affinity for growing things.</li></ul><h3>The Ash-Blood Discussion</h3><p>A group conversation turns to the Ash-Blood population at the Academy — a couple hundred among 70,000 students. {{page:Ignatius}} engages passionately, advocating for his people's culture. {{page:Rill}} contributes a Mizizi perspective on death and interconnection.</p><h3>The Atmospheric Surge</h3><p>The strange energy pulse returns — stronger this time. {{page:Zephyr}} reacts visibly, purple lightning crackling briefly around them before they suppress it. {{page:Ignatius}} feels the heat surge intensely. The moment passes, but it leaves questions.</p><h3>Key Moments</h3><ul><li>{{page:Percy Vane-Smythe III}} introduces the Sixfold Theory to the party</li><li>{{page:Zephyr}}'s purple lightning is witnessed by several students</li><li>{{page:Bramble}} and {{page:Aggie}} bond over shared interests</li><li>The party begins to feel like a group, not just strangers</li></ul>"
                },
                {
                    "name": "Session 2.5: The Power Room",
                    "sort": 350,
                    "content": "<h2>Session 2.5: The Power Room</h2><p><em>A solo session for {{page:Iggy}} — concurrent with the Session 2 bonfire.</em></p><h3>The Irish Goodbye</h3><p>While the bonfire continues in {{page:Block 99}}, {{page:Iggy}} slips away unnoticed. The door to the Academy's power plant catches his eye — it's been left unlocked, and he can see cogs and machinery whirring inside.</p><h3>The Walker-Core</h3><p>{{page:Iggy}} walks into the power plant and meets {{page:Tommy}} — a gnome clerk staffing the front desk — and {{page:Lucina}}, a dwarf mechanic. Neither stops him from wandering deeper.</p><p>Inside, {{page:Iggy}} finds a large warehouse floor filled with glowing crystals plugged into panels, connected to turbines and rotating machinery. He begins sketching everything in detail.</p><h3>Professor Kante</h3><p>{{page:Professor Kante}} — a tortoise professor of harmonics — finds {{page:Iggy}} in his office comparing his sketches to diagrams on a chalkboard. Rather than being angry, Kante is delighted. He recognises {{page:Iggy}}'s technical intuition and invites him to sit and talk.</p><p>Kante explains the resonator battery system — the Panda 5 — and the concept of the Global Amplitude. He gives {{page:Iggy}} an umber crystal as a gift and invites him to return for tea and further collaboration.</p><h3>Key Moments</h3><ul><li>{{page:Iggy}} discovers the power plant infrastructure and the Panda 5 resonator batteries</li><li>{{page:Professor Kante}} becomes {{page:Iggy}}'s first mentor figure at the Academy</li><li>{{page:Iggy}} receives an umber crystal — a core component of the power system</li><li>{{page:Iggy}} rejoins the party later for drinks at the {{page:Celestial Lounge}}</li></ul>"
                },
                {
                    "name": "Session 3: The Celestial Lounge & The Ambush",
                    "sort": 400,
                    "content": "<h2>Session 3: The Celestial Lounge & The Ambush</h2><h3>The Celestial Lounge</h3><p>The party arrives at the {{page:Celestial Lounge}} in the Upper Core. {{page:Iggy}} is captivated by the sweeping view of Vumbua and begins mapping the city layout, gaining a new cartography experience.</p><p>{{page:Lomi}} spots {{page:Valentine Sterling}} and {{page:Ember}} playing a card game called <em>Crown and Ruin</em>. He joins and wins a round against Val.</p><h3>The Study Guide</h3><p>After the game, {{page:Valentine Sterling}} — loosened by drink — admits he wrote a deliberately hard practice test and sold it to {{page:Lucky}} as a \"study guide.\" His logic: anyone who can pass his test has solid fundamentals. He passes out shortly after.</p><h3>The Alley Ambush</h3><p>As the party leaves the Lounge, {{page:Britt}} notices three figures communicating in sign language: {{page:Azor}} and two large bruisers, Zyykl and Tus.</p><p>{{page:Britt}} approaches them for directions. {{page:Azor}} leads her into an alley and springs an ambush — a net, a heavy blow, and an attempt to steal her belongings. Zyykl and Tus flee with her test receipt, but when {{page:Azor}} grabs her family heirloom — a petrified acorn necklace — {{page:Britt}} fights back ferociously and pins him.</p><h3>The Interrogation</h3><p>{{page:Iggy}}, {{page:Aggie}}, {{page:Lomi}}, and {{page:Ignatius}} arrive. {{page:Azor}} reveals he failed his own candidacy and recruited the bruisers from Septal to steal test receipts. He's defiant: <em>\"You may paint me as the villain, but I'm not the one squandering my chance drinking at 2 AM.\"</em></p><p>{{page:Britt}} takes his pocket watch as compensation. {{page:Lomi}}, disgusted by {{page:Azor}}'s attitude, punches the subdued man hard enough to break a rib.</p><h3>Key Moments</h3><ul><li>{{page:Valentine Sterling}} reveals he created the study guide scam</li><li>{{page:Britt}} survives an ambush and proves her toughness</li><li>{{page:Lomi}} shows a darker edge — breaking a downed man's rib</li><li>{{page:Iggy}} gains a cartography experience from mapping Vumbua's layout</li><li>The party plans to find {{page:Lucky}} tomorrow and barter for the study guide</li></ul>"
                },
                {
                    "name": "Session 4: The First Day of Classes",
                    "sort": 500,
                    "content": "<h2>Session 4: The First Day of Classes</h2><h3>Morning Routines</h3><p>The party prepares for their first grueling day of classes at Vumbua Academy. {{page:Lomi}} emphasizes the importance of focus, sensing the intense pressure of the week ahead, while {{page:Iggy}} discovers a vast array of new foods.</p><h3>Aetheric Ballistics & Logistics</h3><p>The first class is a brutal introduction to the Academy's pace. The professor hurls chalk at {{page:Ignatius}} with calculated precision due to his low Evasion, dealing emotional damage. {{page:Lomi}} attempts to copy notes from a {{page:Snobbish Student}} sitting nearby, but is coldly rebuffed.</p><h3>The Circuit Race</h3><p>Looking at the schedule, the party learns about the upcoming extracurricular <strong>Circuit Race</strong> at the {{page:Apex Ring}}. {{page:Lomi}} excitedly explains the sport, revealing himself as a massive fan who grew up watching and analyzing the massive rigs and <strong>Energy Spires</strong>.</p><h3>Trading Secrets with Lucky</h3><p>That evening, {{page:Lomi}}, {{page:Ignatius}}, and {{page:Iggy}} track down {{page:Lucky}} to get the study guide written by {{page:Valentine Sterling}}. Lucky refuses coin, demanding secrets instead. {{page:Ignatius}} weaves a magnificent Ash-Blood creation myth—the tale of the Sky Dragon and Sea Dragon whose tragic embrace formed the Ash-Blood Isles. Impressed, Lucky hands over the questions, but demands *real* secrets for the answers. He notices {{page:Iggy}}'s strange golden entrance exam receipt and suddenly ushers them into a private room, sensing a much deeper mystery.</p><h3>Key Moments</h3><ul><li>{{page:Ignatius}} takes a piece of chalk to the forehead and shares the Ash-Blood Genesis Myth with {{page:Lucky}}</li><li>{{page:Lomi}} clashes with the {{page:Snobbish Student}} and shares his deep knowledge of the Circuit Race</li><li>{{page:Iggy}}'s golden exam receipt catches {{page:Lucky}}'s attention, leading to a secret meeting</li><li>The party learns about the grueling schedule and the looming Friday exam</li></ul>"
                }
            ]
        },
        "pcs": {
            "name": "Player Characters",
            "pages": [
                {
                    "name": "Britt",
                    "sort": 100,
                    "content": "<h2>Britt</h2><table><tr><td><strong>Player</strong></td><td>Sophie</td></tr><tr><td><strong>Clan</strong></td><td>Mizizi (gray fungal-turtle)</td></tr><tr><td><strong>Class</strong></td><td>Guardian</td></tr></table><h3>Who Is Britt?</h3><p>A quiet, protective Mizizi student — a gray fungal-turtle who leads with instinct over words. She carries a petrified acorn necklace, a family heirloom she defended fiercely during an ambush.</p><h3>Key Moments</h3><ul><li><strong>Session 0:</strong> Paired with {{page:Aggie}} during the Trial of Beasts — intervened to protect her when a creature attacked</li><li><strong>Session 1:</strong> Attended the {{page:Block 99}} bonfire, observed the social dynamics</li><li><strong>Session 2:</strong> Deepened her bond with the party at the bonfire</li><li><strong>Session 3:</strong> Ambushed by {{page:Azor}}, Zyykl, and Tus in an alley. Lost her test receipt but fought back to recover her family necklace. Took {{page:Azor}}'s pocket watch as compensation</li></ul><h3>Open Threads</h3><ul><li>Her test receipt was stolen — will the Loom still recognise her?</li><li>The petrified acorn necklace — what is its significance?</li><li>Needs to find {{page:Lucky}} and get the study guide</li></ul>"
                },
                {
                    "name": "Aggie",
                    "sort": 200,
                    "content": "<h2>Aggie</h2><table><tr><td><strong>Player</strong></td><td>Kristina</td></tr><tr><td><strong>Clan</strong></td><td>Mizizi (red-and-white spotted mushroom-turtle)</td></tr><tr><td><strong>Class</strong></td><td>Druid</td></tr></table><h3>Who Is Aggie?</h3><p>A warm, nurturing Mizizi student — a red-and-white spotted mushroom-turtle with an affinity for growing things and a protective streak toward her friends.</p><h3>Key Moments</h3><ul><li><strong>Session 0:</strong> Paired with {{page:Britt}} in the trial — stepped in when {{page:Britt}} froze</li><li><strong>Session 1:</strong> Bonded with {{page:Rill}} at the bonfire</li><li><strong>Session 2:</strong> Connected with {{page:Bramble}} over shared botanical interests</li><li><strong>Session 3:</strong> Responded to {{page:Britt}}'s distress call after the ambush</li></ul><h3>Open Threads</h3><ul><li>Her connection with {{page:Bramble}} — a kindred spirit?</li><li>Needs to find {{page:Lucky}} and get the study guide</li></ul>"
                },
                {
                    "name": "Ignatius",
                    "sort": 300,
                    "content": "<h2>Ignatius</h2><table><tr><td><strong>Player</strong></td><td>John</td></tr><tr><td><strong>Clan</strong></td><td>Ash-Blood (Ember Islander)</td></tr><tr><td><strong>Class</strong></td><td>Warrior</td></tr></table><h3>Who Is Ignatius?</h3><p>A passionate Ash-Blood from Ember Island — proud of his heritage and eager to forge connections. He felt the atmospheric energy surges more intensely than any other student.</p><h3>Key Moments</h3><ul><li><strong>Session 0:</strong> Paired with {{page:Lomi}} in the trial — clashed on approach but found mutual respect</li><li><strong>Session 1:</strong> Led the charge to the {{page:Block 99}} bonfire — the social organiser of the group</li><li><strong>Session 2:</strong> Engaged passionately in the Ash-Blood population discussion. Felt the atmospheric surge viscerally</li><li><strong>Session 3:</strong> Arrived to help {{page:Britt}} after the ambush</li><li><strong>Session 4:</strong> Took a piece of chalk to the head in Logistics class. Shared the Ash-Blood Genesis Myth (the tale of the Sky and Sea Dragons) with {{page:Lucky}} to barter for the study guide questions</li></ul><h3>Open Threads</h3><ul><li>The atmospheric surges — what is his connection to them?</li><li>His passionate advocacy for Ash-Blood culture</li><li>Needs to find {{page:Lucky}} and get the study guide</li></ul>"
                },
                {
                    "name": "Lomi",
                    "sort": 400,
                    "content": "<h2>Lomi</h2><table><tr><td><strong>Player</strong></td><td>Luke F</td></tr><tr><td><strong>Clan</strong></td><td>Harmony-born (Octoumba, Iron-Union)</td></tr><tr><td><strong>Class</strong></td><td>Bard</td></tr></table><h3>Who Is Lomi?</h3><p>A Harmony-born student from Octoumba in the Iron-Union — strategic, social, and sometimes impulsive. He has a darker edge that surfaced during the {{page:Azor}} interrogation.</p><h3>Key Moments</h3><ul><li><strong>Session 0:</strong> Paired with {{page:Ignatius}} in the trial — the planner to Ignatius's charger</li><li><strong>Session 1:</strong> Engaged with {{page:Lucky}}'s betting game at the bonfire</li><li><strong>Session 2:</strong> Observed the bonfire social dynamics</li><li><strong>Session 3:</strong> Won <em>Crown and Ruin</em> against {{page:Valentine Sterling}}. After {{page:Britt}}'s ambush, punched the subdued {{page:Azor}} hard enough to break his rib</li><li><strong>Session 4:</strong> Stressed about the upcoming exam. Clashed with a {{page:Snobbish Student}} over notes. Revealed his deep, extensive knowledge of the Circuit Race and its energy spires</li></ul><h3>Open Threads</h3><ul><li>His violent outburst against {{page:Azor}} — what does it reveal about him?</li><li>Plan to barter with {{page:Lucky}} for the study guide using the pocket watch</li></ul>"
                },
                {
                    "name": "Iggy",
                    "sort": 500,
                    "content": "<h2>Iggy</h2><table><tr><td><strong>Player</strong></td><td>Holly</td></tr><tr><td><strong>Clan</strong></td><td>Earthkin</td></tr><tr><td><strong>Class</strong></td><td>Wizard</td></tr></table><h3>Who Is Iggy?</h3><p>A quiet, mechanically brilliant Earthkin student. He's grumpy on the surface but secretly appreciates being included. He has a natural talent for blending in and slipping away unnoticed.</p><h3>Key Moments</h3><ul><li><strong>Session 0:</strong> Completed his trial solo — quiet but effective</li><li><strong>Session 1:</strong> Observed the bonfire from a crane above {{page:Block 04}}, then joined</li><li><strong>Session 2:</strong> Slipped away from the bonfire into the power plant</li><li><strong>Session 2.5:</strong> Explored the Walker-Core power plant. Met {{page:Tommy}} and {{page:Lucina}}. Had a deep conversation with {{page:Professor Kante}} about the resonator battery system. Received an umber crystal as a gift</li><li><strong>Session 3:</strong> Mapped the view from the {{page:Celestial Lounge}}, gaining a cartography experience. Arrived to help {{page:Britt}} after the ambush</li><li><strong>Session 4:</strong> Had a culinary awakening at breakfast. Accidentally revealed his golden entrance exam receipt to {{page:Lucky}}, prompting a secret meeting</li></ul><h3>Open Threads</h3><ul><li>{{page:Professor Kante}}'s invitation to return for tea and further research</li><li>The umber crystal — what can he build or learn from it?</li><li>Five connection experiments he devised after talking with Kante</li></ul>"
                }
            ]
        },
        "npcs": {
            "name": "NPCs",
            "pages": [
                {
                    "name": "Serra Vox",
                    "sort": 100,
                    "content": "<h2>Serra Vox</h2><img src='portraits/serra_vox_portrait.png' width='200' style='float:right;margin:0 0 10px 10px;border-radius:8px;'/><table><tr><td><strong>Role</strong></td><td>Student</td></tr><tr><td><strong>First Seen</strong></td><td>Session 1</td></tr></table><h3>Who Is Serra Vox?</h3><p>A confident, socially adept student who serves as the unofficial welcome committee. She invited the party to the {{page:Block 99}} bonfire and seems to know everyone.</p><h3>Interactions</h3><ul><li><strong>Session 1:</strong> Invited the party to the bonfire</li><li><strong>Session 2:</strong> Present at the bonfire, the centre of the social scene</li></ul>"
                },
                {
                    "name": "Lucky",
                    "sort": 200,
                    "content": "<h2>Lucky</h2><img src='portraits/lucky_portrait.png' width='200' style='float:right;margin:0 0 10px 10px;border-radius:8px;'/><table><tr><td><strong>Role</strong></td><td>Student Hustler</td></tr><tr><td><strong>First Seen</strong></td><td>Session 1</td></tr></table><h3>Who Is Lucky?</h3><p>A student who runs games of chance at social events. He's enterprising and always angling for a deal.</p><h3>Interactions</h3><ul><li><strong>Session 1:</strong> Ran a betting game at the bonfire — caught {{page:Lomi}}'s attention</li><li><strong>Session 3:</strong> Mentioned — bought {{page:Valentine Sterling}}'s \"study guide\". The party plans to find him and barter for it</li><li><strong>Session 4:</strong> Traded {{page:Valentine Sterling}}'s study guide questions to the party in exchange for the Ash-Blood Genesis Myth. Ushered them into a private room after seeing {{page:Iggy}}'s golden receipt</li></ul>"
                },
                {
                    "name": "Valentine Sterling",
                    "sort": 300,
                    "content": "<h2>Valentine Sterling</h2><img src='portraits/valentine_sterling_portrait.png' width='200' style='float:right;margin:0 0 10px 10px;border-radius:8px;'/><table><tr><td><strong>Role</strong></td><td>Student</td></tr><tr><td><strong>First Seen</strong></td><td>Session 1</td></tr></table><h3>Who Is Valentine Sterling?</h3><p>A well-connected student from a prominent family. He holds court at social gatherings and seems to know the inner workings of the Academy.</p><h3>Interactions</h3><ul><li><strong>Session 1:</strong> Discussed Academy politics at the bonfire</li><li><strong>Session 2:</strong> Continued socialising at the bonfire</li><li><strong>Session 3:</strong> Found playing <em>Crown and Ruin</em> with {{page:Ember}} at the {{page:Celestial Lounge}}. Lost to {{page:Lomi}}. Drunkenly admitted he wrote a deliberately hard test and sold it to {{page:Lucky}} as a \"study guide.\" Passed out</li></ul>"
                },
                {
                    "name": "Dean Isolde Vane",
                    "sort": 400,
                    "content": "<h2>Dean Isolde Vane</h2><img src='portraits/dean_isolde_portrait.png' width='200' style='float:right;margin:0 0 10px 10px;border-radius:8px;'/><table><tr><td><strong>Role</strong></td><td>Dean of Vumbua Academy</td></tr><tr><td><strong>First Seen</strong></td><td>Session 0</td></tr></table><h3>Who Is Dean Isolde Vane?</h3><p>The commanding head of Vumbua Academy. Formal and authoritative, she set the tone during the intake welcome — Vumbua is a proving ground, not a playground.</p><h3>Interactions</h3><ul><li><strong>Session 0:</strong> Addressed the incoming class after the trials</li></ul>"
                },
                {
                    "name": "Sarge",
                    "sort": 500,
                    "content": "<h2>Sarge</h2><table><tr><td><strong>Role</strong></td><td>Upperclassman</td></tr><tr><td><strong>First Seen</strong></td><td>Session 1</td></tr></table><h3>Who Is Sarge?</h3><p>A gruff older student who provides blunt, unvarnished perspective on Academy life. He doesn't sugarcoat things.</p><h3>Interactions</h3><ul><li><strong>Session 1:</strong> Gave the party a no-nonsense rundown of what to expect at the Academy</li></ul>"
                },
                {
                    "name": "Rill",
                    "sort": 600,
                    "content": "<h2>Rill</h2><img src='portraits/rill_portrait.png' width='200' style='float:right;margin:0 0 10px 10px;border-radius:8px;'/><table><tr><td><strong>Role</strong></td><td>Student (Mizizi exchange)</td></tr><tr><td><strong>First Seen</strong></td><td>Session 1</td></tr></table><h3>Who Is Rill?</h3><p>A Mizizi exchange student who bonded quickly with {{page:Britt}} and {{page:Aggie}} over shared cultural roots. She offered a Mizizi perspective on death and interconnection during the bonfire.</p><h3>Interactions</h3><ul><li><strong>Session 1:</strong> Introduced herself at the bonfire and bonded with the Mizizi PCs</li><li><strong>Session 2:</strong> Contributed to the Ash-Blood population discussion with a Mizizi perspective on death</li></ul>"
                },
                {
                    "name": "Percy Vane-Smythe III",
                    "sort": 700,
                    "content": "<h2>Percy Vane-Smythe III</h2><img src='portraits/percy_portrait.png' width='200' style='float:right;margin:0 0 10px 10px;border-radius:8px;'/><table><tr><td><strong>Role</strong></td><td>Student</td></tr><tr><td><strong>First Seen</strong></td><td>Session 2</td></tr></table><h3>Who Is Percy?</h3><p>An enthusiastic student who champions the <strong>Sixfold Theory</strong> — the fringe academic position that more elemental clans exist beyond the five currently known. Most students dismiss him, but his earnest arguing draws a crowd.</p><h3>Interactions</h3><ul><li><strong>Session 2:</strong> Argued loudly for the Sixfold Theory at the bonfire</li></ul>"
                },
                {
                    "name": "Zephyr",
                    "sort": 800,
                    "content": "<h2>Zephyr</h2><img src='portraits/zephyr_portrait.png' width='200' style='float:right;margin:0 0 10px 10px;border-radius:8px;'/><table><tr><td><strong>Role</strong></td><td>Student</td></tr><tr><td><strong>Race</strong></td><td>Unknown</td></tr><tr><td><strong>First Seen</strong></td><td>Session 2</td></tr></table><h3>Who Is Zephyr?</h3><p>An androgynous, mysterious figure who appeared at the edge of the bonfire. They say little and watch everything.</p><h3>Interactions</h3><ul><li><strong>Session 2:</strong> Appeared at the bonfire's edge. During the atmospheric surge, purple lightning crackled around them before they suppressed it</li></ul>"
                },
                {
                    "name": "Bramble",
                    "sort": 900,
                    "content": "<h2>Bramble</h2><table><tr><td><strong>Role</strong></td><td>Student</td></tr><tr><td><strong>First Seen</strong></td><td>Session 2</td></tr></table><h3>Who Is Bramble?</h3><p>A quiet, plant-like student who gravitated toward {{page:Aggie}} at the bonfire. They share an affinity for growing things.</p><h3>Interactions</h3><ul><li><strong>Session 2:</strong> Bonded with {{page:Aggie}} over botanical interests</li></ul>"
                },
                {
                    "name": "Professor Kante",
                    "sort": 1000,
                    "content": "<h2>Professor Kante</h2><img src='portraits/professor_kante_portrait.png' width='200' style='float:right;margin:0 0 10px 10px;border-radius:8px;'/><table><tr><td><strong>Role</strong></td><td>Professor of Harmonics</td></tr><tr><td><strong>Race</strong></td><td>Tortoise</td></tr><tr><td><strong>First Seen</strong></td><td>Session 2.5</td></tr></table><h3>Who Is Professor Kante?</h3><p>A large tortoise professor who works in the Academy's power plant. He wears a jaunty top hat, dresses dapperly, and speaks slowly and deliberately. He has a Galileo-like quality — a genius scientist whose ideas don't quite fit the mainstream.</p><h3>Interactions</h3><ul><li><strong>Session 2.5:</strong> Found {{page:Iggy}} sketching machinery in his office. Instead of reporting him, Kante was delighted by {{page:Iggy}}'s technical intuition. Gave him a lecture on the resonator battery system, gifted him an umber crystal, and invited him to return</li></ul>"
                },
                {
                    "name": "Tommy",
                    "sort": 1100,
                    "content": "<h2>Tommy</h2><table><tr><td><strong>Role</strong></td><td>Power Plant Clerk</td></tr><tr><td><strong>Race</strong></td><td>Gnome</td></tr><tr><td><strong>First Seen</strong></td><td>Session 2.5</td></tr></table><h3>Who Is Tommy?</h3><p>A gnome clerk who staffs the front desk of the Walker-Core power plant. He has a cute, feminine bearded face, big green eyes, and a pointy red hat. He wants to apply to the Academy next year.</p><h3>Interactions</h3><ul><li><strong>Session 2.5:</strong> Greeted {{page:Iggy}} at the power plant lobby but didn't stop him from wandering in</li></ul>"
                },
                {
                    "name": "Lucina",
                    "sort": 1200,
                    "content": "<h2>Lucina</h2><table><tr><td><strong>Role</strong></td><td>Power Plant Mechanic</td></tr><tr><td><strong>Race</strong></td><td>Dwarf</td></tr><tr><td><strong>First Seen</strong></td><td>Session 2.5</td></tr></table><h3>Who Is Lucina?</h3><p>A dwarf mechanic who works maintenance at the Walker-Core power plant. Wears mechanic overalls and questioned whether students are allowed in the back — but didn't stop {{page:Iggy}}.</p><h3>Interactions</h3><ul><li><strong>Session 2.5:</strong> Passed by {{page:Iggy}} in the power plant — asked {{page:Tommy}} if students are allowed, but took no action</li></ul>"
                },
                {
                    "name": "Ember",
                    "sort": 1300,
                    "content": "<h2>Ember</h2><img src='portraits/ember_portrait.png' width='200' style='float:right;margin:0 0 10px 10px;border-radius:8px;'/><table><tr><td><strong>Role</strong></td><td>Student</td></tr><tr><td><strong>Clan</strong></td><td>Ash-Blood</td></tr><tr><td><strong>First Seen</strong></td><td>Session 3</td></tr></table><h3>Who Is Ember?</h3><p>An Ash-Blood student who socialises with {{page:Valentine Sterling}}. She takes notes constantly and has a studious, observant quality. She represents the moderniser wing of the Ash-Blood community.</p><h3>Interactions</h3><ul><li><strong>Session 3:</strong> Found playing <em>Crown and Ruin</em> alongside {{page:Valentine Sterling}} at the {{page:Celestial Lounge}}. Lost the game and returned to taking notes</li></ul>"
                },
                {
                    "name": "Azor",
                    "sort": 1400,
                    "content": "<h2>Azor</h2><img src='portraits/azor_portrait.png' width='200' style='float:right;margin:0 0 10px 10px;border-radius:8px;'/><table><tr><td><strong>Role</strong></td><td>Failed Candidate</td></tr><tr><td><strong>First Seen</strong></td><td>Session 3</td></tr></table><h3>Who Is Azor?</h3><p>A smaller, scheming man who failed his candidacy run into the Academy. He recruited two bruisers — Zyykl and Tus — from Septal to form a theft ring targeting students' test receipts. Uses sign language to communicate with his crew.</p><h3>Interactions</h3><ul><li><strong>Session 3:</strong> Lured {{page:Britt}} into an alley and ambushed her with Zyykl and Tus. They stole her test receipt. {{page:Britt}} fought back, pinned him, and took his pocket watch. {{page:Lomi}} then punched him hard enough to break a rib. Defiant to the end: <em>\"You may paint me as the villain...\"</em></li></ul>"
                },
                {
                    "name": "Snobbish Student",
                    "sort": 1500,
                    "content": "<h2>Snobbish Student</h2><img src='portraits/finch_gable_portrait.png' width='200' style='float:right;margin:0 0 10px 10px;border-radius:8px;'/><table><tr><td><strong>Role</strong></td><td>Student</td></tr><tr><td><strong>Clan</strong></td><td>Harmony-born</td></tr><tr><td><strong>First Seen</strong></td><td>Session 4</td></tr></table><h3>Who Is This Student?</h3><p>A well-dressed, snobbish Harmony-born student in the Logistics class. He is highly competitive and refuses to share his notes.</p><h3>Interactions</h3><ul><li><strong>Session 4:</strong> Refused to let {{page:Lomi}} copy his notes after class, leading to a tense exchange</li></ul>"
                }
            ]
        },
        "locations": {
            "name": "Locations",
            "pages": [
                {
                    "name": "Vumbua Academy",
                    "sort": 100,
                    "content": "<h2>Vumbua Academy</h2><p>A vast mobile city-state that serves as the premier educational institution in Harmony. It recently relocated to a new frontier after 80 years of stagnation. The Academy runs competitive intake trials and sorts students into ranks.</p><h3>What Players Know</h3><ul><li>The intake trials test students in the {{page:Mizizi Petrified Forest}}</li><li>Students are sorted into ranks after the trials</li><li>Housing is in numbered Blocks — the party is in {{page:Block 04}}</li><li>The Upper Core houses upscale establishments like the {{page:Celestial Lounge}}</li><li>The Walker-Core power plant is staffed by non-students and uses Panda 5 resonator batteries</li><li>Population includes ~70,000 students, with a few hundred Ash-Bloods</li></ul>"
                },
                {
                    "name": "Mizizi Petrified Forest",
                    "sort": 200,
                    "content": "<h2>Mizizi Petrified Forest</h2><p>A haunted dead-land outside the Academy walls. Ancient petrified trees stand in eerie silence. This is where the intake trial takes place.</p><h3>What Players Know</h3><ul><li>The Trial of Beasts was held here — students were paired and tested against hostile fauna</li><li>{{page:Britt}} and {{page:Aggie}} were paired; {{page:Ignatius}} and {{page:Lomi}} were paired; {{page:Iggy}} went solo</li><li>The forest has a haunting, unsettling atmosphere</li></ul>"
                },
                {
                    "name": "Block 04",
                    "sort": 300,
                    "content": "<h2>Block 04</h2><p>The student housing district where the party was assigned rooms. A functional residential area with communal spaces.</p><h3>What Players Know</h3><ul><li>{{page:Britt}} and {{page:Aggie}} are roommates</li><li>{{page:Iggy}} was observed perching on a crane above the block</li></ul>"
                },
                {
                    "name": "Block 12",
                    "sort": 400,
                    "content": "<h2>Block 12</h2><p>Mentioned as part of the Academy's block system. Less explored by the party.</p>"
                },
                {
                    "name": "Block 99",
                    "sort": 500,
                    "content": "<h2>Block 99</h2><p>An older, more run-down district where upperclassmen throw unofficial social events. The unofficial social hub of the Academy.</p><h3>What Players Know</h3><ul><li>The welcome bonfire was held here across Sessions 1–2</li><li>Mix of students from all backgrounds — more relaxed than official Academy spaces</li><li>{{page:Serra Vox}} invited the party here</li><li>The bonfire was the site of the Ash-Blood population debate, {{page:Percy Vane-Smythe III}}'s Sixfold Theory arguments, and {{page:Zephyr}}'s purple lightning incident</li></ul>"
                },
                {
                    "name": "Celestial Lounge",
                    "sort": 600,
                    "content": "<h2>The Celestial Lounge</h2><p>A tall building in the Upper Core — the upscale social space of the Academy. Located on the top floor of the tallest building in the northwest district.</p><h3>What Players Know</h3><ul><li>Offers a sweeping, far-reaching view of Vumbua — {{page:Iggy}} used it to map the city</li><li>{{page:Valentine Sterling}} and {{page:Ember}} were found playing <em>Crown and Ruin</em> here</li><li>The party visited in Session 3 before the alley ambush</li><li>Has drinks including a \"Grease Shot\" that {{page:Iggy}} tried</li></ul>"
                },
                {
                    "name": "Walker-Core",
                    "sort": 700,
                    "content": "<h2>Walker-Core (Power Plant)</h2><p>The Academy's power plant, marked by a \"Vumbua POWER\" sign over the archway. Located near {{page:Block 99}}.</p><h3>What Players Know</h3><ul><li>Staffed by non-students: {{page:Tommy}} (gnome clerk), {{page:Lucina}} (dwarf mechanic)</li><li>Contains glowing crystals plugged into panels, connected to turbines and rotating machinery</li><li>Has offices on a catwalk level with chalkboards and stored crystals</li><li>Security is minimal — {{page:Iggy}} walked right in without being stopped</li><li>{{page:Professor Kante}}'s office and laboratory are here</li></ul>"
                },
                {
                    "name": "Apex Ring",
                    "sort": 800,
                    "content": "<h2>The Apex Ring</h2><p>A massive, mile-wide basin located at Vumbua Academy, capable of holding half a million spectators. It serves as the arena for the highly anticipated Circuit Race (Reszo Race).</p><h3>What Lomi Knows</h3><p>{{page:Lomi}} is a massive fan of the sport and grew up working on and analyzing the massive rigs and <strong>Energy Spires</strong>. He knows the arena features simulated terrain from various regions of Harmony.</p><h4>The Energy Spires</h4><p>Teams pilot custom vehicles around the ring to strike erupting \"Energy Spires\" with a metal rod to collect energy and light the central Grand Resonator. Spires are categorized by their Charge Yield (CU) and unique boons. Lomi knows several notable spires that populate the arena:</p><ul><li><strong>Chime Spire (Gilded):</strong> 80 CU (Major). A massive gold compass arc that plays a sustained chord when struck. Grants <em>Harmonic Lock</em>, stabilizing mass reduction physics.</li><li><strong>Umber Crystal (Umbra Mountain):</strong> 70 CU (Major). Deep violet glowing obsidian. Grants <em>Deficit Shear</em>, providing a flat -15 bonus to Craft Draw reduction.</li><li><strong>Soft Forge (Relina):</strong> 45 CU. Bronze-amber arc that shimmers like liquid metal.</li><li><strong>Lift Stone (Juxta):</strong> 40 CU. Blue-grey granite with orbiting rocks, projecting an updraft.</li><li><strong>Focus Glass (Timon):</strong> 35 CU. A clear lens that bends light.</li><li><strong>Live Soil (Feltland):</strong> 35 CU. Earthy arc encased in vines.</li></ul><h4>Rules & Trivia</h4><ul><li><strong>Contention Bonus:</strong> Syncing a spire while a rival is within reach grants an automatic +10 CU.</li></ul>"
                }
            ]
        }
    }
}

# Embed all portrait images
portraits = {}
for fname in sorted(os.listdir(PORTRAITS_DIR)):
    if fname.endswith('.png'):
        b64 = load_portrait(fname)
        if b64:
            portraits[fname] = b64
            print(f"  Embedded: {fname}")

data['portraits'] = portraits

with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

size_mb = os.path.getsize(OUTPUT) / (1024*1024)
print(f"\nOutput: {size_mb:.1f} MB")

# Validate
pages = []
for j in data['journals'].values():
    pages.extend(j['pages'])
names = set(p['name'] for p in pages)
all_content = ' '.join(p['content'] for p in pages)
links = re.findall(r'\{\{page:([^|}]+)', all_content)
missing = [l for l in links if l not in names]
img_refs = set(re.findall(r"src='portraits/([^']+)'", all_content))
missing_imgs = img_refs - set(portraits.keys())

print(f"Pages: {len(pages)}")
print(f"Links: {len(links)} ({len(set(links))} unique)")
print(f"Unresolvable: {missing if missing else 'None'}")
print(f"Image refs: {len(img_refs)}, missing: {missing_imgs if missing_imgs else 'None'}")

# Check for spoiler terms
for term in ['gold-rank', 'silver-rank', 'copper-rank', 'trench-kin', 'GM Note']:
    found = [p['name'] for p in pages if term.lower() in p['content'].lower()]
    if found:
        print(f"SPOILER WARNING: '{term}' found in: {found}")
