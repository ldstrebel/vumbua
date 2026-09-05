"""Configuration and registry loader for the Vumbua Editorial Harness.

Loads canonical characters, locations, tech, player registries, deny-lists,
and stylistic thresholds.
"""

import os
import re
import json
from pathlib import Path


def get_repo_root() -> Path:
    """Returns repository root directory."""
    # harness is in sessions/scripts/harness/
    return Path(__file__).resolve().parent.parent.parent.parent


def get_sessions_dir() -> Path:
    return get_repo_root() / "sessions"


# Real players & mics that should NEVER appear in published ebook prose or dialogue
DENY_LIST_PLAYERS = {
    "luke", "luke strebel", "luke s", "luke f", "luke foreman",
    "sophie", "sophie foreman", "sophie noone", "sophie foreman noone",
    "kristina", "christina", "kristina strebel",
    "john", "john hagey", "hagey",
    "holly", "holly strebel",
}

# TTRPG mechanics and system jargon that must not leak into in-universe novelization
DENY_LIST_MECHANICS = {
    "roll20", "roll 20", "d12", "d20", "d6", "d8", "d4", "d10", "d100",
    "armor slot", "armor slots", "agility roll", "stress slot", "stress slots",
    "hope point", "hope points", "fear point", "fear points",
    "character sheet", "character sheets", "roll for", "saving throw",
    "saving throws", "critical hit", "critical fail", "hit points",
    "difficulty class", "action token", "action tracker", "spell slot",
    "spell slots", "daggerheart", "roll with hope", "roll with fear"
}

# Real-world meta talk & technical audio chatter
DENY_LIST_OOC_REALIA = {
    "wi-fi", "wifi", "got disconnected", "was disconnected", "player disconnected",
    "disconnecting from the call", "lagging out",
    "mic check", "mute yourself", "you're muted", "unmute", "push to talk",
    "discord call", "discord server", "on discord", "zoom call", "google meet",
    "gas bill", "headset", "html file", "browser tab", "screen share", "screenshare"
}

# Common phonetic STT errors mapped to canonical in-universe names
PHONETIC_REPLACEMENTS = {
    "real": "Rill",
    "reel": "Rill",
    "vanball": "Bramble",
    "bramball": "Bramble",
    "nagy": "Aggie",
    "aggy": "Aggie",
    "agie": "Aggie",
    "ignatious": "Ignatius",
    "loami": "Lomi",
    "lowmi": "Lomi",
    "lumi": "Lomi",
    "iggie": "Iggy",
    "brit": "Britt",
    "professor inc": "Professor Ink",
    "professor inc.": "Professor Ink"
}

# Common filter words / crutches that dilute active prose
FILTER_WORDS = [
    r"\bfelt like\b",
    r"\bseemed to\b",
    r"\bcould hear\b",
    r"\bcould see\b",
    r"\bnoticed that\b",
    r"\bappeared as if\b",
    r"\bsuddenly\b",
    r"\ball of a sudden\b",
    r"\bstarted to\b",
    r"\bbegan to\b",
    r"\bin that moment\b"
]

# Sensory registers to monitor for balanced sensory prose
SENSORY_KEYWORDS = {
    "visual": ["glint", "shadow", "gleam", "pale", "dark", "crimson", "azure", "emerald", "silhouette", "glow", "mist", "flash"],
    "auditory": ["hum", "crack", "thud", "roar", "echo", "whisper", "creak", "crackle", "clang", "rattle", "whistle", "shout", "buzz"],
    "olfactory_gustatory": ["ozone", "sulfur", "brine", "copper", "damp", "smoke", "char", "musty", "bitter", "salt", "pine", "ash"],
    "tactile_kinetic": ["vibrate", "chill", "searing", "rough", "slick", "grime", "heft", "drag", "pulse", "stumble", "friction", "splinter"],
    "arcanatech_energy": ["resonance", "embodied energy", "current", "conduit", "frequency", "copper", "harmonic", "circuit", "lavsidian", "steam"]
}


def load_canonical_entities(repo_root: Path = None):
    """Dynamically loads canonical character and location names from repository files."""
    root = repo_root or get_repo_root()
    pcs = set()
    npcs = set()
    locations = set()

    # 1. Player Characters
    pc_dir = root / "characters" / "player-characters"
    if pc_dir.exists():
        for f in pc_dir.glob("*.md"):
            name = f.stem.replace("-", " ").title()
            pcs.add(name)
    # Default core PCs
    pcs.update({"Britt", "Aggie", "Iggy", "Ignatius", "Lomi", "Pip"})

    # 2. NPCs
    npc_dir = root / "characters" / "npcs"
    if npc_dir.exists():
        for f in npc_dir.glob("*.md"):
            name = f.stem.replace("-", " ").title()
            npcs.add(name)
    npcs.update({"Bramble", "Rill", "Saffron", "Cassius Thorne", "Serra Vox", "Dean Isolde Vane", "Mwaza-Kasa"})

    # 3. Lore locations and tech
    lore_dir = root / "lore"
    if lore_dir.exists():
        for f in lore_dir.glob("**/*.md"):
            locations.add(f.stem.replace("-", " ").title())

    locations.update({"Apex Arena", "Campus Harbor", "Deep-Hull", "Celestial Lounge", "Mizizi", "Renali", "Harmony", "Octoumba"})

    return {
        "pcs": sorted(list(pcs)),
        "npcs": sorted(list(npcs)),
        "locations": sorted(list(locations))
    }
