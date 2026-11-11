# Ecruteak QA08 B2 — full-width gates and safe outside arrivals

Source/build identity is recorded in the accompanying build-info.json. Continues
A1 d3ab461912c51270b84d2eb8d9d7b3ee7a255717 without replacing the accepted city.
This is a tested checkpoint, not owner visual acceptance or a100% fidelity claim.

## Implemented

Retains the repaired Theater and Barrier Station leaves. Adds original GBA green
hipped-roof route-gate artwork, guided by the HGSS city mosaic. The west entrance
is now at the canonical x6,y38 center, with all three visible road rows usable.
The east gate straddles the existing city/Route42 seam. Their roofs cover the
walkable horizontal tunnel; front walls and roof ridges are solid. A roof above
Joe is intentional overlap, not permission to enter a wall.

All twelve gate exits now land outside the building, on separate return-only
anchors, and permit walking away. These append warp IDs; old IDs remain. Two
signs move outside the footprints so they cannot obstruct arrivals. Neither half
of any opening is hidden or closed to avoid fixing its warp.

City and adjoining route gate tiles share a narrow primary buffer; the routes
retain their WesternCity secondary. This preserves Route39's farm graphics at
the scrolling seam. Hardware tile mirroring saves graphics space, including in
the owner Ghost Gym, with exact decoded pixel comparisons. No palette count,
save structure, trainer limit, map/layout/heal ID or engine version changes.

## References, coverage and deviations

The inventory lists27 city/interior/landmark maps and all canonical buildings.
The source mosaic and pinned075_T27 event data distinguish two enterable homes
from three genuinely closed background houses. No new private-door messages
stand in for missing accessible rooms. Both homes, Theater/stage, Center/B1F,
Mart, Gym/bridge, gates, Station/corridor, Trail, Bell1–10F/roof and Burned1F/B1F
are retained, furnished and traversed. Owner Gym artwork is an approved addition.

Flat metatiles replace HGSS perspective models. Three-row side gates adapt the
DS horizontal tunnel to the existing roads; the eastern model crosses the map
seam. Center reception is flattened; DS online desks remain offline. Bellchime
has a four-tile southern allowance for the tall flat tower. The Gym bridge uses
two stable maps. Furniture follows source geometry/prop facts in native GBA art;
a complete separate HGSS interior raster comparison remains unfinished. Source
plot battles, rewards and badge progression remain intentionally deferred.

## Actual verification on the B2 delivery bytes

ROM SHA256:11ff9e15387d431c6bfb3b6f7b9642a922c80d7988be578aeedc93adc11d3632.
Emerald payload30,056,736/33,554,432; EWRAM226,448; IWRAM28,392 bytes.

Automated:24 generator/semantic/build-inclusion/source-preservation checks pass.
The new immutable A1 comparison preserves8,699 cells outside98 gate cells and
three sign cells; all six neighbouring viewport strips and53 decoded metatiles
remain identical. All49 shared gate tiles match. All eight owner Gyms match their
source pixels after hardware flips. Test migrations are in VALIDATION_MIGRATION.md.

Controller-driven mGBA, not human manual playtesting:

-27-map tour:308 transitions and73 explicit round-trip pairs.
-174 doorway approaches:161 executed PASS;13 physically unavailable lateral
  approaches explicitly skipped. All fronts execute; no fallback through a
  neighbouring leaf. Upper/middle/lower gate rows tested both ways, with exact
  outside arrivals and walking away.
-Ten new roof/wall/tunnel cases recorded using normal controller movement.
-19 ordinary-ground/tree/facade recordings,36 trunk approaches, no paving arrows;
  all423 expected foreground-leaf pixels match the captured hardware palette.
-Five Theater performers; actual Mart purchase; PC/box/party integrity; healing;
  both Gym falls; Morty practice loss and correct local whiteout.
-Normal Save/cold Continue in the house, Center and gate forecourt. A separately
  disclosed obsolete-coordinate fixture seeds a private copy before normal Save,
  then verifies safe cold Continue; no owner file is overwritten.
-All three live Silph starter rescues, correct met location/level, duplicate guards
  and walking animations, using the disclosed new-game RAM fixture.
-Joe Mach/Acro bike, all four Surf directions, rod/Surf/walking; native Fly to all
  ten existing QA destinations, cancellation, post-flight save/Continue.

See the evidence gallery and reports. Static full-map overview is labelled as a
layout render; it is not an emulator screenshot. Native frames/clips come from
actual controller tests of this exact ROM.

## Still open

Owner Delta visual acceptance; the exact original green-roof report has not been
positively identified from the available attachment/build information; complete
interior raster comparisons. Independently reproduced doorway/gate defects are
fixed and tested, but are not falsely attributed to that unmatched report.
Olivine's existing doors remain functional; its separate canonical reconstruction
is next. No other city/route expansion is authorized or included here.

## Delta review

Back up/export the normal save, import a copy into this uniquely named ROM and
use Continue, not an old emulator state. Enter/exit each Theater and Station leaf.
Cross both route gates on upper/middle/lower rows, approach laterally where space
exists, walk away after every arrival. Check walls from front/rear and roofs over
the tunnel. Visit both homes, shop/heal/PC, both Center floors, Theater/Gym, Trail,
all Bell/Burned floors; return home, Save/reset/Continue and verify starter/party.
Revisit the reported green-roof spot and note its landmark and ROM filename if
anything still fails. Visual acceptance remains the owner's decision.
