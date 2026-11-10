# Black Ledger QA05 — Ecruteak interiors and Joe field actions

Continue feature/hgss-ecruteak-reconstruction-01 from QA04. This is an
Ecruteak QA increment, not a claim of region-wide HGSS completion or owner visual
acceptance. Preserve the owner's liked city exterior. Its only ground-layout
change is opening the canonical second house door. Existing road apertures now
traverse the reference west/east gatehouses. All existing map/layout/heal IDs
retain their order; six new maps append after QA04's station/corridor/Trail.

## Implemented

- Furnished southwest and second houses; the latter has ambient residents and
  does not award the HGSS Dowsing Machine or import its story flags.
- Dance Theater stage, seating and five original GBA kimono performers. All five
  participate in the existing optional short performance; no compulsory battles.
- Dedicated Ecruteak Center/Mart layouts, native healing/PC/shop behaviors and a
  reachable Center basement. Accepted stock and nurse/local heal IDs remain.
  DS online desks explicitly say offline; no internet functionality is claimed.
- Reference west/east gatehouses at existing Route38/42 road apertures. Shared
  border terrain remains compatible; three coordinate aliases cover each road.
- Source-derived station/corridor; monk moved off the source's story choke point.
- Bellchime Trail's broad autumn opening and bends follow canonical permission
  geometry, with leaf stretches and broken paving instead of the two-tile draft.
- Bell Tower1–10F and rooftop, branching stairs, warp pads and one-way plank jumps.
  Burned Tower1F/B1F have distinct charred timber, lower stone and rubble. Existing
  ambient interactions remain; the accepted bell interaction is on the rooftop.
- Gym's HGSS bridge follows the canonical geometry. Its two existing map IDs
  hold the two sections; stepping off returns Joe to the entrance. Morty and the
  student retain optional practice battles; no badge or new encounter decisions.
- Corporate Joe art/wiring for Fly/shared field pose, Surf, Dive, both bikes,
  fishing, watering and decorating. Authored east views preserve satchel position.
  Existing owner walking/running, trainer/Card art, gender and save format remain.

## Save compatibility

Back up your battery save. Import the new ROM and use normal **Continue** rather
than an older emulator snapshot. Old cached map tiles/layout pointers are refreshed
for Johto rooms; positions newly blocked by geometry/NPCs move to nearby safe floor.
An old Ecruteak heal doorway at(21,35) migrates to the same Center's new outdoor
(45,56) doorway. Its new indoor whiteout arrival is(8,13), in front of the nurse.
Party/boxes/starter variables and badges are not migrated or rewritten.

## Actual verification and remaining scope

See [ECRUTEAK_QA05.md](hgss/ECRUTEAK_QA05.md) for per-area references, deviations,
actual emulator coverage, commands and unresolved work. Automated structural tests
are separate from controller-driven mGBA checks. Neither is owner visual acceptance.
Johto outside Ecruteak is preserved; this release does not make it HGSS-complete.

## Delta checklist

1. Back up/export your save, import QA05 and use Continue. Confirm Joe, starter,
   party, boxes, money and existing progress. Test Running Shoes.
2. Fly Olivine -> Ecruteak -> another city and back. Cancel Fly once. Surf in four
   directions and disembark; check that Joe appears during field actions.
3. Walk Olivine/Route39/Route38 through the west gate, then the east gate to Route42
   and back. Test the south Route37 boundary and all house/service/Gym doors.
4. Examine the two houses, Theater show, Mart, Center healing/PC and basement stairs.
   Save/reset/Continue in a house and the Center. Check camera edges and furniture.
5. Traverse Station -> corridor -> autumn Trail -> Bell Tower through10F/roof and
   return. Test plank jumps/pads/stairs both ways, the bell, and Burned Tower's floor.
6. Explore the Gym bridge, deliberately step off, decline/accept optional battles,
   and test a loss after healing locally. Check respawn/healing and repeat battles.
7. Walk against walls/trunks and under intended canopies/roof edges from all sides.
   Send screenshots of visual issues with the map and approximate position.

Visual acceptance remains the project owner's. No new story or badges were added.
