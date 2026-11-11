#!/usr/bin/env python3
"""Semantic room checks from HGSS source facts; compilation is not visual QA."""
import json,struct,re,subprocess
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[2]
def js(p):return json.loads((R/p).read_text())
facts=js('crossroads/hgss/canonical_events/olivine-interior-geometry.json');review=js('crossroads/hgss/olivine-room-review.json');ls={l['id']:l for l in js('data/layouts/layouts.json')['layouts']};art=js('crossroads/hgss/art/olivine-rooms/manifest.json');all_scripts='\n'.join(p.read_text() for p in (R/'crossroads/scripts').glob('*.inc'))
assert len(review)==9 and len({v['name'] for v in review})==9
for c in js('crossroads/hgss/contracts/olivine-common-services-qa08.json')['_shared_templates']:
 l=c['layout'];assert ls[l['id']]==l,'Shared Center/Mart template metadata must remain exact'
 assert (R/l['blockdata_filepath']).read_bytes()==bytes.fromhex(c['raw_hex']) and (R/l['border_filepath']).read_bytes()==bytes.fromhex(c['border_hex']),'Shared service pixels/physics remain exact'
# Existing primary city/office save IDs and nurse identity remain; new maps append.
oldmaps={n:json.loads(subprocess.check_output(['git','show','fd15124245:data/maps/'+n+'/map.json'],cwd=R,text=True)) for n in ['OlivineCity_PokemonCenter_1F','OlivineCity_Mart','OlivineCity_Gym','OlivineCity_Gym_Arena']}
for n,m in oldmaps.items():assert js(f'data/maps/{n}/map.json')['id']==m['id']
objects={};maps={};tiles={};attrs={}
# Resolve actual engine attribute pointers, including private Center/Mart aliases.
headers=(R/'src/data/tilesets/headers.h').read_text();meta_header=(R/'src/data/tilesets/metatiles.h').read_text();attr_files=dict(re.findall(r'const u16 (gMetatileAttributes_\w+)\[\] = INCBIN_U16\("([^" ]+)"\)',meta_header));attr_symbols={}
for sym,body in re.findall(r'const struct Tileset (gTileset_\w+)\s*=\s*\{([^}]+)\}',headers,re.S):
 a=re.search(r'\.metatileAttributes\s*=\s*(\w+)',body)
 if a:attr_symbols[sym]=a[1]
for r in review:
 n=r['name'];m=js(f'data/maps/{n}/map.json');maps[n]=m;l=ls[m['layout']];w,h=l['width'],l['height'];b=(R/l['blockdata_filepath']).read_bytes();assert len(b)==w*h*2;t=struct.unpack('<'+str(w*h)+'H',b);tiles[n]=(t,w,h)
 assert m['region']=='REGION_HOENN' and m['region_map_section']=='MAPSEC_OLIVINE_CITY';assert not m['coord_events'],'No new story/irreversible triggers in room content'
 positions={(o['x'],o['y']) for o in m['object_events']};objects[n]=positions;assert len(positions)==len(m['object_events'])<=16
 for e in m['object_events']:
  x,y=e['x'],e['y'];assert 0<=x<w and 0<=y<h and not t[y*w+x]&0xc00,(n,'Blocked actor',e);assert re.search(r'^'+re.escape(e['script'])+r'::',all_scripts,re.M),(n,'Unlinked ambient/service script',e)
 for e in m['warp_events']:
  x,y=e['x'],e['y'];assert 0<=x<w and 0<=y<h and not t[y*w+x]&0xc00,(n,'Blocked threshold',e)
 assert l['secondary_tileset'] in attr_symbols and attr_symbols[l['secondary_tileset']] in attr_files,(n,'Unresolved actual tileset attribute pointer');p=R/attr_files[attr_symbols[l['secondary_tileset']]];b=p.read_bytes();attrs[n]=struct.unpack('<'+str(len(b)//2)+'H',b)
 # Ordinary public flooring must never gain a warp arrow or slide behavior.
 active={(e['x'],e['y']) for e in m['warp_events']}
 for y in range(h):
  for x in range(w):
   v=t[y*w+x];mid=v&1023
   if mid>=512 and not v&0xc00 and (x,y) not in active:assert attrs[n][mid-512]&255 not in [0x61,0x62,0x63,0x64,0x65,0x66],(n,'Spurious arrow/warp ground',x,y)
 # New homes/cafe must allow every interior doorway half independently.
 if n.endswith(('House','Cafe')):
  warps=m['warp_events'];assert len(warps)==2;assert warps[1]['x']==warps[0]['x']+1 and warps[0]['y']==warps[1]['y']
  for e in warps:
   x,y=e['x'],e['y'];assert attrs[n][(t[y*w+x]&1023)-512]&255==0x65
   assert not t[(y-1)*w+x]&0xc00 and (x,y-1) not in positions,(n,'Threshold approach blocked',x,y)
  seen={(warps[0]['x'],warps[0]['y']-1)};q=deque(seen)
  while q:
   x,y=q.popleft()
   for X,Y in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
    if not(0<=X<w and 0<=Y<h) or (X,Y) in seen or (X,Y) in positions or t[Y*w+X]&0xc00:continue
    seen.add((X,Y));q.append((X,Y))
  for o in m['object_events']:
   x,y=o['x'],o['y'];reachable=False
   for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
    if (x+dx,y+dy) in seen:reachable=True
    elif (x+2*dx,y+2*dy) in seen:
     mid=t[(y+dy)*w+x+dx]&1023
     if mid>=512 and attrs[n][mid-512]&255==0x80:reachable=True
   assert reachable,(n,'No legal interaction approach/counter',o)
  assert all((e['x'],e['y']-1) in seen for e in warps)
  if n.endswith('House'):
   assert (w,h)==(11,10);assert all(t[y*w+x]&0xc00 for y in [5,6] for x in [6,7]),'Source dining-table footprint must block, not clip'
   assert len(m['object_events'])==(3 if n.endswith('_SealHouse') else 1),'Source household actor positions/count retained'
   a=art['home']['house_plant'];assert [t[y*w+9]&1023 for y in [2,3]]==[a['start'],a['start']+1] and all(t[y*w+9]&0xc00 for y in [2,3]),'Actual source0097 right-hand plant footprint'
  else:
   assert (w,h)==(14,12);assert all(t[y*w+x]&0xc00 for y in range(5,8) for x in range(3,6)),'Source cafe communal table is solid'
   for y in range(3,9):assert t[y*w+10]&0xc00 and attrs[n][(t[y*w+10]&1023)-512]&255==0x80,'Serving counter must support real over-counter talk'
   assert t[8*w+11]&0xc00 and attrs[n][(t[8*w+11]&1023)-512]&255==0x80,'Source cafe L-counter return'
   assert (9,4) in seen and (11,4) in positions and (12,8) in seen,'Real counter interaction and safe visible service aisle'
   a=art['home']['cafe_plant']
   for y in [2,9]:assert [t[(y+j)*w+1]&1023 for j in range(2)]==[a['start'],a['start']+1] and all(t[(y+j)*w+1]&0xc00 for j in range(2)),'Actual source0136 cafe plant footprints'
center=maps['OlivineCity_PokemonCenter_1F'];nurse=center['object_events'][0];assert (nurse['x'],nurse['y'],nurse['script'],nurse['local_id'])==(8,11,'Olivine_Nurse','LOCALID_OLIVINE_NURSE')
assert [(e['x'],e['y'],e['dest_warp_id']) for e in center['warp_events'][:2]]==[(8,19,'3'),(9,19,'14')]
t,w,h=tiles[center['name']]
for x,y in [(15,3),(14,14),(15,14)]:assert t[y*w+x]==0x60a and t[(y+1)*w+x]==0x612
assert center['warp_events'][2]['dest_map']==maps['OlivineCity_PokemonCenter_B1F']['id']
assert maps['OlivineCity_PokemonCenter_B1F']['warp_events'][0]['dest_warp_id']=='2'
basement=maps['OlivineCity_PokemonCenter_B1F'];t,w,h=tiles[basement['name']];assert (w,h)==(17,14) and ls[basement['layout']]['secondary_tileset']=='gTileset_HgssCenterBasement','Retain actual public source y12 floor in private basement'
for x in (4,12):assert (t[11*w+x],t[12*w+x])==(0x60a,0x612),'Actual source basement plants'
ba=js('crossroads/hgss/art/center-basement/manifest.json')['specs']
for part,x,y in [('waiting_table',2,8),('communication_terminal',15,4)]+[('yellow_stool',x,y) for x,y in [(4,8),(3,7),(5,12),(7,12),(9,12),(11,12)]]+[('blue_stool',x,y) for x,y in [(4,9),(2,7),(6,12),(10,12)]]:
 a=ba[part]
 for dy in range(a['height']):
  for dx in range(a['width']):assert t[(y+dy)*w+x+dx]==0x400|a['start']+dy*a['width']+dx,('Source-backed native basement fixture',part,x+dx,y+dy)
assert not t[12*w+8]&0xc00,'Public bottom waiting-row clearance remains open'

heal=next(v for v in js('src/data/heal_locations.json')['heal_locations'] if v['id']=='HEAL_LOCATION_OLIVINE_CITY');assert (heal['respawn_x'],heal['respawn_y'],heal['respawn_npc'])==(8,13,'LOCALID_OLIVINE_NURSE')
mart=maps['OlivineCity_Mart'];assert mart['object_events'][0]['script']=='Olivine_Clerk' and mart['object_events'][1]['script']=='Olivine_MartVisitor'
# All three pieces of the long hallway remain live in both directions.
gym=maps['OlivineCity_Gym'];arena=maps['OlivineCity_Gym_Arena'];assert [(e['x'],e['y']) for e in gym['warp_events']]==[(6,10),(7,10),(6,0),(5,0),(7,0)]
for i,j in [(2,0),(3,1),(4,2)]:assert gym['warp_events'][i]['dest_warp_id']==str(j) and arena['warp_events'][j]['dest_warp_id']==str(i)
assert arena['object_events'][0]['script']=='Area_PracticeJasmine' and arena['object_events'][1]['script']=='Area_JasmineApprentice'
for n in ['OlivineCity_Gym','OlivineCity_Gym_Arena']:
 t,w,h=tiles[n]
 for y in range(5 if n.endswith('_Arena') else 0,h if n.endswith('_Arena') else h-1):
  assert all(not t[y*w+x]&0xc00 for x in [5,6,7]),(n,'Continuous source hallway',y)
# Original office/houses are outside this generator's ownership.
assert len((R/'crossroads/hgss/contracts/olivine-center-stock-qa08.bin').read_bytes())==252
print('Olivine source-room dimensions/furniture/counter access, independent paired thresholds, nurse/PC/stairs, optional Gym corridor and stable IDs: PASS')
