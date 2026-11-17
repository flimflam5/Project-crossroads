#!/usr/bin/env python3
"""Compare built kiln metatiles and live VRAM tiles to authored source.

Cold Continue uses a copy of a genuine old Azalea save. This test checks actual
compiled graphics and metatile attributes, not visual quality or player movement.
The ROM, ELF and map/source files must all come from the same candidate.
"""
import argparse
import ctypes as C
import hashlib
import json
from pathlib import Path
import subprocess

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--save', type=Path, required=True)
parser.add_argument('--rom-sha256', required=True)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--library', type=Path, default=Path('/tmp/johto-bridge.so'))
args = parser.parse_args()
rom = (ROOT / 'pokeemerald.gba').read_bytes()
assert hashlib.sha256(rom).hexdigest() == args.rom_sha256, 'Wrong candidate ROM'
symbols = {}
for line in subprocess.check_output(['arm-none-eabi-nm', '-an', str(ROOT / 'pokeemerald.elf')], text=True).splitlines():
    fields = line.split()
    if len(fields) == 3:
        try:
            symbols[fields[2]] = int(fields[0], 16)
        except ValueError:
            pass

plan = json.loads((ROOT / 'crossroads/art/eight_gyms_v1/integration.json').read_text())['cities']['AzaleaTown']['kiln']
tileset = ROOT / 'data/tilesets/secondary/bl_gym_azalea'
metatiles = (tileset / 'metatiles.bin').read_bytes()
attributes = (tileset / 'metatile_attributes.bin').read_bytes()
for metatile in plan['metatile_ids']:
    index = metatile - 512
    for symbol, authored, width in [('gMetatiles_BlGymAzaleaSecondary', metatiles, 16),
                                    ('gMetatileAttributes_BlGymAzaleaSecondary', attributes, 2)]:
        offset = symbols[symbol] - 0x08000000 + index * width
        assert rom[offset:offset + width] == authored[index * width:(index + 1) * width], (symbol, metatile)

save_before = hashlib.sha256(args.save.read_bytes()).hexdigest()
lib = C.CDLL(str(args.library.resolve()))
for name, types in [('emu_init', [C.c_char_p]), ('emu_save', [C.c_char_p, C.c_int]),
                    ('emu_frames', [C.c_int, C.c_int]), ('emu_read', [C.c_uint, C.c_int])]:
    getattr(lib, name).argtypes = types
lib.emu_read.restype = C.c_uint
assert lib.emu_init(str(ROOT / 'pokeemerald.gba').encode())
assert lib.emu_save(str(args.save.resolve()).encode(), 1)
def frames(count, keys=0):
    lib.emu_frames(keys, count)
def read(address, width=4):
    return lib.emu_read(address, width)
frames(4500)
assert read(symbols['gMain'] + 4) == symbols['CB2_BlackLedgerTitle'] | 1
frames(1, 8); frames(200); frames(1, 1); frames(300)
assert read(symbols['gMain'] + 4) == symbols['CB2_Overworld'] | 1
saveblock = read(symbols['gSaveBlock1Ptr'])
groups = json.loads((ROOT / 'data/maps/map_groups.json').read_text())
assert (read(saveblock + 4, 1), read(saveblock + 5, 1)) == (75, groups['gMapGroup_CrossroadsOlivine'].index('AzaleaTown'))

sheets = [Image.open(ROOT / 'data/tilesets/primary/bl_gym_azalea/tiles.png'), Image.open(tileset / 'tiles.png')]
checked = sorted(set(plan['tile_mapping'].values()))
for tile in checked:
    index = tile % 512
    sheet = sheets[tile // 512]
    pixels = sheet.crop((index % 16 * 8, index // 16 * 8, (index % 16 + 1) * 8, (index // 16 + 1) * 8)).tobytes()
    assert len(pixels) == 64 and max(pixels) < 16
    expected = bytes(pixels[i] | (pixels[i + 1] << 4) for i in range(0, 64, 2))
    actual = bytes(read(0x06000000 + tile * 32 + i, 1) for i in range(32))
    assert actual == expected, ('Stale or overwritten VRAM tile', tile)
assert hashlib.sha256(args.save.read_bytes()).hexdigest() == save_before, 'Source save changed'
args.output.parent.mkdir(parents=True, exist_ok=True)
args.output.write_text(json.dumps({'rom_sha256': args.rom_sha256, 'metatiles_checked': len(plan['metatile_ids']),
                                   'vram_tiles_checked': len(checked), 'result': 'PASS',
                                   'scope': 'Cold Continue of copied Azalea save; compiled metatile bytes/attributes and live facade tile VRAM. Palette and visual checks are separate.'}, indent=2) + '\n')
print(f'Kiln compiled metatiles and live VRAM: PASS ({len(plan["metatile_ids"])} metatiles, {len(checked)} tiles).')
