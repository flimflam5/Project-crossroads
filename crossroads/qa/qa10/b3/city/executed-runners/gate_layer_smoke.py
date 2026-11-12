#!/usr/bin/env python3
"""Actual controller BEFORE/AFTER gate garbage-background and Joe visibility.

Only reads OAM/VRAM/palette data to predict Joe's opaque pixels; movement is
normal controller input. The shared harness uses a copied battery and its
disclosed RAM-only survey/encounter fixture. No player/map/warp writes.
"""
import argparse,hashlib,json,runpy,subprocess,sys
from pathlib import Path
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--output',required=True);p.add_argument('--rom-sha256',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');p.add_argument('--expect-fixed',action='store_true');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
assert hashlib.sha256(Path('pokeemerald.gba').read_bytes()).hexdigest()==a.rom_sha256
sys.argv=['johto_network_smoke.py','--save',a.save,'--library',a.library,'--output',str(out),'--targets',''];q=runpy.run_path(str(Path(__file__).with_name('johto_network_smoke.py')))
go,walk,read,frames,pos,current,lib,syms=[q[k]for k in ['go','walk','read','frames','pos','current','lib','syms']]
records=[]
def save_report():
 (out/'results.json').write_text(json.dumps(dict(rom_sha256=a.rom_sha256,phase='fixed regression'if a.expect_fixed else'before reproduction',method='Actual controller movement; Joe opaque pixels decoded independently from current hardware OAM/OBJ VRAM/palette, not assumed from tile collision',records=records),indent=2)+'\n')
def capture(label):
 path=out/(label+'.png');lib.emu_image(str(path).encode());return Image.open(path).convert('RGB')
def joe_pixels(frame):
 s=syms['gSprites']+read(syms['gPlayerAvatar']+4,1)*68;tile=read(s+4,2)&1023;palette=read(s+4,2)>>12;matches=[]
 for i in range(128):
  addr=0x07000000+i*8;v0,v1,v2=read(addr,2),read(addr+2,2),read(addr+4,2)
  if(v2&1023)==tile and v2>>12==palette and not v0&0x300:matches.append((v0,v1,v2))
 assert len(matches)==1,('Cannot identify unique normal Joe OAM entry',tile,palette,matches)
 v0,v1,v2=matches[0];assert not v0&0x2c00,'Joe has an unsupported blend/window/8bpp mode'
 dims=[[(8,8),(16,16),(32,32),(64,64)],[(16,8),(32,8),(32,16),(64,32)],[(8,16),(8,32),(16,32),(32,64)]];width,height=dims[v0>>14][v1>>14];x0,y0=v1&511,v0&255;x0=x0-512 if x0>=256 else x0;y0=y0-256 if y0>=160 else y0
 assert 0<=x0<=240-width and 0<=y0<=160-height
 colors=[]
 for i in range(16):
  v=read(0x05000200+palette*32+i*2,2);colors.append(tuple(((v>>shift)&31)<<3|((v>>shift)&31)>>2 for shift in(0,5,10)))
 stride=width//8 if read(0x04000000,2)&64 else 32
 expected=matched=0
 for y in range(height):
  for x in range(width):
   X=width-1-x if v1&0x1000 else x;Y=height-1-y if v1&0x2000 else y;index=tile+(Y//8)*stride+X//8;b=read(0x06010000+index*32+(Y%8)*4+(X%8)//2,1);color=(b>>(4*(X%2)))&15
   if color:expected+=1;matched+=int(frame.getpixel((x0+x,y0+y))==colors[color])
 return dict(opaque_expected=expected,opaque_visible=matched,opaque_hidden=expected-matched,screen_bounds=[x0,y0,width,height])
for direction in ['West','East']:
 name='EcruteakCity_'+direction+'Gate';go(name)
 for y in(6,7):
  walk((6,y));frames(30);frame=capture(direction.lower()+'-magenta-'+str(y));magenta=sum(c==(255,0,255)for c in frame.getdata());records.append(dict(case='debug-magenta',map=name,position=list(pos()),pixels=magenta,result='PASS'if(a.expect_fixed and magenta==0)or(not a.expect_fixed and magenta>0)else'FAIL'));save_report();assert(magenta==0)if a.expect_fixed else(magenta>0)
 for x,start,button in[(2,(2,8),128),(10,(9,9),16)]:
  walk(start);frames(30);label=direction.lower()+'-floor-'+str(x);control=joe_pixels(capture(label+'-control'));assert control['opaque_visible']==control['opaque_expected'],('Control Joe visibility',name,start,control)
  folder=out/(label+'-walk');folder.mkdir(exist_ok=True);target=(x,9)
  for i in range(96):
   frames(1,button if pos()!=target else 0)
   if i%2==0:lib.emu_image(str(folder/f'{i//2:04d}.png').encode())
  assert current()==name and pos()==target
  visibility=joe_pixels(capture(label+'-arrival'));records.append(dict(case='normal-floor-Joe-visibility',map=name,position=list(pos()),control=control,arrival=visibility,result='PASS'if(a.expect_fixed and visibility['opaque_hidden']==0)or(not a.expect_fixed and visibility['opaque_hidden']>0)else'FAIL'));save_report()
  assert visibility['opaque_hidden']==0 if a.expect_fixed else visibility['opaque_hidden']>0,('Expected before/after visibility',name,target,visibility)
  subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','30','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(out/(label+'-walk.mp4'))],check=True)
  print(name,target,'Joe opaque visibility',visibility,flush=True)
assert hashlib.sha256(Path('pokeemerald.gba').read_bytes()).hexdigest()==a.rom_sha256
print('Gate layer', 'fixed regression'if a.expect_fixed else'before reproduction','complete:',len(records),'cases',flush=True)
