#!/usr/bin/env python3
"""HGSS reconstruction stage: preserve IDs, prove buffer/graphics/exit invariants.

Replaces exact old Ecruteak layout/coordinate expectations only; this is NOT a
visual reference-match test or a claim that the missing Trail/interiors are done.
"""
import json,struct,hashlib
from pathlib import Path
from collections import deque
from hgss_connection_buffer import repair
R=Path(__file__).resolve().parents[2]
def load(p):
 value=json.loads((R/p).read_text())
 if p.startswith('data/maps/') and p.endswith('/map.json'):
  from build_eight_gym_integration import normalize_map
  value=normalize_map(p.split('/')[2],value)
  if p=='data/maps/EcruteakCity/map.json':
   # QA07 has a live authored base, including QA06's appended paired Gym door.
   # Validate the exact alias before projecting to this older 15-warp contract.
   assert value['warp_events'][15]==dict(value['warp_events'][4],x=25,dest_warp_id='1')
   value['warp_events'].pop(15)
 return value
def validate():
 from validate_eight_gyms import validate as validate_gyms
 validate_gyms()
 from build_eight_gym_integration import relocate_layout,CODES
 from hgss_tower_validation import validate_towers
 reviewed=validate_towers()
 from hgss_room_validation import validate_rooms
 from hgss_service_validation import validate_services
 from hgss_gate_validation import validate_gates
 reviewed|=validate_rooms()|validate_services()|validate_gates();reviewed_layouts={load(f'data/maps/{n}/map.json')['layout'] for n in reviewed}
 from validate_hgss_violet import validate as validate_violet
 reviewed|=validate_violet();reviewed_layouts|={load(f'data/maps/{n}/map.json')['layout'] for n in reviewed}
 baseline=load('crossroads/hgss/contracts/save-contracts.json');groups=load('data/maps/map_groups.json');layouts=load('data/layouts/layouts.json');heals=load('src/data/heal_locations.json')
 assert groups['group_order']==baseline['groups']['group_order']
 for key,old in baseline['groups'].items():
  if key=='gMapGroup_CrossroadsJohtoExpansion':assert groups[key][:len(old)]==old and groups[key][len(old):]==['EcruteakCity_BarrierStation','EcruteakCity_BarrierCorridor','BellchimeTrail','EcruteakCity_BellTower_10F','EcruteakCity_BellTower_Roof','EcruteakCity_DowsingHouse','EcruteakCity_PokemonCenter_B1F','EcruteakCity_WestGate','EcruteakCity_EastGate','VioletCity_PokemonCenter_B1F','VioletCity_WestGate','VioletCity_EastGate']
  else:assert groups[key]==old,('Map IDs reordered',key)
 assert [l['id'] for l in layouts['layouts'][:len(baseline['layouts']['layouts'])]]==[l['id'] for l in baseline['layouts']['layouts']]
 for old,new in zip(baseline['layouts']['layouts'],layouts['layouts']):
  if old['id'] in reviewed_layouts:continue # Strong reference geometry/ID contracts run above.
  if old['id']!='LAYOUT_ECRUTEAK_CITY':
   expected=old.copy();name=next((n for n in CODES if load(f'data/maps/{n}/map.json')['layout']==old['id']),None)
   if name:relocate_layout(name,expected)
   if old['id'] in ['LAYOUT_JOHTO_ROUTE37','LAYOUT_JOHTO_ROUTE38','LAYOUT_JOHTO_ROUTE42']:expected['primary_tileset']='gTileset_HgssEcruteakBuffer'
   assert expected==new,('Unrelated layout change',old['id'])
  else:assert new['width']==64 and new['height']==64 and new['primary_tileset']=='gTileset_BlGymEcruteakPrimary' and new['secondary_tileset']=='gTileset_BlGymEcruteakSecondary'
 for old,new in zip(baseline['heals']['heal_locations'],heals['heal_locations']):
  assert old['id']==new['id']
  if old['id']=='HEAL_LOCATION_ECRUTEAK_CITY':assert dict(old,x=45,y=56,respawn_x=8,respawn_y=13)==new
  elif old['id']=='HEAL_LOCATION_VIOLET_CITY':assert dict(old,x=49,y=56,respawn_x=8,respawn_y=13)==new
  else:assert old==new
 for n,digest in baseline['map_metadata_hashes'].items():
  if n in reviewed:continue
  if n not in ['EcruteakCity','JohtoRoute37','JohtoRoute38','JohtoRoute42','EcruteakCity_BellTower']:assert hashlib.sha256((json.dumps(load(f'data/maps/{n}/map.json'),indent=2)+'\n').encode()).hexdigest()==digest,('Unexpected events change',n)

 for name,direction,offset in [('JohtoRoute37','up',-25),('JohtoRoute38','right',-25),('JohtoRoute42','left',-33)]:
  expected_meta=load(f'crossroads/hgss/contracts/{name}-metadata-0.9.1.json')
  next(c for c in expected_meta['connections'] if c['direction']==direction)['offset']=offset
  actual=load(f'data/maps/{name}/map.json');actual['warp_events']=[e for e in actual['warp_events'] if e['dest_map'] not in ['MAP_ECRUTEAK_CITY_WEST_GATE','MAP_ECRUTEAK_CITY_EAST_GATE']];actual['coord_events']=[e for e in actual['coord_events'] if not e['script'].startswith('Hgss_')]
  assert actual==expected_meta,('Only canonical connection offset may change',name)
 old_city=load('crossroads/hgss/contracts/EcruteakCity-metadata-0.9.1.json');new_city=load('data/maps/EcruteakCity/map.json')
 # All preserved scripts, event IDs, graphics IDs and destinations remain pinned.
 import copy
 normalized=copy.deepcopy(new_city)
 assert len(normalized['warp_events'])==15
 normalized['warp_events']=normalized['warp_events'][:9]
 normalized['coord_events']=[] # Exact gate trigger/alias assertions run above.
 private=[dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='Hgss_PrivateResidence') for x,y in [(23,36),(35,36),(54,55)]]
 assert normalized['bg_events'][len(old_city['bg_events']):]==private
 normalized['bg_events']=normalized['bg_events'][:len(old_city['bg_events'])]
 assert normalized['warp_events'].pop()==dict(x=34,y=55,elevation=0,dest_map='MAP_ECRUTEAK_CITY_DOWSING_HOUSE',dest_warp_id='0')
 assert normalized['warp_events'].pop()==dict(new_city['warp_events'][1],x=39,y=25)
 for key in ['warp_events','object_events','bg_events']:
  assert len(normalized[key])==len(old_city[key])
  for event,old_event in zip(normalized[key],old_city[key]):event['x']=old_event['x'];event['y']=old_event['y']
 for connection,old in zip(normalized['connections'],old_city['connections']):connection['offset']=old['offset']
 normalized['warp_events'][1]['dest_map']=old_city['warp_events'][1]['dest_map'];normalized['warp_events'][1]['dest_warp_id']=old_city['warp_events'][1]['dest_warp_id']
 assert normalized==old_city,'No story/event/gameplay rewrites in city reconstruction'
 ls={l['id']:l for l in layouts['layouts']}
 for n in ['JohtoRoute38','JohtoRoute37','JohtoRoute42']:
  old=(R/f'crossroads/hgss/contracts/{n}-0.9.1.bin').read_bytes();m=load(f'data/maps/{n}/map.json');l=ls[m['layout']]
  assert (R/l['blockdata_filepath']).read_bytes()==repair(n,old,l['width'],l['height']),('Only compatible terrain buffer edits are allowed',n)
 m=load('data/maps/EcruteakCity/map.json');assert len(m['warp_events'])==15
 expected=[('MAP_ECRUTEAK_CITY_BURNED_TOWER',24,21),('MAP_ECRUTEAK_CITY_BARRIER_STATION',40,25),('MAP_ECRUTEAK_CITY_RESIDENCE',23,45),('MAP_ECRUTEAK_CITY_DANCE_THEATER',45,45),('MAP_ECRUTEAK_CITY_GYM',24,55),('MAP_ECRUTEAK_CITY_POKEMON_CENTER_1F',45,55),('MAP_ECRUTEAK_CITY_MART',53,45)]
 for e,(dest,x,y) in zip(m['warp_events'],expected):assert (e['dest_map'],e['x'],e['y'])==(dest,x,y)
 w=h=64;t=struct.unpack('<4096H',(R/'data/layouts/EcruteakCity/map.bin').read_bytes());walkable={(x,y) for y in range(h) for x in range(w) if not t[y*w+x]&0xc00 and t[y*w+x]>>12==3};q=deque([(26,27)]);seen=set(q)
 while q:
  x,y=q.popleft()
  for p in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
   if p in walkable and p not in seen:seen.add(p);q.append(p)
 assert walkable<=seen,'Old-save relocation must not land in an isolated canopy pocket'
 assert {y for y in range(h) if (0,y) in walkable}==set(range(37,40))
 assert {y for y in range(h) if (63,y) in walkable}==set(range(46,49))
 assert {x for x in range(w) if (x,63) in walkable}==set(range(38,41))
 assert not any((x,0) in walkable for x in range(w))
 for e in m['object_events']:assert (e['x'],e['y']) in seen
 assert (45,56) in seen,'Preserved heal ID needs safe updated arrival'
 art=load('crossroads/hgss/art/native-manifest.json');assert art['allocated_tiles']<=art['available_tiles']<=1024
 from PIL import Image
 from hgss_ecruteak_terrain import neutral_graphics
 old=neutral_graphics();new=Image.open(R/'data/tilesets/primary/hgss_ecruteak/tiles.png')
 for tile in art['reserved_primary_tiles']:
  x=tile%16*8;y=tile//16*8;box=x,y,x+8,y+8;assert old.crop(box).tobytes()==new.crop(box).tobytes(),('Terrain/animation tile overwritten',tile)
 print('HGSS Ecruteak stable IDs, reciprocal target positions, safe entire ground component, preserved animation slots and compatible buffers: PASS. Reference/visual completion is NOT asserted.')
if __name__=='__main__':validate()
