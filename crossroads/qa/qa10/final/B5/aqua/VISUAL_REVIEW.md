# QA10 B5 S.S. Aqua — independent screenshot review

Reviewed on 2026-11-12. Frozen candidate game source:
`cc643ffe711204f3ef38e34e7aa1eb8c9558720f`.

Frozen candidate ROM SHA-256:
`ee2d81d5d0b55b7f1f9d36d1c9b055700164da439f51af7a66b5fb2d2147f90b`.

This is **fresh B5 image-only evidence**. The reviewer actually opened all
12 new B5 physical-component screenshots and all eight new B5 furnishing
context screenshots listed below. All 20 are native 240 × 160 emulator images
from `build/qa10-aqua-full-detail-b5/`. Inspection contact sheets retained their
native pixels without resampling. Earlier B3/B4 reviews remain historical and
have not been relabeled as B5 verification.

The four complete HGSS mosaics and eight individual HGSS gameplay references
listed below were re-opened for this comparison. This reviewer did not operate
the emulator or independently rerun the separate controller-driven functional
suite. Use its final B5 results for collision, door widths, NPC interactions,
berth service, save/Continue and return-journey claims. This visual report does
not independently declare an overall B5 build/gameplay pass. Owner Delta and
visual acceptance remain pending.

## Actual B5 observations against HGSS

| Area | Visible result in the actual B5 images | Qualification |
| --- | --- | --- |
| `SSAqua_1F`, two components | The orange/gold passenger section and darker officer section have coherent floors, boundaries and cabin mouths. The west context shows four vertical blue benches; the southern context shows the horizontal blue settee and planter. | Native circle/diamond carpet patterns differ from the source. The far northern lounge end and some officer controls are outside these camera crops. |
| `SSAqua_CaptainRoom` | The chart desk, bordered green rug, left berth, orange sofa and portions of the rear fittings read as a furnished captain's cabin. Joe and the captain render coherently. | Native furniture is simpler and flatter; the top crop prevents a complete inspection of every rear-wall fitting. |
| `SSAqua_SoutheastCabins`, two rooms | The red crew room has two portrait berths side by side and rear TV/kitchen fittings. The mustard rest room has a left berth, table and four stools. | The side-by-side portrait beds agree with the source arrangement; they are not landscape-oriented beds. Cloth, carpet and rug details are simplified. |
| `SSAqua_SouthwestCabins`, two rooms | The blue room shows a berth, dining table and two red stools. The gold room shows a table with four green stools and different flooring. | Some rear bookcase/fitting detail is at or beyond the upper camera crop. This image sample does not fully verify that detail. |
| `SSAqua_NortheastCabins`, two rooms | The red room correctly stacks two portrait berths vertically and shows two rear desk groups. The mustard room has a berth, table and four stools. | Rectangular native tablecloths and geometric floor motifs replace the more detailed source cloths and rugs. |
| `SSAqua_NorthwestCabins`, two rooms | The blue room has a berth and table with diagonally opposed red stools. The gold room has two side-by-side portrait berths and a yellow/orange sofa. | Original GBA fixtures preserve the room distinctions without being pixel-identical reproductions. |
| `SSAqua_B1F` | The component and six furnishing views show the wooden perimeter corridor, six crew berths/locker groups, galley table/seating, kitchen equipment and substantial hazard-bounded machinery. Paired crew and galley views cover complementary portions of those areas. | The engine is a flat vented machinery face, with simplified depth and model detail. Bed linen, lockers, kitchen fittings and tablecloth details are redrawn. |

No new obvious graphic corruption, stray ground-arrow artifact, inconsistent
Joe artwork, or missing large fixture within the inspected furnishing views
was found. This is a bounded still-image finding. It does not establish that
every object, collision edge or overlap elsewhere on the ship is correct.

## Chosen adaptations and image-coverage limits

- HGSS model depth, curved surfaces and perspective become flat GBA walls and
  16-pixel metatiles. These are chosen art/projection adaptations, not a claim
  that every simplification is forced by hardware or that the ship is one to
  one with HGSS.
- Carpets, rugs, tablecloth shapes, furniture shading and machinery use original
  reduced-palette motifs. Different room roles and broad arrangements remain
  recognizable; source textures and model detail are not reproduced exactly.
- The documented native gray officer controls differ from the source red
  cabinets. This image set does not fully expose those controls; no complete
  screenshot match for them is claimed.
- The northern lounge end and some rear-wall fixtures are off-camera. This
  review does not infer them absent, nor claim their appearance was inspected.
  Use separate source/static checks or additional camera views for those facts.
- The documented five-cell internal gangway projecting to two exterior leaves
  is a native adaptation. Actual collision, arrivals, facing and reciprocal
  door behavior require the separate B5 movement evidence.
- The authorized physical ship is docked at Olivine. Voyages, Vermilion arrival,
  schedules/tickets, source quests and rewards remain separately unimplemented
  or awaiting design decisions. Furnished-room images do not establish them.

## Exact fresh B5 component frames inspected

Paths are relative to the repository root and identify original runtime outputs
before delivery curation. The 12 components comprise two 1F sections, the captain,
eight separate cabins and the connected lower deck.

| Component | Exact native frame |
| --- | --- |
| 1F passenger section | `build/qa10-aqua-full-detail-b5/SSAqua_1F-component-1.png` |
| 1F officer section | `build/qa10-aqua-full-detail-b5/SSAqua_1F-component-2.png` |
| Captain | `build/qa10-aqua-full-detail-b5/SSAqua_CaptainRoom-component-1.png` |
| Southeast cabin 1 | `build/qa10-aqua-full-detail-b5/SSAqua_SoutheastCabins-component-1.png` |
| Southeast cabin 2 | `build/qa10-aqua-full-detail-b5/SSAqua_SoutheastCabins-component-2.png` |
| Southwest cabin 1 | `build/qa10-aqua-full-detail-b5/SSAqua_SouthwestCabins-component-1.png` |
| Southwest cabin 2 | `build/qa10-aqua-full-detail-b5/SSAqua_SouthwestCabins-component-2.png` |
| Northeast cabin 1 | `build/qa10-aqua-full-detail-b5/SSAqua_NortheastCabins-component-1.png` |
| Northeast cabin 2 | `build/qa10-aqua-full-detail-b5/SSAqua_NortheastCabins-component-2.png` |
| Northwest cabin 1 | `build/qa10-aqua-full-detail-b5/SSAqua_NorthwestCabins-component-1.png` |
| Northwest cabin 2 | `build/qa10-aqua-full-detail-b5/SSAqua_NorthwestCabins-component-2.png` |
| B1F | `build/qa10-aqua-full-detail-b5/SSAqua_B1F-component-1.png` |

## Exact fresh B5 furnishing context frames inspected

| Context | Exact native frame |
| --- | --- |
| Four west benches | `build/qa10-aqua-full-detail-b5/SSAqua_1F-west-lounge-benches.png` |
| Southern settee/planter | `build/qa10-aqua-full-detail-b5/SSAqua_1F-southern-settee-planter.png` |
| Six crew berths | `build/qa10-aqua-full-detail-b5/SSAqua_B1F-six-crew-berths.png` |
| Upper berths/lockers | `build/qa10-aqua-full-detail-b5/SSAqua_B1F-crew-upper-berths.png` |
| Galley table/seating | `build/qa10-aqua-full-detail-b5/SSAqua_B1F-galley-table-seats.png` |
| Galley kitchen | `build/qa10-aqua-full-detail-b5/SSAqua_B1F-galley-kitchen.png` |
| Engine safety edge | `build/qa10-aqua-full-detail-b5/SSAqua_B1F-engine-safety-edge.png` |
| Upper engine equipment | `build/qa10-aqua-full-detail-b5/SSAqua_B1F-engine-upper-equipment.png` |

## Actual HGSS references compared

Cache directory: `/workspace/scratch/hgss-reference/`.
Provenance, dimensions and checksums are recorded in
`crossroads/hgss/qa10/ss-aqua-reference-manifest.json`. Documentary source
geometry/event selection is pinned to `pret/pokeheartgold` revision
`6bf138d6035aa6b43d6f8f4132a12df70f86dcec`; it is distinct from this image review.

Complete mosaics re-opened for B5:

- `SS_Aqua_1F_HGSS.png` — passenger hall/officer wing, 912 × 288.
- `SS_Aqua_1F_Rooms_HGSS.png` — all eight cabins, 912 × 384.
- `SS_Aqua_Captain_Cabin_HGSS.png` — captain, 224 × 192.
- `SS_Aqua_B1F_HGSS.png` — complete lower deck, 1056 × 288.

Additional actual 256 × 192 gameplay references re-opened for B5:

- `SS_Aqua_room_HGSS_reference_385.png`
- `SS_Aqua_room_HGSS_reference_386.png`
- `SS_Aqua_room_HGSS_reference_387.png`
- `SS_Aqua_room_HGSS_reference_388.png`
- `SS_Aqua_room_HGSS_reference_389.png`
- `SS_Aqua_room_HGSS_reference_390.png`
- `SS_Aqua_room_HGSS_reference_391.png`
- `SS_Aqua_room_HGSS_reference_392.png`

The implementation handoff and earlier reviews provide documentary context.
They do not replace the actual new B5 frames above. This review does not label
the ship, port, city or region visually accepted, fully polished or 100% complete.
Owner visual acceptance and the coordinating overall candidate report remain
separate.

Only this new review document was written for this task. No game source, map,
art, test, emulator output or other evidence file was modified by the reviewer.
