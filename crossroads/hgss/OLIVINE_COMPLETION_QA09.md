# Olivine QA09 — BUILD11 technical completion review

**All nine canonical enterable buildings, four preserved Black Ledger additions and 24 native maps are implemented, compiled and controller verified on the frozen BUILD11 ROM.** No known functional defect remains in the exercised scope. **Owner Delta visual acceptance is pending.** This is not a literal DS/GBA pixel-identity claim or completion of deferred voyages/story systems.

Game source: `489c404346f572aefb6856b3dd48a9b364a08ceb`

ROM SHA256: `df69e014e706168c56180828487a9ab12709a9bccd3dff063fee5f7af5d4f2f4`

The frozen ROM is 32 MiB; measured payload 30,261,028 bytes, with 3,293,404 bytes headroom. EWRAM 226,448 bytes; IWRAM 28,392 bytes. [CITIES_QA09.md](CITIES_QA09.md) records delivery instructions. Subsequent documentation commits do not change this game-source/binary identity.

The [detailed 24-map inventory](OLIVINE_COMPLETION_QA09.json) records stable IDs, references, doors, services, adaptations and exact proof.

## Per-building checklist

| Building | Reference and implemented content | Current BUILD11 verification | Scope limits / adaptations |
| --- | --- | --- | --- |
| Gym | Actual HGSS corridor/arena geometry and inspected Gym raster; approved custom Steel facade; Enterable corridor/arena, optional accepted Jasmine practice battle | Named interiors visited; applicable door/return/service/collision/save checks PASS; owner visual review pending | Permanent badges/progression/rewards deferred |
| Pokemon Center | Actual identical common HGSS matrices/raster and source prop inventory; Healing, PC, reception and17x14 basement with three booths/furniture | Named interiors visited; applicable door/return/service/collision/save checks PASS; owner visual review pending | DS communication functionality unsupported/offline; closed blue desk panels are not missing open doorways |
| Poke Mart | Actual common HGSS matrix/raster; fixtures retain source anchors; Native shop, stock and purchase flow; source shelves/table/seats/plants | Named interiors visited; applicable door/return/service/collision/save checks PASS; owner visual review pending | No new stock/progression decisions |
| Glitter Lighthouse | Actual six-floor/balcony source geometry and annotated raster; every maritime prop accounted; Six floors, intentional4F window/balcony branch, paired two-stop lift, preserved beacon | Named interiors visited; applicable door/return/service/collision/save checks PASS; owner visual review pending | No imported Jasmine/Ampharos plot; separate cabin full raster unavailable |
| Fishing house | Actual0097 shared house matrix and inspected house raster; Canonical furnished house and resident dialogue | Named interiors visited; applicable door/return/service/collision/save checks PASS; owner visual review pending | Old Rod reward not added during this no-new-rewards map pass |
| Trade house | Actual0097 shared house matrix and inspected house raster; Canonical furnished house and resident dialogue | Named interiors visited; applicable door/return/service/collision/save checks PASS; owner visual review pending | Source trade/rewards deferred; dialogue is not a functional trade claim |
| Seal house | Actual0097 shared house matrix and inspected house raster; Canonical furnished house and resident dialogue | Named interiors visited; applicable door/return/service/collision/save checks PASS; owner visual review pending | DS Seal Case/Seal feature unsupported and not claimed implemented |
| Cafe | Actual0136 matrix/raster; table, L-counter, windows and two plants; Furnished public cafe with actual counter dialogue/access | Named interiors visited; applicable door/return/service/collision/save checks PASS; owner visual review pending | One-cell staff aisle is a documented native safety adaptation |
| Port terminal | Actual terminal raster plus canonical quay prop/warp facts; reverse full-view limitation explicit; Furnished terminal, main/side leaves, quay, rear facade, docked ferry, boats and dry return | Named interiors visited; applicable door/return/service/collision/save checks PASS; owner visual review pending | S.S.Aqua voyages/ship interiors/other-region arrival outside authorized city pass |
| Joe Mercer residence | Preserved Black Ledger addition, no HGSS counterpart; Accepted residence/rest/interaction and reciprocal door | Named interiors visited; applicable door/return/service/collision/save checks PASS; owner visual review pending | Original location remains separate from canonical homes |
| Accepted neighbour residence | Preserved Black Ledger addition, no HGSS counterpart; Accepted furnished residence/dialogue and reciprocal door | Named interiors visited; applicable door/return/service/collision/save checks PASS; owner visual review pending | Original location remains separate from canonical homes |
| Silph subsidiary office | Preserved Black Ledger addition, no HGSS counterpart; Existing terminal, starter rescue/uniqueness/metadata and office interactions | Named interiors visited; applicable door/return/service/collision/save checks PASS; owner visual review pending | Main prologue/story remains outside this map pass |
| Harbor Office | Preserved Black Ledger addition, no HGSS counterpart; Accepted harbor/travel/dispatch interactions and reciprocal door | Named interiors visited; applicable door/return/service/collision/save checks PASS; owner visual review pending | Existing approved travel is separate from deferred S.S.Aqua voyages |

## Actual current-ROM verification

These are scripted controller-driven mGBA gameplay tests using copies of saves, separate from automated source checks and the owner’s Delta review. All seven serial suites completed with exit0; original and lane-copy batteries remained unchanged. Legacy-coordinate/HP/status fixtures, opt-in Survey assistance and temporary test encounter suppression are disclosed in their reports. No public evidence includes private saves or emulator snapshots.

- All 24 targets visited: 39 maps including approach/transit, 180 actual transitions, 53 round-trip pairs and 173 warp trials. Five native Survey Surf entries are disclosed separately from dry doorway trials. All 24 frames checked with zero FF00FF debug pixels; the native1x contact sheet was visually inspected.
- All 60 Olivine doorway fronts/segments passed; 168 accessible approach/arrival/walk-away trials passed. Twelve physically unavailable lateral starting positions are explicitly excluded. Across both cities: 118 segments, 329 passes, 25 unavailable laterals and zero failures.
- Ten lighthouse/port specials passed: both lift floors with both exit leaves, the complete4F window/balcony/south3F/western-stair return, both Port sea/overhang/body approaches, dry boardwalk return and both high-balcony no-Surf rails.
-51 service interactions passed, including all six actual front desks with exact text/LastTalked, real purchase/heal/PC/rest, office/harbor/cafe/landmark dialogue and Jasmine practice loss with safe local respawn.
-25 Save/coldContinue cases passed without resumes: all nine appended maps, split3F/6F, both actual panel-selected lift exits, Surf and four labelled immutable-V7 stool migrations. Party, boxes, inventory and flags remain intact. This is a representative matrix rather than an independent savepoint at every map.
-204 normal controller collision bumps passed across13 buildings/three tree cases with zero inaccessible skips. Forty Mart furnishing probes across both cities passed with zero skips. Six dedicated front-counter recording cases passed.
-59 city-material semantic checks passed:12 deck walks,43 fence bumps and four Surf boulder groups. Eighteen native movement clips cover these plus parasols/Port sea/dry return. Thirty-seven physically unavailable fence approaches are explicitly excluded; final dry return16,34 passed.
- Shared current-ROM regressions passed: all three actual starter rescues/met origin/level and duplicate guards; Joe walking/running/field-pose graphics; native Fly to ten destinations/cancel/saveContinue; Surf in four directions, bikes and rod casting/return. The doorway report discloses exact scope and fixtures.

Current evidence: [seven-suite completion](../qa/qa09/olivine/final-v11-lane/completed.json), [tour](../qa/qa09/olivine/final-v11-tour/results.json), [saves](../qa/qa09/olivine/final-v11-saves/results.json), [services](../qa/qa09/olivine/final-v11-services/results.json), [collision](../qa/qa09/olivine/final-v11-collision/results.json), [Mart props](../qa/qa09/olivine/final-v11-mart-props/results.json), [materials/native clips](../qa/qa09/olivine/final-v11-materials/results.json), [counters](../qa/qa09/olivine/final-v11-counters/results.json), [doorways/specials/player regressions](../qa/qa09/doorways/v11/results.json), [24-frame manifest](../qa/qa09/olivine-review/native-b11-manifest.json) and [1x contact sheet](../qa/qa09/olivine-review/native-b11-contact-sheet.png).

Final source/generator/topology/semantic/resource/save-ID checks and the real Emerald build passed. Engine palette bounds0–12 are preserved. Compilation/connectivity/probe counts alone do not establish visual quality. BUILD9 and V7 reports remain historical only; no earlier report is relabelled as current B11 evidence.
## Reference fidelity and deliberate adaptations

Canonical entrances, street geography, room matrices, props and permissions derive from pinned actual HGSS facts and inspected raster references. The three canonical homes share matrix0097, with kitchen, windows/bookcase/plant, table and chairs. Cafe0136 retains its checkered floor, cream windows/walls, two plants, communal table and L-counter; a visible native staff aisle prevents a trapped floor pocket. Pale-blue house and cream cafe walls replace the incorrect red-curtained timber motif.

The Center retains its own Olivine nurse/heal identity, warps and services. Its raised DS rear deck is flattened for GBA service systems; the reception emblem/rear panels are represented. The 17×14 private basement includes all three U-shaped communication booths, full waiting footer, ten stools, plants, glass table and terminal. Dedicated source-backed service art is used without changing generic rooms in other cities. Native Mart fixtures retain source placement and actual shop stock. The approved custom Steel Gym facade is a deliberate Black Ledger exception; its source corridor/arena span two stable native maps.

The lighthouse retains the source branched traversal, native two-stop lift and all eight source plants. Purple lantern-room flooring and a substantial original circular housing surround the preserved mechanical beacon actor. Flat masonry/rails represent DS perspective models. Balcony repeated windowed masonry and3×3 optical-housing compression are chosen art adaptations, not unavoidable hardware limits. Off-public lift machine208 is explicitly cropped rather than claimed as a rendered accessible room.

Port terminal furniture is supported by its actual raster: tan flooring, blue rug, white tables, all eight yellow stools, aqua seats and life rings. The quay has the rear terminal’s four door segments, docked ferry and both sailboats. Model placement derives from canonical source anchors; the cropped quay raster does not expose the complete reverse facade or both boats. Original GBA flat art and repeated hull panels replace DS polygons. Unused eastern ocean is cropped to 40×27 while preserving public paths.

Joe’s residence, the accepted neighbour home, Silph subsidiary and Harbor Office remain documented Black Ledger additions, not substitutes for canonical buildings. The accepted exterior/custom Gym designs are preserved. Corrected white fences, timber tables/deck, parasols, gray offshore rocks and65 restored sea cells have current BUILD11 controller proof; visible Port doors and dry return anchors remain independently operative.

The [reference/build gallery](../qa/qa09/olivine-review/comparisons.html) separates actual B11 native frames from static full-layout previews and historical BUILD9/V7 captures. The [42-instance prop inventory](olivine-landmark-prop-coverage.json) accounts for41 rendered/adapted models plus one explicit off-room crop. Zero unhandled prop records alone is not proof of visual approval.

Reference limits remain explicit: the lighthouse guide is an annotated900×668 composition rather than raw native DS frames; published house/common-room images have different scales. A full separate lift-cabin raster and complete reverse-quay view are unverified; their geometry comes from actual source facts. No fake pixel1:1 comparison or invented raster detail is claimed.

## Scope boundaries

S.S. Aqua sailing, ship interiors and other-region arrival are outside this two-city map pass; the ship is visible and its boarding boundary is safe and explicit. Accepted Harbor Office travel remains functional and separate. DS online communication, story progression, badges, trades/rewards and Seal Case events are deferred decisions, not silently invented content. These boundaries are distinct from missing city entrances or rooms; all intended city maps in this checklist are present.

## Delta review

1. Export/back up your normal save. Import the uniquely named BUILD11 ROM and a copy of its battery if Delta creates another game entry. Use normal Continue, never an older emulator save state.
2. Enter/exit every visible doorway leaf independently, try accessible lateral approaches and walk away after arrival. Visit all nine canonical buildings and four additions.
3. Check heal/PC, shop purchase, home, Silph office, Harbor Office, cafe and optional Gym practice. Check that the starter, party and inventory remain intact.
4. Walk the lighthouse stairs and4F window→balcony→south3F→western stairs route. Choose both elevator floors and both exit leaves. Walk the port’s front/side doors and dry boardwalk; verify sea/overhang movement blocks at the actual solid body.
5. Circle building bases, trees, fences and parasols; check correct canopy overlap and no arrows on ordinary ground. Compare the supplied native screenshots with your view.
6. Save, reset to title and Continue. Confirm location, starter, party, inventory and elevator selection. Report any incorrect collision, entrance, sprite or visual detail.

**Owner visual acceptance remains required.** Current BUILD11 technical/controller checks passed; final approval belongs to the project owner.
