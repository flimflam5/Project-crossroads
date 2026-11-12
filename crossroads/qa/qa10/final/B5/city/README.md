# QA10 B5 city evidence

Game source: `cc643ffe711204f3ef38e34e7aa1eb8c9558720f`.
ROM SHA256: `ee2d81d5d0b55b7f1f9d36d1c9b055700164da439f51af7a66b5fb2d2147f90b`.

[Native before/after comparisons](comparisons.html) · [Native images and movement recordings](gallery.html) · [exact results](results.json) ·
[script hashes and direct repository commands](runner-mapping.json) · [checksums](evidence-manifest.json).

All six city suites executed fresh on these exact B5 candidate bytes, followed
by the separately reported full physical S.S.Aqua suite. Their scoped results
are actual scripted mGBA gameplay, distinct from source validators, compilation,
independent reference-image inspection and owner Delta acceptance. Other lanes'
results and the overall candidate decision belong in the root release report.
No statement that an entire city is100% accepted is made here.

## Actual B5 checks

- Eight lighthouse maps,76 real transitions,19 roundtrip edge pairs and73 warp
  trials through ordinary controller travel.
-199 dry building/tree bumps and24 separately disclosed actual native Surf port
  body bumps, all four sides and all eight solid rear bases; no dry skips.
- Both actual terminal portal arrivals23/24,52 and next landings23/24,51 face
  north and show all192 opaque Joe pixels before walking away.
-59 material cases preserve12 table cells,43 fence cases and four rock groups.
  Thirty-seven inaccessible fence starts remain explicitly reported, not passed.
- Six actual front-counter conversations require their correct native NPC/text.
-12 normal lighthouse menu Save/cold Continue cases, five window/lift journeys,
  both selected destinations retained across cold Continue and walking away.
- Two continuous ordinary6F circuits in opposite directions around the optical
  enclosure, recorded in one49-second native video without XY/map/warp setup.
-39 court cells with full composed Joe visibility, all four exact directory
  messages and normal Save/cold Continue followed by walking away.

## Reference image review and adaptations

All eight actual B5 tour images and eleven actual centered/inner-stair B5 lighthouse views
were inspected against seven individual HGSS lighthouse references. The inner
cyan optical housing remains distinct from the outer glass ring. The angular
flat2D projection, flat U core and small northern cap are chosen art adaptations,
not pixel-identical DS geometry or proven hardware limits. A separate verified
HGSS elevator-cabin raster is still missing. See LIGHTHOUSE_VISUAL_REVIEW.md.
The Ecruteak directory court is canonically open ground; its39 art cells were
improved without inventing a structure or changing collision/events/save IDs.

Before images under comparisons/ are specifically QA09 or B3; all phase outputs
are actual fresh B5, never relabelled B4 captures. Historical B4 overall failed
a separate gate/trail intended-facing audit and is preserved separately. B5's
fresh intended-facing/compatibility audit is owned by the other runtime lanes;
these narrower city passes are not substituted for it.

## Fixtures, integrity and reproducibility

Every serial phase guards exact ROM/ELF plus original/copied battery hashes.
Source battery SHA256: `b03ff1ef488fbd25de016e828483bc3001787b84e450a45eaa0ac12a11de30ab`.
The owner's newest private battery was not supplied and is not claimed tested.
Native menu Save/cold Continue uses private output batteries with exact party,
boxes, starter, flags, decoded bag and currency comparisons. No private battery,
state, ROM/ELF, memory dump or raw frame folder is included here.

The shared harness suppresses encounters in test RAM and enables RAM-only
Survey via its actual public desk. Focused dry phases require actual OFF;
water phases use actual desk ON, native Surf, ordinary disembark and desk OFF.
Generic tour/counter assistance is separately disclosed. No player, map, warp
or story-coordinate fixtures set up these movement tests. Native0x61 portal
metadata lands exactly at52 without an automatic animated-door step; the tests
require that exact cell and the next51 landing, with full composed Joe pixels.
No assertion was weakened to pass.

Direct repository commands and exact executed runner hashes are archived in
runner-mapping.json; no hidden temporary launcher is needed. Build the native
bridge with the project's documented command:

```sh
cc -shared -fPIC crossroads/tools/mgba_bridge.c -lmgba -o /tmp/johto-bridge.so
```

Native PNGs remain unmodified240x160; MP4s are H264/yuv420p at240x160. Stills do
not replace movement checks, and neither replaces owner visual acceptance.
Interregional sailings remain a separately documented destination/story decision.
