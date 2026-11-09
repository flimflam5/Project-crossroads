#!/usr/bin/env python3
"""Integration checks for the connected western Johto exploration network."""
import argparse
import json
import re
import struct
from collections import deque
from pathlib import Path
from build_western_johto_layouts import generate
root=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--built',action='store_true')
args=parser.parse_args()
def load(path):return json.loads((root/path).read_text())
groups=load('data/maps/map_groups.json');names=groups['gMapGroup_CrossroadsOlivine']+groups.get('gMapGroup_CrossroadsJohtoExpansion',[])
assert names[:9]==['OlivineCity','OlivineCity_Residence','OlivineCity_NeighborHouse','OlivineCity_Gym','OlivineCity_PokemonCenter_1F','OlivineCity_Mart','OlivineCity_SilphOffice','OlivineCity_HarborOffice','JohtoRoute39']
assert names[9:11]==['JohtoRoute38','EcruteakCity']
maps={m['id']:m for m in [load(f'data/maps/{n}/map.json') for n in names]}
layouts={l['id']:l for l in load('data/layouts/layouts.json')['layouts']}
raw={mid:struct.unpack('<'+'H'*(layouts[m['layout']]['width']*layouts[m['layout']]['height']),(root/layouts[m['layout']]['blockdata_filepath']).read_bytes()) for mid,m in maps.items()}
linked=(root/'data/event_scripts.s').read_text()
scripts='\n'.join(p.read_text() for p in (root/'crossroads/scripts').glob('johto*.inc'))+'\n'+(root/'crossroads/scripts/area_completion.inc').read_text()+'\n'+(root/'crossroads/scripts/olivine_interiors.inc').read_text()+'\n'+'\n'.join((root/f'data/maps/{n}/scripts.inc').read_text() for n in names)+'\n'+(root/'crossroads/scripts/olivine.inc').read_text()+'\n'+(root/'crossroads/scripts/western_johto.inc').read_text()+'\n'+(root/'crossroads/scripts/starter_rescue.inc').read_text()
scripts+='\n'+(root/'crossroads/scripts/hgss_ecruteak.inc').read_text()
assert 'crossroads/scripts/hgss_ecruteak.inc' in linked
for name,data in generate().items():assert (root/f'data/layouts/{name}/map.bin').read_bytes()==data
reverse={'up':'down','down':'up','left':'right','right':'left'}
for mid,m in maps.items():
 assert m['region']=='REGION_HOENN' # Emerald target inclusion, not story region
 assert f'data/maps/{m["name"]}/scripts.inc' in linked
 w,h=layouts[m['layout']]['width'],layouts[m['layout']]['height']
 for e in m['object_events']+m['bg_events']:
  x,y=e['x'],e['y'];assert 0<=x<w and 0<=y<h,(mid,e)
  assert re.search(r'^'+e['script']+r'::?',scripts,re.M),(mid,e)
 for o in m['object_events']:assert raw[mid][o['y']*w+o['x']] & 0xC00==0,(mid,o)
 assert len({(o['x'],o['y']) for o in m['object_events']})==len(m['object_events'])<=16
 for warp in m['warp_events']:
  dest=maps[warp['dest_map']];back=dest['warp_events'][int(warp['dest_warp_id'])]
  assert back['dest_map']==mid,(mid,warp)
 for c in m['connections'] or []:
  dest=maps[c['map']]
  assert any(b==dict(map=mid,direction=reverse[c['direction']],offset=-c['offset']) for b in dest['connections'] or []),(mid,c)
# Flood the actual passable outdoor graph across correctly offset map borders.
start=('MAP_OLIVINE_CITY',12,13);seen={start};queue=deque([start])
while queue:
 mid,x,y=queue.popleft();m=maps[mid];w,h=layouts[m['layout']]['width'],layouts[m['layout']]['height']
 for dx,dy,direction in [(1,0,'right'),(-1,0,'left'),(0,1,'down'),(0,-1,'up')]:
  nx,ny=x+dx,y+dy;dest=mid
  if not(0<=nx<w and 0<=ny<h):
   c=next((c for c in m['connections'] or [] if c['direction']==direction),None)
   if c is None:continue
   dest=c['map'];dw,dh=layouts[maps[dest]['layout']]['width'],layouts[maps[dest]['layout']]['height']
   if direction=='up':nx,ny=nx-c['offset'],dh-1
   elif direction=='down':nx,ny=nx-c['offset'],0
   elif direction=='left':nx,ny=dw-1,ny-c['offset']
   else:nx,ny=0,ny-c['offset']
   if not(0<=nx<dw and 0<=ny<dh):continue
  else:dw=w
  p=(dest,nx,ny)
  if p in seen:continue
  if any((o['x'],o['y'])==(nx,ny) for o in maps[dest]['object_events']):continue
  t=raw[dest][ny*dw+nx]
  if t&0xC00 or t>>12!=3:continue
  seen.add(p);queue.append(p)
for mid in ['MAP_JOHTO_ROUTE39','MAP_JOHTO_ROUTE38','MAP_ECRUTEAK_CITY']:
 m=maps[mid]
 assert any(p[0]==mid for p in seen),('Disconnected map',mid)
 for warp in m['warp_events']:assert (mid,warp['x'],warp['y']+1) in seen,('Unreachable door',mid,warp)
 for e in m['object_events']+m['bg_events']:
  assert any((mid,e['x']+dx,e['y']+dy) in seen for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]),('Unreachable interaction',mid,e)
heals=load('src/data/heal_locations.json')['heal_locations']
heal=next(h for h in heals if h['id']=='HEAL_LOCATION_ECRUTEAK_CITY')
assert (heal['map'],heal['x'],heal['y']) in seen
center=(root/'data/maps/EcruteakCity_PokemonCenter_1F/scripts.inc').read_text()
assert 'CableClub_OnResume' in center and 'Ecruteak_CenterOnTransition' in center
if args.built:
 headers=(root/'data/maps/headers.inc').read_text();groups=(root/'data/maps/groups.inc').read_text()
 for n in names[9:]:
  assert f'data/maps/{n}/header.inc' in headers
  assert re.search(r'^\s*\.4byte '+n+r'\s*$',groups,re.M)
print('Western Johto connected pedestrian graph, all doors/interactions, reciprocal exits, IDs and Center respawn: PASS')
