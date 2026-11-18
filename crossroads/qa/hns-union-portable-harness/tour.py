#!/usr/bin/env python3
"""External emulator tour of a SHA-pinned Union/Ruins ROM, with copied input.
Survey is enabled through its actual interaction; random encounters disabled in test RAM.
No debug position, warp, inventory, puzzle or save writes. Failures are preserved.
"""
import argparse,hashlib,json,runpy,shutil,subprocess,sys
from pathlib import Path
R=Path.cwd();p=argparse.ArgumentParser();p.add_argument('--rom-sha256',required=True);p.add_argument('--save',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');a=p.parse_args()
out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);sha=lambda b:hashlib.sha256(b).hexdigest();assert sha((R/'pokeemerald.gba').read_bytes())==a.rom_sha256
saved=sha(a.save.read_bytes());trial=out/'input-copy.sav';shutil.copyfile(a.save,trial)
sys.path.insert(0,str(R/'crossroads/tools'));sys.argv=['johto_network_smoke.py','--save',str(trial),'--library',a.library,'--output',str(out/'network'),'--targets','']
network=R/'crossroads/tools/johto_network_smoke.py';network_text=network.read_text();anchors=['arrival_only=arrivals();gate_borders=gate_connections();warp_trials=[];dry_only=False',"assert read('sJohtoTestAccess',1)==1\nfor n in targets:",'raw[n][y*w+x]>>12==3','raw[n][y*w+x]>>12 in (1,3)'];assert all(network_text.count(x)==1 for x in anchors),'Network harness changed; review planner substitutions';source=network_text.replace('arrival_only=arrivals();gate_borders=gate_connections();warp_trials=[];dry_only=False','arrival_only=arrivals();gate_borders=gate_connections();warp_trials=[];dry_only=True').replace("assert read('sJohtoTestAccess',1)==1\nfor n in targets:","assert read('sJohtoTestAccess',1)==1\ndry_only=False\nroute_cache.clear()\nfor n in targets:").replace('raw[n][y*w+x]>>12==3','raw[n][y*w+x]>>12 in (0,3)').replace('raw[n][y*w+x]>>12 in (1,3)','raw[n][y*w+x]>>12 in (0,1,3)');d={'__file__':str(network),'__name__':'__main__'};exec(compile(source,str(network),'exec'),d);go,walk,read,frames,key,current,pos,lib,syms,sb=[d[n] for n in ('go','walk','read','frames','key','current','pos','lib','syms','sb')]
report={'rom_sha256':a.rom_sha256,'cases':[],'warnings':[]}
def record(**kw):report['cases'].append(kw);(out/'coverage-in-progress.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',kw,flush=True)
def image(name):assert lib.emu_image(str(out/(name+'.png')).encode())
wanted_snaps={'UnionCave_1F','RuinsOfAlph','RuinsOfAlph_NorthwestPocket','RuinsOfAlph_NorthwestChamber','RuinsOfAlph_HallEntrance'};seen_snaps=set()
def snapshot_if_wanted():
 n=current()
 if n in wanted_snaps and n not in seen_snaps:
  path=out/(n+'.snapshot');assert lib.emu_state(str(path).encode(),0);path.with_suffix('.sha256').write_text(a.rom_sha256+'\n');seen_snaps.add(n);print('SNAPSHOT',n,path,flush=True)
# Explicit edges preserve every floor and the separate west Alph pockets.
edges=[('UnionCave_1F',0),('UnionCave_1F',1),('UnionCave_1F',2),('UnionCave_1F',3),('UnionCave_1F',4),('UnionCave_1F',5),('UnionCave_1F',6),('UnionCave_1F',7),('UnionCave_2F',1),('UnionCave_2F',3),('UnionCave_2F',4),('RuinsOfAlph_SouthwestPocket',1),('RuinsOfAlph_NorthwestPocket',1),('RuinsOfAlph',2),('RuinsOfAlph_HallEntrance',1)]
for n,index in edges:
 e=d['maps'][n]['warp_events'][index];other=d['ids'][e['dest_map']];back=int(e['dest_warp_id'])
 go(n,index);snapshot_if_wanted();d['warp'](index);assert current()==other;snapshot_if_wanted();arrival=pos();image(n+'-warp'+str(index)+'-arrival');d['warp'](back);assert current()==n;record(kind='reciprocal_warp',source=n,index=index,destination=other,return_index=back,arrival=arrival)
# Four cardinal controller bumps for accessible solid samples on each floor.
for n in ['UnionCave_1F','UnionCave_2F','UnionCave_3F']:
 go(n);w,h=d['size'][n];raw=d['raw'][n]
 for dx,dy,k in [(1,0,16),(-1,0,32),(0,1,128),(0,-1,64)]:
  chosen=None
  for y in range(1,h-1):
   if chosen:break
   for x in range(1,w-1):
    cell=(x,y);t=(x+dx,y+dy)
    if (raw[y*w+x]>>12)!=3 or not d['safe'](n,cell) or cell in d['active_warps'](n):continue
    if not(raw[t[1]*w+t[0]]&0xc00) or t in d['active_warps'](n):continue
    if d['path'](n,cell) is not None:chosen=cell;break
  assert chosen,(n,'no reachable collision sample',dx,dy);walk(chosen);old=pos()
  if dx==1 and dy==0:
   folder=out/(n+'-bump-frames');folder.mkdir(exist_ok=True)
   for i in range(16):
    frames(4,k if 4<=i<8 else 0);assert lib.emu_image(str(folder/f'{i:04d}.png').encode())
   subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(out/(n+'-bump.mp4'))],check=True)
  else:frames(16,k);frames(30)
  assert current()==n and pos()==old,(n,old,(dx,dy),pos());record(kind='collision',map=n,position=old,direction=[dx,dy])
 image(n+'-floor')
# Puzzle actions are actual button presses, with solver based on the static puzzle layout.
layouts={1:[[9,0,2,3,4,11],[0,5,6,12,0,14],[8,0,0,0,0,13],[1,7,0,15,16,10]],3:[[15,0,14,3,4,1],[13,0,6,7,0,10],[2,0,0,0,12,9],[8,0,5,0,16,11]]}
orient={1:[[0,0,4,4,4,1],[0,4,4,1,0,2],[0,0,0,0,0,3],[3,2,0,4,4,0]],3:[[2,2,1,4,4,3],[2,0,4,4,0,3],[3,0,0,0,4,0],[1,0,2,0,4,3]]}
solved=[[0,1,2,3,4,0],[0,5,6,7,8,0],[0,9,10,11,12,0],[0,13,14,15,16,0]]
def start_puzzle(n):
 go(n);walk((5,5));frames(1,64);frames(20);key(1);frames(240);assert read(syms['gMain']+4)==syms['CB2_SlidingPuzzle']|1,(n,'puzzle failed to open');image(n+'-puzzle')
for n,pid,dest in [('RuinsOfAlph_SouthwestChamber',1,(5,23)),('RuinsOfAlph_NorthwestChamber',3,(5,6))]:
 start_puzzle(n);key(2);frames(300);assert current()==n and not read('sLockFieldControls',1),(n,'cancel did not return');record(kind='puzzle_cancel',map=n)
 start_puzzle(n);board=[row[:] for row in layouts[pid]];ori={board[y][x]:orient[pid][y][x] for y in range(4) for x in range(6) if board[y][x]};cursor=[0,0]
 def moveto(y,x):
  while cursor[0]!=y:
   inc=(y-cursor[0])%4
   if inc<=2:key(128);cursor[0]=(cursor[0]+1)%4
   else:key(64);cursor[0]=(cursor[0]-1)%4
  while cursor[1]!=x:
   inc=(x-cursor[1])%6
   if inc<=3:key(16);cursor[1]=(cursor[1]+1)%6
   else:key(32);cursor[1]=(cursor[1]-1)%6
 for y in range(4):
  for x in range(1,5):
   target=solved[y][x]
   if board[y][x]==target and ori[target] in (0,4):continue
   source=next((r,c) for r in range(4) for c in range(6) if board[r][c]==target);sy,sx=source
   assert orient[pid][sy][sx]!=4,(pid,'attempt moving fixed tile',target,source)
   moveto(sy,sx);key(1);frames(30);board[sy][sx]=0
   for _ in range(ori[target]):key(512);frames(80)
   ori[target]=0;moveto(y,x);displaced=board[y][x];key(1);frames(30);board[y][x]=target
   if displaced:
    moveto(sy,sx);key(1);frames(30);board[sy][sx]=displaced
 frames(900);key(1);frames(600);assert current()=='RuinsOfAlph_UndergroundHall' and pos()==dest,(n,'solved but no hall arrival',current(),pos(),dest);image(n+'-success');record(kind='puzzle_solve',map=n,arrival=dest)
# The saved payload is decoded before comparison; private party bytes are hashed.
def memory(addr,n):return bytes(read(addr+i,1) for i in range(n))
def payload():
 count=read(read('gPlayerPartyCountPtr'),1);enc=read(read('gSaveBlock2Ptr')+0xac)
 inv=dict(money=read(sb()+0x490)^enc,coins=read(sb()+0x494,2)^(enc&65535),registered=read(sb()+0x496,2),pc=memory(sb()+0x498,0xc8).hex(),bag=[(read(sb()+0x560+i*4,2),read(sb()+0x562+i*4,2)^(enc&65535)) for i in range(186)])
 return dict(starter=read(sb()+0x1590,2),count=count,party=sha(memory(read('gPlayerPartyPtr'),count*100)),boxes=sha(memory(read('gPokemonStoragePtr'),0x83d0)),flags=sha(memory(sb()+0x1270,300)),decoded_inventory=sha(json.dumps(inv,sort_keys=True).encode()),last_heal=memory(sb()+0x1c,8).hex())
# Actual water entry, movement, in-game Save and cold Continue, no persistent Survey flags.
go('UnionCave_2F');n=current();w,h=d['size'][n];candidates=[(x,y) for y in range(h) for x in range(w) if d['raw'][n][y*w+x]>>12==1 and d['safe'](n,(x,y)) and (x,y) not in d['active_warps'](n) and d['path'](n,(x,y)) is not None];assert candidates,'No reachable water';target=min(candidates,key=lambda q:len(d['path'](n,q)));walk(target);assert read('gPlayerAvatar',1)&8,('No actual surfing',target);image('surf-before-save');old=pos();before=payload();key(8);frames(90)
for _ in range(12):
 cursor=read('sStartMenuCursorPos',1)
 if read(syms['sCurrentStartMenuActions']+cursor,1)==5:break
 key(128)
else:raise AssertionError('Native Save unavailable')
key(1);frames(180)
for _ in range(8):key(1);frames(180)
for _ in range(3):key(2);frames(120)
assert current()==n and pos()==old;battery=out/'private-new-water.sav';assert lib.emu_save(str(battery).encode(),0)
assert lib.emu_init(str(R/'pokeemerald.gba').encode()) and lib.emu_save(str(battery).encode(),1);frames(4500);assert read(syms['gMain']+4)==syms['CB2_BlackLedgerTitle']|1;key(8);frames(180);key(1);frames(300);assert current()==n and pos()==old and read('gPlayerAvatar',1)&8,('Surf not restored on cold Continue',current(),pos(),read('gPlayerAvatar',1));assert payload()==before,('Surf save altered party/boxes/flags/inventory/heal data',before,payload());image('surf-cold-continue');d['write']('sWildEncountersDisabled',1,1);adjacent=[(old[0]+dx,old[1]+dy) for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)] if 0<=old[0]+dx<w and 0<=old[1]+dy<h and d['raw'][n][(old[1]+dy)*w+old[0]+dx]>>12==1 and d['safe'](n,(old[0]+dx,old[1]+dy)) and (old[0]+dx,old[1]+dy) not in d['active_warps'](n) and d['path'](n,(old[0]+dx,old[1]+dy)) is not None];assert adjacent,('No adjacent water for cold-Continue movement',old);walk(adjacent[0]);assert read('gPlayerAvatar',1)&8 and current()==n and pos()==adjacent[0];record(kind='surf_save_continue',map=n,position=old,walked_to=pos(),payload_equal=True)
assert sha(a.save.read_bytes())==saved and sha((R/'pokeemerald.gba').read_bytes())==a.rom_sha256
report['result']='PASS';(out/'coverage.json').write_text(json.dumps(report,indent=2)+'\n');print('All requested emulator cases PASS',flush=True)
