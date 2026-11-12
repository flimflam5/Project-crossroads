# S.S. Aqua — read-only visual review of B3

Source `e7e2c085a5a61ef727d06f9f682af7d3a954cc06`; frozen B3 ROM
`af59dff1b06b99a9599c6f98b6fb6bd1e765cc52c0838a2dec5c79a6c1f88373`.
This records the inspected frames at this checkpoint. It does not stand in for
the coordinator's final runtime result, the later B4 lighthouse correction, or
the owner's visual acceptance. No game resources were changed for this review.

## Reference coverage

Compared all seven complete static native layouts against the actual full HGSS
hall, paired-cabins, lower-deck and captain mosaics in the reference manifest.
Those static drawings omit actors and do not prove movement, collision or
emulator rendering. The source-private art is original GBA artwork, not imported
DS textures. The full map references establish where furniture belongs even when
an individual gameplay camera does not show it.

At the first runtime review, ten native component/cold-Continue frames existed:
two main-hall components, captain and both southeast cabins, each before/after
Continue. Also inspected the three1F crew interactions, captain sign/interaction,
and southeast berth prompt/failure diagnostic. No new stray arrow tiles,
corrupted graphics, inconsistent Joe or missing large fixture was visible in
these frames. The berth diagnostic is an unresolved runtime assertion, not a
visual pass or a confirmed game defect; the runtime owner is investigating it.

| Map | Full static reference comparison | Native B3 views inspected so far | Limit |
| --- | --- | --- | --- |
| `SSAqua_1F` | Main hall/lounges, six seating fixtures, plants/portholes, eight hatches, both stairs, separate officer wing/control cabinets match their source roles and relative places. | Both public components/cold Continue; three crew interactions. One interaction shows the vertical bench group. | Center corridor view naturally contains floor and hatches; it cannot verify off-camera lounge ends. Additional lounge context requested. |
| `SSAqua_CaptainRoom` | Chart desk, bordered green rug, berth, orange sofa, bookcase, kitchenette/fridge/windows are present. | Component/cold Continue, captain/chart interaction. | Still frames cannot establish all furniture approaches or overlap. |
| `SSAqua_SoutheastCabins` | Distinct red twin-berth/TV-kitchen cabin and mustard berth/table-four-stools/rest cabin match the source grouping. | Both rooms/cold Continue, crew interaction and rest prompt. | Berth service assertion is separately under investigation; no pass assumed. |
| `SSAqua_SouthwestCabins` | Distinct blue bed/table/two diagonal stools and gold bookcase/table/four green stools. | None at first review. | Static art only; final gameplay views pending. |
| `SSAqua_NortheastCabins` | Red stacked twin berths/two rear desks and mustard bed/table/four stools. | None at first review. | Static art only; final gameplay views pending. |
| `SSAqua_NorthwestCabins` | Blue bed/dining table/two diagonal stools and gold twin beds/yellow sofa. | None at first review. | Static art only; final gameplay views pending. |
| `SSAqua_B1F` | Six beds/locker groups, six-seat galley/kitchen/fridge, large hazardous engine bay, western alcove and perimeter corridor are drawn. | None at first review. | Requested normal-play galley, dormitory and engine context; not yet visually verified in emulator. |

## Deliberate native adaptations and remaining visual differences

- DS perspective, curved walls and model height become orthographic16px GBA
  walls/metatiles. This is a chosen projection; it does not make every native
  texture pixel-identical or every simplification a hardware necessity.
- Bed, table, chair, cabinet and engine models are redrawn with a smaller palette.
  Their named solid footprints are checked separately from HGSS floor permissions.
- The original native carpets use distinct simplified motifs. Small source cabin
  rugs/tablecloth details and DS floor shading are not reproduced one-for-one.
  Officer control banks are native gray rather than the source red cabinets.
- Five source interior gangway floor cells project to two visible external hatch
  leaves, with explicit reciprocal aliases. The competing source Vermilion exit
  is inactive: docked exploration only, with Olivine return.
- The generic source-model projector's temple-pillar interpretation was rejected:
  the captain actually has a bookcase, and the lower-deck bed/locker/ladder groups
  and two passenger-hall plants are explicitly furnished.

No new source correction was justified solely by the initial read-only images.
Final runtime coverage and owner visual acceptance remain required; this review
does not label the ship, port, city or all furniture polished/complete.
