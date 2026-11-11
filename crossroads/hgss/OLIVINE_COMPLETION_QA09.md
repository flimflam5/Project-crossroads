# Olivine QA09 completion review

All **nine canonical enterable buildings**, **four preserved Black Ledger additions**
and **24 native city/interior/landmark maps** are registered. This checklist separates
implemented content, actual source comparison, automated checks, controller-driven
mGBA and owner Delta acceptance. **Final frozen V8 verification is pending.**
V7's actual tests are a diagnostic checkpoint; source previews are not playtests.

The detailed inventory is [OLIVINE_COMPLETION_QA09.json](OLIVINE_COMPLETION_QA09.json).
Exact final source revision/ROM checksum must be filled from the actual delivery
artifact after final source generation/build/testing. Neither compilation nor
connectivity alone certifies visual quality, and no blanket100% claim is made here.

## Building and interior checklist

| Building | Classification | Intended native interiors | Verification |
| --- | --- | --- | --- |
| Gym | HGSS canonical enterable building | Gym, Gym_Arena | Registered; V7 visited; finalV8/Delta pending |
| Pokemon Center | HGSS canonical enterable building | PokemonCenter_1F, PokemonCenter_B1F | Registered; V7 visited; finalV8/Delta pending |
| Poke Mart | HGSS canonical enterable building | Mart | Registered; V7 visited; finalV8/Delta pending |
| Glitter Lighthouse | HGSS canonical enterable building | Lighthouse_1F, Lighthouse_2F, Lighthouse_3F, Lighthouse_4F, Lighthouse_5F, Lighthouse_6F, Lighthouse_Balcony, Lighthouse_Elevator | Registered; V7 visited; finalV8/Delta pending |
| Fishing house | HGSS canonical enterable building | FishingHouse | Registered; V7 visited; finalV8/Delta pending |
| Trade house | HGSS canonical enterable building | TradeHouse | Registered; V7 visited; finalV8/Delta pending |
| Seal house | HGSS canonical enterable building | SealHouse | Registered; V7 visited; finalV8/Delta pending |
| Cafe | HGSS canonical enterable building | Cafe | Registered; V7 visited; finalV8/Delta pending |
| Port terminal | HGSS canonical enterable building | PortTerminal, PortQuay | Registered; V7 visited; finalV8/Delta pending |
| Joe Mercer residence | deliberate Black Ledger addition | Residence | Registered; V7 visited; finalV8/Delta pending |
| Accepted neighbour residence | deliberate Black Ledger addition | NeighborHouse | Registered; V7 visited; finalV8/Delta pending |
| Silph subsidiary office | deliberate Black Ledger addition | SilphOffice | Registered; V7 visited; finalV8/Delta pending |
| Harbor Office | deliberate Black Ledger addition | HarborOffice | Registered; V7 visited; finalV8/Delta pending |

## Reference-backed content and deliberate adaptations

Canonical entrance spacing and relative city geography come from the actual HGSS
mosaic and pinned event/matrix/prop/permission facts. The three homes share actual
0097: kitchen/fridge, rear window/bookcase/plant, table and seats. The actual0136
cafe raster supports its cream/checkered floor, two windows, NW/SW plants, communal
table and L-counter. Pale-blue home walls and cream cafe window/walls replace the
inaccurate red-curtained timber motif. A visible one-cell staff aisle prevents a
GBA-only closed floor pocket; the counter remains solid and supports real talk.

The Center's source raised rear deck is flattened for native GBA service systems.
The source-backed17x14 basement retains the entire public y12 waiting row, plants,
table, ten stools and terminal. Its private blue graphics replace the old mirror
stand-in. Dedicated current Ecruteak service output is copied because the source
matrices are exactly identical; old generic Center/Mart templates for other cities
remain unchanged. Olivine's own nurse, heal ID, scripts, stock, doors and map IDs
remain. The tall silver/salmon Gym spans its two stable native maps; the approved
owner Steel Gym facade remains a deliberate Black Ledger exterior exception.

Lighthouse floors retain the actual branched geometry:4F east window→balcony→south3F
and western stairs→upper floors. Native lift controls serve1F and6F without new
saved progress. Both visible lift panels and exits work. Source1F/2F plants, purple
light room and substantial circular mechanical lens housing are represented;
the existing beacon actor/scripts remain. Flat native rails/masonry replace
perspective models. The source map123 cylinder is a flat body around the U-shaped
balcony. Its sea is far below: every source-blocked water-adjacent edge is railed.
Off-public DS elevator machinery is documented as a cropped model, not a hidden room.

Port furniture matches its actual screenshot: tan planks, blue rug, white tables,
all eight yellow stools, aqua waiting seats and life rings. The quay includes the
rear terminal with all four doorway segments, docked blue/white ferry and both
sailboats. Original GBA art and repeated hull/window panels fit the hardware;
unused eastern ocean is cropped to40x27 while preserving actual public paths.
S.S. Aqua sailing/ship interiors/other-region arrivals are **outside this city pass**.
Its boarding boundary is explicit; accepted Harbor Office travel remains separate.

Joe's home, accepted neighbour home, Silph subsidiary and Harbor Office are
retained additions, not substitutes for canonical homes. City material corrections
include20 source-backed white fence cells,12 timber terrace-table cells, deck and
parasols, gray offshore boulders and preserved genuine cliff.65 obsolete source
model167 body cells now show actual sea. The south-facing GBA port keeps its north
covered approach and bounded east boardwalk. Full visible door leaves have matching
metadata/warps; port returns land outside on clear dry forecourt anchors.

## Actual verification and final gate

V7 ROM: `0734501b031d05156a28e685dc1c2748153cb065222bd67b0d2e7cea47fefbca`.
These are controller-driven mGBA tests, not owner manual Delta acceptance:

- All24 Olivine target maps visited; approach/transit included39 maps,182 transitions,
  53 explicit round-trip pairs and174 warp trials.
-27 service records passed, including real shop/heal/PC/office/home interactions
  and an actual Jasmine practice loss with local nurse/whiteout.
-21 Save/cold Continue records passed with exact party/boxes/bag/flags/starter
  integrity; source battery copies remained unchanged. Obsolete-coordinate
  migration fixtures are separately disclosed; no original private save is overwritten.
- Four elevator panel/exit combinations and six special journeys passed: source
  window return chain, both port sea/overhang/body cases, dry boardwalk/rightleaf
  return and both high-balcony rail/no-Surf attempts.

V8 changes to source props, palettes, lower Center floor and city materials require
fresh frozen-ROM builds and applicable controller reruns. The final artifact must
identify its exact source and SHA256. New Game/title/Continue, Joe/actions/starters,
services/battles and old-save compatibility must retain their regression coverage.
Owner Delta visual acceptance is still required. Source story, badges, rewards,
trades/Seal Case, new encounters and DS online functions remain expressly deferred.

## Evidence and remaining reference limits

- [Reference/build gallery](../qa/qa09/olivine-review/comparisons.html): actual
  published HGSS references with URL/SHA/dimensions; V7 native240x160 frames;
  corrected V8 authored layout previews clearly labelled STATIC, not gameplay.
- [Every landmark source prop instance](olivine-landmark-prop-coverage.json):42
  source instances each map to a native counterpart/footprint or precise adaptation;
  unhandled source instance count0 does not itself prove gameplay or visual approval.
- [Landmark reference index](olivine-landmark-visual-references.json) and
  [room source/design review](OLIVINE_ROOM_DESIGN_QA09.md).

The lighthouse source reference is an annotated published multi-floor composition,
not a raw DS-native screenshot. House/cafe reference publication scales differ
from native game resolution. No fake pixel1:1 comparison is asserted. The lift
cabin has source geometry/functional evidence but lacks a separately verified
full native HGSS cabin screenshot. The four Black Ledger additions have no HGSS
counterpart. These limits are explicit instead of inventing reference details.

## Delta final review

Back up/export your normal save. Import the uniquely named final ROM and a COPY of
the normal battery if Delta treats it as another game. Use Continue, not an older
emulator state. Enter each visible leaf independently and walk away after every
arrival. Visit all nine canonical buildings and four additions; use the shop,
heal/PC/home/office/harbor functions. Walk every lighthouse stair and window branch,
choose both lift floors and exits, cross the port's main/side doors and dry boardwalk,
and test water/roof/body separation. Circle trees/building bases/boundaries and
check no arrows on ordinary ground. Save, reset to title, Continue and verify party,
starter, inventory and location. Final visual acceptance remains yours.
