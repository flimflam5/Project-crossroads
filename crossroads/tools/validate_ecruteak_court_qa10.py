#!/usr/bin/env python3
"""Independent exact39-cell art correction for HGSS's open directory court.

The owner screenshot depicts Ecruteak's genuinely vacant court beside the
Theater, not an omitted canonical building. All original signs, paths, physics,
actors, entrances, saved IDs and every cell outside this exact mask must remain.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct

from validate_ss_aqua import BASE, R, load, old_bytes, old_json, resources, words

BEFORE_SHA256 = '2b7b74952cd3efdde29ce8d6fc048d2424fcc8c7aade0512f98da17339f09d18'


def validate():
 old_map=old_json('data/maps/EcruteakCity/map.json');m=load('data/maps/EcruteakCity/map.json')
 assert m==old_map,'Art-only courtyard correction changed events/doors/header'
 layouts={v['id']:v for v in load('data/layouts/layouts.json')['layouts']};l=layouts[m['layout']]
 prior=next(v for v in old_json('data/layouts/layouts.json')['layouts']if v['id']==m['layout'])
 assert l==prior,'Art-only courtyard correction changed layout identity/pointers'
 before=old_bytes(prior['blockdata_filepath']);assert hashlib.sha256(before).hexdigest()==BEFORE_SHA256
 was=struct.unpack('<4096H',before);now=words(l['blockdata_filepath']);assert len(now)==4096
 allowed={(x,y)for y in range(42,47)for x in range(31,39)}-{(36,45)};assert len(allowed)==39
 changed=set()
 for i,(a,b)in enumerate(zip(was,now)):
  x,y=i%64,i//64
  if (x,y)not in allowed:assert a==b,('City art changed outside exact court mask',x,y,hex(a),hex(b));continue
  assert a==0x32f5,('Immutable court source cell differs',x,y,hex(a))
  col=0 if x==31 else 2 if x==38 else 1;row=0 if y==42 else 2 if y==46 else 1
  assert b==0x3000|0x3f0+row*3+col,('Wrong source-shaped soil/curb module',x,y,hex(b))
  assert a&0xfc00==b&0xfc00,('Court collision/elevation changed',x,y)
  changed.add((x,y))
 assert changed==allowed
 assert now[45*64+36]==was[45*64+36],'Directory sign replaced/removed'
 assert any(e['x']==36 and e['y']==45 and e['script']=='Ecruteak_Directory'for e in m['bg_events'])
 # Resource validator resolves actual C pointers and composition, so high IDs
 # cannot merely name missing art or place opaque soil above Joe.
 report=resources(l,list(now)+list(words(l['border_filepath'])))
 from validate_city_ground_layers import side
 secondary=side(l['secondary_tileset'])
 for n in range(0x3f0,0x3f9):
  assert secondary[1][n-512]==0x1000,('Soil/curb layer behavior differs from immutable earth',hex(n))
  assert any(secondary[0][(n-512)*8:(n-512)*8+4]),('Court ground artwork missing',hex(n))
 return {'baseline':BASE,'changed_art_cells':39,'unchanged_map_cells':4057,
         'all_physics_events_and_ids_preserved':True,'source_directory_plot_not_a_missing_building':True,
         'resources':report,'visual_acceptance':'Owner Delta review remains required'}


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--report');a=p.parse_args();result=validate()
 if a.report:Path(a.report).write_text(json.dumps(result,indent=2)+'\n')
 print('QA10 Ecruteak directory court: exact39-art-cell delta; all other cells/physics/events/IDs preserved; native layers PASS')
