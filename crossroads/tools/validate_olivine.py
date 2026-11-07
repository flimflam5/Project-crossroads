#!/usr/bin/env python3
"""Structural regression checks; not a substitute for emulator playtesting."""
import json
import argparse
import re
import struct
from collections import deque
from pathlib import Path

from build_olivine_layout import generate

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--built', action='store_true', help='also verify mapjson target inclusion after make')
args = parser.parse_args()


def read(path):
    return json.loads((ROOT / path).read_text())


groups = read('data/maps/map_groups.json')
names = groups['gMapGroup_CrossroadsOlivine']
assert groups['group_order'][-1] == 'gMapGroup_CrossroadsOlivine'
assert len(names) == 8
maps = {m['id']: m for m in (read(f'data/maps/{n}/map.json') for n in names)}
layouts = {l['id']: l for l in read('data/layouts/layouts.json')['layouts']}
city = maps['MAP_OLIVINE_CITY']
raw = ROOT / layouts[city['layout']]['blockdata_filepath']
assert raw.read_bytes() == generate(), 'Regenerate the city layout'
linked = (ROOT / 'data/event_scripts.s').read_text()
script = (ROOT / 'crossroads/scripts/olivine.inc').read_text()
assert 'givemon' not in script, 'City must never grant a second starter'

for mid, m in maps.items():
    # mapjson uses this field as the Emerald build filter, not geography.
    assert m['region'] == 'REGION_HOENN'
    assert m['region_map_section'] == 'MAPSEC_OLIVINE_CITY'
    assert f'data/maps/{m["name"]}/scripts.inc' in linked
    layout = layouts[m['layout']]
    w, h = layout['width'], layout['height']
    data = (ROOT / layout['blockdata_filepath']).read_bytes()
    assert len(data) == w * h * 2, mid
    tiles = struct.unpack(f'<{w*h}H', data)
    positions = [(e['x'], e['y']) for e in m['object_events']]
    assert len(positions) == len(set(positions)), mid
    assert len(positions) <= 16, mid
    for obj in m['object_events']:
        assert tiles[obj['y'] * w + obj['x']] & 0xC00 == 0, (mid, obj)
    for event in m['object_events'] + m['bg_events']:
        assert 0 <= event['x'] < w and 0 <= event['y'] < h, (mid, event)
        assert re.search(r'^' + event['script'] + r'(?:::|:)', script, re.M), event
    for warp in m['warp_events']:
        assert 0 <= warp['x'] < w and 0 <= warp['y'] < h, (mid, warp)
        dest = maps[warp['dest_map']]
        back = dest['warp_events'][int(warp['dest_warp_id'])]
        assert back['dest_map'] == mid, (mid, warp, back)
        # Interior twin exits both point to the same exterior doorway.
        if mid == 'MAP_OLIVINE_CITY':
            assert int(back['dest_warp_id']) == m['warp_events'].index(warp)

# On-foot city connectivity, including approach tiles south of every doorway.
w = h = 48
tiles = struct.unpack('<2304H', raw.read_bytes())
blocked = set(positions for positions in ((o['x'], o['y']) for o in city['object_events']))
seen = {(12, 13)}
queue = deque(seen)
while queue:
    x, y = queue.popleft()
    for nx, ny in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
        if not (0 <= nx < w and 0 <= ny < h) or (nx, ny) in seen or (nx, ny) in blocked:
            continue
        tile = tiles[ny*w+nx]
        # Elevation 1 is sea: do not count Surf as a pedestrian connection.
        if tile & 0xC00 or tile >> 12 != 3:
            continue
        seen.add((nx, ny))
        queue.append((nx, ny))
for warp in city['warp_events']:
    assert (warp['x'], warp['y']+1) in seen, ('Unreachable door', warp)
for event in city['object_events'] + city['bg_events']:
    assert any((event['x']+dx, event['y']+dy) in seen for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]), ('Unreachable interaction', event)
assert (20, 42) in seen and (29, 42) in seen, 'Both piers must be reachable'
heal = read('src/data/heal_locations.json')['heal_locations'][-1]
assert heal['id'] == 'HEAL_LOCATION_OLIVINE_CITY'
assert (heal['x'], heal['y']) in seen
assert heal['respawn_map'] == 'MAP_OLIVINE_CITY_POKEMON_CENTER_1F'
center_scripts = (ROOT / 'data/maps/OlivineCity_PokemonCenter_1F/scripts.inc').read_text()
assert 'map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume' in center_scripts, 'Standard nurse requires Union Room name-buffer initialization'
if args.built:
    headers = (ROOT / 'data/maps/headers.inc').read_text()
    table = (ROOT / 'data/maps/groups.inc').read_text()
    for name in names:
        assert f'data/maps/{name}/header.inc' in headers, ('Map excluded from Emerald build', name)
        assert re.search(r'^\s*\.4byte ' + name + r'\s*$', table, re.M), ('Missing map pointer', name)
    print('Generated Emerald map headers and non-null Olivine map pointers: PASS')
print('Olivine map registration, reciprocal warps, NPC placement, pedestrian access and respawn data: PASS')
