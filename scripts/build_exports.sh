#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOCS="$REPO_ROOT/docs"
OUT="$REPO_ROOT/exports"

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
  "$DOCS/characters/player-characters/britt.md" \
  "$DOCS/characters/player-characters/aggie.md" \
  "$DOCS/characters/player-characters/ignatius.md" \
  "$DOCS/characters/player-characters/lomi.md" \
  "$DOCS/characters/player-characters/iggy.md"

concat "02-characters-npcs-faculty.md" \
  "$DOCS/lore/characters/npcs/dean-isolde-vane.md" \
  "$DOCS/lore/characters/npcs/celia-vance.md" \
  "$DOCS/lore/characters/npcs/hesperus.md" \
  "$DOCS/lore/characters/npcs/ratchet.md" \
  "$DOCS/lore/characters/npcs/kojo.md" \
  "$DOCS/lore/characters/npcs/pyrrhus.md"

concat "03-characters-npcs-squads.md" \
  "$DOCS/lore/characters/npcs/valerius-sterling.md" \
  "$DOCS/lore/characters/npcs/serra-vox.md" \
  "$DOCS/lore/characters/npcs/cassius-thorne.md" \
  "$DOCS/lore/characters/npcs/iron-jaw-jax.md" \
  "$DOCS/lore/characters/npcs/maria-wall.md" \
  "$DOCS/lore/characters/npcs/brawn.md" \
  "$DOCS/lore/characters/npcs/nyx.md" \
  "$DOCS/lore/characters/npcs/kaelen.md" \
  "$DOCS/lore/characters/npcs/mira.md" \
  "$DOCS/lore/characters/npcs/calculus-prime.md" \
  "$DOCS/lore/characters/npcs/theorem.md" \
  "$DOCS/lore/characters/npcs/lemma.md" \
  "$DOCS/lore/characters/npcs/dr-rose-halloway.md" \
  "$DOCS/lore/characters/npcs/silas-thorne.md" \
  "$DOCS/lore/characters/npcs/bramble.md" \
  "$DOCS/lore/characters/npcs/cinder-4.md" \
  "$DOCS/lore/characters/npcs/hearth.md" \
  "$DOCS/lore/characters/npcs/kindle.md" \
  "$DOCS/lore/characters/npcs/captain-barnacle.md" \
  "$DOCS/lore/characters/npcs/pressure.md" \
  "$DOCS/lore/characters/npcs/depth.md" \
  "$DOCS/lore/characters/npcs/percival-vane-smythe-iii.md" \
  "$DOCS/lore/characters/npcs/lady-glimmer.md" \
  "$DOCS/lore/characters/npcs/baron-bolt.md" \
  "$DOCS/lore/characters/npcs/sarge.md" \
  "$DOCS/lore/characters/npcs/lucky.md" \
  "$DOCS/lore/characters/npcs/pudge.md"

concat "04-characters-npcs-notable.md" \
  "$DOCS/lore/characters/npcs/lady-ignis.md" \
  "$DOCS/characters/npcs/lady-ignis.md" \
  "$DOCS/lore/characters/npcs/rill.md" \
  "$DOCS/characters/npcs/rill.md" \
  "$DOCS/lore/characters/npcs/zephyr.md" \
  "$DOCS/lore/characters/npcs/lance.md" \
  "$DOCS/characters/npcs/lance.md" \
  "$DOCS/lore/characters/npcs/valerius-sterling-sr.md" \
  "$DOCS/lore/characters/npcs/lady-glissade.md"

concat "05-clans.md" \
  "$DOCS/lore/factions/clans/trench-kin.md" \
  "$DOCS/lore/factions/clans/wadi.md" \
  "$DOCS/lore/factions/clans/renali.md" \
  "$DOCS/lore/factions/clans/fulgur-born.md"

concat "06-harmony-factions.md" \
  "$DOCS/lore/factions/harmony/overview.md" \
  "$DOCS/lore/factions/harmony/vane-lineage.md" \
  "$DOCS/lore/factions/harmony/house-gilded.md" \
  "$DOCS/lore/factions/harmony/syndicate-of-sails.md" \
  "$DOCS/lore/factions/harmony/verdant-trust.md" \
  "$DOCS/lore/factions/harmony/grand-architects.md" \
  "$DOCS/lore/factions/harmony/high-justiciars.md" \
  "$DOCS/lore/factions/harmony/scrivener-guild.md" \
  "$DOCS/lore/factions/harmony/iron-union.md"

concat "07-world-and-bestiary.md" \
  "$DOCS/lore/world/the-bleed.md" \
  "$DOCS/lore/world/the-minimum.md" \
  "$DOCS/lore/world/pre-stitch-artifacts.md" \
  "$DOCS/lore/bestiary/ether-jelly.md" \
  "$DOCS/lore/bestiary/void-beast.md" \
  "$DOCS/lore/bestiary/rot-shepherd.md" \
  "$DOCS/lore/bestiary/whispering-moth.md"

concat "08-locations.md" \
  "$DOCS/lore/locations/vumbua-academy.md"

concat "09-reference.md" \
  "$DOCS/lore/glossary.md" \
  "$DOCS/lore/timeline.md" \
  "$DOCS/lore/knowledge-tracker.md"

concat "10-sessions.md" \
  "$DOCS/sessions/session-00.md"

concat "11-session-raw-transcripts.md" \
  "$DOCS/sessions/s0-raw.md" \
  "$DOCS/sessions/s1-raw.md"

concat "12-session-planning.md" \
  "$DOCS/sessions/s2-planning.md" \
  "$DOCS/sessions/bonfire_scene.md"

echo "Export complete. Files in $OUT:"
ls -lh "$OUT"
