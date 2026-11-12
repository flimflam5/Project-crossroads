# Build 5 — every visible opening, strict native facing

Compiled game checkpoint `cc643ffe711204f3ef38e34e7aa1eb8c9558720f`.
Runtime HEAD `ed375e9f382cafc8f225136876778534ac111a17` adds only the
generator-order verification correction and its documentation; no compiled game
inputs differ. The raw runtime report retains its actual HEAD without rewriting.
ROM SHA-256 `ee2d81d5d0b55b7f1f9d36d1c9b055700164da439f51af7a66b5fb2d2147f90b`.

**Actual controller-driven emulator PASS:** all 45 doorway groups, with all 173
visible leaves approached from their required front, entered and exited, checked
for exact destination, exact arrival, independently intended direction and a
normal dry walk-away. Of 519 front/lateral cases, 482 executed and passed; 37
lateral start cells have no normal dry path from that entry component and are
listed individually in the checklist. No required front was skipped. The 37 excluded lateral start cells are 35 solid
collision cells and two real sea cells beside the north port entrance; they are
not omitted door leaves or failed front approaches.

All 67 real Build 4 facing failures now pass the same independent physical
expectations. An additional independent postchecker requires all 519 records,
correct ROM/manifest identity, every actual facing and no skipped fronts.

`--record-fronts-only` changes only media capture: all 519 controls/assertions
still execute; each of 173 fronts has a normal-play video, and every executed
approach has its own unmodified native 240×160 arrival screenshot. Default
record-all behavior remains available. The short videos are doorway-crossing
excerpts: route navigation and the separately asserted walk-away are not captured
frame by frame. The two-leaf portal journey in `../migration/` is a continuous
movement recording. All input/script hashes are preserved.
No private batteries, snapshots, raw frame caches or ROMs are exported.

This is automated normal-controller emulator gameplay, separate from source
validators and owner Delta visual acceptance. Furniture, services, lighthouse
interiors, ship components and ordinary save tests are reported by other suites.

| Opening / building | Maps (outside → inside) | Visible fronts passed | Total executed | Unavailable laterals |
|---|---|---:|---:|---:|
| theater | EcruteakCity → EcruteakCity_DanceTheater | 4 | 11 | 1 |
| barrier | EcruteakCity → EcruteakCity_BarrierStation | 4 | 12 | 0 |
| gym | EcruteakCity → EcruteakCity_Gym | 4 | 11 | 1 |
| southwest-house | EcruteakCity → EcruteakCity_Residence | 3 | 9 | 0 |
| dowsing-house | EcruteakCity → EcruteakCity_DowsingHouse | 3 | 9 | 0 |
| center | EcruteakCity → EcruteakCity_PokemonCenter_1F | 3 | 9 | 0 |
| mart | EcruteakCity → EcruteakCity_Mart | 3 | 9 | 0 |
| burned-tower | EcruteakCity → EcruteakCity_BurnedTower | 3 | 9 | 0 |
| west-city-gate | EcruteakCity → EcruteakCity_WestGate | 6 | 17 | 1 |
| west-route-gate | JohtoRoute38 → EcruteakCity_WestGate | 6 | 16 | 2 |
| east-city-gate | EcruteakCity → EcruteakCity_EastGate | 6 | 16 | 2 |
| east-route-gate | JohtoRoute42 → EcruteakCity_EastGate | 6 | 16 | 2 |
| bell-tower | BellchimeTrail → EcruteakCity_BellTower | 3 | 9 | 0 |
| trail-station-return | BellchimeTrail → EcruteakCity_BarrierCorridor | 2 | 4 | 2 |
| station-corridor-stairs | EcruteakCity_BarrierStation → EcruteakCity_BarrierCorridor | 2 | 4 | 2 |
| olivine-joe-residence | OlivineCity → OlivineCity_Residence | 3 | 8 | 1 |
| olivine-accepted-neighbour | OlivineCity → OlivineCity_NeighborHouse | 3 | 8 | 1 |
| olivine-custom-gym | OlivineCity → OlivineCity_Gym | 4 | 12 | 0 |
| olivine-pokemon-center | OlivineCity → OlivineCity_PokemonCenter_1F | 4 | 12 | 0 |
| olivine-poke-mart | OlivineCity → OlivineCity_Mart | 3 | 9 | 0 |
| olivine-silph-office | OlivineCity → OlivineCity_SilphOffice | 3 | 9 | 0 |
| olivine-harbor-office | OlivineCity → OlivineCity_HarborOffice | 3 | 8 | 1 |
| olivine-lighthouse | OlivineCity → OlivineCity_Lighthouse_1F | 3 | 8 | 1 |
| olivine-fishing-house | OlivineCity → OlivineCity_FishingHouse | 3 | 8 | 1 |
| olivine-trade-house | OlivineCity → OlivineCity_TradeHouse | 3 | 8 | 1 |
| olivine-seal-house | OlivineCity → OlivineCity_SealHouse | 3 | 8 | 1 |
| olivine-cafe | OlivineCity → OlivineCity_Cafe | 3 | 8 | 1 |
| olivine-port-city-entrance | OlivineCity → OlivineCity_PortTerminal | 4 | 10 | 2 |
| olivine-gym-hallway | OlivineCity_Gym → OlivineCity_Gym_Arena | 6 | 16 | 2 |
| olivine-port-quay-main | OlivineCity_PortQuay → OlivineCity_PortTerminal | 4 | 11 | 1 |
| olivine-port-inspection-side | OlivineCity_PortQuay → OlivineCity_PortTerminal | 4 | 12 | 0 |
| olivine-lighthouse-balcony | OlivineCity_Lighthouse_Balcony → OlivineCity_Lighthouse_3F | 4 | 12 | 0 |
| aqua-gangway | OlivineCity_PortQuay → SSAqua_1F | 7 | 17 | 4 |
| aqua-southwestcabins-0 | SSAqua_1F → SSAqua_SouthwestCabins | 4 | 12 | 0 |
| aqua-southwestcabins-1 | SSAqua_1F → SSAqua_SouthwestCabins | 4 | 12 | 0 |
| aqua-southeastcabins-0 | SSAqua_1F → SSAqua_SoutheastCabins | 4 | 12 | 0 |
| aqua-southeastcabins-1 | SSAqua_1F → SSAqua_SoutheastCabins | 4 | 11 | 1 |
| aqua-northwestcabins-0 | SSAqua_1F → SSAqua_NorthwestCabins | 4 | 12 | 0 |
| aqua-northwestcabins-1 | SSAqua_1F → SSAqua_NorthwestCabins | 4 | 12 | 0 |
| aqua-northeastcabins-0 | SSAqua_1F → SSAqua_NortheastCabins | 4 | 12 | 0 |
| aqua-northeastcabins-1 | SSAqua_1F → SSAqua_NortheastCabins | 4 | 12 | 0 |
| aqua-captainroom-0 | SSAqua_1F → SSAqua_CaptainRoom | 4 | 12 | 0 |
| aqua-west-stairs | SSAqua_1F → SSAqua_B1F | 4 | 10 | 2 |
| aqua-right-stairs-north-rim | SSAqua_1F → SSAqua_B1F | 4 | 10 | 2 |
| aqua-right-stairs-south-rim | SSAqua_1F → SSAqua_B1F | 4 | 10 | 2 |

Each native video is in [`clips/`](clips/); every executed arrival is in
[`actual-arrivals/`](actual-arrivals/). The machine-readable per-opening
checklist links each group to its exact tests and lists unavailable start cells.
