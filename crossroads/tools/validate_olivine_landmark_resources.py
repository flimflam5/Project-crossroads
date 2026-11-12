#!/usr/bin/env python3
"""Independent exact resource-size/bounds checks for Olivine maritime rooms.

An earlier draft accidentally wrote a16x16 prop over the128x256 secondary sheet.
All original metatile references still looked numerically valid, so connectivity
could not detect the resulting VRAM overreads. This test checks actual images,
source glyph preservation and every referenced8x8 glyph, independently of writer.
"""
import json,re,struct,subprocess
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2]
base=R/'data/tilesets/secondary/hgss_temple';dest=R/'data/tilesets/secondary/hgss_olivine_landmarks'
original=Image.open(base/'tiles.png');secondary=Image.open(dest/'tiles.png')
assert secondary.size==(128,256),('Maritime secondary image overwritten/truncated',secondary.size)
assert secondary.mode=='P' and secondary.getextrema()[1]<=15
def words(p):b=p.read_bytes();return struct.unpack('<'+str(len(b)//2)+'H',b)
metas=words(dest/'metatiles.bin');attrs=words(dest/'metatile_attributes.bin');old=words(base/'metatiles.bin')
assert len(metas)==len(attrs)*8 and len(attrs)==len(old)//8+120==512
# QA10 appends exactly two gangway step-warp drawings; every preexisting
# maritime behavior/layer entry remains exact, including the native lift.
old_attr_bytes=subprocess.check_output(['git','show','285cfa4ebddcb390a8a5bde6116748cbb5eaba6b:data/tilesets/secondary/hgss_olivine_landmarks/metatile_attributes.bin'],cwd=R)
old_attrs=struct.unpack('<'+str(len(old_attr_bytes)//2)+'H',old_attr_bytes)
assert len(old_attrs)==510 and attrs[:510]==old_attrs and attrs[510:]==(0x1061,0x1061),'Only the two named new physical boarding leaves may append behavior entries'
def tile(im,n):return im.crop((n%16*8,n//16*8,n%16*8+8,n//16*8+8)).tobytes()
assert secondary.tobytes()==original.tobytes(),'Original temple glyphs were overwritten by private maritime art'
for i,v in enumerate(old):assert metas[i]&0xfff==v&0xfff,('Original glyph/flip reference changed rather than colour adaptation',i)
protected={v&1023 for v in words(R/'data/tilesets/primary/building/metatiles.bin')}|{v&1023 for v in words(R/'data/tilesets/primary/general/metatiles.bin')[0x170*8:0x171*8]}
primaries={};changed={}
for kind in ['building','general']:
 src=Image.open(R/f'data/tilesets/primary/{kind}/tiles.png');im=Image.open(R/f'data/tilesets/primary/hgss_olivine_landmark_{kind}/tiles.png');assert im.size==src.size==(128,256) and im.mode=='P' and im.getextrema()[1]<=15
 edited={n for n in range(512) if tile(im,n)!=tile(src,n)};assert edited and edited<=set(range(432))-protected,(kind,'Native glyph/animation overwritten',sorted(edited))
 primaries[kind]=im;changed[kind]=edited
for value in metas:
 glyph=value&1023;source=secondary if glyph>=512 else primaries['building'];count=(source.width//8)*(source.height//8)
 assert glyph%512<count,('Out-of-bounds8x8 glyph reference',glyph,count)
 assert value>>12<=12,('UI-only palette used for map',value>>12)
headers=(R/'src/data/tilesets/headers.h').read_text()
for sym,kind in [('HgssOlivineLandmarkIndoor','InsideBuilding'),('HgssOlivineLandmarkOutdoor','General')]:
 meta=kind if kind=='InsideBuilding' else sym
 m=re.search(r'const struct Tileset gTileset_'+sym+r'\s*=\s*\{([^}]+)\}',headers,re.S);assert m and f'gTilesetPalettes_{kind}' in m[1] and f'gMetatiles_{meta}' in m[1] and f'gMetatileAttributes_{meta}' in m[1],('Wrong compatible primary alias',sym)
original_general=words(R/'data/tilesets/primary/general/metatiles.bin');original_attrs=words(R/'data/tilesets/primary/general/metatile_attributes.bin');private_general=words(R/'data/tilesets/primary/hgss_olivine_landmark_general/metatiles.bin');private_attrs=words(R/'data/tilesets/primary/hgss_olivine_landmark_general/metatile_attributes.bin')
for n in range(512):
 if n not in range(0x100,0x148):assert private_general[n*8:n*8+8]==original_general[n*8:n*8+8] and private_attrs[n]==original_attrs[n],('Native outdoor metatile changed outside rear port facade',n)
ls={l['id']:l for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
for name in ['OlivineCity_Lighthouse_1F','OlivineCity_Lighthouse_6F']:
 m=json.loads((R/f'data/maps/{name}/map.json').read_text());l=ls[m['layout']];raw=words(R/l['blockdata_filepath']);lift_start=512+len(old)//8
 # QA10 private lighthouse drawing aliases replace only the visible hatch
 # art IDs. Original maritime lift entries remain exact; the actual new map
 # cells must retain each corresponding full behavior/layer attribute.
 from validate_city_ground_layers import side
 assert l['secondary_tileset']=='gTileset_HgssOlivineLighthouse',('Lighthouse private art pointer absent',name)
 actual=side(l['secondary_tileset'])[1]
 for x,old_n in zip([8,9],[lift_start,lift_start+1]):
  n=raw[4*l['width']+x]&1023
  assert n>=512 and actual[n-512]==attrs[old_n-512],('Private hatch lost actual native lift behavior',name,x,hex(n))
 for n in [lift_start,lift_start+1]:assert attrs[n-512]&255==0x61
# The earlier overwrite could pass a writer's own--check; independently reject it
# by its real dimension, even if the generated bytes happen to match the writer.
assert len({v&1023 for v in metas if v&1023>=512})>300,'Secondary art unexpectedly collapsed'
print('Olivine maritime image dimensions,4bpp indices, all glyph bounds/palettes, preserved source glyphs and native primary aliases: PASS')
