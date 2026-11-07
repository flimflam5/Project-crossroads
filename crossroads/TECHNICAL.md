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
The new group is gMapGroup_CrossroadsOlivine (75); maps use REGION_JOHTO and
MAPSEC_OLIVINE_CITY. No full Johto region-map UI exists yet.

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
