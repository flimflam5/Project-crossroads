# QA10 B5 lighthouse — independent screenshot review

Reviewed on 2026-11-12. Frozen candidate game source:
`cc643ffe711204f3ef38e34e7aa1eb8c9558720f`.

Frozen candidate ROM SHA-256:
`ee2d81d5d0b55b7f1f9d36d1c9b055700164da439f51af7a66b5fb2d2147f90b`.

This is fresh **B5 image-only evidence**. The reviewer actually opened all
eight new B5 tour screenshots, all ten expected new B5 centered screenshots,
and the additional new B5 inner-stair context: **19 native 240 × 160 frames**.
The B5 files listed below were inspected directly and in contact sheets that
retained native pixels without resampling. Earlier B4 findings are historical;
they have not been relabeled as B5 verification.

These actual emulator images were produced by a separate controller-driven
runtime lane. This reviewer did not operate the emulator or independently run
its movement, collision, door, stair, service or save tests. Those results and
the overall B5 candidate status remain the responsibility of the coordinating
runtime report. This document does not declare an overall build or gameplay
pass. Owner Delta and visual acceptance remain pending.

## Actual B5 observations against HGSS

| Area | Observation in the actual B5 images | Reference qualification |
| --- | --- | --- |
| 1F | The centered frame shows the teal inset with burgundy edging, pale patterned surround, six ferns and four side table/seat groups. No obvious corrupt or unrelated art appears. | The arrangement and surface families are recognizable; the motifs are original GBA drawings. |
| 2F | The U-shaped teal runner, pale surround, two plants and ladder approaches remain coherent across the tour and centered views. | The DS wall depth and plant/furniture details are simplified. |
| 3F | Green weathered boards, pale perimeter windows, ladders and the central shaft/south branch are coherent in the three inspected views. | Circular walls and the raised central barrier use stepped, flat 2D geometry. |
| 4F | Both branches retain coherent boards, shaft boundaries, ladders and perimeter windows. | The angular outline and simplified wall surfaces remain visible adaptations. |
| 5F | Boards, shaft/wall projection, ladder and perimeter window motifs remain coherent. | The camera samples do not prove every source surface or detail is reproduced. |
| 6F | The inner U-shaped optical housing is cyan and distinct from the diagonal white/teal outer glass ring. The tour shows the small northern cap; the lower-room and extra inner-stair contexts show the same separation. Joe is visibly inside the U in the extra context. | The broad flat U and small cap are chosen art/projection adaptations. They are not one-to-one representations of HGSS's cylindrical optical enclosure, gold bracing or 3D depth, nor established here as unavoidable hardware limits. |
| Balcony | Diagonal paving, blue parapet, dark entrance and one east-side window render consistently in the tour and centered east-side view. | The source cylindrical faceted shell is flattened into an angular structure. |
| Elevator | The compact cabin, floor, two northern control-panel motifs and paired exit markers render coherently. | A separate verified HGSS cabin raster is still missing. Its art remains an adaptation rather than a verified visual match. |

No new obvious rendering corruption or visible clipping was found in these
19 B5 stills. The inner 6F enclosure remains visually distinct from the outer
glass; the earlier B3 surface-assignment defect is not visible in these actual
B5 images. These observations do not establish absence of clipping during
movement or complete visual coverage of every part of every floor.

## Exact new B5 tour images inspected

Paths are relative to the repository root and identify original runtime outputs
before delivery curation.

| Map | Exact native screenshot |
| --- | --- |
| 1F | `build/qa10-lighthouse-tour-b5/OlivineCity_Lighthouse_1F.png` |
| 2F | `build/qa10-lighthouse-tour-b5/OlivineCity_Lighthouse_2F.png` |
| 3F | `build/qa10-lighthouse-tour-b5/OlivineCity_Lighthouse_3F.png` |
| 4F | `build/qa10-lighthouse-tour-b5/OlivineCity_Lighthouse_4F.png` |
| 5F | `build/qa10-lighthouse-tour-b5/OlivineCity_Lighthouse_5F.png` |
| 6F | `build/qa10-lighthouse-tour-b5/OlivineCity_Lighthouse_6F.png` |
| Balcony | `build/qa10-lighthouse-tour-b5/OlivineCity_Lighthouse_Balcony.png` |
| Elevator | `build/qa10-lighthouse-tour-b5/OlivineCity_Lighthouse_Elevator.png` |

## Exact new B5 centered images inspected

| Context | Exact native screenshot |
| --- | --- |
| 1F | `build/qa10-lighthouse-details-b5/lighthouse-1F-component-0-context.png` |
| 2F | `build/qa10-lighthouse-details-b5/lighthouse-2F-component-0-context.png` |
| 3F main | `build/qa10-lighthouse-details-b5/lighthouse-3F-component-0-context.png` |
| 3F south branch | `build/qa10-lighthouse-details-b5/lighthouse-3F-component-5-context.png` |
| 4F main | `build/qa10-lighthouse-details-b5/lighthouse-4F-component-0-context.png` |
| 4F west branch | `build/qa10-lighthouse-details-b5/lighthouse-4F-component-3-context.png` |
| 5F | `build/qa10-lighthouse-details-b5/lighthouse-5F-component-0-context.png` |
| 6F lower room | `build/qa10-lighthouse-details-b5/lighthouse-6F-component-0-context.png` |
| 6F inner stair, additional view | `build/qa10-lighthouse-details-b5/lighthouse-6F-inner-stair-context.png` |
| Balcony east side | `build/qa10-lighthouse-details-b5/lighthouse-Balcony-component-0-context.png` |
| Elevator | `build/qa10-lighthouse-details-b5/lighthouse-Elevator-component-None-context.png` |

## Actual references compared

The seven individual HGSS rasters were re-opened for comparison with the fresh
B5 captures. Cache directory: `/workspace/scratch/hgss-reference/`.
Provenance, dimensions and checksums are recorded in
`crossroads/hgss/qa10/lighthouse-reference-manifest.json`.

- `Glitter_Lighthouse_1F_HGSS.png`
- `Glitter_Lighthouse_2F_HGSS.png`
- `Glitter_Lighthouse_3F_HGSS.png`
- `Glitter_Lighthouse_4F_HGSS.png`
- `Glitter_Lighthouse_5F_HGSS.png`
- `Glitter_Lighthouse_6F_HGSS.png`
- `Glitter_Lighthouse_3F_Balcony_HGSS.png`

The annotated floor guide and earlier reviews are documentary context, not
substitutes for these individual references or the actual B5 images. No
separate HGSS Elevator cabin raster was available for a full visual comparison.

## Acceptance and scope limits

- The angular flat geometry, simplified cyan enclosure, small northern cap and
  native surface motifs require owner visual review. This report makes no
  one-to-one HGSS claim or claim that every simplification is technically
  necessary.
- Still images cannot establish full-width doors, collision during movement,
  stairs, window falls, lift trips, services, save/Continue or compatibility.
  Use the separately identified B5 gameplay and compatibility reports.
- Overall candidate status and owner acceptance remain pending; this report
  does not declare the lighthouse, city or region 100% complete.

Only this new review document was written for this task. No game source, map,
art, test, emulator output or other evidence file was modified by the reviewer.
