# Olivine architectural material correction after V7

An independent comparison of actual HGSS references, native static renders and
compiled V7 screenshots found that collision-only terrain classification had
mistaken fences, furniture and offshore boulders for earth cliffs. This is a
visual defect even when connectivity and wall tests pass. The correction uses
explicit source masks and original compatible GBA material modules.

## Corrected classifications

- The northwest court's white picket fence: source column6, rows10–33, and
  horizontal source sections. The exact surviving V7 fence contract has20
  cells: column6,rows10–19; row10,columns7–9 and17–20; and the northwest
  house garden edge at13,21–23. Other source fence segments were already
  covered/replaced by the documented Black Ledger/native-facade aprons; they
  are not silently counted as rendered fences. The genuine earth cliff at
  column26 remains untouched.
- Source model115's original table footprints: row42, columns7–10,14–17,29–32.
  These twelve obsolete blockers become timber deck because the complete native
  parasol/table objects were relocated. Their new bases still block correctly.
  Brown strips at Harbor8,42 and Silph31,42 were leftover table collision, not
  visible tables that should be treated as inaccessible side approaches.
- The main waterfront terrace uses timber deck, with white quay railing at its
  southern edge. Existing lower dry dock surfaces also use timber rather than
  grass. Accepted Black Ledger facades and stone entrance aprons stamp afterward
  so their exact pixels and doorway behavior remain.
- Parasols and the part of each moored sail over the terrace have a matching
  timber underlay. There are no grass rectangles underneath deck furniture.
- Offshore isolated blocked groups become rounded gray boulders over native sea.
  The attached lighthouse/main-road earth cliffs keep their original materials.
  The old DS model167 Port body, anchored at23.5,58, is specifically excluded
  from natural boulders:65 individually pinned formerly blocked cells become
  real sea after the GBA facade relocation. Existing public pier/apron/boardwalk
  cells remain. New Port/boat models retain their actual graphics and behavior.

## Scrolling and capacity

A fence at column6 lies inside the Route40 scrolling buffer. A private secondary
metatile there would reproduce earlier transition corruption. Three unused
primary metatiles0x100–0x102 use the shared native General gray palette and primary
glyphs outside animation slots. A narrow `HgssOlivineCoastBuffer` copies only those
metatiles/glyphs into the existing neutral General resource for Route40. Every
other route metatile, glyph, palette, raw map cell, map ID and connection remains.
Route39 and all Ecruteak resources are unchanged by this addition.

Original white fence, timber and gray boulder modules use an existing private
palette slot. Dry-run measurement is680 new graphics with121 free before the
owner's115-glyph Gym integration: six slots remain. No engine limits increase,
no accepted artwork is deleted, and the owner Gym remains independently checked.

## Verification changes

`validate_olivine_materials.py` pins V7 source
`3f935d5e8600c5a280b9172b555edb35ca52b6c0` and requires all city collision/elevation
bits to remain exact outside the twelve declared obsolete table cells and the
65 individually recorded obsolete model167 Port-body cells in
`contracts/olivine-port-model-qa09.json`. The latter become native sea after
the documented south-facing GBA facade relocation; public pier/apron/boardwalk
cells remain. The old DS building body is not mislabelled as natural rocks. The
twelve table cells must be visibly deck, clear and behaviorally ordinary; all65
Port-body cells must instead be real sea with native Surf behavior. Positive checks
require the actual white-fence/gray-boulder/deck cells, proper parasol grounding,
unchanged real cliffs, and exact original Route40 resources outside the three
new shared fence definitions/glyphs. The existing73-cell accepted Black Ledger
pixel proof, owner Gym comparison and doorway/save checks remain.

The harbor validator's boat mast underlay assertion changes specifically from
old stone paving to the new source-backed timber deck. Water under the sail,
Surf behavior/elevation, solid hull, roof layering, road openings and the actual
Port's two leaves remain asserted. No assertion is removed merely to obtain PASS.

Fresh native previews and final compiled-ROM movement/Save/Continue tests must
be recorded by the delivery checkpoint. This document does not assert owner
visual acceptance or equate compilation with gameplay verification.
