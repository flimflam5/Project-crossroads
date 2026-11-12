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
 return report


if __name__ == '__main__':
 p=argparse.ArgumentParser();p.add_argument('--built',action='store_true');p.add_argument('--report');a=p.parse_args()
 result=validate(a.built)
 if a.report:Path(a.report).write_text(json.dumps(result,indent=2)+'\n')
 print('QA10 seven lighthouse maps: all interactions/physical cells/behaviors preserved; private native art bounds/layers PASS')
