#!/usr/bin/env python3
"""Real QA10 battery -> candidate Route 33 controller checks, never teleport.

Run inside a frozen candidate checkout with matching pokeemerald.gba/.elf and
map files; outputs contain private copied saves/snapshots so never commit them.
Uses disclosed RAM-only encounter suppression; survey desk is used normally.
Static collision candidates are sampled and do not establish visual acceptance.
"""
import argparse,hashlib,json,runpy,shutil,subprocess,sys
from collections import deque
from pathlib import Path
from PIL import Image
R=Path.cwd()
p=argparse.ArgumentParser();p.add_argument('--save',type=Path,required=True);p.add_argument('--baseline',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--library',type=Path,default=Path('/tmp/johto-bridge.so'));p.add_argument('--rom-sha256',required=True);a=p.parse_args()
out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
sha=lambda v:hashlib.sha256(v).hexdigest(); source=sha(a.save.read_bytes());assert sha((R/'pokeemerald.gba').read_bytes())==a.rom_sha256
base=json.loads(a.baseline.read_text());assert base['source_battery_sha256']==source and base['continued_position']==[22,7]
copy=out/'input-copy.sav';assert copy!=a.save.resolve();shutil.copyfile(a.save,copy)
sys.path.insert(0,str(R/'crossroads/tools'));sys.argv=['johto_network_smoke.py','--save',str(copy),'--library',str(a.library),'--output',str(out/'tour'),'--targets','']
d=runpy.run_path(str(R/'crossroads/tools/johto_network_smoke.py'))
go,walk,warp,border,read,write,frames,key,current,pos,close,lib,syms,sb=[d[n] for n in ('go','walk','warp','border','read','write','frames','key','current','pos','close','lib','syms','sb')]
assert lib.emu_state(str(out/'tour/start.snapshot').encode(),1);assert current()=='JohtoRoute33'
assert pos()!=(22,7) and d['safe']('JohtoRoute33',pos()),('Old position not moved to open terrain',pos())
assert not read('sLockFieldControls',1)
records=[]
def memory(x,n):return bytes(read(x+i,1) for i in range(n))
def payload():
 count=read(read('gPlayerPartyCountPtr'),1); enc=read(read('gSaveBlock2Ptr')+0xac)
 inventory=dict(money=read(sb()+0x490)^enc,coins=read(sb()+0x494,2)^(enc&65535),registered=read(sb()+0x496,2),pc=memory(sb()+0x498,0xc8).hex(),bag=[(read(sb()+0x560+i*4,2),read(sb()+0x562+i*4,2)^(enc&65535)) for i in range(186)])
 return dict(starter=read(sb()+0x1590,2),count=count,party=sha(memory(read('gPlayerPartyPtr'),count*100)),boxes=sha(memory(read('gPokemonStoragePtr'),0x83d0)),flags=sha(memory(sb()+0x1270,300)),decoded_inventory=sha(json.dumps(inventory,sort_keys=True).encode()))
assert payload()==base['payload'],('QA10 save changed',payload(),base['payload'])
def image(label):
 frames(40);f=out/(label+'.png');assert lib.emu_image(str(f).encode());im=Image.open(f).convert('RGB');assert im.size==(240,160) and (255,0,255) not in im.getdata();return f
def joe_visible(frame_path, allow_short_grass=False):
    # Compare the actual normal player OAM sprite's nontransparent pixels with
    # the native framebuffer at an open floor arrival. This catches accidental
    # floor foreground layers while respecting intended wall/roof overhangs.
    frame=Image.open(frame_path).convert('RGB')
    sprite=syms['gSprites']+read(syms['gPlayerAvatar']+4,1)*68
    tile=read(sprite+4,2)&1023; palette=read(sprite+4,2)>>12; matches=[]
    for i in range(128):
        addr=0x07000000+i*8;v0,v1,v2=read(addr,2),read(addr+2,2),read(addr+4,2)
        if (v2&1023)==tile and v2>>12==palette and not v0&0x300:matches.append((v0,v1,v2))
    assert len(matches)==1,('Normal player OAM entry missing or ambiguous',matches)
    v0,v1,v2=matches[0];assert not v0&0x2c00
    dims=[[(8,8),(16,16),(32,32),(64,64)],[(16,8),(32,8),(32,16),(64,32)],[(8,16),(8,32),(16,32),(32,64)]]
    width,height=dims[v0>>14][v1>>14];x0,y0=v1&511,v0&255
    x0=x0-512 if x0>=256 else x0;y0=y0-256 if y0>=160 else y0
    assert 0<=x0<=240-width and 0<=y0<=160-height
    colors=[]
    for i in range(16):
        v=read(0x05000200+palette*32+i*2,2)
        colors.append(tuple(((v>>shift)&31)<<3|((v>>shift)&31)>>2 for shift in (0,5,10)))
    stride=width//8 if read(0x04000000,2)&64 else 32;expected=visible=0; mismatches=[]
    for y in range(height):
        for x in range(width):
            X=width-1-x if v1&0x1000 else x;Y=height-1-y if v1&0x2000 else y
            index=tile+(Y//8)*stride+X//8;b=read(0x06010000+index*32+(Y%8)*4+(X%8)//2,1)
            color=(b>>(4*(X%2)))&15
            if color:
                expected+=1;actual=frame.getpixel((x0+x,y0+y));visible+=int(actual==colors[color])
                if actual!=colors[color]:mismatches.append((x,y))
    assert expected>0
    if allow_short_grass:
        assert d['behavior']('JohtoRoute33',*pos())==7,('Not SHORT_GRASS',pos())
        assert len(mismatches)<=10 and all(y>=height-2 for x,y in mismatches),('Unexpected grass occlusion',mismatches,expected)
    else:assert visible==expected,('Joe occluded on ordinary floor',mismatches,expected)
    return dict(opaque_expected=expected,opaque_visible=visible,masked_pixels=mismatches,short_grass=allow_short_grass)

frame=image('old-save-continued-short-grass')
visibility=joe_visible(frame,allow_short_grass=True)
records.append(dict(case='genuine-QA10-continue',old_position=[22,7],new_position=pos(),joe_visibility=visibility,exact_party_boxes_flags_starter_decoded_inventory=True,result='PASS'))
write('sWildEncountersDisabled',1,1) # disclosed process-only test fixture
# On actual ordinary floor, require every opaque pixel visible; grass's allowed
# masking above is restricted to the last 2 sprite rows and max 10 pixels.
w,h=d['size']['JohtoRoute33'];options=[]
for y in range(2,h-2):
 for x in range(2,w-2):
  q=(x,y)
  if d['safe']('JohtoRoute33',q) and d['behavior']('JohtoRoute33',x,y)==0 and q not in d['active_warps']('JohtoRoute33') and d['path']('JohtoRoute33',q) is not None:
   options.append(q)
assert options,'No reachable non-grass ground for visibility control'
target=min(options,key=lambda q:abs(q[0]-pos()[0])+abs(q[1]-pos()[1]));walk(target)
plain_visibility=joe_visible(image('ordinary-ground-joe-visibility'))
records.append(dict(case='ordinary-ground-joe-visibility',position=pos(),visibility=plain_visibility,result='PASS'))
def clip(label,fn):
 g=warp.__globals__;old=g['frames'];folder=out/(label+'-frames');folder.mkdir(exist_ok=True);number=[0]
 def capture(n=60,k=0):
  while n:
   step=min(n,4);old(step,k);n-=step;assert lib.emu_image(str(folder/f'{number[0]:04d}.png').encode());number[0]+=1
 g['frames']=capture
 try:fn()
 finally:g['frames']=old
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(out/(label+'.mp4'))],check=True)
def connection(src,dst):
 return next(c for c in d['maps'][src]['connections'] or [] if d['ids'][c['map']]==dst)
# Test the real border in both directions; no location or warp writes.
go('JohtoRoute33');origin=pos();clip('route-to-azalea',lambda:border(connection('JohtoRoute33','AzaleaTown')));assert current()=='AzaleaTown';image('azalea-border-arrival')
clip('azalea-to-route',lambda:border(connection('AzaleaTown','JohtoRoute33')));assert current()=='JohtoRoute33';image('route-border-arrival')
records.append(dict(case='actual-reciprocal-border',origin=origin,route_return=pos(),result='PASS'))
# The unchanged cave warp indices are part of the save and connection contract.
go('JohtoRoute33',0);clip('route-to-cave',lambda:warp(0));assert current()=='UnionCave_1F';image('cave-arrival')
clip('cave-to-route',lambda:warp(2));assert current()=='JohtoRoute33';image('route-cave-return')
records.append(dict(case='actual-reciprocal-cave',result='PASS'))
# Traverse its actual contiguous floor component using decoded tile behavior,
# then physically push representative collision-marked targets from each
# selected accessible side. Sample is explicitly not full-region collision QA.
w,h=d['size']['JohtoRoute33'];raw=d['raw']['JohtoRoute33'];active=d['active_warps']('JohtoRoute33');queue=deque([pos()]);seen={pos()}
while queue:
 x,y=queue.popleft()
 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
  v=d['next_position'](x,y,dx,dy,lambda xx,yy:d['behavior']('JohtoRoute33',xx,yy))
  if v is not None and v not in seen and v not in active and d['safe']('JohtoRoute33',v):seen.add(v);queue.append(v)
targets=[];chosen=set();excluded=[]
for x,y in sorted(seen):
 if (x,y) in active:continue
 for dx,dy,k in ((1,0,16),(-1,0,32),(0,1,128),(0,-1,64)):
  xx,yy=x+dx,y+dy
  if 0<=xx<w and 0<=yy<h and (xx,yy) not in active and raw[yy*w+xx]&0xc00:
   signature=(raw[yy*w+xx]&1023,k)
   if signature not in chosen:
    chosen.add(signature)
    modeled=d['next_position'](x,y,dx,dy,lambda ax,ay:d['behavior']('JohtoRoute33',ax,ay))
    if modeled is not None and modeled!=(xx,yy) and (modeled in active or not d['safe']('JohtoRoute33',modeled)):
     excluded.append(dict(approach=[x,y],target=[xx,yy],behavior=d['behavior']('JohtoRoute33',xx,yy),reason='Modeled jump landing is unsafe or active warp; not executed'))
    else:targets.append(((x,y),(xx,yy),k,modeled))
assert targets;targets=targets[:64];sample_count=len(targets)
while targets:
 i=min(range(len(targets)),key=lambda j:abs(targets[j][0][0]-pos()[0])+abs(targets[j][0][1]-pos()[1]));approach,target,k,modeled=targets.pop(i)
 walk(approach);old=pos();frames(16,k);frames(30)
 if modeled is not None and modeled!=target:
  assert current()=='JohtoRoute33' and pos()==modeled,('Expected directional jump failed',approach,target,modeled,current(),pos())
  records.append(dict(case='directional-ledge-jump',approach=approach,target=target,behavior=d['behavior']('JohtoRoute33',*target),expected_landing=modeled,result='PASS'))
 else:
  assert current()=='JohtoRoute33' and pos()==old,('Pass-through solid tile',approach,target,current(),pos())
  records.append(dict(case='sampled-collision-bump',approach=approach,target=target,result='PASS'))
image('sampled-collision')
# Actual A on every preserved NPC/sign. Neither scripts nor display text are
# imported from donor; no scripted rewards are granted.
for group in ('object_events','bg_events'):
 for i,event in enumerate(d['maps']['JohtoRoute33'][group]):
  x,y=event['x'],event['y'];found=None
  for dx,dy,k in ((0,1,64),(-1,0,16),(1,0,32),(0,-1,128)):
   q=(x+dx,y+dy)
   if q not in active and d['path']('JohtoRoute33',q) is not None:found=(q,k);break
  assert found is not None,('No physical interaction approach',group,i,event)
  walk(found[0]);frames(1,found[1]);frames(20);key(1);frames(140);assert read('sLockFieldControls',1),('Interaction did not open',group,i)
  image(f'{group}-{i}');close();assert current()=='JohtoRoute33' and pos()==found[0]
  records.append(dict(case='interaction',group=group,index=i,result='PASS'))
# Real normal save and cold Continue on candidate bytes, compare decrypted data.
before=(current(),pos());saved=payload();key(8);frames(90)
for _ in range(12):
 cursor=read('sStartMenuCursorPos',1)
 if read(syms['sCurrentStartMenuActions']+cursor,1)==5:break
 key(128)
else:raise AssertionError('Native Save action absent')
key(1);frames(180)
for _ in range(8):key(1);frames(180)
for _ in range(3):key(2);frames(120)
assert read(syms['gMain']+4)==syms['CB2_Overworld']|1
battery=out/'route33-normal-save.sav';assert lib.emu_save(str(battery).encode(),0)
assert lib.emu_init(str(R/'pokeemerald.gba').encode()) and lib.emu_save(str(battery).encode(),1)
frames(4500);assert read(syms['gMain']+4)==syms['CB2_BlackLedgerTitle']|1
key(8);frames(180);key(1);frames(300)
assert read(syms['gMain']+4)==syms['CB2_Overworld']|1 and (current(),pos())==before and payload()==saved and not read('sLockFieldControls',1)
image('route-save-cold-continue');records.append(dict(case='normal-save-cold-continue',position=pos(),exact_party_boxes_flags_starter_decoded_inventory=True,result='PASS'))
assert sha(a.save.read_bytes())==source and sha((R/'pokeemerald.gba').read_bytes())==a.rom_sha256
(out/'results.json').write_text(json.dumps(dict(rom_sha256=a.rom_sha256,source_battery_unchanged=True,method='Normal controller and genuine old battery; disclosed RAM-only encounter suppression; no location/warp writes.',collision_or_ledge_approaches=sample_count,excluded_unsafe_ledge_jumps=excluded,records=records),indent=2)+'\n')
print('Route 33 actual old-save, both-way borders/cave, sampled collision, interactions and Save/Continue PASS',sample_count,'bumps',flush=True)
