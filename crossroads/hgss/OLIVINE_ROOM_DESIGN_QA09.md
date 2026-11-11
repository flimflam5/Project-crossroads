# Olivine room reconstruction — QA09 source/design review

This document records source implementation and static visual review. It is not
an emulator test report or owner visual acceptance. See the delivery checklist
and exact-ROM controller evidence for those separate states.

## Source authority and conversion

All nine room maps use the stripped, SHA-backed HGSS matrix/prop/permission/event
facts in `canonical_events/olivine-interior-geometry.json`; each map's review entry
records the upstream source URLs/blob IDs. Actual reference images inspected:

- Olivine trade-house screenshot: the three houses share the exact0097 matrix.
  Fridge/stove cabinet on the rear left, rear wall/window and right bookcase, source2x2
  dining table and four seats, plus the actual source0097 rear-right potted plant; single resident in the fishing/trade homes and
  three-person household in the northeastern house follow source coordinates.
- Common Center and Mart HGSS mosaics. Their matrices, props and permissions are
  exactly equal to the Ecruteak source rooms. Reusing the tested GBA adaptation is
  source-supported, not a generic unrelated interior. New Olivine plants also
  follow the actual source prop positions.
- Olivine Gym HGSS screenshot: pale silver/salmon walls, dark hexagonal side
  flooring, straight three-wide steel runway, pylons and leader canopy. Original
  generated GBA modules reproduce those motifs without embedding HGSS textures.

The actual cafe screenshot was also obtained and inspected at
`https://www.serebii.net/heartgoldsoulsilver/gym/gym6-r.png` (Jasmine rematch
section), SHA256eae47433799fbd97549e8e58df5b47f057bbd608fada5161243b1d1175bbc647.
Its cream/checkered floor, left communal table, right bar/staff alcove, two rear
windows, kitchen and source0136 northwest/southwest plants now have native GBA counterparts. The original3D countertop
decorations/barstool models and perspective are adapted, not pixel-identical.

## Per-room inventory

| Native map | Source location | Implemented furnishing/function | Explicit adaptation |
| --- | --- | --- | --- |
| OlivineCity_FishingHouse | Northwestern house | Rear kitchen/storage, dining table/four chairs, fishing resident at5,5 | Native GBA furniture/palette; rod reward deferred |
| OlivineCity_TradeHouse | Northern house | Same source house matrix/furniture, resident at5,5 | Trade/reward system not imported in map pass |
| OlivineCity_SealHouse | Northeastern house | Source furniture, family at5,5;8,5;2,6 | Seal Case/DS seals not implemented by this map milestone |
| OlivineCity_Cafe | Cafe | Source3x3 communal table, stools, right-hand counter/staff kitchen, host and customers | Source12,8 is a visible GBA service aisle so the staff-floor pocket has a safe exit; solid counter retains native over-counter interaction |
| OlivineCity_PokemonCenter_1F | Center | Working nurse pod, native PC, desks, waiting seats, three source plants, basement escalator | Raised DS rear deck flattened; unavailable DS online functions labelled offline; original shared14x9 layout retained for other cities, Olivine gets appended dedicated layout |
| OlivineCity_PokemonCenter_B1F | Center basement | Source-shaped offline reception desks, waiting bench, reciprocal native escalator | Offline communication reception, no simulated online service |
| OlivineCity_Mart | Mart | Source stock-island/counter/shelf placement; existing shop stock and script | Native GBA merchandise/counter assets; shared Mart template remains unchanged |
| OlivineCity_Gym | Lower steel hall | Source hallway, entrance pylons and guide; both exterior leaves, three-wide internal boundary | Long HGSS hall split at sourcey17 over the two stable native map IDs |
| OlivineCity_Gym_Arena | Upper steel hall | Source runway/canopy/platform, Jasmine and optional apprentice | Accepted repeatable practice scripts retained; no badges, source plot battle or rewards |

Joe's residence, accepted neighbour room, Silph office and Harbor Office are
outside this generator's ownership. Their actual functions, starter case and
existing IDs remain. New homes/cafe/basement append map IDs; the two Gym IDs and
all existing map IDs remain stable. Olivine's Center/Mart switch to appended
private layouts while their historically shared layout entries/raw data remain
byte-identical for every other city.

## Entrance and safety contracts

Each new house and cafe interior has two independently operative red exit leaves.
Center leaves8/9,19 correspond to the two visible exterior leaves. The split Gym
has three operative corridor segments each way, not a single working center slot.
No ordinary public floor uses an arrow/warp behavior. The serving counter is
solid and has native MB_COUNTER, so the host can be spoken to from the public side;
the far-end service aisle also makes the rear floor safely escapable.

`validate_hgss_olivine_rooms.py` independently checks source dimensions, furniture
footprints, actual over-counter access, every exit front, correct nurse/localID,
source plants, escalators, continuous three-wide Gym corridor, practice scripts,
stable IDs and original shared template identity. This is a semantic static check;
controller movement, purchase/heal/PC, whiteout and Save/Continue still have to run
on the actual delivery ROM. No static render is a gameplay screenshot.

Native16px static room and annotated collision renders are generated by
`render_olivine_rooms.py` under the selected output directory. The parent delivery
report records final screenshots, movement clips, source commit and ROM checksum.
