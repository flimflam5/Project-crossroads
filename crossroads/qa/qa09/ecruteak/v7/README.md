# Ecruteak V7 regression evidence

This is the **previous V7 test checkpoint**, before the later Theater, gate,
Center, Mart and tower furnishing corrections. It is not the final V8 ROM or
visual acceptance. V8 needs its own fresh build and emulator results.

- Tested ROM SHA256: `0734501b031d05156a28e685dc1c2748153cb065222bd67b0d2e7cea47fefbca`.
- Game-source checkpoint: `3f935d5e8600c5a280b9172b555edb35ca52b6c0`.
- mGBA controller tour: all 27 targets, 308 transitions, 73 round-trip pairs,
  296 warp trials. Furniture: 26 trials. Ground: 19 clips, 36 trunk approaches,
  zero sampled stray arrows, 423/423 expected foreground-leaf pixels.
- Actual service tests include a Mart purchase, PC cancellation with party/box
  integrity, healing, three normal Save/cold Continue cases, Gym falls and a
  Morty practice loss/local whiteout. Fixture limitations are disclosed in the
  sanitized [controller report](reports/controller-results.json).

`native-views/` and `services/` contain untouched 240×160 emulator frames.
`movement/` contains 25 short 240×160 controller recordings, not coordinate
teleports or static path probes. `static-layouts/` contains separately labelled
source-layout renders. Static renders omit actors, lighting and runtime effects;
they are not emulator screenshots. The contact sheet thumbnails are a visual
index, not native-resolution comparisons.

No ROM, personal battery save or emulator snapshot is included. The full file
checksums and sizes are in [manifest.json](manifest.json).

## Reference-versus-checkpoint comparisons

Reference files retain their published pixels and dimensions. No image was
resized to imply a pixel-perfect DS/GBA match. The DS screen is normally256×192;
GBA viewports here are240×160. Some references are published crops or complete
map mosaics, as identified below. They are documentary comparisons, never game
textures. Their source URLs, SHA256 hashes and exact dimensions are recorded in
[references/provenance.json](references/provenance.json).

| Area | Actual HGSS reference | V7 build evidence | Difference / later work |
| --- | --- | --- | --- |
| Theater | [Pokébip stage,256×192](references/Theater_actual_HGSS_Pokebip.png) | [Native240×160](services/five-performer-show.png); [full static room](static-layouts/EcruteakCity_DanceTheater.png) | V7 seating is source-derived, but the green backdrop lacked gold crest/red lanterns. V8 adds original stage art. The complete HGSS audience-room raster is still missing. |
| House | [Guide Strats common0066 house,750×558 published enlarged crop](references/Common_Ecruteak_house_matrix0066_HGSS.jpg) | [Native240×160](services/southwest-house.png); [full static room](static-layouts/EcruteakCity_Residence.png) | Same source matrix/areaData as both Ecruteak houses. Native kitchen/window/cabinet/table represent the source furniture. This enlarged JPEG is not falsely labelled an untouched256×192 DS screen. |
| City | [HGSS full-map mosaic,1032×785](references/Ecruteak_City_HGSS.png) | [GBA full static layout,1024×1024](static-layouts/EcruteakCity.png); [native arrival](native-views/EcruteakCity.png) | DS perspective/height becomes flat16px metatiles. Owner-approved custom Gym is a deliberate addition. Both full-map views are maps, not gameplay viewports. |
| Barrier Station | [HGSS full-room mosaic,676×403](references/Bellchime_Trail_gate_1F_HGSS.png) | [GBA full static room](static-layouts/EcruteakCity_BarrierStation.png); [native room](native-views/EcruteakCity_BarrierStation.png) | Three monks, two alcoves, side stairs and return corridor retained; native timber/tatami compresses DS perspective. |
| Road gate | [Actual common interior,214×180 crop](references/Gate_inside_HGSS.png) | [V7 static room](static-layouts/EcruteakCity_WestGate.png); [native room](native-views/EcruteakCity_WestGate.png) | Matrix0070/areaData63/moveModel15 matches Ecruteak source. V7 lacked the four plants and appropriate counters/window wall; V8 corrects them privately without changing entrances. |

The original unmatched green-roof phone screenshot remains unlocated. These
recordings identify their actual coordinates; they do not pretend that a
convenient nearby gate reproduced the exact historical report. Owner Delta
review remains required for the new combined build.
