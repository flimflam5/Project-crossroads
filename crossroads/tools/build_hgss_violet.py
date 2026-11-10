#!/usr/bin/env python3
"""HGSS Violet reconstruction. Canonical ground/endpoints, original GBA art.

No imported source story scripts, trades, trainer teams or badge gates. Existing
IDs are retained; gatehouses and Center basement append. Old current-area maps
are independent. Gym owner art is fitted after this authored base is produced.
"""
from pathlib import Path
from collections import deque
import argparse,json,struct,copy,math
from hgss_room_projection import project,ART,warp_tile
R=Path(__file__).resolve().parents[2]
def load(p):return json.loads((R/p).read_text())
ROOM_HEADERS={'VioletCity_Residence':'MAP_VIOLET_BELLSPROUT_ONYX_TRADE_HOUSE','VioletCity_Workshop':'MAP_VIOLET_NORTHWEST_HOUSE','VioletAcademy':'MAP_VIOLET_POKEMON_SCHOOL','VioletCity_Gym':'MAP_VIOLET_GYM','SproutTower_1F':'MAP_SPROUT_TOWER_1F','SproutTower_2F':'MAP_SPROUT_TOWER_2F','SproutTower_3F':'MAP_SPROUT_TOWER_3F','VioletCity_WestGate':'MAP_VIOLET_ROUTE_36_GATEHOUSE','VioletCity_EastGate':'MAP_ROUTE_31_VIOLET_GATEHOUSE'}
NEW=['VioletCity_PokemonCenter_B1F','VioletCity_WestGate','VioletCity_EastGate']
OWNED=set(ROOM_HEADERS)|set(NEW)|{'VioletCity','VioletCity_PokemonCenter_1F','VioletCity_Mart'}
def patch_neighbor(name,m):
 """Only replace Violet's old debug seam by its physical HGSS gatehouse."""
 for direction,route,x,y in [('West','JohtoRoute36',55,14),('East','JohtoRoute31',0,14)]:
  if name!=route:continue
  mid='MAP_VIOLET_CITY_'+direction.upper()+'_GATE';label='HgssViolet_'+direction+'RouteEnter'
  m['warp_events']=[e for e in m['warp_events'] if e['dest_map']!=mid]+[dict(x=x,y=y,elevation=0,dest_map=mid,dest_warp_id='1')]
  m['coord_events']=[e for e in m['coord_events'] if e['script']!=label]+[dict(type='trigger',x=x,y=y,elevation=0,var='VAR_TEMP_0',var_value='0',script=label)]
  m['connections']=[e for e in m['connections'] or [] if e['map']!='MAP_VIOLET_CITY']
 if name=='JohtoRoute32':
  m['connections']=[e for e in m['connections'] or [] if e['map']!='MAP_VIOLET_CITY']+[dict(map='MAP_VIOLET_CITY',direction='up',offset=-9)]
 return m
def neighbor_tiles(name,b,w,h):
 if name not in ['JohtoRoute31','JohtoRoute32','JohtoRoute36']:return b
 b=bytes.fromhex(load('crossroads/hgss/contracts/violet-qa06.json')['route'+name[10:]+'_raw_hex'])
 t=list(struct.unpack('<'+str(w*h)+'H',b))
 if name!='JohtoRoute32':
  x=55 if name=='JohtoRoute36' else 0;t[14*w+x]=0x3024
  return struct.pack('<'+str(len(t))+'H',*t)
 for y in range(7):
  for x in range(w):
   if t[y*w+x]&1023>=512:t[y*w+x]=(t[y*w+x]&~1023)|(0x1ff if not t[y*w+x]&0xc00 else 0xc6)
  for x in (14,15):t[y*w+x]=0x31ff
 return struct.pack('<'+str(len(t))+'H',*t)
def generate(check=False):
 def write(path,b):
  if isinstance(b,str):b=b.encode()
  # Compare the final owner-Gym layer, while keeping its source input separate.
  if path=='data/maps/VioletCity/map.json':
   from build_eight_gym_integration import patch_events
   b=(json.dumps(patch_events('VioletCity',json.loads(b)),indent=2)+'\n').encode()
  if path=='data/layouts/VioletCity/map.bin':
   from build_eight_gym_integration import overlay
   b=overlay('VioletCity',b,64,72)
  p=R/path
  if check:assert p.exists() and p.read_bytes()==b,('Regenerate canonical Violet',path)
  elif not p.exists() or p.read_bytes()!=b:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 def js(p,v):write(p,json.dumps(v,indent=2)+'\n')
 layouts=load('data/layouts/layouts.json');ls={l['id']:l for l in layouts['layouts']};groups=load('data/maps/map_groups.json');manifest=load('crossroads/johto/manifest.json');source=load('crossroads/hgss/canonical_events/johto-outdoor-geometry.json')['areas']['MAP_VIOLET'];facts=load('crossroads/hgss/canonical_events/violet-interior-geometry.json');art=load('crossroads/hgss/art/violet/manifest.json')['specs'];W,H=64,72;pad=8;perms=[0x8000]*(64*64)
 for c in source['cells']:
  for y in range(32):
   for x in range(32):perms[(c['y']*32+y)*64+c['x']*32+x]=c['permissions'][y*32+x]
 # Strip the empty DS matrix/debug fragments. Legitimate water/island access is
 # included in the survey graph, not silently converted into ordinary grass.
 seeds={(e['x'],e['y']) for e in source['warps']}|{(23,63),(24,63)};public=set(seeds);q=deque(seeds)
 while q:
  x,y=q.popleft()
  for a,b in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if 0<=a<64 and 0<=b<64 and not perms[b*64+a]&0x8000 and (a,b) not in public:public.add((a,b));q.append((a,b))
 t=[0x4c6]*(W*H)
 def put(x,y,value):assert 0<=x<W and 0<=y<H,(x,y);t[y*W+x]=value
 def rect(x,y,w,h,value):
  for yy in range(y,y+h):
   for xx in range(x,x+w):put(xx,yy,value)
 for y in range(64):
  for x in range(64):
   p=perms[y*64+x];behavior=p&255
   if (x,y) in public:put(x,y+pad,0x1170 if behavior in [16,17,19,21] else (0x3000|art['paving']['start']) if p&0x600 else 0x3001)
   elif behavior==6:put(x,y+pad,0x400|[0x1d4,0x1d5,0x1dc,0x1dd][y%2*2+x%2])
   else:put(x,y+pad,0x4c6)
 # Two source bridge spans: x38..40 walking deck, x37/41 solid rails.
 # Preserve the central plaza and each canonical approach, not a guessed path.
 a=art['bridge']
 for first in [10,21]:
  for yy in range(5):
   for xx in range(5):put(37+xx,first+pad+yy,a['start']+yy*5+xx+(0x400 if xx in [0,4] else 0x3000))
 def building(kind,doorX,doorY,flip=False):
  a=art[kind];x=doorX-a['door_x'];y=doorY-a['door_y'];assert not flip
  for yy in range(a['height']):
   for xx in range(a['width']):
    X,Y=x+xx,y+yy;cell=a.get('stamps',list(range(a['start'],a['start']+a['width']*a['height'])))[yy*a['width']+xx];opened=(X,Y)==(doorX,doorY);solid=yy>=a['height']-2 and not opened;under=t[Y*W+X]&0xfc00
    put(X,Y,cell|(0x400 if solid else 0x3000 if opened else under))
  put(doorX,doorY,0x3000|a['start']+a['door_y']*a['width']+a['door_x'])
 # All seven historic doorway indices retain their identity/destination.
 c=copy.deepcopy(load('crossroads/art/eight_gyms_v1/baseline/contracts.json')['cities']['VioletCity']['map']);doors=[(49,55),(21,41),(31,41),(36,61),(11,38),(47,41),(39,12)]
 for e,(x,y) in zip(c['warp_events'],doors):e.update(x=x,y=y)
 c['warp_events'].append(dict(c['warp_events'][2],x=32,dest_warp_id='1')) # Existing QA06 Gym alias7.
 building('center',49,55);building('mart',21,41);building('house',36,61);building('house',11,38);building('school',47,41);building('sprout',39,12)
 # The compressed southern house facade needs one extra courtyard corner:
 # otherwise its source side alley terminates against the larger GBA wall.
 put(34,62,0x3000|art['paving']['start'])
 # A DS roof can project above the matrix. North padding accommodates the whole
 # GBA tower without changing any relative source coordinates or clipping it.
 for x in range(64):put(x,0,0x4c6)
 # Gate buildings replace the old direct debug seams with the canonical rooms.
 building('gate',6,30);building('gate',62,53)
 c['warp_events'].append(dict(c['warp_events'][5],x=46,dest_warp_id='1')) # School's other glass panel8.
 put(46,41,0x3000|art['school']['start']+art['school']['door_y']*art['school']['width']+2)
 # Pixel entry is static; add proper warp behavior to the second school panel
 # using the existing public entrance metatile (paired door remains legible).
 for name,points in [('West',[(6,30),(6,31)]),('East',[(63,53),(63,54)])]:
  mid='MAP_VIOLET_CITY_'+name.upper()+'_GATE'
  for x,y in points:c['warp_events'].append(dict(x=x,y=y,elevation=0,dest_map=mid,dest_warp_id='0'))
 # Keep the source west/east road portals usable, while the map-to-map connection
 # now runs through real gatehouse rooms. The southern Route32 border stays real.
 c['connections']=[dict(map='MAP_JOHTO_ROUTE32',direction='down',offset=9)]
 for x in range(64):
  if x not in [23,24]:put(x,71,0x4c6)
 # South road is a two-tile canonical aperture; do not paint generic corridors.
 for y in range(65,72):
  for x in [23,24]:
   if (x,y-pad) in public:put(x,y,0x31ff)
 # Shared-primary-only data along the surviving southern scrolling seam.
 for y in range(65,72):
  for x in range(64):
   v=t[y*64+x]
   if v&1023>=512:put(x,y,(v&~1023)|0x1ff)
 signs=[(40,47),(47,56),(46,56),(19,42),(27,41),(35,63),(10,39),(43,41),(37,14)]
 for e,(x,y) in zip(c['bg_events'],signs):e.update(x=x,y=y);put(x,y,0x403)
 # Existing ambient actors retain scripts and local IDs, off the bridge choke.
 occupied=set(signs)|{(e['x'],e['y']) for e in c['warp_events']};land={(x,y+pad) for x,y in public if perms[y*64+x]&255 not in [16,17,19,21] and not t[(y+pad)*64+x]&0xc00}
 preferred=[(27,43),(42,47),(50,57),(39,26)]
 for o,target in zip(c['object_events'],preferred):
  options=[p for p in land-occupied if sum((p[0]+dx,p[1]+dy) in land-occupied for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)])>=3];point=min(options,key=lambda p:(abs(p[0]-target[0])+abs(p[1]-target[1]),p));o.update(x=point[0],y=point[1]);occupied.add(point)
 c['coord_events']=[dict(type='trigger',x=e['x'],y=e['y'],elevation=0,var='VAR_TEMP_0',var_value='0',script='HgssViolet_'+('West' if i<11 else 'East')+'Enter') for i,e in enumerate(c['warp_events']) if i>=9]
 def layout(m,w,h,secondary,primary='gTileset_Building',dedicated=False):
  if dedicated:m['layout']='LAYOUT_HGSS_'+m['name'].upper()
  l=dict(id=m['layout'],name=('Hgss' if dedicated else '')+m['name']+'_Layout',width=w,height=h,primary_tileset=primary,secondary_tileset=secondary,border_filepath=f'data/layouts/{m["name"]}/border.bin',blockdata_filepath=f'data/layouts/{m["name"]}/map.bin',layout_version='emerald')
  if l['id'] in ls:ls[l['id']].clear();ls[l['id']].update(l)
  else:layouts['layouts'].append(l);ls[l['id']]=l
  return ls[l['id']]
 maps={};reviews=[];raw_rooms={}
 def save(m,data,w,h,header,secondary='gTileset_HgssTemple',primary='gTileset_Building',dedicated=False):
  l=layout(m,w,h,secondary,primary,dedicated);write(l['blockdata_filepath'],struct.pack('<'+str(w*h)+'H',*data));border=0x600 if secondary=='gTileset_HgssTemple' else 0x601 if secondary=='gTileset_PokemonCenter' else 0x401;write(l['border_filepath'],struct.pack('<4H',*([border]*4)));js(f'data/maps/{m["name"]}/map.json',m);maps[m['name']]=m;raw_rooms[m['name']]=dict(layout=copy.deepcopy(l),data=data);reviews.append(dict(name=m['name'],source_header=header,dimensions=[w,h],runtime_qa='pending for this source tree',owner_visual_qa='pending'))
 def obj(template,x,y,script,gfx=None):
  o=copy.deepcopy(template);o.update(x=x,y=y,script=script)
  if gfx:o['graphics_id']=gfx
  o.pop('local_id',None);return o
 def warp(x,y,dest,index):return dict(x=x,y=y,elevation=0,dest_map=dest,dest_warp_id=str(index))
 # Houses use the same canonical HGSS room matrix as Ecruteak; copy its original
 # GBA furniture layout, not the old generic blank room. Preserve guest-rest scripts.
 for n in ['VioletCity_Residence','VioletCity_Workshop']:
  m=copy.deepcopy(load('crossroads/hgss/contracts/violet-qa06.json')['maps'][n]);base=load('data/maps/EcruteakCity_Residence/map.json');l=ls[base['layout']];data=list(struct.unpack('<110H',(R/l['blockdata_filepath']).read_bytes()));m['object_events'][0].update(x=5,y=5)
  if len(m['object_events'])>1:m['object_events'][1].update(x=8,y=7)
  m['warp_events']=[warp(4,8,c['id'],3 if n.endswith('Residence') else 4),warp(5,8,c['id'],3 if n.endswith('Residence') else 4)];m['bg_events']=[];m['coord_events']=[];save(m,data,11,10,ROOM_HEADERS[n],dedicated=True)
 # Source school desks/blackboard; all stairs/door clearance is deliberately free.
 n='VioletAcademy';m=copy.deepcopy(load('crossroads/hgss/contracts/violet-qa06.json')['maps'][n]);room=project(ROOM_HEADERS[n],bounds=(17,13),facts=facts);data=room['tiles'];w,h=17,13
 def stamp(part,x,y,data,w,h):
  a=ART[part]
  for yy in range(a['height']):
   for xx in range(a['width']):
    if 0<=x+xx<w and 0<=y+yy<h:data[(y+yy)*w+x+xx]=(data[(y+yy)*w+x+xx]&0xfc00)|a['start']+yy*a['width']+xx
 for x,y in [(3,6),(7,6),(3,8),(7,8),(5,4)]:stamp('prayer_table',x,y,data,w,h)
 stamp('television',5,1,data,w,h);stamp('cabinet',1,2,data,w,h)
 m['object_events'][0].update(x=6,y=5)
 template=m['object_events'][0]
 for x,y in [(3,7),(8,7),(4,9),(9,9)]:m['object_events'].append(obj(template,x,y,'HgssViolet_Student','OBJ_EVENT_GFX_BOY_1' if x%2 else 'OBJ_EVENT_GFX_GIRL_1'))
 m['object_events']=m['object_events'][:5];m['warp_events']=[warp(6,11,c['id'],5),warp(7,11,c['id'],8)];m['bg_events']=[];m['coord_events']=[]
 for e in m['warp_events']:data[e['y']*w+e['x']]=ART['exit']['start']
 save(m,data,w,h,ROOM_HEADERS[n])
 # Dedicated native service rooms preserve the existing nurse/clerk scripts and
 # local IDs. No reward/trade/online source scripts are imported.
 for n,base_name,header,city_index in [('VioletCity_PokemonCenter_1F','EcruteakCity_PokemonCenter_1F','MAP_VIOLET_POKECENTER_1F',0),('VioletCity_Mart','EcruteakCity_Mart','MAP_VIOLET_POKEMART',1)]:
  m=load(f'data/maps/{n}/map.json');base=load(f'data/maps/{base_name}/map.json');bl=ls[base['layout']];w,h=bl['width'],bl['height'];data=list(struct.unpack('<'+str(w*h)+'H',(R/bl['blockdata_filepath']).read_bytes()));actors=copy.deepcopy(base['object_events'])
  for old,new in zip(m['object_events'],actors):new['script']=old['script'];new['local_id']=old.get('local_id',new.get('local_id'))
  for o in actors:
   if o.get('local_id') is None:o.pop('local_id',None)
  m['object_events']=actors;m['warp_events']=copy.deepcopy(base['warp_events'])
  for e in m['warp_events'][:2]:e.update(dest_map=c['id'],dest_warp_id=str(city_index))
  if n.endswith('PokemonCenter_1F'):m['warp_events'][2].update(dest_map='MAP_VIOLET_CITY_POKEMON_CENTER_B1F',dest_warp_id='0')
  m['coord_events']=[];m['bg_events']=copy.deepcopy(base['bg_events']);save(m,data,w,h,header,secondary=bl['secondary_tileset'],dedicated=True)
 n='VioletCity_PokemonCenter_B1F';base=load('data/maps/EcruteakCity_PokemonCenter_B1F/map.json');m=copy.deepcopy(base);m.update(name=n,id='MAP_VIOLET_CITY_POKEMON_CENTER_B1F',region_map_section='MAPSEC_VIOLET_CITY');m['warp_events'][0].update(dest_map=maps['VioletCity_PokemonCenter_1F']['id'],dest_warp_id='2');bl=ls[base['layout']];data=list(struct.unpack('<204H',(R/bl['blockdata_filepath']).read_bytes()));save(m,data,17,12,'MAP_VIOLET_POKECENTER_B1F',secondary=bl['secondary_tileset'],dedicated=True)
 # Source Gym maze/lift platform flattened to fixed GBA access. No trainer roster,
 # Falkner badge award or mandatory battle is invented for this map pass.
 n='VioletCity_Gym';m=load(f'data/maps/{n}/map.json');f=facts['MAP_VIOLET_GYM']['chunks'][0]['permissions'];ox,oy,w,h=7,2,18,28;data=[0x600]*(w*h)
 for y in range(h):
  for x in range(w):
   sx,sy=x+ox,y+oy
   if 8<=sx<=22 and 4<=sy<=28 and not f[sy*32+sx]&0x8000:data[y*w+x]=0x3000|ART['wood']['start']
 for y in range(19-oy,25-oy):data[y*w+15-ox]=0x3000|ART['ladder']['start']+(y%2)
 m['object_events'][0].update(x=14-ox,y=26-oy);m['object_events']=m['object_events'][:1];m['warp_events']=[warp(15-ox,28-oy,c['id'],2),warp(16-ox,28-oy,c['id'],7)];m['bg_events']=[];m['coord_events']=[]
 for e in m['warp_events']:data[e['y']*w+e['x']]=ART['exit']['start']
 save(m,data,w,h,'MAP_VIOLET_GYM')
 # Three canonical Sprout floors and all stair branches. Retain old primary
 # down/up indices, append source aliases rather than deleting working IDs.
 floor_names=['SproutTower_1F','SproutTower_2F','SproutTower_3F'];floor_maps={n:load(f'data/maps/{n}/map.json') for n in floor_names};mapping={1:{0:1,1:0,2:2,3:3,4:4,5:5,6:6},2:{0:0,1:2,2:3,3:1},3:{0:0}}
 for level,n in enumerate(floor_names,1):
  m=floor_maps[n];header=f'MAP_SPROUT_TOWER_{level}F';room=project(header,bounds=(32,32),facts=facts);data=room['tiles'];w=h=32;events=[None]*len(facts[header]['warps'])
  for i,e in enumerate(facts[header]['warps']):
   if e['header']=='MAP_VIOLET':dest=c['id'];anchor=6
   else:
    dstlevel=int(e['header'].rsplit('_',1)[1][0]);dest=floor_maps[f'SproutTower_{dstlevel}F']['id'];anchor=mapping[dstlevel][e['anchor']]
   events[mapping[level][i]]=warp(e['x'],e['z'],dest,anchor);data[e['z']*w+e['x']]=ART['exit']['start'] if e['header']=='MAP_VIOLET' else warp_tile(data[e['z']*w+e['x']])
  m['warp_events']=events;m['coord_events']=[]
  occupied={(e['x'],e['y']) for e in events};safe={(x,y) for x,y in room['walkable'] if not data[y*w+x]&0xc00}
  for e in m['object_events']+m['bg_events']:
   options=[p for p in safe-occupied if sum((p[0]+dx,p[1]+dy) in safe-occupied for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)])>=3];x,y=min(options,key=lambda p:(abs(p[0]-18)+abs(p[1]-24),p));e.update(x=x,y=y);occupied.add((x,y))
  save(m,data,w,h,header)
 # Gatehouses use the verified source floor/pillar geometry and safe city/route
 # destinations. Current external routes are preserved pending their own rebuild.
 for direction,route_name,city_index,route_x,route_y in [('West','JohtoRoute36',9,55,14),('East','JohtoRoute31',11,0,14)]:
  n='VioletCity_'+direction+'Gate';header=ROOM_HEADERS[n];m=copy.deepcopy(load('data/maps/EcruteakCity_WestGate/map.json'));m.update(name=n,id='MAP_VIOLET_CITY_'+direction.upper()+'_GATE',layout='LAYOUT_HGSS_'+n.upper(),region_map_section='MAPSEC_VIOLET_CITY',object_events=[],warp_events=[],bg_events=[],coord_events=[]);room=project(header,'stone',facts=facts);w,h=room['width'],room['height'];data=room['tiles'];route=patch_neighbor(route_name,load(f'data/maps/{route_name}/map.json'));index=len(route['warp_events'])-1;js(f'data/maps/{route_name}/map.json',route)
  # Canonical source order in both gatehouses: city endpoint0, route endpoint1.
  for i,e in enumerate(facts[header]['warps']):m['warp_events'].append(warp(e['x'],e['z'],c['id'] if i==0 else route['id'],city_index if i==0 else index));data[e['z']*w+e['x']]=0x3000|ART['stone_warp']['start']
  template=load('data/maps/EcruteakCity_WestGate/map.json')['object_events'][0];m['object_events']=[obj(template,5,6,'HgssViolet_'+direction+'GateGuide')];save(m,data,w,h,header,dedicated=True)
 # Southern route keeps its old geography; update only reciprocal seam/buffer.
 r32=load('data/maps/JohtoRoute32/map.json');next(e for e in r32['connections'] if e['map']==c['id'])['offset']=-9;js('data/maps/JohtoRoute32/map.json',r32)
 # Match the two native road elevations at the top, retaining all other cells.
 rl=ls[r32['layout']];rl['primary_tileset']='gTileset_HgssVioletRoutePrimary'
 contract=load('crossroads/hgss/contracts/violet-qa06.json');rb=bytes.fromhex(contract['route32_raw_hex']);rw,rh=rl['width'],rl['height'];rt=list(struct.unpack('<'+str(rw*rh)+'H',rb))
 for y in range(7):
  for x in range(rw):
   id=rt[y*rw+x]&1023
   if id>=512:rt[y*rw+x]=(rt[y*rw+x]&~1023)|(0x1ff if not rt[y*rw+x]&0xc00 else 0xc6)
  for x in (14,15):rt[y*rw+x]=0x31ff
 write(rl['blockdata_filepath'],struct.pack('<'+str(len(rt))+'H',*rt))
 # A paired source portal gets nonanimated warp behavior, not a bare road tile.
 for i,e in enumerate(c['warp_events'][9:],9):
  if i in [10,11,12]:put(e['x'],e['y'],0x3000|art['portal']['start'])
 l=layout(c,W,H,'gTileset_HgssVioletSecondary','gTileset_HgssVioletPrimary');write('crossroads/hgss/authoring/VioletCity.bin',struct.pack('<'+str(W*H)+'H',*t));author=dict(map=c,layout=copy.deepcopy(l),gym_warp=2,gym_alias=7,interior=maps['VioletCity_Gym'],raw_path='crossroads/hgss/authoring/VioletCity.bin');js('crossroads/hgss/authoring/VioletCity.json',author)
 from build_eight_gym_integration import relocate_layout
 relocate_layout('VioletCity',l)
 for n,v in raw_rooms.items():write(f'crossroads/hgss/authoring/{n}.bin',struct.pack('<'+str(len(v['data']))+'H',*v['data']))
 js('data/maps/VioletCity/map.json',c);write(l['blockdata_filepath'],struct.pack('<'+str(W*H)+'H',*t));write(l['border_filepath'],struct.pack('<4H',*([0x4c6]*4)))
 reviews.insert(0,dict(name='VioletCity',source_header='MAP_VIOLET',origin_translation=[0,8],dimensions=[64,72],runtime_qa='pending for this source tree',owner_visual_qa='pending',adaptations=['Eight-row north padding preserves full2D tower, same relative HGSS coordinates','Owner custom Gym replaces source facade','DS lift is fixed GBA access; no badge/battle gate','Legacy Workshop/Residence IDs now occupy the two actual canonical houses','Gate rooms replace old direct west/east debug borders; outside routes remain unreconstructed']))
 for n in NEW:
  if n not in groups['gMapGroup_CrossroadsJohtoExpansion']:groups['gMapGroup_CrossroadsJohtoExpansion'].append(n)
  if not any(p['name']==n for p in manifest['planned']):manifest['planned'].append(dict(name=n,kind='hgss',parent='VioletCity',cluster='central',status='reference-runtime-review-pending'))
  write(f'data/maps/{n}/scripts.inc',n+'_MapScripts::\n    .byte 0\n')
 for p in manifest['planned']:
  if p['name'] in maps or p['name']=='VioletCity':p['kind']='hgss';p['status']='reference-runtime-review-pending'
 js('data/maps/map_groups.json',groups);js('data/layouts/layouts.json',layouts);js('crossroads/johto/manifest.json',manifest);js('crossroads/hgss/violet-review.json',reviews)
 heals=load('src/data/heal_locations.json');next(e for e in heals['heal_locations'] if e['id']=='HEAL_LOCATION_VIOLET_CITY').update(x=49,y=56,respawn_x=8,respawn_y=13);js('src/data/heal_locations.json',heals)
 inc=(R/'data/event_scripts.s').read_text()
 for n in NEW:
  line=f'\t.include "data/maps/{n}/scripts.inc"'
  if line not in inc:inc+='\n'+line+'\n'
 line='\t.include "crossroads/scripts/hgss_violet.inc"'
 if line not in inc:inc+='\n'+line+'\n'
 write('data/event_scripts.s',inc)
 print('Canonical Violet ground/doors and twelve interior/gate/floor maps generated; runtime/visual QA required.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');generate(p.parse_args().check)
