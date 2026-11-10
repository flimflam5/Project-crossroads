#!/usr/bin/env python3
"""Real menu/flight test using a copied old battery save; no map/warp RAM writes."""
import argparse,sys,runpy,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--record',action='store_true');p.add_argument('--library',default='/tmp/johto-bridge.so');args=p.parse_args()
sys.argv=['qa_kit_smoke.py','--save',args.save,'--library',args.library]
k=runpy.run_path('crossroads/tools/qa_kit_smoke.py');d=k['d'];read=d['read'];key=d['key'];frames=d['frames'];sb=d['sb'];syms=d['syms'];lib=d['lib'];out=Path('build/qa04-fly');out.mkdir(parents=True,exist_ok=True)
d['go']('OlivineCity')
count=read(read('gPlayerPartyCountPtr'),1);choice=read(sb()+0x1590,2)
def badges():return tuple((read(sb()+0x1270+i//8,1)>>(i%8))&1 for i in range(0x867,0x86f))
beforebadges=badges()
def menu_action(action):
 key(8);frames(90)
 for _ in range(12):
  cursor=read('sStartMenuCursorPos',1)
  if read(syms['sCurrentStartMenuActions']+cursor,1)==action:break
  key(128)
 else:raise AssertionError(('Start menu action missing',action))
 key(1);frames(180)
def open_fly():
 menu_action(1)
 for _ in range(7):
  if read(syms['gPartyMenu']+9,1)==k['before']:break
  key(128)
 assert read(syms['gPartyMenu']+9,1)==k['before']
 key(1);frames(60);key(128);key(1);frames(180)
 assert read(syms['gMain']+4)==syms['CB2_Atlas']|1,'Fly did not open Johto map through party menu'
 assert read('sAtlasFlyMode',1)==1
lib.emu_image(str(out/'departure.png').encode())
open_fly();lib.emu_image(str(out/'fly-selection.png').encode());key(2);frames(180)
assert read(syms['gMain']+4)==syms['CB2_UpdatePartyMenu']|1
for _ in range(3):key(2);frames(180)
assert d['current']()=='OlivineCity'
print('Party-menu Fly and B cancel back to party/field without travel: PASS',flush=True)
atlas=json.load(open('crossroads/johto/atlas.json'));heals=json.load(open('src/data/heal_locations.json'))['heal_locations'];destinations=atlas['fly_destinations'];visits=[]
for name,heal_id in destinations.items():
 target=next(i for i,n in enumerate(atlas['nodes']) if n['name']==name);h=next(h for h in heals if h['id']==heal_id)
 open_fly()
 for _ in range(11):
  if read('sAtlasSelection',1)==target:break
  key(16)
 assert read('sAtlasSelection',1)==target,(name,'selection failed')
 key(1)
 if args.record and not visits:
  movie=out/'fly-frames';movie.mkdir(exist_ok=True);seen_gfx=set();joe_verified=False
  expected=(Path('build/assets/graphics/object_events/pics/people/joe/corporate/field_move.png_mwidth_4__mheight_4.4bpp')).read_bytes()
  for frame in range(250):
   frames(4);obj=syms['gObjectEvents']+read(syms['gPlayerAvatar']+5,1)*36;gfx=read(obj+4,2);seen_gfx.add(gfx)
   if gfx==0x3f08:
    sprite=syms['gSprites']+read(syms['gPlayerAvatar']+4,1)*68;tile=read(sprite+4,2)&1023;v=bytes(read(0x6010000+tile*32+j,1) for j in range(512))
    # Graphics ID changes before the queued VBlank tile DMA completes.
    if v not in [expected[k:k+512] for k in range(0,len(expected),512)]:
     frames(1);v=bytes(read(0x6010000+tile*32+j,1) for j in range(512))
    assert v in [expected[k:k+512] for k in range(0,len(expected),512)],'Fly field pose must upload Joe pixels after VBlank'
    if not joe_verified:lib.emu_image(str(out/'joe-fly-pose.png').encode())
    joe_verified=True
   lib.emu_image(str(movie/f'{frame:04}.png').encode())
  assert joe_verified,(seen_gfx,'Joe field pose was not observed')
  print('Fly frame-by-frame Joe field-action ID and actual VRAM pixels: PASS',flush=True)
 for _ in range(35):
  frames(60)
  if read(syms['gMain']+4)==syms['CB2_Overworld']|1 and d['current']()==name and not read('sLockFieldControls',1):break
 else:raise AssertionError((name,'Fly arrival failed',d['current'](),d['pos']()))
 frames(60);assert d['pos']()==(h['x'],h['y']),(name,d['pos'](),h)
 assert read(read('gPlayerPartyCountPtr'),1)==count and read(sb()+0x1590,2)==choice and badges()==beforebadges
 lib.emu_image(str(out/(name+'.png')).encode());print('Actual Fly animation/landing:',name,d['pos'](),'PASS',flush=True);visits.append(name)
(out/'coverage.json').write_text(json.dumps(dict(cities=visits,cancel=True,old_save_continue=True,badge_flags_unchanged=True,starter_retained=True),indent=2)+'\n')
print('All ten Johto QA Fly destinations, native departure/arrival and cancellation: PASS',flush=True)
# Save through the normal menu, then cold-boot a fresh core from battery SRAM.
menu_action(5)
for _ in range(8):key(1);frames(180)
for _ in range(3):key(2);frames(180)
assert read(syms['gMain']+4)==syms['CB2_Overworld']|1
saved_city=d['current']();saved_pos=d['pos']();saved_party=bytes(read(read('gPlayerPartyPtr')+i,1) for i in range(count*100));battery=out/'post-flight.sav'
assert lib.emu_save(str(battery).encode(),0)
assert lib.emu_init(str(Path('pokeemerald.gba').resolve()).encode())
assert lib.emu_save(str(battery).encode(),1)
frames(4500);assert read(syms['gMain']+4)==syms['CB2_BlackLedgerTitle']|1
key(8);frames(180);key(1);frames(300)
assert read(syms['gMain']+4)==syms['CB2_Overworld']|1
assert d['current']()==saved_city and d['pos']()==saved_pos
assert bytes(read(read('gPlayerPartyPtr')+i,1) for i in range(count*100))==saved_party
assert read(sb()+0x1590,2)==choice and badges()==beforebadges
open_fly();assert read('sAtlasFlyMode',1)==1;key(2);frames(180)
print('Normal post-flight Save, fresh-core title/Continue, exact party/position persistence and Fly reopened: PASS',flush=True)
