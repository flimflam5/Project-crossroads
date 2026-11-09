# Current authority update — canonical logical grid

The actual HGSS world matrix confirms a64x64 Ecruteak area at global tile origin
(352,128). Door/house/gate positions are now traced from source event coordinates,
not estimated from perspective pixels. The older64x50 projection notes below are
superseded. Source facts/provenance are in canonical_events/. Nothing is marked
reference-matched or accepted; station/Trail/interiors/gates/detail remain unfinished.

---

# Ecruteak reconstruction reference audit

Baseline: 512a4d5658973d7d54c531ba8aa62037c67b517a (0.9.1 repair).
Authoritative screenshot sources are linked and hashed in reference-manifest.json.
The downloaded full-city mosaic is1032x785; the Gym gameplay frame is native256x192.
Reference images are analysis/comparison material, not an asset pack or base ROM.
Generated facade source art is an explicitly unaccepted conversion draft; it is
not evidence that the build matches HGSS.

## Inspected reference features

- Raised Burned Tower site northwest, surrounded by an autumn grove; south stair.
- Northern Barrier Station/gatehouse, not Bell Tower directly in the main city.
- Barrier Station passage leads to the distinct autumn Bellchime Trail and Bell Tower.
- Five ordinary house plots, northeast pond, central empty square.
- Dance Theater east of the square, Mart east of theater, Gym southwest,
  Pokemon Center southeast of the square, and southern/western/eastern approaches.
- Gym has rounded ochre roof/ridge, purple front band/sign and glazed doors.
  The Slateport Harbor warehouse stand-in is incorrect and must be replaced.
- Houses have orange/red traditional tiled roofs. Theater has a blue tiled roof.

## Work still required

Trace features into an authored grid; retain stable map IDs but update valid warp
coordinates/reciprocal destinations as required by canonical positions. Add the
missing Barrier Station/Trail using appended map/layout IDs. Inspect interior/floor
references before calling those accurate. Compile, compare native gameplay captures,
and test movement/collision/save migration. No reference-matched area is claimed yet.

## Deliberate deviations/additions to assess

The fixed GBA camera/pixel grid cannot reproduce DS perspective or real-time3D.
Existing optional practice arenas and developer/legacy travel bridges must remain
functional and be identified as Black Ledger additions rather than HGSS features.
Old save positions must remain safe when buildings move. Olivine's required original
residence/Silph/harbor additions need a separate layout conflict review.

## Initial measured implementation checkpoint

A64x50 city draft and seven dedicated facades are generated. Primary/secondary
art allocation uses811 of881 available tiles after reserving General terrain
and animation slots. A real build and initial40-transition controller tour ran,
but the first native inspection exposed the scrolling engine's primary-tileset
assumption. Conditional primary reload and compatible terrain strips are being
verified. No source/reference matched status or owner acceptance is asserted.
The old0.9.1 exact-layout validator must be superseded by equally strict HGSS
ID/contract/buffer tests for authorized changes, never silently weakened.
