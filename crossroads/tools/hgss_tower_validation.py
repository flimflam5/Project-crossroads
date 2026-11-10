"""Strict reference graph/escape checks replacing generic single-aisle assumptions."""
from pathlib import Path
from collections import deque
import json,re,struct
from johto_movement import next_position
R=Path(__file__).resolve().parents[2]
def validate_towers():
 def load(p):return json.loads((R/p).read_text())
 review=load('crossroads/hgss/interior-review.json');facts=load('crossroads/hgss/canonical_events/ecruteak-interior-geometry.json');base=load('crossroads/hgss/contracts/ecruteak-interiors-qa04.json')['maps'];rs={a['name']:a for a in review};hs={a['source_header']:a for a in review}
 assert len(rs)==13 and len(hs)==13
 assert set(hs)=={f'MAP_BELL_TOWER_{i}F' for i in range(1,11)}|{'MAP_BELL_TOWER_ROOF','MAP_BURNED_TOWER_1F','MAP_BURNED_TOWER_B1F'}
 layouts={l['id']:l for l in load('data/layouts/layouts.json')['layouts']};maps={n:load(f'data/maps/{n}/map.json') for n in rs};ids={m['id']:n for n,m in maps.items()};raw={};sizes={};behaviors={};actors={}
 attrs=struct.unpack('<'+str((R/'data/tilesets/secondary/hgss_temple/metatile_attributes.bin').stat().st_size//2)+'H',(R/'data/tilesets/secondary/hgss_temple/metatile_attributes.bin').read_bytes())
 for n,m in maps.items():
  l=layouts[m['layout']];w,h=l['width'],l['height'];sizes[n]=(w,h);data=(R/l['blockdata_filepath']).read_bytes();assert len(data)==w*h*2;raw[n]=struct.unpack('<'+str(w*h)+'H',data);actors[n]={(o['x'],o['y']) for o in m['object_events']}
  assert l['secondary_tileset']=='gTileset_HgssTemple' and l['primary_tileset']=='gTileset_Building'
  assert (R/l['border_filepath']).read_bytes()==struct.pack('<4H',*([0x600]*4))
  if n in base:
   old=base[n]
   for key in ['id','name','layout','region','region_map_section','battle_scene','requires_flash','weather','map_type','allow_escaping','allow_running','show_map_name']:assert m[key]==old[key],(n,'Preserved contract',key)
   old_scripts={e['script'] for e in old['object_events']+old['bg_events']};new_scripts={e['script'] for e in m['object_events']+m['bg_events']}
   assert old_scripts-{'Area_RingBell'}<=new_scripts,(n,'Lost ambient interaction')
  a=rs[n];ox,oy=a['origin_crop'];source=facts[a['source_header']];mapping={int(k):v for k,v in a['source_to_native_warps'].items()}
  for source_index,native_index in mapping.items():
   e=source['warps'][source_index];actual=m['warp_events'][native_index]
   assert (actual['x'],actual['y'])==(e['x']-ox,e['z']-oy),(n,'Reference stair/door moved',e,actual)
   if e['header'] in hs:
    dst=hs[e['header']];assert actual['dest_map']==maps[dst['name']]['id'] and int(actual['dest_warp_id'])==int(dst['source_to_native_warps'][str(e['anchor'])])
   else:assert actual['dest_map'] in ['MAP_ECRUTEAK_CITY','MAP_BELLCHIME_TRAIL']
  for tile in raw[n]:assert 512<=tile&1023<512+len(attrs),(n,'Invalid temple tile',tile)
  assert all(not raw[n][y*w+x]&0xc00 for x,y in actors[n]),(n,'Actor inside wall')
 roof=maps[hs['MAP_BELL_TOWER_ROOF']['name']];assert sum(e['script']=='Area_RingBell' for e in roof['bg_events'])==1,'Preserve accepted bell interaction at finial'
 def behavior(n,x,y):
  w,h=sizes[n]
  if not(0<=x<w and 0<=y<h):return None
  return attrs[(raw[n][y*w+x]&1023)-512]&255
 nodes=set();edges={};reverse={};outside=set()
 for n,m in maps.items():
  w,h=sizes[n];warps={(e['x'],e['y']) for e in m['warp_events']}
  for y in range(h):
   for x in range(w):
    t=raw[n][y*w+x]
    if (x,y) not in actors[n] and ((not t&0xc00 and t>>12==3) or (x,y) in warps):nodes.add((n,x,y))
 for state in nodes:
  n,x,y=state;m=maps[n];dest=[]
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   p=next_position(x,y,dx,dy,lambda a,b:behavior(n,a,b))
   if p is not None and (n,*p) in nodes:dest.append((n,*p))
  for e in m['warp_events']:
   if (e['x'],e['y'])!=(x,y):continue
   if e['dest_map'] in ids:
    dst=ids[e['dest_map']];back=maps[dst]['warp_events'][int(e['dest_warp_id'])];assert back['dest_map']==m['id'];dest.append((dst,back['x'],back['y']))
   else:outside.add(state)
  edges[state]=dest
  for to in dest:reverse.setdefault(to,[]).append(state)
 def flood(seeds,graph):
  seen=set(seeds);q=deque(seeds)
  while q:
   for to in graph.get(q.popleft(),[]):
    if to not in seen:seen.add(to);q.append(to)
  return seen
 forward=flood(outside,edges);escapes=flood(outside,reverse)
 for n,m in maps.items():
  for e in m['warp_events']:
   p=(n,e['x'],e['y']);assert p in forward,(n,'Unreachable canonical exit',e);assert p in escapes,(n,'No return from exit',e)
  for e in m['object_events']+m['bg_events']:
   adjacent={(n,e['x']+dx,e['y']+dy) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]};assert adjacent&forward,(n,'Unreachable interaction',e)
 assert nodes<=escapes,('Player trap in canonical tower graph',list(nodes-escapes)[:12])
 print('HGSS tower contracts, canonical stair/pad graph, directed jumps and escape from every public tile: PASS',len(nodes),'tiles')
 return set(rs)
if __name__=='__main__':validate_towers()
