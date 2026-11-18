#!/usr/bin/env python3
"""Normal-controller Route 33 pavement visibility and tree collision check.

Requires a matching built ROM/ELF, mGBA bridge and a disposable old battery.
The survey desk is used in game, and random encounters are suppressed only in
the running emulator. Outputs contain a copied battery and snapshots: keep
them private. Use --expect occluded to reproduce the released defect, and
--expect visible on the corrected candidate. Screenshots are native 240x160.
"""
import argparse
import hashlib
import json
import runpy
import shutil
import subprocess
import sys
from pathlib import Path
from PIL import Image

R = Path(__file__).resolve().parents[2]
p = argparse.ArgumentParser()
p.add_argument('--save', type=Path, required=True)
p.add_argument('--library', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--rom-sha256', required=True)
p.add_argument('--expect', choices=('visible', 'occluded'), required=True)
a = p.parse_args()
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
assert digest(R / 'pokeemerald.gba') == a.rom_sha256, 'Wrong ROM'
source_hash = digest(a.save)
a.output.mkdir(parents=True, exist_ok=True)
copy = a.output / 'input-copy.sav'
assert copy.resolve() != a.save.resolve()
shutil.copyfile(a.save, copy)
sys.path.insert(0, str(R / 'crossroads/tools'))
sys.argv = ['johto_network_smoke.py', '--save', str(copy), '--library', str(a.library), '--output', str(a.output / 'tour'), '--targets', '']
d = runpy.run_path(str(R / 'crossroads/tools/johto_network_smoke.py'))
go, walk, read, frames, pos, current, lib, syms = (d[n] for n in ('go', 'walk', 'read', 'frames', 'pos', 'current', 'lib', 'syms'))
go('JohtoRoute33')

def visible_pixels(path):
    """Count player sprite's opaque pixels visible in the actual framebuffer."""
    frame = Image.open(path).convert('RGB')
    assert frame.size == (240, 160)
    sprite = syms['gSprites'] + read(syms['gPlayerAvatar'] + 4, 1) * 68
    tile, palette = read(sprite + 4, 2) & 1023, read(sprite + 4, 2) >> 12
    found = []
    for i in range(128):
        address = 0x07000000 + i * 8
        v0, v1, v2 = read(address, 2), read(address + 2, 2), read(address + 4, 2)
        if v2 & 1023 == tile and v2 >> 12 == palette and not v0 & 0x300:
            found.append((v0, v1))
    assert len(found) == 1, ('player OAM', found)
    v0, v1 = found[0]
    assert not v0 & 0x2c00
    dims = [[(8,8),(16,16),(32,32),(64,64)], [(16,8),(32,8),(32,16),(64,32)], [(8,16),(8,32),(16,32),(32,64)]]
    width, height = dims[v0 >> 14][v1 >> 14]
    x0, y0 = v1 & 511, v0 & 255
    x0 = x0 - 512 if x0 >= 256 else x0
    y0 = y0 - 256 if y0 >= 160 else y0
    assert 0 <= x0 <= 240-width and 0 <= y0 <= 160-height
    colors = []
    for i in range(16):
        v = read(0x05000200 + palette * 32 + i * 2, 2)
        colors.append(tuple(((v >> s) & 31) << 3 | ((v >> s) & 31) >> 2 for s in (0, 5, 10)))
    stride = width // 8 if read(0x04000000, 2) & 64 else 32
    expected = visible = 0
    for y in range(height):
        for x in range(width):
            X = width-1-x if v1 & 0x1000 else x
            Y = height-1-y if v1 & 0x2000 else y
            index = tile + (Y // 8) * stride + X // 8
            b = read(0x06010000 + index * 32 + (Y % 8) * 4 + (X % 8) // 2, 1)
            color = (b >> (4 * (X % 2))) & 15
            if color:
                expected += 1
                visible += frame.getpixel((x0+x, y0+y)) == colors[color]
    assert expected > 0
    return visible, expected

results = []
for row in (15, 16, 17):
    walk((7, row))
    assert current() == 'JohtoRoute33' and pos() == (7, row)
    samples = []
    for i in range(30):
        frames(2)
        f = a.output / f'pavement-{row}-{i:02}.png'
        assert lib.emu_image(str(f).encode())
        samples.append((*visible_pixels(f), str(f.name)))
    # Rain may mask isolated pixels for a frame; require a fully visible sample
    # for the fix, or persistent substantial obstruction for reproduction.
    best = max(samples, key=lambda sample: sample[0] / sample[1])
    if a.expect == 'visible':
        assert best[0] == best[1], ('pavement hides player', row, best)
    else:
        assert best[0] * 4 < best[1] * 3, ('expected persistent obstruction', row, best)
    results.append(dict(case='pavement_visibility', position=[7,row], visible=best[0], expected=best[1], screenshot=best[2]))

# Cross the centre of the transition from all four adjacent walkable cells.
# Retain actual walking frames so the owner can inspect foreground order during
# movement as well as the stationary samples above. The optional MP4 is made
# only when ffmpeg is installed; the original native frames remain available.
movement_frames = a.output / 'transition-walk-frames'
movement_frames.mkdir(exist_ok=True)
original_frames = walk.__globals__['frames']
frame_number = 0
def recorded_frames(n=60, k=0):
    global frame_number
    while n:
        step = min(n, 4)
        original_frames(step, k)
        n -= step
        assert lib.emu_image(str(movement_frames / f'{frame_number:04}.png').encode())
        frame_number += 1
for approach in ((6,16), (8,16), (7,15), (7,17)):
    walk(approach)
    walk.__globals__['frames'] = recorded_frames
    try:
        walk((7,16))
    finally:
        walk.__globals__['frames'] = original_frames
    assert pos() == (7,16), ('paving approach failed', approach, pos())
    results.append(dict(case='pavement_approach', approach=list(approach), arrival=[7,16]))
if shutil.which('ffmpeg'):
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(movement_frames/'%04d.png'),'-pix_fmt','yuv420p',str(a.output/'transition-walk.mp4')], check=True)

# Apricorn trees are object events, not solid trunk tiles. Push into every
# reachable side of each separately and verify ordinary controller movement is
# blocked. Do not demand the same sprite foreground order as paving: canopy
# overlap can be intentional, depending on which side of the tree Joe stands.
for event in d['maps']['JohtoRoute33']['object_events']:
    if 'APRICORN' not in event['graphics_id']:
        continue
    x, y = event['x'], event['y']
    attempts = []
    for dx,dy,key in ((0,-1,128),(0,1,64),(-1,0,16),(1,0,32)):
        target = (x+dx, y+dy)
        if not d['safe']('JohtoRoute33', target) or d['path']('JohtoRoute33', target) is None:
            continue
        walk(target)
        frames(32, key)
        frames(30)
        assert pos() == target, ('walked through Apricorn tree', event['graphics_id'], target, pos())
        f = a.output / f"tree-{x}-{y}-from-{dx}-{dy}.png"
        assert lib.emu_image(str(f).encode())
        attempts.append([dx,dy])
    assert attempts, ('tree has no reachable side', event['graphics_id'])
    results.append(dict(case='tree_collision', tree=[x,y], accessible_sides=attempts))

assert digest(a.save) == source_hash, 'Input battery changed'
(a.output / 'results.json').write_text(json.dumps(dict(rom_sha256=a.rom_sha256, expectation=a.expect, cases=results), indent=2)+'\n')
print('PASS Route 33 pavement visibility and accessible Apricorn sides:', len(results), 'cases', flush=True)
