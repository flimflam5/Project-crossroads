#!/usr/bin/env python3
"""Independent source-specific material and immutable V7 physics regressions.

HGSS collision flags identify obstruction, not whether it is a fence, table,
cliff or boulder. Positive material/underlay checks supplement normal-play QA.
"""
import json,struct,subprocess,hashlib
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2];BASE='3f935d5e8600c5a280b9172b555edb35ca52b6c0'
def js(p):return json.loads((R/p).read_text())
def words(b):return struct.unpack('<'+str(len(b)//2)+'H',b)
def old(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R)
t=words((R/'data/layouts/OlivineCity/map.bin').read_bytes());before=words(old('data/layouts/OlivineCity/map.bin'));assert len(t)==len(before)==4096
art=js('crossroads/hgss/art/olivine/manifest.json')['specs'];table={(x,42) for a in [7,14,29] for x in range(a,a+4)}
port_contract=js('crossroads/hgss/contracts/olivine-port-model-qa09.json');assert port_contract['source_commit']==BASE and port_contract['source_model']==167 and port_contract['source_model_bbox']==[16,54,27,60]
port={(v['x'],v['y']):v for v in port_contract['allowed_blocked_to_sea']};assert len(port)==65 and port_contract['count']==65
reference=js('crossroads/hgss/canonical_events/johto-outdoor-geometry.json')['areas']['MAP_OLIVINE'];permissions={};anchors=[]
for c in reference['cells']:
 for y in range(32):
  for x in range(32):permissions[c['x']*32+x,c['y']*32+y]=c['permissions'][y*32+x]
 for prop in c['props']:
  if prop['model']==167:anchors.append([prop['tile_x']+c['x']*32,prop['tile_z']+c['y']*32])
assert anchors==[[23.5,58]] and port_contract['source_model_absolute_anchor']==[23.5,58]
assert port_contract['source_terrain_blob_sha']==reference['source']['terrain_blob_sha']
assert set(port)=={(x,y) for y in range(54,61) for x in range(16,28) if before[y*64+x]&0xc00 and permissions[x,y]==0x8000},'Only immutable formerly blocked cells in the documented source model bbox may open'
# First retain the full immutable V7→QA09 material repair proof. QA10's
# independently reviewed north-port physical migration is applied afterwards.
qa09_bytes=subprocess.check_output(['git','show','285cfa4ebddcb390a8a5bde6116748cbb5eaba6b:data/layouts/OlivineCity/map.bin'],cwd=R)
qa09=words(qa09_bytes)
for i,(a,b) in enumerate(zip(before,qa09)):
 if (i%64,i//64) in port:
  q=port[i%64,i//64];assert a==int(q['before_hex'],16) and a&0xc00 and b==0x1170,('Exact obsolete Port167 body→sea repair',i%64,i//64);continue
 if (i%64,i//64) not in table:assert a&0xfc00==b&0xfc00,('Unrelated city collision/elevation changed',i%64,i//64,hex(a),hex(b))
 else:assert b&0xfc00==0x3000,('Relocated source table blocker must open',i%64,i//64)
# Exact82-cell transition from the authenticated QA09 physical map. The
# authored mask covers actual north-facing body/pier/retired-boardwalk changes
# and the relocated plaque. It never exempts a whole arbitrary rectangle.
contract_path=R/'crossroads/hgss/qa10/olivine-north-port-physics-contract.json'
contract_bytes=contract_path.read_bytes()
assert hashlib.sha256(contract_bytes).hexdigest()=='a45a84d77f40606d21168ca3c9a6e40589bffcf516376cc6f3389cb2f1d9e23a','Reviewed QA10 physics mask changed'
contract=json.loads(contract_bytes)
assert contract['baseline']=='285cfa4ebddcb390a8a5bde6116748cbb5eaba6b' and contract['physical_changed_cells']==82
assert contract['raw_before_sha256']==hashlib.sha256(qa09_bytes).hexdigest()=='74cbcf16c294259e0ebbce0c541bd70cf061c5617654a802510411ac4d9fba6c'
changes={(e['x'],e['y']):e for e in contract['changes']};assert len(changes)==82
seen_changes=set()
for i,(a,b)in enumerate(zip(qa09,t)):
 point=i%64,i//64
 if point in changes:
  rec=changes[point];assert a==rec['before_word'] and a&0xfc00==rec['before_physics']
  assert b&0xfc00==rec['after_physics'] and rec['before_physics']!=rec['after_physics'],('Exact north-port physics delta missing/changed',point,hex(a),hex(b))
  seen_changes.add(point)
 else:assert a&0xfc00==b&0xfc00,('Unrelated QA09 physical/elevation change',point,hex(a),hex(b))
assert seen_changes==set(changes)
primary=words((R/'data/tilesets/primary/bl_gym_olivine/metatiles.bin').read_bytes());secondary=words((R/'data/tilesets/secondary/bl_gym_olivine/metatiles.bin').read_bytes());coast=words((R/'data/tilesets/primary/hgss_olivine_coast_buffer/metatiles.bin').read_bytes());ca=words((R/'data/tilesets/primary/hgss_olivine_coast_buffer/metatile_attributes.bin').read_bytes())
def row(n):return [primary,secondary][n//512][n%512*8:n%512*8+8]
def at(x,y):return t[y*64+x]&1023
deck=row(art['deck']['metatiles'][0])[:4]
# Every old table footprint is now the visible deck or the correctly grounded
# relocated parasol canopy. Blocking unrelated ground is not an accepted repair.
for x,y in table:assert row(at(x,y))[:4]==deck,('Old source table rendered as cliff or grass',x,y)
for n in art['parasol']['metatiles']:assert row(n)[:4]==deck,'No grass beneath furniture on a wooden deck'
for x,y in [(8,43),(14,43),(24,43),(35,43)]:assert at(x,y)==art['deck']['metatiles'][0],('Timber terrace sample',x,y)
# Explicit NW white fence boundaries, excluding cells already covered by a real
# V7 facade. Earth cliff at the main street's eastern edge is separately pinned.
# Exact surviving source fence sections, audited against HGSS and immutable
# V7 raw cells. BL infill/native facade aprons already replace the other source
# sections; this proof must neither invent a coverage target nor block an apron.
expected_fences={(6,y) for y in range(10,20)}|{(x,10) for x in [7,8,9,17,18,19,20]}|{(13,y) for y in [21,22,23]}
assert len(expected_fences)==20
for x,y in expected_fences:
 a=before[y*64+x];assert a&0xc00 and a&1023 in [0x71,0x75,0x76,0x79,0x7c],('Immutable prior fence footing',x,y)
 expected='fence_corner' if (x,y)==(6,10) else 'fence_v' if x in [6,13] else 'fence_h';assert at(x,y)==art[expected]['metatiles'][0],('White court fence misclassified as earth',x,y)
fences=len(expected_fences)
# Rows7–9 contain the pennant arch composite, whose private metatile IDs
# repack. Pin genuine unobscured primary earth-cliff words above that model.
for x,y in [(26,2),(26,4),(26,6)]:assert t[y*64+x]==before[y*64+x],'Genuine main-road cliff remains unchanged'
# All four independently identified offshore rock groups use actual gray boulder
# art over native sea, while collision remains exactly the pre-material flags.
for x,y in [(58,20),(59,24),(55,26),(58,30)]:assert at(x,y)==art['sea_boulder']['metatiles'][0],('Offshore gray boulder',x,y)
# The Route40 primary clone changes only the three explicitly unused metatiles
# and glyphs they reference, preserving all original route cells and resources.
oldm=words(old('data/tilesets/primary/hgss_ecruteak_buffer/metatiles.bin'));olda=words(old('data/tilesets/primary/hgss_ecruteak_buffer/metatile_attributes.bin'))
refs=set()
for n in range(512):
 if n in range(0x100,0x103):
  assert coast[n*8:n*8+8]==primary[n*8:n*8+8];refs.update(v&1023 for v in coast[n*8:n*8+8])
 else:assert coast[n*8:n*8+8]==oldm[n*8:n*8+8] and ca[n]==olda[n],('Unrelated coast buffer metadata',n)
assert max(refs)<432
new=Image.open(R/'data/tilesets/primary/hgss_olivine_coast_buffer/tiles.png');native=Image.open(R/'data/tilesets/primary/hgss_ecruteak_buffer/tiles.png');city=Image.open(R/'data/tilesets/primary/bl_gym_olivine/tiles.png')
for n in range(512):
 box=(n%16*8,n//16*8,n%16*8+8,n//16*8+8)
 if n in refs:assert new.crop(box).tobytes()==city.crop(box).tobytes()
 else:assert new.crop(box).tobytes()==native.crop(box).tobytes(),('Unrelated route glyph changed',n)
layouts={v['id']:v for v in js('data/layouts/layouts.json')['layouts']};route=js('data/maps/JohtoRoute40/map.json');l=layouts[route['layout']];assert l['primary_tileset']=='gTileset_HgssOlivineCoastBuffer' and l['secondary_tileset']=='gTileset_WesternCity';assert (R/l['blockdata_filepath']).read_bytes()==old(l['blockdata_filepath']);assert route==json.loads(old('data/maps/JohtoRoute40/map.json'))
# Palette3 is shared General on each side; no copied secondary palette slots are
# needed for the fence, and no engine palette capacity is expanded.
for n in [0x100,0x101,0x102]:assert all(v>>12==3 for v in coast[n*8:n*8+8]),'Seam fence uses shared native gray palette'
print('Olivine material classification,12relocated tables,',fences,'white fence cells, timber/parasols, gray breakwater and Route40 buffer: PASS; exact V7→QA09 12table/65model migration retained; exact82-cell QA09→QA10 north-port migration, all other physics unchanged')
