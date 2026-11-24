#!/usr/bin/env python3
"""Controller test of the Ruins of Alph second/hidden-room prototype.

Disclosed RAM fixtures only: one Water Stone placed in the Items pocket, and the
first party Pokemon re-encoded as Ho-Oh (then as an egg Ho-Oh). Gates are opened
through the real Bag UI and the real chamber interaction, never by writing
metatiles, warps or flags. Uses a copied battery; never writes the input save.
"""
import argparse, hashlib, json, runpy, shutil, struct, sys
from pathlib import Path

R = Path.cwd()
p = argparse.ArgumentParser()
p.add_argument('--save', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--library', default='/tmp/johto-bridge.so')
a = p.parse_args()
out = a.output.resolve(); out.mkdir(parents=True, exist_ok=True)
sha = lambda b: hashlib.sha256(b).hexdigest()
rom_sha = sha((R / 'pokeemerald.gba').read_bytes()); save_sha = sha(a.save.read_bytes())
trial = out / 'input-copy.sav'; shutil.copyfile(a.save, trial)
sys.path.insert(0, str(R / 'crossroads/tools'))
sys.argv = ['johto_network_smoke.py', '--save', str(trial), '--library', a.library, '--output', str(out / 'network'), '--targets', '']
d = runpy.run_path(str(R / 'crossroads/tools/johto_network_smoke.py'))
go, walk, read, write, frames, key, current, pos, close, lib, syms, sb = [d[n] for n in
    ('go', 'walk', 'read', 'write', 'frames', 'key', 'current', 'pos', 'close', 'lib', 'syms', 'sb')]
write('sWildEncountersDisabled', 1, 1)
UP, DOWN, LEFT, RIGHT, A, B, START = 64, 128, 32, 16, 1, 2, 8
WATER_STONE, HO_OH, OPEN_TILE, POCKETS = 212, 250, 40, 5
report = {'rom_sha256': rom_sha, 'cases': [], 'fixtures': [
    'Water Stone inserted into Items pocket slot in test RAM',
    'Party slot 0 re-encoded as Ho-Oh, then as egg Ho-Oh, in test RAM',
    'Wild encounters disabled in test RAM; Survey access through its real desk interaction']}

def record(**kw):
    report['cases'].append(kw); print('PASS', kw, flush=True)
    (out / 'coverage-in-progress.json').write_text(json.dumps(report, indent=2) + '\n')

def image(name): assert lib.emu_image(str(out / (name + '.png')).encode())

def overworld(): return read(syms['gMain'] + 4) == syms['CB2_Overworld'] | 1

def metatile(x, y):
    layout = syms['gBackupMapLayout']; width = read(layout, 4); grid = read(layout + 8, 4)
    return read(grid + ((y + 7) * width + (x + 7)) * 2, 2) & 0x3ff

def step(k, n=1):
    for _ in range(n): frames(16, k); frames(24)

def face(k): frames(1, k); frames(20)

# --- Bag fixture -----------------------------------------------------------
def enc_key(): return read(read('gSaveBlock2Ptr') + 0xac, 4) & 0xffff

def items_slots():
    base = read('gBagPockets', 4)
    return [(read(base + i * 4, 2), read(base + i * 4 + 2, 2) ^ enc_key()) for i in range(30)], base

def water_stones():
    slots, _ = items_slots(); return sum(q for i, q in slots if i == WATER_STONE)

def give_water_stone():
    slots, base = items_slots()
    if any(i == WATER_STONE for i, _ in slots): return
    empty = next(n for n, (i, _) in enumerate(slots) if i == 0)
    if slots[0][0]:  # keep the stone at the top so the Bag cursor starts on it
        write(base + empty * 4, slots[0][0], 2); write(base + empty * 4 + 2, slots[0][1] ^ enc_key(), 2)
    write(base, WATER_STONE, 2); write(base + 2, 1 ^ enc_key(), 2)

def use_top_item():
    pos_ = syms['gBagPosition']; write(pos_ + 5, 0, 1)
    # cursorPosition[0] at +8 and scrollPosition[0] after POCKETS_COUNT u16s.
    write(pos_ + 8, 0, 2); write(pos_ + 8 + 2 * POCKETS, 0, 2)
    key(START); frames(60)
    for _ in range(12):
        c = read('sStartMenuCursorPos', 1)
        if read(syms['sCurrentStartMenuActions'] + c, 1) == 2: break
        key(DOWN)
    else: raise AssertionError('Bag not in start menu')
    key(A); frames(120)
    image('bag-open')
    key(A); frames(40); image('bag-context'); key(A); frames(240)

# --- Party fixture ---------------------------------------------------------
ORDER0 = [0,0,0,0,0,0,1,1,2,3,2,3,1,1,2,3,2,3,1,1,2,3,2,3]
ORDER3 = [3,2,3,2,1,1,3,2,3,2,1,1,3,2,3,2,1,1,0,0,0,0,0,0]
def set_party0(species=None, egg=None):
    mon = read('gPlayerPartyPtr', 4); pers = read(mon); cipher = pers ^ read(mon + 4)
    sec = bytearray().join(struct.pack('<I', read(mon + 32 + i * 4) ^ cipher) for i in range(12))
    g = ORDER0[pers % 24] * 12; m = ORDER3[pers % 24] * 12
    if species is not None:
        w = struct.unpack_from('<H', sec, g)[0]; struct.pack_into('<H', sec, g, (w & ~0x7ff) | species)
    if egg is not None:
        w = struct.unpack_from('<I', sec, m + 4)[0]; w = (w | 1 << 30) if egg else (w & ~(1 << 30))
        struct.pack_into('<I', sec, m + 4, w)
        hdr = read(mon + 19, 1); write(mon + 19, (hdr | 4) if egg else (hdr & ~4), 1)
    write(mon + 28, sum(struct.unpack('<24H', sec)) & 0xffff, 2)
    for i in range(12): write(mon + 32 + i * 4, struct.unpack_from('<I', sec, i * 4)[0] ^ cipher)

def party_state():
    mon = read('gPlayerPartyPtr', 4); return bytes(read(mon + i, 1) for i in range(100))

def at_gate(chamber):
    go(chamber); walk((5, 2)); face(UP); assert pos() == (5, 2)

def assert_closed(chamber, label):
    assert current() == chamber and metatile(5, 1) != OPEN_TILE, (label, metatile(5, 1))
    face(UP); step(UP); assert current() == chamber and pos() == (5, 2), (label, 'walked through a closed wall', pos())

def read_sign(label):
    key(A); frames(90); image(label); close(); assert not read('sLockFieldControls', 1)

def enter_open_gate(chamber, second, label):
    assert metatile(5, 1) == OPEN_TILE, (label, 'wall did not open', metatile(5, 1)); image(label + '-open')
    step(UP); frames(180)
    assert current() == second and pos() == (6, 17), (label, 'open wall did not enter second room', current(), pos())
    image(label + '-second-room')

def leave_second(chamber, label):
    d['warp'](0); frames(60)
    assert current() == chamber and pos() == (5, 2), (label, 'second-room exit', current(), pos())
    assert_closed(chamber, label + ' reclosed after reload')

def fall_through(second, hidden, hidden_arrival, hidden_fall, hall_arrival, label):
    walk((6, 4)); step(UP); frames(240)
    assert current() == hidden and pos() == hidden_arrival, (label, 'second-room fall', current(), pos())
    image(label + '-hidden-room')
    fx, fy = hidden_fall; walk((fx - 1, fy)); step(RIGHT); frames(240)
    assert current() == 'RuinsOfAlph_UndergroundHall' and pos() == hall_arrival, (label, 'hidden-room fall', current(), pos())
    image(label + '-hall-arrival')

SW, NW = 'RuinsOfAlph_SouthwestChamber', 'RuinsOfAlph_NorthwestChamber'

# Southwest: Water Stone gate.
at_gate(SW); assert_closed(SW, 'SW without stone'); read_sign('sw-sign-closed'); assert_closed(SW, 'SW after sign')
record(kind='gate_closed', map=SW, condition='no Water Stone used')
give_water_stone(); assert water_stones() == 1
# Wrong position: the stone must take its normal party-menu route, not the gate.
walk((5, 3)); face(UP); use_top_item(); image('sw-wrong-tile')
assert not overworld(), 'Water Stone at the wrong tile should open the normal party menu'
for _ in range(4): key(B); frames(90)
for _ in range(6):
    if overworld(): break
    key(B); frames(120)
assert overworld() and current() == SW and metatile(5, 1) != OPEN_TILE and water_stones() == 1
record(kind='gate_wrong_tile', map=SW, position=[5, 3], party_menu=True, wall_open=False)
walk((5, 2)); face(UP); use_top_item(); frames(60)
assert overworld() and water_stones() == 1, ('Water Stone consumed or field not restored', water_stones())
enter_open_gate(SW, 'RuinsOfAlph_SouthwestSecondRoom', 'sw')
record(kind='gate_open_enter', map=SW, condition='Water Stone used facing north at (5,2)', stone_kept=True)
leave_second(SW, 'sw'); record(kind='second_room_return_recloses', map=SW, arrival=[5, 2])
walk((5, 2)); face(UP); use_top_item(); frames(60); enter_open_gate(SW, 'RuinsOfAlph_SouthwestSecondRoom', 'sw2')
fall_through('RuinsOfAlph_SouthwestSecondRoom', 'RuinsOfAlph_SouthwestHiddenRoom', (11, 7), (20, 13), (5, 42), 'sw')
record(kind='falls', second='RuinsOfAlph_SouthwestSecondRoom', hidden_arrival=[11, 7], hall_arrival=[5, 42])

# Northwest: Ho-Oh party gate.
original_party = party_state()
at_gate(NW); assert_closed(NW, 'NW no Ho-Oh'); read_sign('nw-sign-closed'); assert_closed(NW, 'NW after sign')
record(kind='gate_closed', map=NW, condition='no Ho-Oh in party')
set_party0(species=HO_OH, egg=True); face(UP); read_sign('nw-egg-closed'); assert_closed(NW, 'NW egg Ho-Oh')
record(kind='gate_closed', map=NW, condition='egg Ho-Oh only')
set_party0(egg=False); face(UP); key(A); frames(120)
enter_open_gate(NW, 'RuinsOfAlph_NorthwestSecondRoom', 'nw')
record(kind='gate_open_enter', map=NW, condition='non-egg Ho-Oh in party')
leave_second(NW, 'nw'); record(kind='second_room_return_recloses', map=NW, arrival=[5, 2])
walk((5, 2)); face(UP); key(A); frames(120); enter_open_gate(NW, 'RuinsOfAlph_NorthwestSecondRoom', 'nw2')
fall_through('RuinsOfAlph_NorthwestSecondRoom', 'RuinsOfAlph_NorthwestHiddenRoom', (11, 14), (20, 21), (5, 24), 'nw')
record(kind='falls', second='RuinsOfAlph_NorthwestSecondRoom', hidden_arrival=[11, 14], hall_arrival=[5, 24])

assert sha(a.save.read_bytes()) == save_sha and sha((R / 'pokeemerald.gba').read_bytes()) == rom_sha
report['result'] = 'PASS'; (out / 'coverage.json').write_text(json.dumps(report, indent=2) + '\n')
print('Ruins hidden-room controller cases PASS', flush=True)
