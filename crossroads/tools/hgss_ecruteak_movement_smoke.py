#!/usr/bin/env python3
"""Controller collision probes. Uses a copied battery save, never commits saves.

Wild encounters are suppressed by the existing harness only inside its process;
its disclosed survey helper is RAM-only. Does not certify all trees or visual QA.
"""
import sys,runpy,argparse
p=argparse.ArgumentParser();p.add_argument('--save',required=True);args=p.parse_args()
from pathlib import Path
sys.argv=['johto_network_smoke.py','--save',args.save,'--library','/tmp/johto-bridge.so','--output','build/hgss-qa02-movement','--targets','']
d=runpy.run_path('crossroads/tools/johto_network_smoke.py');d['go']('EcruteakCity')
for label,point,key in [('tree-north',(26,42),128),('tree-west',(25,43),16),('tree-east',(28,43),32),('tree-south',(26,44),64)]:
 d['walk'](point);d['frames'](24,key);d['frames'](20);assert d['pos']()==point,(label,d['pos']());d['lib'].emu_image(str(Path('build/hgss-qa02-movement')/(label+'.png')).encode());print(label,'normal controller trunk collision PASS',flush=True)
for label,point in [('mart-front',(53,46)),('station-front',(39,26)),('east-road',(61,47))]:
 d['walk'](point);d['lib'].emu_image(str(Path('build/hgss-qa02-movement')/(label+'.png')).encode())
print('Four-direction representative trunk collision and native screenshots PASS',flush=True)
