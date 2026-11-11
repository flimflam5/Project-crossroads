#!/usr/bin/env python3
"""Normal controller wall/tunnel/arrow clips for both reference-led gate models."""
import argparse,hashlib,json,runpy,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--output',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
sys.argv=['johto_network_smoke.py','--save',a.save,'--library',a.library,'--output',str(out),'--targets',''];d=runpy.run_path(str(Path(__file__).with_name('johto_network_smoke.py')));go,walk,frames,current,pos,read,lib,syms=[d[k]for k in ['go','walk','frames','current','pos','read','lib','syms']];rows=[]
def record(label,n,point,button):
 go(n);walk(point);folder=out/label;folder.mkdir(exist_ok=True);lib.emu_image(str(out/(label+'-before.png')).encode())
 visible=0
 for i in range(20):
  frames(4,button if i<8 else 0);lib.emu_image(str(folder/f'{i:04}.png').encode())
  obj=syms['gObjectEvents']+read(syms['gPlayerAvatar']+5,1)*36;arrow=read(obj+0x1b,1)
  visible+=int(not bool(read(syms['gSprites']+arrow*68+0x3e,1)&4))
 assert current()==n and pos()==point,(label,'Walked into solid gate wall',current(),pos(),point)
 assert visible==0,(label,'Unintended gate ground arrow',visible)
 lib.emu_image(str(out/(label+'.png')).encode());subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(out/(label+'.mp4'))],check=True)
 rows.append(dict(label=label,map=n,approach=point,button=button,result='blocked by solid wall through controller input',arrow_visible_samples=visible));print(label,'PASS',flush=True)
for label,point,button in [('west-front-wall-side',(7,40),32),('east-front-wall-left',(60,52),64),('east-front-wall-right',(61,52),64),('east-rear-wall-left',(60,44),128),('east-rear-wall-right',(61,44),128),('east-front-wall-from-tunnel',(61,48),128)]:record(label,'EcruteakCity',point,button)
for y in [12,16,17,18]:record('east-road-wall-'+str(y),'JohtoRoute42',(3,y),32)
go('EcruteakCity');walk((8,38));lib.emu_image(str(out/'west-gate-forecourt.png').encode());walk((59,47));lib.emu_image(str(out/'east-gate-forecourt.png').encode())
(out/'results.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256(Path('pokeemerald.gba').read_bytes()).hexdigest(),setup='Copied old battery, cold Continue and controller travel; no map/warp/position RAM writes; RAM-only survey desk/encounter suppression from shared harness',records=rows),indent=2)+'\n')
