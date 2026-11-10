# Ecruteak QA07 — repair build, owner acceptance pending

Active branch: `feature/ecruteak-dependability-qa07`, continuing QA06
`9cd6a73717c1bfd124967b7e485740aa5b25d651`. Implementation checkpoint:
`2daea5e0aace6c23fa7159bec8e85431f1f49609`. The delivered package identifies
its exact final source revision separately in `build-info.json`.

Regional expansion is paused. Do not move to another area until the owner reviews
this Ecruteak build. The exterior and buildings the owner likes, custom Ghost
Gym, all map/layout/heal IDs, save structure, Joe, title/V5 music, approved
encounters, starter uniqueness and accepted practice scripts remain preserved.

## Recovered evidence and actual defects

Local QA06 and its delivered ROM both hash to
`ffe8f84c8dee1e688d5e8f7615078a03953c51e0a337c2036fd4fa6a8bf820cb`.
The earlier screenshots are recovered from attachment storage. They show the
older blue Gym/exterior and the orange Barrier Station; they predate QA06.
No newly attached screenshot identifies the current green-roof report. The
owner's exact Delta filename and Continue-versus-save-state answer are still
unconfirmed. Do not claim the phone's loaded binary was identified.

- **Ground arrows reproduced on exact QA06:** walking south at40,58–61 shows an
  arrow. `hgss_connection_buffer.repair` substituted General0x24 for ordinary
  paving. Its behavior is0x65, `MB_SOUTH_ARROW_WARP`; the engine displays an arrow
  without requiring a warp event. Use private unused metatile0x1ff with normal
  ground behavior and the project's existing brick texture. Original General
  arrow/door behavior and all road coordinate portals stay intact.
- **Tree overlap reproduced:** enter the canopy at26,42 from25,42. The General
  tree's leaves were entirely in the lower metatile layer; an empty top layer
  cannot occlude Joe. Retain original bottom pixels and add a leaf-only foreground
  mask. Grass/shadow remain beneath Joe; the two-cell trunk remains blocked.
  Static art is identical. Native leaf matching rises from262/423 to423/423 pixels.
- **Building investigation:** the recorded house gutter20,43 is a roof overhang;
  it correctly lets Joe pass behind the roof. The adjacent base19,44 and front
  wall22,46 block. Station and every other current Ecruteak facade were checked
  independently, with native clips. No reproduced solid-wall penetration was
  found in these cases, so no building was repainted or blanket-blocked.
- **Ambiguous private doors:** source Ecruteak has two accessible houses. The
  three preserved closed facades now say “Private residence. The door is locked.”
  Existing BG-event positions/indexes are retained; three labels are appended.
  No generic rooms or story events were invented.

The specific green-roof example remains **unmatched/unreproduced**, not marked
fixed. If it remains in QA07, obtain its current screenshot/location and exact ROM
filename before altering that building. Do not expand the map while it is open.

## Changes and preservation

Game data changed in EcruteakCity and the seven-tile scrolling buffers of the
already connected Routes37/38/42. These route edits are required for identical
neutral-ground decoding across city seams; they add no geography or encounters.
Bellchime Trail's private tree resources receive the same foreground treatment;
its walking footprint/warps and every interior/floor layout stay byte-identical
to QA06. The city Gym is repacked from the unchanged owner art, not replaced.

The live Ecruteak authoring base now feeds the isolated Gym packer, so future
regeneration cannot restore the old road bug. The immutable QA06 contract is a
separate preservation check: every map/layout/heal ID, every existing Ecruteak
event/entrance, every interior byte and6111 unaffected city/Trail static cells are
pinned. Exactly289 city seam cells change from flower/arrow ground to brick.

Main files: `build_hgss_ecruteak{,_assets,_chain}.py`,
`hgss_connection_buffer.py`, new `hgss_ecruteak_terrain.py`, private tilesets,
`authoring/EcruteakCity.*`, city map JSON and the three neighbor buffers.
`validate_ecruteak_qa07.py` and `ecruteak_qa07_repro.py` add independent semantic
and actual native-pixel regressions. Other smoke tools gain isolated output paths
and explicit shop/PC/private-door coverage; gameplay service scripts are preserved.

## HGSS comparison and necessary adaptations

Pinned references remain in `canonical_events/ecruteak-interior-geometry.json`,
`075_T27.json`, `interior-review.json`, `room-review.json`, `service-review.json`
and `gate-review.json`. The per-map checklist includes provenance/coordinates,
IDs, entrances, services, deviations and current evidence. Existing HGSS raster
references are linked beside native GBA views in the evidence gallery.

- DS perspective, vertical models and per-model occlusion become flat GBA
  metatiles, foreground roof/leaf masks and ground-plane collision footprints.
  Accepted city buildings/street spacing are preserved, not redrawn during repair.
- Bell Tower's source staircase/pad/one-way-jump graph remains intact. Timber
  walkways, rails/braces, pillars and blocked slopes use original GBA temple art.
  Bellchime's footprint is translated four cells south to fit the tall2D tower.
- HGSS's tall Gym bridge is split across the two existing GBA map IDs. Safe fall
  returns and the accepted optional practices work. Badge/story progression and
  candle-extinguishing battle gates remain deliberately deferred.
- Center reception is flattened; the native nurse/PC and basement stairs work.
  DS online desks explicitly say offline. That service is unavailable, not a
  phantom entrance or an implemented internet feature.
- Houses, Theater, Center, Mart and road gates have canonical geometry/event/prop
  evidence but lack a separate complete native HGSS interior raster in the current
  reference cache. Their GBA furniture is an adaptation; exact decorative visual
  matching is **not certified**. Two furnished houses and a functioning five-person
  Theater are present, rather than empty generic rooms.
- No legendary/source plot actors, rewards, new teams, badge gates or main-story
  scenes are imported. Those omissions are design boundaries, not map completion.

## Actual checks

BUILD PASS: Emerald compiled, ROM payload30,039,792/33,554,432 bytes; padded32MiB.
EWRAM226,448/262,144; IWRAM28,392/32,768. RAM use is unchanged. ROM grows20,676 bytes
from delivered QA06; capacity is not a blocker.

AUTOMATED STATIC PASS:30 existing build/generator/opening/Olivine/western/Johto/
interior/graphics/music checks, plus the final native-recording regression.
All27 declared Ecruteak maps are included in the real Emerald build.

CONTROLLER-DRIVEN mGBA PASS (automated emulator gameplay, separately inspected
screenshots; no claim of a human manual playthrough):

-27 target maps,288 transitions,63 explicit round-trip doorway/stair/pad/border
  pairs. Covers both leaves/aliases of intended doors and all three city roads.
-500 reachable exterior blocked-edge approaches,36 independently specified trunk
  approaches across all six freestanding trees,19 recorded ground/tree/facade cases.
- All three private-door messages; Theater's five performers move/return and
  release controls; original Mart stock and one actual200-money Poke Ball purchase.
- Center PC menu/cancel retains exact box/party bytes; healing; both Gym fall
  returns; actual Morty practice loss, correct local whiteout arrival and healing.
- House and Center normal Save → fresh core → title/Continue, exact party/position;
  copied obsolete-layout fixture migration. Real old0.8 Bell9F battery Continue.
- All ten existing QA Fly landings/cancel, exact Joe departure/arrival VRAM and
  postflight Save/Continue/reopen Fly; Joe Surf four directions, bikes/wheelie,
  rod casting and return to walking; all three starter rescues/met/duplicate guards.
- Normal cold title, animation, Start/New Game handoff and reset. The unchanged
  old Birch new-game introduction is not claimed replaced or fully playtested.

Fixtures: only private save copies. The source battery is read-only. Encounter
suppression,1HP/stale-layout and bike/rod gear are test-RAM setup, never ROM grants.
Water assistance uses the real session-only survey desk. Starter tests disclose
debugger initialization that skips the unchanged old intro, then real scripts and
controller movement. No owner saves, ROMs, snapshots or private SRAM are committed.

## Remaining / completion decision

Owner Delta visual/collision acceptance is **PENDING**. The current green-roof
report is open. Not every individual furniture perimeter received controller
probing; all public-floor escape and every declared warp were checked separately.
Dive/watering/advanced tricks/contests/multiplayer remain outside normal tests.
These facts prevent calling Ecruteak finally accepted or the region polished.

Do not infer acceptance from the old positive exterior review, a validator count,
or compilation. After owner review, reproduce any remaining exact position through
controller input and repair the responsible generator/data before another build.

## Reproduce / evidence

See `../qa/ecruteak-qa07/TEST_RESULTS.json`, native gallery `comparisons.html`,
`city-tour/coverage.json`, `collision-coverage.json`, `after/reproduction.json`,
`after/semantic-tree-probes.json`, `after/visual-regressions.json` and run logs.
The27-row table follows; its machine-readable counterpart is
`ecruteak-qa07-checklist.json`.

| Map | ID group:number / layout | Inspected purpose | Emulator / visual acceptance |
|---|---|---|---|
| EcruteakCity | 75:10 / 790 | Liked exterior and owner Ghost Gym; signs, private-door labels, six freestanding trees, pond and three road apertures | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_BurnedTower | 75:11 / 808 | Charred rear wall, statues, stone/wood floor, basement stair and return | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_BellTower | 75:12 / 799 | Reference Bell Tower 1F: wooden walkways, rails/braces, pillars and canonical stair/pad/jump network | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_Residence | 75:13 / 918 | Furnished southwest home: refrigerator, cabinet, TV, dining table, chairs and two residents | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_DanceTheater | 75:14 / 810 | Stage, audience seating, five performers, optional working show | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_Gym | 75:15 / 813 | Owner custom exterior; lower bridge, lamps, guide and safe falls | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_PokemonCenter_1F | 75:16 / 920 | Healing, PC, local respawn, waiting area and communication reception | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_Mart | 75:17 / 922 | Two counters, stocked shelves and accepted original shop inventory | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_BellTower_2F | 75:24 / 800 | Reference Bell Tower 2F: wooden walkways, rails/braces, pillars and canonical stair/pad/jump network | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_BellTower_3F | 75:25 / 801 | Reference Bell Tower 3F: wooden walkways, rails/braces, pillars and canonical stair/pad/jump network | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_BellTower_4F | 75:26 / 802 | Reference Bell Tower 4F: wooden walkways, rails/braces, pillars and canonical stair/pad/jump network | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_BellTower_5F | 75:27 / 803 | Reference Bell Tower 5F: wooden walkways, rails/braces, pillars and canonical stair/pad/jump network | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_BellTower_6F | 75:28 / 804 | Reference Bell Tower 6F: wooden walkways, rails/braces, pillars and canonical stair/pad/jump network | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_BellTower_7F | 75:29 / 805 | Reference Bell Tower 7F: wooden walkways, rails/braces, pillars and canonical stair/pad/jump network | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_BellTower_8F | 75:30 / 806 | Reference Bell Tower 8F: wooden walkways, rails/braces, pillars and canonical stair/pad/jump network | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_BellTower_9F | 75:31 / 807 | Reference Bell Tower 9F: wooden walkways, rails/braces, pillars and canonical stair/pad/jump network | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_BurnedTower_B1F | 75:32 / 809 | Ash/rubble, pillars, paths and reciprocal basement stair | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_Gym_Arena | 75:34 / 814 | Upper bridge, lamps, optional Morty/student practices and safe falls | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_BarrierStation | 76:22 / 913 | Three caretakers, prayer alcoves, clear entrance and corridor stair | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_BarrierCorridor | 76:23 / 914 | Timber corridor, rails and both stair endpoints | All declared warps round trip PASS; native view inspected; owner PENDING |
| BellchimeTrail | 76:24 / 915 | Canonical autumn route footprint, station return, tall tower and clear approaches | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_BellTower_10F | 76:25 / 916 | Reference Bell Tower 10F: wooden walkways, rails/braces, pillars and canonical stair/pad/jump network | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_BellTower_Roof | 76:26 / 917 | Reference Bell Tower roof, spire and ladder | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_DowsingHouse | 76:27 / 919 | Second furnished canonical home, no unapproved item reward | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_PokemonCenter_B1F | 76:28 / 921 | Offline communication desks, waiting bench and working return stairs | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_WestGate | 76:29 / 923 | Furnished reference gate, route/city wayfinding, all road-width aliases | All declared warps round trip PASS; native view inspected; owner PENDING |
| EcruteakCity_EastGate | 76:30 / 924 | Furnished reference gate, route/city wayfinding, all road-width aliases | All declared warps round trip PASS; native view inspected; owner PENDING |
