#!/usr/bin/env python3
"""Controller checks with QA kit and temporary gear in a private emulator save copy.

Only the test process receives bike/rod inventory and registered-item fixtures.
No ROM items, badges, maps or source-save data are patched.
"""
import argparse,runpy,sys,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');args=p.parse_args()
sys.argv=['qa_kit_smoke.py','--save',args.save,'--library',args.library];k=runpy.run_path('crossroads/tools/qa_kit_smoke.py');d=k['d'];read=d['read'];write=d['write'];frames=d['frames'];key=d['key'];syms=d['syms'];sb=d['sb'];out=Path('build/qa05-joe-fields');out.mkdir(parents=True,exist_ok=True)
def graphics():return read(syms['gObjectEvents']+read(syms['gPlayerAvatar']+5,1)*36+4,2)
def verify(name,gfx):
 assert graphics()==gfx,(name,hex(graphics()),hex(gfx))
 sprite=syms['gSprites']+read(syms['gPlayerAvatar']+4,1)*68;tile=read(sprite+4,2)&1023
 data=Path(f'build/assets/graphics/object_events/pics/people/joe/corporate/{name}.png_mwidth_4__mheight_4.4bpp').read_bytes();frames(1);actual=bytes(read(0x6010000+tile*32+i,1) for i in range(512))
 assert actual in [data[j:j+512] for j in range(0,len(data),512)],(name,'actual VRAM does not match Joe')
def gear(item):
 base=sb()+0x560+30*4;key16=read(read('gSaveBlock2Ptr')+0xac)&65535
 empty=next(i for i in range(30) if read(base+i*4,2) in (0,item));write(base+empty*4,item,2);write(base+empty*4+2,1^key16,2);write(sb()+0x496,item,2)
d['go']('JohtoRoute39')
for name,item,gfx in [('mach_bike',707,0x3f04),('acro_bike',708,0x3f05)]:
 gear(item);key(4);frames(120);verify(name,gfx);d['lib'].emu_image(str(out/(name+'.png')).encode())
 if name=='acro_bike':frames(24,2);frames(60);verify(name,gfx);d['lib'].emu_image(str(out/'acro-wheelie.png').encode())
 key(4);frames(120);assert graphics()==250
 print('Registered-item bike mount/dismount + Joe pixels:',name,'PASS',flush=True)
d['go']('JohtoRoute40');n=d['current']();w,h=d['size'][n];raw=d['raw'][n]
water=[(x,y) for y in range(2,h-2) for x in range(2,w-2) if all(raw[(y+dy)*w+x+dx]>>12==1 for dx,dy in [(0,0),(1,0),(-1,0),(0,1),(0,-1)])]
water.sort(key=lambda p:abs(p[0]-d['pos']()[0])+abs(p[1]-d['pos']()[1]))
point=next(p for p in water if d['path'](n,p) is not None);d['walk'](point);verify('surfing',0x3f06)
for direction,button in [('south',128),('north',64),('west',32),('east',16)]:
 frames(8,button);frames(20);verify('surfing',0x3f06);d['lib'].emu_image(str(out/('surf-'+direction+'.png')).encode())
print('Actual survey Surf boarding and four-direction Joe VRAM:', 'PASS',flush=True)
gear(709);key(4);seen=False
for i in range(180):
 frames(4)
 if graphics()==0x3f09:
  verify('fishing',0x3f09)
  if not seen:d['lib'].emu_image(str(out/'fishing.png').encode())
  seen=True
 if i%20==19:key(2)
assert seen,'Registered rod did not enter Joe fishing state'
for _ in range(8):key(2);frames(60)
assert graphics()==0x3f06,'Fishing must return to Joe Surf'
d['go']('OlivineCity');d['walk']((12,13));assert graphics()==250
print('Registered rod casting Joe pixels, return to Surf, disembark to Joe walking: PASS',flush=True)
(out/'coverage.json').write_text(json.dumps(dict(actual=['Mach Bike mount/dismount','Acro Bike mount/wheelie/dismount','Surf four directions','fishing while Surfing','disembark'],gear_fixture='Private emulator RAM only',not_normally_activated=['Dive','watering','decorating','VS Seeker']),indent=2)+'\n')
