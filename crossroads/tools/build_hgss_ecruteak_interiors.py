#!/usr/bin/env python3
"""Ecruteak canonical tower geometry/graph with stable legacy map/layout IDs."""
import json,struct,copy,argparse
from collections import deque
from johto_movement import next_position
from pathlib import Path
from hgss_room_projection import project,ART,FACTS,warp_tile
R=Path(__file__).resolve().parents[2]
BELL={f'MAP_BELL_TOWER_{i}F':('EcruteakCity_BellTower' if i==1 else f'EcruteakCity_BellTower_{i}F') for i in range(1,11)}
BELL['MAP_BELL_TOWER_ROOF']='EcruteakCity_BellTower_Roof'
TARGETS={**BELL,'MAP_BURNED_TOWER_1F':'EcruteakCity_BurnedTower','MAP_BURNED_TOWER_B1F':'EcruteakCity_BurnedTower_B1F'}
NEW=['EcruteakCity_BellTower_10F','EcruteakCity_BellTower_Roof']
def load(p):return json.loads((R/p).read_text())
def generate(check=False):
 def write(p,b):
  if isinstance(b,str):b=b.encode()
  p=R/p
  if check:assert p.exists() and p.read_bytes()==b,('Regenerate HGSS interiors',str(p))
  elif not p.exists() or p.read_bytes()!=b:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 def js(p,v):write(p,json.dumps(v,indent=2)+'\n')
 maps={};layouts=load('data/layouts/layouts.json');bylayout={l['id']:l for l in layouts['layouts']};groups=load('data/maps/map_groups.json');manifest=load('crossroads/johto/manifest.json');plans={p['name']:p for p in manifest['planned']}
 template=load('data/maps/EcruteakCity_BellTower_9F/map.json')
 for header,name in TARGETS.items():
  path=R/f'data/maps/{name}/map.json'
  if path.exists():m=load(f'data/maps/{name}/map.json')
  else:
   m=copy.deepcopy(template);suffix=name.removeprefix('EcruteakCity_').replace('_','').upper();m.update(id='MAP_ECRUTEAKCITY_'+suffix,name=name,layout='LAYOUT_HGSS_'+suffix,object_events=[],bg_events=[],warp_events=[])
  maps[header]=m
 # Canonical source indices map onto the old primary down/up warp indices.
 orders={h:list(range(len(FACTS[h]['warps']))) for h in TARGETS}
 orders['MAP_BELL_TOWER_5F']=[0,3,1,2,4]
 source_to_native={h:{source:i for i,source in enumerate(order)} for h,order in orders.items()}
 for h in ['MAP_BELL_TOWER_1F','MAP_BURNED_TOWER_1F']:
  source_to_native[h]={k:(0 if k==0 else k+1) for k in range(len(FACTS[h]['warps']))}
 legacy_bells=[copy.deepcopy(o) for o in maps['MAP_BELL_TOWER_9F']['object_events'] if o['script']=='Area_RingBell']
 review=[]
 for header,name in TARGETS.items():
  m=maps[header];theme='burned_floor' if header=='MAP_BURNED_TOWER_1F' else 'stone' if header in ['MAP_BURNED_TOWER_B1F','MAP_BELL_TOWER_ROOF'] else 'wood';room=project(header,theme,bounds=(32,32))
  seen=room['walkable'];ox=oy=4;oldw=oldh=28;w=h=24
  if header=='MAP_BELL_TOWER_ROOF':ox=oy=0;oldw=oldh=32;w=h=32
  # Fixed architectural envelope preserves the decorative cross-braces around
  # narrow upper-floor paths instead of shrinking the building to its walkway.
  tiles=[v for y in range(oy,oldh) for v in room['tiles'][y*32+ox:y*32+oldw]]
  if header=='MAP_BELL_TOWER_ROOF':
   # A2D rooftop, with the original source platform/ladder footprint. Slopes
   # are scenery, not hidden passable ground. No legendary actor/event.
   for y in range(10,31):
    for x in range(2,30):
     if (x,y) not in seen:tiles[y*w+x]=0x400|ART['roof_skin']['start']
   for part,x,y in [('roof_nw',2,10),('roof_ne',28,10),('roof_sw',2,28),('roof_se',28,28)]:
    a=ART[part]
    for yy in range(a['height']):
     for xx in range(a['width']):tiles[(y+yy)*w+x+xx]=0x400|a['start']+yy*a['width']+xx
   for y in range(12,19):
    for x in range(12,19):tiles[y*w+x]=(0x3000 if (x,y) in seen else 0x400)|ART['stone']['start']
   for y in range(19,25):
    a=ART['ladder_stone'];tiles[y*w+15]=0x3000|a['start']+(y%2)*a['width']
   a=ART['gold_spire_roof_skin']
   for yy in range(a['height']):
    for xx in range(a['width']):
     x,y=14+xx,10+yy;tiles[y*w+x]=(0x3000 if (x,y) in seen else 0x400)|a['start']+yy*a['width']+xx
   for x,y in [(12,11),(18,11)]:
    a=ART['statue_stone']
    for yy in range(a['height']):tiles[(y-1+yy)*w+x]=0x400|a['start']+yy*a['width']
  events=[None]*(max(source_to_native[header].values())+1)
  for i,e in enumerate(FACTS[header]['warps']):
   dest=e['header'];dest_index=e['anchor'];x,y=e['x']-ox,e['z']-oy
   if dest in TARGETS:dest_map=maps[dest]['id'];dest_index=source_to_native[dest][dest_index]
   elif dest=='MAP_BELLCHIME_TOWER':dest_map='MAP_BELLCHIME_TRAIL';dest_index=1
   elif dest=='MAP_ECRUTEAK':dest_map='MAP_ECRUTEAK_CITY';dest_index=0
   else:raise AssertionError(('Unexpected tower destination',header,e))
   events[source_to_native[header][i]]=dict(x=x,y=y,elevation=0,dest_map=dest_map,dest_warp_id=str(dest_index))
   behavior=room['permissions'][e['z']*room['source_width']+e['x']]&255
   tiles[y*w+x]=ART['exit']['start'] if dest not in TARGETS else 0x3000|ART['panel']['start'] if behavior==103 else warp_tile(tiles[y*w+x])
  if header in ['MAP_BELL_TOWER_1F','MAP_BURNED_TOWER_1F']:
   events[1]=dict(events[0],x=events[0]['x']+1);e=events[1];tiles[e['y']*w+e['x']]=ART['exit']['start']
  assert all(events);m['warp_events']=events
  # Preserve ambient interactions and scripts; no HGSS story actors/flags imported.
  if header=='MAP_BELL_TOWER_ROOF' and not m['object_events']:
   m['object_events']=copy.deepcopy(legacy_bells)
  m['object_events']=[o for o in m['object_events'] if header not in ['MAP_BELL_TOWER_9F','MAP_BELL_TOWER_ROOF'] or o['script']!='Area_RingBell']
  if header=='MAP_BELL_TOWER_ROOF':m['bg_events']=[dict(type='sign',x=15,y=15,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='Area_RingBell')]
  occupied={(e['x'],e['y']) for e in events};safe={(x-ox,y-oy) for x,y in seen if ox<=x<oldw and oy<=y<oldh and not (tiles[(y-oy)*w+x-ox]&0xc00)}
  # An ambient actor must never seal a narrow source puzzle passage.
  attrs=struct.unpack('<'+str((R/'data/tilesets/secondary/hgss_temple/metatile_attributes.bin').stat().st_size//2)+'H',(R/'data/tilesets/secondary/hgss_temple/metatile_attributes.bin').read_bytes())
  warp_points={(e['x'],e['y']) for e in events};public=safe|warp_points;reverse={}
  def behavior(a,b):
   if not(0<=a<w and 0<=b<h):return None
   return attrs[(tiles[b*w+a]&1023)-512]&255
  for X,Y in public:
   for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
    to=next_position(X,Y,dx,dy,behavior)
    if to in public:reverse.setdefault(to,[]).append((X,Y))
  actor_tiles=set()
  def leaves_exits_open(candidate):
   blocked=actor_tiles|{candidate};reachable=set(warp_points);q=deque(warp_points)
   while q:
    for point in reverse.get(q.popleft(),[]):
     if point not in blocked and point not in reachable:reachable.add(point);q.append(point)
   return public-blocked<=reachable
  preferred={'Area_BellCaretaker':(8-ox,8-oy),'Area_BurnedCaretaker':(7-ox,10-oy),'Area_BurnedVisitor':(15-ox,23-oy),'Area_RingBell':(15-ox,14-oy),'Area_TowerVisitor':(16-ox,24-oy)}
  for o in m['object_events']:
   if o['script'] in ['Area_BellCaretaker','Area_BurnedCaretaker']:o['graphics_id']='OBJ_EVENT_GFX_ECRUTEAK_MONK'
   target=preferred.get(o['script'],(w//2,h//2));choices=[p for p in safe-occupied if any((p[0]+dx,p[1]+dy) in safe-occupied for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)])];assert choices,(name,'No safe NPC location')
   choices.sort(key=lambda p:(abs(p[0]-target[0])+abs(p[1]-target[1]),p));point=next((p for p in choices if leaves_exits_open(p)),None);assert point is not None,(name,'No NPC placement preserves escape');x,y=point;o.update(x=x,y=y);occupied.add(point);actor_tiles.add(point)
  for e in m['bg_events']:
   if header=='MAP_BELL_TOWER_ROOF':continue
   choices=safe-occupied;x,y=min(choices,key=lambda p:abs(p[0]-w//2)+abs(p[1]-h//2));e.update(x=x,y=y)
  m['music']='MUS_MT_PYRE';m['allow_cycling']=False
  lid=m['layout'];l=dict(id=lid,name=name+'_Layout',width=w,height=h,primary_tileset='gTileset_Building',secondary_tileset='gTileset_HgssTemple',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin',layout_version='emerald')
  if lid in bylayout:bylayout[lid].clear();bylayout[lid].update(l)
  else:layouts['layouts'].append(l);bylayout[lid]=l
  js(f'data/maps/{name}/map.json',m);write(l['blockdata_filepath'],struct.pack('<'+str(w*h)+'H',*tiles));write(l['border_filepath'],struct.pack('<4H',*([0x400|ART['void']['start']]*4)))
  if name in NEW:
   group=groups['gMapGroup_CrossroadsJohtoExpansion']
   if name not in group:group.append(name)
   if name not in plans:manifest['planned'].append(dict(name=name,kind='hgss',parent='EcruteakCity_BellTower',cluster='west',status='reference-runtime-review-pending'))
   write(f'data/maps/{name}/scripts.inc',name+'_MapScripts::\n    .byte 0\n')
  review.append(dict(name=name,source_header=header,source=FACTS[header]['source'],source_to_native_warps=source_to_native[header],origin_crop=[ox,oy],dimensions=[w,h],reference_geometry='projected; ledge/warp traversal requires runtime validation',visual_qa='pending',adaptations=['Original GBA-compatible temple art, no HGSS graphics copied','DS coordinates translated to crop unused matrix margin; no relative layout change','Existing legacy exterior warp aliases preserved where applicable']))
 js('data/layouts/layouts.json',layouts);js('data/maps/map_groups.json',groups);js('crossroads/johto/manifest.json',manifest);js('crossroads/hgss/interior-review.json',review)
 inc=(R/'data/event_scripts.s').read_text()
 for name in NEW:
  line=f'\t.include "data/maps/{name}/scripts.inc"'
  if line not in inc:inc+='\n'+line+'\n'
 write('data/event_scripts.s',inc)
 print('Projected',len(TARGETS),'canonical tower floors; missing10F/roof appended. Visual/runtime review required.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');generate(p.parse_args().check)
