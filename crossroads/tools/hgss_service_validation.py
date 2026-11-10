"""Reference service/Gym contracts; retained save IDs and safe usable geometry."""
from pathlib import Path
from collections import deque
import json,struct
R=Path(__file__).resolve().parents[2]
def validate_services():
 def load(p):return json.loads((R/p).read_text())
 rs=load('crossroads/hgss/service-review.json');ls={l['id']:l for l in load('data/layouts/layouts.json')['layouts']};base=load('crossroads/hgss/contracts/ecruteak-rooms-qa04.json');names=set();count=0
 for r in rs:
  n=r['name'];names.add(n);m=load(f'data/maps/{n}/map.json');l=ls[m['layout']];w,h=l['width'],l['height'];b=(R/l['blockdata_filepath']).read_bytes();assert len(b)==w*h*2;t=struct.unpack('<'+str(w*h)+'H',b);assert [w,h]==r['dimensions']
  if n in base:
   old=base[n]
   for key in ['id','name','region','region_map_section','map_type','allow_escaping','show_map_name']:assert old[key]==m[key],(n,key)
   for o in old['object_events']:assert any(v['script']==o['script'] and v.get('local_id')==o.get('local_id') for v in m['object_events']),(n,'Lost accepted actor')
  for e in m['warp_events']:
   dst=load('data/maps/'+next(name for name in load('data/maps/map_groups.json')['gMapGroup_CrossroadsOlivine']+load('data/maps/map_groups.json')['gMapGroup_CrossroadsJohtoExpansion'] if load(f'data/maps/{name}/map.json')['id']==e['dest_map'])+'/map.json');assert dst['warp_events'][int(e['dest_warp_id'])]['dest_map']==m['id']
  actors={(e['x'],e['y']) for e in m['object_events']};doors={(e['x'],e['y']) for e in m['warp_events']};public={(x,y) for y in range(h) for x in range(w) if not t[y*w+x]&0xc00 and (x,y) not in actors}
  assert all(not t[y*w+x]&0xc00 for x,y in actors),(n,'Actor in solid object')
  seen=set(doors);q=deque(seen)
  while q:
   x,y=q.popleft()
   for v in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if v in public and v not in seen:seen.add(v);q.append(v)
  assert public<=seen,(n,'Trapped public floor',sorted(public-seen))
  for e in m['object_events']:
   assert any((e['x']+dx,e['y']+dy) in seen for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(2,0),(-2,0),(0,2),(0,-2)]),(n,'Inaccessible actor',e)
  if 'bridge_tiles' in r:
   bridge={tuple(p) for p in r['bridge_tiles']};fall={tuple(p) for p in r['fall_tiles']};assert bridge.isdisjoint(fall)
   assert {(e['x'],e['y']) for e in m['coord_events']}==fall
   assert all(e['script']=='Hgss_GymReturn' and e['var']=='VAR_TEMP_0' and e['var_value']=='0' for e in m['coord_events'])
   # Every painted public non-bridge cell must actually execute the safe return.
   assert public <= bridge|fall|doors,(n,'Unscripted void')
   ox,oy=r['origin_crop'];f=load('crossroads/hgss/canonical_events/ecruteak-interior-geometry.json')['MAP_ECRUTEAK_GYM'];p=[v for c in f['chunks'] for v in c['permissions']]
   expected={(x,y) for y in range(h) for x in range(w) if p[(y+oy)*32+x+ox]&0x8600==0x600}
   assert expected<=bridge,(n,'Source bridge missing')
  count+=len(public)
 heal=next(h for h in load('src/data/heal_locations.json')['heal_locations'] if h['id']=='HEAL_LOCATION_ECRUTEAK_CITY');assert (heal['respawn_x'],heal['respawn_y'])==(8,13)
 # Scope: no shared native layouts were rebound or changed.
 shared=load('crossroads/hgss/contracts/save-contracts.json')['layouts']['layouts']
 for old in shared:
  if old['id'] in ['LAYOUT_MART','LAYOUT_OLIVINE_POKEMON_CENTER_1F','LAYOUT_HOUSE_WITH_BED']:assert ls[old['id']]==old
 print('HGSS Center/Mart/Gym reference paths, accepted service/practice scripts, safe floor and scripted fall coverage: PASS',count,'public tiles')
 return names
if __name__=='__main__':validate_services()
