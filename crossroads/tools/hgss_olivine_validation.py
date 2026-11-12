"""Explicit Olivine source graph, native dynamic lift and every-tile escape.

Replaces only generic fixed-reciprocal/single-room assumptions for these mapped
HGSS floors. All source coordinates, aliases and the one-way window are pinned
independently; unrelated doors retain the ordinary reciprocity assertions.
"""
import json,re,struct
from collections import deque
from pathlib import Path
from johto_movement import next_position
R=Path(__file__).resolve().parents[2]
LH=[f'OlivineCity_Lighthouse_{i}F' for i in range(1,7)]
BAL='OlivineCity_Lighthouse_Balcony';LIFT='OlivineCity_Lighthouse_Elevator';PORT='OlivineCity_PortTerminal';QUAY='OlivineCity_PortQuay'
def active():return (R/'crossroads/hgss/authoring/OlivineCity.json').exists()
def load(p):return json.loads((R/p).read_text())
def dynamic_destinations(n,e,maps):
 if e['dest_map']!='MAP_DYNAMIC':return None
 assert active() and n==LIFT and (e['x'],e['y']) in [(3,6),(4,6)] and e['dest_warp_id']=='WARP_ID_DYNAMIC',('Unexpected dynamic warp',n,e)
 # Either panel really sets the native dynamicWarp. The script/panel access
 # itself is independently checked below and controller-tested by the harness.
 return [(LH[0],maps[LH[0]]['warp_events'][3]),(LH[5],maps[LH[5]]['warp_events'][1])]
def dynamic_pair(n,index,e,maps,ids):
 if e['dest_map']=='MAP_DYNAMIC':dynamic_destinations(n,e,maps);return True
 if active() and n in [LH[0],LH[5]] and e['dest_map']==maps[LIFT]['id']:
  expected={LH[0]:{3:(8,4,0),4:(9,4,1)},LH[5]:{1:(8,4,0),2:(9,4,1)}}
  assert index in expected[n] and (e['x'],e['y'],int(e['dest_warp_id']))==expected[n][index]
  assert maps[LIFT]['warp_events'][int(e['dest_warp_id'])]['dest_map']=='MAP_DYNAMIC'
  return True
 return False
def extra_edges(n,x,y):
 return [(BAL,14,9)] if active() and n==LH[3] and (x,y)==(16,9) else []
def validate_olivine_graph():
 if not active():return set()
 from validate_hgss_olivine import validate
 validate()
 # Validate the seven exact Aqua floors/components before extending this
 # every-tile graph. This is not a generic exemption for disconnected rooms.
 aqua_names=['SSAqua_1F','SSAqua_CaptainRoom','SSAqua_SoutheastCabins','SSAqua_SouthwestCabins','SSAqua_NortheastCabins','SSAqua_NorthwestCabins','SSAqua_B1F'] if (R/'data/maps/SSAqua_1F/map.json').exists() else []
 if aqua_names:
  from validate_ss_aqua import validate as validate_aqua
  aqua_report=validate_aqua()
  assert [row['map']for row in aqua_report['maps']]==aqua_names
  assert aqua_report['component_graph']==dict(ship_components=12,every_component_boardable_and_returnable=True)
 groups=load('data/maps/map_groups.json');names=[n for n in groups['gMapGroup_CrossroadsOlivine']+groups['gMapGroup_CrossroadsJohtoExpansion'] if(n.startswith('OlivineCity')and n!='OlivineCity')or n in aqua_names];maps={n:load(f'data/maps/{n}/map.json') for n in names};ids={m['id']:n for n,m in maps.items()};ls={l['id']:l for l in load('data/layouts/layouts.json')['layouts']};facts=load('crossroads/hgss/canonical_events/olivine-interior-geometry.json')
 source_headers={**{n:'MAP_OLIVINE_LIGHTHOUSE_'+(str(i)+'F' if i<6 else 'LIGHT_ROOM') for i,n in enumerate(LH,1)},BAL:'MAP_OLIVINE_LIGHTHOUSE_EXTERIOR',LIFT:'MAP_OLIVINE_LIGHTHOUSE_ELEVATOR',PORT:'MAP_SS_AQUA_OLIVINE_PORT_INTERIOR',QUAY:'MAP_SS_AQUA_OLIVINE_PORT_EXTERIOR'}
 source_mapping={LH[0]:{0:0,1:3,2:2},LH[1]:{0:0,1:1,2:2},LH[2]:{0:0,1:1,2:2,3:3,4:4,5:5},LH[3]:{0:0,1:3,2:1,3:2},LH[4]:{0:0,1:1,2:2},LH[5]:{0:0,1:1},BAL:{0:0},LIFT:{0:0},PORT:{0:0,1:1,2:2},QUAY:{0:0,2:1}}
 header_names={v:k for k,v in source_headers.items()}
 for n,mapping in source_mapping.items():
  m=maps[n];source=facts[source_headers[n]]
  for source_index,native_index in mapping.items():
   before=source['warps'][source_index];after=m['warp_events'][native_index]
   assert (after['x'],after['y'])==(before['x'],before['z']),(n,'Canonical source threshold moved',source_index,after)
   if before['header']==4095:assert dynamic_pair(n,native_index,after,maps,ids)
   elif before['header'] in header_names:
    to=header_names[before['header']];assert after['dest_map']==maps[to]['id'] and int(after['dest_warp_id'])==source_mapping[to][before['anchor']],(n,'Canonical destination changed',before,after)
   else:assert before['header']=='MAP_OLIVINE' and after['dest_map']=='MAP_OLIVINE_CITY'
 # Exact declarations, not a blanket exemption for coordinate warps.
 window=maps[LH[3]]['coord_events'];assert window==[dict(type='trigger',x=16,y=9,elevation=0,var='VAR_TEMP_0',var_value='0',script='Hgss_OlivineWindowDrop')]
 scripts=(R/'crossroads/scripts/hgss_olivine_landmarks.inc').read_text()
 block=re.search(r'^Hgss_OlivineWindowDrop::\n(.*?)(?=^\w+::|\Z)',scripts,re.M|re.S);assert block and re.search(r'^\s+warp MAP_OLIVINE_CITY_LIGHTHOUSE_BALCONY, 14, 9\s*$',block[1],re.M)
 for label,target,warp,x in [('Hgss_OlivineLift1F','MAP_OLIVINECITY_LIGHTHOUSE_1F',3,2),('Hgss_OlivineLift6F','MAP_OLIVINECITY_LIGHTHOUSE_6F',1,5)]:
  assert any(e['x']==x and e['y']==2 and e['script']==label for e in maps[LIFT]['bg_events'])
  block=re.search(r'^'+label+r'::\n(.*?)(?=^\w+::|\Z)',scripts,re.M|re.S);assert block and f'setdynamicwarp {target}, {warp}' in block[1] and 'goto_if_eq VAR_RESULT, NO' in block[1]
 for n,index in [(LH[0],3),(LH[5],1)]:assert f'setdynamicwarp {maps[n]["id"]}, {index}' in (R/f'data/maps/{n}/scripts.inc').read_text(),'Native lift must remember return floor on arrival'
 assert not re.search(r'^\s*(setflag|clearflag|givemon|giveitem|setvar VAR_CROSSROADS)',scripts,re.M),'Landmark scripts may not grant permanent progress'
 headers=(R/'src/data/tilesets/headers.h').read_text();meta=(R/'src/data/tilesets/metatiles.h').read_text();paths=dict(re.findall(r'const u16 (gMetatileAttributes_\w+)\[\] = INCBIN_U16\("([^" ]+)"\)',meta));attrs={}
 for symbol,body in re.findall(r'const struct Tileset (gTileset_\w+)\s*=\s*\{([^}]+)\}',headers,re.S):
  match=re.search(r'\.metatileAttributes\s*=\s*(\w+)',body)
  if match and match[1] in paths:
   b=(R/paths[match[1]]).read_bytes();attrs[symbol]=struct.unpack('<'+str(len(b)//2)+'H',b)
 raw={};size={};actors={};nodes=set();edges={};reverse={};outside=set()
 for n,m in maps.items():
  l=ls[m['layout']];w,h=l['width'],l['height'];size[n]=(w,h);b=(R/l['blockdata_filepath']).read_bytes();raw[n]=struct.unpack('<'+str(w*h)+'H',b);actors[n]={(e['x'],e['y']) for e in m['object_events']};doors={(e['x'],e['y']) for e in m['warp_events']}
  for y in range(h):
   for x in range(w):
    v=raw[n][y*w+x]
    if (x,y) not in actors[n] and ((not v&0xc00 and v>>12==3) or (x,y) in doors):nodes.add((n,x,y))
 def behavior(n,x,y):
  w,h=size[n]
  if not(0<=x<w and 0<=y<h):return None
  v=raw[n][y*w+x]&1023;l=ls[maps[n]['layout']];return attrs[l['primary_tileset'] if v<512 else l['secondary_tileset']][v%512]&255
 for state in nodes:
  n,x,y=state;m=maps[n];to=extra_edges(n,x,y)
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   p=next_position(x,y,dx,dy,lambda a,b:behavior(n,a,b))
   if p is not None and (n,*p) in nodes:to.append((n,*p))
  for i,e in enumerate(m['warp_events']):
   if (x,y)!=(e['x'],e['y']):continue
   dynamic=dynamic_destinations(n,e,maps)
   if dynamic is not None:to.extend((dst,back['x'],back['y']) for dst,back in dynamic)
   elif e['dest_map'] in ids:
    dst=ids[e['dest_map']];back=maps[dst]['warp_events'][int(e['dest_warp_id'])];to.append((dst,back['x'],back['y']))
   else:assert e['dest_map']=='MAP_OLIVINE_CITY';outside.add(state)
  assert all(p in nodes for p in to),('Arrival inside wall/outside public ground',state,[p for p in to if p not in nodes])
  edges[state]=to
  for target in to:reverse.setdefault(target,[]).append(state)
 def flood(seed,graph):
  seen=set(seed);q=deque(seed)
  while q:
   for p in graph.get(q.popleft(),[]):
    if p not in seen:seen.add(p);q.append(p)
  return seen
 forward=flood(outside,edges);escapes=flood(outside,reverse)
 for n,m in maps.items():
  for e in m['warp_events']:
   point=(n,e['x'],e['y']);assert point in forward and point in escapes,('Unreachable/trapped canonical exit',n,e)
  for e in m['object_events']+m['bg_events']:
   assert any((n,e['x']+dx,e['y']+dy) in forward for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(2,0),(-2,0),(0,2),(0,-2)]),('Unreachable Olivine interaction',n,e)
 assert nodes<=escapes,('Trapped Olivine public floor',sorted(nodes-escapes)[:24])
 assert (LH[3],16,9) in forward and (BAL,14,9) in escapes,'Source window/balcony return chain absent'
 print('HGSS Olivine/Aqua exact threshold graph, paired lift, source window, all12ship components and every public tile escape: PASS',len(nodes),'tiles',len(names),'interior maps')
 return set(names)
if __name__=='__main__':validate_olivine_graph()
