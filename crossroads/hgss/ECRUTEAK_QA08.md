# Ecruteak QA08 — doorway repair checkpoint

Continues QA07 A1 (`8d13bd62ecaa3fa73ef4b1870cbb44cb369eeba6`) on
`feature/ecruteak-olivine-doorways-qa08`. The latest owner authorizes Olivine next,
with no expansion elsewhere. This is a repair checkpoint, not final city acceptance.

## Reproduced and corrected

- Theater left leaf44,45 was a solid wall with no warp. Both existing visible
  panels now enter, with corresponding left/right interior return destinations.
  Exterior alias16 appends; all historical indices remain stable. Pixels unchanged.
- Barrier Station exit10,11 had ordinary floor and no warp, while9,11 worked.
  Append exit2, retain staircase1, and pair the two leaves with city aliases7/1.
- Both road gatehouses have three-cell-high open aisles. Only their middle row
  exited. Append upper/lower aliases2–5; all three road rows enter and return
  through corresponding gate rows. Row-specific coordinate scripts retain the
  original temporary-variable contract and make no permanent progress grants.

Doors are specified independently in `doorways-qa08.json`. The new controller
test never falls back to a working neighbour. It starts from a copied normal
battery save, restores same-ROM trial snapshots, approaches each segment from its
front and available lateral landings, verifies destination, then actually walks
away. No player/map/warp coordinates are written. Ten of153 initial Ecruteak
approaches are physically unavailable beside signs or outside the bounded road;
143 were executed and passed. Skipped approaches are reported separately.
Additional tower/station threshold trials and the full landmark tour are separate.

Exact source revision and ROM SHA256 are in the delivered build-info. Baseline
door failures use the exact QA07 A1 ROM SHA256
`1553ad2872e5e0b4a5c5d9fe78d47b73d8f7a541ce294e897db20ded8a6e21c3`.
The gate baseline was recorded after the first two fixes, before gate repairs;
its own report identifies that different intermediate ROM. Never conflate them.

## Building inventory and HGSS comparison

`CITY_BUILDING_INVENTORY_QA08.json` records every canonical city building and
the three closed background homes. The cached HGSS city mosaic shows five home
facades, while pinned075_T27 events have exactly two house destinations: the
southwest home and the Dowsing house. The other three are genuinely closed in
HGSS; they are not missing accessible rooms disguised by new lock messages.
No additional private-door messages were added in QA08.

Both furnished homes, Theater/stage, Center/B1F, Mart, split Gym bridge, two road
gates, Station/corridor, Trail, Bell1F–10F/roof and Burned1F/B1F already existed
in QA07 and are retained. Their SHA-backed matrix, terrain, prop and warp facts
are actual HGSS references. All27 maps are visited in the new controller tour.

Necessary/current GBA deviations remain explicit:

- Flat metatiles and palette/layer masks replace perspective3D models. Owner
  Ghost Gym artwork supersedes the HGSS exterior by explicit approval.
- The tall Gym bridge spans two stable GBA maps, with safe fall returns. Optional
  practice battles remain; badges, source plot battles and rewards are deferred.
- Center's raised reception is flattened. Nurse, PC, shop and stairs work; DS
  online communication desks are offline, not an implemented network service.
- Bellchime moves four tiles south to fit the tall flat tower. Road gates use
  the existing boundary apertures instead of changing the liked street layout.
- House/Theater/service furniture is original GBA art guided by source geometry
  and prop facts. Separate complete native HGSS interior raster comparisons for
  those rooms are still incomplete; do not certify decorative1:1 matching.

## Verification and limits

BUILD PASS: local Emerald payload30,039,808/33,554,432 bytes; EWRAM226,448 and
IWRAM28,392 bytes. No save structures, trainer limits, IDs, approved encounters,
title/music, Joe sprites, starter scripts or battle teams change.

Automated validators retain immutable QA06 preservation, exact authorized QA08
door/event deltas, static exterior pixel identity, semantic trunks/walls and
all-public-tile escape. Added explicit threshold/reciprocal-arrival checks run in
CI. Generator checks cover the actual authored sources and generated outputs.
See VALIDATION_MIGRATION.md for narrow assertion changes.

Actual controller-driven mGBA gameplay (not a human manual playthrough):

-27-map city/landmark tour,296 transitions and every declared warp/stair/pad pair.
- Each specified public doorway leaf and all gate rows, both ways, lateral
  landings and safe departure; native clips retain failures and fixes.
- Ordinary paving has no stray arrows; six tree trunks resist36 specified
  approaches. Native foreground leaves are checked pixel by pixel.
- Five-person Theater show; actual Mart purchase; Center PC, exact party/box
  integrity, healing; both Gym falls; Morty practice loss/local whiteout.
- Normal Save → fresh emulator → title/Continue in a house and Center, plus the
  old cached-layout fixture. Original read-only owner/fixture SRAM is preserved.
- All three starter rescues, Olivine met origin/level, uniqueness and Joe walking.

The green-roof report is still not positively identified from the available
attachments. The owner was asked for its city/landmark and QA07 A1 filename;
do not claim a particular green-roof building fixed without that match. Current
gatehouse defects are independently reproduced and repaired. Owner Delta visual
acceptance, remaining interior raster comparisons and that report remain open.

## Delta checklist

Back up/export the current save. Import the uniquely named QA08 ROM, import a
copy of the normal battery save if Delta treats it as another game, and select
Continue. Do not restore an older emulator save state.

1. Enter Theater through each leaf independently; exit each red threshold. Walk
   left/right immediately after each arrival. Repeat at Barrier Station and Gym.
2. Cross west/east gates through upper, middle and lower aisle rows in both
   directions; repeat from each available side landing. Return to the same road.
3. Visit both homes, Mart, both Center levels; shop, use PC and heal. Save, reset
   to the title and Continue; check party, inventory, starter and location.
4. Walk Station → corridor → autumn Trail → Bell roof and back, and both Burned
   floors. Exercise stairs/pads/ledges and both leaves of tower floor exits.
5. Circle accessible building bases and all six free trees. Check foreground
   leaf/roof overlap and no arrows on ordinary paving, especially40,58–61.
6. Revisit the reported green-roof spot. Record the ROM filename and nearest
   landmark if any pass-through or entrance problem remains.

Olivine has its own forthcoming source/build checkpoint; do not label this repair
as an HGSS-complete Olivine release or either city100%.
