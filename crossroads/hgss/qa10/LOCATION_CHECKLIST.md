# QA10 — location-by-location changes, references and remaining work

**Draft verification state: final delivery-byte gameplay is still pending.**
Source implementations and actual references below exist. Current controller
verification is in progress; interrupted diagnostic builds and QA09 passes are
not relabelled as final QA10 passes. The coordinator must fill the final source
revision, ROM checksum and evidence links after the last frozen candidate passes.
Owner Delta/visual acceptance remains **PENDING** for every location.

Current frozen candidate B3: source `e7e2c085a5a61ef727d06f9f682af7d3a954cc06`;
ROM SHA256 `af59dff1b06b99a9599c6f98b6fb6bd1e765cc52c0838a2dec5c79a6c1f88373`.
These identify the active tests, not a final pass or owner acceptance.

Baseline: source `285cfa4ebddcb390a8a5bde6116748cbb5eaba6b`, delivered ROM SHA256
`df69e014e706168c56180828487a9ab12709a9bccd3dff063fee5f7af5d4f2f4`.
[Actual BEFORE captures](../../qa/qa10/before/manifest.json) use those identified
bytes. Owner photographs visually match the baseline layouts; photographs alone
do not establish a cryptographic hash of the owner's Delta ROM.

## Photograph identification and the signed court

| Location | Finding and implemented correction | Reference / deliberate adaptation | Final gameplay evidence |
| --- | --- | --- | --- |
| Ecruteak directory court, sign(36,45), photos1–2 | This is the vacant court **west of the Dance Theater**, not an Olivine building lot.39 soil/curb drawing cells replace the old featureless gray surface. Sign, movement and surrounding buildings remain. No building was invented. | Actual HGSS Ecruteak city mosaic and075_T27 background event place the sign here with no door/building. The real house at23,45 is a separate enterable plot. Original16px soil/curb artwork adapts the source surface. | Exact BEFORE court/sign/residence contrast captured. AFTER movement/sign and unchanged approaches PENDING. |
| Ecruteak Center exterior, photo10 | Existing red Poké Ball facade and services preserved; it is not the Mart. | Accepted existing facade; no unrelated reconstruction introduced in this pass. | Regression doors/arrival/healing/Continue PENDING. |

The earlier Olivine directory(24,42) and Route40 Frontier-gate hypotheses are
superseded as identifications of photos1–2. Olivine's terrace directory is also
canonical. Route40 separately lacks its source Frontier gatehouse, but that is
an adjacent future-area gap, not the photographed court or a new city building.

## Olivine city and its thirteen building destinations

All nine canonical HGSS enterable city destinations exist alongside four
intentional Black Ledger additions. This inventory establishes presence and
scope, **not visual approval**. No canonical house was silently replaced by Joe's
home or an office. Source door coordinates are retained unless an explicitly
named existing alias is involved.

| Location / city door | Changes or preserved content | Reference / limits | Final gameplay evidence |
| --- | --- | --- | --- |
| City streets/waterfront | Canonical relative layout and accepted buildings retained. Direct northern passenger pier replaces the port's former forced east U-turn. Only the named82-cell port physical/elevation mask changes; other city physical cells stay pinned. | Actual HGSS city mosaic and world permissions/events; flatGBA facade/terrain projection. Not a claim that every city texture is pixel-identical. | All signs, walking/Surf, facade boundaries, local connections and return journeys PENDING. |
| Gym —13/14,14 | Owner Steel Gym design and two-map hall/arena retained. Optional accepted Jasmine practice battle remains. | HGSS hall/arena geometry; custom facade is an approved Black Ledger exception. Badges/story gates remain deferred. | Both doorway leaves, hall/arena returns, practice loss/local healing PENDING. |
| Pokémon Center —16/17,33 | Reception, PC, healing, furniture and full14-row basement retained. | Actual common HGSS service matrices/raster. Raised DS rear deck is flattened; DS online functions are offline, not claimed implemented. | Both leaves, stairs, all service fronts, PC/party/box integrity and Save/Continue PENDING. |
| Poké Mart —29,33 | Source-backed shelves, plants, glass display/stools and normal shop retained. No new stock/progression rule. | Actual common HGSS matrix/raster; native art projection. | Door, purchase/currency, furniture collision and Save/Continue PENDING. |
| Northwestern fishing house —17,23 | Canonical furnished0097 home/resident retained. | Actual house matrix/raster. Rod reward was not silently added during this map pass. | Entry/return, furnishings and resident interaction PENDING. |
| Northern trade house —31,17 | Canonical furnished0097 home/resident retained. | Actual house matrix/raster. A functional species trade/reward has not been implemented. | Entry/return, furnishings and resident interaction PENDING. |
| Northeastern Seal house —36,17 | Canonical furnished0097 family home retained. | Actual house matrix/raster. DS Seal Case/Seal system is unsupported, not passed off as a working service. | Entry/return, furnishings and family interaction PENDING. |
| Cafe —9,33, photo5 street | Source0136 room, communal table, L-counter, kitchen, windows/plants and ambient people retained. | Actual HGSS cafe imagery. One native staff aisle is a documented clearance adaptation. | Door, actual front-counter conversation, NPC clearances and return PENDING. |
| Lighthouse —45,39, photo4 interior | Existing exterior preserved; six floors and balcony receive the visual corrections listed below. Lift/branch geometry remains. | Seven newly recovered individual HGSS floor/balcony map references; native art rather than copied textures. | Every floor/branch/lift/door/service and old-save return PENDING. |
| Port terminal —23/24,52, photos6–9 | North-entry facade, direct pier, logical terminal flow, paired gangway and a real docked ship replace the former awkward detour/closed boarding scenery. | Actual HGSS city/terminal/quay facts and images; see maritime rows below. | Every front/reverse/side leaf, arrival/facing, walking away, signs and boarding/disembarking PENDING. |
| Joe's residence —8,23 | Accepted original facade, furnished room, rest and Alpha bridge preserved. | Intentional Black Ledger addition; not a substitute for a canonical home. | Door/rest/travel, party/starter and Save/Continue regression PENDING. |
| Neighbour residence —8,28 | Accepted original room/facade preserved. | Intentional Black Ledger addition. | Door/NPC/furniture/return regression PENDING. |
| Silph subsidiary —31,40 | Accepted office, terminal, starter case and existing story state preserved. No new plot event. | Intentional Black Ledger addition. Starter variable, one-choice grant and new-Pokémon met origin remain stable; old Pokémon are not rewritten. | Terminal, all3 rescue choices, met location, duplicates, battle and persistence PENDING. |
| Harbor Office —8,40 | Accepted dispatch/Survey/Alpha travel preserved separately from passenger sailings. | Intentional Black Ledger addition. Session Survey access does not grant permanent story/badge progress. | Office/NPC/sign, actual Survey toggle/travel, return and persistence PENDING. |

## Lighthouse: seven visually changed maps plus retained lift

All seven existing map/layout identities, dimensions, events, actors, warps and
physical/behavior/layer values are preserved. New original private drawing
references replace missing or incorrect motifs; preserved geometry does not make
this a literal DS rendering. [Detailed visual audit](LIGHTHOUSE_VISUAL_REFERENCE_QA10.md)
and [actual raster provenance](lighthouse-reference-manifest.json) separate
references, native adaptations and source/static checks.
The [HGSS versus historical native BEFORE gallery](../../qa/qa10/reference-comparisons/index.html)
uses original QA09 df69 frames, explicitly labelled historical; final QA10 AFTER
frames still require the coordinator's actual gameplay capture.

| Native location | Actual corrected surfaces/furnishings | Deliberate GBA adaptation | Final gameplay evidence |
| --- | --- | --- | --- |
| `OlivineCity_Lighthouse_1F` | Pale diamond surround, teal inset/double burgundy border, four brown table/eight orange-seat groups, preserved six ferns, pale window panels, red stair and paired red lift. | Combined table/two-seat motifs fit the original one-column/two-row solid groups instead of adding invisible furniture collision. | Entry/exit/stairs/both lift leaves, every table/plant approach, layering and visitor/beacon route PENDING. |
| `OlivineCity_Lighthouse_2F` | Pale surround and teal U runner/burgundy edge, both existing ferns, red lower stairs and upper ladder. | Pattern fits the existing native coordinate footprint; source height is flattened. | Both stairs, both upper-mouth rows, plants/runner clearances and returns PENDING. |
| `OlivineCity_Lighthouse_3F` | Weathered green boards/cracks, pale arched-window/perimeter panels, gold edge and retained gray internal barrier. | Source curved masonry becomes stepped16px native panels. | Both public components, all mouths and balcony return PENDING. |
| `OlivineCity_Lighthouse_4F` | Matching boards/windows/trim; existing east window drop remains. | Existing branch/height geometry retained rather than replacing traversal with a teleport. | Both staircase branches and actual window drop PENDING. |
| `OlivineCity_Lighthouse_5F` | Matching boards/windows/trim; original ladder/hatch geometry retained. | Native flat floor projection. | Every stair/hatch leaf, collision and return PENDING. |
| `OlivineCity_Lighthouse_6F` | Pink square tiles, cyan optical housing, **outer** glass/white framing and red lift doors. ActualB3 review found26 inner-body cells incorrectly using glass plus2 black model corners; the named28-cell B4 art fix is prepared, not yet gameplay verified. | Existing3×3 northern cap/overlap, larger physical enclosure and mechanical beacon actor retained; inner optical body stays cyan, outer room ring stays glass. No imported Ampharos/Jasmine story. | Beacon/NPC, housing layering, ladder, both lift leaves and Save/Continue PENDING. |
| `OlivineCity_Lighthouse_Balcony` | Gray-purple shell, one east window, diagonal paving, blue parapets and paired dark tower mouth. | Existing17×17 shell/high walkway; curve/height compressed into native panels. Sea remains below solid safety rails. | Window arrival, both doorway leaves, entire rail/boundary and normal return PENDING. |
| `OlivineCity_Lighthouse_Elevator` | Existing two-stop cabin/panels and paired dynamic exits retained. | Uses native dynamic-warp state; no new save structure or progression flags. | Both selected floors × both exit leaves, destination/facing, cold Continue PENDING. |

The old uniform floor and generic furniture were genuine omissions even when
all props and connections counted correctly. Old shader/art references were
also corrected to follow freshly packed primary glyph slots, preventing fern
corruption. Shared Port/Ecruteak/Temple resources are not overwritten by these
private lighthouse changes.

## Port terminal, quay and the docked S.S. Aqua

| Location | Before / current implementation | Reference / adaptation | Final gameplay evidence |
| --- | --- | --- | --- |
| City-facing terminal exterior | Former south-facing door required an east U-turn despite a north terminal exit. New blue-vault north portal keeps the existing city warp indices13/15 at23/24,52, with fronts/returns at23/24,51. Sign moves from inside new body22,53 to visible apron22,50. | Actual canonical terminal approach, accepted GBA palette/style. New rear body is solid; no fake second south exit is painted. | Each leaf from front/available sides, exact facing/arrivals, dry departure, body/sea/roof layering and sign PENDING. |
| `OlivineCity_PortTerminal` | Existing furnished tan-plank waiting room: blue rug, two tables/eight stools, aqua benches/life rings, desk and visitors. Its two north city exits, two south main-quay leaves and two western side-quay leaves connect to their actual visible mouths. It is a terminal, not a mislabeled ship room. | HGSS terminal raster/props; native furniture/projection. Reusing old south-facing city pixels for the reverse facade is explicitly separated from the new city-front art. | All6 leaves independently, NPC/desk/sign, furniture/camera clearance, arrival/facing and return PENDING. |
| `OlivineCity_PortQuay` | Existing ferry/sailboats/bollards and four terminal returns retained. Two actual ship hatch leaves at27/28,20 append new warp ordinals4/5. The old solid gangway now boards real ship maps. | Source quay/gangway/model anchors. Five source interior gangway cells project to two external leaves; the old four terminal ordinals remain stable. | Main/side terminal leaves, both hatch leaves, walking away/return, ship body/sea/overhang, boarding notice and signs PENDING. |
| `SSAqua_1F` —57×21, **2 components** | New orange/gold hall with four vertical benches plus two horizontal settees, portholes/life rings/plants, eight two-leaf cabin mouths, two B1F stairways and east captain passage. All5 interior gangway cells22–26,19 return to Olivine. | Actual full HGSS hall mosaic/permissions. East/west components connect through B1F; no wall is opened to fake a one-room graph. No Vermilion warp competes at the docked exit. | Every visible hatch/stair/gangway cell, exact facing/arrival, furniture, NPCs/signs and each component's return PENDING. |
| `SSAqua_CaptainRoom` —14×13, **1 component** | New chart desk/rug, berth, sofa, bookcase, kitchenette/fridge and framed charts/windows; neutral captain interaction. | Actual full captain mosaic and prop anchors; ship-context bookcase replaces an inappropriate temple-pillar assumption. No plate gifts or captain quest. | Both door leaves, chart/NPC, furniture and return PENDING. |
| `SSAqua_SoutheastCabins` —28×13, **2 components** | Left red crew cabin with horizontal twin berths and rear TV/kitchen. Right mustard rest cabin with berth, four-stool table and rear fittings. | Actual lower-right cabin mosaic/source origin. Ordinary party rest is separate from HGSS voyage/sleep arrival state. | Each cabin independently, both leaves, rest/healing without travel-state change, collision/NPC and returns PENDING. |
| `SSAqua_SouthwestCabins` —28×13, **2 components** | Left blue berth/dining cabin; right gold dining/bookcase cabin. | Actual lower-left mosaic, with distinct carpets/furniture rather than identical empty rooms. | Each cabin independently, both leaves, furniture/NPC and returns PENDING. |
| `SSAqua_NortheastCabins` —28×13, **2 components** | Left red cabin with two vertically arranged beds/rear desks; right mustard berth/four-stool dining cabin. | Actual upper-right mosaic. Embedded terrain furniture is drawn even where separate source prop count is sparse. | Each cabin independently, both leaves, furniture/NPC and returns PENDING. |
| `SSAqua_NorthwestCabins` —28×13, **2 components** | Left blue berth/table cabin with **two diagonal red stools**; right gold twin-berth/yellow-sofa cabin. | Actual upper-left mosaic. Reference grandfather/missing-child plot is not imported. | Each cabin independently, both leaves, furniture/NPC and returns PENDING. |
| `SSAqua_B1F` —57×21, **1 component** | New six-bed crew dormitory/lockers, galley with one3×5 table/six chairs, kitchenette/fridge, engine/hazard bay, western alcove and connecting corridors. | Actual full lower-deck mosaic. Exact native model-base solids and wider door/stair landings are named in the independent source contract; DS model collision is not inferred from floor permissions alone. | Both stair mouths and all aliases, every dorm/galley/engine route, furniture/body/foreground collision, NPCs and return PENDING. |

The seven new ship maps have **12 physical components and8 separate cabins**.
No cabin pair is joined through its wall. New identities append to existing
map/layout/group prefixes; old identities and save format remain stable.
[Ship implementation details](SS_AQUA_IMPLEMENTATION.md),
[exact source/model/door projection review](ss-aqua-build-review.json) and
[visible doorway/facing contract](ss-aqua-doorways.json) record the deliberate
native adaptations.55 new visible ship threshold segments extend the legacy
118-segment audit; counts alone do not prove successful gameplay or appearance.

## Sailing, missing destinations and story boundaries

QA09's non-operating-sailings message hid no dormant voyage or ship room. The
ship was scenery with an intentionally solid boundary. Physical dockside boarding
is now implemented; passenger voyages remain a separate unfinished system.

Actual HGSS travel requires game-clear/Ticket state, Olivine/Vermilion destination
maps, boat direction/arrival/scene state, first-trip sleeping-sailor/missing-child
progression and later weekday/sleep rules. None is automatically Black Ledger
canon. Source Metal Coat and badge/daily captain plate gifts are not imported.
Black Ledger still lacks the approved destination/region, travel/ticket/fare/
schedule policy and story unlock. Removing a notice must not fabricate these.

The docked implementation returns to Olivine and explains that sailing is not
available. Accepted Harbor Office/Survey/Alpha transport remains separate. It
must not claim the ferry sails, arrive at a generic room or silently teleport to
another city. No new main story, badge order, encounters, trainers or rewards are
introduced to make the port appear complete.

## Final verification and limitations ledger

| Verification category | Actual current state / result to fill |
| --- | --- |
| BEFORE owner-scene matching | Completed on identified QA09 bytes; native signs, closed gangway, terminal leaves, court and residence contrast are archived. |
| New source/generator/reference checks | Implementations and independent contracts exist; final exact-source command results must be linked by coordinator. No weakening of generic assertions or missing-map exemptions is presumed. |
| Emerald build / memory | Coordinator must record the final source, actual build exit, ROM checksum, payload/RAM and generated map inclusion. Prior diagnostic builds are not final delivery. |
| Normal controller movement | **PENDING final-ROM results**: every door segment/direction, lateral approach where physically available, destination/arrival/facing and post-arrival walk-away. |
| Collision / layering | **PENDING final-ROM results**: land and actual Surf approaches, all new terminal rear body cells, trees, canopies, hull/water, all ship furnishings, lighthouse foreground and balcony rails. Physically unavailable approaches must be reported rather than called passes. |
| NPCs / services / story preservation | **PENDING final-ROM results**: crew/chart/rest, signs, existing heal/PC/Mart/practice battles, Silph interactions, all3 starters/met/uniqueness, title/music/Joe/Fly/Surf/run and approved encounter preservation. No new major story event is claimed. |
| Normal Save / cold Continue | **PENDING final-ROM results** on copied saves, including genuine old walking/Surf positions around the reoriented port, safe arrivals, all12 ship components and accepted party/box/bag/flags. Original batteries must remain unchanged; screenshots/old cross-ROM states are not save-compatibility evidence. |
| Native visual proof | Final240×160 BEFORE/AFTER screenshots and normal-input movement clips must be linked; complete authored layouts are separately labelled static, without simulated gameplay. |
| Owner Delta / visual acceptance | **PENDING**. No city100% claim, pixel-identical HGSS claim or automatic acceptance from compilation/traversal. |

Remaining limits are explicit: actual passenger voyages/destination/unapproved
story/rewards; DS online/Seal functions and deferred source trades/rod gifts;
projection/native furniture/sizing choices listed above; and owner visual approval.
A full reverse-quay facade raster is less complete than the now-recovered whole
ship/lighthouse maps. The newest private owner save was not supplied; only copied
historical/genuine before-build saves and disclosed compatibility fixtures can be
reported tested. Other Johto areas and the adjacent Route40 Frontier gate are not
silently included in this pass.
