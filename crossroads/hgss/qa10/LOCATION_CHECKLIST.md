# QA10 — location-by-location changes, references and remaining work

**B5 software verification complete; owner Delta/visual acceptance PENDING.**
Game checkpoint `cc643ffe711204f3ef38e34e7aa1eb8c9558720f`;
ROM `ee2d81d5d0b55b7f1f9d36d1c9b055700164da439f51af7a66b5fb2d2147f90b`.
All 68 checks, fresh emulator suites and independent all-45 facing audit passed.
Raw reports keep their real source identities; ed375e9f is a generator/documentation
successor with unchanged game inputs. B3/B4 results remain historical, including
B4's 67 facing failures. This checklist does not certify either city100% complete.
[Exact scope/results](../../qa/qa10/verification-summary.json),
[native comparisons/recordings](../../qa/qa10/index.html).

Baseline: source `285cfa4ebddcb390a8a5bde6116748cbb5eaba6b`, delivered ROM SHA256
`df69e014e706168c56180828487a9ab12709a9bccd3dff063fee5f7af5d4f2f4`.
[Actual BEFORE captures](../../qa/qa10/before/manifest.json) use those identified
bytes. Owner photographs visually match the baseline layouts; photographs alone
do not establish a cryptographic hash of the owner's Delta ROM.

## Photograph identification and the signed court

| Location | Finding and implemented correction | Reference / deliberate adaptation | Final gameplay evidence |
| --- | --- | --- | --- |
| Ecruteak directory court, sign(36,45), photos1–2 | This is the vacant court **west of the Dance Theater**, not an Olivine building lot.39 soil/curb drawing cells replace the old featureless gray surface. Sign, movement and surrounding buildings remain. No building was invented. | Actual HGSS Ecruteak city mosaic and075_T27 background event place the sign here with no door/building. The real house at23,45 is a separate enterable plot. Original16px soil/curb artwork adapts the source surface. | B5 PASS:39 ordinary cells/full Joe, four directory messages, normal Save/cold Continue. [Court proof](../../qa/qa10/final/B5/city/ecruteak-court/results.json). |
| Ecruteak Center exterior, photo10 | Existing red Poké Ball facade and services preserved; it is not the Mart. | Accepted existing facade; no unrelated reconstruction introduced in this pass. | B5 doorway/facing/return and reception-counter checks PASS. Existing room/services preserved; this is not a fresh exhaustive Ecruteak-service audit. [Door inventory](../../qa/qa10/final/B5/doorways/README.md). |

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
| City streets/waterfront | Canonical relative layout and accepted buildings retained. Direct northern passenger pier replaces the port's former forced east U-turn. Only the named82-cell port physical/elevation mask changes; other city physical cells stay pinned. | Actual HGSS city mosaic and world permissions/events; flatGBA facade/terrain projection. Not a claim that every city texture is pixel-identical. | B5 PASS:13 building/3 tree cases,199 dry+24 actual Surf bumps and59 materials cases; strict doors/return paths. [City proof](../../qa/qa10/final/B5/city/results.json). |
| Gym —13/14,14 | Owner Steel Gym design and two-map hall/arena retained. Optional accepted Jasmine practice battle remains. | HGSS hall/arena geometry; custom facade is an approved Black Ledger exception. Badges/story gates remain deferred. | B5 PASS:full-width doorway/facing/return plus the named NPC/service regression cases. Furnishings preserved; visual inspection covers documented native viewports. [Doors](../../qa/qa10/final/B5/doorways/README.md), [services](../../qa/qa10/final/B5/regressions/results.json). |
| Pokémon Center —16/17,33 | Reception, PC, healing, furniture and full14-row basement retained. | Actual common HGSS service matrices/raster. Raised DS rear deck is flattened; DS online functions are offline, not claimed implemented. | B5 PASS:full-width doorway/facing/return plus the named NPC/service regression cases. Furnishings preserved; visual inspection covers documented native viewports. [Doors](../../qa/qa10/final/B5/doorways/README.md), [services](../../qa/qa10/final/B5/regressions/results.json). |
| Poké Mart —29,33 | Source-backed shelves, plants, glass display/stools and normal shop retained. No new stock/progression rule. | Actual common HGSS matrix/raster; native art projection. | B5 PASS:full-width doorway/facing/return plus the named NPC/service regression cases. Furnishings preserved; visual inspection covers documented native viewports. [Doors](../../qa/qa10/final/B5/doorways/README.md), [services](../../qa/qa10/final/B5/regressions/results.json). |
| Northwestern fishing house —17,23 | Canonical furnished0097 home/resident retained. | Actual house matrix/raster. Rod reward was not silently added during this map pass. | B5 PASS:full-width doorway/facing/return plus the named NPC/service regression cases. Furnishings preserved; visual inspection covers documented native viewports. [Doors](../../qa/qa10/final/B5/doorways/README.md), [services](../../qa/qa10/final/B5/regressions/results.json). |
| Northern trade house —31,17 | Canonical furnished0097 home/resident retained. | Actual house matrix/raster. A functional species trade/reward has not been implemented. | B5 PASS:full-width doorway/facing/return plus the named NPC/service regression cases. Furnishings preserved; visual inspection covers documented native viewports. [Doors](../../qa/qa10/final/B5/doorways/README.md), [services](../../qa/qa10/final/B5/regressions/results.json). |
| Northeastern Seal house —36,17 | Canonical furnished0097 family home retained. | Actual house matrix/raster. DS Seal Case/Seal system is unsupported, not passed off as a working service. | B5 PASS:full-width doorway/facing/return plus the named NPC/service regression cases. Furnishings preserved; visual inspection covers documented native viewports. [Doors](../../qa/qa10/final/B5/doorways/README.md), [services](../../qa/qa10/final/B5/regressions/results.json). |
| Cafe —9,33, photo5 street | Source0136 room, communal table, L-counter, kitchen, windows/plants and ambient people retained. | Actual HGSS cafe imagery. One native staff aisle is a documented clearance adaptation. | B5 PASS:full-width doorway/facing/return plus the named NPC/service regression cases. Furnishings preserved; visual inspection covers documented native viewports. [Doors](../../qa/qa10/final/B5/doorways/README.md), [services](../../qa/qa10/final/B5/regressions/results.json). |
| Lighthouse —45,39, photo4 interior | Existing exterior preserved; six floors and balcony receive the visual corrections listed below. Lift/branch geometry remains. | Seven newly recovered individual HGSS floor/balcony map references; native art rather than copied textures. | B5 PASS:floor/branch/door/stair visits, selected clearances and normal Save/Continue. All source physical/layer contracts preserved; every furnishing edge was not individually bumped. [Details](../../qa/qa10/final/B5/city/lighthouse-details/results.json); [native view limits](../../qa/qa10/final/B5/city/LIGHTHOUSE_VISUAL_REVIEW.md). |
| Port terminal —23/24,52, photos6–9 | North-entry facade, direct pier, logical terminal flow, paired gangway and a real docked ship replace the former awkward detour/closed boarding scenery. | Actual HGSS city/terminal/quay facts and images; see maritime rows below. | B5 PASS:all visible segments/fronts/accessible laterals, exact arrivals/facing/walk-away, native services/signs and boarding/returns. Port body/sea/overhang tests PASS. [Doors](../../qa/qa10/final/B5/doorways/README.md); [city](../../qa/qa10/final/B5/city/results.json). |
| Joe's residence —8,23 | Accepted original facade, furnished room, rest and Alpha bridge preserved. | Intentional Black Ledger addition; not a substitute for a canonical home. | B5 PASS:full-width doorway/facing/return plus the named NPC/service regression cases. Furnishings preserved; visual inspection covers documented native viewports. [Doors](../../qa/qa10/final/B5/doorways/README.md), [services](../../qa/qa10/final/B5/regressions/results.json). |
| Neighbour residence —8,28 | Accepted original room/facade preserved. | Intentional Black Ledger addition. | B5 PASS:full-width doorway/facing/return plus the named NPC/service regression cases. Furnishings preserved; visual inspection covers documented native viewports. [Doors](../../qa/qa10/final/B5/doorways/README.md), [services](../../qa/qa10/final/B5/regressions/results.json). |
| Silph subsidiary —31,40 | Accepted office, terminal, starter case and existing story state preserved. No new plot event. | Intentional Black Ledger addition. Starter variable, one-choice grant and new-Pokémon met origin remain stable; old Pokémon are not rewritten. | B5 PASS:full-width doorway/facing/return plus the named NPC/service regression cases. Furnishings preserved; visual inspection covers documented native viewports. [Doors](../../qa/qa10/final/B5/doorways/README.md), [services](../../qa/qa10/final/B5/regressions/results.json). |
| Harbor Office —8,40 | Accepted dispatch/Survey/Alpha travel preserved separately from passenger sailings. | Intentional Black Ledger addition. Session Survey access does not grant permanent story/badge progress. | B5 PASS:full-width doorway/facing/return plus the named NPC/service regression cases. Furnishings preserved; visual inspection covers documented native viewports. [Doors](../../qa/qa10/final/B5/doorways/README.md), [services](../../qa/qa10/final/B5/regressions/results.json). |

## Lighthouse: seven visually changed maps plus retained lift

All seven existing map/layout identities, dimensions, events, actors, warps and
physical/behavior/layer values are preserved. New original private drawing
references replace missing or incorrect motifs; preserved geometry does not make
this a literal DS rendering. [Detailed visual audit](LIGHTHOUSE_VISUAL_REFERENCE_QA10.md)
and [actual raster provenance](lighthouse-reference-manifest.json) separate
references, native adaptations and source/static checks.
The [HGSS versus historical native BEFORE gallery](../../qa/qa10/reference-comparisons/index.html)
uses original QA09 df69 frames, explicitly labelled historical; final QA10 AFTER
frames are paired in the final gallery and city comparisons.

| Native location | Actual corrected surfaces/furnishings | Deliberate GBA adaptation | Final gameplay evidence |
| --- | --- | --- | --- |
| `OlivineCity_Lighthouse_1F` | Pale diamond surround, teal inset/double burgundy border, four brown table/eight orange-seat groups, preserved six ferns, pale window panels, red stair and paired red lift. | Combined table/two-seat motifs fit the original one-column/two-row solid groups instead of adding invisible furniture collision. | B5 PASS:floor/branch/door/stair visits, selected clearances and normal Save/Continue. All source physical/layer contracts preserved; every furnishing edge was not individually bumped. [Details](../../qa/qa10/final/B5/city/lighthouse-details/results.json); [native view limits](../../qa/qa10/final/B5/city/LIGHTHOUSE_VISUAL_REVIEW.md). |
| `OlivineCity_Lighthouse_2F` | Pale surround and teal U runner/burgundy edge, both existing ferns, red lower stairs and upper ladder. | Pattern fits the existing native coordinate footprint; source height is flattened. | B5 PASS:floor/branch/door/stair visits, selected clearances and normal Save/Continue. All source physical/layer contracts preserved; every furnishing edge was not individually bumped. [Details](../../qa/qa10/final/B5/city/lighthouse-details/results.json); [native view limits](../../qa/qa10/final/B5/city/LIGHTHOUSE_VISUAL_REVIEW.md). |
| `OlivineCity_Lighthouse_3F` | Weathered green boards/cracks, pale arched-window/perimeter panels, gold edge and retained gray internal barrier. | Source curved masonry becomes stepped16px native panels. | B5 PASS:floor/branch/door/stair visits, selected clearances and normal Save/Continue. All source physical/layer contracts preserved; every furnishing edge was not individually bumped. [Details](../../qa/qa10/final/B5/city/lighthouse-details/results.json); [native view limits](../../qa/qa10/final/B5/city/LIGHTHOUSE_VISUAL_REVIEW.md). |
| `OlivineCity_Lighthouse_4F` | Matching boards/windows/trim; existing east window drop remains. | Existing branch/height geometry retained rather than replacing traversal with a teleport. | B5 PASS:floor/branch/door/stair visits, selected clearances and normal Save/Continue. All source physical/layer contracts preserved; every furnishing edge was not individually bumped. [Details](../../qa/qa10/final/B5/city/lighthouse-details/results.json); [native view limits](../../qa/qa10/final/B5/city/LIGHTHOUSE_VISUAL_REVIEW.md). |
| `OlivineCity_Lighthouse_5F` | Matching boards/windows/trim; original ladder/hatch geometry retained. | Native flat floor projection. | B5 PASS:floor/branch/door/stair visits, selected clearances and normal Save/Continue. All source physical/layer contracts preserved; every furnishing edge was not individually bumped. [Details](../../qa/qa10/final/B5/city/lighthouse-details/results.json); [native view limits](../../qa/qa10/final/B5/city/LIGHTHOUSE_VISUAL_REVIEW.md). |
| `OlivineCity_Lighthouse_6F` | Pink square tiles, cyan optical housing, **outer** glass/white framing and red lift doors. ActualB3 review found26 inner-body cells incorrectly using glass plus2 black model corners; the named28-cell correction is delivered and freshly inspected/played on B5. | Existing3×3 northern cap/overlap, larger physical enclosure and mechanical beacon actor retained; inner optical body stays cyan, outer room ring stays glass. No imported Ampharos/Jasmine story. | B5 PASS:clockwise/reverse continuous circuit, stairs/lift, normal Save/Continue and native-frame review. [Details](../../qa/qa10/final/B5/city/lighthouse-details/results.json); [visual scope](../../qa/qa10/final/B5/city/LIGHTHOUSE_VISUAL_REVIEW.md). |
| `OlivineCity_Lighthouse_Balcony` | Gray-purple shell, one east window, diagonal paving, blue parapets and paired dark tower mouth. | Existing17×17 shell/high walkway; curve/height compressed into native panels. Sea remains below solid safety rails. | B5 PASS:window arrival, both threshold leaves, normal return and Save/Continue. Rail physics/behaviors preserved by source+built checks; not every rail edge was pushed in B5. [Details](../../qa/qa10/final/B5/city/lighthouse-details/results.json). |
| `OlivineCity_Lighthouse_Elevator` | Existing two-stop cabin/panels and paired dynamic exits retained. | Uses native dynamic-warp state; no new save structure/flags. Actual HGSS has a separate cabin with automatic opposite-floor riding; the preserved GBA two-panel chooser is a deliberate functional adaptation. Cabin decor is original GBA art and remains unverified against an actual HGSS cabin raster; see [focused follow-up](LIGHTHOUSE_ELEVATOR_REFERENCE_QA10.md). | B5 PASS:both selected floors ×both leaves, exact arrivals/facing, retained selections on normal Continue. [Details](../../qa/qa10/final/B5/city/lighthouse-details/results.json). Original cabin art is not raster-verified. |

The old uniform floor and generic furniture were genuine omissions even when
all props and connections counted correctly. Old shader/art references were
also corrected to follow freshly packed primary glyph slots, preventing fern
corruption. Shared Port/Ecruteak/Temple resources are not overwritten by these
private lighthouse changes.

## Port terminal, quay and the docked S.S. Aqua

| Location | Before / current implementation | Reference / adaptation | Final gameplay evidence |
| --- | --- | --- | --- |
| City-facing terminal exterior | Former south-facing door required an east U-turn despite a north terminal exit. New blue-vault north portal keeps the existing city warp indices13/15 at23/24,52, with fronts/returns at23/24,51. Sign moves from inside new body22,53 to visible apron22,50. | Actual canonical terminal approach, accepted GBA palette/style. New rear body is solid; no fake second south exit is painted. | B5 PASS:all visible segments/fronts/accessible laterals, exact arrivals/facing/walk-away, native services/signs and boarding/returns. Port body/sea/overhang tests PASS. [Doors](../../qa/qa10/final/B5/doorways/README.md); [city](../../qa/qa10/final/B5/city/results.json). |
| `OlivineCity_PortTerminal` | Existing furnished tan-plank waiting room: blue rug, two tables/eight stools, aqua benches/life rings, desk and visitors. Its two north city exits, two south main-quay leaves and two western side-quay leaves connect to their actual visible mouths. It is a terminal, not a mislabeled ship room. | HGSS terminal raster/props; native furniture/projection. Reusing old south-facing city pixels for the reverse facade is explicitly separated from the new city-front art. | B5 PASS:all visible segments/fronts/accessible laterals, exact arrivals/facing/walk-away, native services/signs and boarding/returns. Port body/sea/overhang tests PASS. [Doors](../../qa/qa10/final/B5/doorways/README.md); [city](../../qa/qa10/final/B5/city/results.json). |
| `OlivineCity_PortQuay` | Existing ferry/sailboats/bollards and four terminal returns retained. Two actual ship hatch leaves at27/28,20 append new warp ordinals4/5. The old solid gangway now boards real ship maps. | Source quay/gangway/model anchors. Five source interior gangway cells project to two external leaves; the old four terminal ordinals remain stable. | B5 PASS:all visible segments/fronts/accessible laterals, exact arrivals/facing/walk-away, native services/signs and boarding/returns. Port body/sea/overhang tests PASS. [Doors](../../qa/qa10/final/B5/doorways/README.md); [city](../../qa/qa10/final/B5/city/results.json). |
| `SSAqua_1F` —57×21, **2 components** | New orange/gold hall with four vertical benches plus two horizontal settees, portholes/life rings/plants, eight two-leaf cabin mouths, two B1F stairways and east captain passage. All5 interior gangway cells22–26,19 return to Olivine. | Actual full HGSS hall mosaic/permissions. East/west components connect through B1F; no wall is opened to fake a one-room graph. No Vermilion warp competes at the docked exit. | B5 PASS:every physical component in this map, source-wall/furniture approaches, all registered NPC/sign interactions, normal Save/cold Continue and full-width door/facing/return checks. [Full ship proof](../../qa/qa10/final/B5/aqua/results.json); [visible-crop review](../../qa/qa10/final/B5/aqua/VISUAL_REVIEW.md). |
| `SSAqua_CaptainRoom` —14×13, **1 component** | New chart desk/rug, berth, sofa, bookcase, kitchenette/fridge and framed charts/windows; neutral captain interaction. | Actual full captain mosaic and prop anchors; ship-context bookcase replaces an inappropriate temple-pillar assumption. No plate gifts or captain quest. | B5 PASS:every physical component in this map, source-wall/furniture approaches, all registered NPC/sign interactions, normal Save/cold Continue and full-width door/facing/return checks. [Full ship proof](../../qa/qa10/final/B5/aqua/results.json); [visible-crop review](../../qa/qa10/final/B5/aqua/VISUAL_REVIEW.md). |
| `SSAqua_SoutheastCabins` —28×13, **2 components** | Left red crew cabin with side-by-side portrait twin berths and rear TV/kitchen. Right mustard rest cabin with berth, four-stool table and rear fittings. | Actual lower-right cabin mosaic/source origin. Ordinary party rest is separate from HGSS voyage/sleep arrival state. | B5 PASS:every physical component in this map, source-wall/furniture approaches, all registered NPC/sign interactions, normal Save/cold Continue and full-width door/facing/return checks. [Full ship proof](../../qa/qa10/final/B5/aqua/results.json); [visible-crop review](../../qa/qa10/final/B5/aqua/VISUAL_REVIEW.md). |
| `SSAqua_SouthwestCabins` —28×13, **2 components** | Left blue berth/dining cabin; right gold dining/bookcase cabin. | Actual lower-left mosaic, with distinct carpets/furniture rather than identical empty rooms. | B5 PASS:every physical component in this map, source-wall/furniture approaches, all registered NPC/sign interactions, normal Save/cold Continue and full-width door/facing/return checks. [Full ship proof](../../qa/qa10/final/B5/aqua/results.json); [visible-crop review](../../qa/qa10/final/B5/aqua/VISUAL_REVIEW.md). |
| `SSAqua_NortheastCabins` —28×13, **2 components** | Left red cabin with two portrait berths stacked north–south/rear desks; right mustard berth/four-stool dining cabin. | Actual upper-right mosaic. Embedded terrain furniture is drawn even where separate source prop count is sparse. | B5 PASS:every physical component in this map, source-wall/furniture approaches, all registered NPC/sign interactions, normal Save/cold Continue and full-width door/facing/return checks. [Full ship proof](../../qa/qa10/final/B5/aqua/results.json); [visible-crop review](../../qa/qa10/final/B5/aqua/VISUAL_REVIEW.md). |
| `SSAqua_NorthwestCabins` —28×13, **2 components** | Left blue berth/table cabin with **two diagonal red stools**; right gold twin-berth/yellow-sofa cabin. | Actual upper-left mosaic. Reference grandfather/missing-child plot is not imported. | B5 PASS:every physical component in this map, source-wall/furniture approaches, all registered NPC/sign interactions, normal Save/cold Continue and full-width door/facing/return checks. [Full ship proof](../../qa/qa10/final/B5/aqua/results.json); [visible-crop review](../../qa/qa10/final/B5/aqua/VISUAL_REVIEW.md). |
| `SSAqua_B1F` —57×21, **1 component** | New six-bed crew dormitory/lockers, galley with one3×5 table/six chairs, kitchenette/fridge, engine/hazard bay, western alcove and connecting corridors. | Actual full lower-deck mosaic. Exact native model-base solids and wider door/stair landings are named in the independent source contract; DS model collision is not inferred from floor permissions alone. | B5 PASS:every physical component in this map, source-wall/furniture approaches, all registered NPC/sign interactions, normal Save/cold Continue and full-width door/facing/return checks. [Full ship proof](../../qa/qa10/final/B5/aqua/results.json); [visible-crop review](../../qa/qa10/final/B5/aqua/VISUAL_REVIEW.md). |

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
| New source/generator/reference checks | All68 actual checks PASS, with initial failures and exact rechecks retained. New positive/facing checks add coverage; no generic assertion was removed. See the verification summary. |
| Emerald build / memory | B5 BUILD PASS; payload30,322,784, EWRAM226,448/IWRAM28,392 unchanged. Actual seven ship maps/seven lighthouse maps and six compiled facing hooks verified; exact SHA above. |
| Normal controller movement | B5 PASS:173/173 fronts;482 executed approaches,37 unavailable lateral starts (35solid/2sea), zero missing/failing; all45 intended facings. [Proof](../../qa/qa10/final/B5/doorways/independent-facing-audit.json). |
| Collision / layering | B5 PASS:199 dry+24 Surf;59 materials;1,169 exact new ship source/model-body approaches. Lighthouse physical/layer preservation and selected traversal/views passed; not every unchanged interior fixture/rail was pushed. [City](../../qa/qa10/final/B5/city/results.json), [ship](../../qa/qa10/final/B5/aqua/results.json). |
| NPCs / services / story preservation | B5 PASS:51 accepted Olivine services,14 new ship NPC/sign interactions, berth YES/NO, all3 starters/met/uniqueness, battle/whiteout, title/Continue, Joe field identity/Fly/Surf/run. No new story/rewards claimed. [Regression proof](../../qa/qa10/final/B5/regressions/results.json). |
| Normal Save / cold Continue | B5 PASS:seven genuine old-gate/control saves, old-port walking/Surf/valid-water controls,12 lighthouse saves and12 ship-component saves; input originals and checked party/boxes/bag/flags intact. [Save proof](../../qa/qa10/final/B5/arrival-save-continue/README.md). |
| Native visual proof | Native240×160 before/after PNGs,173 crossing clips, continuous portal/6F recordings and same-view comparisons are linked in the final gallery. Labelled contact sheets retain untouched native panels; static maps are not gameplay. |
| Owner Delta / visual acceptance | **PENDING**. No city100% claim, pixel-identical HGSS claim or automatic acceptance from compilation/traversal. |

Remaining limits are explicit: actual passenger voyages/destination/unapproved
story/rewards; DS online/Seal functions and deferred source trades/rod gifts;
projection/native furniture/sizing choices listed above; and owner visual approval.
A full reverse-quay facade raster is less complete than the now-recovered whole
ship/lighthouse floor maps. The separate elevator-cabin raster was not located;
source room/mechanics are verified, but original GBA decor and its deliberate
two-panel chooser are not claimed HGSS appearance/interaction matched.
The newest private owner save was not supplied; only copied
historical/genuine before-build saves and disclosed compatibility fixtures can be
reported tested. Other Johto areas and the adjacent Route40 Frontier gate are not
silently included in this pass.
