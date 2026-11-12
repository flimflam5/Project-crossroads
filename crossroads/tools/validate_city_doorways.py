#!/usr/bin/env python3
"""Independent visible-threshold contracts; complements controller segment trials."""
import json,re,struct
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def load(p):return json.loads((R/p).read_text())
ls={l['id']:l for l in load('data/layouts/layouts.json')['layouts']}
headers=(R/'src/data/tilesets/headers.h').read_text();met=(R/'src/data/tilesets/metatiles.h').read_text()
files=dict(re.findall(r'const u16 (gMetatileAttributes_\w+)\[\] = INCBIN_U16\("([^" ]+)"\)',met));attrs={}
for name,body in re.findall(r'const struct Tileset (gTileset_\w+)\s*=\s*\{([^}]+)\}',headers,re.S):
 m=re.search(r'\.metatileAttributes\s*=\s*(\w+)',body)
 if m and m[1] in files:
  b=(R/files[m[1]]).read_bytes();attrs[name]=struct.unpack('<'+str(len(b)//2)+'H',b)
groups=load('data/maps/map_groups.json');names=groups['gMapGroup_CrossroadsOlivine']+groups['gMapGroup_CrossroadsJohtoExpansion'];maps={n:load(f'data/maps/{n}/map.json') for n in names};ids={m['id']:n for n,m in maps.items()};count=0
manifest='crossroads/hgss/doorways-qa10.json' if (R/'crossroads/hgss/doorways-qa10.json').exists() else 'crossroads/hgss/doorways-qa09.json' if (R/'crossroads/hgss/authoring/OlivineCity.json').exists() else 'crossroads/hgss/doorways-qa08.json'
for group in load(manifest)['groups']:
 for side in ['outside','inside']:
  src=group[side];n=src['map'];m=maps[n];other=group['inside' if side=='outside' else 'outside']['map'];l=ls[m['layout']];w,h=l['width'],l['height'];raw=struct.unpack('<'+str(w*h)+'H',(R/l['blockdata_filepath']).read_bytes())
  ax,ay=src['anchor'];assert 0<=ax<w and 0<=ay<h and not raw[ay*w+ax]&0xc00 and raw[ay*w+ax]>>12==3,(n,'Staging anchor is not dry public floor',src['anchor'])
  assert not any(o['x']==ax and o['y']==ay for o in m['object_events']),(n,'Staging anchor is occupied by an NPC',src['anchor'])
  for x,y in src['segments']:
   events=[e for e in m['warp_events'] if (e['x'],e['y'])==(x,y)]
   assert len(events)==1,(n,'Visible threshold missing or duplicated',x,y)
   e=events[0];assert e['dest_map']==maps[other]['id'],(n,'Wrong segment destination',e)
   tile=raw[y*w+x]
   at=attrs[l['primary_tileset'] if tile&1023<512 else l['secondary_tileset']][(tile&1023)%512]&255
   # A native animated closed door starts its opening from the tile in front;
   # its closed leaf is solid. Open thresholds and horizontal aisles may not be.
   assert not tile&0xc00 or at==0x69,(n,'Visible open threshold blocked',x,y)
   assert at in [0x60,0x61,0x65,0x69] or at==0 and any(q['x']==x and q['y']==y and re.fullmatch(r'Hgss_(West|East)(City|Route)GateEnter[012]',q['script']) for q in m['coord_events']),(n,'Inert opening',x,y,at)
   back=maps[other]['warp_events'][int(e['dest_warp_id'])];assert back['dest_map']==m['id'],(n,'No reciprocal return',e)
   dst=group['inside' if side=='outside' else 'outside']
   assert [back['x'],back['y']] in dst.get('arrivals',dst['segments']),(n,'Arrival does not match outside landing',e,back)
   count+=1
assert count>=75,'Door inventory unexpectedly shrank'
print('Explicit city visible doorway segments, unblocked thresholds, native behavior/coordinate scripts and reciprocal arrivals: PASS',count,'segments. Controller coverage is separate.')
