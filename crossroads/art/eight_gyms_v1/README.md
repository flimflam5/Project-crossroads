# Black Ledger — Eight Custom Johto Gym Exteriors, v1

Original custom designs for Violet/Flying, Azalea/Bug, Goldenrod/Normal,
Ecruteak/Ghost, Cianwood/Fighting, Olivine/Steel, Mahogany/Ice, Blackthorn/Dragon.
These are **engine-format exterior assets**, not just large concept images.
They are NOT literal HGSS reproductions, interiors, trainer teams, or a finished ROM.

## Included

Each `assets/<city>/` contains:
- `building.png`: indexed 128×112 source image, transparency at index 0.
- `tiles.png`: indexed 128×256 hardware tile atlas (512 tile capacity).
- `tiles.4bpp`: 16,384 bytes, nibble-packed 8×8 GBA tiles, padded safely to the
  full secondary allocation. Between 115 and 139 tiles are used per design.
- `palette.gbapal`: 16 RGB555 colors, 32 bytes; `palette.pal`: editable JASC palette.
- `metatiles.bin`: 56 16×16 metatiles, 8 little-endian tile entries each.
- `metatile_attributes.bin`: 56 Emerald 16-bit behavior/layer attributes.
- `stamp.bin`: 8×7 map stamp with metatile IDs, collision and elevation 3.
- `demo_16x16_map.bin`: an unregistered test layout (General grass plus stamp).
- manifest and binary-roundtrip image.

The package also provides an asset registrar, validation script, preview,
collision preview, build log and precise test report.

## Target and allocations

Inspected Black Ledger `feature/johto-visual-collision-01` at
`512a4d5658973d7d54c531ba8aa62037c67b517a`, pokeemerald-expansion 1.17.2.
Codex may now have newer work. Recover that work before integrating.

- Emerald primary/secondary split: 512/512 8×8 tiles; 512/512 metatiles.
- Each Gym is a separate secondary tileset (`gTileset_BLGymViolet`, etc.).
- Tile base 512, metatile base 512, palette bank 6.
- General primary grass metatile 1 supplies the four ground-plane tile entries.
  This is a dependency on the inspected General primary tileset, not a generic
  guarantee for every primary tileset.
- Each Gym reserves one palette at runtime. The array contains all 16 palette
  slots because this engine indexes secondary palettes at slot 6.
- Static, nonanimated doors: two bottom-center tiles, local `(3,6)` and `(4,6)`.
  Assign reciprocal exterior/interior warps to BOTH to make both halves usable.
  Recommended exterior return position is `(3,7)` relative to stamp origin.
- Roof rows 0–4 use NORMAL layers (art above player); facade rows 5–6 use
  COVERED layers (art behind player). Ground-footprint collision blocks row 5,
  columns 1–6, and row 6 columns 1–2/5–6. Other cells allow walking underneath
  the roof overhang or around the building. Door cells are passable and use
  `MB_NON_ANIMATED_DOOR` (0x60). This is a deliberately simple starting stencil;
  test actual movement after placement, especially diagonal-looking roof edges.

## Why this is not a blind replacement ZIP

The inspected shared WesternCity secondary tileset already has 490 of 512
metatiles and a full-sized tile atlas. Adding all eight designs to that one
sheet would exceed the engine allocation. **Do not overwrite WesternCity or
change a whole city's secondary tileset to one of these without remapping its
existing secondary metatiles.** That would corrupt unrelated buildings/terrain.

The safe integration choices are:
1. Import the Gym into a city-specific secondary tileset, preserving/repacking
   only that city's required art. Allocate/remap its tiles, palette and metatiles,
   update the city's generator, and verify all other map content.
2. Use a dedicated exterior approach map with General primary and the relevant
   BLGym secondary, if that layout choice is acceptable to the owner. Do not add
   such a map merely to avoid finishing faithful city integration.

The first choice is recommended for the ongoing HGSS city rebuild. Your current
map task can allocate these assets as it rebuilds each city. The included fixed
IDs are relocation defaults, not permission to overwrite occupied slots.

## Register assets without changing maps

Run with Python 3 (installer itself has no third-party dependencies):

```
python3 install_assets.py /path/to/Project-crossroads
python3 install_assets.py /path/to/Project-crossroads --apply
```

The first command is a dry run. The second copies only these new assets and
appends delimited registrations to graphics/metatiles/headers and tilesets.h.
It refuses altered existing assets, changed registration blocks and conflicting
symbols. Repeating the exact install is idempotent. It does NOT assign tilesets,
place buildings, edit map IDs, add warps, grant flags or alter saves.

Run `python3 validate.py` (Pillow required) to repeat asset checks.
The code is source; inspect the dry-run and Git diff before applying it to an
actively edited project. Integrate in the current feature branch, not an old
snapshot. Preserve all accepted work and original map/warp IDs.

## Placement / completion checklist for Codex

1. Recover current repo state. Read project instructions. Back up owner saves.
2. Reserve/remap graphics within tile, palette and metatile limits, never by
   increasing engine constants or deleting accepted assets silently.
3. Place the 8×7 structure, respecting the actual city's layout. Replace the old
   placeholder fully, including any large decorative object-event building.
4. Keep a clear approach south of both doorway cells. Add reciprocal warps to
   the intended existing Gym interior, verify return coordinates. Update map
   source generators so a rebuild cannot restore the old placeholder.
5. Walk all four sides, behind roofs, in front of facade, through both doors,
   and around adjacent trees/buildings. Check roof priority and solid wall
   blocking at day/night. Do not claim a mathematical stencil is a playtest.
6. Test all eight, save/Continue, whiteout destination, and other city buildings.
7. Provide native-resolution in-game screenshots and an identifiable ROM build.

## Verification status

**Passed:** all eight indexed PNG/4bpp round trips, palette sizes, pixel indices,
metatile references, layer flags, collision stencil and doorway metadata,
reconstruction of rendered pixels from binary, installer dry-run/apply/idempotence
in an isolated clone, existing opening and Olivine validators and layout check.

**Blocked:** full ROM build. This machine lacks ARM GCC and libpng development
headers (`arm-none-eabi-gcc` and `png.h`). See `build_attempt.log`.

**Not performed:** real game placement, emulator traversal, full city tileset
repacking, or owner visual acceptance. No live project or remote branch changed.

The eight designs are delivered in real engine data formats. Calling the entire
integration complete would be inaccurate until the placement/build checks above
are done.
