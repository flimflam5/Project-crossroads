#!/usr/bin/env python3
"""Actual controller interactions/save cycles in rebuilt Ecruteak.

Private fixture RAM: 1HP for healing/loss and one stale-layout cache case.
No warp/map RAM writes, no owner save writes, no production inventory/flag grants.
"""
import argparse,sys,runpy,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');a=p.parse_args()
out=Path('build/qa05-detailed');out.mkdir(parents=True,exist_ok=True)
sys.argv=['johto_network_smoke.py','--save',a.save,'--library',a.library,'--output',str(out),'--targets',''];d=runpy.run_path('crossroads/tools/johto_network_smoke.py')
go,walk,read,write,frames,key,current,pos,close,lib,syms,sb=[d[n] for n in ['go','walk','read','write','frames','key','current','pos','close','lib','syms','sb']]
def image(name):assert lib.emu_image(str(out/(name+'.png')).encode())
def talk(point,button=64):walk(point);frames(1,button);frames(20);key(1);frames(120)
def menu_action(action):
 key(8);frames(90)
 for _ in range(12):
  cursor=read('sStartMenuCursorPos',1)
  if read(syms['sCurrentStartMenuActions']+cursor,1)==action:break
  key(128)
 else:raise AssertionError(('Missing start menu action',action))
 key(1);frames(180)
def save_continue(label,legacy_layout=None):
 if legacy_layout is not None:write(sb()+0x32,legacy_layout,2)
 menu_action(5)
 for _ in range(8):key(1);frames(180)
 for _ in range(3):key(2);frames(180)
 assert read(syms['gMain']+4)==syms['CB2_Overworld']|1
 before=(current(),pos());count=read(read('gPlayerPartyCountPtr'),1);party=bytes(read(read('gPlayerPartyPtr')+i,1) for i in range(count*100));choice=read(sb()+0x1590,2);save=out/(label+'.sav');assert lib.emu_save(str(save).encode(),0)
 assert lib.emu_init(str(Path('pokeemerald.gba').resolve()).encode());assert lib.emu_save(str(save).encode(),1);frames(4500);key(8);frames(180);key(1);frames(300)
 assert read(syms['gMain']+4)==syms['CB2_Overworld']|1
 assert (current(),pos())==before,(label,before,current(),pos());assert read(sb()+0x1590,2)==choice
 assert bytes(read(read('gPlayerPartyPtr')+i,1) for i in range(count*100))==party
 assert read(sb()+0x32,2)==read(syms['gMapHeader']+0x12,2),('Stale layout still cached',label)
 write('sWildEncountersDisabled',1,1);image(label);print('Normal Save/fresh-core Continue and exact position/party:',label,'PASS',flush=True)
# Furnishing/camera inspection views, all reached from the actual network.
for name,point,label in [('EcruteakCity_Residence',(4,5),'southwest-house'),('EcruteakCity_DowsingHouse',(4,5),'second-house'),('EcruteakCity_Mart',(4,8),'mart-interior'),('EcruteakCity_PokemonCenter_1F',(8,14),'center-interior'),('EcruteakCity_PokemonCenter_B1F',(8,7),'center-basement'),('EcruteakCity_BarrierStation',(15,8),'barrier-station'),('BellchimeTrail',(25,14),'autumn-trail'),('EcruteakCity_BellTower_Roof',(15,17),'tower-summit')]:
 go(name);walk(point);image(label)
go('EcruteakCity_DanceTheater');talk((9,9),16);assert read('sLockFieldControls',1)
performers={i:o for i,o in enumerate(d['maps'][current()]['object_events'],1) if i>=2};moved=set()
for step in range(360):
 if step%30==0:key(1)
 frames(2)
 for j in range(16):
  event=syms['gObjectEvents']+j*36;lid=read(event+8,1)
  if read(event,1)&1 and lid in performers:
   o=performers[lid]
   if (read(event+16,2)-7,read(event+18,2)-7)==(o['x']-1,o['y']):moved.add(lid)
 if step>30 and not read('sLockFieldControls',1):break
close();assert moved==set(performers),('Not all five dancers moved',moved)
for lid,o in performers.items():assert any(read(syms['gObjectEvents']+j*36+8,1)==lid and (read(syms['gObjectEvents']+j*36+16,2)-7,read(syms['gObjectEvents']+j*36+18,2)-7)==(o['x'],o['y']) for j in range(16))
walk((7,9));image('five-performer-show');print('Actual optional performance: all five move and return, controls released: PASS',flush=True)
go('EcruteakCity_PokemonCenter_1F');write(read('gPlayerPartyPtr')+86,1,2);talk((8,13))
for _ in range(12):key(1);frames(180)
close();assert read(read('gPlayerPartyPtr')+86,2)==read(read('gPlayerPartyPtr')+88,2)>1;image('nurse-healed');print('Actual rebuilt Center nurse heals and keeps heal ID: PASS',flush=True)
save_continue('center-normal-save')
go('EcruteakCity_Residence');walk((4,6));save_continue('house-normal-save')
# A synthetic old shared-layout cache, saved normally in a COPY, proves the scoped
# migration path. This is separate from the real old Bell9F battery test.
layouts=json.load(open('data/layouts/layouts.json'))['layouts'];old=next(i+1 for i,l in enumerate(layouts) if l['id']=='LAYOUT_HOUSE_WITH_BED');save_continue('old-shared-layout-fixture',old)
go('EcruteakCity_Gym');walk((10,10));frames(16,32);frames(300);close();assert current()=='EcruteakCity_Gym' and pos()==(10,20);image('lower-bridge-safe-return')
go('EcruteakCity_Gym_Arena');walk((4,10));frames(16,16);frames(300);close();assert current()=='EcruteakCity_Gym' and pos()==(10,20);image('upper-bridge-safe-return');print('Actual stepping off both bridge halves returns safely to entrance: PASS',flush=True)
go('EcruteakCity_Gym_Arena');talk((4,4));key(1);frames(120);key(1);frames(300)
assert read(syms['gTrainerBattleParameter']+2,2)==856;image('morty-battle')
# This fixture is for battle-loss/respawn, not battle difficulty assessment.
p=read('gPlayerPartyPtr');write(p+86,1,2)
for _ in range(200):
 key(1);frames(120)
 if current()!='EcruteakCity_Gym_Arena':break
close();assert current()=='EcruteakCity_PokemonCenter_1F',(current(),pos());assert read(p+86,2)==read(p+88,2)>0;assert pos()==(8,13),(current(),pos());image('ecruteak-whiteout');print('Actual Morty practice loss -> rebuilt local Center, heal and correct nurse arrival: PASS',flush=True)
