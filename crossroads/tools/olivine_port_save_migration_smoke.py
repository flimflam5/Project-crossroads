#!/usr/bin/env python3
"""Cold-Continue real QA09 walking/Surf batteries across the QA10 port footprint.

The input positions were genuinely reached and normally saved on the old ROM;
no XY/map/warp/party/save-flag RAM writes are used here. Never overwrites them.
"""
import argparse,ctypes as C,hashlib,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--fixtures',type=Path,required=True);p.add_argument('--rom-sha256',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');p.add_argument('--output',type=Path,required=True);p.add_argument('--only-label',help='Explicitly focused diagnostic; unselected fixtures are not claimed tested');p.add_argument('--valid-surf-battery',type=Path,help='Actual historical normally-saved Surf battery at a still-water control position');p.add_argument('--valid-surf-position',nargs=2,type=int,metavar=('X','Y'));a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True)
rom=R/'pokeemerald.gba';digest=lambda b:hashlib.sha256(b).hexdigest();assert digest(rom.read_bytes())==a.rom_sha256
source=json.loads(a.fixtures.read_text());assert len(source['fixtures'])==2
lib=C.CDLL(a.library)
for n,t in [('emu_init',[C.c_char_p]),('emu_frames',[C.c_int,C.c_int]),('emu_read',[C.c_uint,C.c_int]),('emu_save',[C.c_char_p,C.c_int]),('emu_image',[C.c_char_p])]:getattr(lib,n).argtypes=t
lib.emu_read.restype=C.c_uint;syms={}
for line in subprocess.check_output(['arm-none-eabi-nm','-an',str(R/'pokeemerald.elf')],text=True).splitlines():
 v=line.split()
 if len(v)==3:
  try:syms[v[2]]=int(v[0],16)
  except ValueError:pass

def read(addr,width=4):return lib.emu_read(syms.get(addr,addr),width)
def frames(count=60,keys=0):lib.emu_frames(keys,count)
def key(keys):frames(1,keys);frames(20)
def sb():return read('gSaveBlock1Ptr')
def pos():return read(sb(),2),read(sb()+2,2)
def memory(addr,size):return bytes(read(addr+i,1)for i in range(size))
def state():
 count=read(read('gPlayerPartyCountPtr'),1);enc=read(read('gSaveBlock2Ptr')+0xac);inventory=dict(money=read(sb()+0x490)^enc,coins=read(sb()+0x494,2)^(enc&65535),registered=read(sb()+0x496,2),pc=memory(sb()+0x498,0xc8).hex(),bag=[(read(sb()+0x560+i*4,2),read(sb()+0x562+i*4,2)^(enc&65535))for i in range(186)])
 return dict(count=count,party_sha256=digest(memory(read('gPlayerPartyPtr'),count*100)),boxes_sha256=digest(memory(read('gPokemonStoragePtr'),0x83d0)),starter=read(sb()+0x1590,2),flags_sha256=digest(memory(sb()+0x1270,300)),decoded_inventory_sha256=digest(json.dumps(inventory,sort_keys=True).encode()))
groups=json.loads((R/'data/maps/map_groups.json').read_text());city_location=(75,groups['gMapGroup_CrossroadsOlivine'].index('OlivineCity'));city=json.loads((R/'data/maps/OlivineCity/map.json').read_text());blocked_events={(e['x'],e['y'])for key_ in ['warp_events','object_events','bg_events']for e in city[key_]}
def current_location():return read(sb()+4,1),read(sb()+5,1)
def actual_tile(x,y):
 width=read('gBackupMapLayout');ptr=read(syms['gBackupMapLayout']+8);assert width>14 and ptr
 return read(ptr+((y+7)*width+x+7)*2,2)
def boot(battery):
 assert lib.emu_init(str(rom).encode()) and lib.emu_save(str(battery).encode(),1);frames(4500);assert read(syms['gMain']+4)==syms['CB2_BlackLedgerTitle']|1
 key(8);frames(180);key(1);frames(300);assert read(syms['gMain']+4)==syms['CB2_Overworld']|1;assert not read('sLockFieldControls',1);assert read('sJohtoTestAccess',1)==0

def normal_save(battery):
 key(8);frames(90)
 for _ in range(12):
  cursor=read('sStartMenuCursorPos',1)
  if read(syms['sCurrentStartMenuActions']+cursor,1)==5:break
  key(128)
 else:raise AssertionError('Native Save action missing')
 key(1);frames(180)
 for _ in range(8):key(1);frames(180)
 for _ in range(3):key(2);frames(120)
 assert read(syms['gMain']+4)==syms['CB2_Overworld']|1;assert lib.emu_save(str(battery).encode(),0)

def verify_joe(surf):
 object_id=read(syms['gPlayerAvatar']+5,1);actual_graphics=read(syms['gObjectEvents']+object_id*36+4,2);expected=0x3f06 if surf else 250;assert actual_graphics==expected,('Wrong player graphics after Continue',surf,actual_graphics,expected)
 sprite=syms['gSprites']+read(syms['gPlayerAvatar']+4,1)*68;tile=read(sprite+4,2)&1023;name='surfing.png_mwidth_4__mheight_4.4bpp'if surf else'walking.png_mwidth_2__mheight_4.4bpp';size=512 if surf else 256;data=(R/'build/assets/graphics/object_events/pics/people/joe/corporate'/name).read_bytes();actual=memory(0x06010000+tile*32,size);assert actual in[data[j:j+size]for j in range(0,len(data),size)],('Actual OBJ VRAM is not Joe',surf,actual_graphics)
 return dict(graphics=actual_graphics,actual_obj_vram_matches_joe=True)

records=[]
selected=[row for row in source['fixtures']if not a.only_label or row['label']==a.only_label];assert selected,('No matching fixture',a.only_label)
for row in selected:
 battery=a.fixtures.parent/row['battery_file'];assert digest(battery.read_bytes())==row['battery_sha256'];label=row['label'];boot(battery)
 arrival=pos();tile=actual_tile(*arrival);avatar=read('gPlayerAvatar',1);assert lib.emu_image(str(out/(label+'-candidate-arrival-before-safety-assert.png')).encode());(out/(label+'-candidate-arrival.json')).write_text(json.dumps(dict(label=label,rom_sha256=a.rom_sha256,arrival=list(arrival),tile=hex(tile),avatar_flags=avatar,expected_safety='Must be dry, unblocked, outside active doors/actors and naturally walking; test writes no avatar/position/map state'),indent=2)+'\n');assert current_location()==city_location and state()==row['state_before'],(label,'Save payload/progress changed')
 assert arrival!=tuple(row['actual_old_position']),('Footprint migration did not move actual old save',label,arrival)
 assert not tile&0xc00 and tile>>12==3 and not avatar&8,(label,'Not a safe walking arrival',arrival,hex(tile),avatar)
 assert arrival not in blocked_events,(label,'Arrival occupies an actor/sign/active door',arrival);joe_arrival=verify_joe(False)
 assert lib.emu_image(str(out/(label+'-migrated-arrival.png')).encode())
 x,y=arrival
 for dx,dy,k in [(0,1,128),(0,-1,64),(1,0,16),(-1,0,32)]:
  target=(x+dx,y+dy);v=actual_tile(*target)
  if not v&0xc00 and v>>12==3 and target not in blocked_events:break
 else:raise AssertionError((label,'No actual dry walk-away cell',arrival))
 frames(16,k);frames(30);assert pos()==target and current_location()==city_location,(label,'Cannot actually walk away',arrival,target,pos());assert not read('gPlayerAvatar',1)&8;verify_joe(False)
 assert lib.emu_image(str(out/(label+'-walk-away.png')).encode());post_walk_payload=state();private=out/(label+'-new-normal-save.sav');normal_save(private);saved_position=pos();boot(private)
 assert pos()==saved_position and state()==post_walk_payload and not read('gPlayerAvatar',1)&8,(label,'New Save/coldContinue not stable')
 verify_joe(False);assert lib.emu_image(str(out/(label+'-new-cold-continue.png')).encode());assert digest(battery.read_bytes())==row['battery_sha256']
 records.append(dict(label=label,result='PASS',old_position=row['actual_old_position'],old_surf=row['old_surf'],new_arrival=list(arrival),walk_away=list(target),new_save_continue=list(pos()),native_tile=hex(tile),exact_party_boxes_starter_flags_decoded_inventory=True,old_battery_unchanged=True,joe=joe_arrival));print(label,'PASS',records[-1],flush=True)
if a.valid_surf_battery:
 assert not a.only_label and a.valid_surf_position is not None
 valid_hash=digest(a.valid_surf_battery.read_bytes());boot(a.valid_surf_battery);expected=tuple(a.valid_surf_position);assert current_location()==city_location and pos()==expected
 tile=actual_tile(*pos());assert not tile&0xc00 and tile>>12==1 and read('gPlayerAvatar',1)&8,('Valid old water Surf was incorrectly forced off',pos(),hex(tile),read('gPlayerAvatar',1));joe=verify_joe(True);assert lib.emu_image(str(out/'valid-old-surf-water-arrival.png').encode())
 x,y=pos()
 for dx,dy,k in[(0,1,128),(0,-1,64),(1,0,16),(-1,0,32)]:
  target=(x+dx,y+dy);v=actual_tile(*target)
  if not v&0xc00 and v>>12==1 and target not in blocked_events:break
 else:raise AssertionError('Valid Surf control has no water continuation')
 frames(8,k);frames(30)
 if pos()==expected:frames(8,k);frames(30)
 assert pos()==target and read('gPlayerAvatar',1)&8;verify_joe(True);payload=state();new=out/'valid-old-surf-water-new-save.sav';normal_save(new);boot(new);assert pos()==target and state()==payload and read('gPlayerAvatar',1)&8;verify_joe(True);assert lib.emu_image(str(out/'valid-old-surf-water-new-continue.png').encode());assert digest(a.valid_surf_battery.read_bytes())==valid_hash
 records.append(dict(label='valid-old-surf-water-retained',result='PASS',actual_old_position=list(expected),new_arrival=list(expected),actual_water_movement=list(target),new_normal_save_cold_continue=list(pos()),source_battery_sha256=valid_hash,source_battery_unchanged=True,joe=joe));print('Actual existing Surf-water control PASS',records[-1],flush=True)
(out/'results.json').write_text(json.dumps(dict(rom_sha256=a.rom_sha256,source_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),dirty_tracked_sources=bool(subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=R)),actual_old_rom_sha256=source['source_rom_sha256'],explicitly_focused_label=a.only_label,selected_fixture_count=len(selected),method='Actual old-ROM normally saved walking and Surf batteries; fresh-core normal Continue on new ROM; actual buffer tile reads, normal walk-away and new normal Save/cold Continue. No coordinate or save-state writes.',records=records),indent=2)+'\n');assert digest(rom.read_bytes())==a.rom_sha256
print('Selected genuine old port save migration PASS',len(selected),'fixtures',flush=True)
