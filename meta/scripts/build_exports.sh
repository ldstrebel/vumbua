#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VAULT="$REPO_ROOT"
OUT="$REPO_ROOT/meta/exports"

rm -rf "$OUT"
mkdir -p "$OUT"

concat() {
  local outfile="$1"
  shift
  for f in "$@"; do
    if [ -f "$f" ]; then
      cat "$f"
      printf '\n\n---\n\n'
    fi
  done > "$OUT/$outfile"
}

concat "01-characters-pcs.md" \
  "$VAULT/lore/characters/player-characters/britt.md" \
  "$VAULT/lore/characters/player-characters/aggie.md" \
  "$VAULT/lore/characters/player-characters/ignatius.md" \
  "$VAULT/lore/characters/player-characters/lomi.md" \
  "$VAULT/lore/characters/player-characters/iggy.md"

concat "02-characters-npcs-faculty.md" \
  "$VAULT/lore/characters/npcs/dean-isolde-vane.md" \
  "$VAULT/lore/characters/npcs/celia-vance.md" \
  "$VAULT/lore/characters/npcs/hesperus.md" \
  "$VAULT/lore/characters/npcs/ratchet.md" \
  "$VAULT/lore/characters/npcs/kojo.md" \
  "$VAULT/lore/characters/npcs/pyrrhus.md"

concat "03-characters-npcs-squads.md" \
  "$VAULT/lore/characters/npcs/valerius-sterling.md" \
  "$VAULT/lore/characters/npcs/serra-vox.md" \
  "$VAULT/lore/characters/npcs/cassius-thorne.md" \
  "$VAULT/lore/characters/npcs/iron-jaw-jax.md" \
  "$VAULT/lore/characters/npcs/maria-wall.md" \
  "$VAULT/lore/characters/npcs/brawn.md" \
  "$VAULT/lore/characters/npcs/nyx.md" \
  "$VAULT/lore/characters/npcs/kaelen.md" \
  "$VAULT/lore/characters/npcs/mira.md" \
  "$VAULT/lore/characters/npcs/calculus-prime.md" \
  "$VAULT/lore/characters/npcs/theorem.md" \
  "$VAULT/lore/characters/npcs/lemma.md" \
  "$VAULT/lore/characters/npcs/dr-rose-halloway.md" \
  "$VAULT/lore/characters/npcs/silas-thorne.md" \
  "$VAULT/lore/characters/npcs/bramble.md" \
  "$VAULT/lore/characters/npcs/cinder-4.md" \
  "$VAULT/lore/characters/npcs/hearth.md" \
  "$VAULT/lore/characters/npcs/kindle.md" \
  "$VAULT/lore/characters/npcs/captain-barnacle.md" \
  "$VAULT/lore/characters/npcs/pressure.md" \
  "$VAULT/lore/characters/npcs/depth.md" \
  "$VAULT/lore/characters/npcs/percival-vane-smythe-iii.md" \
  "$VAULT/lore/characters/npcs/lady-glimmer.md" \
  "$VAULT/lore/characters/npcs/baron-bolt.md" \
  "$VAULT/lore/characters/npcs/sarge.md" \
  "$VAULT/lore/characters/npcs/lucky.md" \
  "$VAULT/lore/characters/npcs/pudge.md"

concat "04-characters-npcs-notable.md" \
  "$VAULT/lore/characters/npcs/lady-ignis.md" \
  "$VAULT/lore/characters/npcs/rill.md" \
  "$VAULT/lore/characters/npcs/zephyr.md" \
  "$VAULT/lore/characters/npcs/lance.md" \
  "$VAULT/lore/characters/npcs/valerius-sterling-sr.md" \
  "$VAULT/lore/characters/npcs/lady-glissade.md"

concat "05-clans.md" \
  "$VAULT/lore/factions/clans/trench-kin.md" \
  "$VAULT/lore/factions/clans/wadi.md" \
  "$VAULT/lore/factions/clans/renali.md" \
  "$VAULT/lore/factions/clans/fulgur-born.md"

concat "06-harmony-factions.md" \
  "$VAULT/lore/factions/harmony/overview.md" \
  "$VAULT/lore/factions/harmony/vane-lineage.md" \
  "$VAULT/lore/factions/harmony/house-gilded.md" \
  "$VAULT/lore/factions/harmony/syndicate-of-sails.md" \
  "$VAULT/lore/factions/harmony/verdant-trust.md" \
  "$VAULT/lore/factions/harmony/grand-architects.md" \
  "$VAULT/lore/factions/harmony/high-justiciars.md" \
  "$VAULT/lore/factions/harmony/scrivener-guild.md" \
  "$VAULT/lore/factions/harmony/iron-union.md"

concat "07-world-and-bestiary.md" \
  "$VAULT/lore/world/the-bleed.md" \
  "$VAULT/lore/world/the-minimum.md" \
  "$VAULT/lore/world/pre-stitch-artifacts.md" \
  "$VAULT/lore/bestiary/ether-jelly.md" \
  "$VAULT/lore/bestiary/void-beast.md" \
  "$VAULT/lore/bestiary/rot-shepherd.md" \
  "$VAULT/lore/bestiary/whispering-moth.md"

concat "08-locations.md" \
  "$VAULT/lore/locations/vumbua-academy.md"

concat "09-reference.md" \
  "$VAULT/lore/glossary.md" \
  "$VAULT/lore/timeline.md" \
  "$VAULT/lore/knowledge-tracker.md"

concat "10-sessions.md" \
  "$VAULT/lore/sessions/transcripts/session-00.md"

concat "11-session-raw-transcripts.md" \
  "$VAULT/lore/sessions/transcripts/s0-raw.md" \
  "$VAULT/lore/sessions/transcripts/s1-raw.md"

concat "12-session-planning.md" \
  "$VAULT/lore/sessions/planning/s2/s2-planning.md" \
  "$VAULT/lore/sessions/planning/s2/bonfire_scene.md"

echo "Export complete. Files in $OUT:"
ls -lh "$OUT"
