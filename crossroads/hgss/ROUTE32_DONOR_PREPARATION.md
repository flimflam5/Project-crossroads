# Route 32 donor staging — uninstalled

This branch stages an actual Heart & Soul Route 32, whose 42 × 103 cell
source is preserved under `crossroads/donor/hns-route32` with its pinned
source commit, hashes and aggregate credits. It changes no active map,
connection, script, save, heal location or encounter. Source inspection and
an offline donor render were compared to the HGSS Route 32 reference at
https://archives.bulbagarden.net/wiki/File:Johto_Route_32_HGSS.png. Neither
that offline render nor the staged graphics is an emulator playtest.

The donor shows the north gate, winding highland path, elevated crossing over
water, piers, southern Pokémon Center and Union Cave mouth. Its Center façade
and GBA landscape presentation differ from HGSS; its map additionally declares
a direct Route 33 southern connection, which is not a correct HGSS route
connection and must not be adopted. The donor tiles and bridge need detailed
reference comparison in game. This is an art/technical staging increment, not
a claim that Route 32 has been implemented or faithfully reconstructed.

`python3 crossroads/tools/stage_hns_route32.py --output /tmp/empty-stage-dir`
verifies every source SHA, stages 4,326 cells, 267 used metatiles, 301 used
8×8 graphics and the referenced palettes in an Emerald-sized primary set,
then checks source-to-output metatile references, layer and palette bits,
indexed pixels, map bits and source attributes. It requires an empty output
directory outside the repository. Palette 12 requires an appropriate secondary
palette; donor behavior values are copied, not proven engine-compatible.

Before installing, preserve the existing Violet shared-tile transition and
connection, coordinate the new Ruins gate and Union Cave exits against their
currently tested revisions, implement and test both directions of the Center
and gate, retain save/map IDs, add migration for old Route 32 positions and
resident states, and check field moves, surf, ledges and behavior mappings.
The present 28 × 64 route and its existing scripts/warps stay active. Do not
reuse donor story, trainers or rewards. Build and emulator-test the exact
installed candidate, including old saves and clipping, before offering it for
visual QA.

The recovered HGSS world-matrix reference describes Route 32 as 32 × 160,
with gate exits at (6,5)/(6,6), Center entrance at (20,130), and Union Cave
at (14,142). The H&S source compresses this geography to 42 × 103. The
separate `stage_hns_route32_violet_seam.py` prototype retains the donor at
36 × 110 after preserving seven rows of the accepted Violet seam; it does not
match canonical dimensions or those entrances and must not be installed as a
finished route. It does prove a graphics-packing approach: seven existing
Violet seam metatile IDs, their referenced graphics and palette banks remain
unchanged while 254 donor metatiles and 291 donor graphics fit in the primary
slots. Unsupported H&S headbutt behavior is reduced to ordinary behavior in
the staged copy only, leaving collision data intact. Its collision-only flood
reaches gate, Center approach and cave; this does not check directional movement,
field actions, doors or rendering.

A comparison of currently valid old walking cells against that candidate found
525 blocked, 91 elevation-1, 35 elevation-4 and 6 elevation-0 positions. Safe
old-save migration must account for sprite and Surf state and reachable dry
landings. The prototype is an intermediate engineering experiment, not a
replacement for building and validating the reference-sized route.
