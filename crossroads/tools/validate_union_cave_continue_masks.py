#!/usr/bin/env python3
"""Check Union Cave continue masks against HGSS geometry; not a playtest."""
from collections import deque
import json
from pathlib import Path

R = Path(__file__).resolve().parents[2]
FLOORS = {
    'UnionCave_1F': 'MAP_UNION_CAVE_1F',
    'UnionCave_2F': 'MAP_UNION_CAVE_B1F',
    'UnionCave_3F': 'MAP_UNION_CAVE_B2F',
}
facts = json.loads((R / 'crossroads/hgss/canonical_events/union-cave-geometry.json').read_text())
plan = json.loads((R / 'crossroads/donor/hns-union-cave/hgss-corrected-warp-plan.json').read_text())

for name, ref in FLOORS.items():
    fact = facts[ref]
    cols, rows = fact['matrix_dimensions']
    w, h = cols * 32, rows * 32
    terrain = [None] * (w * h)
    for chunk_index, chunk in enumerate(fact['chunks']):
        ox, oy = chunk_index % cols * 32, chunk_index // cols * 32
        for i, permission in enumerate(chunk['permissions']):
            terrain[(oy + i // 32) * w + ox + i % 32] = permission
    assert None not in terrain
    mask = (R / f'data/layouts/{name}/safe_continue.bin').read_bytes()
    assert len(mask) == w * h
    assert all((m & ~7) == 0 and (not m & 4 or m & 1) and not (m & 1 and m & 2) for m in mask)
    assert sum(bool(m & 4) for m in mask) > 10
    warps = {(e['hgss_x'], e['hgss_y']) for e in plan['warps'] if e['existing_map'] == name}
    assert all(mask[y*w+x] == 0 for x, y in warps), (name, 'warp landing marked safe')
    start = (fact['warps'][0]['x'], fact['warps'][0]['z'])
    queue = deque([start])
    public = {start}
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x-1,y), (x+1,y), (x,y-1), (x,y+1)):
            if not (0 <= nx < w and 0 <= ny < h) or (nx, ny) in public:
                continue
            p = terrain[ny*w+nx]
            if p & 0x8000 or (p & 255) == 0x15:
                continue
            public.add((nx,ny))
            queue.append((nx,ny))
    for i, bits in enumerate(mask):
        p = terrain[i]
        if bits & 1:
            assert not (p & 0x8000) and (p & 255) != 0x15, (name, i, 'unsafe dry')
        if bits & 2:
            assert not (p & 0x8000) and (p & 255) == 0x15, (name, i, 'unsafe water')
        if bits & 4:
            assert (i % w, i // w) in public, (name, i, 'isolated fallback')
    # Once the generated floor is installed, also verify every authored warp
    # and actor against its actual generated map, not just the reference plan.
    # The layout is still old while the prototype is being prepared.
    maps = json.loads((R / f'data/maps/{name}/map.json').read_text())
    layouts = json.loads((R / 'data/layouts/layouts.json').read_text())['layouts']
    layout = next(v for v in layouts if v['id'] == maps['layout'])
    if (layout['width'], layout['height']) == (w, h):
        for group in ('warp_events', 'object_events', 'bg_events'):
            for e in maps[group]:
                x, y = e['x'], e['y']
                assert 0 <= x < w and 0 <= y < h, (name, group, x, y)
                assert mask[y*w+x] == 0, (name, group, x, y, 'occupied safe cell')
    print(f'{name}: {w}x{h}, dry={sum(bool(m & 1) for m in mask)}, '
          f'Surf={sum(bool(m & 2) for m in mask)}, fallback={sum(bool(m & 4) for m in mask)}')

print('PASS: masks match reference geometry, exclude thresholds, and place fallbacks in the public dry component.')
print('Static permission modeling only; generated-map event checks run only on installed floors. '
      'Verify rendering, components, walking and Surf saves in emulator.')
