#!/usr/bin/env python3
"""HGSS-shaped service rooms/Gym with stable accepted scripts and save IDs.

Native GBA counter/PC/heal tiles preserve their engine behaviors. No DS online
service or HGSS story flags are imported. Gym bridges preserve source ground
coordinates; stepping into adjacent void returns to the entrance by script.
"""
import argparse,json,struct,copy
from pathlib import Path
from hgss_room_projection import FACTS
R=Path(__file__).resolve().parents[2]
def load(p):return json.loads((R/p).read_text())
def generate(check=False):
 def write(p,b):
  if isinstance(b,str):b=b.encode()
  d=R/p
  if check:assert d.exists() and d.read_bytes()==b,('Regenerate service room',p)
  elif not d.exists() or d.read_bytes()!=b:d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(b)
 def js(p,v):write(p,json.dumps(v,indent=2)+'\n')
 layouts=load('data/layouts/layouts.json');ls={l['id']:l for l in layouts['layouts']};groups=load('data/maps/map_groups.json');manifest=load('crossroads/johto/manifest.json');new=[];reviews=[];maps={}
 base=load('crossroads/hgss/contracts/ecruteak-rooms-qa04.json')
 def obj(x,y,script,gfx='WOMAN_3'):
  o=copy.deepcopy(base['EcruteakCity_Residence']['object_events'][0]);o.update(x=x,y=y,script=script,graphics_id='OBJ_EVENT_GFX_'+gfx);o.pop('local_id',None);return o
 def native(n,header,secondary,w,h,floor):
  m=load(f'data/maps/{n}/map.json') if (R/f'data/maps/{n}/map.json').exists() else copy.deepcopy(base['EcruteakCity_PokemonCenter_1F'])
  if n.endswith('_B1F'):m.update(name=n,id='MAP_ECRUTEAK_CITY_POKEMON_CENTER_B1F',object_events=[],bg_events=[]);new.append(n)
  if n in ['EcruteakCity_PokemonCenter_1F','EcruteakCity_Mart'] or n.endswith('_B1F'):m['layout']='LAYOUT_HGSS_'+n.upper()
  m['coord_events']=[]
  if 'POKECENTER' in header:m['music']='MUS_POKE_CENTER'
  t=[0x601 if secondary=='gTileset_PokemonCenter' else 0x401]*(w*h)
  f=FACTS[header];cw=f['matrix_dimensions'][0];perms={}
  for i,c in enumerate(f['chunks']):
   for y in range(32):
    for x in range(32):perms[(i%cw*32+x,i//cw*32+y)]=c['permissions'][y*32+x]
  for y in range(h):
   for x in range(w):
    if not perms.get((x,y),0x8000)&0x8000:t[y*w+x]=floor
  return m,t,perms
 def save(m,t,w,h,secondary,header,adapt):
  n=m['name'];l=dict(id=m['layout'],name=n+'_Layout',width=w,height=h,primary_tileset='gTileset_Building',secondary_tileset=secondary,border_filepath=f'data/layouts/{n}/border.bin',blockdata_filepath=f'data/layouts/{n}/map.bin',layout_version='emerald')
  if l['id'] in ls:ls[l['id']].clear();ls[l['id']].update(l)
  else:layouts['layouts'].append(l);ls[l['id']]=l
  write(l['blockdata_filepath'],struct.pack('<'+str(w*h)+'H',*t));write(l['border_filepath'],struct.pack('<4H',*([0x601 if secondary=='gTileset_PokemonCenter' else 0x401 if secondary=='gTileset_Shop' else 0x600]*4)));js(f'data/maps/{n}/map.json',m);maps[n]=m
  reviews.append(dict(name=n,source_header=header,source=FACTS[header]['source'],dimensions=[w,h],adaptations=adapt,visual_qa='pending',runtime_qa='pending'))
 def warp(x,y,dst,index):return dict(x=x,y=y,elevation=0,dest_map=dst,dest_warp_id=str(index))
 # Native GBA Center module: sample existing accepted layout, never edit it.
 original=ls['LAYOUT_OLIVINE_POKEMON_CENTER_1F'];b=(R/original['blockdata_filepath']).read_bytes();stock=struct.unpack('<126H',b)
 n='EcruteakCity_PokemonCenter_1F';w,h=17,21;m,t,perms=native(n,'MAP_ECRUTEAK_POKECENTER_1F','gTileset_PokemonCenter',w,h,0x3202)
 def put(x,y,v):t[y*w+x]=v
 # Two-level DS reception adapted to a connected flat GBA service deck.
 for y in (0,1):
  for x in range(1,w-1):put(x,y,0x60b if y==0 else 0x621)
 for y in range(2,6):
  for x in range(1,w-1):put(x,y,0x3202)
 for x in (2,6,11):
  for xx in range(x-1,x+2):put(xx,3,0x621)
 for y in range(5):
  for x in range(4,10):put(x+1,y+9,stock[y*14+x])
 # Source stair/PC locations; dedicated service room below, no phantom door.
 for x,y in [(1,17),(2,17),(12,15),(13,15)]:put(x,y,0x3234)
 put(12,10,0x404);put(12,11,0x3224)
 for y in range(7,15):
  if perms[(3,y)]&0x8000:put(3,y,0x620)
 m['object_events']=copy.deepcopy(base[n]['object_events']);m['object_events'][0].update(x=8,y=11);m['object_events'][1].update(x=4,y=18)
 put(1,2,0x621)
 for x in (2,6,11):m['object_events'].append(obj(x,2,'Hgss_CommunicationDesk','LINK_RECEPTIONIST'))
 for o in m['object_events']:put(o['x'],o['y'],0x3202)
 m['warp_events']=[warp(8,19,'MAP_ECRUTEAK_CITY',5),warp(9,19,'MAP_ECRUTEAK_CITY',5),warp(14,17,'MAP_ECRUTEAK_CITY_POKEMON_CENTER_B1F',0)]
 # Native escalators walk one extra tile sideways after landing.
 for yy in (17,18):
  for xx in (13,14,15):put(xx,yy,0x3202)
 put(8,19,0x3203);put(9,19,0x3204);put(14,17,0x3289)
 for yy in range(8,13):
  for xx in range(3,13):
   if t[yy*w+xx]==0x601:t[yy*w+xx]=0x621
 m['bg_events']=[dict(type='sign',x=7,y=2,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='Hgss_CommunicationDesk')]
 save(m,t,w,h,'gTileset_PokemonCenter','MAP_ECRUTEAK_POKECENTER_1F',['Native GBA heal/counter/PC tiles at HGSS service positions','DS elevated rear reception flattened; unavailable DS online entrance is a labeled service desk, not a broken warp','Existing nurse/heal ID/local ID preserved; shared Olivine layout unchanged'])
 n='EcruteakCity_PokemonCenter_B1F';w,h=17,12;m,t,perms=native(n,'MAP_ECRUTEAK_POKECENTER_B1F','gTileset_PokemonCenter',w,h,0x3202)
 for y in (0,1):
  for x in range(1,16):t[y*w+x]=0x60b if y==0 else 0x621
 m['object_events']=[obj(x,4,'Hgss_CommunicationDesk','LINK_RECEPTIONIST') for x in (4,8,12)]
 for y in range(2,5):
  for x in range(2,16):
   if (x,y) not in {(4,4),(8,4),(12,4)}:t[y*w+x]=0x602
 for x in range(2,15):t[5*w+x]=0x621
 for x in (4,8,12):
  t[4*w+x]=0x3202
  for xx in range(x-1,x+2):t[5*w+xx]=0x621
 # Native waiting bench occupies the DS staircase/partition footprint.
 for yy,row in enumerate([[0x63d,0x63e],[0x645,0x646]],8):
  for xx,v in enumerate(row,2):t[yy*w+xx]=v
 for yy in (9,10):
  for xx in (13,14,15):t[yy*w+xx]=0x3202
 m['warp_events']=[warp(14,10,'MAP_ECRUTEAK_CITY_POKEMON_CENTER_1F',2)];t[10*w+14]=0x32a1
 save(m,t,w,h,'gTileset_PokemonCenter','MAP_ECRUTEAK_POKECENTER_B1F',['Wi-Fi desks are ambient offline reception; no internet functionality claimed','Native GBA stairs retain canonical source coordinate'])
 # Shop uses its original script/stock and GBA shelves, placed at HGSS positions.
 n='EcruteakCity_Mart';w,h=14,13;m,t,perms=native(n,'MAP_ECRUTEAK_POKEMART','gTileset_Shop',w,h,0x3201)
 for x in range(1,13):t[w+x]=0x613;t[2*w+x]=0x61b
 for x in (5,7):t[2*w+x]=0x623;t[2*w+x+1]=0x624;t[3*w+x]=0x628;t[3*w+x+1]=0x629
 for x in (6,9):
  for y in (6,7):t[y*w+x]=0x62b if y==6 else 0x633;t[y*w+x+1]=0x62c if y==6 else 0x634
 for y in range(3,8):
  t[y*w+1]=0x3208;t[y*w+2]=0x3208;t[y*w+3]=0x63a
 t[3*w+1]=0x644;t[3*w+2]=0x62a
 # Small stock display at the source's southern merchandise island.
 for x in (8,9):
  t[9*w+x]=0x62b+(x-8);t[10*w+x]=0x633+(x-8)
 m['object_events']=copy.deepcopy(base[n]['object_events']);m['object_events'][0].update(x=2,y=6);m['object_events'][1].update(x=9,y=4)
 assistant=copy.deepcopy(m['object_events'][0]);assistant.pop('local_id',None);assistant.update(x=2,y=4);m['object_events'].append(assistant)
 for o in m['object_events']:t[o['y']*w+o['x']]=0x3208 if o['x']==2 else 0x3201
 m['warp_events']=[warp(4,11,'MAP_ECRUTEAK_CITY',6),warp(5,11,'MAP_ECRUTEAK_CITY',6)];t[11*w+4]=0x216;t[11*w+5]=0x217
 save(m,t,w,h,'gTileset_Shop','MAP_ECRUTEAK_POKEMART',['Native GBA shelf/counter tiles replace DS furniture; accepted shop inventory unchanged','DS story delivery actors omitted'])
 # Gym reference bridge. Keep both existing IDs as two halves of the tall DS room.
 from hgss_room_projection import ART
 source=FACTS['MAP_ECRUTEAK_GYM'];p=[v for c in source['chunks'] for v in c['permissions']];bridge={(x,y) for y in range(64) for x in range(32) if p[y*32+x]&0x8600==0x600};bridge.add((16,53))
 for n,oy,h in [('EcruteakCity_Gym',32,24),('EcruteakCity_Gym_Arena',5,27)]:
  ox=6;w=18;m=load(f'data/maps/{n}/map.json');t=[0x600]*(w*h);allowed=[];falls=[]
  for y in range(h):
   for x in range(w):
    P=(x+ox,y+oy)
    if P in bridge:t[y*w+x]=0x3000|ART['wood']['start'];allowed.append([x,y])
    elif any((P[0]+dx,P[1]+dy) in bridge for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]) and not p[P[1]*32+P[0]]&0x8000:
     t[y*w+x]=0x3000|ART['void']['start'];falls.append([x,y])
  if n.endswith('_Arena'):
   m['warp_events']=[warp(13,26,'MAP_ECRUTEAK_CITY_GYM',2)];t[26*w+13]=0x3000|ART['warp']['start']
   m['object_events'][0].update(x=4,y=3);m['object_events'][1].update(x=13,y=25)
   # The source trainer occupied a one-tile bridge. Keep optional interaction
   # beside the bridge instead of silently adding a compulsory battle gate.
   m['object_events'][1].update(x=14,y=24);t[24*w+14]=0x3000|ART['wood']['start'];allowed.append([14,24])
  else:
   m['warp_events']=[warp(10,21,'MAP_ECRUTEAK_CITY',4),warp(11,21,'MAP_ECRUTEAK_CITY',4),warp(13,0,'MAP_ECRUTEAKCITY_GYM_ARENA',0)];t[21*w+10]=ART['exit']['start'];t[21*w+11]=ART['exit']['start'];t[13]=0x3000|ART['warp']['start'];allowed.append([11,21]);m['object_events'][0].update(x=12,y=19)
  m['object_events']=m['object_events'][:2] if n.endswith('_Arena') else m['object_events'][:1]
  for xx,yy in ([(3,5),(5,5)] if n.endswith('_Arena') else [(9,18),(11,18)]):m['object_events'].append(obj(xx,yy,'Hgss_GymLamp','AREA_LANTERN'))
  actors={(o['x'],o['y']) for o in m['object_events']}
  falls=[q for q in falls if tuple(q) not in actors and q not in allowed]
  m['coord_events']=[dict(type='trigger',x=x,y=y,elevation=0,var='VAR_TEMP_0',var_value='0',script='Hgss_GymReturn') for x,y in falls]
  m['music']='MUS_GYM'
  save(m,t,w,h,'gTileset_HgssTemple','MAP_ECRUTEAK_GYM',['Tall DS room split at source chunk seam into existing two GBA map IDs','Native scripted return when stepping off bridge; no badge gate or candle-extinguishing battle rule','Accepted Morty/student practice scripts retained; optional student beside path'])
  reviews[-1].update(origin_crop=[ox,oy],bridge_tiles=allowed,fall_tiles=falls)
 for n in new:
  if n not in groups['gMapGroup_CrossroadsJohtoExpansion']:groups['gMapGroup_CrossroadsJohtoExpansion'].append(n)
  if not any(p['name']==n for p in manifest['planned']):manifest['planned'].append(dict(name=n,kind='hgss',parent='EcruteakCity',cluster='west',status='reference-runtime-review-pending'))
  write(f'data/maps/{n}/scripts.inc',n+'_MapScripts::\n    .byte 0\n')
 js('data/layouts/layouts.json',layouts);js('data/maps/map_groups.json',groups);js('crossroads/johto/manifest.json',manifest);js('crossroads/hgss/service-review.json',reviews)
 inc=(R/'data/event_scripts.s').read_text()
 for n in new:
  line=f'\t.include "data/maps/{n}/scripts.inc"'
  if line not in inc:inc+='\n'+line+'\n'
 write('data/event_scripts.s',inc)
 print('HGSS service footprints/Gym bridge generated; no DS online/story/badge implementation claimed.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');generate(p.parse_args().check)
