#!/usr/bin/env python3
"""Static Route 33 prototype checks; not a substitute for emulator play."""
from pathlib import Path
from collections import deque
from PIL import Image
import json, struct, subprocess
R=Path(__file__).resolve().parents[2]
def words(p):
 b=p.read_bytes();return list(struct.unpack('<%dH'%(len(b)//2),b))
d=words(R/'crossroads/donor/hns-route33/data/layouts/Route33_hns/map.bin')
h=R/'crossroads/donor/hns_azalea_exterior/data/tilesets/primary/johto_south_hns'
c=R/'data/tilesets/secondary/bl_gym_azalea'; o=R/'data/tilesets/secondary/hns_route33'
new=words(R/'data/layouts/JohtoRoute33/map.bin');source=[d[(y+10)*44+x+3] for y in range(24) for x in range(32)]
old=words(R/'crossroads/donor/hns-route33/data/layouts/Route33_hns/black-ledger-baseline.bin')
meta=words(h/'metatiles.bin');attr=words(h/'metatile_attributes.bin');outmeta=words(o/'metatiles.bin');outattr=words(o/'metatile_attributes.bin');used=sorted({v&1023 for v in source});freemeta=[v for v in range(512,1024) if v!=514];mmap={v:freemeta[i] for i,v in enumerate(used)}
assert len(source)==len(new)==len(old)==768 and len(used)==55
signs={(13,15),(23,8)}
for i,(raw,val) in enumerate(zip(source,new)):
 x,y=i%32,i//32
 if x<7: assert val==old[i];continue
 if (x,y) in signs:assert val==0x3403;continue
 want=(raw&0xfc00)|mmap[raw&1023]
 if want>>12==0 and not want&0xc00:want|=0x400
 assert val==want,(x,y,hex(val),hex(want))
assert len(outattr)==512 and len(outmeta)==512*8
si=Image.open(h/'tiles.png');oi=Image.open(o/'tiles.png');primary=Image.open(R/'data/tilesets/primary/bl_gym_azalea/tiles.png')
def tile(im,i):
 x=(i%16)*8;y=(i//16)*8;return im.crop((x,y,x+8,y+8)).tobytes()
for oldid,newid in mmap.items():
 expected=attr[oldid] if attr[oldid]&255!=0xf0 else attr[oldid]&~255
 assert outattr[newid-512]==expected
 for s,t in zip(meta[oldid*8:oldid*8+8],outmeta[(newid-512)*8:(newid-511)*8]):
  assert s&0xc00==t&0xc00 and (s>>12)+7==t>>12
  assert tile(si,s&1023)==tile(primary,t&1023) if (t&1023)<512 else tile(si,s&1023)==tile(oi,(t&1023)-512)
for i in (0,1):assert (h/f'palettes/{i:02}.pal').read_bytes()==(o/f'palettes/{i+7:02}.pal').read_bytes()
# Required shared transition assets: primary is exactly shared, secondary
# metatile 514, behavior, palette 6 and its referenced graphic 582 match town.
assert outmeta[16:24]==words(c/'metatiles.bin')[16:24] and outattr[2]==words(c/'metatile_attributes.bin')[2]
assert (o/'palettes/06.pal').read_bytes()==(c/'palettes/06.pal').read_bytes()
assert tile(oi,70)==tile(Image.open(c/'tiles.png'),70)
city=words(R/'data/layouts/AzaleaTown/map.bin')
assert {city[y*48+x]&1023 for y in range(10,34) for x in range(41,48)}=={1,198,514}
assert {new[y*32+x]&1023 for y in range(24) for x in range(7)}=={1,198,514}
l=next(v for v in json.loads((R/'data/layouts/layouts.json').read_text())['layouts'] if v['id']=='LAYOUT_JOHTO_ROUTE33');assert (l['width'],l['height'],l['primary_tileset'],l['secondary_tileset'])==(32,24,'gTileset_BlGymAzaleaPrimary','gTileset_HnsRoute33')
m=json.loads((R/'data/maps/JohtoRoute33/map.json').read_text());src=json.loads(subprocess.check_output(['git','show','3138de89d9:data/maps/JohtoRoute33/map.json'],cwd=R));assert m==src
assert m['warp_events'][0]['x']==24 and m['warp_events'][0]['y']==7 and m['warp_events'][0]['dest_warp_id']=='2'
assert outattr[(new[7*32+24]&1023)-512]&255==0x60
objects={(v['x'],v['y']) for v in m['object_events']};warps={(v['x'],v['y']) for v in m['warp_events']}
def walk(x,y):return 0<=x<32 and 0<=y<24 and not new[y*32+x]&0xc00 and new[y*32+x]>>12==3 and (x,y) not in objects
q=deque([(0,12)]);seen={(0,12)}
while q:
 x,y=q.popleft()
 for dx,dy in ((0,1),(0,-1),(1,0),(-1,0)):
  p=x+dx,y+dy
  if p not in seen and walk(*p):seen.add(p);q.append(p)
assert (24,7) in seen and all((0,y) in seen for y in (11,12,13))
assert all(any((x+dx,y+dy) in seen for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))) for x,y in signs|objects)
assert all((x,y) in seen for y in range(24) for x in range(32) if walk(x,y))
oldwalk={(x,y) for y in range(24) for x in range(32) if not old[y*32+x]&0xc00 and old[y*32+x]>>12 in (0,3)}
assert len(oldwalk)==530
relocated=0
for x,y in oldwalk:
 if walk(x,y):assert (x,y) in seen;continue
 for rad in range(1,57):
  p=next(((nx,ny) for ny in range(y-rad,y+rad+1) for nx in range(x-rad,x+rad+1) if abs(nx-x)+abs(ny-y)==rad and walk(nx,ny) and (nx,ny) not in warps),None)
  if p:break
 assert p in seen,(x,y,p);relocated+=1
print('PASS donor metatile remap/attributes/pixels, preserved 7-column seam and boundary resources, cave+west graph, %d-cell static path and %d old collision-free cells; %d require nearest-clear relocation.'%(len(seen),len(oldwalk),relocated))
print('Prototype only: no actual build, play, clipping/priority, reload or visual approval established.')
