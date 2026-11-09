#!/usr/bin/env python3
"""Optional runtime smoke checks. Requires libmgba-dev, host C compiler and ARM nm.

Uses debugger RAM setup to skip the unmodified Emerald introduction, then sends
controller input through real scripts/doors. Never modifies the ROM. Test snapshots
and screenshots go into ignored build output. Not a substitute for owner playtesting.
"""
import argparse
import hashlib
import sys
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
parser.add_argument('--gender', type=int, choices=(0, 1), default=0, help='exercise both existing save gender values')
parser.add_argument('--title-only', action='store_true', help='normal cold boot, native title VRAM, animation, Start/New Game handoff and soft reset')
parser.add_argument('--first-loss-only', action='store_true', help='fresh player practice loss must respawn in Olivine')
parser.add_argument('--battle-resume', type=Path, help='exact-ROM Elgyem fixture for optional practice battle flow tests')
parser.add_argument('--area-resume', type=Path, help='resume the area-only tour from an exact-ROM area-ready.snapshot')
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
if args.title_only:
    # No debugger initialization: run the actual boot/intro/title chain.
    frames(4500)
    assert read(syms['gMain'] + 4) == syms['CB2_BlackLedgerTitle'] | 1
    assets = root / 'graphics/title_screen/black_ledger'
    expected = (assets / 'tiles.bin').read_bytes()
    assert bytes(read(0x06000000 + i, 1) for i in range(len(expected))) == expected
    index = json.loads((assets / 'metadata.json').read_text())['light_palette_index']
    before = read(0x05000000 + index * 2, 2)
    frames(32)
    assert read(0x05000000 + index * 2, 2) != before, 'Harbor light palette must animate'
    assert lib.emu_image(str(args.output / 'title.png').encode())
    key(8)
    frames(180)
    assert read(syms['gMain'] + 4) == syms['CB2_MainMenu'] | 1
    assert lib.emu_image(str(args.output / 'main-menu.png').encode())
    key(1)
    frames(300)
    speech = {value | 1 for name, value in syms.items() if name.startswith('Task_NewGameBirchSpeech')}
    assert any(read(syms['gTasks'] + i * 40 + 4, 1) and read(syms['gTasks'] + i * 40) in speech for i in range(16)), 'New Game must hand off to existing intro'
    assert lib.emu_image(str(args.output / 'new-game-handoff.png').encode())
    frames(3, 15)  # A+B+Start+Select: real in-game soft reset.
    frames(4500)
    assert read(syms['gMain'] + 4) == syms['CB2_BlackLedgerTitle'] | 1
    print('Normal cold boot, exact title VRAM, lighting animation, Start, New Game handoff and soft reset: PASS')
    print('Original Birch introduction is still present; replacement opening and owner title QA remain pending.')
    sys.exit(0)

# Debugger-assisted fresh-game setup; the Emerald opening is not playtested.
frames(400)
write(syms['gMain'] + 1080, 0, 1)
write(read('gSaveBlock2Ptr') + 8, args.gender, 1)
write(syms['gMain'] + 4, syms['CB2_NewGame'] | 1)
frames(300)
# Supply the valid name normally entered in the skipped naming screen.
sb2 = read('gSaveBlock2Ptr')
for i, v in enumerate([196, 201, 191, 255, 255, 255, 255, 255]):
    write(sb2 + i, v, 1)
write('sWildEncountersDisabled', 1, 1)
script('Olivine_OfferVisit')
frames(120)
for _ in range(4):
    key(1)
    frames(90)
frames(180)
assert read(syms['gMain'] + 4) == syms['CB2_Overworld'] | 1
assert read(read('gSaveBlock1Ptr') + 4, 1) == 75
assert lib.emu_image(str(args.output / 'city.png').encode())


def verify_joe():
    obj_id = read(syms['gPlayerAvatar'] + 5, 1)
    obj = syms['gObjectEvents'] + obj_id * 36
    assert read(obj + 4, 2) == 250, 'Actual player must use reserved Joe graphics ID'
    assert read(read('gSaveBlock2Ptr') + 8, 1) == args.gender, 'Never rewrite saved gender'
    sprite_id = read(syms['gPlayerAvatar'] + 4, 1)
    sprite = syms['gSprites'] + sprite_id * 68
    assert read(sprite + 63, 1) & 1 == 0, 'Joe must use authored east art, not hFlip'
    tile = read(sprite + 4, 2) & 1023
    return bytes(read(0x06010000 + tile * 32 + i, 1) for i in range(256))

joe_tiles = (root / 'build/assets/graphics/object_events/pics/people/joe/corporate/walking.png_mwidth_2__mheight_4.4bpp').read_bytes()
for direction, button, base in [('south', 128, 0), ('north', 64, 12), ('west', 32, 4), ('east', 16, 8)]:
    frames(8, button)
    frames(30)
    current = verify_joe()
    matches = [i for i in range(16) if current == joe_tiles[i*256:(i+1)*256]]
    assert lib.emu_image(str(args.output / f'joe-standing-{direction}.png').encode())
    assert any(base <= i < base + 4 for i in matches), (direction, matches)
    assert lib.emu_image(str(args.output / f'joe-standing-{direction}.png').encode())
    print('Joe idle/turn VRAM matches supplied direction:', direction, flush=True)
# Movement is performed later by walk(); collect actual changing walking frames too.
seen_joe_frames = set()
for _ in range(40):
    frames(1, 32)
    seen_joe_frames.add(verify_joe())
frames(30)
assert len(seen_joe_frames) >= 2, 'Walking must animate instead of sliding a static sprite'
verify_joe()
print('Joe walking frames change in VRAM; saved gender preserved', args.gender, flush=True)

import struct
from collections import deque
city = json.load(open(root / 'data/maps/OlivineCity/map.json'))
layouts = {l['id']: l for l in json.loads((root / 'data/layouts/layouts.json').read_text())['layouts']}

def pos():
    sb = read('gSaveBlock1Ptr')
    return (read(sb, 2), read(sb + 2, 2))

def direction(a, b):
    return 16 if b[0] > a[0] else 32 if b[0] < a[0] else 128 if b[1] > a[1] else 64

def walk(target, map_name='OlivineCity'):
    """Navigate with controller input; verify every actual in-game step."""
    current = json.loads((root / f'data/maps/{map_name}/map.json').read_text())
    layout = layouts[current['layout']]
    width, height = layout['width'], layout['height']
    tiles = struct.unpack(f'<{width*height}H', (root / layout['blockdata_filepath']).read_bytes())
    blocked = {(o['x'], o['y']) for o in current['object_events']}
    start = pos()
    blocked.update((e["x"],e["y"]) for e in current["warp_events"] if (e["x"],e["y"]) not in (start,target))
    q = deque([start])
    prev = {start: None}
    while q:
        p = q.popleft()
        if p == target:
            break
        for n in [(p[0] + 1, p[1]), (p[0] - 1, p[1]), (p[0], p[1] + 1), (p[0], p[1] - 1)]:
            x, y = n
            if n in prev or n in blocked or (not 0 <= x < width) or (not 0 <= y < height):
                continue
            t = tiles[y * width + x]
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
map_ids = {json.loads((root/f'data/maps/{n}/map.json').read_text())['id']: i for i,n in enumerate(json.loads((root/'data/maps/map_groups.json').read_text())['gMapGroup_CrossroadsOlivine'])}
if args.first_loss_only:
    script('Crossroads_EventScript_VisitRescueCase')
    frames(180)
    for _ in range(5):key(1);frames(90)
    walk((4,5),'OlivineCity_SilphOffice')
    frames(1,64);frames(20);key(1);frames(120)
    for _ in range(3):key(1);frames(120)
    for _ in range(8):key(2);frames(60)
    assert read(read('gPlayerPartyCountPtr'),1)==1
    script('Olivine_OfferVisit');frames(180)
    for _ in range(4):key(1);frames(90)
    sb=read('gSaveBlock1Ptr')
    assert (read(sb+0x1c,1),read(sb+0x1d,1))==(75,0)
    walk((38,10));frames(16,64);frames(180)
    walk((7,3),'OlivineCity_Gym')
    for _ in range(2):frames(16,64);frames(180)
    walk((6,4),'OlivineCity_Gym_Arena');frames(1,64);frames(20)
    write(read('gPlayerPartyPtr')+86,1,2)
    key(1);frames(180);key(1);frames(120);key(1);frames(300)
    for _ in range(120):
        key(1);frames(120)
        sb=read('gSaveBlock1Ptr')
        if read(sb+4,1)!=75 or read(sb+5,1)!=33:break
    for _ in range(16):
        if not read('sLockFieldControls',1):break
        key(1);frames(120)
    assert (read(sb+4,1),read(sb+5,1))==(75,4), 'First loss must return to local Center'
    p=read('gPlayerPartyPtr')
    assert read(p+86,2)==read(p+88,2)>0
    verify_joe()
    assert lib.emu_image(str(args.output/'first-loss-olivine-center.png').encode())
    print('Fresh player with no prior Center visit: real practice battle loss returns to Olivine Center, heals and preserves Joe/party: PASS')
    sys.exit(0)

if args.battle_resume:
    assert args.battle_resume.with_suffix('.rom.sha256').read_text().strip() == hashlib.sha256(args.rom.read_bytes()).hexdigest()
    assert lib.emu_state(str(args.battle_resume).encode(),1)
    from practice_battle_smoke import run
    run(root,syms,lib,args.output,read,write,frames,key,walk,pos,verify_joe)
    sys.exit(0)

if args.area_resume:
    expected = args.area_resume.with_suffix('.rom.sha256').read_text().strip()
    assert expected == hashlib.sha256(args.rom.read_bytes()).hexdigest(), 'Snapshot belongs to a different ROM'
    assert lib.emu_state(str(args.area_resume).encode(),1)
    from area_completion_smoke import run as run_area_checks
    run_area_checks(root,syms,lib,args.output,read,frames,key,walk,pos,verify_joe)
    sys.exit(0)

for i, w in enumerate(city['warp_events']):
    walk((w['x'], w['y'] + 1))
    frames(16, 64)
    frames(180)
    sb = read('gSaveBlock1Ptr')
    assert read(sb + 4, 1) == 75 and read(sb + 5, 1) == map_ids[w['dest_map']], (i, pos(), read(sb + 5, 1))
    assert read(syms['gMain'] + 4) == syms['CB2_Overworld'] | 1
    verify_joe()
    print('Entered with Joe', w['dest_map'], flush=True)
    assert lib.emu_image(str(args.output / f'interior-{i}.png').encode())
    if i == 0:
        # Rest must also work before the first rescue, without inventing a party.
        walk((0,5), 'OlivineCity_Residence')
        frames(1,64)
        frames(20)
        key(1)
        frames(180)
        key(1)
        frames(600)
        for _ in range(8):
            if read('sLockFieldControls',1)==0:
                break
            key(1)
            frames(90)
        assert read('sLockFieldControls',1)==0
        assert read(read('gPlayerPartyCountPtr'),1)==0
        assert read(read('gSaveBlock1Ptr')+0x139c+500,2)==0
        walk((3,6), 'OlivineCity_Residence')
        frames(16,128)
        frames(20)
        print('Home rest before rescue preserves empty party and unchosen starter: PASS',flush=True)
    frames(16, 128)
    frames(180)
    sb = read('gSaveBlock1Ptr')
    assert read(sb + 4, 1) == 75 and read(sb + 5, 1) == 0, (i, pos(), read(sb + 5, 1))
    verify_joe()
    print('Returned with Joe from', w['dest_map'], flush=True)
walk((20, 42))
walk((29, 42))
print('Both piers reached on foot', flush=True)

# Cross every new seam on foot; inspect all city exits/lobbies and return.
from western_johto_smoke import tour
western = tour(root, syms, lib, args.output, read, frames, key, walk, pos, verify_joe)
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
# The legacy notebook now offers travel, never a grant in Littleroot.
for _ in range(3):
    key(1)
    frames(120)
frames(180)
sb = read('gSaveBlock1Ptr')
assert read(sb + 4, 1) == 75 and read(sb + 5, 1) == 6
assert read(read('gPlayerPartyCountPtr'), 1) == 0
for _ in range(2):
    frames(16, 64)
    frames(20)
frames(1, 16)
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
    sub3 = [3, 2, 3, 2, 1, 1, 3, 2, 3, 2, 1, 1, 3, 2, 3, 2, 1, 1, 0, 0, 0, 0, 0, 0][read(p) % 24]
    origin = read(p + 32 + 12 * sub3) ^ read(p) ^ read(p + 4)
    sections = json.loads((root / 'src/data/region_map/region_map_sections.json').read_text())['map_sections']
    olivine = next(i for i, section in enumerate(sections) if section['id'] == 'MAPSEC_OLIVINE_CITY')
    assert (origin >> 8 & 255) == olivine and (origin >> 16 & 127) == 5
    assert lib.emu_image(str(args.output / f'rescue-{species}.png').encode())
    for _ in range(8):
        key(1)
        frames(100)
    for _ in range(8):
        key(2)
        frames(90)
    assert read(read('gPlayerPartyCountPtr'), 1) == 1
    assert read(read('gSaveBlock1Ptr') + 5020 + 500, 2) == choice
    script('Olivine_ReturnToAlpha')
    frames(120)
    for _ in range(4):
        key(1)
        frames(90)
    frames(180)
    assert read(read('gSaveBlock1Ptr') + 4, 1) == 1
    # Recheck the old notebook with the same saved guard.
    for _ in range(2):
        frames(16, 32)
        frames(20)
    frames(1, 64)
    frames(20)
    key(1)
    frames(120)
    for _ in range(5):
        key(2)
        frames(90)
    assert read(read('gPlayerPartyCountPtr'), 1) == 1
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
    print('Live Olivine met location/level, rescue, duplicate guard and terminal travel passed:', species, flush=True)
    if choice == 1:
        assert lib.emu_state(str(args.output/'elgyem-field.snapshot').encode(),0)
        (args.output/'elgyem-field.rom.sha256').write_text(hashlib.sha256(args.rom.read_bytes()).hexdigest())
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
assert lib.emu_state(str(args.output / 'field-ready.snapshot').encode(), 0)
# Revisit the connected network with a real acquired partner and heal in Ecruteak.
walk((7,7), 'OlivineCity_PokemonCenter_1F')
for _ in range(2):
    frames(16,128)
    frames(180)
    if read(read('gSaveBlock1Ptr')+5,1)==0:
        break
assert read(read('gSaveBlock1Ptr')+5,1)==0
western[0]()
walk((21,35), 'EcruteakCity')
frames(16,64)
frames(180)
assert read(read('gSaveBlock1Ptr')+5,1)==16
walk((7,4), 'EcruteakCity_PokemonCenter_1F')
p=read('gPlayerPartyPtr')
write(p+86,1,2)
frames(1,64)
frames(20)
key(1)
frames(180)
for _ in range(7):
    key(1)
    frames(180)
for _ in range(5):
    key(2)
    frames(60)
p=read('gPlayerPartyPtr')
assert read(p+86,2)==read(p+88,2) and read('gFonts')!=0
sb=read('gSaveBlock1Ptr')
assert (read(sb+0x1c,1),read(sb+0x1d,1))==(75,10)
verify_joe()
assert lib.emu_state(str(args.output/'ecruteak-field-ready.snapshot').encode(),0)
print('Connected return visit with starter: Ecruteak nurse heals 1 HP to full and retains correct respawn/fonts/Joe: PASS',flush=True)
from olivine_detail_smoke import run as run_detail_checks
run_detail_checks(root,syms,lib,args.output,read,write,frames,key,walk,pos,verify_joe,western)
assert lib.emu_state(str(args.output/'area-ready.snapshot').encode(),0)
(args.output/'area-ready.rom.sha256').write_text(hashlib.sha256(args.rom.read_bytes()).hexdigest())
from area_completion_smoke import run as run_area_checks
run_area_checks(root,syms,lib,args.output,read,frames,key,walk,pos,verify_joe)

key(8)
frames(120)
assert lib.emu_image(str(args.output / 'menu-after-healing.png').encode())
print('Nurse healed 1 HP to full and preserved fonts/menu', flush=True)
print('Debugger-assisted runtime smoke checks: PASS. Real save/reload, purchases and owner testing are separate checks.')
