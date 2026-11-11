#!/usr/bin/env python3
"""Actual B-running versus walking and Joe VRAM on a clear existing road.

Uses the owner-authorized kit UI in a private emulator copy. A same-ROM state,
reached by normal controller travel, makes the two input trials comparable.
No map, coordinate, Running Shoes flag or ROM data is patched directly.
The shared helper suppresses encounters only in the private test process.
"""
import argparse,hashlib,json,runpy,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
sys.argv=['qa_kit_smoke.py','--save',a.save,'--library',a.library,'--output',str(out/'kit')];k=runpy.run_path('crossroads/tools/qa_kit_smoke.py');d=k['d'];read,frames,lib,syms=[d[x] for x in ['read','frames','lib','syms']]
d['go']('JohtoRoute39');d['walk']((14,24));state=out/'road-start.snapshot';assert lib.emu_state(str(state).encode(),0)
sheet=Path('build/assets/graphics/object_events/pics/people/joe/corporate/walking.png_mwidth_2__mheight_4.4bpp').read_bytes();valid=[sheet[i:i+256] for i in range(0,len(sheet),256)];rows=[]
for label,keys in [('walking',128),('running',128|2)]:
 assert lib.emu_state(str(state).encode(),1);start=d['pos']();folder=out/label;folder.mkdir(exist_ok=True)
 for i in range(8):
  frames(4,keys);obj=syms['gObjectEvents']+read(syms['gPlayerAvatar']+5,1)*36;assert read(obj+4,2)==250,'B-running switched away from Joe'
  sprite=syms['gSprites']+read(syms['gPlayerAvatar']+4,1)*68;tile=read(sprite+4,2)&1023;pixels=bytes(read(0x6010000+tile*32+j,1) for j in range(256));assert pixels in valid,'Actual running frame is not Joe artwork'
  lib.emu_image(str(folder/f'{i:04}.png').encode())
 end=d['pos']();assert d['current']()=='JohtoRoute39' and end[0]==start[0]
 rows.append(dict(input=label,held_frames=32,start=start,end=end,tiles_south=end[1]-start[1],joe_id=250,joe_vram=True));lib.emu_image(str(out/(label+'.png')).encode())
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(out/(label+'.mp4'))],check=True)
assert rows[1]['tiles_south']>rows[0]['tiles_south']>0,('Running Shoes did not increase actual movement speed',rows)
(out/'results.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256(Path('pokeemerald.gba').read_bytes()).hexdigest(),setup='Actual kit Running Shoes grant; normal controller road travel; same-ROM paired input trials; no map/coordinate/Running Shoes flag patches; shared RAM-only encounter suppression',results=rows,status='PASS'),indent=2)+'\n');print('Actual B-running is faster than walking; both use Joe VRAM: PASS',rows,flush=True)
