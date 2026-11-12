# QA10 B4 lighthouse — independent screenshot review

Reviewed on 2026-11-12. Frozen game source:
`df8c4598d88c7770626be4621a5f39cf60dadb95`.

Frozen ROM SHA-256:
`4fb28fe64fc44c0546462a935655346a61f13b644bc3040468146d136cd6d656`.

This is a read-only inspection of actual emulator screenshots. The reviewer
opened all eight tour images and all ten centered context images listed below,
at their native 240 × 160 resolution, and compared them with the seven actual
HGSS reference rasters. Contact sheets used for inspection retained those native
pixels without resampling. The screenshots were produced by the separate
controller-driven runtime lane; this reviewer did not operate the emulator or
independently execute its movement, collision, doorway, stair or save tests.
Those scripted gameplay results must be reported separately.

## Observed results

| Area | Visible result in the reviewed B4 frames | Reference qualification |
| --- | --- | --- |
| 1F | Teal inset floor with burgundy edging, patterned pale surround, six ferns and four side table/seat groups form a furnished reception floor. No obvious unrelated or corrupt art is visible. | The arrangement and surface families are recognizable against the actual 1F reference; this is original GBA art, not a pixel match. |
| 2F | The teal U-shaped runner, pale surround, two plants and ladder landings remain coherent in both camera views. | The DS wall depth and furniture shading are simplified. |
| 3F | Weathered green boards, ladders, pale perimeter windows, central shaft and southern branch are visible without obvious new rendering errors. | The source's circular room, raised wall and depth are flattened into stepped 2D geometry. |
| 4F | Both reviewed branches retain the green boards, ladders, shaft boundaries and pale windowed perimeter. | Angular outline and simplified walls remain visible adaptations. |
| 5F | Green boards, shaft/wall projection, ladder and perimeter window motifs remain coherent. | The screenshot supports the visible surface comparison, not an assertion that every source detail is reproduced. |
| 6F | The B3 visual defect is corrected: the inner U-shaped optical enclosure is cyan, while the white/teal diagonal glass motif stays on the outer room ring. The northern cap remains visible in the tour frame. The centered lower-room frame confirms the same distinction on both inner arms. | The large flat angular U and small northern cap are chosen art/projection adaptations. They do not reproduce HGSS's cylindrical optical enclosure, gold-braced wall and 3D depth one to one. They are not established here as unavoidable hardware limits. |
| Balcony | Diagonal paving, blue parapet, dark entrance and single east-side window read consistently in the tour and centered east-side views. | The cylindrical faceted shell is represented as a flat angular 2D structure. |
| Elevator | The compact cabin has a consistent floor, two northern control-panel motifs and paired exit markers. No obvious new corruption is visible. | A separate actual HGSS cabin raster is still missing; the cabin's appearance is an adaptation, not a verified visual match. |

The specific B3 problem was the use of the outer glass-ring motif on the inner
6F enclosure. The actual HGSS 6F raster distinguishes those surfaces. B4 now
distinguishes them too. No new obvious rendering defect was found in the 18
reviewed B4 stills. This finding is limited to what those frames show; it does
not establish complete floor coverage, absence of clipping during movement, or
owner visual acceptance.

## Exact native screenshots inspected

Paths below are relative to the repository root and identify the original
runtime outputs before any delivery curation.

| Tour image | Exact path |
| --- | --- |
| 1F | `build/qa10-lighthouse-tour-b4/OlivineCity_Lighthouse_1F.png` |
| 2F | `build/qa10-lighthouse-tour-b4/OlivineCity_Lighthouse_2F.png` |
| 3F | `build/qa10-lighthouse-tour-b4/OlivineCity_Lighthouse_3F.png` |
| 4F | `build/qa10-lighthouse-tour-b4/OlivineCity_Lighthouse_4F.png` |
| 5F | `build/qa10-lighthouse-tour-b4/OlivineCity_Lighthouse_5F.png` |
| 6F | `build/qa10-lighthouse-tour-b4/OlivineCity_Lighthouse_6F.png` |
| Balcony | `build/qa10-lighthouse-tour-b4/OlivineCity_Lighthouse_Balcony.png` |
| Elevator | `build/qa10-lighthouse-tour-b4/OlivineCity_Lighthouse_Elevator.png` |

| Centered view | Exact path |
| --- | --- |
| 1F | `build/qa10-lighthouse-details-b4/lighthouse-1F-component-0-context.png` |
| 2F | `build/qa10-lighthouse-details-b4/lighthouse-2F-component-0-context.png` |
| 3F main | `build/qa10-lighthouse-details-b4/lighthouse-3F-component-0-context.png` |
| 3F south branch | `build/qa10-lighthouse-details-b4/lighthouse-3F-component-5-context.png` |
| 4F main | `build/qa10-lighthouse-details-b4/lighthouse-4F-component-0-context.png` |
| 4F west branch | `build/qa10-lighthouse-details-b4/lighthouse-4F-component-3-context.png` |
| 5F | `build/qa10-lighthouse-details-b4/lighthouse-5F-component-0-context.png` |
| 6F lower room | `build/qa10-lighthouse-details-b4/lighthouse-6F-component-0-context.png` |
| Balcony east side | `build/qa10-lighthouse-details-b4/lighthouse-Balcony-component-0-context.png` |
| Elevator | `build/qa10-lighthouse-details-b4/lighthouse-Elevator-component-None-context.png` |

## Actual references inspected

Individual raster cache directory: `/workspace/scratch/hgss-reference/`.
Provenance, dimensions and checksums are recorded in
`crossroads/hgss/qa10/lighthouse-reference-manifest.json`.

- `Glitter_Lighthouse_1F_HGSS.png`
- `Glitter_Lighthouse_2F_HGSS.png`
- `Glitter_Lighthouse_3F_HGSS.png`
- `Glitter_Lighthouse_4F_HGSS.png`
- `Glitter_Lighthouse_5F_HGSS.png`
- `Glitter_Lighthouse_6F_HGSS.png`
- `Glitter_Lighthouse_3F_Balcony_HGSS.png`

The annotated `Olivine_Lighthouse_Floors_HGSS.png` guide and earlier B3 captures
were also inspected as diagnostic context. They do not replace the seven
individual HGSS rasters as the appearance references. No distinct cabin raster
was supplied or verified by this review.

## Remaining acceptance and limitations

- Owner Delta and visual review remain pending. This document does not declare
  the lighthouse, Olivine or the region visually accepted or 100% complete.
- The angular flat geometry, simplified cyan enclosure, small northern cap and
  original GBA surface motifs remain visible artistic adaptations requiring
  owner review; they are not a claim of a one-to-one HGSS recreation.
- A still image cannot verify collision, layering during movement, full-width
  doors, stairs, window falls, lift behavior, services or save/Continue. Use the
  separately recorded B4 movement and compatibility results for those claims.
- This review adds no story, encounter, reward, badge or progression approval.

Only this new review document was written by this reviewer. No game source,
map, art, test, emulator output or other evidence file was modified.
