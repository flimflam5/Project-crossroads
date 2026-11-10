#!/usr/bin/env python3
"""Normal controller probes against every reachable blocked edge in Ecruteak.

Not region-wide visual QA. Does not inspect inaccessible back-side wall cells or
pretend deliberate roof/canopy overhang is solid. Native screenshots/recording
capture the representative trunk and building examples as well as the counts.
"""
import argparse,runpy,sys,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');a=p.parse_args();out=Path('build/qa05-collision');out.mkdir(parents=True,exist_ok=True)
sys.argv=['johto_network_smoke.py','--save',a.save,'--library',a.library,'--output',str(out),'--targets',''];d=runpy.run_path('crossroads/tools/johto_network_smoke.py');d['go']('EcruteakCity');n=d['current']();w,h=d['size'][n];raw=d['raw'][n];walk=d['walk'];pos=d['pos'];frames=d['frames'];lib=d['lib'];rows=[];warps={(e['x'],e['y']) for e in d['maps'][n]['warp_events']}
for label,point,button in [('tree-north',(26,42),128),('tree-west',(25,43),16),('tree-east',(28,43),32),('tree-south',(26,44),64)]:
 walk(point);movie=out/label;movie.mkdir(exist_ok=True)
 for i in range(18):frames(2,button if i<12 else 0);assert lib.emu_image(str(movie/f'{i:04}.png').encode())
 assert pos()==point,(label,pos());assert lib.emu_image(str(out/(label+'.png')).encode());rows.append(dict(label=label,point=point,blocked=True))
probes=[]
for y in range(h):
 for x in range(w):
  point=(x,y)
  if point in warps or not d['safe'](n,point):continue
  for dx,dy,k in [(1,0,16),(-1,0,32),(0,1,128),(0,-1,64)]:
   xx,yy=x+dx,y+dy
   if 0<=xx<w and 0<=yy<h and raw[yy*w+xx]&0xc00 and (xx,yy) not in warps and d['behavior'](n,xx,yy) not in range(0x38,0x3c):probes.append((point,(xx,yy),k))
# Greedy nearest-next order shortens controller travel while testing every probe.
count=0
while probes:
 probes.sort(key=lambda e:abs(e[0][0]-pos()[0])+abs(e[0][1]-pos()[1]));point,target,k=probes.pop(0)
 if d['path'](n,point) is None:raise AssertionError(('Inaccessible public probe',point,target))
 walk(point);frames(16,k);frames(20);assert d['current']()==n and pos()==point,(point,target,d['current'](),pos());count+=1
 rows.append(dict(point=point,target=target,blocked=True))
 if count%100==0:print('Actual controller blocked-edge probes:',count,'PASS',flush=True)
assert count>200
(out/'coverage.json').write_text(json.dumps(dict(map=n,normal_controller_blocked_edges=count,representative_trunk_directions=4,probes=rows,scope='Reachable city walls/tree roots/inner boundary edges; visual acceptance remains owner'),indent=2)+'\n')
print('Actual city blocked-edge sweep and four-direction recorded trunk probes: PASS',count,flush=True)
