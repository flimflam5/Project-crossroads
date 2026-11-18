#!/usr/bin/env python3
"""Cold-Continue a genuine QA10 cave or Ruins save and verify recovery.

Uses a copied battery, real title UI and movement; disables encounters only
in test-process RAM. Writes output saves/snapshots and never commits them.
"""
import argparse,hashlib,json,runpy,shutil,sys
from pathlib import Path
from PIL import Image
R=Path.cwd();p=argparse.ArgumentParser();p.add_argument('--save',type=Path,required=True);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--rom-sha256',required=True);p.add_argument('--expect-relocation',action='store_true');p.add_argument('--expect-map',required=True);p.add_argument('--exit-map',required=True);p.add_argument('--expect-x',type=int,required=True);p.add_argument('--expect-y',type=int,required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');a=p.parse_args()
out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);sha=lambda b:hashlib.sha256(b).hexdigest();source=sha(a.save.read_bytes());base=json.loads(a.baseline.read_text());assert source==base['source_battery_sha256'];assert sha((R/'pokeemerald.gba').read_bytes())==a.rom_sha256
trial=out/'input-copy.sav';assert trial!=a.save.resolve();shutil.copyfile(a.save,trial);sys.path.insert(0,str(R/'crossroads/tools'));sys.argv=['johto_network_smoke.py','--save',str(trial),'--library',a.library,'--output',str(out/'tour'),'--targets','']
harness=R/'crossroads/tools/johto_network_smoke.py';d={'__file__':str(harness),'__name__':'union_partial_network'};exec(compile(harness.read_text().split("plans=json.loads(",1)[0],str(harness),'exec'),d);d['dry_only']=True;read,frames,key,current,pos,walk,lib,syms,sb=[d[n] for n in ('read','frames','key','current','pos','walk','lib','syms','sb')];assert lib.emu_state(str(out/'tour/start.snapshot').encode(),1);assert current()==a.expect_map,(base['continued_map'],current(),a.expect_map);old=tuple(base['continued_position']);landing=pos();assert landing==(a.expect_x,a.expect_y),('Unexpected exact candidate recovery',old,landing,(a.expect_x,a.expect_y));assert ((landing!=old or a.expect_map!=base['continued_map']) if a.expect_relocation else (landing==old and a.expect_map==base['continued_map'])),(old,landing,a.expect_relocation);assert d['safe'](a.expect_map,landing) and landing not in d['active_warps'](a.expect_map),('Unsafe relocation',landing);assert d['raw'][a.expect_map][landing[1]*d['size'][a.expect_map][0]+landing[0]]>>12==3,('Walking save landed off dry ground',landing)
def memory(x,n):return bytes(read(x+i,1) for i in range(n))
def payload():
 count=read(read('gPlayerPartyCountPtr'),1);enc=read(read('gSaveBlock2Ptr')+0xac);inv=dict(money=read(sb()+0x490)^enc,coins=read(sb()+0x494,2)^(enc&65535),registered=read(sb()+0x496,2),pc=memory(sb()+0x498,0xc8).hex(),bag=[(read(sb()+0x560+i*4,2),read(sb()+0x562+i*4,2)^(enc&65535)) for i in range(186)]);return dict(starter=read(sb()+0x1590,2),count=count,party=sha(memory(read('gPlayerPartyPtr'),count*100)),boxes=sha(memory(read('gPokemonStoragePtr'),0x83d0)),flags=sha(memory(sb()+0x1270,300)),decoded_inventory=sha(json.dumps(inv,sort_keys=True).encode()))
assert payload()==base['payload'],('Saved data changed',payload(),base['payload']);assert memory(sb()+0x1c,8).hex()==base['last_heal_location'],('Heal location changed',memory(sb()+0x1c,8).hex(),base['last_heal_location']);assert not read('sLockFieldControls',1)
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
assert expected>0;behavior=d['behavior'](a.expect_map,*landing)
if behavior==7:assert len(mismatches)<=10 and all(y>=height-2 for x,y in mismatches),('Unexpected grass occlusion',mismatches)
else:assert visible==expected,('Joe not fully visible on non-grass',landing,behavior,mismatches)
# Walk to another nearby ordinary floor tile, proving the arrival does not trap.
w,h=d['size'][a.expect_map];choices=[]
for y in range(2,h-2):
 for x in range(2,w-2):
  q=(x,y)
  if q!=landing and d['safe'](a.expect_map,q) and d['raw'][a.expect_map][y*w+x]>>12==3 and q not in d['active_warps'](a.expect_map) and d['path'](a.expect_map,q) is not None:choices.append(q)
assert choices,'No safe normal floor reachable';target=min(choices,key=lambda q:abs(q[0]-landing[0])+abs(q[1]-landing[1]));walk(target);assert pos()==target and current()==a.expect_map;frames(40);assert lib.emu_image(str(out/'walk-away.png').encode());assert payload()==base['payload'];assert memory(sb()+0x1c,8).hex()==base['last_heal_location']
# Perform a real in-game Save, then cold Continue the private copied battery.
key(8);frames(90)
for _ in range(12):
 cursor=read('sStartMenuCursorPos',1)
 if read(syms['sCurrentStartMenuActions']+cursor,1)==5:break
 key(128)
else:raise AssertionError('Native Save action absent')
key(1);frames(180)
for _ in range(8):key(1);frames(180)
for _ in range(3):key(2);frames(120)
assert current()==a.expect_map and pos()==target
assert lib.emu_save(str(trial).encode(),0)
assert lib.emu_init(str(R/'pokeemerald.gba').encode()) and lib.emu_save(str(trial).encode(),1);frames(4500);assert read(syms['gMain']+4)==syms['CB2_BlackLedgerTitle']|1;key(8);frames(180);key(1);frames(300)
assert current()==a.expect_map and pos()==target and payload()==base['payload'];assert memory(sb()+0x1c,8).hex()==base['last_heal_location'];d['write']('sWildEncountersDisabled',1,1)
# Track the engine's own modulo-128 friendship counter while walking to the exit.
# Controller direction holds are <= 16 frames, so no sampled call can contain
# 128 steps; longer calls carry no directional input.
party_count=read(read('gPlayerPartyCountPtr'),1);party_before=memory(read('gPlayerPartyPtr'),party_count*100)
friend_counter=lambda:read(sb()+0x139c+(0x402a-0x4000)*2,2)
start_counter=friend_counter();assert 0<=start_counter<128
step_track=[0];raw_frames=d['frames']
def tracked_frames(n=60,k=0):
 assert n<=127 or not(k & (16|32|64|128)),('Unbounded directional hold',n,k)
 a0=friend_counter();raw_frames(n,k);a1=friend_counter();assert a0<128 and a1<128;step_track[0]+=(a1-a0)%128
d['frames']=tracked_frames
d['go'](a.exit_map);assert current()==a.exit_map,('Cannot reach dry public exit',current(),a.exit_map)
assert friend_counter()==(start_counter+step_track[0])%128
wraps=(start_counter+step_track[0])//128
# Walking grants base +1, with at most +1 each for Luxury Ball and matching
# met location, and a 50% chance of no gain. Verify byte-by-byte with valid
# checksum adjustment, allowing no unrelated party mutation.
after=payload();assert {k:v for k,v in after.items() if k!='party'}=={k:v for k,v in base['payload'].items() if k!='party'},('Non-party payload changed',after,base['payload'])
party_after=memory(read('gPlayerPartyPtr'),party_count*100);deltas=[];order=[0,0,0,0,0,0,1,1,2,3,2,3,1,1,2,3,2,3,1,1,2,3,2,3]
for i in range(party_count):
 before=party_before[i*100:(i+1)*100];after_mon=party_after[i*100:(i+1)*100];personality=int.from_bytes(before[:4],'little');ot=int.from_bytes(before[4:8],'little');key=(personality^ot).to_bytes(4,'little');friend_index=32+12*order[personality%24]+9
 old_friend=before[friend_index]^key[(friend_index-32)%4];new_friend=after_mon[friend_index]^key[(friend_index-32)%4];delta=new_friend-old_friend
 for mon in (before,after_mon):
  clear=bytes(mon[j]^key[(j-32)%4] for j in range(32,80));checksum=sum(int.from_bytes(clear[j:j+2],'little') for j in range(0,48,2))&65535
  assert checksum==int.from_bytes(mon[28:30],'little'),('Invalid complete decrypted party checksum',i,checksum,int.from_bytes(mon[28:30],'little'))
 assert 0<=delta<=3*wraps,('Friendship gain exceeds engine walk bound',i,old_friend,new_friend,wraps,step_track[0])
 assert all(before[j]==after_mon[j] for j in range(100) if j not in (28,29,friend_index)),('Unexpected changed party bytes',i,[(j,before[j],after_mon[j]) for j in range(100) if before[j]!=after_mon[j]])
 assert (int.from_bytes(after_mon[28:30],'little')-int.from_bytes(before[28:30],'little'))%65536==(delta<<8)%65536,('Friendship checksum mismatch',i,delta)
 deltas.append(delta)
assert memory(sb()+0x1c,8).hex()==base['last_heal_location'];assert sha(a.save.read_bytes())==source and sha((R/'pokeemerald.gba').read_bytes())==a.rom_sha256
(out/'results.json').write_text(json.dumps(dict(rom_sha256=a.rom_sha256,old_map=base['continued_map'],old_position=old,arrival_map=a.expect_map,arrival=landing,walked_to=target,expected_relocation=a.expect_relocation,new_save_cold_continue=True,tracked_steps=step_track[0],friendship_wraps=wraps,friendship_deltas=deltas,walked_to_exit=a.exit_map,visible=visible,opaque=expected,behavior=behavior,private_source_unchanged=True,result='PASS'),indent=2)+'\n');print('genuine old position PASS',old,'->',landing,'->',target,'visible',visible,'/',expected,flush=True)
