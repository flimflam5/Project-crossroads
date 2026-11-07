#!/usr/bin/env python3
"""Optional runtime smoke checks. Requires libmgba-dev, host C compiler and ARM nm.

Uses debugger RAM setup to skip the unmodified Emerald introduction, then sends
controller input through real scripts/doors. Never modifies the ROM. Test snapshots
and screenshots go into ignored build output. Not a substitute for owner playtesting.
"""
import argparse
import ctypes as C
import subprocess
import shutil
import json
from pathlib import Path
root = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description='Debugger-assisted Olivine smoke test, not an opening playthrough.')
parser.add_argument('--rom', type=Path, default=root / 'pokeemerald.gba')
parser.add_argument('--output', type=Path, default=root / 'build/emulator-smoke')
parser.add_argument('--library', type=Path, help='optional prebuilt mgba_bridge shared library')
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
bridge = args.library or args.output / 'mgba_bridge.so'
if not args.library:
    subprocess.run(['cc', '-shared', '-fPIC', str(root / 'crossroads/tools/mgba_bridge.c'), '-lmgba', '-o', str(bridge)], check=True)
lib = C.CDLL(str(bridge.resolve()))
lib.emu_init.argtypes = [C.c_char_p]
lib.emu_init.restype = C.c_int
lib.emu_frames.argtypes = [C.c_int, C.c_int]
lib.emu_read.argtypes = [C.c_uint, C.c_int]
lib.emu_read.restype = C.c_uint
lib.emu_write.argtypes = [C.c_uint, C.c_uint, C.c_int]
lib.emu_state.argtypes = [C.c_char_p, C.c_int]
lib.emu_state.restype = C.c_int
lib.emu_image.argtypes = [C.c_char_p]
lib.emu_image.restype = C.c_int
rom = str(args.rom.resolve())
state = str(args.output / 'choice.snapshot')
syms = {}
for line in subprocess.check_output([shutil.which('arm-none-eabi-nm') or 'arm-none-eabi-nm', '-an', str(Path(rom).with_suffix('.elf'))], text=True).splitlines():
    a = line.split()
    if len(a) == 3:
        try:
            syms[a[2]] = int(a[0], 16)
        except ValueError:
            pass
assert lib.emu_init(rom.encode())

def read(a, w=4):
    return lib.emu_read(syms.get(a, a), w)

def write(a, v, w=4):
    lib.emu_write(syms.get(a, a), syms.get(v, v), w)

def frames(n=60, k=0):
    lib.emu_frames(k, n)

def key(k, n=1):
    frames(n, k)
    frames(20)

def script(name):
    """Initialize the existing script context in RAM, using this engine ABI."""
    a = syms['sGlobalScriptContext']
    for i in range(116):
        write(a + i, 0, 1)
    write(a + 1, 1, 1)
    write(a + 8, syms[name])
    write(a + 92, syms['gScriptCmdTable'])
    write(a + 96, syms['gScriptCmdTableEnd'])
    write('sLockFieldControls', 1, 1)
    write('sGlobalScriptContextStatus', 0, 1)
# Debugger-assisted fresh-game setup; the Emerald opening is not playtested.
frames(400)
write(syms['gMain'] + 1080, 0, 1)
write(syms['gMain'] + 4, syms['CB2_NewGame'] | 1)
frames(300)
# Supply the valid name normally entered in the skipped naming screen.
sb2 = read('gSaveBlock2Ptr')
for i, v in enumerate([196, 201, 191, 255, 255, 255, 255, 255]):
    write(sb2 + i, v, 1)
script('Olivine_OfferVisit')
frames(120)
for _ in range(4):
    key(1)
    frames(90)
frames(180)
assert read(syms['gMain'] + 4) == syms['CB2_Overworld'] | 1
assert read(read('gSaveBlock1Ptr') + 4, 1) == 75
assert lib.emu_image(str(args.output / 'city.png').encode())
import struct
from collections import deque
city = json.load(open(root / 'data/maps/OlivineCity/map.json'))
tiles = struct.unpack('<2304H', (root / 'data/layouts/OlivineCity/map.bin').read_bytes())
blocked = {(o['x'], o['y']) for o in city['object_events']}

def pos():
    sb = read('gSaveBlock1Ptr')
    return (read(sb, 2), read(sb + 2, 2))

def direction(a, b):
    return 16 if b[0] > a[0] else 32 if b[0] < a[0] else 128 if b[1] > a[1] else 64

def walk(target):
    """Navigate with controller input; verify every actual in-game step."""
    start = pos()
    q = deque([start])
    prev = {start: None}
    while q:
        p = q.popleft()
        if p == target:
            break
        for n in [(p[0] + 1, p[1]), (p[0] - 1, p[1]), (p[0], p[1] + 1), (p[0], p[1] - 1)]:
            x, y = n
            if n in prev or n in blocked or (not 0 <= x < 48) or (not 0 <= y < 48):
                continue
            t = tiles[y * 48 + x]
            if t & 3072 or t >> 12 != 3:
                continue
            prev[n] = p
            q.append(n)
    assert target in prev
    path = []
    p = target
    while prev[p] is not None:
        path.append(p)
        p = prev[p]
    for n in reversed(path):
        old = pos()
        k = direction(old, n)
        frames(16, k)
        frames(20)
        if pos() == old:
            frames(16, k)
            frames(20)
        assert pos() == n, (old, n, pos())
for i, w in enumerate(city['warp_events']):
    walk((w['x'], w['y'] + 1))
    frames(16, 64)
    frames(180)
    sb = read('gSaveBlock1Ptr')
    assert read(sb + 4, 1) == 75 and read(sb + 5, 1) == i + 1, (i, pos(), read(sb + 5, 1))
    assert read(syms['gMain'] + 4) == syms['CB2_Overworld'] | 1
    print('Entered', w['dest_map'], flush=True)
    assert lib.emu_image(str(args.output / f'interior-{i}.png').encode())
    frames(16, 128)
    frames(180)
    sb = read('gSaveBlock1Ptr')
    assert read(sb + 4, 1) == 75 and read(sb + 5, 1) == 0, (i, pos(), read(sb + 5, 1))
    print('Returned from', w['dest_map'], flush=True)
walk((20, 42))
walk((29, 42))
print('Both piers reached on foot', flush=True)
script('Olivine_ReturnToAlpha')
frames(120)
for _ in range(4):
    key(1)
    frames(90)
frames(180)
assert read(read('gSaveBlock1Ptr') + 4, 1) == 1
for _ in range(2):
    frames(16, 32)
    frames(20)
frames(1, 64)
frames(20)
key(1)
frames(120)
for _ in range(2):
    key(1)
    frames(120)
assert lib.emu_state(state.encode(), 0)
for choice, species in ((1, 605), (2, 273), (3, 568)):
    assert lib.emu_state(state.encode(), 1)
    for _ in range(choice - 1):
        key(128)
        key(1)
        frames(120)
    key(1)
    frames(180)
    for _ in range(2):
        key(1)
        frames(90)
    for _ in range(8):
        key(2)
        frames(90)
    p = read('gPlayerPartyPtr')
    offset = [0, 0, 0, 0, 0, 0, 1, 1, 2, 3, 2, 3, 1, 1, 2, 3, 2, 3, 1, 1, 2, 3, 2, 3][read(p) % 24]
    actual = (read(p + 32 + 12 * offset) ^ read(p) ^ read(p + 4)) & 2047
    assert actual == species and read(p + 84, 1) == 5
    for _ in range(8):
        key(1)
        frames(100)
    for _ in range(8):
        key(2)
        frames(90)
    assert read(read('gPlayerPartyCountPtr'), 1) == 1
    assert read(read('gSaveBlock1Ptr') + 5020 + 500, 2) == choice
    for _ in range(2):
        frames(16, 16)
        frames(20)
    frames(1, 64)
    frames(20)
    key(1)
    frames(180)
    for _ in range(24):
        key(1)
        frames(140)
    frames(180)
    sb = read('gSaveBlock1Ptr')
    assert read(sb + 4, 1) == 75 and read(sb + 5, 1) == 0
    assert read(sb + 5020 + 500, 2) == choice and read(read('gPlayerPartyCountPtr'), 1) == 1
    print('Live rescue, duplicate guard and terminal travel passed:', species, flush=True)
walk((11, 22))
frames(16, 64)
frames(180)
for _ in range(4):
    frames(16, 64)
    frames(20)
p = read('gPlayerPartyPtr')
write(p + 86, 1, 2)
key(1)
frames(180)
for _ in range(7):
    key(1)
    frames(180)
for _ in range(5):
    key(2)
    frames(60)
p = read('gPlayerPartyPtr')
assert read(p + 86, 2) == read(p + 88, 2) and read('gFonts') != 0
key(8)
frames(120)
assert lib.emu_image(str(args.output / 'menu-after-healing.png').encode())
print('Nurse healed 1 HP to full and preserved fonts/menu', flush=True)
print('Debugger-assisted runtime smoke checks: PASS. Real save/reload, purchases and owner testing are separate checks.')
