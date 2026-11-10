# Black Ledger QA06 — eight owner Gyms and Violet reconstruction

Feature branch: feature/hgss-johto-gym-integration-01, based on QA05 commit526829f967.
The build artifact includes the exact source commit and ROM SHA256 in build-info.json.
This is a QA checkpoint; the rest of Johto is not finished.

Implemented: all eight supplied Gym exteriors, both door halves, private resource
packing; HGSS-reference Violet terrain/pond/bridges/door positions, school, houses,
Center/basement, Mart, fixed Gym access, three Sprout floors and two gatehouses.
Old saves/IDs, Joe, title/V5 music, starters, approved encounters and practice
battles are preserved. No new story, badge, team or encounter decisions are made.

See [Violet scope/deviations](hgss/VIOLET_QA06.md), [regional checklist](hgss/REGION_CHECKLIST.md)
and [topology](johto/TOPOLOGY.md). Compiling/connectivity do not establish visual
acceptance. Native screenshots, a bridge movement recording and actual test logs
are in qa/hgss-qa06 and the evidence download. Owner visual acceptance is pending.

## Delta on iPhone

1. Export/back up your battery save. Import the QA06 .gba, import a COPY of the
   save if Delta creates a separate game entry, and use normal Continue. Check
   Joe, starter, party, boxes, money and progress. Avoid an older save state.
2. Fly to Violet, cancel Fly once, then land again. Walk between Mart, Gym, school,
   both houses and Center. Inspect buildings/trees from all sides. Enter/exit
   each door, including both panels of the Gym and school.
3. Walk across both pond bridges to Sprout Tower and return WITHOUT Surf. Explore
   all three floors and every stair branch in both directions. Check the central
   pillar, railings and wall collisions; no unseen final story event is expected.
4. Walk west through the gate to Route36 and back; east through its gate to
   Route31 and back; south across the scrolling Route32 boundary and return.
   Check camera edges and seam graphics. These surrounding routes still need
   their full HGSS terrain/art reconstruction.
5. Heal in Violet, use its PC/Mart, enter/exit the basement, rest at the house,
   save/reset/Continue indoors and outdoors. If using survey Surf, opt in again
   after resetting; verify Joe on water and after disembarking. Save on water
   and reload normally. Report any old-save arrival that is blocked or stranded.
6. Visit all eight new Gyms. Test both visible doorway halves, walking behind
   intentional high roof edges and against the solid facade. Current optional
   Jasmine/Morty battles remain; other Gym battle/badge progression is pending.
7. Revisit Ecruteak's accepted streets, Theater, gates, Bell/Burned floors and
   Olivine's office starter case/terminal/home/harbor. Confirm starter uniqueness,
   encounters and previously accepted interactions. Check Joe during Fly/Surf.

Please report location, doorway/side and direction for any clipping. Most Johto
outside Ecruteak/Violet remains the older exploration draft; new Gym art does not
make its surrounding city or interiors fully reconstructed.
