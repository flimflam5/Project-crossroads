#!/usr/bin/env python3
"""Independent canonical anchors, saved IDs, local/branched exits and escape.

Exact reference coordinates supplement the generator check. This is a structural
test, never a claim of visual acceptance or actual emulator playtesting.
"""
import copy,json,re,struct
from pathlib import Path
from collections import deque
from johto_movement import next_position
from build_hgss_violet import OWNED,NEW,patch_neighbor,neighbor_tiles
R=Path(__file__).resolve().parents[2]
def validate():
 from validate_violet_service_preservation import validate as preserved_services
 preserved_services()
 def load(p):return json.loads((R/p).read_text())
 contract=load('crossroads/hgss/contracts/violet-qa06.json');ls={l['id']:l for l in load('data/layouts/layouts.json')['layouts']};groups=load('data/maps/map_groups.json')
 for key,old in contract['groups'].items():
  assert groups[key][:len(old)]==old,(key,'Existing map IDs changed')
 tail=groups['gMapGroup_CrossroadsJohtoExpansion'][len(contract['groups']['gMapGroup_CrossroadsJohtoExpansion']):]
 # Violet's three new IDs remain at the exact original ordinals. The later
 # explicitly contracted Olivine increment appends after them, never shifts
 # them. All Violet map/layout/terrain/heal assertions below remain unchanged.
 olivine_new=['OlivineCity_FishingHouse','OlivineCity_TradeHouse','OlivineCity_SealHouse','OlivineCity_Cafe','OlivineCity_PokemonCenter_B1F','OlivineCity_Lighthouse_Balcony','OlivineCity_Lighthouse_Elevator','OlivineCity_PortTerminal','OlivineCity_PortQuay'] if (R/'crossroads/hgss/authoring/OlivineCity.json').exists() else []
 assert tail==NEW+olivine_new,('Violet IDs shifted or uncontracted appended maps',tail)
 maps={n:load(f'data/maps/{n}/map.json') for n in OWNED};ids={m['id']:n for n,m in maps.items()};raw={};size={};attrs={};actors={}
 paths=dict(re.findall(r'const u16 (gMetatileAttributes_\w+)\[\] = INCBIN_U16\("([^"]+)"\)',(R/'src/data/tilesets/metatiles.h').read_text()))
 for key,body in re.findall(r'const struct Tileset (gTileset_\w+)\s*=\s*\{([^}]+)\}',(R/'src/data/tilesets/headers.h').read_text(),re.S):
  hit=re.search(r'\.metatileAttributes\s*=\s*(\w+)',body)
  if hit and hit[1] in paths:
   b=(R/paths[hit[1]]).read_bytes();attrs[key]=struct.unpack('<'+str(len(b)//2)+'H',b)
 for n,m in maps.items():
  if n in contract['maps']:
   old=contract['maps'][n]
   for key in ['id','name','region','region_map_section','map_type','music','allow_escaping','requires_flash']:assert m[key]==old[key],(n,'Preserved header',key)
   old_scripts={e['script'] for e in old['object_events']};assert old_scripts<={e['script'] for e in m['object_events']},(n,'Lost accepted actor')
  l=ls[m['layout']];w,h=l['width'],l['height'];assert (w+14)*(h+14)<=10240
  b=(R/l['blockdata_filepath']).read_bytes();assert len(b)==2*w*h;raw[n]=struct.unpack('<'+str(w*h)+'H',b);size[n]=(w,h);actors[n]={(o['x'],o['y']) for o in m['object_events']}
  assert len(actors[n])==len(m['object_events'])<=16
  for x,y in actors[n]:assert not raw[n][y*w+x]&0xc00,(n,'Actor in solid object',x,y)
  for e in m['warp_events']:assert 0<=e['x']<w and 0<=e['y']<h and not raw[n][e['y']*w+e['x']]&0xc00,(n,'Blocked/outside portal',e)
 c=maps['VioletCity'];expected=[(49,55),(21,41),(31,41),(36,61),(11,38),(47,41),(39,12),(32,41),(46,41),(6,30),(6,31),(63,53),(63,54)]
 assert [(e['x'],e['y']) for e in c['warp_events']]==expected
 assert c['connections']==[dict(map='MAP_JOHTO_ROUTE32',direction='down',offset=9)]
 world=load('crossroads/hgss/canonical_events/johto-outdoor-geometry.json')['areas']['MAP_VIOLET'];assert world['origin']==[448,224]
 for n in ['JohtoRoute31','JohtoRoute32','JohtoRoute36']:
  m=load(f'data/maps/{n}/map.json');assert m==patch_neighbor(n,copy.deepcopy(contract['maps'][n])),(n,'Unrelated neighbor events changed')
  l=ls[m['layout']];old=bytes.fromhex(contract['route'+n[10:]+'_raw_hex']);assert (R/l['blockdata_filepath']).read_bytes()==neighbor_tiles(n,old,l['width'],l['height']),(n,'Unrelated route terrain changed')
  expected=copy.deepcopy(contract['layouts'][m['layout']])
  if n=='JohtoRoute32':
   expected['primary_tileset']='gTileset_HgssVioletRoutePrimary';assert all(v&1023!=0x1ff for v in struct.unpack('<'+str(len(old)//2)+'H',old))
  assert l==expected,(n,'Unrelated route layout changed')
 gm=list(struct.unpack('<4096H',(R/'data/tilesets/primary/general/metatiles.bin').read_bytes()));actual=list(struct.unpack('<4096H',(R/'data/tilesets/primary/hgss_violet/metatiles.bin').read_bytes()));gm[0x1ff*8:0x200*8]=[0x30aa,0x30ab,0x30aa,0x30ab,0,0,0,0];assert actual==gm,'Only the unused shared-buffer paving metatile may differ'
 bridge=load('crossroads/hgss/art/violet/manifest.json')['specs']['bridge']
 for first in [18,29]:
  for y in range(5):
   for x in range(5):assert raw['VioletCity'][(first+y)*64+37+x]==bridge['start']+y*5+x+(0x400 if x in [0,4] else 0x3000),'Canonical bridge span/rail collision changed'
 # Preserve old primary up/down indices; match every source stair and branch.
 facts=load('crossroads/hgss/canonical_events/violet-interior-geometry.json');mapping={1:{0:1,1:0,2:2,3:3,4:4,5:5,6:6},2:{0:0,1:2,2:3,3:1},3:{0:0}}
 for level in range(1,4):
  m=maps[f'SproutTower_{level}F'];f=facts[f'MAP_SPROUT_TOWER_{level}F']
  assert len(m['warp_events'])==len(f['warps'])
  for i,e in enumerate(f['warps']):
   a=m['warp_events'][mapping[level][i]];assert (a['x'],a['y'])==(e['x'],e['z'])
   if e['header']=='MAP_VIOLET':assert a['dest_map']==c['id'] and int(a['dest_warp_id'])==6
   else:
    dstlevel=int(e['header'].rsplit('_',1)[1][0]);assert a['dest_map']==maps[f'SproutTower_{dstlevel}F']['id'] and int(a['dest_warp_id'])==mapping[dstlevel][e['anchor']]
 def behavior(n,x,y):
  w,h=size[n]
  if not(0<=x<w and 0<=y<h):return None
  l=ls[maps[n]['layout']];tile=raw[n][y*w+x]&1023;return attrs[l['primary_tileset'] if tile<512 else l['secondary_tileset']][tile%512]&255
 nodes=set();edges={};reverse={};outside=set()
 for n,m in maps.items():
  w,h=size[n];doors={(e['x'],e['y']) for e in m['warp_events']}
  for y in range(h):
   for x in range(w):
    if (x,y) not in actors[n] and (not raw[n][y*w+x]&0xc00 or (x,y) in doors):nodes.add((n,x,y))
 for state in nodes:
  n,x,y=state;m=maps[n];dest=[]
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   to=next_position(x,y,dx,dy,lambda a,b:behavior(n,a,b))
   if to is not None and (n,*to) in nodes:dest.append((n,*to))
  for e in m['warp_events']:
   if (x,y)!=(e['x'],e['y']):continue
   if e['dest_map'] in ids:
    dst=ids[e['dest_map']];back=maps[dst]['warp_events'][int(e['dest_warp_id'])];assert back['dest_map']==m['id'];dest.append((dst,back['x'],back['y']))
   else:outside.add(state)
  if n=='VioletCity' and y==71 and x in [23,24]:outside.add(state)
  edges[state]=dest
  for to in dest:reverse.setdefault(to,[]).append(state)
 def flood(graph):
  seen=set(outside);q=deque(seen)
  while q:
   for to in graph.get(q.popleft(),[]):
    if to not in seen:seen.add(to);q.append(to)
  return seen
 forward=flood(edges);escapes=flood(reverse)
 for n,m in maps.items():
  for e in m['warp_events']:
   p=(n,e['x'],e['y']);assert p in forward and p in escapes,(n,'Unreachable/trapped canonical exit',e)
  for e in m['object_events']+m['bg_events']:
   assert {(n,e['x']+dx,e['y']+dy) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(2,0),(-2,0),(0,2),(0,-2)]}&forward,(n,'Unreachable interaction',e)
 assert nodes<=escapes,('Trapped public Violet floor',len(nodes-escapes),sorted(nodes-escapes)[:18])
 heal=next(e for e in load('src/data/heal_locations.json')['heal_locations'] if e['id']=='HEAL_LOCATION_VIOLET_CITY');old=next(e for e in contract['heals']['heal_locations'] if e['id']==heal['id']);assert heal==dict(old,x=49,y=56,respawn_x=8,respawn_y=13)
 assert ('VioletCity',49,56) in forward and ('VioletCity_PokemonCenter_1F',8,13) in forward
 print('Canonical Violet door/stair coordinates, retained map/save IDs, exact neighbor changes and every-tile escape: PASS',len(nodes),'tiles in',len(maps),'maps')
 return set(OWNED)|{'JohtoRoute31','JohtoRoute32','JohtoRoute36'}
if __name__=='__main__':validate()
