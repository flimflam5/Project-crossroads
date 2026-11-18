#!/usr/bin/env python3
"""Cold-Continue a genuine QA10 route save and verify recovery/negative control.

Uses native copied battery, real title UI and movement; only wild encounters and
survey access use disclosed runtime fixtures in the shared tour. Never commits saves.
"""
import argparse,hashlib,json,runpy,shutil,sys
from pathlib import Path
from PIL import Image
R=Path.cwd();p=argparse.ArgumentParser();p.add_argument('--save',type=Path,required=True);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--rom-sha256',required=True);p.add_argument('--expect-relocation',action='store_true');p.add_argument('--library',default='/tmp/johto-bridge.so');a=p.parse_args()
out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);sha=lambda b:hashlib.sha256(b).hexdigest();source=sha(a.save.read_bytes());base=json.loads(a.baseline.read_text());assert source==base['source_battery_sha256'];assert sha((R/'pokeemerald.gba').read_bytes())==a.rom_sha256
trial=out/'input-copy.sav';assert trial!=a.save.resolve();shutil.copyfile(a.save,trial);sys.path.insert(0,str(R/'crossroads/tools'));sys.argv=['johto_network_smoke.py','--save',str(trial),'--library',a.library,'--output',str(out/'tour'),'--targets','']
d=runpy.run_path(str(R/'crossroads/tools/johto_network_smoke.py'));read,frames,current,pos,walk,lib,syms,sb=[d[n] for n in ('read','frames','current','pos','walk','lib','syms','sb')];assert lib.emu_state(str(out/'tour/start.snapshot').encode(),1);assert current()=='JohtoRoute33';old=tuple(base['continued_position']);landing=pos();assert (landing!=old) if a.expect_relocation else (landing==old),(old,landing,a.expect_relocation);assert d['safe']('JohtoRoute33',landing) and landing not in d['active_warps']('JohtoRoute33'),('Unsafe relocation',landing)
def memory(x,n):return bytes(read(x+i,1) for i in range(n))
def payload():
 count=read(read('gPlayerPartyCountPtr'),1);enc=read(read('gSaveBlock2Ptr')+0xac);inv=dict(money=read(sb()+0x490)^enc,coins=read(sb()+0x494,2)^(enc&65535),registered=read(sb()+0x496,2),pc=memory(sb()+0x498,0xc8).hex(),bag=[(read(sb()+0x560+i*4,2),read(sb()+0x562+i*4,2)^(enc&65535)) for i in range(186)]);return dict(starter=read(sb()+0x1590,2),count=count,party=sha(memory(read('gPlayerPartyPtr'),count*100)),boxes=sha(memory(read('gPokemonStoragePtr'),0x83d0)),flags=sha(memory(sb()+0x1270,300)),decoded_inventory=sha(json.dumps(inv,sort_keys=True).encode()))
assert payload()==base['payload'],('Saved data changed',payload(),base['payload']);assert not read('sLockFieldControls',1)
frames(40);assert lib.emu_image(str(out/'continued.png').encode());frame=Image.open(out/'continued.png').convert('RGB');assert frame.size==(240,160)
sprite=syms['gSprites']+read(syms['gPlayerAvatar']+4,1)*68;tile=read(sprite+4,2)&1023;palette=read(sprite+4,2)>>12;matches=[]
for i in range(128):
 a0=0x07000000+i*8;v0,v1,v2=read(a0,2),read(a0+2,2),read(a0+4,2)
 if (v2&1023)==tile and v2>>12==palette and not v0&0x300:matches.append((v0,v1,v2))
assert len(matches)==1;v0,v1,v2=matches[0];assert not v0&0x2c00;dims=[[(8,8),(16,16),(32,32),(64,64)],[(16,8),(32,8),(32,16),(64,32)],[(8,16),(8,32),(16,32),(32,64)]];width,height=dims[v0>>14][v1>>14];x0,y0=v1&511,v0&255;x0=x0-512 if x0>=256 else x0;y0=y0-256 if y0>=160 else y0;assert 0<=x0<=240-width and 0<=y0<=160-height
colors=[]
for i in range(16):
 v=read(0x05000200+palette*32+i*2,2);colors.append(tuple(((v>>shift)&31)<<3|((v>>shift)&31)>>2 for shift in (0,5,10)))
stride=width//8 if read(0x04000000,2)&64 else 32;expected=visible=0;mismatches=[]
for y in range(height):
 for x in range(width):
  X=width-1-x if v1&0x1000 else x;Y=height-1-y if v1&0x2000 else y;index=tile+(Y//8)*stride+X//8;b=read(0x06010000+index*32+(Y%8)*4+(X%8)//2,1);color=(b>>(4*(X%2)))&15
  if color:
   expected+=1;actual=frame.getpixel((x0+x,y0+y));visible+=int(actual==colors[color])
   if actual!=colors[color]:mismatches.append((x,y))
assert expected>0;behavior=d['behavior']('JohtoRoute33',*landing)
if behavior==7:assert len(mismatches)<=10 and all(y>=height-2 for x,y in mismatches),('Unexpected grass occlusion',mismatches)
else:assert visible==expected,('Joe not fully visible on non-grass',landing,behavior,mismatches)
# Walk to another nearby ordinary floor tile, proving the arrival does not trap.
w,h=d['size']['JohtoRoute33'];choices=[]
for y in range(2,h-2):
 for x in range(2,w-2):
  q=(x,y)
  if q!=landing and d['safe']('JohtoRoute33',q) and d['behavior']('JohtoRoute33',x,y)==0 and q not in d['active_warps']('JohtoRoute33') and d['path']('JohtoRoute33',q) is not None:choices.append(q)
assert choices,'No safe normal floor reachable';target=min(choices,key=lambda q:abs(q[0]-landing[0])+abs(q[1]-landing[1]));walk(target);assert pos()==target and current()=='JohtoRoute33';frames(40);assert lib.emu_image(str(out/'walk-away.png').encode());assert payload()==base['payload'];assert sha(a.save.read_bytes())==source and sha((R/'pokeemerald.gba').read_bytes())==a.rom_sha256
(out/'results.json').write_text(json.dumps(dict(rom_sha256=a.rom_sha256,old_position=old,arrival=landing,walked_to=target,expected_relocation=a.expect_relocation,visible=visible,opaque=expected,behavior=behavior,private_source_unchanged=True,result='PASS'),indent=2)+'\n');print('genuine old position PASS',old,'->',landing,'->',target,'visible',visible,'/',expected,flush=True)
