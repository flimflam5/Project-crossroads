"""Reference-room contracts and every-public-tile escape with actors/furniture."""
import json,struct
from collections import deque
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def validate_rooms():
 def load(p):return json.loads((R/p).read_text())
 rs=load('crossroads/hgss/room-review.json');base=load('crossroads/hgss/contracts/ecruteak-rooms-qa04.json');facts=load('crossroads/hgss/canonical_events/ecruteak-interior-geometry.json');ls={l['id']:l for l in load('data/layouts/layouts.json')['layouts']};city=load('data/maps/EcruteakCity/map.json');reviewed=set()
 for r in rs:
  n=r['name'];reviewed.add(n);m=load(f'data/maps/{n}/map.json');l=ls[m['layout']];w,h=l['width'],l['height'];data=(R/l['blockdata_filepath']).read_bytes();assert len(data)==w*h*2;t=struct.unpack('<'+str(w*h)+'H',data)
  assert [w,h]==r['dimensions']
  if n in base:
   old=base[n]
   for key in ['id','name','region','region_map_section','map_type','allow_escaping','allow_running','show_map_name']:assert old[key]==m[key],(n,key)
   for o in old['object_events']:assert any(o.get('local_id')==v.get('local_id') and o['script']==v['script'] for v in m['object_events']),(n,'Lost original actor')
  e=facts[r['source_header']]['warps'][0];assert (m['warp_events'][0]['x'],m['warp_events'][0]['y'])==(e['x'],e['z'])
  actors={(o['x'],o['y']) for o in m['object_events']};doors={(e['x'],e['y']) for e in m['warp_events']};public={(x,y) for y in range(h) for x in range(w) if not t[y*w+x]&0xc00 and (x,y) not in actors}
  assert all(not t[y*w+x]&0xc00 for x,y in actors),(n,'NPC on collision')
  seen=set(doors);q=deque(seen)
  while q:
   x,y=q.popleft()
   for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if p in public and p not in seen:seen.add(p);q.append(p)
  assert public<=seen,(n,'Trapped floor',sorted(public-seen))
  for o in m['object_events']:
   assert any((o['x']+dx,o['y']+dy) in seen for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]),(n,'Unreachable actor',o)
  for e in m['warp_events']:
   assert e['dest_map']==city['id'];back=city['warp_events'][int(e['dest_warp_id'])];assert back['dest_map']==m['id']
  if n=='EcruteakCity_DanceTheater':
   assert len(m['object_events'])==6
   for o in m['object_events'][1:]:assert (o['x']-1,o['y']) in seen and o['graphics_id']=='OBJ_EVENT_GFX_ECRUTEAK_PERFORMER',(n,'Unsafe performance step')
 print('Canonical Ecruteak houses/theater, preserved actors/IDs, furnished room access, performance lanes and every-tile escape: PASS',len(rs))
 return reviewed
if __name__=='__main__':validate_rooms()
