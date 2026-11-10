#!/usr/bin/env python3
"""Controller bridge/collision, services, normal Save/Continue and save fixtures.

No map/warp writes. Disclosed fixtures:1HP for existing Morty practice loss and
one obsolete walking position in a copied save. Never writes the source battery.
"""
import argparse,runpy,sys,json,hashlib,subprocess
from pathlib import Path
from collections import deque
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');a=p.parse_args();out=Path('build/qa06-violet-detail');out.mkdir(parents=True,exist_ok=True)
sys.argv=['johto_network_smoke.py','--save',a.save,'--library',a.library,'--output',str(out),'--targets',''];d=runpy.run_path('crossroads/tools/johto_network_smoke.py')
go,walk,read,write,frames,key,current,pos,close,lib,syms,sb=[d[n] for n in ['go','walk','read','write','frames','key','current','pos','close','lib','syms','sb']]
def image(n):assert lib.emu_image(str(out/(n+'.png')).encode())
def menu(action):
 key(8);frames(90)
 for _ in range(12):
  c=read('sStartMenuCursorPos',1)
  if read(syms['sCurrentStartMenuActions']+c,1)==action:break
  key(128)
 else:raise AssertionError(('Missing menu action',action))
 key(1);frames(180)
def memory(addr,size):return bytes(read(addr+i,1) for i in range(size))
def save_continue(label,relocate=False):
 before=(current(),pos());count=read(read('gPlayerPartyCountPtr'),1);party=memory(read('gPlayerPartyPtr'),count*100);boxes=memory(read('gPokemonStoragePtr'),0x83d0);choice=read(sb()+0x1590,2)
 menu(5)
 for _ in range(8):key(1);frames(180)
 for _ in range(3):key(2);frames(120)
 assert read(syms['gMain']+4)==syms['CB2_Overworld']|1
 battery=out/(label+'.sav');assert lib.emu_save(str(battery).encode(),0)
 assert lib.emu_init(str(Path('pokeemerald.gba').resolve()).encode());assert lib.emu_save(str(battery).encode(),1);frames(4500);key(8);frames(180);key(1);frames(300)
 assert read(syms['gMain']+4)==syms['CB2_Overworld']|1
 assert read('sJohtoTestAccess',1)==0,'Survey access must remain RAM-only after cold boot'
 assert memory(read('gPlayerPartyPtr'),count*100)==party and memory(read('gPokemonStoragePtr'),0x83d0)==boxes and read(sb()+0x1590,2)==choice
 assert current()==before[0]
 if relocate:
  x,y=pos();tile=d['raw'][current()][y*d['size'][current()][0]+x];assert pos()!=before[1] and not tile&0xc00 and tile>>12==3 and not read('gPlayerAvatar',1)&8
 else:assert (current(),pos())==before,(label,before,current(),pos())
 write('sWildEncountersDisabled',1,1);image(label);print('Normal Save/cold Continue, exact party/boxes/starter and '+('safe obsolete-position migration' if relocate else 'exact position')+':',label,'PASS',flush=True)
def dry_walk(target):
 n=current();start=pos();q=deque([start]);prev={start:None};blocked={(e['x'],e['y']) for e in d['maps'][n]['warp_events']}-{start,target};w,h=d['size'][n]
 while q:
  x,y=q.popleft()
  for v in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if v in prev or v in blocked or not d['safe'](n,v):continue
   if d['raw'][n][v[1]*w+v[0]]>>12!=3:continue
   prev[v]=(x,y);q.append(v)
 assert target in prev,(n,start,'No dry path',target)
 route=[];v=target
 while prev[v] is not None:route.append(v);v=prev[v]
 for v in reversed(route):walk(v);assert not read('gPlayerAvatar',1)&8,'Pedestrian bridge route entered Surf'
def nearest_view(target):
 n=current();w,h=d['size'][n];points=sorted(((x,y) for y in range(h) for x in range(w) if d['safe'](n,(x,y))),key=lambda v:(abs(v[0]-target[0])+abs(v[1]-target[1]),v))
 return next(v for v in points if d['path'](n,v) is not None)
def enable_survey():
 # Cold Continue intentionally clears assistance. Plan a genuinely dry trip
 # to the actual desk, then opt in again through its ordinary interaction.
 if read('sJohtoTestAccess',1):return
 g=walk.__globals__;old=g['safe']
 def dry_safe(n,p):return old(n,p) and d['raw'][n][p[1]*d['size'][n][0]+p[0]]>>12==3
 g['safe']=dry_safe;g['route_cache'].clear()
 try:
  go('OlivineCity_HarborOffice');walk((1,6));frames(1,64);frames(20);key(1);frames(180)
  for _ in range(8):
   if not read('sLockFieldControls',1):break
   key(1);frames(180)
  assert read('sJohtoTestAccess',1)==1
 finally:g['safe']=old;g['route_cache'].clear()
views=[('VioletCity',(39,26),'pond-plaza'),('VioletCity',(39,14),'sprout-exterior'),('VioletCity',(31,44),'owner-gym'),('VioletCity',(47,44),'school-exterior'),('VioletCity',(49,58),'center-exterior'),('VioletCity',(12,40),'northwest-house-exterior'),('VioletCity_Residence',(4,5),'guest-house'),('VioletCity_Workshop',(4,5),'northwest-house'),('VioletAcademy',(6,7),'school-classroom'),('SproutTower_1F',(15,20),'sprout-1f'),('SproutTower_2F',(15,20),'sprout-2f'),('SproutTower_3F',(15,20),'sprout-3f'),('VioletCity_Gym',(8,12),'gym-fixed-access'),('VioletCity_PokemonCenter_B1F',(8,7),'center-basement'),('VioletCity_Mart',(4,8),'mart-interior')]
for n,target,label in views:go(n);walk(nearest_view(target));image(label)
# Record a truly pedestrian round trip over both newly drawn source bridges.
go('VioletCity');walk((31,44));dry_walk((39,35));movie=out/'bridge-frames';movie.mkdir(exist_ok=True);g=walk.__globals__;original_frames=g['frames'];frame_count=0
def recorded(n=60,k=0):
 global frame_count
 while n:
  step=min(4,n);original_frames(step,k);assert lib.emu_image(str(movie/f'{frame_count:05}.png').encode());frame_count+=1;n-=step
g['frames']=recorded
dry_walk((39,16));dry_walk((39,35));g['frames']=original_frames;frames=original_frames
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(movie/'%05d.png'),'-vf','scale=480:320:flags=neighbor','-pix_fmt','yuv420p',str(out/'violet-bridges.mp4')],check=True)
print('Actual pedestrian round trip across both reference bridges, no Surf:',frame_count,'recorded frames PASS',flush=True)
# Accessible forest edges/bridge rails/building footprint probes in all directions.
go('VioletCity');probes=[];warps={(e['x'],e['y']) for e in d['maps'][current()]['warp_events']};w,h=d['size'][current()]
for y in range(h):
 for x in range(w):
  for dx,dy,button in [(1,0,16),(-1,0,32),(0,1,128),(0,-1,64)]:
   tx,ty=x+dx,y+dy
   if 0<=tx<w and 0<=ty<h and (x,y) not in warps and (tx,ty) not in warps and d['raw'][current()][ty*w+tx]&0xc00 and d['safe'](current(),(x,y)) and d['raw'][current()][y*w+x]>>12==3:probes.append(((x,y),(tx,ty),button))
# Cover every reachable dry edge, excluding inaccessible backs rather than
# pretending the whole source forest boundary was inspected from inside it.
count=0;unreachable=[]
while probes:
 probes.sort(key=lambda e:abs(e[0][0]-pos()[0])+abs(e[0][1]-pos()[1]));point,target,button=probes.pop(0)
 if d['path'](current(),point) is None:unreachable.append([point,target]);continue
 walk(point);frames(16,button);frames(20);assert current()=='VioletCity' and pos()==point,(point,target,current(),pos());count+=1
assert count>100
print('Actual Violet city dry-edge wall/tree/bridge/boundary controller probes:',count,'PASS',flush=True)
go('VioletCity_PokemonCenter_1F');walk((8,13));write(read('gPlayerPartyPtr')+86,1,2);frames(1,64);frames(20);key(1);frames(120)
for _ in range(12):key(1);frames(180)
close();assert read(read('gPlayerPartyPtr')+86,2)==read(read('gPlayerPartyPtr')+88,2)>1;image('nurse-healed');save_continue('center-normal-save')
go('VioletCity_Residence');walk((4,6));save_continue('house-normal-save')
enable_survey();go('VioletCity');walk((31,44));walk((35,20));assert read('gPlayerAvatar',1)&8;save_continue('surf-normal-save');assert read('gPlayerAvatar',1)&8
walk((31,44));assert not read('gPlayerAvatar',1)&8
# Synthetic legacy walking save on a coordinate flooded by new canonical pond.
target=(31,20);assert d['raw']['VioletCity'][target[1]*64+target[0]]>>12==1
write(sb(),target[0],2);write(sb()+2,target[1],2)
event=syms['gObjectEvents']+read(syms['gPlayerAvatar']+5,1)*36
for offset in (12,16,20):write(event+offset,target[0]+7,2);write(event+offset+2,target[1]+7,2)
save_continue('old-walking-pond-fixture',relocate=True)
enable_survey()
# Genuine loss in an existing approved practice fight, not a fabricated trainer.
go('VioletCity_PokemonCenter_1F');go('EcruteakCity_Gym_Arena');walk((4,4));frames(1,64);frames(20);key(1);frames(120);key(1);frames(120);key(1);frames(300)
assert read(syms['gTrainerBattleParameter']+2,2)==856
write(read('gPlayerPartyPtr')+86,1,2)
for _ in range(200):
 key(1);frames(120)
 if current()!='EcruteakCity_Gym_Arena':break
close();assert current()=='VioletCity_PokemonCenter_1F' and pos()==(8,13),(current(),pos());assert read(read('gPlayerPartyPtr')+86,2)>1;image('violet-whiteout')
(out/'coverage.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256(Path('pokeemerald.gba').read_bytes()).hexdigest(),views=[x[2] for x in views],pedestrian_bridges_both_directions=True,blocked_edge_probes=count,unreachable_probe_backs=unreachable,normal_saves=['center','house','surf'],synthetic_legacy_walking_migration=True,exact_party_box_starter_persistence=True,actual_morty_loss_to_violet_center=True),indent=2)+'\n')
print('Actual approved practice loss -> Violet Center correct nurse landing/healing: PASS',flush=True)
