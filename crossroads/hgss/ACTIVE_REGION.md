# Active Johto reconstruction — QA06 source checkpoint

Branch: feature/hgss-johto-gym-integration-01, based on526829f9674905d4d7efde83c65af65d31ebe3d6.
The owner wants the remaining HGSS Johto map, with supplied eight custom Gyms.
Do not restart Ecruteak or overwrite valid work. No story/teams/rosters/badges or
engine upgrade are authorized. See REGION_CHECKLIST.md and VIOLET_QA06.md.

## Surviving implementation

Eight original owner Gyms are really integrated with both doors and private city
resources, immutable QA05 baseline, exact PNG/non-Gym pixel/attribute/event checks.
Violet now has reference64x72 source-shaped terrain/pond/two original bridges,
corrected long purple-roof school, two furnished houses, dedicated services/B1F,
fixed-access Gym, all3 Sprout floors/branches and12x12 gatehouses. Source original
round-roof study is deliberately unused for the school. New maps append only.

The dedicated Violet generator owns13 maps and scoped Route31/36 gate portals /
Route32 northern7-row seam. Network skips owned rooms and invokes generators;
--check passes. Route32 primary shares General graphics/palettes and only adds
unused metatile1ff for safe common paving. All other terrain remains exact.
Do not let the immutable Gym baseline regenerate the old Violet draft.

Reference world facts for all ten towns/Routes29–48 and12 Violet room headers
are committed geometry/provenance, not completed reconstructions. Raw reference
archive/downloads are scratch only; no ROM or private save belongs in Git.

## Current build / validation

Latest real Emerald build: /tmp/qa06-school-build.log PASS. ROM used30,019,116B,
EWRAM226448/IWRAM28392; padded32MiB. ROM SHA256
28b12ad6b01a5ef765f313c6eff6a35eb6a512a823e315b0811b097a6e0d6f28.
Native13-map tour /tmp/qa06-source-final-tour.log PASS124 transitions.
Eight-Gym,526-edge collision sweep, both pedestrian bridges, normal Center/house/
Surf saves, synthetic obsolete walking position, exact party/boxes/starter, real
Morty loss to Violet nurse, ten-city Fly, Joe action/VRAM, three starter rescues
and title/reset checks PASS. Logs/evidence are in crossroads/qa/hgss-qa06.
Never report pending tests as passed. Owner visual acceptance remains pending.

A genuine new Surf-migration regression was caught: saved graphics IDs are byte
swapped by SaveObjectEvents. NeedsDryLanding now mirrors LoadObjectEvents, retaining
real Surf saves while moving obsolete walking saves newly covered by the pond.
Direct real Surf battery cold-Continue at(35,20) PASS on the current ROM.
Survey assistance clears on cold boot; tests must use the actual desk again.

Reproducible run logs: /tmp/qa06-exploration-proof.log (native views/bridge/
collision with --exploration-only); /tmp/qa06-save-proof.log (normal saves/
migration/whiteout with --saves-only); /tmp/qa06-source-final-gyms.log; subsequent Fly/Joe/starter/
title checks in /tmp/qa06-source-final-*.log. Use source battery COPY at
build/area-delivery-sram/EcruteakCity_BellTower-save.state.sav; never overwrite it.

## First unfinished work after this checkpoint

Finalize artifact source identity and delivery; draft PR #13 is open. No master
merge. Source commits3f25fa9a1c and175997877f were pushed; later evidence/CI fixes
are recorded by git log and build-info. CI found a missing Pillow import in the
minimal story job (now lazy) and an existing FireRed/LeafGreen compile leak of
the Emerald-only QA Fly flag (now guarded); do not claim all CI jobs pass unless
the actual latest run finishes. Local Emerald remains byte-identical after fixes.
 The whole Johto reconstruction remains open. Next section:
Routes31/32/36 from recovered world geometry and inspected rasters, then source
cave/ruins headers/interiors. Existing layouts outside Ecruteak/Violet are still
exploration drafts even though the eight Gym facades are new. Preserve map/layout/
heal ordinals, source generators, save compatibility, Joe/title/music, starters,
approved Route38/39 tables and practice battles. Record each actual reviewed area.
