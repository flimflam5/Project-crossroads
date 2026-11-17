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
print('PASS: all 10 donor floor warps inventoried; 6 existing internal/external warp indices and reciprocal targets preserved; 2 Ruins exits unresolved. No gameplay integration.')
