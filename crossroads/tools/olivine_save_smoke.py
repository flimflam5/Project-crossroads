#!/usr/bin/env python3
"""Actual Save/cold Continue using copied batteries and explicit legacy fixtures.

Normal cases use controller movement. Legacy cases alone seed obsolete XY, heal
or cached-layout fields in private test RAM before normal Save. Never writes the
input battery, party, box, inventory, starter flags or permanent story progress.
"""
import argparse,hashlib,json,runpy,struct,subprocess,sys
from collections import deque
from pathlib import Path
R=Path(__file__).resolve().parents[2];BASE='fd151242458efe5759b18650f35a5e5b2fa47e45'
p=argparse.ArgumentParser();p.add_argument('--save',type=Path,required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');p.add_argument('--output',type=Path,default=R/'build/olivine-save-check');a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True)
source_hash=hashlib.sha256(a.save.read_bytes()).hexdigest()
sys.argv=['johto_network_smoke.py','--save',str(a.save),'--library',a.library,'--output',str(out),'--targets',''];d=runpy.run_path(str(R/'crossroads/tools/johto_network_smoke.py'))
go,walk,read,write,frames,key,current,pos,close,lib,syms,sb=[d[n]for n in ['go','walk','read','write','frames','key','current','pos','close','lib','syms','sb']]
records=[]
def memory(addr,size):return bytes(read(addr+i,1) for i in range(size))
def inventory_state():
 # Load/Continue legitimately rotates this engine's encryption key. Compare
 # every decoded value, not encrypted bytes that are expected to change.
 encryption=read(read('gSaveBlock2Ptr')+0xac,4)
 return dict(money=read(sb()+0x490,4)^encryption,coins=read(sb()+0x494,2)^(encryption&0xffff),registered_item=read(sb()+0x496,2),pc_items=memory(sb()+0x498,0xc8).hex(),bag=[(read(sb()+0x560+i*4,2),read(sb()+0x562+i*4,2)^(encryption&0xffff)) for i in range(186)])
def menu(action):
 key(8);frames(90)
 for _ in range(12):
  cursor=read('sStartMenuCursorPos',1)
  if read(syms['sCurrentStartMenuActions']+cursor,1)==action:break
  key(128)
 else:raise AssertionError(('Menu action missing',action))
 key(1);frames(180)
def dry_go(target):
 g=walk.__globals__;old=g['safe']
 def safe(n,p):return old(n,p) and d['raw'][n][p[1]*d['size'][n][0]+p[0]]>>12==3
 g['safe']=safe;g['route_cache'].clear()
 try:go(target)
 finally:g['safe']=old;g['route_cache'].clear()
def enable_survey():
 if read('sJohtoTestAccess',1):return
 dry_go('OlivineCity_HarborOffice');walk((1,6));frames(1,64);frames(20);key(1);frames(180)
 for _ in range(8):
  if not read('sLockFieldControls',1):break
  key(1);frames(180)
 assert read('sJohtoTestAccess',1)==1
def save_continue(label,relocated=False,heal_migration=False):
 before=(current(),pos());count=read(read('gPlayerPartyCountPtr'),1);party=memory(read('gPlayerPartyPtr'),count*100);boxes=memory(read('gPokemonStoragePtr'),0x83d0);choice=read(sb()+0x1590,2)
 dynamic_before=memory(sb()+0x14,8) if current()=='OlivineCity_Lighthouse_Elevator' else None
 inventory=inventory_state();flags=memory(sb()+0x1270,300)
 menu(5)
 for _ in range(8):key(1);frames(180)
 for _ in range(3):key(2);frames(120)
 assert read(syms['gMain']+4)==syms['CB2_Overworld']|1
 battery=out/(label+'.sav');assert lib.emu_save(str(battery).encode(),0)
 assert lib.emu_init(str(R/'pokeemerald.gba').encode());assert lib.emu_save(str(battery).encode(),1);frames(4500);key(8);frames(180);key(1);frames(300)
 assert read(syms['gMain']+4)==syms['CB2_Overworld']|1
 assert read('sJohtoTestAccess',1)==0,'Survey assistance must clear at cold boot'
 assert memory(read('gPlayerPartyPtr'),count*100)==party and memory(read('gPokemonStoragePtr'),0x83d0)==boxes and read(sb()+0x1590,2)==choice
 assert inventory_state()==inventory and memory(sb()+0x1270,300)==flags
 assert current()==before[0]
 if dynamic_before is not None:assert memory(sb()+0x14,8)==dynamic_before,'Native elevator return destination lost across cold Continue'
 if relocated:
  x,y=pos();v=d['raw'][current()][y*d['size'][current()][0]+x];assert pos()!=before[1] and not v&0xc00 and v>>12==3 and not read('gPlayerAvatar',1)&8,(label,before,pos(),hex(v))
  assert not any((e['x'],e['y'])==pos() for e in d['maps'][current()]['warp_events']+d['maps'][current()]['object_events']),'Migration must avoid doors/actors'
 else:assert (current(),pos())==before,(label,before,current(),pos())
 if heal_migration:
  heal=next(h for h in json.loads((R/'src/data/heal_locations.json').read_text())['heal_locations'] if h['id']=='HEAL_LOCATION_OLIVINE_CITY')
  assert (read(sb()+0x1c,1),read(sb()+0x1d,1))==d['locations']['OlivineCity']
  assert read(sb()+0x1e,1)==255 and (read(sb()+0x20,2),read(sb()+0x22,2))==(heal['x'],heal['y'])
 write('sWildEncountersDisabled',1,1);assert lib.emu_image(str(out/(label+'.png')).encode())
 records.append(dict(label=label,result='PASS',before=before,after=[current(),pos()],legacy_fixture=relocated or heal_migration,exact_party_boxes_inventory_flags_starter=True));print(label,'PASS',before,'->',current(),pos(),flush=True)
def seed_position(target):
 # This is an explicitly synthetic obsolete-coordinate fixture, not a claim
 # that the current ROM allowed controller movement into its solid wall/sea.
 write(sb(),target[0],2);write(sb()+2,target[1],2)
 player=syms['gObjectEvents']+read(syms['gPlayerAvatar']+5,1)*36
 for offset in (12,16,20):write(player+offset,target[0]+7,2);write(player+offset+2,target[1]+7,2)
def clear_point(n,near):
 pts=[(x,y) for y in range(d['size'][n][1]) for x in range(d['size'][n][0]) if d['safe'](n,(x,y)) and d['raw'][n][y*d['size'][n][0]+x]>>12==3 and (x,y) not in d['active_warps'](n)]
 return next(p for p in sorted(pts,key=lambda p:abs(p[0]-near[0])+abs(p[1]-near[1])) if d['path'](n,p) is not None)
dry_go('OlivineCity_PokemonCenter_1F');walk((8,13));save_continue('center-normal-save')
dry_go('OlivineCity_Residence');walk(clear_point(current(),(3,6)));save_continue('joe-home-normal-save')
# Existing old Center choice, not a new progress grant.
dry_go('OlivineCity');walk(clear_point(current(),(16,34)));g,n=d['locations']['OlivineCity'];write(sb()+0x1c,g,1);write(sb()+0x1d,n,1);write(sb()+0x1e,255,1);write(sb()+0x20,11,2);write(sb()+0x22,22,2);save_continue('old-olivine-heal-fixture',heal_migration=True)
# Actual Surf entry and saved surfing avatar must survive new waterfront repair.
enable_survey();go('OlivineCity');w,h=d['size']['OlivineCity'];raw=d['raw']['OlivineCity'];pairs=[]
for y in range(h):
 for x in range(w):
  if raw[y*w+x]>>12!=1 or not d['safe']('OlivineCity',(x,y)):continue
  for land in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   u,v=land
   if 0<=u<w and 0<=v<h and raw[v*w+u]>>12==3 and d['safe']('OlivineCity',land) and d['path']('OlivineCity',land) is not None:pairs.append((land,(x,y)))
assert pairs,'No genuine shore entry exists'
land,water=min(pairs,key=lambda p:abs(p[0][0]-pos()[0])+abs(p[0][1]-pos()[1]));walk(land);walk(water);assert read('gPlayerAvatar',1)&8;save_continue('surf-normal-save');assert read('gPlayerAvatar',1)&8;walk(land);assert not read('gPlayerAvatar',1)&8
# Choose obsolete positions from the immutable delivered48x48 source, rather
# than guessing cells that a previous game may never have allowed Joe to occupy.
previous=json.loads(subprocess.check_output(['git','show',BASE+':data/layouts/layouts.json'],cwd=R));oldmap=json.loads(subprocess.check_output(['git','show',BASE+':data/maps/OlivineCity/map.json'],cwd=R));layout=next(l for l in previous['layouts'] if l['id']==oldmap['layout']);b=subprocess.check_output(['git','show',BASE+':'+layout['blockdata_filepath']],cwd=R);oldtiles=struct.unpack('<'+str(len(b)//2)+'H',b);ow=layout['width'];exclude={(e['x'],e['y']) for e in oldmap['object_events']+oldmap['warp_events']}
for kind in ['water','wall']:
 candidates=[]
 for i,v in enumerate(oldtiles):
  x,y=i%ow,i//ow
  if (x,y) in exclude or v&0xc00 or v>>12!=3:continue
  now=raw[y*w+x]
  if kind=='water' and now>>12==1 and not now&0xc00 or kind=='wall' and now&0xc00:candidates.append((x,y))
 if not candidates:
  assert kind=='water','No genuine old walkable-wall fixture exists'
  # This particular delivered48x48 baseline has no walking cell newly flooded
  # by the source coastline. Still exercise the defensive walking/water guard
  # with an explicitly synthetic current shoreline coordinate, never pretend
  # it was walked in the older ROM.
  candidates=[water];label='synthetic-walking-water-safety-fixture'
 else:label='old-walking-'+kind+'-fixture'
 walk(clear_point('OlivineCity',(16,34)));target=min(candidates,key=lambda p:abs(p[0]-pos()[0])+abs(p[1]-pos()[1]));seed_position(target);save_continue(label,relocated=True)
# A deliberately stale shared-house layout must resolve to the current Center.
dry_go('OlivineCity_PokemonCenter_1F');walk((8,13));shared=next(i+1 for i,l in enumerate(previous['layouts']) if l['id']=='LAYOUT_HOUSE_WITH_BED');write(sb()+0x32,shared,2);save_continue('old-cached-layout-fixture');assert read(sb()+0x32,2)==read(syms['gMapHeader']+0x12,2)!=shared
dry_go('OlivineCity_SilphOffice');walk(clear_point(current(),(3,6)));seed_position((7,0));save_continue('old-office-ceiling-cap-fixture',relocated=True)
# Every new map and the critical branched lighthouse sections: genuinely walk
# to the saved point, Save/cold Continue, walk away, leave and return by its
# actual door/stair. No synthetic coordinate fixtures in these normal cases.
normal_rooms=[('OlivineCity_FishingHouse',(4,6),0),('OlivineCity_TradeHouse',(4,6),0),('OlivineCity_SealHouse',(4,6),0),('OlivineCity_Cafe',(6,9),0),('OlivineCity_PokemonCenter_B1F',(8,8),0),('OlivineCity_Lighthouse_Balcony',(14,9),0),('OlivineCity_Lighthouse_Elevator',(4,4),0),('OlivineCity_PortTerminal',(7,7),0),('OlivineCity_PortQuay',(16,18),0),('OlivineCity_Lighthouse_3F',(8,16),5),('OlivineCity_Lighthouse_6F',(11,13),0)]
for name,near,exit_index in normal_rooms:
 # Specifying the source3F balcony threshold selects its isolated southern
 # component through the real window/balcony/west-stair journey.
 g=walk.__globals__;original_safe=g['safe']
 def safe(n,p):return original_safe(n,p) and d['raw'][n][p[1]*d['size'][n][0]+p[0]]>>12==3
 g['safe']=safe;g['route_cache'].clear()
 try:go(name,exit_index)
 finally:g['safe']=original_safe;g['route_cache'].clear()
 target=clear_point(name,near);walk(target)
 if name=='OlivineCity_Lighthouse_3F':assert target[1]>=12 and d['path'](name,(13,7)) is None,'Test must save in the source isolated southern3F section'
 save_continue(name+'-normal-save')
 x,y=pos();away=next(p for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] if p not in d['active_warps'](name) and d['safe'](name,p) and d['raw'][name][p[1]*d['size'][name][0]+p[0]]>>12==3 and d['path'](name,p) is not None)
 walk(away);assert pos()==away and not read('gPlayerAvatar',1)&8
 go(name,exit_index);d['warp'](exit_index);assert current()!=name,(name,'Door/stair did not return after cold Continue')
 departed=current();go(name,exit_index);walk(target);assert current()==name and pos()==target
 records[-1].update(actual_walkaway=away,actual_exit_destination=departed,actual_return_to_saved_point=True)
 print('Actual post-Continue walkaway, door/stair exit and return:',name,'PASS',flush=True)
# Preserve both selectable cabin destinations across a cold boot. These use
# the actual panel messages/YES choice, not writes to native dynamicWarp.
for x,expected,label in [(2,'OlivineCity_Lighthouse_1F','elevator-selected-1F-normal-save'),(5,'OlivineCity_Lighthouse_6F','elevator-selected-6F-normal-save')]:
 dry_go('OlivineCity_Lighthouse_Elevator');walk((x,3));frames(1,64);frames(20);key(1);frames(120);key(1);frames(180);d['close']()
 expected_location=d['locations'][expected];assert (read(sb()+0x14,1),read(sb()+0x15,1))==expected_location,('Panel did not select actual lift destination',label)
 save_continue(label);walk((4,4));d['warp'](0);assert current()==expected,(label,'Cold Continue lost selected elevator floor',current(),pos())
 records[-1].update(actual_exit_destination=expected,actual_selected_floor_retained=True)
 print('Actual panel selection, cold Continue and exit:',label,'PASS',flush=True)
assert hashlib.sha256(a.save.read_bytes()).hexdigest()==source_hash,'Input owner/fixture battery was modified'
(out/'results.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest(),source_battery_sha256=source_hash,source_battery_unchanged=True,setup='Normal controller movement and menu saves. Explicit legacy fixtures seed obsolete XY/heal/cached-layout fields in private RAM; no party/box/bag/flag writes. The water guard uses a labelled synthetic current-shore coordinate because this baseline has no former walking cell newly flooded; actual Surf preservation is tested separately.',records=records),indent=2)+'\n')
print('Olivine normal/Surf/obsolete-location/heal/cache Save/cold Continue regression: PASS',flush=True)
