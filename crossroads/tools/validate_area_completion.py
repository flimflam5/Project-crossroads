#!/usr/bin/env python3
"""Verify completed-area graph, indoor access, graphics budgets and save invariants."""
import json,struct,re
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[2]
def load(p):return json.loads((R/p).read_text())
layouts={l['id']:l for l in load('data/layouts/layouts.json')['layouts']}
names=load('data/maps/map_groups.json')['gMapGroup_CrossroadsOlivine']
maps={m['id']:m for m in [load(f'data/maps/{n}/map.json') for n in names]}
script=(R/'crossroads/scripts/area_completion.inc').read_text()
for spec in load('crossroads/art/western/rooms.json'):
 m=load(f'data/maps/{spec["name"]}/map.json');l=layouts[m['layout']];w,h=l['width'],l['height']
 t=struct.unpack('<'+str(w*h)+'H',(R/l['blockdata_filepath']).read_bytes());start=m['warp_events'][0];seed=(start['x'],start['y'])
 blocked={(o['x'],o['y']) for o in m['object_events']};q=deque([seed]);seen={seed}
 while q:
  x,y=q.popleft()
  for p in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
   a,b=p
   if p in seen or p in blocked or not(0<=a<w and 0<=b<h):continue
   if t[b*w+a]&0xc00:continue
   seen.add(p);q.append(p)
 for warp in m['warp_events']:
  assert (warp['x'],warp['y']) in seen,(spec['name'],'unreachable stairs',warp)
  dst=maps[warp['dest_map']];back=dst['warp_events'][int(warp['dest_warp_id'])];assert back['dest_map']==m['id'],(m,warp)
 for e in m['object_events']+m['bg_events']:
  assert any((e['x']+a,e['y']+b) in seen for a,b in [(1,0),(-1,0),(0,1),(0,-1)]),(m['name'],'unreachable event',e)
  assert e['script']+'::' in script,(m['name'],e)
art=load('crossroads/art/western/architecture.json')
assert len(art['tile_slots'])==len(set(art['tile_slots']))<=402
assert set(art['tile_slots']).isdisjoint(range(224,228)),'Do not overwrite animated balloon tiles'
base=(R/'data/tilesets/secondary/slateport/metatiles.bin').read_bytes();custom=(R/'data/tilesets/secondary/western_city/metatiles.bin').read_bytes()
for i in load('crossroads/art/western/preserved-city-metatiles.json'):
 if i>=512:assert base[(i-512)*16:(i-511)*16]==custom[(i-512)*16:(i-511)*16]
assert len(custom)//16<=512
ops=(R/'include/constants/opponents.h').read_text();assert '#define MAX_TRAINERS_COUNT_EMERALD 864' in ops
assert 'TRAINER_FLAGS_END' not in script and 'setflag FLAG_BADGE' not in script and 'givemon' not in script
assert '    NUM_OBJ_EVENT_GFX,' in (R/'include/constants/event_objects.h').read_text()
enc=load('src/data/wild_encounters.json')['wild_encounter_groups'][0]['encounters']
for route,lo,hi,allowed in [('39',4,7,{'SENTRET','HOOTHOOT','MAREEP','MILTANK'}),('38',5,9,{'MEOWTH','FARFETCHD','MAGNEMITE','HOOTHOOT'})]:
 e=next(e for e in enc if e['map']=='MAP_JOHTO_ROUTE'+route)['land_mons'];assert len(e['mons'])==12
 assert {s['species'][8:] for s in e['mons']}==allowed
 assert all((s['min_level'],s['max_level'])==(lo,hi) for s in e['mons'])
from PIL import Image
for path in list((R/'graphics/trainers/crossroads_jasmine').glob('*.png'))+list((R/'graphics/trainers/crossroads_morty').glob('*.png'))+[R/'graphics/object_events/pics/misc/area_bell.png',R/'graphics/object_events/pics/misc/area_lantern.png']:
 im=Image.open(path);assert im.mode=='P' and max(im.tobytes())<16,(path,'native 4bpp indices')
for spec in load('crossroads/art/western/rooms.json'):
 assert (R/f'data/layouts/{spec["name"]}/border.bin').read_bytes()==struct.pack('<4H',*([0x601]*4))
print('All landmark/farm/Gym doors, indoor access, original graphics, tile limits, approved roster and unchanged flag space: PASS')
