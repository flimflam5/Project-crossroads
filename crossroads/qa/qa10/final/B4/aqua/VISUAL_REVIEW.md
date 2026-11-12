# QA10 B4 S.S. Aqua — independent screenshot review

Reviewed on 2026-11-12. Frozen game source:
`df8c4598d88c7770626be4621a5f39cf60dadb95`.

Frozen ROM SHA-256:
`4fb28fe64fc44c0546462a935655346a61f13b644bc3040468146d136cd6d656`.

**B4 is an overall failed candidate, not an accepted or final delivery.** The
coordinator separately reported intended-facing failures at Ecruteak gates and
the trail; a B5 successor is pending. This document preserves B4 image-only
evidence under its exact original identity. It must not be relabeled as B5
verification or used as an overall release pass.

This review independently inspected the **12 actual B4 room-component
screenshots and eight additional actual B4 furnishing context screenshots**
listed below. All are native 240 × 160 emulator frames from
`build/qa10-aqua-full-detail-b4/`. Inspection contact sheets retained those
pixels without resampling. These are fresh B4 outputs; the earlier B3 review
was consulted as background and is not relabeled as final B4 evidence.

The reviewer did not operate the emulator, alter its inputs, or execute the
separate scripted movement suite. The functional suite was still running when
this visual review was completed. Collision, door widths, berth service,
save/Continue and other gameplay results belong to that lane's final report,
not to this still-image review. Owner Delta and visual acceptance remain
pending.

## Observed comparison

The four complete HGSS mosaics and eight individual HGSS gameplay references
listed below were opened and compared with the actual B4 images.

| Native area | What the actual B4 images show | Limits and differences from HGSS |
| --- | --- | --- |
| `SSAqua_1F`, two components | Distinct orange/gold passenger-hall floor and darker officer-wing floor, wall boundaries and dark cabin mouths are coherent. The west lounge context exposes four vertical blue benches; the southern context exposes the horizontal blue settee and planter. | Native circle/diamond carpet motifs replace the source textures. The far northern lounge end and some officer-wing equipment are outside these camera crops; this review does not claim to have seen every fixture there. |
| `SSAqua_CaptainRoom` | The chart desk and bordered green rug, left berth, orange sofa and portions of the rear fittings form a recognizable furnished captain's cabin. Joe and the captain render consistently in the frame. | Original GBA furniture is simpler and more orthographic than the HGSS models. Some rear-wall fittings are cropped at the top of the camera view. |
| `SSAqua_SoutheastCabins`, two rooms | The red crew cabin contains two portrait berths side by side and rear TV/kitchen fittings. The mustard rest cabin has a left berth, dining table and four stools. | The side-by-side arrangement of the red cabin's portrait berths agrees with the source; it must not be confused with landscape-oriented beds. Carpet/rug details and DS shading are simplified. |
| `SSAqua_SouthwestCabins`, two rooms | The blue cabin shows its berth, dining table and two red stools. The gold cabin shows a table with four green stools and different floor treatment. | The reference bookcase/rear fittings are only partly visible at the upper crop; a complete visual inspection of those details is not established by these stills. |
| `SSAqua_NortheastCabins`, two rooms | The red cabin correctly stacks its two portrait berths vertically and has two rear desk groups. The mustard cabin contains a berth, table and four stools. | Native rectangular tablecloths, geometric floors and compact furniture replace the source's detailed cloth and rugs. |
| `SSAqua_NorthwestCabins`, two rooms | The blue cabin has a berth and dining table with two diagonally opposed red stools. The gold cabin has two portrait berths side by side and a yellow/orange sofa. | Furniture and floors are original simplified GBA motifs. The two rooms remain visibly distinct rather than sharing one empty generic furnishing scheme. |
| `SSAqua_B1F`, connected lower deck | The component and six furnishing contexts show the wooden perimeter corridor, crew quarters with six berths and locker groups, a galley table/seating and kitchen fittings, and a substantial machinery bay bordered by hazard striping. The two crew views and two galley views complement each other's camera crops. | The native engine uses a flat vented machinery face rather than the complete source model's 3D depth. Kitchen, lockers, bed linen and tablecloth details are simplified. |

No new obvious graphic corruption, stray ground-arrow artifact, inconsistent
Joe artwork, or missing large fixture within the inspected furnishing views
was found. This is a bounded observation about these frames, not proof that
every object, overlap or pixel elsewhere on the ship is correct.

## Chosen adaptations and remaining qualifications

- The DS perspective, model height and curved or deep surfaces are redrawn as
  flat 16-pixel GBA walls and metatiles. This is a chosen projection, not a claim
  that every simplification is forced by hardware or that the result is one to
  one with HGSS.
- Carpets, rugs, rectangular tablecloths, furniture shading and engine details
  use original reduced-palette art. They retain different room purposes and
  broad arrangements but do not reproduce all source patterns or model detail.
- The implementation documents native gray officer controls where the source
  uses red cabinets. Those controls are not fully visible in this image set;
  the difference remains an explicit art decision rather than a screenshot
  match claim.
- These camera samples do not cover every rear-wall fitting or the far northern
  lounge end. Off-camera content is not inferred missing, and its presence or
  accuracy must rely on separate source/static checks or further camera views.
- The documented five-cell internal gangway to two-leaf exterior projection is
  a native adaptation. This review does not establish its collision, arrival or
  reciprocal-door behavior; use the actual doorway/movement evidence.
- The authorized scope is a physically explorable **docked** ship. Voyages,
  Vermilion arrival, schedules, tickets, source quests and rewards are separately
  unimplemented or awaiting design decisions. A furnished ship screenshot does
  not establish those systems.

## Exact actual B4 component screenshots inspected

All paths are relative to the repository root and identify the original runtime
outputs before delivery curation. The 12 components comprise two 1F sections,
the captain's room, eight separate cabins and the connected lower deck.

| Component | Exact native frame |
| --- | --- |
| 1F passenger section | `build/qa10-aqua-full-detail-b4/SSAqua_1F-component-1.png` |
| 1F officer section | `build/qa10-aqua-full-detail-b4/SSAqua_1F-component-2.png` |
| Captain | `build/qa10-aqua-full-detail-b4/SSAqua_CaptainRoom-component-1.png` |
| Southeast cabin 1 | `build/qa10-aqua-full-detail-b4/SSAqua_SoutheastCabins-component-1.png` |
| Southeast cabin 2 | `build/qa10-aqua-full-detail-b4/SSAqua_SoutheastCabins-component-2.png` |
| Southwest cabin 1 | `build/qa10-aqua-full-detail-b4/SSAqua_SouthwestCabins-component-1.png` |
| Southwest cabin 2 | `build/qa10-aqua-full-detail-b4/SSAqua_SouthwestCabins-component-2.png` |
| Northeast cabin 1 | `build/qa10-aqua-full-detail-b4/SSAqua_NortheastCabins-component-1.png` |
| Northeast cabin 2 | `build/qa10-aqua-full-detail-b4/SSAqua_NortheastCabins-component-2.png` |
| Northwest cabin 1 | `build/qa10-aqua-full-detail-b4/SSAqua_NorthwestCabins-component-1.png` |
| Northwest cabin 2 | `build/qa10-aqua-full-detail-b4/SSAqua_NorthwestCabins-component-2.png` |
| B1F | `build/qa10-aqua-full-detail-b4/SSAqua_B1F-component-1.png` |

## Exact actual B4 furnishing contexts inspected

| Context | Exact native frame |
| --- | --- |
| Four west lounge benches | `build/qa10-aqua-full-detail-b4/SSAqua_1F-west-lounge-benches.png` |
| Southern settee/planter | `build/qa10-aqua-full-detail-b4/SSAqua_1F-southern-settee-planter.png` |
| Crew's six berths | `build/qa10-aqua-full-detail-b4/SSAqua_B1F-six-crew-berths.png` |
| Crew's upper berths/lockers | `build/qa10-aqua-full-detail-b4/SSAqua_B1F-crew-upper-berths.png` |
| Galley table/seating | `build/qa10-aqua-full-detail-b4/SSAqua_B1F-galley-table-seats.png` |
| Galley kitchen | `build/qa10-aqua-full-detail-b4/SSAqua_B1F-galley-kitchen.png` |
| Engine safety edge | `build/qa10-aqua-full-detail-b4/SSAqua_B1F-engine-safety-edge.png` |
| Upper engine equipment | `build/qa10-aqua-full-detail-b4/SSAqua_B1F-engine-upper-equipment.png` |

## Actual HGSS references inspected

Cached directory: `/workspace/scratch/hgss-reference/`.
Provenance, dimensions and hashes are recorded in
`crossroads/hgss/qa10/ss-aqua-reference-manifest.json`. Source geometry and event
selection are pinned to `pret/pokeheartgold` revision
`6bf138d6035aa6b43d6f8f4132a12df70f86dcec` by that manifest; that documentary
context is distinct from this visual image comparison.

Complete mosaics opened:

- `SS_Aqua_1F_HGSS.png` — passenger hall and officer section, 912 × 288.
- `SS_Aqua_1F_Rooms_HGSS.png` — all eight cabins, 912 × 384.
- `SS_Aqua_Captain_Cabin_HGSS.png` — captain's cabin, 224 × 192.
- `SS_Aqua_B1F_HGSS.png` — complete lower deck, 1056 × 288.

Additional actual 256 × 192 HGSS gameplay references opened:

- `SS_Aqua_room_HGSS_reference_385.png`
- `SS_Aqua_room_HGSS_reference_386.png`
- `SS_Aqua_room_HGSS_reference_387.png`
- `SS_Aqua_room_HGSS_reference_388.png`
- `SS_Aqua_room_HGSS_reference_389.png`
- `SS_Aqua_room_HGSS_reference_390.png`
- `SS_Aqua_room_HGSS_reference_391.png`
- `SS_Aqua_room_HGSS_reference_392.png`

`crossroads/hgss/qa10/SS_AQUA_IMPLEMENTATION.md` and
`SS_AQUA_VISUAL_REVIEW_B3.md` supplied implementation and earlier diagnostic
context. Their prior results do not substitute for the actual B4 frames listed
here. This review does not declare the ship, port, city or region visually
accepted, fully polished or 100% complete.

Only this new review document was written for this task. No game source, map,
art, test, emulator output or other evidence file was modified by the reviewer.
