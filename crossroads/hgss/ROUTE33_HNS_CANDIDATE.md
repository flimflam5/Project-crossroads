# Route 33 prototype — HGSS comparison and open work

Candidate source: `feature/hns-route33-prototype` at
`5c308d1fbc66e202ee6da0c4de712079955851b0`, based on the Azalea kiln B2
checkpoint `b4d14a260b`. This document is a review note, not proof of a build,
gameplay, save migration or visual acceptance. The current source is frozen for
an independent build and mGBA tests.

## Reference evidence

- Inspected [HGSS Route 33 image](https://media.pokemoncentral.it/wiki/thumb/7/70/Percorso_33_HGSS.png/513px-Percorso_33_HGSS.png),
  from [Pokémon Central's Route 33 page](https://wiki.pokemoncentral.it/Percorso_33_%28Johto%29).
  It shows the rocky Union Cave opening on the north side, a short westbound
  path to Azalea, trees and grass south and west, flowers near the cliff, and two
  Apricorn trees toward the lower right. Rain is an in-game weather effect.
- `crossroads/hgss/canonical_events/johto-outdoor-geometry.json`, `MAP_ROUTE_33`,
  records the HGSS world-matrix footprint as 32 × 32 and cave event (19,13)
  targeting Union Cave 1F anchor 2. It records two Apricorn objects at (23,26)
  and (24,26), a Hiker at (10,19) and a woman at (21,25). These are reference
  facts; they are not proof those events are present in Black Ledger. The
  extraction's original matrix and event blob references are in the JSON.
- The [HGSS walkthrough](https://bulbapedia.bulbagarden.net/wiki/Walkthrough%3APok%C3%A9mon_HeartGold_and_SoulSilver/Part_4)
  describes the westbound route from Union Cave to Azalea. Unlike the donor, HGSS
  does not put a direct Route 32 outdoor seam here.

## Candidate implementation and differences

- Preserves `MAP_JOHTO_ROUTE33` (75:83), `LAYOUT_JOHTO_ROUTE33`, its original
  32 × 24 size, west edge and offset −10 to Azalea, rain weather, existing
  resident and two sign interactions, and cave event at (24,7) targeting Union
  Cave warp 2. Union Cave and its reciprocal event have not been changed.
- Converts a 32 × 24 crop of Heart & Soul's 44 × 40 Route33_hns map (crop origin
  3,10). It retains the donor's general cave/cliff, grassy clearing, flower,
  path and tree motifs. Moving the cave to the HGSS coordinate (19,13), resizing
  the map to 32 × 32, or changing events would require a separately verified map
  and save migration; the current cave placement is an explicit deviation.
- Retains the exact old western seven columns to preserve the current town seam
  and compatible tileset rendering. This leaves a visible straight transition
  between the old generic path and donor art. It is not a faithful final HGSS
  street/path treatment and should be redesigned with the Azalea reconstruction.
  The candidate's tree geometry and weather are also 2D GBA interpretations.
- HGSS's two Apricorn objects and documented HGSS NPC positions do not currently
  exist in the matching locations. The donor's Headbutt-tree behavior is mapped
  to normal without adding its reward/encounter system; its extra Route 32 seam,
  progression triggers, story, trainer and wild-overworld actors are excluded.
  No item, badge, encounter roster or story decision is implied. Further visual,
  furnishing and interactive reconstruction remains open rather than represented
  as complete.
- Elevation-zero donor canopy cells beyond the west buffer receive collision to
  prevent traversal through the tree layer in this Emerald engine. This is a
  deliberate physics change, not evidence of correct in-game priority or all
  trunk/overhang behavior. Physical and rendered boundaries need normal gameplay
  inspection.

## Credits and provenance

Heart & Soul donor commit `167aa6d537b109bb229c231ddce4616974c4da71`; exact map
source path and SHA-256 plus the original Black Ledger west-buffer provenance are
in `crossroads/donor/hns-route33/README.md`. South-region tiles and palette source
hashes are already recorded in `crossroads/donor/hns_azalea_exterior/provenance.json`.
The donor requests Pokémon Heart and Soul and the upstream credit chain. Its
aggregate map credits include Crystal Advance/Kertra, Fire Gold/blackfragrant,
and SkidMarc25; aggregate tileset credits include Crystal Advance/Kertra, Ekat99,
TheDeadHeroAlistair, Johto Redrawn Team, zatavares852, lbsbezerra, WesleyFG and
Kalarie. Individual file authorship and explicit redistribution terms were not
established. These aggregate names are not assertions that each contributed to
this exact route.

## Source-only results and further verification

`validate_hns_route33.py` passes: source remapping, 7-column seam/boundary
resources, cave and west passage static connectivity, 327 reachable floor cells
and nearest-clear relocation modeling for 530 QA10 collision-free coordinates;
203 are newly blocked or occupied. An additional inspection of all 44 rows of
Azalea’s rightmost seven columns found only IDs 1, 198 and 514, as expected by
the seam resource checks; no in-game scroll is implied. A genuine QA10 normal Save and cold Continue
fixture at old position (22,7) was recorded outside Git; that position is blocked
in the candidate. The new ROM's behavior, resulting player visibility and saved
party/inventory have not yet been tested.

The network generator `--check`, Johto structural graph, opening, Olivine and
owner Gym source validators also passed on this candidate. The structural graph
uses survey-water assumptions and is not an emulator playtest. Build, actual
Azalea ↔ Route 33 scrolling in both directions, cave entry/return, the visibly
walkable path and trees from accessible sides, normal saving and Continue,
QA10 save migration, compiled tiles/palettes, full regressions, and owner Delta
visual acceptance are pending. Most other Johto areas remain earlier exploration
foundations; this prototype does not establish regional completion.
