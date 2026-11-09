#!/usr/bin/env python3
"""Normal old-save Continue then actual controller tours. No map/warp RAM writes."""
import argparse,ctypes as C,hashlib,json,struct,subprocess,shutil
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--save',type=Path,required=True);p.add_argument('--library',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--cluster');p.add_argument('--resume',type=Path);args=p.parse_args();args.output.mkdir(parents=True,exist_ok=True)
lib=C.CDLL(str(args.library.resolve()))
for fn,types in [('emu_init',[C.c_char_p]),('emu_frames',[C.c_int,C.c_int]),('emu_read',[C.c_uint,C.c_int]),('emu_write',[C.c_uint,C.c_uint,C.c_int]),('emu_save',[C.c_char_p,C.c_int]),('emu_state',[C.c_char_p,C.c_int]),('emu_image',[C.c_char_p])]:getattr(lib,fn).argtypes=types
lib.emu_read.restype=C.c_uint
syms={}
for line in subprocess.check_output(['arm-none-eabi-nm','-an',str(R/'pokeemerald.elf')],text=True).splitlines():
 a=line.split()
 if len(a)==3:
  try:syms[a[2]]=int(a[0],16)
  except ValueError:pass
assert lib.emu_init(str(R/'pokeemerald.gba').encode())
def read(a,w=4):return lib.emu_read(syms.get(a,a),w)
def write(a,v,w=4):lib.emu_write(syms.get(a,a),v,w)
def frames(n=60,k=0):lib.emu_frames(k,n)
def key(k):frames(1,k);frames(20)
def sb():return read('gSaveBlock1Ptr')
def pos():return read(sb(),2),read(sb()+2,2)
names=json.loads((R/'data/maps/map_groups.json').read_text())['gMapGroup_CrossroadsOlivine'];maps={n:json.loads((R/f'data/maps/{n}/map.json').read_text()) for n in names};ids={m['id']:n for n,m in maps.items()};layouts={l['id']:l for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
size={n:(layouts[m['layout']]['width'],layouts[m['layout']]['height']) for n,m in maps.items()};raw={n:struct.unpack('<'+str(size[n][0]*size[n][1])+'H',(R/layouts[m['layout']]['blockdata_filepath']).read_bytes()) for n,m in maps.items()}
def current():
 assert read(sb()+4,1)==75,('Left Johto',read(sb()+4,1))
 return names[read(sb()+5,1)]
def close():
 for _ in range(18):
  if not read('sLockFieldControls',1):return
  key(1);frames(90)
 assert not read('sLockFieldControls',1)
if args.resume:
 assert args.resume.with_suffix('.sha256').read_text().strip()==hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest()
 assert lib.emu_state(str(args.resume).encode(),1)
else:
 assert lib.emu_save(str(args.save.resolve()).encode(),1)
 frames(4500);assert read(syms['gMain']+4)==syms['CB2_BlackLedgerTitle']|1
 key(8);frames(180);key(1);frames(300);assert read(syms['gMain']+4)==syms['CB2_Overworld']|1
 print('Normal old battery-save Continue:',current(),pos(),'PASS',flush=True)
import sys
def failed(kind,error,trace):
 lib.emu_state(str(args.output/'failure.snapshot').encode(),0)
 (args.output/'failure.sha256').write_text(hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest())
 lib.emu_image(str(args.output/'failure.png').encode())
 sys.__excepthook__(kind,error,trace)
sys.excepthook=failed
start=args.output/'start.snapshot';assert lib.emu_state(str(start).encode(),0);start.with_suffix('.sha256').write_text(hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest())
# Disable random encounters only in the test process, never the ROM.
write('sWildEncountersDisabled',1,1)
choice=read(sb()+0x1590,2);partycount=read(read('gPlayerPartyCountPtr'),1)
def safe(n,p):
 x,y=p;w,h=size[n]
 return 0<=x<w and 0<=y<h and raw[n][y*w+x]&0xc00==0 and raw[n][y*w+x]>>12==3 and not any((o['x'],o['y'])==p for o in maps[n]['object_events'])
def path(n,target):
 start=pos();blocked={(e['x'],e['y']) for e in maps[n]['warp_events']} - {start,target};q=deque([start]);prev={start:None}
 while q:
  x,y=q.popleft()
  if (x,y)==target:break
  for v in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
   if v not in prev and v not in blocked and safe(n,v):prev[v]=(x,y);q.append(v)
 if target not in prev:return None
 route=[];v=target
 while prev[v] is not None:route.append(v);v=prev[v]
 return list(reversed(route))
def walk(target):
 n=current();route=path(n,target);assert route is not None,(n,pos(),'No foot path',target)
 for to in route:
  old=pos();k=16 if to[0]>old[0] else 32 if to[0]<old[0] else 128 if to[1]>old[1] else 64
  frames(16,k);frames(20)
  if pos()==old:frames(16,k);frames(20)
  assert current()==n and pos()==to,(n,old,to,current(),pos())
def warp(index):
 n=current();e=maps[n]['warp_events'][index];x,y=e['x'],e['y'];w,h=size[n]
 approaches=[((x,y+1),64),((x-1,y),16),((x+1,y),32),((x,y-1),128)]
 if y==h-1:approaches=[((x,y-1),128)]+approaches[:-1]
 for target,k in approaches:
  if path(n,target) is not None:walk(target);break
 else:raise AssertionError((n,'No warp approach',e,pos()))
 for _ in range(3):
  frames(16,k);frames(180)
  if current()!=n:break
 assert current()==ids[e['dest_map']],('Wrong warp',n,index,current(),pos())
 return n,current()
def border(c):
 n=current();dst=ids[c['map']];w,h=size[n];dw,dh=size[dst];d=c['direction'];candidates=[]
 for t in range(w if d in ['up','down'] else h):
  old=(t,0) if d=='up' else (t,h-1) if d=='down' else (0,t) if d=='left' else (w-1,t)
  new=(t-c['offset'],dh-1) if d=='up' else (t-c['offset'],0) if d=='down' else (dw-1,t-c['offset']) if d=='left' else (0,t-c['offset'])
  route=path(n,old)
  if route is not None and safe(dst,new):candidates.append((len(route),old,new))
 assert candidates,(n,pos(),'No crossing',c)
 _,old,new=min(candidates);walk(old);k={'up':64,'down':128,'left':32,'right':16}[d];frames(16,k);frames(180)
 assert current()==dst,('Wrong border',n,c,current(),pos())
 return n,current()
visited=set();transitions=[]
def go(dst):
 for _ in range(60):
  cur=current()
  if cur==dst:return
  q=deque([cur]);prev={cur:None};edges={}
  while q:
   n=q.popleft()
   if n==dst:break
   for kind,e in [('border',c) for c in maps[n]['connections'] or []]+[('warp',i) for i in range(len(maps[n]['warp_events']))]:
    other=ids[e['map']] if kind=='border' else ids[maps[n]['warp_events'][e]['dest_map']]
    if other not in prev:prev[other]=n;edges[other]=(kind,e);q.append(other)
  assert dst in prev,('No map route',cur,dst)
  v=dst
  while prev[v]!=cur:v=prev[v]
  kind,e=edges[v];a,b=border(e) if kind=='border' else warp(e);transitions.append([a,b,kind]);visited.add(b)
 raise AssertionError(('Too many transitions',dst))
plans=json.loads((R/'crossroads/johto/manifest.json').read_text())['planned'];targets=[p['name'] for p in plans if p['name'] in names and (not args.cluster or p['cluster']==args.cluster)]
for n in targets:
 go(n);visited.add(n)
 assert lib.emu_image(str(args.output/f'{n}.png').encode())
 if 'PokemonCenter_1F' in n:
  walk((7,4));write(read('gPlayerPartyPtr')+86,1,2);frames(1,64);frames(20);key(1);frames(180)
  for _ in range(8):key(1);frames(180)
  for _ in range(5):key(2);frames(60)
  assert read(read('gPlayerPartyPtr')+86,2)==read(read('gPlayerPartyPtr')+88,2)>0
  assert read(sb()+0x1c,1)==75
  print('Nurse healing/local respawn:',n,'PASS',flush=True)
 assert read(sb()+0x1590,2)==choice and read(read('gPlayerPartyCountPtr'),1)==partycount
 print('Controller visit:',n,pos(),'PASS',flush=True)
go('OlivineCity')
end=args.output/'finished.snapshot';lib.emu_state(str(end).encode(),0);end.with_suffix('.sha256').write_text(hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest())
(args.output/'coverage.json').write_text(json.dumps(dict(visited=sorted(visited),targets=targets,transitions=transitions),indent=2)+'\n')
print('Actual controller visits/return, healing and retained starter/party: PASS',len(targets),'new maps',len(transitions),'transitions',flush=True)
