#!/usr/bin/env python3
"""Static Route 33 reconstruction checks; not a substitute for emulator play."""
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
new=words(R/'data/layouts/JohtoRoute33/map.bin');source=[d[(y+4)*44+x+8] for y in range(32) for x in range(32)]
old=words(R/'crossroads/donor/hns-route33/data/layouts/Route33_hns/black-ledger-baseline.bin')
meta=words(h/'metatiles.bin');attr=words(h/'metatile_attributes.bin');outmeta=words(o/'metatiles.bin');outattr=words(o/'metatile_attributes.bin');used=sorted({v&1023 for v in source});freemeta=[v for v in range(512,1024) if v!=514];mmap={v:freemeta[i] for i,v in enumerate(used)}
assert len(source)==len(new)==1024 and len(old)==768 and len(used)==71
signs={(13,19),(18,14)}
tree_aprons={(23,26),(24,26),(24,25)}
transition={(7,15+row):freemeta[len(used)+row] for row in range(3)}
for i,(raw,val) in enumerate(zip(source,new)):
 x,y=i%32,i//32
 if x<7: assert val==old[max(0,min(23,y-4))*32+x];continue
 if (x,y) in signs:assert val==0x3403;continue
 if (x,y) in tree_aprons:assert val==0x3000|mmap[1];continue
 if (x,y) in transition:
  assert not raw&0xc00 and raw>>12==3, ('Transition must not open an obstacle',x,y)
  assert val==0x3000|transition[(x,y)];continue
 want=(raw&0xfc00)|mmap[raw&1023]
 if want>>12==0 and not want&0xc00:want|=0x400
 assert val==want,(x,y,hex(val),hex(want))
assert len(outattr)==512 and len(outmeta)==512*8
si=Image.open(h/'tiles.png');oi=Image.open(o/'tiles.png');primary=Image.open(R/'data/tilesets/primary/bl_gym_azalea/tiles.png')
def tile(im,i):
 x=(i%16)*8;y=(i//16)*8;return im.crop((x,y,x+8,y+8)).tobytes()
bankmap={0:7,1:8,4:9,6:10}
for oldid,newid in mmap.items():
 expected=attr[oldid] if attr[oldid]&255!=0xf0 else attr[oldid]&~255
 assert outattr[newid-512]==expected
 for s,t in zip(meta[oldid*8:oldid*8+8],outmeta[(newid-512)*8:(newid-511)*8]):
  assert s&0xc00==t&0xc00 and bankmap[s>>12]==t>>12
  assert tile(si,s&1023)==tile(primary,t&1023) if (t&1023)<512 else tile(si,s&1023)==tile(oi,(t&1023)-512)
for oldbank,newbank in bankmap.items():assert (h/f'palettes/{oldbank:02}.pal').read_bytes()==(o/f'palettes/{newbank:02}.pal').read_bytes()
# Verify each transition pixel against the preserved town paving and exact
# intended transparent taper; this is still only a static render check.
road=Image.open(c/'tiles.png').crop((70%16*8,70//16*8,70%16*8+8,70//16*8+8)).tobytes()
ground=outmeta[(mmap[9]-512)*8:(mmap[9]-512)*8+4]
for row in range(3):
 mi=transition[(7,15+row)]-512; words4=outmeta[mi*8:mi*8+8]
 assert words4[:4]==ground and outattr[mi]==0
 for y in range(16):
  limit=(8+y//2 if row==0 else 15 if row==1 else 15-y//2)
  for x in range(16):
   v=words4[4+(y//8)*2+x//8]
   if v:
    assert v>>12==6 and (v&1023)>=512 and (v&1023)!=582
    pixel=oi.getpixel((((v&1023)-512)%16*8+x%8,((v&1023)-512)//16*8+y%8))
   else:pixel=0
   assert pixel==(road[(y%8)*8+x%8] if x<limit else 0), ('Paving transition pixel',row,x,y)
# Required shared transition assets: primary is exactly shared, secondary
# metatile 514, behavior, palette 6 and its referenced graphic 582 match town.
assert outmeta[16:24]==words(c/'metatiles.bin')[16:24] and outattr[2]==words(c/'metatile_attributes.bin')[2]
assert (o/'palettes/06.pal').read_bytes()==(c/'palettes/06.pal').read_bytes()
assert tile(oi,70)==tile(Image.open(c/'tiles.png'),70)
city=words(R/'data/layouts/AzaleaTown/map.bin')
assert {city[y*48+x]&1023 for y in range(10,34) for x in range(41,48)}=={1,198,514}
assert {new[y*32+x]&1023 for y in range(32) for x in range(7)}=={1,198,514}
l=next(v for v in json.loads((R/'data/layouts/layouts.json').read_text())['layouts'] if v['id']=='LAYOUT_JOHTO_ROUTE33');assert (l['width'],l['height'],l['primary_tileset'],l['secondary_tileset'])==(32,32,'gTileset_BlGymAzaleaPrimary','gTileset_HnsRoute33')
m=json.loads((R/'data/maps/JohtoRoute33/map.json').read_text());src=json.loads(subprocess.check_output(['git','show','3138de89d9:data/maps/JohtoRoute33/map.json'],cwd=R))
for k in m.keys()-{'connections','object_events','warp_events','bg_events'}:assert m[k]==src[k],('Unrelated route metadata changed',k)
assert m['connections']==[{'map':'MAP_AZALEA_TOWN','offset':-6,'direction':'left'}]
town=json.loads((R/'data/maps/AzaleaTown/map.json').read_text())
assert {'map':'MAP_JOHTO_ROUTE33','offset':6,'direction':'right'} in town['connections']
assert len(m['warp_events'])==len(src['warp_events'])==1
assert m['warp_events'][0]==dict(src['warp_events'][0],x=19,y=13)
assert outattr[(new[13*32+19]&1023)-512]&255==0x60
# Pin the complete event dictionaries: this protects their flags, movement,
# scripts, elevation and all other fields, not just the visible locations.
resident=src['object_events'][0]
assert m['object_events']==[
 dict(resident,x=21,y=25),
 dict(resident,graphics_id='OBJ_EVENT_GFX_HIKER',x=10,y=19,script='Johto_JohtoRoute33_Hiker'),
 dict(resident,graphics_id='OBJ_EVENT_GFX_ROUTE33_APRICORN_PINK',x=23,y=26,script='Johto_JohtoRoute33_ApricornTree'),
 dict(resident,graphics_id='OBJ_EVENT_GFX_ROUTE33_APRICORN_BLACK',x=24,y=26,script='Johto_JohtoRoute33_ApricornTree'),
]
assert m['bg_events']==[dict(src['bg_events'][0],x=13,y=19),dict(src['bg_events'][1],x=18,y=14)]
objects={(v['x'],v['y']) for v in m['object_events']};warps={(v['x'],v['y']) for v in m['warp_events']}
def walk(x,y):return 0<=x<32 and 0<=y<32 and not new[y*32+x]&0xc00 and new[y*32+x]>>12==3 and (x,y) not in objects
q=deque([(0,16)]);seen={(0,16)}
while q:
 x,y=q.popleft()
 for dx,dy in ((0,1),(0,-1),(1,0),(-1,0)):
  p=x+dx,y+dy
  if p not in seen and walk(*p):seen.add(p);q.append(p)
assert (19,13) in seen and all((0,y) in seen for y in (15,16,17))
assert all(any((x+dx,y+dy) in seen for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))) for x,y in signs|objects)
assert all((x,y) in seen for y in range(32) for x in range(32) if walk(x,y))
# An old saved NPC may retain the pre-reconstruction coordinates until the
# object state refreshes.  Reserve that tile as occupied as well and prove the
# cave and town remain reachable; do not assume it teleports to the new site.
legacy_npc=(src['object_events'][0]['x'],src['object_events'][0]['y'])
legacy_seen={(0,16)}; q=deque(legacy_seen)
while q:
 x,y=q.popleft()
 for dx,dy in ((0,1),(0,-1),(1,0),(-1,0)):
  p=x+dx,y+dy
  if p not in legacy_seen and p!=legacy_npc and walk(*p):legacy_seen.add(p);q.append(p)
assert (19,13) in legacy_seen and all((0,y) in legacy_seen for y in (15,16,17))
assert all(any((x+dx,y+dy) in legacy_seen for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))) for x,y in signs|objects)
oldwalk={(x,y) for y in range(24) for x in range(32) if not old[y*32+x]&0xc00 and old[y*32+x]>>12 in (0,3)}
assert len(oldwalk)==530
relocated=0
for x,y in oldwalk:
 if walk(x,y) and (x,y) not in warps:assert (x,y) in seen;continue
 for rad in range(1,57):
  p=next(((nx,ny) for ny in range(y-rad,y+rad+1) for nx in range(x-rad,x+rad+1) if abs(nx-x)+abs(ny-y)==rad and walk(nx,ny) and (nx,ny) not in warps),None)
  if p:break
 assert p in seen,(x,y,p);relocated+=1
print('PASS donor metatile remap/attributes/pixels, preserved 7-column seam and boundary resources, cave+west graph, %d-cell static path and %d old collision-free cells; %d require nearest-clear relocation.'%(len(seen),len(oldwalk),relocated))
print('Prototype only: no actual build, play, clipping/priority, reload or visual approval established.')
