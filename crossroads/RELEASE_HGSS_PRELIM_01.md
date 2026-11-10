# Black Ledger — HGSS preliminary QA 01

This is an Ecruteak reconstruction draft, not a finished Johto release.
Source commit and ROM SHA-256 are included in the downloadable package.

## Implemented scope

Reference-backed 64x64 Ecruteak exterior, dedicated facade graphics, corrected
primary tileset loading during walking transitions, and the new Barrier Station,
underground corridor and Bellchime Trail connection to the existing Bell Tower.
Existing map/layout/heal IDs are preserved; new maps append. No save layout,
starter contract, approved encounters, practice teams, title or music changes.

## Known unfinished work

Station furnishings remain provisional. Houses, Gym and landmark floors are not
fully reconstructed against HGSS. Dowsing house is not yet enterable; Bell Tower
10F/summit are not added. Terrain detail and remaining regional visual/collision
reviews remain unfinished. Existing regional destinations are not a claim of
HGSS accuracy. The original New Game prologue is unchanged.

## Delta installation and focused QA

1. Export/back up your existing battery save and keep your previous ROM.
2. Download and extract the ZIP in iPhone Files. Open the enclosed .gba in Delta.
3. If Delta creates a separate game, import a COPY of your old battery save.
   Use normal Continue; do not load an emulator save state from an older ROM.
4. Check the title/music, Joe, starter, party, inventory and money after Continue.
5. Travel Olivine -> Route 39 -> Route 38 -> Ecruteak normally. Inspect the city
   boundary in both directions for scrambled graphics or abrupt terrain defects.
6. Walk around each Ecruteak building and tree from all sides. Walls and trunks
   must block; intentional roof/canopy overlap should look natural. Photograph
   clipping and include the direction you approached from.
7. Enter/leave the Center, Mart, house, Gym, theater and Burned Tower. Test healing
   and shopping. Interiors here are compatibility checks, not finished HGSS rooms.
8. Enter the northeastern Barrier Station, descend through the corridor, follow
   Bellchime Trail and enter Bell Tower. Return through the same chain. Test both
   stair directions and report unexpected arrival positions or trapping.
9. Save normally in Ecruteak and one new chain map, quit/reset and Continue.
   Confirm a safe position and unchanged party. Keep the original save backup.
10. Return to Olivine and interact with the rescued-starter case: no second grant.

Report location, entrance used, old-save/new-game status, movement direction and
screenshots. Owner visual acceptance is pending. Full-region polish, all starters,
whiteouts and all special movement states are not newly certified by this package.

## Verification

Fresh Emerald build PASS. Opening, Olivine, western Johto, landmark/area,
HGSS save-contract, visual-repair and whole-network structural validators PASS.
Built-ROM inclusion checks PASS. Controller traversal results are supplied in
TEST_RESULTS.txt in the package; compilation/connectivity do not prove visual QA.
