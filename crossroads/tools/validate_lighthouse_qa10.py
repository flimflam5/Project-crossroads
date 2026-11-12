#!/usr/bin/env python3
"""QA10 reference-finish constraints for the six unchanged lighthouse floors and their balcony.

Checks the actual map/resource outputs against immutable QA09 physical and
interaction data. New floor artwork must use private resources and proper
hardware layers; a build/source pass is not visual acceptance.
"""
import argparse
from collections import Counter
from PIL import Image
import json
from pathlib import Path
import re
import shutil
import struct
import subprocess

from validate_ss_aqua import BASE, R, load, old_bytes, old_json, resources, words

NAMES = tuple(f'OlivineCity_Lighthouse_{i}F' for i in range(1, 7)) + ('OlivineCity_Lighthouse_Balcony',)


def baseline_attrs(symbol):
 header = old_bytes('src/data/tilesets/headers.h').decode()
 definitions = old_bytes('src/data/tilesets/metatiles.h').decode()
 body = re.search(r'const struct Tileset\s+'+re.escape(symbol)+r'\s*=\s*\{(.*?)\};',header,re.S)
 assert body, ('Unresolved baseline tileset', symbol)
 attr = re.search(r'\.metatileAttributes\s*=\s*(\w+)',body[1])[1]
 path = re.search(re.escape(attr)+r'\[\]\s*=\s*INCBIN_U16\("([^"]+)"',definitions)[1]
 b = old_bytes(path)
 return struct.unpack('<' + str(len(b)//2) + 'H', b)


def composed_colors(layout, cell):
 from validate_city_ground_layers import side
 p,s=[side(layout[k])for k in('primary_tileset','secondary_tileset')]
 def glyph(word):
  n=word&1023;im=(p,s)[n>=512][2];i=n%512
  tile=im.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8))
  if word&0x400:tile=tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if word&0x800:tile=tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  bank=word>>12;pal=(p,s)[bank>=6][3][bank]
  return tuple(pal[v]if v else None for v in tile.tobytes())
 n=cell&1023;pool=(p,s)[n>=512];i=n%512;refs=pool[0][i*8:i*8+8];layer=pool[1][i]>>12
 bottom=sum((glyph(v)for v in refs[:4]),());top=sum((glyph(v)for v in refs[4:]),());backdrop=p[3][0][0]
 filler=glyph(0x3014)*4 if layer==0 else(backdrop,)*256
 return Counter(t if t is not None else b if b is not None else f if f is not None else backdrop for b,t,f in zip(bottom,top,filler))


def motif_assertions(name,layout,raw):
 # Independently selected ordinary-floor points, compared with inspected HGSS
 # rasters. These literal RGB555 roles are the reviewed original GBA palette,
 # not pixels imported from the reference or values read from the writer.
 w=layout['width'];colors=lambda x,y:composed_colors(layout,raw[y*w+x]);records=[]
 if name.endswith(('_1F','_2F')):
  pale=colors(1,6)if name.endswith('_1F')else colors(6,13);teal=colors(8,10)if name.endswith('_1F')else colors(3,6)
  border=colors(3,6)if name.endswith('_1F')else colors(2,6)
  assert pale[(22,24,23)]>=100,('Missing pale source surround',name,pale)
  assert teal[(9,16,18)]>=100,('Missing teal source runner',name,teal)
  assert border[(17,10,12)]+border[(20,13,14)]>=20,('Missing source burgundy inset edge',name,border)
  records+=['pale surround','teal runner','burgundy edge']
 if name.endswith('_6F'):
  pink=colors(4,14);cyan=colors(8,5)
  assert pink[(22,17,19)]>=100,('Lantern-room pink floor missing',pink)
  assert sum(v for c,v in cyan.items()if c[1]>=18 and c[2]>=20 and c[0]<=20)>=50,('Cyan optical enclosure missing',cyan)
  records+=['pink lantern-room tile','cyan optical housing']
 return records


# Literal mask reviewed against the full HGSS6F raster and actual B3 framebuffer.
# Do not derive expected scope from the writer's delta report.
B3 = "e7e2c085a5a61ef727d06f9f682af7d3a954cc06"
INNER_CORE = {(6,7),(10,7),(5,8),(6,8),(10,8),(11,8),
 (5,9),(6,9),(10,9),(11,9),(5,10),(6,10),(10,10),(11,10),
 (5,11),(6,11),(10,11),(11,11),(5,12),(6,12),(7,12),(9,12),
 (10,12),(11,12),(6,13),(7,13),(9,13),(10,13)}


def verify_inner_core(layouts):
 from validate_city_ground_layers import side
 prior = lambda path: subprocess.check_output(['git','show',B3+':'+path],cwd=R)
 changes=[];pool='data/tilesets/secondary/hgss_olivine_lighthouse/'
 raw_refs=prior(pool+'metatiles.bin');old_refs=struct.unpack('<'+str(len(raw_refs)//2)+'H',raw_refs)
 old_attrs=struct.unpack('<512H',prior(pool+'metatile_attributes.bin'))
 current_refs=words(pool+'metatiles.bin');current_attrs=words(pool+'metatile_attributes.bin')
 used=set()
 for name in NAMES:
  m=load(f'data/maps/{name}/map.json');l=layouts[m['layout']]
  for field in ('blockdata_filepath','border_filepath'):
   b=prior(l[field]);before=struct.unpack('<'+str(len(b)//2)+'H',b);now=words(l[field]);assert len(before)==len(now)
   used.update(v&1023 for v in before if v&1023>=512)
   different={(i%l['width'],i//l['width']) for i,(a,b)in enumerate(zip(before,now))if a!=b}
   expected=INNER_CORE if name.endswith('_6F') and field=='blockdata_filepath' else set()
   assert different==expected,('B4 exact inner-core art scope mismatch',name,field,different,expected)
   for x,y in different:
    a=before[y*l['width']+x];b=now[y*l['width']+x]
    assert a&0xfc00==b&0xfc00,('Inner-core physical data changed',x,y)
    assert old_attrs[(a&1023)-512]==current_attrs[(b&1023)-512],('Inner-core layer/behavior changed',x,y)
    colors=composed_colors(l,b)
    assert colors[(8,26,28)]>=96,('Inner optical wall still lacks continuous cyan body',x,y,colors)
    assert colors[(28,30,29)]==0,('Outer diagonal window reflection leaked into inner enclosure',x,y)
   changes.extend((name,x,y)for x,y in different)
 for n in used:
  i=n-512;assert old_refs[i*8:i*8+8]==current_refs[i*8:i*8+8] and old_attrs[i]==current_attrs[i],('Old used lighthouse alias changed',hex(n))
 from io import BytesIO
 before_sheet=Image.open(BytesIO(prior(pool+'tiles.png')));current_sheet=Image.open(R/pool/'tiles.png')
 glyphs={v&1023 for n in used for v in old_refs[(n-512)*8:(n-512)*8+8]if v&1023>=512}
 for n in glyphs:
  i=n-512;box=(i%16*8,i//16*8,i%16*8+8,i//16*8+8)
  assert before_sheet.crop(box).tobytes()==current_sheet.crop(box).tobytes(),('Previously used lighthouse glyph changed',n)
 for p in sorted((R/pool/'palettes').glob('*.pal')):
  assert p.read_text().splitlines()==prior(str(p.relative_to(R))).decode().splitlines(),('Existing lighthouse palette changed',p.name)
 return {'baseline_game_source':B3,'exact_art_cells':len(changes),'other_six_map_words':'EXACT','physical_bits_and_full_attributes':'EXACT','positive_inner_cyan_cells':28,'two_model_corner_voids_filled':True}


def validate(built=False):
 before_layouts = {v['id']: v for v in old_json('data/layouts/layouts.json')['layouts']}
 layouts = {v['id']: v for v in load('data/layouts/layouts.json')['layouts']}
 from validate_city_ground_layers import side
 report = {'baseline': BASE, 'physical_maps': [], 'visual_acceptance': 'Owner Delta review required'}
 for name in NAMES:
  path=f'data/maps/{name}/map.json'; m=load(path); old=old_json(path)
  assert m == old, ('Lighthouse script/header/event/warp changed during art-only finish', name)
  layout=layouts[m['layout']]; prior=before_layouts[m['layout']]
  for key in ('id','name','width','height','border_filepath','blockdata_filepath','layout_version'):
   assert layout[key] == prior[key], ('Lighthouse layout identity/extent changed',name,key)
  assert (layout['primary_tileset'],layout['secondary_tileset']) != (prior['primary_tileset'],prior['secondary_tileset']), ('Private lighthouse art helper not applied',name)
  assert 'Lighthouse' in layout['secondary_tileset'], ('Lighthouse art leaked into shared/port resource',name,layout['secondary_tileset'])
  previous=[baseline_attrs(prior[k])for k in ('primary_tileset','secondary_tileset')]
  current=[side(layout[k])[1]for k in ('primary_tileset','secondary_tileset')]
  physical=0;art_deltas=0;all_cells=[]
  for field in ('blockdata_filepath','border_filepath'):
   old_data=old_bytes(prior[field]); old_words=struct.unpack('<'+str(len(old_data)//2)+'H',old_data)
   now=words(layout[field]);assert len(now)==len(old_words)
   for index,(was,cell)in enumerate(zip(old_words,now)):
    assert was&0xfc00 == cell&0xfc00, ('Lighthouse collision/elevation changed',name,field,index,hex(was),hex(cell))
    before_id=was&1023;new_id=cell&1023
    assert previous[before_id>=512][before_id%512]&0xfff == current[new_id>=512][new_id%512]&0xfff, ('Lighthouse movement/terrain behavior changed',name,field,index)
    physical+=1;art_deltas+=before_id!=new_id
   all_cells.extend(now)
  quality=resources(layout,all_cells)
  motifs=motif_assertions(name,layout,words(layout['blockdata_filepath']))
  report['physical_maps'].append({'map':name,'physical_cells_unchanged':physical,'metatile_id_changes':art_deltas,'resource_check':quality,'positive_reference_motifs':motifs})
 if built:
  nm=shutil.which('arm-none-eabi-nm') or '/workspace/toolchain/root/usr/bin/arm-none-eabi-nm'
  symbols={p[2]:int(p[0],16)for line in subprocess.check_output([nm,'-an',str(R/'pokeemerald.elf')],text=True).splitlines()if len(p:=line.split())==3}
  rom=(R/'pokeemerald.gba').read_bytes();headers=(R/'data/maps/headers.inc').read_text()
  for name in NAMES:
   m=load(f'data/maps/{name}/map.json');l=layouts[m['layout']];symbol=l['name']+'_Blockdata'
   assert f'data/maps/{name}/header.inc' in headers and symbol in symbols
   offset=symbols[symbol]-0x08000000;data=(R/l['blockdata_filepath']).read_bytes();assert rom[offset:offset+len(data)]==data,('Stale compiled lighthouse art map',name)
  report['built_maps']=7
 report['inner_core_correction']=verify_inner_core(layouts)
 return report


if __name__ == '__main__':
 p=argparse.ArgumentParser();p.add_argument('--built',action='store_true');p.add_argument('--report');a=p.parse_args()
 result=validate(a.built)
 if a.report:Path(a.report).write_text(json.dumps(result,indent=2)+'\n')
 print('QA10 seven lighthouse maps: all interactions/physical cells/behaviors preserved; private native art bounds/layers PASS')
