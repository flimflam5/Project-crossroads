#!/usr/bin/env python3
"""Independent HGSS S.S. Aqua geometry, IDs, exits and resource regressions.

This validator reads the SHA-pinned reference facts and the actual native map,
C-resource and event outputs. It never imports the ship writer. Source checks
are structural evidence, not visual acceptance or a replacement for controller
movement/Save/Continue on the delivered ROM.
"""
from __future__ import annotations
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
import re
import shutil
import struct
import subprocess
from PIL import Image

R = Path(__file__).resolve().parents[2]
BASE = '285cfa4ebddcb390a8a5bde6116748cbb5eaba6b'
FACTS = 'crossroads/hgss/qa10/ss-aqua-geometry.json'
FACTS_SHA256 = 'a63af8054cf30e5b7724e7831e4d8d79d07d866b5522d3d03d1819123c09de07'
# Names/order and public counts were derived independently from the selected
# pret HGSS source permissions and exact event exits before writing native maps.
SPECS = (
 ('SSAqua_1F', 'MAP_SS_AQUA_1F', (57, 21), 500, 2),
 ('SSAqua_CaptainRoom', 'MAP_SS_AQUA_CAPTAIN_ROOM', (14, 13), 89, 1),
 ('SSAqua_SoutheastCabins', 'MAP_SS_AQUA_1F_SOUTHEAST_ROOMS', (28, 13), 187, 2),
 ('SSAqua_SouthwestCabins', 'MAP_SS_AQUA_1F_SOUTHWEST_ROOMS', (28, 13), 201, 2),
 ('SSAqua_NortheastCabins', 'MAP_SS_AQUA_1F_NORTHEAST_ROOMS', (28, 13), 186, 2),
 ('SSAqua_NorthwestCabins', 'MAP_SS_AQUA_1F_NORTHWEST_ROOMS', (28, 13), 192, 2),
 ('SSAqua_B1F', 'MAP_SS_AQUA_B1F', (57, 21), 627, 1),
)
SOURCE_TO_NATIVE = {source: name for name, source, *_ in SPECS}
MAP_IDS = {
 'SSAqua_1F': 'MAP_SS_AQUA_1F',
 'SSAqua_CaptainRoom': 'MAP_SS_AQUA_CAPTAIN_ROOM',
 'SSAqua_SoutheastCabins': 'MAP_SS_AQUA_SOUTHEAST_CABINS',
 'SSAqua_SouthwestCabins': 'MAP_SS_AQUA_SOUTHWEST_CABINS',
 'SSAqua_NortheastCabins': 'MAP_SS_AQUA_NORTHEAST_CABINS',
 'SSAqua_NorthwestCabins': 'MAP_SS_AQUA_NORTHWEST_CABINS',
 'SSAqua_B1F': 'MAP_SS_AQUA_B1F',
}
PRESERVED_PATHS = (
 'include/global.h', 'include/global.fieldmap.h', 'include/pokemon.h',
 'include/fieldmap.h', 'include/save.h', 'include/config/save.h',
 'include/constants/vars.h', 'include/constants/flags.h',
 'include/constants/event_objects.h', 'include/constants/opponents.h',
 'include/constants/species.h', 'src/data/region_map/region_map_sections.json',
 'src/data/heal_locations.json',
 'crossroads/scripts/starter_rescue.inc', 'crossroads/scripts/prologue.inc',
 'crossroads/scripts/olivine.inc', 'crossroads/scripts/olivine_interiors.inc',
)
ADDITIONS = ('OlivineCity_Residence', 'OlivineCity_NeighborHouse',
             'OlivineCity_SilphOffice', 'OlivineCity_HarborOffice')


# Independently reviewed against the complete HGSS room mosaics: model collision
# is distinct from the source permission plane. These literal native footprints
# name actual solid bed/cabinet/table/chair bodies, never an exception rectangle.
MODEL_BODIES = {
 'SSAqua_1F': [(42,2,3,2,'north control bank'),(48,2,3,2,'north control bank')],
 'SSAqua_CaptainRoom': [(1,3,2,3,'captain berth')],
 'SSAqua_SoutheastCabins': [(25,2,2,2,'cabin sink'),(15,3,2,3,'east cabin berth'),(6,9,2,3,'west cabin twin berth'),(10,9,2,3,'west cabin twin berth')]+[(x,y,1,1,'four dining stools')for x in(20,24)for y in(7,10)],
 'SSAqua_SouthwestCabins': [(1,3,2,3,'blue cabin berth'),(22,6,3,3,'east dining table')]+[(x,y,1,1,'east dining stools')for x in(21,25)for y in(6,9)]+[(10,8,1,1,'west table stool'),(7,9,1,1,'west table stool')],
 'SSAqua_NortheastCabins': [(1,6,2,3,'west twin berth'),(1,9,2,3,'west twin berth'),(15,9,2,3,'east cabin berth')]+[(x,y,1,1,'east dining stools')for x in(19,24)for y in(6,9)],
 'SSAqua_NorthwestCabins': [(1,3,2,3,'blue cabin berth'),(19,4,2,3,'gold twin berth'),(23,4,2,3,'gold twin berth'),(15,7,3,4,'gold cabin settee'),(10,6,1,1,'blue table stool'),(5,7,1,1,'blue table stool')],
 'SSAqua_B1F': [(x,y,2,3,'six crew berths')for x in(9,13,17)for y in(4,8)]+[(x,y,1,1,'six galley stools')for x in(31,35)for y in(6,8,10)]+[(54,2,3,2,'engine control bank')],
}
OPEN_CLEARANCES = {
 'SSAqua_1F': {(14,8),(20,8),(31,8),(37,8),(50,15)},
 'SSAqua_CaptainRoom': set(),
 'SSAqua_SoutheastCabins': {(10,2),(24,2)},
 'SSAqua_SouthwestCabins': {(10,2),(24,2)},
 'SSAqua_NortheastCabins': set(),
 'SSAqua_NorthwestCabins': set(),
 'SSAqua_B1F': {(25,3),(25,4)},
}

# Literal independently reviewed second-leaf destinations. This catches a
# visible hatch that reaches the wrong cabin despite an otherwise connected graph.
ALIASES = {
 'SSAqua_1F': {
  12:(25,19,'OlivineCity_PortQuay',5),13:(22,19,'OlivineCity_PortQuay',4),
  14:(23,19,'OlivineCity_PortQuay',4),15:(26,19,'OlivineCity_PortQuay',5),
  16:(42,8,'SSAqua_B1F',2),
  17:(14,14,'SSAqua_SouthwestCabins',2),18:(20,14,'SSAqua_SouthwestCabins',3),
  19:(31,14,'SSAqua_SoutheastCabins',2),20:(37,14,'SSAqua_SoutheastCabins',3),
  21:(14,8,'SSAqua_NorthwestCabins',2),22:(20,8,'SSAqua_NorthwestCabins',3),
  23:(31,8,'SSAqua_NortheastCabins',2),24:(37,8,'SSAqua_NortheastCabins',3),
  25:(50,15,'SSAqua_CaptainRoom',1),26:(43,9,'SSAqua_B1F',3),
  27:(43,8,'SSAqua_B1F',4),28:(25,3,'SSAqua_B1F',5),
 },
 'SSAqua_CaptainRoom': {1:(10,11,'SSAqua_1F',25)},
 'SSAqua_SoutheastCabins': {2:(10,2,'SSAqua_1F',19),3:(24,2,'SSAqua_1F',20)},
 'SSAqua_SouthwestCabins': {2:(10,2,'SSAqua_1F',17),3:(24,2,'SSAqua_1F',18)},
 'SSAqua_NortheastCabins': {2:(10,11,'SSAqua_1F',23),3:(24,11,'SSAqua_1F',24)},
 'SSAqua_NorthwestCabins': {2:(10,11,'SSAqua_1F',21),3:(24,11,'SSAqua_1F',22)},
 'SSAqua_B1F': {3:(43,9,'SSAqua_1F',26),4:(43,8,'SSAqua_1F',27),5:(25,3,'SSAqua_1F',28)},
}


def expected_projection(name, source_public):
 bodies={(x+dx,y+dy)for x,y,w,h,reason in MODEL_BODIES[name]for dx in range(w)for dy in range(h)}
 opened=OPEN_CLEARANCES[name]
 assert not bodies&opened,('A named model body overlaps a reviewed hatch clearance',name)
 return(source_public-bodies)|opened,bodies


def load(path):
 return json.loads((R / path).read_text())


def old_bytes(path):
 return subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=R)


def old_json(path):
 return json.loads(old_bytes(path))


def words(path):
 b = (R / path).read_bytes()
 assert len(b) % 2 == 0, ('Odd native map/metatile byte count', path)
 return struct.unpack('<' + str(len(b) // 2) + 'H', b)


def neighbors(point):
 x, y = point
 return ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1))


def components(points):
 remaining = set(points)
 result = []
 while remaining:
  start = remaining.pop(); seen = {start}; todo = deque([start])
  while todo:
   for point in neighbors(todo.popleft()):
    if point in remaining:
     remaining.remove(point); seen.add(point); todo.append(point)
  result.append(seen)
 return sorted(result, key=lambda c: min(c))


def source_floor(facts):
 """Flood only floor reachable from actual source exits, excluding blank padding."""
 cols, rows = facts['matrix_dimensions']; permissions = {}
 assert len(facts['chunks']) == cols * rows
 for i, chunk in enumerate(facts['chunks']):
  assert len(chunk['permissions']) == 1024
  ox, oy = i % cols * 32, i // cols * 32
  for j, value in enumerate(chunk['permissions']):
   permissions[ox + j % 32, oy + j // 32] = value
 seeds = {(w['x'], w['z']) for w in facts['warps']}
 # HGSS north-facing door seeds carry0x8069: the solid model threshold
 # is still an actual animated exit. Include exact event seeds, never every
 # blocked cell with that behavior.
 assert all(p in permissions for p in seeds)
 seen = set(seeds); todo = deque(seeds)
 while todo:
  for point in neighbors(todo.popleft()):
   if point not in seen and point in permissions and not permissions[point] & 0x8000:
    seen.add(point); todo.append(point)
 return seen, permissions


def assert_prefix(current, prior, label):
 assert current[:len(prior)] == prior, ('Existing ordinal prefix changed', label)


def assert_public(name, actual, expected):
 assert actual == expected, ('Dropped source floor or invented padding access', name, sorted(expected-actual), sorted(actual-expected))


def preservation():
 groups = load('data/maps/map_groups.json'); prior = old_json('data/maps/map_groups.json')
 assert groups['group_order'] == prior['group_order'], 'Map group ordinals changed'
 for name in prior['group_order']:
  assert_prefix(groups[name], prior[name], name)
 before = old_json('data/layouts/layouts.json')['layouts']
 now = load('data/layouts/layouts.json')['layouts']
 assert [v['id'] for v in now[:len(before)]] == [v['id'] for v in before], 'Existing layout IDs moved'
 assert len({v['id'] for v in now}) == len(now), 'Duplicate layout ID'
 for path in PRESERVED_PATHS:
  assert (R / path).read_bytes() == old_bytes(path), ('Save/engine/starter contract changed', path)
 old_layouts = {v['id']: v for v in before}; current_layouts = {v['id']: v for v in now}
 for name in ADDITIONS:
  path = f'data/maps/{name}/map.json'; was = old_json(path); m = load(path)
  assert m == was, ('Accepted Black Ledger interior event/header changed', name)
  for key in ('blockdata_filepath', 'border_filepath'):
   path = current_layouts[m['layout']][key]
   assert path == old_layouts[was['layout']][key]
   assert (R / path).read_bytes() == old_bytes(path), ('Accepted Black Ledger room changed', name, key)
  path = f'data/maps/{name}/scripts.inc'
  assert (R / path).read_bytes() == old_bytes(path), ('Accepted room script changed', name)
 return {'baseline': BASE, 'existing_map_ids_preserved': True,
         'existing_layout_ids_preserved': True, 'critical_files_exact': list(PRESERVED_PATHS),
         'accepted_original_rooms_exact': list(ADDITIONS)}


def native_context():
 groups = load('data/maps/map_groups.json')
 names = groups['gMapGroup_CrossroadsOlivine'] + groups['gMapGroup_CrossroadsJohtoExpansion']
 maps = {n: load(f'data/maps/{n}/map.json') for n in names}
 layouts = {v['id']: v for v in load('data/layouts/layouts.json')['layouts']}
 return groups, maps, layouts


def script_body(name):
 return (R / f'data/maps/{name}/scripts.inc').read_text()


def check_no_story(maps):
 included = (R / 'data/event_scripts.s').read_text(); labels = set(); text = ''
 for name, *_ in SPECS:
  m = maps[name]; path = f'data/maps/{name}/scripts.inc'
  assert path in included, ('New native map script omitted', name)
  body = script_body(name); text += '\n' + body
  assert m['coord_events'] == [], ('Unreviewed automatic story trigger', name)
  assert len(m['object_events']) <= 16
  for actor in m['object_events']:
   assert actor.get('trainer_type') == 'TRAINER_TYPE_NONE', ('Unapproved ship trainer', name, actor)
   assert str(actor.get('flag', '0')) == '0', ('Story-hidden ship actor', name, actor)
   labels.add(actor['script'])
  labels.update(e['script'] for e in m['bg_events'])
 # New helpers may be included in a single ship-only script file. Only inspect
 # the exact file(s) defining the new labels, not all legacy game story scripts.
 for p in (R / 'crossroads/scripts').glob('*.inc'):
  body = p.read_text()
  if any(re.search(r'^' + re.escape(label) + r'::?', body, re.M) for label in labels):
   assert str(p.relative_to(R)) in included, ('Ambient ship script not linked', p)
   text += '\n' + body
 for opcode in ('givemon', 'giveitem', 'setflag', 'clearflag', 'setvar', 'addvar',
                'subvar', 'trainerbattle', 'setdynamicwarp', 'callnative', 'special'):
  assert not re.search(r'^\s*' + opcode + r'\b', text, re.M), ('Unapproved progression opcode in physical ship', opcode)
 assert not re.search(r'^\s*(?:warp|setwarp|setdynamicwarp)\s+(?:MAP_SS_AQUA_VERMILION_PORT\w*|MAP_VERMILION\w*)\b',text,re.M), 'Unapproved new destination'
 for label in labels:
  assert re.search(r'^' + re.escape(label) + r'::?', text, re.M), ('Missing ship interaction', label)
 return {'no_new_story_trainer_reward_or_departure_opcodes': True,
         'linked_ambient_labels': sorted(labels)}


def resources(layout, cells):
 # These helpers resolve actual C pointers/palette aliases and compose the
 # field_camera layer semantics; they contain no ship-generator expectations.
 from validate_city_graphics_limits import resource
 from validate_city_ground_layers import side
 primary, secondary = [side(layout[key]) for key in ('primary_tileset', 'secondary_tileset')]
 for symbol in (layout['primary_tileset'], layout['secondary_tileset']):resource(symbol)
 for pool in (primary, secondary):
  assert len(pool[0]) == len(pool[1]) * 8 and len(pool[1]) <= 512
  assert pool[2].mode == 'P' and pool[2].size == (128, 256) and max(pool[2].tobytes()) < 16
 cache = {}
 def glyph(word):
  n = word & 1023; bank = word >> 12; assert bank < 13, ('Unloaded map palette bank', bank)
  im = (primary, secondary)[n >= 512][2]; i = n % 512
  tile = im.crop((i % 16 * 8, i // 16 * 8, i % 16 * 8 + 8, i // 16 * 8 + 8))
  if word & 0x400:tile = tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if word & 0x800:tile = tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  palette = (primary, secondary)[bank >= 6][3][bank]
  return tuple(palette[v] if v else None for v in tile.tobytes())
 for word in cells:
  n = word & 1023
  if n not in cache:
   pool = (primary, secondary)[n >= 512]; i = n % 512
   assert i < len(pool[1]), ('Unallocated map metatile', n)
   refs = pool[0][i * 8:i * 8 + 8]; assert len(refs) == 8
   layer = pool[1][i] >> 12; assert layer in (0, 1, 2), ('Unsupported metatile layer', n, layer)
   bottom = sum((glyph(v) for v in refs[:4]), ()); top = sum((glyph(v) for v in refs[4:]), ())
   backdrop = primary[3][0][0]
   filler = glyph(0x3014) * 4 if layer == 0 else (backdrop,) * 256
   pixels = tuple(t if t is not None else b if b is not None else f if f is not None else backdrop for b,t,f in zip(bottom,top,filler))
   assert (31, 0, 31) not in pixels, ('Composed debug magenta', n)
   cache[n] = (layer, sum(v is not None for v in bottom), sum(v is not None for v in top))
  layer, bottom, top = cache[n]
  if not word & 0xc00 and word >> 12 in (1, 3) and layer in (0, 2):
   assert not (bottom == 0 and top), ('Public floor art is in foreground above Joe', n)
 return {'map_cells': len(cells), 'distinct_checked_metatiles': len(cache), 'native_palette_and_layer_checks': True}


def validate(built=False, preservation_only=False):
 report = {'preservation': preservation(), 'maps': []}
 if preservation_only:return report
 raw_facts = (R / FACTS).read_bytes(); assert hashlib.sha256(raw_facts).hexdigest() == FACTS_SHA256, 'Selected HGSS source facts changed'
 facts = json.loads(raw_facts); groups, maps, layouts = native_context()
 old_group = old_json('data/maps/map_groups.json')['gMapGroup_CrossroadsJohtoExpansion']; start = len(old_group)
 assert groups['gMapGroup_CrossroadsJohtoExpansion'][start:start+7] == [s[0] for s in SPECS], 'Seven ship maps must append in fixed order'
 assert len(groups['gMapGroup_CrossroadsJohtoExpansion']) <= 127
 ids = {v['id']: n for n, v in maps.items()}; linked = (R / 'data/event_scripts.s').read_text()
 native_components = {}; native_public = {}
 for name, source, size, count, component_count in SPECS:
  assert name in maps, ('Missing physical ship map', name)
  m = maps[name]; layout = layouts[m['layout']]
  assert m['id'] == MAP_IDS[name] and (layout['width'], layout['height']) == size
  assert m['region'] == 'REGION_HOENN' and m['region_map_section'] == 'MAPSEC_OLIVINE_CITY'
  assert m['connections'] in (None, []), ('Ship interior must use documented doors/stairs', name)
  source_public, permissions = source_floor(facts[source]); assert len(source_public) == count
  assert len(components(source_public)) == component_count, ('Source component extraction mismatch', name)
  raw = words(layout['blockdata_filepath']); w, h = size; assert len(raw) == w*h
  public = {(i % w, i // w) for i, v in enumerate(raw) if not v & 0xc00 and v >> 12 == 3}
  # Native animated doors may retain their collision flag. Other blocked
  # fake warps cannot be counted as public floor.
  from validate_city_ground_layers import side
  pools = [side(layout[k]) for k in ('primary_tileset', 'secondary_tileset')]
  for e in m['warp_events']:
   x,y=e['x'],e['y']; cell=raw[y*w+x]; tile=cell&1023
   attr=pools[tile>=512][1][tile%512]&255
   assert attr in (0x60,0x61,0x62,0x63,0x64,0x65,0x66,0x67,0x68,0x69), ('Inert ship door or stair',name,e,hex(attr))
   if cell&0xc00:
    assert attr in (0x60,0x69), ('Solid nonanimated ship threshold',name,e,hex(attr))
    public.add((x,y))
  # Exact native model-body and two-leaf hatch projections were independently
  # reviewed against the complete HGSS mosaics; all other source floor remains.
  expected_public,model_bodies=expected_projection(name,source_public)
  assert_public(name, public, expected_public)
  assert all(raw[y*w+x]&0xc00 for x,y in model_bodies),('Visible model body is pass-through',name)
  assert all(not raw[y*w+x]&0xc00 for x,y in OPEN_CLEARANCES[name]),('Visible second hatch leaf/stair landing blocked',name)
  native_public[name] = public
  actors = {(o['x'], o['y']) for o in m['object_events']}; assert len(actors) == len(m['object_events'])
  assert actors <= public, ('Actor in wall or blank padding', name, actors-public)
  native_components[name] = components(public-actors)
  doors = {(e['x'], e['y']) for e in m['warp_events']}; assert len(doors) == len(m['warp_events']), ('Duplicate overlapping active native warp', name)
  assert doors <= public, ('Door in wall/void', name, doors-public)
  for component in components(public-actors):
   assert component & doors, ('Furniture/NPC strands public floor without any exit', name, sorted(component))
  # An active threshold cannot be used as an ordinary connecting floor to
  # conceal an isolated pocket. Every remaining component needs its own
  # immediate door access, as well as the later global ship-to-dock graph.
  for component in components(public-actors-doors):
   assert any(set(neighbors(point))&doors for point in component), ('Floor pocket escapes only by walking through an active threshold',name,sorted(component))
  expected_warps = facts[source]['warps'][:12] if name == 'SSAqua_1F' else facts[source]['warps']
  assert len(m['warp_events']) == len(expected_warps)+len(ALIASES[name]), ('Dropped canonical door or unreviewed extra warp',name)
  for i,(x,y,dest,index)in ALIASES[name].items():
   assert m['warp_events'][i]==dict(x=x,y=y,elevation=0,dest_map=maps[dest]['id'],dest_warp_id=str(index)), ('Second visible leaf has wrong endpoint',name,i,m['warp_events'][i])
  for i, e in enumerate(expected_warps):
   actual = m['warp_events'][i]
   assert (actual['x'], actual['y']) == (e['x'], e['z']), ('Source warp ordinal/coordinate moved', name, i, actual)
   if e['header'] == 'MAP_SS_AQUA_OLIVINE_PORT_EXTERIOR':
    assert i == 0 and actual['dest_map'] == maps['OlivineCity_PortQuay']['id'] and int(actual['dest_warp_id']) == 4
   else:
    expected_name = SOURCE_TO_NATIVE[e['header']]
    assert actual['dest_map'] == maps[expected_name]['id'] and int(actual['dest_warp_id']) == e['anchor'], ('Source warp destination/anchor changed', name, i, actual)
  for i, e in enumerate(m['warp_events']):
   assert e['dest_map'] in ids and e['dest_map'] != 'MAP_DYNAMIC', ('Missing or synthetic destination', name, i, e)
   dest = maps[ids[e['dest_map']]]; j = int(e['dest_warp_id']); assert 0 <= j < len(dest['warp_events'])
   assert dest['warp_events'][j]['dest_map'] == m['id'], ('No reciprocal destination map', name, i, e)
  assert f'data/maps/{name}/scripts.inc' in linked
  layer = resources(layout, list(raw)+list(words(layout['border_filepath'])))
  report['maps'].append({'map': name, 'source': source, 'dimensions': size,
                         'source_public_floor_cells': count, 'native_projected_public_cells':len(expected_public), 'named_model_body_cells':len(model_bodies), 'named_open_clearances':sorted(OPEN_CLEARANCES[name]), 'components': component_count,
                         'native_warps': len(m['warp_events']), 'resources': layer})
 # A map-name graph alone misses the two separate1F components and eight
 # separate cabins. Build directed component edges from actual native warps;
 # every occupied/public component must have a route back to the Olivine dock.
 component_ids = {(name,point):(name,i) for name,parts in native_components.items() for i,part in enumerate(parts) for point in part}
 edges = {node:set() for node in component_ids.values()}; dock=('OlivineDock',0); edges[dock]=set()
 for name,*_ in SPECS:
  for event in maps[name]['warp_events']:
   start_node=component_ids[name,(event['x'],event['y'])]
   dest_name=ids[event['dest_map']]
   if dest_name=='OlivineCity_PortQuay':edges[start_node].add(dock);continue
   assert dest_name in native_components,('Unapproved ship destination',name,event)
   arrival=maps[dest_name]['warp_events'][int(event['dest_warp_id'])]
   point=arrival['x'],arrival['y'];assert (dest_name,point)in component_ids,('Arrival obstructed by an actor or wall',name,event,point)
   edges[start_node].add(component_ids[dest_name,point])
 quay=maps['OlivineCity_PortQuay']
 for event in quay['warp_events']:
  dest_name=ids[event['dest_map']]
  if dest_name not in native_components:continue
  assert dest_name=='SSAqua_1F',('Boarding skips directly into a cabin/lower deck',event)
  arrival=maps[dest_name]['warp_events'][int(event['dest_warp_id'])]
  edges[dock].add(component_ids[dest_name,(arrival['x'],arrival['y'])])
 assert edges[dock], 'Ship has exits but no physical dock boarding warp'
 def reach(start, graph):
  seen={start};todo=deque([start])
  while todo:
   for node in graph[todo.popleft()]:
    if node not in seen:seen.add(node);todo.append(node)
  return seen
 reachable=reach(dock,edges);assert reachable==set(edges),('Disconnected physical ship component',set(edges)-reachable)
 reverse={node:set() for node in edges}
 for start,targets in edges.items():
  for target in targets:reverse[target].add(start)
 returnable=reach(dock,reverse);assert returnable==set(edges),('Ship component cannot return to Olivine',set(edges)-returnable)
 report['component_graph']={'ship_components':len(edges)-1,'every_component_boardable_and_returnable':True}
 report['scripts'] = check_no_story(maps)
 if built:
  nm = shutil.which('arm-none-eabi-nm') or '/workspace/toolchain/root/usr/bin/arm-none-eabi-nm'
  symbols = {p[2]: int(p[0],16) for line in subprocess.check_output([nm,'-an',str(R/'pokeemerald.elf')],text=True).splitlines() if len(p:=line.split()) == 3}
  rom = (R/'pokeemerald.gba').read_bytes(); headers=(R/'data/maps/headers.inc').read_text(); table=(R/'data/maps/groups.inc').read_text()
  for name, *_ in SPECS:
   m=maps[name]; layout=layouts[m['layout']]; symbol=layout['name']+'_Blockdata'
   assert f'data/maps/{name}/header.inc' in headers and re.search(r'^\s*\.4byte '+re.escape(name)+r'\s*$',table,re.M), ('Ship map omitted by Emerald filter', name)
   assert symbol in symbols; data=(R/layout['blockdata_filepath']).read_bytes(); offset=symbols[symbol]-0x08000000
   assert rom[offset:offset+len(data)] == data, ('Stale compiled ship floor', name)
  report['built_maps'] = 7
 return report


def self_test():
 raw=(R/FACTS).read_bytes();assert hashlib.sha256(raw).hexdigest()==FACTS_SHA256
 facts=json.loads(raw);negative=0
 def reject(action):
  nonlocal negative
  try:action()
  except AssertionError:negative+=1;return
  raise AssertionError('Negative control was incorrectly accepted')
 groups=old_json('data/maps/map_groups.json');prior=groups['gMapGroup_CrossroadsJohtoExpansion']
 assert_prefix(prior+['example_new_map'],prior,'positive append')
 reordered=list(prior);reordered[0],reordered[1]=reordered[1],reordered[0]
 reject(lambda:assert_prefix(reordered,prior,'negative moved ID'))
 for name,source,size,count,number in SPECS:
  public,_=source_floor(facts[source]);assert len(public)==count and len(components(public))==number
  projected,_=expected_projection(name,public)
  assert_public(name,set(projected),projected)
  missing=set(projected);missing.remove(next(iter(missing)))
  reject(lambda:assert_public(name,missing,projected))
  extra=set(projected);extra.add((size[0]-1,size[1]-1))
  reject(lambda:assert_public(name,extra,projected))
 assert negative==15
 return {'positive_source_maps':7,'negative_controls_rejected':negative,'method':'In-memory corruption only; no native source/map/ROM mutation'}


if __name__ == '__main__':
 p=argparse.ArgumentParser();p.add_argument('--built',action='store_true');p.add_argument('--preservation-only',action='store_true');p.add_argument('--self-test',action='store_true');p.add_argument('--report');a=p.parse_args()
 report=self_test() if a.self_test else validate(a.built,a.preservation_only)
 if a.report:Path(a.report).write_text(json.dumps(report,indent=2)+'\n')
 print('QA10 source-map/ID negative controls: PASS' if a.self_test else 'QA10 immutable save/ID/addition preservation'+('' if a.preservation_only else ', all7 source-shaped Aqua maps/exits/resources')+': PASS')
