# Johto exploration architecture —0.9

Append-only groups 75 (nums0..126) and76 (nums0..21) avoid signed WarpData and reserved mapNum 127. Emerald build filtering uses REGION_HOENN for these narratively Johto maps. Met sections214..252 are appended while NONE213/special253..255 stay stable. RAM-only survey Surf and 51-node field atlas add no save fields. Measured ROM29,455,512 bytes; EWRAM226,448; IWRAM28,392. Legacy PokeNav/Fly/habitat maps remain unchanged. See johto/manifest.json for IDs/services and johto/coverage.json for measured coverage.

---

# Technical architecture and builds

## Existing engine and toolchain

RHH pokeemerald-expansion 1.17.2; retain the existing Makefile and APIs. Emerald
is the game target. Upstream FireRed/LeafGreen targets remain in CI. `make all`
uses modern ARM GCC, GNU17, Thumb/ARM7TDMI and no original-ROM checksum comparison.
`make release` enables LTO through config.mk. See INSTALL.md for OS setup.

Debian/Ubuntu dependencies: build-essential, binutils-arm-none-eabi,
gcc-arm-none-eabi, libnewlib-arm-none-eabi, libpng-dev, python3.

```sh
python3 crossroads/tools/validate_opening.py
python3 crossroads/tools/validate_olivine.py
python3 crossroads/tools/build_olivine_layout.py --check
make -j4 -O all
```

Output: pokeemerald.gba plus ELF/map files. Never use an older artifact as evidence
for new source changes.

The audit workspace initially lacked ARM GCC/newlib/PNG headers. Debian trixie
packages were extracted under /workspace/toolchain/root, outside the repository,
without system configuration changes. Local GCC is 14.2.1. Newlib include/lib
symlinks were supplied inside that extracted toolchain. To reuse this workspace:

```sh
export PATH=/workspace/toolchain/root/usr/bin:$PATH
export CPATH=/workspace/toolchain/root/usr/include
export LIBRARY_PATH=/workspace/toolchain/root/usr/lib/x86_64-linux-gnu
export LD_LIBRARY_PATH=/workspace/toolchain/root/usr/lib/x86_64-linux-gnu
make -j4 -O all
```

## Maps and persistence

Map headers/events are JSON; scripts use existing assembly macros. Map groups and
layouts generate constants; do not hand-edit generated headers. New IDs append.
The new group is gMapGroup_CrossroadsOlivine (75); maps use MAPSEC_OLIVINE_CITY. The JSON region field must be REGION_HOENN
for inclusion in the Emerald target: mapjson uses it as a build filter, not a
geographic field in the runtime map header. Olivine is narratively in Johto. No full Johto region-map UI exists yet.

crossroads/tools/build_olivine_layout.py authors the blockout reproducibly using
compatible General/Slateport metatiles and collision data. Copy rectangles are
placeholders for final Johto art. Porymap can inspect the JSON and binary maps.
Update the generator with blockout changes.

The Center uses the engine nurse and storage behavior; link-club stairs are removed
from its dedicated layout. A new heal location keeps whiteout/Teleport destinations
in Olivine. Interiors have reciprocal exits. No new trainer battles, story triggers,
forced cutscenes or save fields are added. Starter choice stays at var 0x40FA.
Visiting with a rescued partner enables the normal Pokémon menu flag.

Back up saves: old locations retain their IDs, but a save made in a new map cannot
be loaded in an older build lacking it. Compatibility requires emulator testing.
The scripted return bridge does not reset party, inventory, or story variables.

## CI, artifacts and capacity

Existing CI builds Emerald, FireRed, LeafGreen, release and battle tests. Emerald
artifacts include source SHA, ROM hash, build label, checklist and limitations.
Upload success is not gameplay verification. ROMs are never committed. Public
release patch/base-ROM requirements remain release work.

Before adding regions measure linked ROM/EWRAM/IWRAM against 32 MiB / 256 KiB /
32 KiB limits. Audit tileset/sprite budgets, map ID widths, save capacity, travel,
world-state persistence and encounter/progression balance. Do not promise all
regions fit. Existing engine difficulty constants are not approved Crossroads rules.

## Optional emulator regression runner

`crossroads/tools/emulator_smoke.py` uses mGBA 0.10 (tested with Debian's 0.10.5),
Python, an ARM `nm`, a host C compiler and libmgba-dev. It builds the small
mgba_bridge.c helper in ignored build output; no ROM modifications or supplied
commercial BIOS are required.

```sh
python3 crossroads/tools/emulator_smoke.py
```

It initializes a fresh test game through the debugger, skips the original intro,
sets a valid test name, then sends controller input through real door transitions,
the Alpha notebook/terminal and nurse scripts. It checks all seven building returns,
both piers, each level-5 starter, duplication prevention, city travel and healing
without loss of menu fonts. Engine-specific RAM layout assumptions are deliberately
pinned to the audited version. Revisit those if the engine is ever upgraded.
Screenshots/snapshots stay in build/emulator-smoke and must not be committed.
This runner uses emulator snapshots for branch setup; it does **not** claim to test
normal SRAM saving, the normal introduction, battle stability, or owner acceptance.

## Starter acquisition location (0.2)

The rescue implementation now lives in crossroads/scripts/starter_rescue.inc.
Only the Olivine Silph office case links to its entry point. The old notebook
links to Crossroads_EventScript_VisitRescueCase, a transport/duplicate-check bridge.
Mon creation itself assigns the actual current map section; no summary changes
or hidden rewrite of existing party/box origins are involved. The runtime smoke
test decrypts each new mon's growth/origin blocks to check species, level,
MAPSEC_OLIVINE_CITY and recorded met level 5.

## Western extension 0.6

Route 39's north road joins Route 38 with offset 0. Route 38's right connection
has offset -14 into Ecruteak; the city's reciprocal left offset is +14. This
aligns Route 38 rows 12–14 with the Ecruteak street at rows 26–28. Map group 75
remains append-only: Route 38=9, city=10, interiors=11–17. Ecruteak heal location
and map sections append via their source JSON; generated headers are not authored.
The Center retains CableClub_OnResume for safe nurse/menu buffer initialization.

Regenerate city/Route 38 with build_western_johto_layouts.py, Route 39 with
build_route39_layout.py. Run validate_western_johto.py --built after an Emerald
build. emulator_smoke.py now tours the whole network, all seven Ecruteak doors,
city interactions and both Centers. Use --gender 0/1 for both saved gender values.
Private SRAM/snapshots remain ignored build output. No save structure changed.

## Olivine detail 0.7

OlivineCity_SilphOffice and HarborOffice keep map IDs 75.6/75.7, dimensions 10×8,
and accepted warps. Their appended layouts use Building/Facility tiles; exit
metatiles 0x206/0x207 retain MB_SOUTH_ARROW_WARP (unlike GenericBuilding's 0x208/9).
Author via build_olivine_interiors.py and run validate_olivine_interiors.py. The
validator also checks interaction access and escape from old walkable coordinates.
Home rest calls HealPlayerParty without setting respawn, story or starter state.
The detail smoke module covers decline/accept, empty party, HP/status, notes,
records and both offices, alongside the existing regional regression runner.
