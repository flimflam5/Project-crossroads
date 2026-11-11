#!/usr/bin/env python3
"""Exercise explicit door segments using controller input on a copied battery.

Unlike the network tour, a failed segment cannot fall back to its working neighbour.
Snapshots only isolate trials on the same ROM; no coordinates/warps are written.
"""
import argparse, hashlib, json, runpy, subprocess, sys
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--save',required=True)
p.add_argument('--library',default='/tmp/johto-bridge.so')
p.add_argument('--output',required=True)
p.add_argument('--baseline',action='store_true')
p.add_argument('--city',choices=['ecruteak','olivine'],default='ecruteak')
p.add_argument('--filter',default='')
a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
sys.argv=['johto_network_smoke.py','--save',a.save,'--library',a.library,'--output',str(out),'--targets','']
d=runpy.run_path(str(Path(__file__).with_name('johto_network_smoke.py')))
go,walk,frames,current,pos,lib=[d[k] for k in ['go','walk','frames','current','pos','lib']]
manifest=json.loads(Path('crossroads/hgss/doorways-qa08.json').read_text())
results=[]
for group in manifest['groups']:
 if group['city']!=a.city or a.filter and a.filter not in group['label']:continue
 for side in ['outside','inside']:
  source=group[side];n=source['map'];other=group['inside' if side=='outside' else 'outside']['map']
  go(n)
  # Begin on reachable public floor, not a warp left by the previous trial.
  anchor=source['anchor'];walk(tuple(anchor));state=out/'trial.snapshot';lib.emu_state(str(state).encode(),0)
  for i,cell in enumerate(source['segments']):
   x,y=cell;nx,ny=source.get('press',[0,-1] if side=='outside' else [0,1]);k={(0,-1):64,(0,1):128,(-1,0):32,(1,0):16}[(nx,ny)]
   # Front and the two lateral approaches into the same front landing. This
   # tests each leaf without crossing the adjacent doorway to reach it.
   for approach,dx in [('front',0),('left',-1),('right',1)]:
    lib.emu_state(str(state).encode(),1)
    label=f"{group['label']}-{side}-{i}-{approach}";folder=out/label;folder.mkdir(exist_ok=True)
    row=dict(label=label,source=n,segment=cell,expected_destination=other)
    count=0
    def record(nframes,keys=0):
     global count
     while nframes:
      q=min(4,nframes);frames(q,keys);nframes-=q
      lib.emu_image(str(folder/f'{count:04}.png').encode());count+=1
    try:
     landing=(x-nx,y-ny);start=(landing[0]+dx*ny,landing[1]-dx*nx)
     if d['path'](n,start) is None:
      row.update(result='inaccessible approach',position=pos());results.append(row);continue
     walk(start);lib.emu_image(str(folder/'0000.png').encode())
     if dx:
      sx,sy=landing[0]-start[0],landing[1]-start[1]
      record(16,{(0,-1):64,(0,1):128,(-1,0):32,(1,0):16}[(sx,sy)]);record(24)
     assert current()==n and pos()==landing,('Lateral landing',current(),pos(),landing)
     record(16,k);record(180)
     # Arrow exits trigger by holding south after stepping onto the exact tile.
     if current()==n and pos()==(x,y):record(16,k);record(180)
     assert current()==other,('Segment did not warp',current(),pos())
     arrival=pos();frames(40)
     # Walk away from the actual arrival, not a RAM/coordinate relocation.
     candidates=[(arrival[0],arrival[1]+v) for v in [1,-1]]+[(arrival[0]+v,arrival[1]) for v in [-1,1]]
     target=next((c for c in candidates if d['safe'](other,c) and c not in {(e['x'],e['y']) for e in d['maps'][other]['warp_events']} and d['path'](other,c) is not None),None)
     assert target is not None,('No safe walk-away',other,arrival)
     walk(target);record(24)
     row.update(result='PASS',arrival=arrival,walk_away=pos())
    except (AssertionError,StopIteration) as error:
     row.update(result='FAIL',error=str(error),actual_map=current(),position=pos());lib.emu_image(str(out/(label+'-failure.png')).encode())
    if count:
     subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(out/(label+'.mp4'))],check=True)
    results.append(row);print(json.dumps(row),flush=True)
report=dict(rom_sha256=hashlib.sha256(Path('pokeemerald.gba').read_bytes()).hexdigest(),source_revision=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),setup='Copied battery; cold Continue, controller travel; RAM encounter suppression and opt-in survey desk only; no map/warp/position writes',results=results)
(out/'doorway-results.json').write_text(json.dumps(report,indent=2)+'\n')
failures=[r for r in results if r['result']=='FAIL']
print('Doorway segment trials:',len(results),'failures:',len(failures),flush=True)
if not a.baseline:assert not failures,failures
