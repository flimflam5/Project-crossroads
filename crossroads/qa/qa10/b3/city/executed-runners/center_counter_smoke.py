#!/usr/bin/env python3
"""Actual front-A proof for all six communication desks, before or after repair."""
import argparse
import hashlib
import json
import runpy
import subprocess
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
p = argparse.ArgumentParser(); p.add_argument('--save', type=Path, required=True)
p.add_argument('--output', type=Path, required=True); p.add_argument('--library', default='/tmp/johto-bridge.so')
p.add_argument('--expect-blocked', action='store_true'); p.add_argument('--rom-sha256', required=True)
a = p.parse_args(); out = a.output; out.mkdir(parents=True, exist_ok=True)
assert hashlib.sha256((R / 'pokeemerald.gba').read_bytes()).hexdigest() == a.rom_sha256
source_hash = hashlib.sha256(a.save.read_bytes()).hexdigest()
sys.argv = ['johto_network_smoke.py', '--save', str(a.save), '--library', a.library, '--output', str(out), '--targets', '']
d = runpy.run_path(str(R / 'crossroads/tools/johto_network_smoke.py'))
go, walk, frames, key, read, current, pos, lib = [d[k] for k in ['go', 'walk', 'frames', 'key', 'read', 'current', 'pos', 'lib']]
records = []
def text(label):
    address = d['syms'][label]; b = bytearray()
    for i in range(512):
        value = read(address + i, 1); b.append(value)
        if value == 255: return bytes(b)
    raise AssertionError(('Unterminated text', label))
for suffix, xs, staff_y in [('PokemonCenter_1F', [2, 6, 11], 2), ('PokemonCenter_B1F', [4, 8, 12], 4)]:
    name = 'OlivineCity_' + suffix; go(name)
    for x in xs:
        point = x, staff_y + 2; walk(point); frames(1, 64); frames(20)
        assert current() == name and pos() == point and not read('sLockFieldControls', 1)
        label = suffix + '-' + str(x); folder = out / (label + '-frames'); folder.mkdir(exist_ok=True)
        for i in range(30):
            frames(4, 1 if i == 0 else 0)
            lib.emu_image(str(folder / f'{i:04}.png').encode())
        locked = bool(read('sLockFieldControls', 1))
        if a.expect_blocked:
            assert not locked, (name, x, 'Before fixture unexpectedly received a message')
        else:
            assert locked, (name, x, 'Front A failed to reach the receptionist across the counter')
            assert text('gStringVar4') == text('Hgss_CommunicationText'), (name, x, 'Wrong displayed message')
        assert current() == name and pos() == point
        lib.emu_image(str(out / (label + '.png')).encode())
        if suffix.endswith('B1F') and x == 4:
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '15', '-i', str(folder / '%04d.png'), '-pix_fmt', 'yuv420p', str(out / (label + '.mp4'))], check=True)
        records.append(dict(map=name, staff=[x, staff_y], player=point, counter=[x, staff_y + 1], message_received=locked,
                            result='BEFORE defect reproduced:frontA receives no message' if a.expect_blocked else 'AFTER actual frontA exact message/control return PASS'))
        print(name, x, 'BEFORE no message reproduced' if a.expect_blocked else 'AFTER exact message PASS', flush=True)
        if locked: d['close'](); assert not read('sLockFieldControls', 1)
assert hashlib.sha256(a.save.read_bytes()).hexdigest() == source_hash
(out / 'results.json').write_text(json.dumps(dict(rom_sha256=a.rom_sha256, source_battery_sha256=source_hash,
    source_battery_unchanged=True, expected_defect_baseline=a.expect_blocked,
    setup='Normal copied battery/title Continue and controller travel; no map/warp/player position writes. Shared harness discloses temporary encounter suppression and survey assistance.', records=records), indent=2) + '\n')
