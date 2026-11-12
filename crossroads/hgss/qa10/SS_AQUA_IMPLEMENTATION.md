# S.S. Aqua implementation — QA10 engineering handoff

The owner now authorizes a complete physical ship and logical Olivine boarding.
This expands QA09's deliberately closed boarding boundary. It does not approve
a new region, destination, ticket/schedule rule, missing-child quest or reward.
Owner visual acceptance remains separate from source and emulator verification.

## What existed before this pass

QA09 supplied the15×13 terminal,40×27 quay, visible ferry/sailboats and four
reciprocal terminal/quay exits. The two city entrance leaves led to the terminal's
north end despite the former city facade facing south. Native controller checks
could pass those connections while the physical orientation was wrong.

The source gangway warp at(27,20) was replaced by a solid railing. The nearby
sign said passenger sailings were not operating. There was **no S.S. Aqua ship
interior, dormant boarding unlock or hidden voyage implementation** behind it.
The accepted Harbor Office travel system is separate and must remain intact.

Emerald's S.S. Tidal rooms are present but cannot simply be linked as Aqua: their
scripts include Scott/Briney/Peeko, Slateport/Lilycove departures, voyage state,
trainers, a TM gift and bed-driven cruise progression. None is imported here.

## Source-owned physical ship

`build_ss_aqua.py` creates seven append-only native maps from the pinned HGSS
geometry and complete inspected mosaics recorded in the reference manifest.
All retain source coordinate origin(0,0); only unused southeast extent is cropped.

| Native map | Dimensions | Physical contents |
| --- | --- | --- |
| `SSAqua_1F` |57×21|Orange/gold passenger hall, six seating fixtures, portholes/life rings/two plants, eight cabin hatches, gangway, both lower-deck stairs, officer corridor and captain approach. |
| `SSAqua_CaptainRoom` |14×13|Chart desk/rug, bookcase, kitchenette/fridge, berth, windows/charts and vertical sofa. |
| `SSAqua_SoutheastCabins` |28×13|Two separate cabins: red crew room with TV/kitchen and twin berths; mustard berth/rest room with dining table, four stools and rear fittings. |
| `SSAqua_SouthwestCabins` |28×13|Separate blue berth/dining cabin and gold bookcase/dining cabin. |
| `SSAqua_NortheastCabins` |28×13|Separate red twin-berth/desks room and mustard berth/four-stool dining cabin. |
| `SSAqua_NorthwestCabins` |28×13|Separate blue berth/dining cabin and gold twin-berth/yellow-sofa room. |
| `SSAqua_B1F` |57×21|Six-bed crew quarters/lockers, galley with one complete table and six chairs, kitchenette/fridge, substantial engine/hazard bay, western alcove and perimeter corridors. |

The1F east/west public components are intentionally separate and join through
the lower deck. Each paired-cabin map retains two independent rooms; no wall is
opened merely to simplify a graph. Every native public component has a real exit.

The new private assets are original indexed GBA drawings guided by actual HGSS
references. They use411 glyphs and508 secondary metatiles across native-sized
sheets and loaded palette banks6–12. The existing maritime pool is already510/512
and is not enlarged. Shared tilesets, engine limits and save structures stay fixed.

## Door and arrival rules

All new hatches have two visible operative leaves. Both west-stair columns and
all four cells of the right stair mouth work; the actual source right-stair alias
is preserved. South room exits use low native sills, rather than painting a tall
opaque door across ordinary walking floor. Northern mouths use native0x60 exit
behavior where a south-facing arrival and one exit step are required;0x61 keeps
the incoming direction for southern/lateral thresholds. No engine change is used.

The source five-cell interior gangway row22–26,19 remains completely open and
operative. It projects to two outside hatch leaves27/28,20 as a documented native
art decision. Ship indices0(center24,19) and12(right-center25,19) return to quay
indices4/5. Aliases13/14/15 cover22/23/26. Source conditional Vermilion event12 at
the same physical point is recorded but inactive; native12 is the new right leaf,
not an invented sailing destination.

`ss-aqua-doorways.json` records13 groups/55 visible segments, exact normal
approaches, intended facing and the asymmetric arrival lists. Right-stair source
B1F ordinal2 legitimately returns to canonical1F ordinal10 rather than the top
alias; the explicit arrival contract preserves that fact.

## Collision and furnishings

HGSS floor permissions do not contain all DS model collision. The generator
therefore records every exact new native solid bed/table/chair/cabinet base and
each door-width/landing expansion in `ss-aqua-build-review.json`. These are named
GBA projection decisions, not claims that source floor flags alone prove physics.
Upper furniture drawing rows have proper foreground layers over opaque ground;
solid bodies and actual public approaches are independently checked.

The source model inventory is paired with the actual native fixture/anchor,
including the two plants and ship-specific bookcase/ladder meanings. Embedded
cabin beds/tables/sofas are explicitly furnished even where source props are empty.
Expanded fixtures preserve edge panels instead of wrapping their texture and
accidentally drawing several tables. The galley uses a dedicated3×5 single table.
Continuous rear wall backgrounds prevent floating porthole/header fragments.

Ambient crew/passengers use neutral dialogue and no trainer or story flags.
The source berth offers ordinary party rest using the existing common heal
routine, without calling any Tidal cruise progression or changing travel state.
The chart and ship-purpose interactions add no items, badges, quests or rewards.

## Integration and verification

Root centrally runs `build_ss_aqua.py` **after** existing Olivine landmarks, then
the aggregate doorway/network generators. The new generator appends map/layout
IDs and manifest entries; it does not own or overwrite the city, terminal or quay.
Its `--check` is deterministic. `--output-root /tmp/...` provides a source-only
prototype without replacing the ROM/ELF while an emulator is running.

The initial seven-map prototype passed source geometry, component escape, actor
clearance and Python compilation checks, and all full static layouts were inspected.
The first independent audit caught the plant/bin mismatch and a source stair
arrival contract error; both were corrected rather than waived. The four native
control-bank body cells were independently inspected against the actual mosaic.

Compilation, actual final-byte controller gameplay, save/Continue, service/NPC
checks, before/after evidence and owner visual acceptance must be recorded by the
coordinating final QA report. Prototype/static success is not an emulator result.

Voyages still require an approved destination map, route/ticket policy, schedule
and any Black Ledger story dependencies. Actual HGSS Olivine/Vermilion schedules,
missing-granddaughter/sailor quest and Metal Coat/plate gifts remain reference
facts, not silently adopted Black Ledger canon.
