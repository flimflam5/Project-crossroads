#!/usr/bin/env python3
"""Actual controller travel, both Gym doors and facade/overhang probes."""
import argparse,runpy,sys,json,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');p.add_argument('--output',default='build/qa06-gyms');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
sys.argv=['johto_network_smoke.py','--save',a.save,'--library',a.library,'--output',str(out),'--targets',''];d=runpy.run_path('crossroads/tools/johto_network_smoke.py');plans=json.load(open('crossroads/art/eight_gyms_v1/integration.json'))['cities'];records=[]
for name,p in plans.items():
 d['go'](name);X,Y=p['origin'];door=p['doors'][0];d['walk']((door[0],door[1]+2));assert d['lib'].emu_image(str(out/(name+'-front.png')).encode())
 for i in p['exterior_warps']:
  d['go'](name,i);d['warp'](i);assert d['current']()==p['interior'];inside=d['maps'][p['interior']];back=0 if i==p['exterior_warps'][0] else 1;d['warp'](back);assert d['current']()==name
 lower_left=next((X+xx,Y+7) for xx in (1,2) if d['path'](name,(X+xx,Y+7)) is not None)
 lower_right=next((X+xx,Y+7) for xx in (6,5) if d['path'](name,(X+xx,Y+7)) is not None)
 for point,button in [(lower_left,64),(lower_right,64),((X,Y+5),16),((X+7,Y+5),32)]:
  assert d['path'](name,point) is not None,(name,'No perimeter access',point)
  d['walk'](point);d['frames'](20,button);d['frames'](20);assert d['current']()==name and d['pos']()==point,(name,'Walked into facade',point,d['pos']())
 # Walk behind the high roof rather than treating the entire picture as ground.
 for point in [(X+2,Y+4),(X+5,Y+4)]:
  d['walk'](point);assert d['pos']()==point
 d['lib'].emu_image(str(out/(name+'-overhang.png')).encode());records.append(dict(city=name,both_doors=True,facade_sides=4,walkable_overhang=True,rom_sha256=hashlib.sha256(Path('pokeemerald.gba').read_bytes()).hexdigest()));print('Actual custom Gym doors, solid facade and walkable roof overhang:',name,'PASS',flush=True)
(out/'coverage.json').write_text(json.dumps(records,indent=2)+'\n')
print('All eight custom Gym exteriors actually traversed: PASS',flush=True)
