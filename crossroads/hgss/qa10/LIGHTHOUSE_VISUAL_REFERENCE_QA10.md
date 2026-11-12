# Lighthouse visual correction against actual HGSS references

Owner photo4 in the new D187C84F attachment set is the Olivine Lighthouse1F
visitor deck: six planters, four table positions/eight seats, north stairs and
lift match the source. Its flat green native floor is a genuine missing visual
detail. Prop counts and successful traversal did not establish reference fidelity.

[The reference manifest](lighthouse-reference-manifest.json) records actual image
URLs, SHA256 values, dimensions, source geometry provenance and owner-photo hashes.
Seven individual, unannotated HGSS map images were recovered and inspected, replacing
the previous reliance on the900×668 annotated guide composition. These are published
map views with DS projection, not identically framed GBA gameplay screenshots.

## Reference versus old native rendering

| Area | Actual HGSS appearance | Correction and retained adaptation |
| --- | --- | --- |
|1F tourist deck|Pale gray diamond outer floor; central teal-blue brick-pattern inset with a double burgundy edge; four brown tables with eight orange seats; six ferns; pale walls/round windows; red-railed stairs and paired red lift hatch.|Original native pale diamond/teal/burgundy motifs; four combined table-and-seat groups at the existing solid footprints; original ferns retained; red stair/lift finish and pale wall panels. |
|2F landing|Pale patterned floor with a burgundy-edged teal U-shaped runner, two ferns beside its eastern arm, red-railed descending stairs and wooden ascending ladder.|Original U runner and pale surround, preserved plants and upper ladder, matching lower stair/wall finish. |
|3F|Round cracked green boards, gold perimeter trim, pale curved walls/white arched windows, wood ladders and gray internal barrier.|Original vertical weathered boards/cracks, pale/window/perimeter panels; source ladders and every source barrier remain. |
|4F|Same round board/masonry style, branching stairs and actual eastern window drop.|Same restrained floor/window finish; existing drop/branch geometry unchanged. |
|5F|Same cracked-board room with central wall projection, upper ladder and lower hatch.|Same floor/wall finish; all movement/stairs retained. |
|6F|Pink repeated square tiles, bright cyan optical enclosure, glass window ring and red lift doors.|Original pink tile/cyan ring/glass motifs; preserved mechanical beacon actor and existing3×3 native ring footprint. No Ampharos/Jasmine plot is imported. |
|Balcony|Gray-purple cylindrical shell, one east window, diagonal paving, dark paired tower mouth and blue roof/parapet edges.|Private original masonry/paving/blue-parapet motif and paired dark entrance, keeping the existing17×17 physical shell, high walkway and safe rails. |

## Source coordinates and placement

All native coordinates retain the existing source origin. The1F inset spans
x3–13/y5–16. The2F U runner follows x2–4/y5–16 on the west, x12–14/y8–16 on the
east, and x2–14/y14–16 across the south. These are deliberate16px GBA projections
of the inspected DS pattern, not a claim that source camera pixels map1:1.

Source1F table solids are the one-column/two-row groups at(3,8–9),(13,8–9),
(3,13–14),(13,13–14). Original combined table/two-seat motifs fit those exact
solid cells; this compresses horizontal DS furniture width rather than adding
new invisible blockers or painting walkable chairs outside their footprint.
The six fern tops remain(6,7),(10,7),(6,10),(10,10),(6,13),(10,13).

New floor drawing is opaque bottom/blank top. Existing plant/door underlayers
use the appropriate new floor while retaining their current foreground pixels.
The optical housing preserves its original intentional overlap/layer attributes.
Red hatches retain both existing leaves; the balcony's black opening likewise
matches its existing paired warps. No doorway segment is hidden by a new blocker.

The glass/pale panels occupy existing physical walls. Curved DS walls become
native16px panels along the already retained stepped outline; internal barriers
and source physical cores are not removed to obtain a simpler screenshot. The
existing3×3 optical ring remains a chosen native compression. These are explicit
art adaptations rather than unavoidable claims of pixel-identical HGSS rendering.

## Generator ownership and compatibility

`build_hgss_olivine_lighthouse_art.py` exposes
`patch(rooms, maps, check=False)`. The parent landmark generator invokes it after
warps/actors are finalized and before map/layout writes. It creates/registers a
private secondary and mutates drawing references for exactly the six floors and
existing balcony; their actual primary resource pointers remain unchanged.

The immutable285cfa4e baseline defines used metatile IDs and all physical/behavior/
layer constraints. Drawing words come from the freshly generated maritime resource,
because adding port artwork may relocate primary fern glyph slots while preserving
metatile IDs. Using old drawing words with a newly packed primary would corrupt
plants, so that mismatch was caught and fixed during isolated static review.

Private glyph/metatile allocation reuses only IDs unused by these seven baseline
maps, within the original512 bounds. New palette banks7/9/10/12 are private; shared
Port/Ecruteak/Temple resources and palette bank8 remain untouched. No engine limit,
save structure, map/layout/heal ordinal, actor, event, script, warp, collision,
elevation or movement behavior is changed by the visual helper.

## Verification state

Helper Python syntax and isolated deterministic generation passed. All seven
complete static native layouts were inspected, including corrected fern drawing,
replaced timber rails and balcony finish. Static previews contain no actors and
are not emulator evidence. Central generation, actual C resource/ground limits,
independent physical/reference regressions and final-ROM controller/visual tests
are owned by root and the validation/runtime agents; their actual results must
be recorded separately. Owner Delta/visual acceptance remains required.
