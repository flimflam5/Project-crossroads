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
    assert v>>12==3 and not v&0xc00 and at&255==0;deck=art['deck']['metatiles'][0];assert ground==metas[(deck-512)*8:(deck-512)*8+4],'Actual timber terrace retained beneath the mast'
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
# QA10 source-facing Port: preserve canonical warp coordinates23/24,52;
# the visible covered entrance is at the north end, solid body extends south.
a=art['port'];ox,oy=20,51
assert (a['width'],a['height'],a['door_x'],a['door_y'])==(8,6,3,1)
assert a['doors']==[[3,1],[4,1]] and a['canopy']==[[3,0],[4,0]]
expected_solid={(x,y)for y in range(1,6)for x in range(8)if(y>=4 or x not in(0,7))and(x,y)not in{(3,1),(4,1)}}
assert set(map(tuple,a['solid']))==expected_solid,'Port body mask cannot shrink to hide entry faults'
deck_id=art['deck']['metatiles'][0];deck=metas[(deck_id-512)*8:(deck_id-512)*8+4]
for y in range(6):
 for x in range(8):
  v=t[(oy+y)*64+ox+x];n=v&1023;at=attrs[n-512];door=(x,y)in{(3,1),(4,1)};canopy=(x,y)in{(3,0),(4,0)};solid=(x,y)in expected_solid
  assert n==a['metatiles'][y*8+x],('Port sign/other stamp overwrote visible body',x,y)
  assert bool(v&0xc00)==solid,('Port solid wall or visible opening mismatch',x,y)
  # The two public north landings must not hide Joe's torso/legs under the
  # blue arch. COVERED1 draws these unchanged pixels below Joe; all other
  # roof/eave/body layers retain the exact reviewed original profile.
  expected_layer=0x1000 if y>=4 or door or canopy else 0
  expected_behavior=0x61 if door else 0x15 if not solid and not canopy else 0
  assert at==expected_layer|expected_behavior,('Port arrival canopy or other exact layer/behavior differs',x,y,hex(at),hex(expected_layer|expected_behavior))
  if door or canopy:
   assert v>>12==3 and metas[(n-512)*8:(n-512)*8+4]==deck,'Covered portal needs real dry deck under its artwork'
   assert at&255==(0x61 if door else 0),'Both north-facing leaves need actual native warp behavior; canopy itself is ordinary floor'
  else:
   assert v>>12==1 and metas[(n-512)*8:(n-512)*8+4]==general[0x170*8:0x170*8+4],'Waterfront roof/body must retain native sea underlay'
   if not solid:assert at&255==0x15,'Thin eaves are real water, never a hidden pedestrian bypass'
# No U-turn or water entry is necessary: both north fronts join the harbor pier.
for x in(23,24):
 for y in range(46,52):assert t[y*64+x]>>12==3 and not t[y*64+x]&0xc00,('North passenger pier/front obstructed',x,y)
assert t[53*64+23]&0xc00 and t[53*64+24]&0xc00,'Closed south body must not remain a second invisible door'
assert all(v==0x1570 for v in t[63*64:64*64]),'Southern sea is not a rectangular forest hedge'
assert words('data/layouts/OlivineCity/border.bin')==(0x1170,)*4,'Off-map south view continues the ocean'
print('Canonical harbor sailboats/3street pennants: water/layer/hull/pole footprints, clear5-wide roads, no arrows and ocean boundary: PASS')
