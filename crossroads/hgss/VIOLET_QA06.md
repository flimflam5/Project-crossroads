# Violet and eight owner Gyms — QA06 scope

This is a reconstruction checkpoint, not completed Johto or owner visual
acceptance. [REGION_CHECKLIST.md](REGION_CHECKLIST.md) lists the remaining work.

## References and implemented areas

Violet's actual HGSS mosaic was inspected, SHA256
419cd943756c9324eb18a92a8f61e0f997c0cfe46a8d626ba22ff15128145495.
The canonical world matrix, terrain permissions, prop positions and doorway
coordinates come from pret/pokeheartgold tree6bf138d6035aa6b43d6f8f4132a12df70f86dcec.
The source selections, file/blob hashes and stripped geometry are versioned in
canonical_events. No source story scripts, ROMs or raw reference archive are
committed. Raster references are linked in reference-manifest.json.

| Area | Reference-derived implementation | Adaptation or pending work |
|---|---|---|
| Violet exterior | Source forest/pond, central plaza, two bridges, exact relative door positions, services, two houses, school and tower |64x72 native map adds8 northern rows to fit full GBA tower; flat original GBA architecture replaces DS models. Fine DS lightposts/shore detail and owner visual acceptance remain open. |
| Sprout Tower1–3F | Source floor geometry, central pillar and every stair branch/alias | Fixed pillar art; original trainers, rewards and story omitted. Old primary up/down warp indices retained. |
| Northwest house | Source11x10 room, furniture and resident | Old internal Workshop map ID retained; it now represents the real canonical house, not an invented workshop plot. |
| Southern house | Source11x10 room and furniture, retained rest service | Old Residence ID retained; no Bellsprout/Onix trade imported. One exterior courtyard corner and sign position adapt the larger GBA footprint. |
| School | Source17x13 room, four student desks, teacher area, storage and monitor | Original GBA furniture; ambient pupils only, no new gameplay lesson/reward flags. |
| Center1F/B1F | Reference native room dimensions, healing/PC, staff, stairs and safe respawn | Existing service art reused; DS communication desks explicitly offline. Basement appended. |
| Mart | Source14x13 room, existing shop stock and clerks | Native service graphics; no imported parcel/story event. |
| Violet Gym | Source raised walkway geometry and entrance | DS lift uses fixed GBA access. No new trainer roster, badge award or story gate. Exterior is the owner's custom Flying Gym. |
| West/east gates | Source12x12 floors/portals, reciprocal city/route doors | Two new IDs append. East facade moves one column west to leave a real approach to the canonical boundary portal. Adjacent routes retain their old exploration drafts. |
| Route32 seam | Reciprocal scrolling connection offset9/-9, matching elevations/paving | Only the northern7-row buffer changes. A private General-based primary uses previously unused metatile1ff with existing concrete pixels. All other route terrain is preserved. |

All seven historical Violet exterior warp indices retain their destinations.
Gym alias7, school alias8 and gate aliases9–12 append; no old map, layout or heal
IDs are reordered. The three new maps are CenterB1F, WestGate and EastGate.

The source world facts also cover the other nine towns and Routes29–48. Those
records are references only; they do not reconstruct the corresponding areas.

## Owner Gym integration

All eight128x112 owner PNGs are really placed in Olivine, Ecruteak, Violet,
Azalea, Goldenrod, Cianwood, Mahogany and Blackthorn. These explicitly supplied
Black Ledger buildings replace literal HGSS Gym facades. The original97-file pack
is preserved in crossroads/art/eight_gyms_v1 with96 verified SHA entries. Its
installer alone would only register unused assets; do not use it as integration.

build_eight_gym_integration.py packs private city resources around each existing
map's visible tiles/palettes and animation slots. No shared General/Western/HGSS
art is replaced. The immutable QA05 baseline and new authored Violet base are
separate inputs. The original Gym pixels are independently compared after tile
relocation. Non-Gym terrain, events, attributes and graphics are compared exactly.
Both door halves have reciprocal destinations; no badges/teams are added.

## Save handling

Use normal Continue with a COPY of an exported battery save, not a cross-build
emulator snapshot. Existing room cache/layout refresh remains. Violet's old heal
doorway(35,33) moves to the same Center at(49,56), with whiteout arrival(8,13).
Newly blocked saved positions move to nearby clear floor. An old walking position
newly covered by Violet's pond moves to dry ground; a real saved Surf avatar stays
on water. No save structure, party/box data, starter variables or badge IDs change.
Survey water assistance intentionally clears on cold boot; opt in again at the
actual harbor/Center desk when needed. Continue while already surfing is separate.

## Validation and actual emulator coverage

Results and exact ROM hash are recorded in qa/hgss-qa06 after the final run.
Do not infer emulator success from generation or compilation. Automated checks
verify source door/stair coordinates, every-public-tile escape, exact neighbor
scope, append-only IDs, capacity and build inclusion. The eight-Gym test verifies
archive/pixel identity and legacy non-Gym pixels/attributes/events independently.

Historical validators now delegate Violet's changed geometry to these stronger
source/escape contracts instead of asserting the old blank-room hashes. Their
other assertions remain. The western script scan includes the new linked Violet
script file. Collision probes exclude standing on a live doorway trigger, which
legitimately enters the room; both doorway halves are tested separately. A test
planner must re-enable RAM-only survey access through its real desk after a cold
Continue, rather than assuming it persists in saves.

Reproducible local checks:

```sh
python3 crossroads/tools/build_hgss_violet_assets.py --check
python3 crossroads/tools/build_johto_network.py --through west --check
python3 crossroads/tools/validate_hgss_violet.py
python3 crossroads/tools/validate_eight_gyms.py
python3 crossroads/tools/validate_johto_network.py --built
python3 crossroads/tools/validate_visual_repairs.py
python3 crossroads/tools/johto_network_smoke.py --save COPY.sav --library /tmp/johto-bridge.so --output build/violet-tour --targets VioletCity,VioletCity_Residence,VioletCity_Workshop,VioletAcademy,VioletCity_PokemonCenter_1F,VioletCity_PokemonCenter_B1F,VioletCity_Mart,VioletCity_Gym,SproutTower_1F,SproutTower_2F,SproutTower_3F,VioletCity_WestGate,VioletCity_EastGate --all-edges
python3 crossroads/tools/violet_detail_smoke.py --save COPY.sav
python3 crossroads/tools/eight_gyms_smoke.py --save COPY.sav
```

The detailed test discloses its private1HP loss fixture, obsolete walking-position
fixture, encounter suppression and save copies. It does not edit an owner save or
grant production progression. DS moving lift/pillar behavior, new regional Gym
teams/progression, additional encounter tables and the unapproved prologue remain
outside this increment. The inherited New Game prologue is still unfinished.
