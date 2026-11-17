#!/usr/bin/env python3
"""Check the donor-to-Emerald kiln projection, not emulator or HGSS fidelity."""
from pathlib import Path
from collections import deque
import json,struct
from PIL import Image
R=Path(__file__).resolve().parents[2]
S=R/'crossroads/donor/hns-charcoal-kiln/data'
D=R/'data/tilesets/primary/hns_charcoal_kiln'
def words(path):
    b=path.read_bytes();return list(struct.unpack('<'+str(len(b)//2)+'H',b))
donor=words(S/'layouts/AzaleaTown_House1_hns/map.bin')
out=words(R/'data/layouts/AzaleaTown_CharcoalKiln/map.bin')
oldmeta=words(S/'tilesets/primary/johto_building_hns/metatiles.bin')+words(S/'tilesets/secondary/barn_hns/metatiles.bin')
oldattr=words(S/'tilesets/primary/johto_building_hns/metatile_attributes.bin')+words(S/'tilesets/secondary/barn_hns/metatile_attributes.bin')
newmeta=words(D/'metatiles.bin');newattr=words(D/'metatile_attributes.bin')
pics=[Image.open(S/'tilesets/primary/johto_building_hns/tiles.png'),Image.open(S/'tilesets/secondary/barn_hns/tiles.png')]
outpic=Image.open(D/'tiles.png')
def tile(im,i):
    x=(i%16)*8;y=(i//16)*8
    return im.crop((x,y,x+8,y+8)).tobytes()
def palette(path):
    lines=path.read_text().splitlines();assert lines[:3]==['JASC-PAL','0100','16'];return [tuple(map(int,x.split())) for x in lines[3:19]]
banks=[0,3,5,7,8]
for i,b in enumerate(banks):
    source=S/('tilesets/primary/johto_building_hns' if b<7 else 'tilesets/secondary/barn_hns')/f'palettes/{b:02}.pal'
    assert palette(source)==palette(D/f'palettes/{i:02}.pal')
assert len(donor)==len(out)==110
artcells={}
for y in range(3,9):
    for x in range(1,10):
        if ((x>=6 or y>=7) and not (7<=x<=9 and 2<=y<=4)
            and not (y==8 and x in (4,5,6))):artcells[x,y]='stone'
for x in range(1,6):artcells[x,6]='edge'
for x in (1,2):artcells[x,1]='shelf'
for x in (3,4,5):artcells[x,1]='bench'
for y in (0,1):artcells[8,y]='chimney'
art_order={pos:46+i for i,pos in enumerate(sorted(artcells,key=lambda p:(p[1],p[0])))}
artrefs={kind:list(range(116+i*4,120+i*4)) for i,kind in enumerate(('stone','edge','shelf','bench','chimney'))}
for i,(a,b) in enumerate(zip(donor,out)):
    x,y=i%11,i//11
    kiln=7<=x<=9 and 2<=y<=4
    if kiln:
        assert a&0xfc00 == 0x3000 and b&0xfc00 == 0x3400, ('kiln collision',i)
        assert b&1023 == 37+(y-2)*3+(x-7)
    elif (x,y) in artcells:
        assert a&0xfc00 == b&0xfc00 and b&1023 == art_order[x,y], ('adapted cell',i)
    else:
        assert a&0xfc00 == b&0xfc00, ('collision/elevation',i)
    old=a&1023;new=b&1023
    assert oldattr[old]==newattr[new], ('metatile behavior/layer',i)
    if kiln:
        overlay=newmeta[8*new+4:8*new+8]
        expected=[79+((y-2)*2+dy)*6+(x-7)*2+dx for dy in range(2) for dx in range(2)]
        assert overlay==expected and all(any(tile(outpic,j)) for j in overlay), ('kiln art',i)
    elif (x,y) in artcells:
        kind=artcells[x,y]
        if kind=='edge':assert newmeta[8*new+4:8*new+8]==artrefs[kind]
        else:assert newmeta[8*new:8*new+8]==artrefs[kind]+[115]*4
    count=4 if kiln or artcells.get((x,y))=='edge' else 0 if (x,y) in artcells else 8
    for a_ref,b_ref in zip(oldmeta[8*old:8*old+count],newmeta[8*new:8*new+count]):
        assert a_ref&0x0c00 == b_ref&0x0c00
        assert banks[b_ref>>12] == a_ref>>12
        aidx=a_ref&1023
        assert tile(pics[aidx>=640],aidx-(640 if aidx>=640 else 0))==tile(outpic,b_ref&1023), ('8x8 pixel',i,aidx)
warp=out[8*11+5]; assert warp&0x0c00==0 and warp>>12==3 and newattr[warp&1023]&255==0x65
# Conservative walkable reachability from the exit, no implicit claim about event collisions.
q=deque([(5,8)]);seen={(5,8)}
while q:
    x,y=q.popleft()
    for u,v in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
        if 0<=u<11 and 0<=v<10 and (u,v) not in seen and out[v*11+u]&0x0c00==0 and out[v*11+u]>>12==3:
            seen.add((u,v));q.append((u,v))
assert len(seen)==51 and (2,4) in seen
m=json.loads((R/'data/maps/AzaleaTown_CharcoalKiln/map.json').read_text()); assert m['warp_events']==[dict(x=5,y=8,elevation=0,dest_map='MAP_AZALEA_TOWN',dest_warp_id='7')]
assert m['object_events'][0]['script']=='AzaleaTown_CharcoalKiln_EventScript_Worker'
print(f'PASS: {110-9-len(artcells)} donor cells mapped exactly; {len(artcells)} visual-only adaptations; nine blocked kiln cells; 51-tile static walkable component.')
print('Not a visual/HGSS comparison, actual door test, or emulator playtest.')
