"""Exact reference gate endpoints, road aliases, coordinate triggers and escapes."""
import json,struct
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[2]
def validate_gates():
 def load(p):return json.loads((R/p).read_text())
 reviews=load('crossroads/hgss/gate-review.json');facts=load('crossroads/hgss/canonical_events/ecruteak-interior-geometry.json');ls={l['id']:l for l in load('data/layouts/layouts.json')['layouts']};city=load('data/maps/EcruteakCity/map.json');names=set()
 for r in reviews:
  n=r['name'];names.add(n);m=load(f'data/maps/{n}/map.json');route=load(f'data/maps/{r["route"]}/map.json');direction='West' if 'West' in n else 'East';c=next(c for c in city['connections'] if c['direction']==('left' if direction=='West' else 'right'));cl=ls[city['layout']];rl=ls[route['layout']]
  for i,e in enumerate(facts[r['source_header']]['warps']):
   actual=m['warp_events'][i];assert (actual['x'],actual['y'])==(e['x'],e['z']);outer=city if e['header']=='MAP_ECRUTEAK' else route;key='city' if outer is city else 'route';indices=r[key+'_alias_indices'];assert actual['dest_map']==outer['id'] and int(actual['dest_warp_id'])==indices[1]
   label='Hgss_'+direction+('City' if key=='city' else 'Route')+'GateEnter';triggers=[e for e in outer['coord_events'] if e['script']==label];assert len(triggers)==3
   yy=list(range(37,40) if direction=='West' else range(46,49));expected=[(0 if direction=='West' else 63,y) if outer is city else (rl['width']-1 if direction=='West' else 0,y-c['offset']) for y in yy]
   for j,point in zip(indices,expected):
    event=outer['warp_events'][j];assert (event['x'],event['y'])==point and event['dest_map']==m['id'] and int(event['dest_warp_id'])==i
   assert {(e['x'],e['y']) for e in triggers}==set(expected)
   assert all(e['var']=='VAR_TEMP_0' and e['var_value']=='0' for e in triggers)
  l=ls[m['layout']];w,h=l['width'],l['height'];assert [w,h]==r['dimensions'];t=struct.unpack('<'+str(w*h)+'H',(R/l['blockdata_filepath']).read_bytes());actors={(e['x'],e['y']) for e in m['object_events']};public={(x,y) for y in range(h) for x in range(w) if not t[y*w+x]&0xc00 and (x,y) not in actors};seed={(e['x'],e['y']) for e in m['warp_events']};seen=set(seed);q=deque(seen)
  while q:
   x,y=q.popleft()
   for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if p in public and p not in seen:seen.add(p);q.append(p)
  assert public<=seen and seed<=public,(n,'Gate trap')
  assert all(not t[y*w+x]&0xc00 for x,y in actors)
 scripts=(R/'crossroads/scripts/hgss_gates.inc').read_text();assert all(s not in scripts for s in ['setflag','setvar','giveitem','givemon','trainerbattle'])
 print('Canonical west/east gate endpoints, all six aliases per road, temporary coordinate portals and safe floor: PASS')
 return names
if __name__=='__main__':validate_gates()
