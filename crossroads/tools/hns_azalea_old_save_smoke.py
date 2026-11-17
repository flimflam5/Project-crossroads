#!/usr/bin/env python3
"""Cold-Continue an actual prior QA10 battery saved in the new kiln footprint.

Baseline and candidate use the same copied .sav; never writes source save,
coordinates or flags. Verifies party, boxes, flags, bag and starter and uses
controller movement to escape the resulting position. Candidate must have its
own matching ROM, ELF and map data, not an old emulator state.
"""
import argparse
from collections import deque
import ctypes as C
import hashlib
import json
from pathlib import Path
import struct
import subprocess
from PIL import Image
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--save',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--library',type=Path,default=Path('/tmp/johto-bridge.so'));p.add_argument('--rom-sha256',required=True);p.add_argument('--baseline',type=Path,help='baseline JSON from the QA10 ROM, required for candidate');p.add_argument('--payload-only',action='store_true',help='Capture initial payload only; no walking test');p.add_argument('--expected-position',default='20,32');p.add_argument('--require-original-position',action='store_true');a=p.parse_args()
a.output.mkdir(parents=True,exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest();source=sha(a.save.read_bytes());assert sha((R/'pokeemerald.gba').read_bytes())==a.rom_sha256
lib=C.CDLL(str(a.library.resolve()))
for fn,args in [('emu_init',[C.c_char_p]),('emu_frames',[C.c_int,C.c_int]),('emu_read',[C.c_uint,C.c_int]),('emu_save',[C.c_char_p,C.c_int]),('emu_image',[C.c_char_p])]:getattr(lib,fn).argtypes=args
lib.emu_read.restype=C.c_uint
syms={}
for line in subprocess.check_output(['arm-none-eabi-nm','-an',str(R/'pokeemerald.elf')],text=True).splitlines():
    f=line.split()
    if len(f)==3:
        try:syms[f[2]]=int(f[0],16)
        except ValueError:pass
read=lambda x,n=4:lib.emu_read(syms.get(x,x),n)
def frames(n,k=0):lib.emu_frames(k,n)
def key(k):frames(1,k);frames(20)
def memory(x,n):return bytes(read(x+i,1) for i in range(n))
assert lib.emu_init(str(R/'pokeemerald.gba').encode()) and lib.emu_save(str(a.save.resolve()).encode(),1)
frames(4500);assert read(syms['gMain']+4)==syms['CB2_BlackLedgerTitle']|1
key(8);frames(180);key(1);frames(300);assert read(syms['gMain']+4)==syms['CB2_Overworld']|1
sb=read('gSaveBlock1Ptr');loc=(read(sb+4,1),read(sb+5,1));position=(read(sb,2),read(sb+2,2))
groups=json.loads((R/'data/maps/map_groups.json').read_text());expected=(75,groups['gMapGroup_CrossroadsOlivine'].index('AzaleaTown'));assert loc==expected,(loc,expected)
count=read(read('gPlayerPartyCountPtr'),1)
enc=read(read('gSaveBlock2Ptr')+0xac)
inventory=dict(money=read(sb+0x490)^enc,coins=read(sb+0x494,2)^(enc&65535),registered=read(sb+0x496,2),pc=memory(sb+0x498,0xc8).hex(),bag=[(read(sb+0x560+i*4,2),read(sb+0x562+i*4,2)^(enc&65535)) for i in range(186)])
payload=dict(starter=read(sb+0x1590,2),count=count,party=sha(memory(read('gPlayerPartyPtr'),count*100)),boxes=sha(memory(read('gPokemonStoragePtr'),0x83d0)),flags=sha(memory(sb+0x1270,300)),decoded_inventory=sha(json.dumps(inventory,sort_keys=True).encode()))
if a.baseline:
    baseline=json.loads(a.baseline.read_text());assert baseline['source_battery_sha256']==source
    assert payload==baseline['payload'],('Old-save payload changed',payload,baseline['payload'])
    if a.require_original_position:assert list(position)==baseline['continued_position'],('Unchanged old position moved',position,baseline['continued_position'])
else:assert position==tuple(map(int,a.expected_position.split(','))),position
if a.payload_only:
    assert not a.baseline and sha(a.save.read_bytes())==source
    (a.output/'results.json').write_text(json.dumps(dict(source_battery_sha256=source,rom_sha256=a.rom_sha256,payload=payload,continued_position=position,method='Native cold battery Continue; payload only.'),indent=2)+'\n')
    print('QA10 baseline decoded payload captured',flush=True)
    raise SystemExit(0)
assert not read('sLockFieldControls',1)
def joe_visible(frame_path):
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
    stride=width//8 if read(0x04000000,2)&64 else 32;expected=visible=0
    for y in range(height):
        for x in range(width):
            X=width-1-x if v1&0x1000 else x;Y=height-1-y if v1&0x2000 else y
            index=tile+(Y//8)*stride+X//8;b=read(0x06010000+index*32+(Y%8)*4+(X%8)//2,1)
            color=(b>>(4*(X%2)))&15
            if color:
                expected+=1;visible+=int(frame.getpixel((x0+x,y0+y))==colors[color])
    assert expected>0 and visible==expected,('Joe occluded on open kiln arrival floor',visible,expected)
    return dict(opaque_expected=expected,opaque_visible=visible)

image=a.output/'continued.png';assert lib.emu_image(str(image).encode());im=Image.open(image).convert('RGB');assert im.size==(240,160) and (255,0,255) not in im.getdata()
visibility=joe_visible(image)
# Find a conservative route from the actual continued position out of the
# exterior art footprint. A saved player can start on a newly blocked tile; only
# destination cells are required to be open. Actual controller walking must
# still execute every step and may expose tile behavior or object collisions.
world=json.loads((R/'data/maps/AzaleaTown/map.json').read_text())
layouts=json.loads((R/'data/layouts/layouts.json').read_text())['layouts']
layout=next(x for x in layouts if x['id']==world['layout']);w,h=layout['width'],layout['height']
raw=struct.unpack('<'+str(w*h)+'H',(R/layout['blockdata_filepath']).read_bytes())
warps={(x['x'],x['y']) for x in world['warp_events']}
objects={(x['x'],x['y']) for x in world['object_events']}
footprint=lambda p:19<=p[0]<=22 and 30<=p[1]<=33
q=deque([position]);previous={position:None};goal=None
while q:
    x,y=q.popleft()
    if (x,y)!=position and not footprint((x,y)):
        goal=(x,y);break
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        v=(x+dx,y+dy)
        if not (0<=v[0]<w and 0<=v[1]<h) or v in previous or v in warps or v in objects:continue
        cell=raw[v[1]*w+v[0]]
        if cell&0xc00 or cell>>12!=3:continue
        previous[v]=(x,y);q.append(v)
assert goal is not None,('No static exit from old saved position',position)
route=[];v=goal
while previous[v] is not None:route.append(v);v=previous[v]
route.reverse()
for target in route:
    old=(read(sb,2),read(sb+2,2))
    k=16 if target[0]>old[0] else 32 if target[0]<old[0] else 128 if target[1]>old[1] else 64
    frames(16,k);frames(20)
    now=(read(sb,2),read(sb+2,2))
    if now==old:frames(16,k);frames(20);now=(read(sb,2),read(sb+2,2))
    assert (read(sb+4,1),read(sb+5,1))==loc and now==target,('Cannot walk to exit',old,target,now)
moved=(read(sb,2),read(sb+2,2));assert not footprint(moved)
assert lib.emu_image(str(a.output/'walk-away.png').encode())
assert sha(a.save.read_bytes())==source
result=dict(source_battery_sha256=source,rom_sha256=a.rom_sha256,continued_map='AzaleaTown',continued_position=position,walked_away_to=moved,payload=payload,joe_visibility=visibility,source_battery_unchanged=True,method='Native cold battery Continue plus actual controller walking to outside the new footprint.',result='PASS')
(a.output/'results.json').write_text(json.dumps(result,indent=2)+'\n');print('QA10 old-footprint Continue, payload and walk away: PASS',position,'->',moved,flush=True)
