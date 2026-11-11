#!/usr/bin/env python3
"""Normal copied-save controller collision checks of both source-furnished Marts."""
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
a = p.parse_args(); out = a.output; out.mkdir(parents=True, exist_ok=True)
source_hash = hashlib.sha256(a.save.read_bytes()).hexdigest()
sys.argv = ['johto_network_smoke.py', '--save', str(a.save), '--library', a.library, '--output', str(out), '--targets', '']
d = runpy.run_path(str(R / 'crossroads/tools/johto_network_smoke.py'))
go, walk, frames, key, read, current, pos, lib = [d[k] for k in ['go', 'walk', 'frames', 'key', 'read', 'current', 'pos', 'lib']]
go('OlivineCity_HarborOffice'); walk((1, 6)); frames(1, 64); frames(20); key(1); frames(180); d['close']()
assert read('sJohtoTestAccess', 1) == 0, 'Disable survey through the real desk before furniture trials'
g = walk.__globals__; original_safe = g['safe']
g['safe'] = lambda n, q: original_safe(n, q) and d['raw'][n][q[1] * d['size'][n][0] + q[0]] >> 12 == 3
g['route_cache'].clear()
objects = [('northeast-plant', {(12, 3)}), ('southwest-plant', {(1, 11)}), ('southeast-plant', {(12, 11)}),
           ('east-rack', {(12, 6), (12, 7)}), ('glass-display', {(8, 9), (9, 9), (8, 10), (9, 10)}),
           ('stool-northwest', {(7, 9)}), ('stool-southwest', {(7, 10)}),
           ('stool-northeast', {(10, 9)}), ('stool-southeast', {(10, 10)})]
records = []; skipped = []; movies = []
for name in ['EcruteakCity_Mart', 'OlivineCity_Mart']:
    go(name); assert not read('gPlayerAvatar', 1) & 8
    w, h = d['size'][name]; raw = d['raw'][name]; warps = d['active_warps'](name)
    actors = {(o['x'], o['y']) for o in d['maps'][name]['object_events']}; covered = set(); recorded = set()
    for label, bases in objects:
        for x, y in sorted(bases):
            assert raw[y * w + x] & 0xc00, (name, label, 'Actual furniture base must block', x, y)
            for dx, dy, button in [(1, 0, 16), (-1, 0, 32), (0, 1, 128), (0, -1, 64)]:
                point = x - dx, y - dy
                if not (0 <= point[0] < w and 0 <= point[1] < h): continue
                if point in warps or point in actors or not g['safe'](name, point): continue
                if d['path'](name, point) is None:
                    skipped.append(dict(map=name, label=label, approach=point, reason='No normal dry route'))
                    continue
                walk(point); assert current() == name and pos() == point
                clip = label in ['northeast-plant', 'stool-northwest'] and label not in recorded
                basename = name + '-' + label
                if clip:
                    folder = out / (basename + '-frames'); folder.mkdir(exist_ok=True)
                    lib.emu_image(str(out / (basename + '-before.png')).encode())
                    for i in range(24):
                        frames(4, button if i < 8 else 0)
                        lib.emu_image(str(folder / f'{i:04}.png').encode())
                    lib.emu_image(str(out / (basename + '.png')).encode())
                    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', '15', '-i', str(folder / '%04d.png'), '-pix_fmt', 'yuv420p', str(out / (basename + '.mp4'))], check=True)
                    movies.append(basename); recorded.add(label)
                else:
                    frames(24, button); frames(30)
                assert current() == name and pos() == point, (name, label, 'Walked into furniture', point, (x, y), current(), pos())
                assert not read('gPlayerAvatar', 1) & 8 and read('sJohtoTestAccess', 1) == 0
                covered.add(label); records.append(dict(map=name, label=label, approach=point, base=[x, y], result='normal controller bump blocked'))
                print(name, label, point, '->', (x, y), 'PASS', flush=True)
    assert covered == {o[0] for o in objects}, (name, 'Missing actual prop coverage', covered)
    lib.emu_image(str(out / (name + '-furnished.png')).encode())
assert hashlib.sha256(a.save.read_bytes()).hexdigest() == source_hash
(out / 'results.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256((R / 'pokeemerald.gba').read_bytes()).hexdigest(),
    source_battery_sha256=source_hash, source_battery_unchanged=True,
    setup='Copied normal battery/cold title Continue; actual public desk disables survey. Normal dry controller travel only. No map/warp/position/progress/party/bag writes; shared harness discloses temporary random-encounter suppression.',
    records=records, skipped_inaccessible_approaches=skipped, recordings=movies), indent=2) + '\n')
print('Both actual common-Marts:all source plant/rack/glass/stool bases controller PASS;', len(records), 'bumps;', len(skipped), 'skips', flush=True)
