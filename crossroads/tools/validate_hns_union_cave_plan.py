#!/usr/bin/env python3
"""Check a not-yet-integrated cave warp mapping against donor and current IDs."""
from pathlib import Path
import json
R=Path(__file__).resolve().parents[2]
D=R/'crossroads/donor/hns-union-cave'
def read(p):return json.loads(p.read_text())
p=read(D/'warp-mapping.json');assert p['status'].startswith('prototype-only')
for floor in p['floors']:
 current=read(R/'data/maps'/floor['existing_map']/'map.json')
 donor=read(D/'data/maps'/floor['donor_map']/'map.json')
 assert current['id']==floor['existing_id']
 used=set()
 for e in floor['warp_mapping']:
  di=e['donor_index'];assert di not in used and 0<=di<len(donor['warp_events']);used.add(di)
  if e.get('new'):
   assert e['existing_index'] is None or e['existing_index']>=len(current['warp_events'])
  else:
   actual=current['warp_events'][e['existing_index']]
   assert actual['dest_map']==e['destination'] and int(actual['dest_warp_id'])==e['destination_index'],(floor['existing_map'],e)
   target=read(R/'data/maps'/{'MAP_UNION_CAVE_1_F':'UnionCave_1F','MAP_UNION_CAVE_2_F':'UnionCave_2F','MAP_UNION_CAVE_3_F':'UnionCave_3F','MAP_JOHTO_ROUTE32':'JohtoRoute32','MAP_JOHTO_ROUTE33':'JohtoRoute33'}[e['destination']]/'map.json')
   back=target['warp_events'][e['destination_index']]
   assert back['dest_map']==current['id'] and int(back['dest_warp_id'])==e['existing_index']
 assert used==set(range(len(donor['warp_events'])))
# Donor's two cave exits return to separate areas of the same exterior map.
# The constrained dry grid is an approximate check only, not an engine test.
from collections import deque
import struct
outside=read(D/'data/maps/RuinsOfAlph_Outside_hns/map.json')
b=(D/'data/layouts/RuinsOfAlph_Outside_hns/map.bin').read_bytes()
assert len(b)==46*48*2
cells=struct.unpack('<2208H',b)
b1=read(D/'data/maps/UnionCave_B1F_hns/map.json')
for bi,oi in [(3,3),(4,2)]:
    assert b1['warp_events'][bi]['dest_map']==outside['id']
    assert int(b1['warp_events'][bi]['dest_warp_id'])==oi
    assert outside['warp_events'][oi]['dest_map']==b1['id']
    assert int(outside['warp_events'][oi]['dest_warp_id'])==bi

def dry_component(warp_index):
    e=outside['warp_events'][warp_index];start=(e['x'],e['y']);q=deque([start]);seen={start}
    while q:
        x,y=q.popleft()
        for X,Y in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if not(0<=X<46 and 0<=Y<48) or (X,Y) in seen:continue
            v=cells[Y*46+X]
            if v&0xc00 or v>>12 not in (3,4):continue
            seen.add((X,Y));q.append((X,Y))
    return seen
components=[dry_component(i) for i in (0,2,3)]
assert not(components[0]&components[1]) and not(components[0]&components[2]) and not(components[1]&components[2])
print('PASS: 10 donor warps inventoried; 6 existing reciprocal indices preserved; '
      'the 2 donor Ruins exits return to distinct dry components separated from public Route 32 entrance. '
      'No gameplay integration; directional movement/Surf untested.')
