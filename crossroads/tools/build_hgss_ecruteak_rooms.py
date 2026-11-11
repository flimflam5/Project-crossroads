#!/usr/bin/env python3
"""Reference-shaped Ecruteak houses/theater. Existing IDs/scripts remain.

The source houses share one HGSS matrix; their similar furnishings are intentional.
Original GBA furniture replaces DS models. Source plot actors/rewards are omitted.
"""
import argparse,copy,json,struct
from pathlib import Path
from hgss_room_projection import project,ART,FACTS
R=Path(__file__).resolve().parents[2]
TARGETS={'MAP_ECRUTEAK_SOUTHWEST_HOUSE':'EcruteakCity_Residence','MAP_ECRUTEAK_DOWSING_MACHINE_HOUSE':'EcruteakCity_DowsingHouse','MAP_ECRUTEAK_DANCE_THEATER':'EcruteakCity_DanceTheater'}
def load(p):return json.loads((R/p).read_text())
def generate(check=False):
 def write(p,b):
  if isinstance(b,str):b=b.encode()
  dest=R/p
  if check:assert dest.exists() and dest.read_bytes()==b,('Regenerate Ecruteak room',p)
  elif not dest.exists() or dest.read_bytes()!=b:dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
 def js(p,v):write(p,json.dumps(v,indent=2)+'\n')
 layouts=load('data/layouts/layouts.json');ls={l['id']:l for l in layouts['layouts']};groups=load('data/maps/map_groups.json');manifest=load('crossroads/johto/manifest.json');city=load('data/maps/EcruteakCity/map.json');review=[]
 for header,name in TARGETS.items():
  existing=(R/f'data/maps/{name}/map.json').exists();m=load(f'data/maps/{name}/map.json') if existing else copy.deepcopy(load('data/maps/EcruteakCity_Residence/map.json'))
  if name=='EcruteakCity_DowsingHouse':m.update(name=name,id='MAP_ECRUTEAK_CITY_DOWSING_HOUSE',object_events=[],bg_events=[])
  if m['layout']=='LAYOUT_HOUSE_WITH_BED' or name=='EcruteakCity_DowsingHouse':m['layout']='LAYOUT_HGSS_'+name.upper()
  projection_facts=None
  if header=='MAP_ECRUTEAK_DANCE_THEATER':
   # The generic projector draws wide temple tables; this room instead owns
   # its13 one-cell HGSS audience benches. Never draw both representations.
   projection_facts=copy.deepcopy(FACTS)
   for chunk in projection_facts[header]['chunks']:chunk['props']=[p for p in chunk['props'] if p['model']!=56]
  room=project(header,facts=projection_facts);w,h=room['width'],room['height'];tiles=room['tiles'];seen=room['walkable']
  def stamp(part,x,y):
   a=ART[part]
   for yy in range(a['height']):
    for xx in range(a['width']):
     X,Y=x+xx,y+yy
     if 0<=X<w and 0<=Y<h:tiles[Y*w+X]=(0x3000 if (X,Y) in seen else 0x400)|a['start']+yy*a['width']+xx
  if 'HOUSE' in header:
   for y in (1,2):
    for x in range(1,10):tiles[y*w+x]=0x400|ART['house_wall']['start']+(y-1)*4+x%4
   stamp('house_window',4,1);stamp('fridge',1,2);stamp('house_kitchen',2,2);stamp('cabinet',8,2);stamp('dining_table',6,5)
   for x in (5,8):
    for y in (5,6):stamp('chair',x,y)
   if not m['object_events']:
    template=copy.deepcopy(load('data/maps/EcruteakCity_Residence/map.json')['object_events'][0]);template.update(script='Hgss_HouseResident',graphics_id='OBJ_EVENT_GFX_MAN_3');m['object_events']=[template]
   m['object_events'][0].update(x=5,y=5)
   if len(m['object_events'])==1:
    child=copy.deepcopy(m['object_events'][0]);child.update(x=8,y=5,graphics_id='OBJ_EVENT_GFX_BOY_1',script='Hgss_HouseChild');child.pop('local_id',None);m['object_events'].append(child)
  else:
   stage_art=load('crossroads/hgss/art/theater/manifest.json')['specs']
   for y in (3,4):
    for x in range(1,w-1):tiles[y*w+x]=0x400|stage_art['stage_backdrop']['start']+(y-3)*12+x-1
   for y in range(5,8):
    for x in range(1,w-1):tiles[y*w+x]=0x3000|ART['wood']['start']
   # HGSS stage riser with two open stair aisles; no mandatory fight gate.
   for x in range(1,w-1):
    if (x,8) not in seen:tiles[8*w+x]=0x400|stage_art['stage_rope']['start']
   # Read actual model56 positions: the upper center aisle deliberately has
   # no benches at6,10 or8,10. A rectangular fill closed that aisle and also
   # duplicated the generic projector's seats one row below.
   for chunk in FACTS[header]['chunks']:
    for prop in chunk['props']:
     if prop['model']!=56:continue
     x,y=int(prop['tile_x']),int(prop['tile_z']);stamp('theater_bench',x,y);tiles[y*w+x]=0x400|ART['theater_bench']['start']
   # Actual final HGSS audience uses a green checker and purple floor
   # cushions. The private seat drawing keeps its historical895 ID; replace
   # only audience ground wood, leaving the brown raised stage/steps intact.
   for y in range(9,h):
    for x in range(w):
     i=y*w+x
     if tiles[i]&1023==ART['wood']['start']:tiles[i]=(tiles[i]&0xfc00)|stage_art['audience_floor']['start']
   m['object_events'][0].update(x=10,y=9)
   while len(m['object_events'])<6:
    o=copy.deepcopy(m['object_events'][1]);o.pop('local_id',None);m['object_events'].append(o)
   for i,o in enumerate(m['object_events'][1:6]):o.update(x=2+i*2,y=6,graphics_id='OBJ_EVENT_GFX_ECRUTEAK_PERFORMER')
  door=FACTS[header]['warps'][0];outside=2 if name=='EcruteakCity_Residence' else 3 if name=='EcruteakCity_DanceTheater' else 8
  m['warp_events']=[dict(x=door['x']+i,y=door['z'],elevation=0,dest_map=city['id'],dest_warp_id=str(outside)) for i in range(2)]
  if name=='EcruteakCity_DanceTheater':m['warp_events'][0]['dest_warp_id']='16'
  for e in m['warp_events']:tiles[e['y']*w+e['x']]=ART['exit']['start']
  for o in m['object_events']:assert not tiles[o['y']*w+o['x']]&0xc00,(name,'Actor in furniture',o)
  l=dict(id=m['layout'],name=name+'_Layout',width=w,height=h,primary_tileset='gTileset_Building',secondary_tileset='gTileset_HgssTheater' if name=='EcruteakCity_DanceTheater' else 'gTileset_HgssTemple',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin',layout_version='emerald')
  if l['id'] in ls:ls[l['id']].clear();ls[l['id']].update(l)
  else:layouts['layouts'].append(l);ls[l['id']]=l
  write(l['blockdata_filepath'],struct.pack('<'+str(w*h)+'H',*tiles));write(l['border_filepath'],struct.pack('<4H',*([0x600]*4)));js(f'data/maps/{name}/map.json',m)
  if name=='EcruteakCity_DowsingHouse':
   if len(city['warp_events'])==8:city['warp_events'].append(dict(x=34,y=55,elevation=0,dest_map=m['id'],dest_warp_id='0'))
   assert city['warp_events'][8]['dest_map']==m['id']
   if name not in groups['gMapGroup_CrossroadsJohtoExpansion']:groups['gMapGroup_CrossroadsJohtoExpansion'].append(name)
   if not any(p['name']==name for p in manifest['planned']):manifest['planned'].append(dict(name=name,kind='hgss',parent='EcruteakCity',cluster='west',status='reference-runtime-review-pending'))
   write(f'data/maps/{name}/scripts.inc',name+'_MapScripts::\n    .byte 0\n')
  review.append(dict(name=name,source_header=header,source=FACTS[header]['source'],dimensions=[w,h],adaptations=['GBA furniture/flat room instead of DS models','No HGSS plot actors or item reward imported','Legacy paired exit retained'],visual_qa='pending',runtime_qa='pending'))
 js('data/maps/EcruteakCity/map.json',city);js('data/layouts/layouts.json',layouts);js('data/maps/map_groups.json',groups);js('crossroads/johto/manifest.json',manifest);js('crossroads/hgss/room-review.json',review)
 inc=(R/'data/event_scripts.s').read_text();line='\t.include "data/maps/EcruteakCity_DowsingHouse/scripts.inc"'
 if line not in inc:inc+='\n'+line+'\n'
 write('data/event_scripts.s',inc)
 print('Canonical house/theater rooms generated; source rewards/story omitted; runtime/visual review required.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');generate(p.parse_args().check)
