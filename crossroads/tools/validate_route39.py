#!/usr/bin/env python3
"""Validate a genuinely reachable, reciprocal Route 39 exploration connection."""
import json
import struct
from collections import deque
from pathlib import Path
from build_route39_layout import generate
root = Path(__file__).resolve().parents[2]
def load(path):
    return json.loads((root / path).read_text())
hgss=(root/'crossroads/hgss/authoring/OlivineCity.json').exists()
offset=12 if hgss else 16
city = load('data/maps/OlivineCity/map.json')
route = load('data/maps/JohtoRoute39/map.json')
assert dict(map='MAP_JOHTO_ROUTE39', offset=offset, direction='up') in city['connections']
assert route['connections'] == [dict(map='MAP_OLIVINE_CITY', offset=-offset, direction='down'), dict(map='MAP_JOHTO_ROUTE38', offset=0, direction='up')]
groups = load('data/maps/map_groups.json')['gMapGroup_CrossroadsOlivine']
assert groups[:8] == ['OlivineCity', 'OlivineCity_Residence', 'OlivineCity_NeighborHouse', 'OlivineCity_Gym', 'OlivineCity_PokemonCenter_1F', 'OlivineCity_Mart', 'OlivineCity_SilphOffice', 'OlivineCity_HarborOffice']
assert groups[8] == 'JohtoRoute39', 'Append map IDs without changing saved locations'
assert (root / 'data/layouts/JohtoRoute39/map.bin').read_bytes() == generate()
tiles = struct.unpack('<1152H', generate())
blocked = {(o['x'], o['y']) for o in route['object_events']}
seen = {(12, 47)}
q = deque(seen)
while q:
    x, y = q.popleft()
    for p in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
        nx, ny = p
        if p in seen or p in blocked or not (0 <= nx < 24 and 0 <= ny < 48):
            continue
        t = tiles[ny*24+nx]
        if t & 0xC00 or t >> 12 != 3:
            continue
        seen.add(p)
        q.append(p)
assert (12, 4) in seen
for event in route['object_events'] + route['bg_events']:
    x,y = event['x'], event['y']
    assert any((x+dx,y+dy) in seen for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)])
city_tiles = struct.unpack('<'+str(64*64 if hgss else 48*48)+'H', (root / 'data/layouts/OlivineCity/map.bin').read_bytes())
for x in range(9 if hgss else 11,14):
    assert tiles[47*24+x] == city_tiles[x+offset] == (0x31ff if hgss else 0x3202)
assert route['region'] == 'REGION_HOENN'  # Emerald target filter
assert route['region_map_section'] == 'MAPSEC_JOHTO_ROUTE_39'
assert 'data/maps/JohtoRoute39/scripts.inc' in (root / 'data/event_scripts.s').read_text()
print('Route 39 reciprocal connections, stable map IDs, reachable signs/NPC and city seam: PASS')
