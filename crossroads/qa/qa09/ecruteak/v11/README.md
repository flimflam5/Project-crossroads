# Ecruteak final BUILD11 evidence

Source `489c404346f572aefb6856b3dd48a9b364a08ceb`; Emerald ROM SHA256
`df69e014e706168c56180828487a9ab12709a9bccd3dff063fee5f7af5d4f2f4`.
This folder contains native frames, normal-controller recordings and sanitized
reports. It contains no ROM, private battery save or emulator snapshot.

**All six final serial stages completed with exit0 on the frozen ROM.**
Owner Delta/visual acceptance remains pending.

- Full27-map city/interior/landmark tour: PASS,308 transitions,73 round-trip
  pairs and296 warp trials. All27 actual native frames were visually inspected
  independently by two agents. Exact magenta rejection: zero in every frame.
- Focused gate layer repair: PASS,8 actual controller cases and4 short movement
  recordings. Both gates show every opaque Joe pixel on the previously faulty
  floor cells and zero debug magenta at both tested camera positions.
- Local static/source regressions: all60 CI commands PASS on this same source/
  ROM; root ledger preserves the actual commands and exit codes.
- Details/services/save: PASS, all six real service fronts, actual show, Mart
  purchase/PC/healing, four normal Save/cold Continue cases, restored B1F
  stair return, both Gym falls and actual Morty whiteout.
- Furniture: PASS,43 normal controller cases, all13 cushions,20 logo-cell walks
  with Joe visible; native stage6144, audience3584, emblem5120 and each gate3072
  expected pixels matched.
- Ground: PASS,19 recordings,36 trunk approaches,0 arrows and423/423 expected
  foreground leaf pixels. All source/pixel contracts remain meaningful.
- [Sanitized complete results](reports/controller-results.json) preserve exact
  ROM/source identity, actual commands/exits, fixtures and coverage limits.

## Viewing the evidence

`native-views/` preserves all27 unaltered240×160 arrival viewports. Some show
black outside an interior because the camera follows Joe near an arrival at the
room edge; captures settle180 frames after warps. `services/` contains centered,
contextual room and service views. `static-layouts/` shows complete native16px
source layouts **without actors**, explicitly static rather than emulator play.

The [gate before/after comparisons](gate-layers/README.md) keep native240×160
images unscaled inside comparison panels. The earlier defective BUILD10 images
are [separately labelled diagnostic](../gate-layers-before/README.md).

| Actual HGSS reference | BUILD11 counterpart |
| --- | --- |
| [Theater stage and all13 cushions,256×192](references/Theater_HGSS_wikidex.jpg) | [Actual audience,240×160](services/theater-audience.png), [stage,240×160](services/theater-stage.png) and [unscaled paired comparison](theater-reference-comparison.png). |
| [House matrix0066, published750×558 enlarged crop](references/Common_Ecruteak_house_matrix0066_HGSS.jpg) | [Actual southwest home,240×160](services/southwest-house.png) |
| [Center basement, published242×163 crop](references/Common_Center_B1F_HGSS.png) | [Actual blue basement,240×160](services/center-basement.png) |
| [Mart, published source mosaic](references/Common_Mart_interior_HGSS.png) | [Actual Mart,240×160](services/mart-interior.png) |
| [Common gate, published214×180 crop](references/Gate_inside_HGSS.png) | [Actual west gate,240×160](gate-layers/west-magenta-6.png) |
| [City1032×785 published full-map mosaic](references/Ecruteak_City_HGSS.png) | [Complete1024×1024 static GBA city layout; not gameplay](static-layouts/EcruteakCity.png) |
| [Station676×403 published full-map mosaic](references/Bellchime_Trail_gate_1F_HGSS.png) | [Actual Station,240×160](services/barrier-station.png) and [complete static layout](static-layouts/EcruteakCity_BarrierStation.png) |

Reference files retain their published dimensions and bytes. They are not
presented as identically framed DS/GBA camera views. Source URLs, dimensions,
SHA256 checksums and transformations are recorded in
[references/provenance.json](references/provenance.json). No HGSS reference
pixels are used as ROM textures.

The GBA uses original/native flat art instead of DS perspective, and maintains
source relative geometry/accessible floors. The custom Ghost Gym is an approved
Black Ledger addition. DS network services are explicitly offline while their
public rooms, staff and furniture remain. The Theater's southern threshold lacks
a complete published raster view; source events/permissions and actual traversal
verify its geometry. The owner must still review the finished appearance.

Tests use copies of a historical normal battery save, RAM-only survey access and
encounter suppression. Details disclose1HP/legacy-layout fixtures; movement uses
normal controller inputs, with no player-coordinate/map/warp writes. Fresh-core
Save/Continue is distinct from loading an old emulator save state. The owner's
latest private Delta save was not supplied and has not been overwritten.
