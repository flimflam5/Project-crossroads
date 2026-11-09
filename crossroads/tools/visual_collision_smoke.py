#!/usr/bin/env python3
"""Controller-only wall/tree probes, repaired-door roundtrips and visual captures.

No map/warp writes. Inherits the tour's disclosed encounter suppression fixture.
Use copies of saves. Screenshots are evidence to inspect, not visual assertions.
"""
import argparse,runpy,sys,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--library',required=True);p.add_argument('--output',default='build/visual-after');a=p.parse_args()
sys.argv=['johto_network_smoke.py','--save',a.save,'--library',a.library,'--output',a.output,'--targets','EcruteakCity,MahoganyTown,MahoganyTown_Workshop,JohtoRoute38,JohtoRoute39','--all-edges']
d=runpy.run_path(str(Path(__file__).with_name('johto_network_smoke.py')))
go,walk,frames,pos,current,lib=[d[k] for k in ['go','walk','frames','pos','current','lib']];out=Path(a.output);probes=[]
def probe_rect(name,x,y,w,h,label):
 go(name);count=0;sides=set()
 candidates=[]
 for xx in range(x,x+w):candidates.extend([((xx,y-1),(xx,y),'north',128),((xx,y+h),(xx,y+h-1),'south',64)])
 for yy in range(y,y+h):candidates.extend([((x-1,yy),(x,yy),'west',16),((x+w,yy),(x+w-1,yy),'east',32)])
 for start,target,side,key in candidates:
  W,H=d['size'][name]
  if not(0<=target[0]<W and 0<=target[1]<H):continue
  if not d['raw'][name][target[1]*W+target[0]]&0xc00:continue
  if any((e['x'],e['y'])==target for e in d['maps'][name]['warp_events']):continue
  if not d['safe'](name,start) or d['path'](name,start) is None:continue
  walk(start);frames(32,key);frames(24)
  assert current()==name and pos()==start,('Walked into solid footprint',name,label,side,start,target,pos())
  count+=1;sides.add(side);probes.append(dict(map=name,fixture=label,side=side,start=start,solid=target,result='blocked'))
 print('Normal movement collision probes:',name,label,count,'PASS',sorted(sides),flush=True)
 assert count>0
# All six shared custom building compositions, including the unchanged Olivine
# exterior whose lower layer attributes changed; no region-wide art claim.
for spec in [('EcruteakCity',36,2,3,6,'Bell Tower'),('EcruteakCity',9,4,4,4,'Burned Tower'),('EcruteakCity',10,16,3,3,'Residence'),('EcruteakCity',20,16,4,3,'Theater'),('OlivineCity',38,28,3,5,'Lighthouse'),('JohtoRoute39',5,5,3,3,'Farmhouse'),('JohtoRoute39',3,15,4,3,'Barn'),('EcruteakCity',16,17,2,3,'Native tree'),('MahoganyTown',34,7,4,4,'Workshop exterior'),('MahoganyTown_Workshop',8,4,2,2,'Dry workbench'),('MahoganyTown_Workshop',2,7,2,2,'Timber workbench')]:probe_rect(*spec)

go('MahoganyTown');walk((35,6));frames(16,128);frames(24)
assert pos()==(35,7),('Roof overhang must allow walking behind',pos())
lib.emu_image(str(out/'normal-roof-overhang.png').encode())
frames(32,128);frames(24);assert pos()==(35,7),'Solid wall below overhang must block'
frames(16,64);frames(24);assert pos()==(35,6)
print('Normal north roof overhang allows entry/exit; solid wall below blocks: PASS',flush=True)

for name,point,label in [('EcruteakCity',(38,8),'bell'),('EcruteakCity',(12,8),'burned'),('EcruteakCity',(16,20),'tree'),('EcruteakCity',(18,19),'tree-side'),('MahoganyTown',(35,12),'MahoganyTown'),('MahoganyTown_Workshop',(6,6),'MahoganyTown_Workshop'),('JohtoRoute38',(24,14),'route38'),('JohtoRoute39',(14,26),'route39'),('OlivineCity',(40,33),'lighthouse')]:
 go(name);walk(point);lib.emu_image(str(out/(label+'.png')).encode());lib.emu_state(str(out/(label+'.snapshot')).encode(),0)
 if label in ['bell','tree']:
  folder=out/(label+'-frames');folder.mkdir(exist_ok=True)
  for j,key in enumerate([64,32,128,16]):
   for i in range(24):frames(2,key);lib.emu_image(str(folder/f'{j*24+i:04}.png').encode())
  subprocess.run(['ffmpeg','-v','error','-framerate','30','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p','-y',str(out/(label+'-movement.mp4'))],check=True)
(out/'collision-probes.json').write_text(json.dumps(probes,indent=2)+'\n')
print('Controller wall/tree/furniture probes and native visual evidence captured: PASS',len(probes),flush=True)
