#!/usr/bin/env python3
"""Genuine normal-controller pre-fix batteries and independent cold Continue checks.

Create mode travels normally, uses native Save, and verifies each battery on the
old compiled ROM. Check mode binds no memory-write/snapshot API: it only cold
Continues these immutable batteries and compares exact payload/position/facing.
"""
import argparse,ctypes as C,hashlib,json,runpy,shutil,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('mode',choices=['create','check']);p.add_argument('--save',type=Path);p.add_argument('--fixtures',type=Path);p.add_argument('--library',default='/tmp/johto-bridge.so');p.add_argument('--rom-sha256',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest();rom=R/'pokeemerald.gba';assert sha(rom.read_bytes())==a.rom_sha256
syms={}
for line in subprocess.check_output(['arm-none-eabi-nm','-an',str(R/'pokeemerald.elf')],text=True).splitlines():
 v=line.split()
 if len(v)==3:
  try:syms[v[2]]=int(v[0],16)
  except ValueError:pass
lib=C.CDLL(a.library)
for n,t in [('emu_init',[C.c_char_p]),('emu_frames',[C.c_int,C.c_int]),('emu_read',[C.c_uint,C.c_int]),('emu_save',[C.c_char_p,C.c_int]),('emu_image',[C.c_char_p])]:getattr(lib,n).argtypes=t
lib.emu_read.restype=C.c_uint
read=lambda n,w=4:lib.emu_read(syms.get(n,n),w)
def frames(n=60,k=0):lib.emu_frames(k,n)
def key(k):frames(1,k);frames(20)
def sb():return read('gSaveBlock1Ptr')
def pos():return read(sb(),2),read(sb()+2,2)
groups=json.loads((R/'data/maps/map_groups.json').read_text());bylocation={(75,i):n for i,n in enumerate(groups['gMapGroup_CrossroadsOlivine'])}|{(76,i):n for i,n in enumerate(groups['gMapGroup_CrossroadsJohtoExpansion'])}
def current():return bylocation[read(sb()+4,1),read(sb()+5,1)]
def memory(addr,n):return bytes(read(addr+i,1)for i in range(n))
def state():
 count=read(read('gPlayerPartyCountPtr'),1);enc=read(read('gSaveBlock2Ptr')+0xac);inventory=dict(money=read(sb()+0x490)^enc,coins=read(sb()+0x494,2)^(enc&65535),registered=read(sb()+0x496,2),pc=memory(sb()+0x498,0xc8).hex(),bag=[(read(sb()+0x560+i*4,2),read(sb()+0x562+i*4,2)^(enc&65535))for i in range(186)])
 return dict(count=count,party=sha(memory(read('gPlayerPartyPtr'),count*100)),boxes=sha(memory(read('gPokemonStoragePtr'),0x83d0)),starter=read(sb()+0x1590,2),flags=sha(memory(sb()+0x1270,300)),decoded_inventory=sha(json.dumps(inventory,sort_keys=True).encode()))
def facing():return read(syms['gObjectEvents']+read(syms['gPlayerAvatar']+5,1)*36+24,1)&15
def boot(battery):
 assert lib.emu_init(str(rom).encode()) and lib.emu_save(str(battery).encode(),1);frames(4500);assert read(syms['gMain']+4)==syms['CB2_BlackLedgerTitle']|1;key(8);frames(180);key(1);frames(300);assert read(syms['gMain']+4)==syms['CB2_Overworld']|1;assert not read('sLockFieldControls',1);assert read('sJohtoTestAccess',1)==0

def native_save(battery):
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

if a.mode=='create':
 assert a.save and not a.fixtures;source_hash=sha(a.save.read_bytes());private=out/'input-copy.sav';assert a.save.resolve()!=private.resolve();shutil.copyfile(a.save,private)
 sys.path.insert(0,str(R/'crossroads/tools'));sys.argv=['johto_network_smoke.py','--save',str(private),'--library',a.library,'--output',str(out/'normal-setup'),'--targets',''];d=runpy.run_path(str(R/'crossroads/tools/johto_network_smoke.py'));go,walk,warp=[d[n]for n in ['go','walk','warp']];walk.__globals__['dry_only']=True;d['route_cache'].clear()
 cases=[('city-west-landing','EcruteakCity_WestGate',3,'EcruteakCity',(7,39),4),('route38-landing','EcruteakCity_WestGate',5,'JohtoRoute38',(62,14),3),('route42-landing','EcruteakCity_EastGate',5,'JohtoRoute42',(3,15),4),('westgate-landing','JohtoRoute38',1,'EcruteakCity_WestGate',(1,7),4),('eastgate-landing','JohtoRoute42',4,'EcruteakCity_EastGate',(10,7),3),('corridor-landing','BellchimeTrail',0,'EcruteakCity_BarrierCorridor',(6,3),1),('offlanding-control',None,None,'EcruteakCity',(32,43),None)]
 existing=json.loads((out/'fixtures.json').read_text())if(out/'fixtures.json').exists()else None
 if existing:assert existing['source_rom_sha256']==a.rom_sha256 and existing['source_battery_sha256']==source_hash
 records=[]if existing is None else existing['fixtures']
 for label,start,index,destination,xy,wanted in cases:
  if any(r['label']==label for r in records):
   old=next(r for r in records if r['label']==label);assert sha((out/old['battery_file']).read_bytes())==old['battery_sha256'];print('Retain completed genuine fixture',label,flush=True);continue
  if start is None:go(destination);walk(xy)
  else:go(start,index);warp(index)
  assert current()==destination and pos()==xy,(label,current(),pos(),destination,xy)
  payload=state();actual_facing=facing();assert lib.emu_image(str(out/(label+'-actual-old-arrival.png')).encode());battery=out/(label+'.sav');native_save(battery);assert state()==payload and current()==destination and pos()==xy and facing()==actual_facing
  boot(battery);assert current()==destination and pos()==xy and state()==payload and facing()==actual_facing,(label,'B4 native Save/cold Continue changed fixture',current(),pos(),facing(),actual_facing)
  assert lib.emu_image(str(out/(label+'-actual-old-cold-continue.png')).encode());row=dict(label=label,battery_file=battery.name,battery_sha256=sha(battery.read_bytes()),actual_map=destination,actual_position=list(xy),actual_old_facing=actual_facing,expected_new_facing=actual_facing if wanted is None else wanted,offlanding_control=wanted is None,exact_state_before=payload,old_normal_save_cold_continue_verified=True);records.append(row);(out/'fixtures.json').write_text(json.dumps(dict(source_rom_sha256=a.rom_sha256,source_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),source_battery_sha256=source_hash,source_battery_unchanged=sha(a.save.read_bytes())==source_hash,method='All positions genuinely reached with normal controller travel, native Save, then cold Continue on B4. No map/warp/position writes. Shared setup uses disclosed RAM-only encounter suppression/Survey desk, cleared by cold Continue.',fixtures=records),indent=2)+'\n');print('Actual B4 fixture PASS',label,current(),pos(),'facing',actual_facing,'new expected',row['expected_new_facing'],flush=True)
 assert sha(a.save.read_bytes())==source_hash
else:
 assert a.fixtures and not a.save;source=json.loads(a.fixtures.read_text());assert len(source['fixtures'])==7;records=[]
 for row in source['fixtures']:
  battery=a.fixtures.parent/row['battery_file'];assert sha(battery.read_bytes())==row['battery_sha256'];boot(battery);assert lib.emu_image(str(out/(row['label']+'-actual-new-cold-continue.png')).encode());actual=dict(map=current(),position=list(pos()),facing=facing(),state=state());assert actual['map']==row['actual_map'] and actual['position']==row['actual_position'] and actual['state']==row['exact_state_before'] and actual['facing']==row['expected_new_facing'],(row['label'],'Exact Continue target/payload/facing failed',actual,row);assert sha(battery.read_bytes())==row['battery_sha256'];records.append(dict(label=row['label'],actual_map=current(),actual_position=list(pos()),old_facing=row['actual_old_facing'],actual_new_facing=facing(),expected_new_facing=row['expected_new_facing'],offlanding_control=row['offlanding_control'],exact_party_boxes_starter_flags_decoded_inventory=True,source_battery_unchanged=True,result='PASS'));print('Actual new Continue PASS',records[-1],flush=True)
 (out/'results.json').write_text(json.dumps(dict(rom_sha256=a.rom_sha256,source_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),old_rom_sha256=source['source_rom_sha256'],method='Seven genuinely reached/native-saved B4 batteries, fresh-core normal Continue on candidate. No memory writes, snapshots, coordinate changes or survey toggles in check mode. Six intended facing corrections; one untouched offlanding control. Exact position and save payload asserted.',records=records),indent=2)+'\n')
assert sha(rom.read_bytes())==a.rom_sha256
print('Arrival normal Save/Continue',a.mode,'PASS',flush=True)
