# Visual/collision repair checkpoint 0.9.1

0.9 connectivity works according to the owner. Its visual/collision QA did NOT
pass. Expansion is paused. Owner visual acceptance of this repair remains pending.

## Exact scope

- Ecruteak City exterior: Bell/Burned Tower forecourts and garden approaches;
  assembled trees replacing isolated repeated foliage strips. Ground-level custom
  building layers no longer use the roof foreground layer. Tower interiors are
  unchanged; this pass does not claim their individual visual review.
- Mahogany Town exterior: north street, workshop delivery yard, southern service
  lane and woodland placement; service/building thresholds remain at their IDs
  and coordinates. The rest of its interiors are not visually reviewed here.
- Mahogany Town Workshop: full cabinets/equipment, two assembled benches, sink,
  storage and clear walking/interaction aisles; room dimensions and exit retained.
- Route38: offset trail through two meadows and complete isolated trees.
- Route39: farm/pasture lane and planted groves; accepted grass encounters retained.
- Olivine City: shared lighthouse/house ground-layer attributes only; layout unchanged.

The 149-entry manifest records each map separately: five first-layout repair passes,
one shared-layer-only pass and 143 not individually visually reviewed. These are
review statuses, not assertions of final polish. Existing connections, events,
map/layout/heal IDs, saves and approved gameplay are preserved. No new geography,
story, trainers or encounters were introduced.

## Diagnosis and evidence

Original isolated tree stamps repeat one foliage tile in a 2x4 strip, without an
assembled base. Native root graphics also use the foreground layer; their Johto-only
copies now use the covered ground layer. The shared primary tileset is untouched.
Custom landmarks had the same foreground layer all the way to ground level;
the lower two rows now render behind an adjacent player. Roof rows remain foreground.
All door behavior values and solid building footprints remain intact.

Normal movement probes in the sampled areas blocked on solid walls, tree roots
and benches. We reproduced visual overlap; these tests do not establish that every
reported region-wide issue was merely cosmetic. The Mahogany house's north roof
edge is deliberately passable: Joe walks behind the overhang, is blocked by the
wall below, and can leave normally. That case is recorded separately from defects.

before/ and after/ contain actual emulator screenshots at 240x160 and native-resolution
movement MP4s. No generated concept art stands in for gameplay evidence. Bell,
Burned and tree-side captures use matching positions; the after tree-front capture
is one tile closer to the new complete base. Workshop comparison includes the
entry view before and an aisle view after; camera position therefore differs.
Clips show controller movement, including collisions; they are not exhaustive
recordings of the entire 126-probe test. Coordinates/results are in collision-probes.json.

## Verification and limits

- Real Emerald build PASS; ROM used 29,455,592 bytes; EWRAM 226,448; IWRAM 28,392.
- Structural149-map graph,285 warp entries,70 directed borders PASS.
- Changed-area controller tour:70 transitions,22 unique roundtrip pairs PASS.
- 126 actual controller collision probes PASS. Native screenshots inspected by Codex;
  owner visual acceptance remains pending.
- Actual normal roof-overhang movement and wall blocking PASS.
- Normal in-game Save/fresh-core Continue at Mahogany Workshop and Ecruteak precinct
  PASS, preserving exact party record, starter value and position.
- Existing-area emulator regression PASS: all three rescue choices, duplicate guard,
  met location, Joe, services, old travel and landmark stairs/interactions. This
  runner uses disclosed debugger-assisted fixtures; it is not owner playtesting.
- Existing assertions retained. New validator pins all 149 map-event metadata hashes,
  map/layout/heal contracts, unchanged encounter/starter/title sources, exactly the
  five recorded layout changes, ground-layer/door behavior and assembled benches.
  The tour's status wording now says 'target maps' rather than 'new maps'.

Test setup suppresses random encounters in RAM and uses existing HP fixtures for
repeatability. No map/warp debugger writes in the movement tour or collision probes.
Build success/connectivity do not imply visual approval. No claim of region-wide
building/tree, route/interior or level-design completion is made.

## Delta QA

1. Export/backup your battery save. Import the extracted 0.9.1 ROM and a COPY of the
   existing save, then use normal Continue. Do not reuse an older emulator save state.
2. Revisit both Ecruteak towers. Walk along each wall from all four sides and
   compare foreground overlap at the front, side and rear. Enter, climb, descend,
   leave, then save/reset/Continue. Inspect the forecourts and approaches critically.
3. Walk around Ecruteak's complete trees, especially between residence and theater.
   Stand directly south of the base and approach from all four directions.
4. In Mahogany, inspect workshop exterior/yard and enter. Walk around both benches,
   storage and sink; read notes/talk to the worker; leave and re-enter. Save/reload.
5. Traverse Routes38/39 both ways, inspect new trail/tree placement, visit farm/barn,
   and confirm familiar approved encounters and optional trainers still behave.
6. Check Olivine lighthouse/house foreground overlap, title/music, Joe, party and
   existing services. Try the rescue case again: no duplicate starter should appear.
7. Report map, exact side/object, last entrance and screenshot/video for any remaining
   wall penetration, wrong overlap, assembly, arrival or design issue.

## Resumable checkpoint

Branch feature/johto-visual-collision-01. Source commit/checksum are supplied in the
artifact's build-info.json. Generators: visual_repairs.py, area_layouts.py,
build_johto_network.py and build_area_art.py. Run validate_visual_repairs.py plus
existing validators and build. Next work is individual review of the 143 unreviewed
maps and outstanding parts of these six areas, not geographic expansion. Do not
propagate a visual pattern solely because a validator passed.
