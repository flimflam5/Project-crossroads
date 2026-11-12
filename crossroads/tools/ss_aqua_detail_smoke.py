#!/usr/bin/env python3
"""Actual normal-controller Aqua component, furnishing, NPC and wall checks.

Uses the independently SHA-pinned HGSS permission facts for blocked-target
expectations. Does not write positions, maps, warps, identity/items or story flags. A separately
labelled private berth-heal fixture reduces first-mon HP/status, then restores its
same-ROM snapshot after actual decline/accept verification; it is not a save-
compatibility fixture and never changes the input battery.
The shared harness discloses its RAM-only encounter/Survey fixture. Compile and
connectivity checks remain separate from this gameplay and from owner visual QA.
"""
import argparse,hashlib,json,runpy,struct,subprocess,sys
from collections import deque
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--save',type=Path,required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');p.add_argument('--output',type=Path,required=True);p.add_argument('--rom-sha256',required=True);p.add_argument('--skip-bumps',action='store_true',help='Separate scoped details run; never reports unexecuted bumps as passed');a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest();sourcehash=sha(a.save.read_bytes());assert sha((R/'pokeemerald.gba').read_bytes())==a.rom_sha256
factpath=R/'crossroads/hgss/qa10/ss-aqua-geometry.json';assert sha(factpath.read_bytes())=='a63af8054cf30e5b7724e7831e4d8d79d07d866b5522d3d03d1819123c09de07';facts=json.loads(factpath.read_text())
# This independently authored validator records exact named furniture bodies
# and explicit widened hatch/stair clearances reviewed against the HGSS mosaics.
# It is not the ship/map writer. No broad exception rectangles are accepted.
from validate_ss_aqua import MODEL_BODIES,OPEN_CLEARANCES
model_bodies={n:{(x+dx,y+dy)for x,y,w,h,reason in bodies for dx in range(w)for dy in range(h)}for n,bodies in MODEL_BODIES.items()}
headers={'SSAqua_1F':'MAP_SS_AQUA_1F','SSAqua_CaptainRoom':'MAP_SS_AQUA_CAPTAIN_ROOM','SSAqua_SoutheastCabins':'MAP_SS_AQUA_1F_SOUTHEAST_ROOMS','SSAqua_SouthwestCabins':'MAP_SS_AQUA_1F_SOUTHWEST_ROOMS','SSAqua_NortheastCabins':'MAP_SS_AQUA_1F_NORTHEAST_ROOMS','SSAqua_NorthwestCabins':'MAP_SS_AQUA_1F_NORTHWEST_ROOMS','SSAqua_B1F':'MAP_SS_AQUA_B1F'}
sys.argv=['johto_network_smoke.py','--save',str(a.save),'--library',a.library,'--output',str(out),'--targets',''];d=runpy.run_path(str(Path(__file__).with_name('johto_network_smoke.py')));go,walk,read,frames,key,current,pos,close,lib,syms,sb=[d[n]for n in ['go','walk','read','frames','key','current','pos','close','lib','syms','sb']];assert all(n in d['maps']for n in headers)
walk.__globals__['dry_only']=True;d['route_cache'].clear();records=[];native=[]
def memory(addr,n):return bytes(read(addr+i,1)for i in range(n))
def party_integrity(data):
 # Vanilla UpdateFriendshipStepCounter legitimately changes friendship every128
 # walked steps. Mask ONLY that growth byte and its checksum after decryption;
 # every species/owner/met/move/item/stat/status/other party byte stays exact.
 result=bytearray();order=[0,0,0,0,0,0,1,1,2,3,2,3,1,1,2,3,2,3,1,1,2,3,2,3]
 for i in range(0,len(data),100):
  mon=data[i:i+100];personality,ot=struct.unpack_from('<II',mon);cipher=personality^ot;secure=bytearray().join(struct.pack('<I',struct.unpack_from('<I',mon,32+j*4)[0]^cipher)for j in range(12));secure[order[personality%24]*12+9]=0;header=bytearray(mon[:32]);header[28:30]=bytes(2);result.extend(header+secure+mon[80:100])
 return sha(result)
def preserved():
 count=read(read('gPlayerPartyCountPtr'),1);enc=read(read('gSaveBlock2Ptr')+0xac);inventory=dict(money=read(sb()+0x490)^enc,coins=read(sb()+0x494,2)^(enc&65535),registered=read(sb()+0x496,2),pc=memory(sb()+0x498,0xc8).hex(),bag=[(read(sb()+0x560+i*4,2),read(sb()+0x562+i*4,2)^(enc&65535))for i in range(186)]);return dict(count=count,party=sha(memory(read('gPlayerPartyPtr'),count*100)),party_integrity_except_normal_walking_friendship=party_integrity(memory(read('gPlayerPartyPtr'),count*100)),boxes=sha(memory(read('gPokemonStoragePtr'),0x83d0)),starter=read(sb()+0x1590,2),flags=sha(memory(sb()+0x1270,300)),decoded_inventory=sha(json.dumps(inventory,sort_keys=True).encode()))
initial=preserved()
def save_report():
 (out/'results.json').write_text(json.dumps(dict(rom_sha256=a.rom_sha256,source_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),dirty_tracked_sources=bool(subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=R)),source_battery_sha256=sourcehash,source_battery_unchanged=sha(a.save.read_bytes())==sourcehash,method='Normal controller travel from copied battery. Source HGSS blocking facts independently SHA-pinned. Native screenshot inspection is separate from source tests and owner acceptance.',executed_collision_bumps=not a.skip_bumps,records=records,native_views=native),indent=2)+'\n')
def image(label):
 path=out/(label+'.png');frames(40);assert lib.emu_image(str(path).encode());im=Image.open(path).convert('RGB');assert im.size==(240,160);assert not any(v==(255,0,255)for v in im.getdata()),(label,'Actual framebuffer debug magenta');native.append(path.name);return im

def normal_save_cold_continue(label):
 before=(current(),pos());payload=preserved();key(8);frames(90)
 for _ in range(12):
  cursor=read('sStartMenuCursorPos',1)
  if read(syms['sCurrentStartMenuActions']+cursor,1)==5:break
  key(128)
 else:raise AssertionError(('Native Save menu action missing',before))
 key(1);frames(180)
 for _ in range(8):key(1);frames(180)
 for _ in range(3):key(2);frames(120)
 assert read(syms['gMain']+4)==syms['CB2_Overworld']|1
 battery=out/(label+'-normal-save.sav');assert lib.emu_save(str(battery).encode(),0)
 assert lib.emu_init(str(R/'pokeemerald.gba').encode()) and lib.emu_save(str(battery).encode(),1);frames(4500);assert read(syms['gMain']+4)==syms['CB2_BlackLedgerTitle']|1;key(8);frames(180);key(1);frames(300)
 assert read(syms['gMain']+4)==syms['CB2_Overworld']|1 and(current(),pos())==before and preserved()==payload,(label,'Normal Save/cold Continue changed room/position/payload',before,current(),pos())
 assert read('sJohtoTestAccess',1)==0 and not read('sLockFieldControls',1)
 image(label+'-cold-continue');records.append(dict(case='normal-save-cold-continue',map=current(),position=list(pos()),exact_party_boxes_starter_flags_decoded_inventory=True,result='PASS'));save_report()

def joe_visible(frame):
 s=syms['gSprites']+read(syms['gPlayerAvatar']+4,1)*68;tile=read(s+4,2)&1023;palette=read(s+4,2)>>12;matches=[]
 for i in range(128):
  addr=0x07000000+i*8;v0,v1,v2=read(addr,2),read(addr+2,2),read(addr+4,2)
  if(v2&1023)==tile and v2>>12==palette and not v0&0x300:matches.append((v0,v1,v2))
 assert len(matches)==1,('Unique normal Joe OAM entry missing',matches)
 v0,v1,v2=matches[0];assert not v0&0x2c00;dims=[[(8,8),(16,16),(32,32),(64,64)],[(16,8),(32,8),(32,16),(64,32)],[(8,16),(8,32),(16,32),(32,64)]];width,height=dims[v0>>14][v1>>14];x0,y0=v1&511,v0&255;x0=x0-512 if x0>=256 else x0;y0=y0-256 if y0>=160 else y0;assert 0<=x0<=240-width and 0<=y0<=160-height
 colors=[]
 for i in range(16):
  v=read(0x05000200+palette*32+i*2,2);colors.append(tuple(((v>>shift)&31)<<3|((v>>shift)&31)>>2 for shift in(0,5,10)))
 stride=width//8 if read(0x04000000,2)&64 else 32;expected=visible=0
 for y in range(height):
  for x in range(width):
   X=width-1-x if v1&0x1000 else x;Y=height-1-y if v1&0x2000 else y;index=tile+(Y//8)*stride+X//8;b=read(0x06010000+index*32+(Y%8)*4+(X%8)//2,1);color=(b>>(4*(X%2)))&15
   if color:expected+=1;visible+=int(frame.getpixel((x0+x,y0+y))==colors[color])
 assert visible==expected,('Joe hidden by ordinary open-room floor',current(),pos(),visible,expected)
 return dict(opaque_expected=expected,opaque_visible=visible)

def component(n):
 q=deque([pos()]);seen={pos()};warps=d['active_warps'](n)
 while q:
  x,y=q.popleft()
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   v=d['next_position'](x,y,dx,dy,lambda a_,b_:d['behavior'](n,a_,b_))
   if v is not None and v not in seen and v not in warps and d['safe'](n,v):seen.add(v);q.append(v)
 return seen

def source_blocked(n,x,y):
 f=facts[headers[n]];mw,mh=f['matrix_dimensions']
 if not(0<=x<mw*32 and 0<=y<mh*32):return True
 chunk=f['chunks'][(y//32)*mw+x//32];return bool(chunk['permissions'][(y%32)*32+x%32]&0x8000)

def record_clip(label,fn):
 g=walk.__globals__;old=g['frames'];local=globals()['frames'];folder=out/(label+'-frames');folder.mkdir(exist_ok=True);counter=[0]
 def record(n=60,k=0):
  while n:
   z=min(n,4);old(z,k);n-=z;lib.emu_image(str(folder/f'{counter[0]:04d}.png').encode());counter[0]+=1
 g['frames']=record;globals()['frames']=record
 try:fn()
 finally:g['frames']=old;globals()['frames']=local
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(out/(label+'.mp4'))],check=True)

def berth_rest(point,button,label):
 # This health-only service fixture follows existing Olivine heal tests. It is
 # separate from the strict migration test, which binds no emu_write at all.
 payload=preserved();snapshot=out/(label+'-health-fixture.snapshot');assert lib.emu_state(str(snapshot).encode(),0);party=read('gPlayerPartyPtr');count=read(read('gPlayerPartyCountPtr'),1)
 assert count>0;d['write'](party+86,1,2);d['write'](party+80,8,4)
 def open_prompt():
  frames(1,button);frames(20);key(1);frames(160);assert read('sLockFieldControls',1),(label,'Berth did not offer rest')
 open_prompt();image(label+'-decline-prompt');key(128);key(1);frames(180);close();assert read(party+86,2)==1 and read(party+80)==8,(label,'Declining rest altered health');assert pos()==point
 open_prompt();key(1);frames(600);close()
 assert all(read(party+i*100+86,2)==read(party+i*100+88,2)>0 and read(party+i*100+80)==0 for i in range(count)),(label,'Accepted berth failed to heal actual party')
 assert current()=='SSAqua_SoutheastCabins' and pos()==point and not read('sLockFieldControls',1);image(label+'-rested');assert lib.emu_state(str(snapshot).encode(),1);assert preserved()==payload,(label,'Health fixture isolation did not restore exact payload')
 records.append(dict(case='berth-rest',label=label,map=current(),position=list(point),fixture='Private first-mon1HP/poison only, isolated by exact-ROM snapshot; no identity/item/coordinate/story writes',decline_preserves_low_hp_and_poison=True,accept_all_party_full_hp_and_status_cured=True,source_battery_unchanged=True,result='PASS'));save_report()

def interact(event,label,index=None):
 n=current();x,y=event['x'],event['y'];candidate=None
 for distance in [1,2]:
  for dx,dy,k in [(0,1,64),(-1,0,16),(1,0,32),(0,-1,128)]:
   point=(x+dx*distance,y+dy*distance)
   if distance==2 and d['behavior'](n,x+dx,y+dy)!=0x80:continue
   if d['path'](n,point)is not None:candidate=(point,k);break
  if candidate:break
 assert candidate is not None,('No usable physical approach',n,event)
 point,k=candidate;walk(point)
 if event['script']=='SSAqua_Berth':berth_rest(point,k,label);return
 payload=preserved();frames(1,k);frames(20);key(1);frames(140);assert read('sLockFieldControls',1),(n,label,'NPC/sign did not interact')
 if index is not None:
  active=[]
  for i in range(16):
   b=syms['gObjectEvents']+i*36
   if read(b,1)&1 and(read(b+16,2)-7,read(b+18,2)-7)==(x,y):active.append(read(b+8,1))
  assert len(active)==1 and read('gSpecialVar_LastTalked',2)==active[0],(n,label,'Wrong actual NPC received A',active,read('gSpecialVar_LastTalked',2))
 image(label);close();assert current()==n and pos()==point and not read('sLockFieldControls',1);assert preserved()==payload,('New ambient interaction altered story/party data',n,label);records.append(dict(case='interaction',map=n,label=label,target=[x,y],approach=list(point),actual_npc_local_id=active[0]if index is not None else None,result='PASS'));save_report()

seen_components={n:[]for n in headers};bumps=0
for n in headers:
 for entry in range(len(d['maps'][n]['warp_events'])):
  go(n,entry);cells=component(n)
  if any(cells==old for old in seen_components[n]):continue
  # Overlapping reach sets with different initial active thresholds are the same
  # room. Only compare non-threshold floors; no paired cabin is silently skipped.
  core=cells-d['active_warps'](n)
  if any(core==(old-d['active_warps'](n))for old in seen_components[n]):continue
  seen_components[n].append(cells);part=len(seen_components[n]);eligible=[v for v in cells if v not in d['active_warps'](n)and all((v[0]+dx,v[1]+dy)in cells for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)])];assert eligible,('No clear room context',n,entry)
  point=min(eligible,key=lambda v:abs(v[0]-sum(x for x,y in cells)/len(cells))+abs(v[1]-sum(y for x,y in cells)/len(cells)));walk(point);frame=image(n+'-component-'+str(part));visibility=joe_visible(frame);records.append(dict(case='public-room-component',map=n,entry_warp=entry,component=part,position=list(pos()),floor_cells=len(core),joe_visibility=visibility,result='PASS'));save_report();normal_save_cold_continue(n+'-component-'+str(part));print('Room component',n,part,'PASS',len(core),'floor cells +Save/coldContinue',flush=True)
  if not a.skip_bumps:
   targets=[]
   for x,y in core:
    for dx,dy,k in [(0,1,128),(0,-1,64),(1,0,16),(-1,0,32)]:
     target=(x+dx,y+dy)
     if(source_blocked(n,*target)and target not in OPEN_CLEARANCES[n]or target in model_bodies[n])and target not in d['active_warps'](n):targets.append(((x,y),target,k))
   while targets:
    i=min(range(len(targets)),key=lambda j:abs(targets[j][0][0]-pos()[0])+abs(targets[j][0][1]-pos()[1]));approach,target,k=targets.pop(i);walk(approach);old=pos()
    def push():frames(32,k);frames(30)
    if bumps%35==0:record_clip(n+'-component-'+str(part)+'-wall-'+str(bumps),push)
    else:push()
    assert current()==n and pos()==old,('Walked through source wall/furnishing',n,approach,target,current(),pos());records.append(dict(case='source-blocked-bump',map=n,approach=list(approach),expected_solid_target=list(target),expectation='reference-reviewed furniture body'if target in model_bodies[n]else'source permission wall',result='PASS'));bumps+=1
   save_report()
 # Every visible source-room NPC/sign must actually interact, not only exist.
 for i,event in enumerate(d['maps'][n]['object_events']):
  for entry in range(len(d['maps'][n]['warp_events'])):
   go(n,entry)
   try:interact(event,n+'-npc-'+str(i+1),i);break
   except AssertionError as error:
    if error.args and isinstance(error.args[0],tuple)and error.args[0][0]=='No usable physical approach':continue
    raise
  else:raise AssertionError(('NPC unreachable in all room components',n,event))
 for i,event in enumerate(d['maps'][n]['bg_events']):
  for entry in range(len(d['maps'][n]['warp_events'])):
   go(n,entry)
   try:interact(event,n+'-sign-'+str(i+1));break
   except AssertionError as error:
    if error.args and isinstance(error.args[0],tuple)and error.args[0][0]=='No usable physical approach':continue
    raise
  else:raise AssertionError(('Sign unreachable in all room components',n,event))
expected={'SSAqua_1F':2,'SSAqua_CaptainRoom':1,'SSAqua_SoutheastCabins':2,'SSAqua_SouthwestCabins':2,'SSAqua_NortheastCabins':2,'SSAqua_NorthwestCabins':2,'SSAqua_B1F':1};actual={n:len(v)for n,v in seen_components.items()};assert actual==expected,('Actual source-room components not all exercised',actual,expected)
go('OlivineCity');final=preserved();assert {k:v for k,v in final.items()if k!='party'}=={k:v for k,v in initial.items()if k!='party'},'Payload changed beyond legitimate normal-walking friendship';records.append(dict(case='whole-tour-party-integrity',all_identity_species_owner_met_moves_items_stats_status_flags_boxes_inventory_preserved=True,normal_walking_friendship_change=final['party']!=initial['party'],result='PASS'));assert sha(a.save.read_bytes())==sourcehash and sha((R/'pokeemerald.gba').read_bytes())==a.rom_sha256;save_report();print('All7 ship maps/12 physical components, ambient NPC/signs andactualreturn PASS',actual,'sourcewallbumps',('SKIPPED, not a pass'if a.skip_bumps else'PASS'),bumps,flush=True)
