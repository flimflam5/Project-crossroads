#!/usr/bin/env python3
"""Normal controller reproduction on the exact QA06 baseline; no map/warp writes."""
import argparse,runpy,sys,json,hashlib,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--output',default='build/qa07-baseline');p.add_argument('--library',default='/tmp/johto-bridge.so');p.add_argument('--expect-fixed',action='store_true');p.add_argument('--resume',help='Optional private snapshot; shared harness requires exact ROM SHA256');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
sys.argv=['johto_network_smoke.py','--save',a.save,'--library',a.library,'--output',str(out),'--targets','']+(['--resume',a.resume]if a.resume else []);d=runpy.run_path('crossroads/tools/johto_network_smoke.py');go,walk,read,frames,current,pos,lib,syms=[d[n]for n in ['go','walk','read','frames','current','pos','lib','syms']]
go('EcruteakCity');rows=[]
def obj():return syms['gObjectEvents']+read(syms['gPlayerAvatar']+5,1)*36
def arrow():
 i=read(obj()+0x1b,1);return dict(sprite=i,visible=not bool(read(syms['gSprites']+i*68+0x3e,1)&4),behavior=read(obj()+0x1e,1))
def record(label,steps,expected_final=None):
 folder=out/label;folder.mkdir(exist_ok=True);i=0;visible=0
 for n,k in steps:
  while n:
   q=min(n,4);frames(q,k);n-=q;lib.emu_image(str(folder/f'{i:04}.png').encode());i+=1;visible+=int(arrow()['visible'])
 lib.emu_image(str(out/(label+'.png')).encode());subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(out/(label+'.mp4'))],check=True);rows.append(dict(label=label,map=current(),position=pos(),arrow=arrow(),arrow_visible_samples=visible,tree_palette_rgb555=[read(0x05000040+i*2,2) for i in range(16)]))
 if a.expect_fixed:
  assert not visible,('Unintended walking arrow',label,visible)
  expected={'ordinary-paving-south':(40,61),'canopy-entry':(26,42),'trunk-from-north':(26,42),'trunk-west':(25,43),'trunk-east':(28,43),'trunk-south':(26,44),'house-west-gutter':(20,43),'house-west-base':(19,44),'house-front-wall':(22,46),'station-front-wall':(37,26)}
  wanted=expected_final if expected_final is not None else expected[label]
  assert current()=='EcruteakCity' and pos()==wanted,('Semantic ground footprint',label,current(),pos(),wanted)
walk((40,58));record('ordinary-paving-south',[(16,128),(40,0),(16,128),(40,0),(16,128),(40,0)])
walk((25,42));lib.emu_image(str(out/'tree-before-entry.png').encode());record('canopy-entry',[(16,16),(40,0)]);record('trunk-from-north',[(32,128),(40,0)])
for label,point,k in [('trunk-west',(25,43),16),('trunk-east',(28,43),32),('trunk-south',(26,44),64)]:walk(point);record(label,[(32,k),(40,0)])
for label,point,k in [('house-west-gutter',(19,43),16),('house-west-base',(19,44),16),('house-front-wall',(22,46),64),('station-front-wall',(37,26),64)]:
 if d['path'](current(),point) is not None:walk(point);record(label,[(32,k),(40,0)])
# Independent expected targets come from the ground-plane facade contract, not
# from enumerating cells that happen already to have a collision bit set.
# QA08 opens Theater44,45 as the missing left door leaf. Probe the actual
# right wall46,45 instead; the new doorway smoke separately requires44,45 entry.
for label,point in [('dowsing-wall',(32,56)),('theater-wall',(46,46)),('center-wall',(44,56)),('mart-wall',(52,46)),('burned-wall',(23,22)),('custom-gym-wall',(23,56)),('northwest-private-wall',(22,37)),('north-private-wall',(34,37)),('southeast-private-wall',(53,56))]:
 assert d['path'](current(),point) is not None,('Unreachable facade approach',label,point)
 walk(point);record(label,[(32,64),(40,0)],point)
# Probe both trunk cells of all six freestanding trees from every accessible side.
# Inaccessible sides (an adjacent wall/NPC) are explicit in coverage, never passed.
tree_probes=[]
for x,y in [(26,33),(38,33),(26,42),(29,52),(49,52),(58,42)]:
 probes=[((x-1,y+1),16),((x+2,y+1),32)]+[((x+dx,y),128) for dx in range(2)]+[((x+dx,y+2),64) for dx in range(2)]
 for point,k in probes:
  if not d['safe']('EcruteakCity',point) or d['path'](current(),point) is None:
   tree_probes.append(dict(tree=[x,y],approach=point,button=k,result='not accessible from public floor'));continue
  walk(point);frames(32,k);frames(40)
  assert current()=='EcruteakCity' and pos()==point,('Semantic trunk penetrated',x,y,point,pos())
  assert not arrow()['visible']
  tree_probes.append(dict(tree=[x,y],approach=point,button=k,result='blocked through controller input'))
(out/'semantic-tree-probes.json').write_text(json.dumps(tree_probes,indent=2)+'\n')
(out/'reproduction.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256(Path('pokeemerald.gba').read_bytes()).hexdigest(),records=rows,setup=('Exact-ROM SHA-checked private snapshot from prior cold-Continue controller tour'if a.resume else 'Copied old battery; normal Continue')+' and controller travel. Existing harness uses temporary encounter suppression and actual survey desk, no map/warp writes.'),indent=2)+'\n');print(json.dumps(rows,indent=2),flush=True)
