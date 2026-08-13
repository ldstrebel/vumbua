#!/usr/bin/env python3
"""Turn a storyboard into clean-transcript entries the render can splice in.

The ancestral-vision sequence never reached the microphones — the GM sent the pages to
the table and the players read them silently — so it cannot come out of the attribution
pass. This module reads a `sN-vision-inserts.json` spec, extracts the storyboard's panel
descriptions, narration boxes, sound effects and speech bubbles, and resolves each
bubble's label to an identity **using only the spec's `speakers` map**. An unmapped label
is an error: a storyboard voice is never guessed at render time, and never quietly dropped.

Identity rules match the attribution stage: `NPC:<Name>` is a GM-voiced NPC and may not
name a character the session config declares, and a bare identity must be the GM or a
declared player character. Insert entries carry no microphone and no `person`; they are
labelled as storyboard material so they can never be mistaken for recorded speech.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract_storyboard
import session_config as sc

NPC_PREFIX = "NPC:"


class InsertError(Exception):
    pass


def resolve(identity, config, where):
    """Map a spec identity string onto (kind, identity), rejecting laundering."""
    if identity.startswith(NPC_PREFIX):
        name = identity[len(NPC_PREFIX):].strip()
        if not name:
            raise InsertError(f"{where}: empty NPC name")
        if name in config.characters or name == sc.GM_IDENTITY or name == config.gm:
            raise InsertError(
                f"{where}: {name!r} is declared in the session config, so it cannot be "
                f"attributed as an NPC. Use the identity {name!r} directly."
            )
        return "npc", name
    if identity == sc.GM_IDENTITY:
        return "gm", sc.GM_IDENTITY
    if identity in config.characters:
        return "player_character", identity
    raise InsertError(
        f"{where}: {identity!r} is neither the GM, a character the session config "
        f"declares, nor an NPC (`NPC:<Name>`)."
    )


def load(spec_path, config, sessions_dir):
    with open(spec_path, encoding="utf-8") as handle:
        spec = json.load(handle)

    if spec.get("session_id") != config.session_id:
        raise InsertError(
            f"{spec_path}: session_id {spec.get('session_id')!r} does not match "
            f"{config.session_id!r}"
        )
    anchor = spec.get("anchor", {}).get("after_line")
    if not isinstance(anchor, int):
        raise InsertError(f"{spec_path}: anchor.after_line must be a line number")

    repo_dir = os.path.dirname(os.path.abspath(sessions_dir))
    storyboard = os.path.join(repo_dir, spec["storyboard"])
    if not os.path.exists(storyboard):
        raise InsertError(f"{spec_path}: storyboard {spec['storyboard']} not found")

    speakers = {k: v for k, v in spec.get("speakers", {}).items() if not k.startswith("_")}
    narration_kind, narration_identity = resolve(
        spec.get("narration_identity", sc.GM_IDENTITY), config, spec_path
    )

    entries = []

    def narration(page, panel, role, text):
        if text:
            entries.append({
                "page": page, "panel": panel, "role": role,
                "kind": narration_kind, "identity": narration_identity,
                "label": None, "text": text.strip(),
            })

    for page in extract_storyboard.parse(storyboard):
        pg = page["page"]
        narration(pg, None, "setting",
                  f"{page['title']} — {page['scene_location']}".strip(" —"))
        for panel in page["panels"]:
            ref = f"p{pg}.{panel['panel']}"
            narration(pg, panel["panel"], "panel", panel["fallback"])
            for box in panel["narration"]:
                narration(pg, panel["panel"], "caption", box["text"])
            for bubble in panel["dialogue"]:
                label = bubble["label"]
                identity = speakers.get(f"{ref}:{label}", speakers.get(label))
                if not identity:
                    raise InsertError(
                        f"{spec_path}: storyboard bubble {ref} labelled {label!r} has no "
                        f"entry in `speakers`. Add {label!r} (or {ref}:{label!r}) — a "
                        f"storyboard voice is never guessed."
                    )
                kind, resolved = resolve(identity, config, f"{spec_path} ({ref})")
                entries.append({
                    "page": pg, "panel": panel["panel"], "role": "dialogue",
                    "kind": kind, "identity": resolved,
                    "label": label, "text": bubble["text"],
                })
            for sfx in panel["sfx"]:
                narration(pg, panel["panel"], "sound", sfx)

    return spec, anchor, entries


def entry_label(entry):
    ref = f"p{entry['page']}"
    if entry["panel"]:
        ref += f".{entry['panel']}"
    if entry["role"] == "dialogue":
        if entry["kind"] == "npc":
            return f"[[{entry['identity']}]] (NPC, voiced by GM, storyboard {ref})"
        return (f"[[{entry['identity']}]] (PC dialogue written by GM, storyboard {ref} "
                f"— not spoken on mic)")
    return f"[[GM]] (narration, storyboard {ref} {entry['role']})"
