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
  "$VAULT/characters/player-characters/britt.md" \
  "$VAULT/characters/player-characters/aggie.md" \
  "$VAULT/characters/player-characters/ignatius.md" \
  "$VAULT/characters/player-characters/lomi.md" \
  "$VAULT/characters/player-characters/iggy.md"

concat "02-characters-npcs-faculty.md" \
  "$VAULT/characters/npcs/dean-isolde-vane.md" \
  "$VAULT/characters/npcs/celia-vance.md" \
  "$VAULT/characters/npcs/hesperus.md" \
  "$VAULT/characters/npcs/ratchet.md" \
  "$VAULT/characters/npcs/kojo.md" \
  "$VAULT/characters/npcs/pyrrhus.md"

concat "03-characters-npcs-squads.md" \
  "$VAULT/characters/npcs/valerius-sterling.md" \
  "$VAULT/characters/npcs/serra-vox.md" \
  "$VAULT/characters/npcs/cassius-thorne.md" \
  "$VAULT/characters/npcs/iron-jaw-jax.md" \
  "$VAULT/characters/npcs/maria-wall.md" \
  "$VAULT/characters/npcs/brawn.md" \
  "$VAULT/characters/npcs/nyx.md" \
  "$VAULT/characters/npcs/kaelen.md" \
  "$VAULT/characters/npcs/mira.md" \
  "$VAULT/characters/npcs/calculus-prime.md" \
  "$VAULT/characters/npcs/theorem.md" \
  "$VAULT/characters/npcs/lemma.md" \
  "$VAULT/characters/npcs/dr-rose-halloway.md" \
  "$VAULT/characters/npcs/silas-thorne.md" \
  "$VAULT/characters/npcs/bramble.md" \
  "$VAULT/characters/npcs/cinder-4.md" \
  "$VAULT/characters/npcs/hearth.md" \
  "$VAULT/characters/npcs/kindle.md" \
  "$VAULT/characters/npcs/captain-barnacle.md" \
  "$VAULT/characters/npcs/pressure.md" \
  "$VAULT/characters/npcs/depth.md" \
  "$VAULT/characters/npcs/percival-vane-smythe-iii.md" \
  "$VAULT/characters/npcs/lady-glimmer.md" \
  "$VAULT/characters/npcs/baron-bolt.md" \
  "$VAULT/characters/npcs/sarge.md" \
  "$VAULT/characters/npcs/lucky.md" \
  "$VAULT/characters/npcs/pudge.md"

concat "04-characters-npcs-notable.md" \
  "$VAULT/characters/npcs/lady-ignis.md" \
  "$VAULT/characters/npcs/rill.md" \
  "$VAULT/characters/npcs/zephyr.md" \
  "$VAULT/characters/npcs/lance.md" \
  "$VAULT/characters/npcs/valerius-sterling-sr.md" \
  "$VAULT/characters/npcs/lady-glissade.md"

concat "05-clans.md" \
  "$VAULT/factions/clans/trench-kin.md" \
  "$VAULT/factions/clans/wadi.md" \
  "$VAULT/factions/clans/renali.md" \
  "$VAULT/factions/clans/fulgur-born.md"

concat "06-harmony-factions.md" \
  "$VAULT/factions/harmony/overview.md" \
  "$VAULT/factions/harmony/vane-lineage.md" \
  "$VAULT/factions/harmony/house-gilded.md" \
  "$VAULT/factions/harmony/syndicate-of-sails.md" \
  "$VAULT/factions/harmony/verdant-trust.md" \
  "$VAULT/factions/harmony/grand-architects.md" \
  "$VAULT/factions/harmony/high-justiciars.md" \
  "$VAULT/factions/harmony/scrivener-guild.md" \
  "$VAULT/factions/harmony/iron-union.md"

concat "07-world-and-bestiary.md" \
  "$VAULT/world/the-bleed.md" \
  "$VAULT/world/the-minimum.md" \
  "$VAULT/world/pre-stitch-artifacts.md" \
  "$VAULT/bestiary/ether-jelly.md" \
  "$VAULT/bestiary/void-beast.md" \
  "$VAULT/bestiary/rot-shepherd.md" \
  "$VAULT/bestiary/whispering-moth.md"

concat "08-locations.md" \
  "$VAULT/locations/vumbua-academy.md"

concat "09-reference.md" \
  "$VAULT/glossary.md" \
  "$VAULT/timeline.md" \
  "$VAULT/knowledge-tracker.md"

concat "10-sessions.md" \
  "$VAULT/sessions/transcripts/session-00.md"

concat "11-session-raw-transcripts.md" \
  "$VAULT/sessions/transcripts/s0-raw.md" \
  "$VAULT/sessions/transcripts/s1-raw.md"

concat "12-session-planning.md" \
  "$VAULT/sessions/planning/s2/s2-planning.md" \
  "$VAULT/sessions/planning/s2/bonfire_scene.md"

echo "Export complete. Files in $OUT:"
ls -lh "$OUT"
