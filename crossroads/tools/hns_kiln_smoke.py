#!/usr/bin/env python3
"""Normal-controller donor-room test, using a copied QA10 in-room battery save.

Requires source map files, ROM and ELF from the same build. Real native mGBA
movement, menus and screenshots; the shared tour uses a RAM-only encounter
suppression and normal Survey desk access. No save data/position teleport writes.
This is gameplay evidence, not HGSS visual or owner acceptance.
"""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
from PIL import Image

R = Path(__file__).resolve().parents[2]
p = argparse.ArgumentParser()
p.add_argument('--save', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--library', type=Path, default=Path('/tmp/johto-bridge.so'))
p.add_argument('--rom-sha256', required=True)
p.add_argument('--map', required=True, help='Added kiln map name in map_groups.json')
a = p.parse_args()
out = a.output.resolve()
out.mkdir(parents=True, exist_ok=True)
sha = lambda data: hashlib.sha256(data).hexdigest()
source_save_hash = sha(a.save.read_bytes())
assert sha((R / 'pokeemerald.gba').read_bytes()) == a.rom_sha256
trial = out / 'input-copy.sav'
assert a.save.resolve() != trial
shutil.copyfile(a.save, trial)
sys.path.insert(0, str(R / 'crossroads/tools'))
sys.argv = ['johto_network_smoke.py', '--save', str(trial), '--library', str(a.library), '--output', str(out / 'tour'), '--targets', '']
d = runpy.run_path(str(R / 'crossroads/tools/johto_network_smoke.py'))
go, walk, warp, read, frames, key, current, pos, close, lib, syms, sb = [d[n] for n in ('go','walk','warp','read','frames','key','current','pos','close','lib','syms','sb')]
assert a.map in d['maps']
# The tour stores the real post-Continue snapshot before enabling its Survey
# fixture. Restore it to verify the genuine prior-version in-room save and exit.
assert lib.emu_state(str(out / 'tour/start.snapshot').encode(), 1)
assert current() == 'AzaleaTown_Workshop' and pos() == (6,8), (current(),pos())
records = []

def image(label):
    frames(40)
    dest = out / (label + '.png')
    assert lib.emu_image(str(dest).encode())
    im = Image.open(dest).convert('RGB')
    assert im.size == (240,160) and (255,0,255) not in im.getdata(), label
    return dest

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

def record_clip(label, action):
    # Capture native frames while controller movement/transition is happening.
    # This records actual game output, not a reconstruction from map data.
    g=warp.__globals__; old=g['frames']; folder=out/(label+'-frames')
    folder.mkdir(exist_ok=True); count=[0]
    def capture(n=60,k=0):
        while n:
            step=min(n,4);old(step,k);n-=step
            assert lib.emu_image(str(folder/f'{count[0]:04d}.png').encode())
            count[0]+=1
    g['frames']=capture
    try:action()
    finally:g['frames']=old
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(out/(label+'.mp4'))],check=True)

def memory(address, size):
    return bytes(read(address+i,1) for i in range(size))

def payload():
    count = read(read('gPlayerPartyCountPtr'),1)
    enc=read(read('gSaveBlock2Ptr')+0xac)
    inventory=dict(money=read(sb()+0x490)^enc,coins=read(sb()+0x494,2)^(enc&65535),registered=read(sb()+0x496,2),pc=memory(sb()+0x498,0xc8).hex(),bag=[(read(sb()+0x560+i*4,2),read(sb()+0x562+i*4,2)^(enc&65535)) for i in range(186)])
    return dict(starter=read(sb()+0x1590,2), count=count,
                party=sha(memory(read('gPlayerPartyPtr'),count*100)),
                boxes=sha(memory(read('gPokemonStoragePtr'),0x83d0)),
                flags=sha(memory(sb()+0x1270,300)),
                decoded_inventory=sha(json.dumps(inventory,sort_keys=True).encode()))

image('qa10-old-save-continued'); assert not read('sLockFieldControls',1)
initial=payload(); warp(0); assert current() == 'AzaleaTown'
records.append(dict(case='old-save-normal-continue-and-workshop-exit', result='PASS'))
city = d['maps']['AzaleaTown']
entry_indices=[i for i,e in enumerate(city['warp_events']) if d['ids'].get(e['dest_map'])==a.map]
assert entry_indices, ('No actual exterior entry', a.map)
back=[i for i,e in enumerate(d['maps'][a.map]['warp_events']) if d['ids'].get(e['dest_map'])=='AzaleaTown']
assert back, ('No actual exit back to city',a.map)
for entry in entry_indices:
    for leave in back:
        go('AzaleaTown',entry); record_clip(f'entry-{entry}',lambda:warp(entry)); assert current()==a.map
        view=image(f'kiln-entry-{entry}-exit-{leave}');visibility=joe_visible(view)
        go(a.map,leave); record_clip(f'exit-{leave}',lambda:warp(leave)); assert current()=='AzaleaTown'
        arrival=pos(); adjacent=[]
        for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
            target=(arrival[0]+dx,arrival[1]+dy)
            if target not in d['active_warps']('AzaleaTown') and d['path']('AzaleaTown',target) is not None:
                adjacent.append(target)
        assert adjacent, ('No safe walking-away path from arrival',arrival)
        walk(adjacent[0])
        records.append(dict(case='actual-entry-and-return', exterior_warp=entry,
                            interior_warp=leave, arrival=arrival,
                            walked_away_to=pos(), joe_visibility=visibility, result='PASS'))
# Verify the ROM actually embeds the authored secondary palettes and the
# renderer has loaded their nontransparent colors. This catches a stale
# generated .gbapal even when source-only image validation passes.
for bank in range(8,13):
    lines=(R / f'data/tilesets/secondary/bl_gym_azalea/palettes/{bank:02}.pal').read_text().splitlines()
    assert lines[:3]==['JASC-PAL','0100','16']
    rgb=[tuple(map(int,line.split())) for line in lines[3:19]]
    expected=[(r>>3)|((g>>3)<<5)|((b>>3)<<10) for r,g,b in rgb]
    rom=[read(syms['gTilesetPalettes_BlGymAzaleaSecondary']+bank*32+i*2,2) for i in range(16)]
    loaded=[read(syms['gPlttBufferUnfaded']+bank*32+i*2,2) for i in range(16)]
    assert rom==expected,('Compiled Azalea palette differs from authored source',bank,rom,expected)
    assert loaded[1:]==expected[1:],('Runtime Azalea palette differs from authored source',bank,loaded,expected)
    records.append(dict(case='azalea-rom-and-runtime-palette',bank=bank,colors=len(expected),result='PASS'))
# Enter again, enumerate the actual room's public component, and physically
# push every reachable collision-marked neighbor from every accessible side.
go('AzaleaTown',entry_indices[0]); warp(entry_indices[0]); assert current()==a.map
walk((5,5)); image('kiln-centered-interior'); records.append(dict(case='centered-native-interior-view',position=pos(),result='captured; visual acceptance pending'))
w,h=d['size'][a.map]; raw=d['raw'][a.map]; active=d['active_warps'](a.map)
q=deque([pos()]); seen={pos()}
while q:
    x,y=q.popleft()
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
        v=d['next_position'](x,y,dx,dy,lambda xx,yy:d['behavior'](a.map,xx,yy))
        if v is not None and v not in seen and v not in active and d['safe'](a.map,v):
            seen.add(v);q.append(v)
targets=[]
for x,y in seen:
    if (x,y) in active: continue
    for dx,dy,k in ((1,0,16),(-1,0,32),(0,1,128),(0,-1,64)):
        xx,yy=x+dx,y+dy
        if 0<=xx<w and 0<=yy<h and raw[yy*w+xx]&0xc00 and (xx,yy) not in active:
            targets.append(((x,y),(xx,yy),k))
assert targets, 'No physically accessible collision checks identified'
while targets:
    i=min(range(len(targets)),key=lambda j:abs(targets[j][0][0]-pos()[0])+abs(targets[j][0][1]-pos()[1]))
    approach,target,k=targets.pop(i); walk(approach); old=pos();frames(32,k);frames(30)
    assert current()==a.map and pos()==old, ('Walked through blocked cell',approach,target,current(),pos())
    records.append(dict(case='collision-bump',approach=approach,target=target,result='PASS'))
image('kiln-collision-checked')
# Exercise each reachable static actor/sign through A and verify control returns.
for group in ('object_events','bg_events'):
    for index,event in enumerate(d['maps'][a.map][group]):
        x,y=event['x'],event['y']; found=None
        for dx,dy,k in ((0,1,64),(-1,0,16),(1,0,32),(0,-1,128)):
            p=(x+dx,y+dy)
            if p not in active and d['path'](a.map,p) is not None:
                found=(p,k);break
        assert found is not None, ('Unreachable interaction',group,index,event)
        walk(found[0]);frames(1,found[1]);frames(20);key(1);frames(140)
        assert read('sLockFieldControls',1), ('Interaction did not open',group,index,event)
        image(f'kiln-{group}-{index}');close();assert current()==a.map and pos()==found[0]
        records.append(dict(case='interaction',group=group,index=index,result='PASS'))
# Native Save menu and cold title/Continue; exact party, flags and boxes at the
# moment of saving must survive. Source input battery remains untouched.
before=(current(),pos()); data=payload();key(8);frames(90)
for _ in range(12):
    cursor=read('sStartMenuCursorPos',1)
    if read(syms['sCurrentStartMenuActions']+cursor,1)==5:break
    key(128)
else:raise AssertionError('Native Save menu action missing')
key(1);frames(180)
for _ in range(8):key(1);frames(180)
for _ in range(3):key(2);frames(120)
assert read(syms['gMain']+4)==syms['CB2_Overworld']|1
battery=out/'kiln-normal-save.sav';assert lib.emu_save(str(battery).encode(),0)
assert lib.emu_init(str(R/'pokeemerald.gba').encode()) and lib.emu_save(str(battery).encode(),1)
frames(4500);assert read(syms['gMain']+4)==syms['CB2_BlackLedgerTitle']|1
key(8);frames(180);key(1);frames(300)
assert read(syms['gMain']+4)==syms['CB2_Overworld']|1 and (current(),pos())==before
assert payload()==data and not read('sLockFieldControls',1)
image('kiln-cold-continue'); records.append(dict(case='kiln-normal-save-cold-continue',position=pos(),result='PASS'))
warp(back[0]); assert current()=='AzaleaTown'; image('kiln-return-to-azalea')
assert sha(a.save.read_bytes())==source_save_hash and sha((R/'pokeemerald.gba').read_bytes())==a.rom_sha256
result=dict(rom_sha256=a.rom_sha256, map=a.map, source_battery_sha256=source_save_hash,
            source_battery_unchanged=True,old_save_initial=initial,
            actual_controller_bump_count=sum(x['case']=='collision-bump' for x in records),
            note='Actual controller movement; RAM-only encounter suppression and Survey desk fixture; visual owner acceptance remains pending.',records=records)
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print('Old QA10 Continue, actual kiln entry/exit, collision, interactions, Save/Continue: PASS',result['actual_controller_bump_count'],'collision approaches',flush=True)
