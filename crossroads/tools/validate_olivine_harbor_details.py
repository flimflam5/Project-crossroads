#!/usr/bin/env python3
"""Positive semantic regression for actual HGSS sailboats/street pennants.

Checks visible hull/overhang footprints, native Surf behavior and open arch lanes;
this does not replace normal-movement emulator tests or owner visual review.
"""
import json,struct
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def js(p):return json.loads((R/p).read_text())
def words(p):b=(R/p).read_bytes();return struct.unpack('<'+str(len(b)//2)+'H',b)
art=js('crossroads/hgss/art/olivine/manifest.json')['specs'];t=words('data/layouts/OlivineCity/map.bin');assert len(t)==4096
# Test the actually integrated city resources, including the owner Gym packer.
metas=words('data/tilesets/secondary/bl_gym_olivine/metatiles.bin');attrs=words('data/tilesets/secondary/bl_gym_olivine/metatile_attributes.bin');general=words('data/tilesets/primary/general/metatiles.bin');western=words('data/tilesets/secondary/western_city/metatiles.bin')
a=art['sailboat'];p=art['sailboat_paving'];assert (a['width'],a['height'])==(6,5)
for ox,oy in [(13,45),(30,45)]:
 for y in range(5):
  for x in range(6):
   v=t[(oy+y)*64+ox+x];n=v&1023;assert n>=512;at=attrs[n-512];ground=metas[(n-512)*8:(n-512)*8+4]
   if y>=2:
    assert (v>>12)==1 and at&255==0x15,'No invisible grass islands in the harbor'
    assert ground==general[0x170*8:0x170*8+4],'Native animated water retained beneath transparent sail pixels'
    assert bool(v&0xc00)==(y>=3),'Only the visible hull blocks Surf; mast/sail overhang stays traversable'
    assert bool(at&0x1000)==(y>=3),'Sail is foreground; hull is covered plane'
   elif y==0:
    assert v>>12==3 and not v&0xc00 and at&255==0;assert ground==western[16:20],'Quay paving retained beneath the mast'
   else:assert v&0xc00,'Actual quay seawall remains solid'
a=art['pennant_arch'];assert (a['width'],a['height'])==(7,3)
for ox,oy in [(20,7),(7,16),(20,28)]:
 for y in range(3):
  for x in range(7):
   v=t[(oy+y)*64+ox+x];n=v&1023;at=attrs[n-512]
   assert at&255==0,'No stray arrow/warp behavior under street decorations'
   assert bool(v&0xc00)==(y==2 and x in [0,6]),'Arch posts block only their ground footprint'
   assert bool(at&0x1000)==(y==2 and x in [0,6]),'Bunting/pole overhang is drawn above Joe'
   assert metas[(n-512)*8:(n-512)*8+4]==western[16:20],'Consistent road paving under entire opening'
 for y in range(3):assert all(not t[(oy+y)*64+ox+x]&0xc00 for x in range(1,6)),'All five road columns remain open'
# Port body/glass is solid, not a pass-through workaround for arrival facing.
a=art['port'];ox,oy=20,47
for y in range(a['height']):
 for x in range(a['width']):
  v=t[(oy+y)*64+ox+x];n=v&1023;at=attrs[n-512];solid=[x,y] in a['solid'];door=[x,y] in a['doors']
  assert bool(v&0xc00)==solid,'Port upper glass/roof body must block; both actual lower leaves stay open'
  assert metas[(n-512)*8:(n-512)*8+4]==general[0x170*8:0x170*8+4],'No grass under a waterfront roof'
  if door:assert v>>12==3 and at&255==0x60
  elif not solid:assert v>>12==1 and at&255==0x15,'Eaves retain real sea beneath them'
assert all(v==0x1570 for v in t[63*64:64*64]),'Southern sea is not a rectangular forest hedge'
assert words('data/layouts/OlivineCity/border.bin')==(0x1170,)*4,'Off-map south view continues the ocean'
print('Canonical harbor sailboats/3street pennants: water/layer/hull/pole footprints, clear5-wide roads, no arrows and ocean boundary: PASS')
