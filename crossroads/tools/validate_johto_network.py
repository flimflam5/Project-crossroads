#!/usr/bin/env python3
"""Flood actual Johto tiles, doors and borders; verify IDs/services/build inclusion."""
import argparse,json,re,struct,hashlib
from collections import deque
from pathlib import Path
R=Path(__file__).resolve().parents[2]
ap=argparse.ArgumentParser();ap.add_argument('--built',action='store_true');a=ap.parse_args()
def load(p):return json.loads((R/p).read_text())
from hgss_gate_arrivals import arrivals
from hgss_olivine_validation import active as olivine_active,dynamic_pair,dynamic_destinations,extra_edges,validate_olivine_graph
arrival_only=arrivals()
groups=load('data/maps/map_groups.json');base=groups['gMapGroup_CrossroadsOlivine'];west=groups.get('gMapGroup_CrossroadsJohtoExpansion',[]);names=base+west;locations={n:(75,i) for i,n in enumerate(base)}|{n:(76,i) for i,n in enumerate(west)};manifest=load('crossroads/johto/manifest.json')
for preserved,digest in manifest.get('preserved_sources',{}).items():
 assert hashlib.sha256((R/preserved).read_bytes()).hexdigest()==digest,('Accepted source changed',preserved)
assert names[:37]==[p['name'] for p in manifest['existing']]
assert groups['group_order'].index('gMapGroup_CrossroadsOlivine')==75
if west:assert groups['group_order'].index('gMapGroup_CrossroadsJohtoExpansion')==76
assert len(base)<=127 and len(west)<=127, 'Signed warp indices must avoid reserved dynamic value 127'
maps={n:load(f'data/maps/{n}/map.json') for n in names};ids={m['id']:n for n,m in maps.items()}
layouts={l['id']:l for l in load('data/layouts/layouts.json')['layouts']};raw={};sizes={};attrs={};actors={}
headers=(R/'src/data/tilesets/headers.h').read_text();met=(R/'src/data/tilesets/metatiles.h').read_text()
paths=dict(re.findall(r'const u16 (gMetatileAttributes_\w+)\[\] = INCBIN_U16\("([^"]+)"\)',met));lookup={}
for name,body in re.findall(r'const struct Tileset (gTileset_\w+)\s*=\s*\{([^}]+)\}',headers,re.S):
 match=re.search(r'\.metatileAttributes\s*=\s*(\w+)',body)
 if match and match[1] in paths:
  data=(R/paths[match[1]]).read_bytes();lookup[name]=struct.unpack('<'+str(len(data)//2)+'H',data)
inc=(R/'data/event_scripts.s').read_text();scripts='\n'.join(p.read_text() for p in (R/'crossroads/scripts').glob('*.inc'))+'\n'+'\n'.join((R/f'data/maps/{n}/scripts.inc').read_text() for n in names)
for n,m in maps.items():
 assert m['id'] in ids and m['region']=='REGION_HOENN'
 assert f'data/maps/{n}/scripts.inc' in inc
 l=layouts[m['layout']];w,h=l['width'],l['height'];sizes[n]=(w,h);b=(R/l['blockdata_filepath']).read_bytes();assert len(b)==w*h*2;raw[n]=struct.unpack('<'+str(w*h)+'H',b)
 actors[n]={(o['x'],o['y']) for o in m['object_events']};assert len(actors[n])==len(m['object_events'])<=16
 for e in m['object_events']+m['bg_events']:
  assert 0<=e['x']<w and 0<=e['y']<h,(n,e)
  assert re.search(r'^'+re.escape(e['script'])+r'::?',scripts,re.M),(n,e['script'])
 for index,e in enumerate(m['warp_events']):
  assert 0<=e['x']<w and 0<=e['y']<h
  if dynamic_pair(n,index,e,maps,ids):continue # Narrowly pinned native lift; every other reciprocal check remains.
  dst=ids[e['dest_map']];num=int(e['dest_warp_id']);assert 0<=num<len(maps[dst]['warp_events'])
  assert maps[dst]['warp_events'][num]['dest_map']==m['id'],('Unpaired warp',n,e)
 for c in m['connections'] or []:
  dst=ids[c['map']];reverse={'up':'down','down':'up','left':'right','right':'left'}[c['direction']]
  assert dict(map=m['id'],direction=reverse,offset=-c['offset']) in (maps[dst]['connections'] or []),(n,c)
  dw,dh=layouts[maps[dst]['layout']]['width'],layouts[maps[dst]['layout']]['height']
  assert abs(c['offset'])<max(w,h,dw,dh),'No edge overlap'
 # Primary General water IDs are elevation one; other collide-zero terrain is walkable.
 for x,y in actors[n]:assert raw[n][y*w+x]&0xc00==0,(n,'NPC on collision',x,y)
 for e in m['warp_events']:
  t=raw[n][e['y']*w+e['x']]&1023
  at=lookup[l['primary_tileset'] if t<512 else l['secondary_tileset']]
  assert t-(512 if t>=512 else 0)<len(at),('Metatile out of bounds',n,e,t)
  if at[t-(512 if t>=512 else 0)]&255==0:
   if (n,m['warp_events'].index(e)) in arrival_only:
    entry=m['warp_events'][arrival_only[(n,m['warp_events'].index(e))]]
    assert entry['dest_map']==e['dest_map'] and entry['dest_warp_id']==e['dest_warp_id']
    assert raw[n][e['y']*w+e['x']]&0xc00==0 and not any(q['x']==e['x'] and q['y']==e['y'] for q in m['coord_events'])
    continue # Independently required return-only landing, not an entry door.
   # A neutral road portal is driven by an exact coordinate script, not a door
   # metatile. Require the actual script to warp to this same destination/index;
   # blank ordinary doors or stairs still fail. Canonical gate geometry and all
   # aliases are independently checked below by validate_gates().
   trigger=next((q for q in m['coord_events'] if (q['x'],q['y'])==(e['x'],e['y']) and q['var']=='VAR_TEMP_0' and q['var_value']=='0' and re.fullmatch(r'Hgss_(West|East)(City|Route)GateEnter[012]',q['script'])),None)
   assert trigger is not None,('Warp lost its door/stair behavior',n,e,t)
   label=re.search(r'^'+trigger['script']+r'::\n(.*?)(?=^\w+::|\Z)',scripts,re.M|re.S)
   assert label and re.search(r'^\s+warp '+e['dest_map']+r', '+re.escape(str(e['dest_warp_id']))+r'\s*$',label[1],re.M),('Coordinate portal destination mismatch',n,e,trigger)
   assert raw[n][e['y']*w+e['x']]&0xc00==0,('Blocked coordinate portal',n,e)
 # Animated doors legitimately use a collision bit; they are entered via the warp interaction.
# Connections need at least one matching-elevation seam, not a forced Surf
# animation across an unloaded map boundary.
for n,m in maps.items():
 w,h=sizes[n]
 for c in m['connections'] or []:
  dst=ids[c['map']];dw,dh=sizes[dst];d=c['direction'];matched=[]
  for t in range(w if d in ['up','down'] else h):
   x,y=(t,0) if d=='up' else (t,h-1) if d=='down' else (0,t) if d=='left' else (w-1,t)
   xx,yy=(t-c['offset'],dh-1) if d=='up' else (t-c['offset'],0) if d=='down' else (dw-1,t-c['offset']) if d=='left' else (0,t-c['offset'])
   if not(0<=xx<dw and 0<=yy<dh):continue
   left_tile,right_tile=raw[n][y*w+x],raw[dst][yy*dw+xx]
   if not (left_tile&0xc00 or right_tile&0xc00) and left_tile>>12==right_tile>>12:matched.append(t)
  assert matched,('No matching terrain/elevation across seam',n,c)
from hgss_tower_validation import validate_towers
from johto_movement import next_position
reviewed=validate_towers()
from hgss_room_validation import validate_rooms
from hgss_service_validation import validate_services
from hgss_gate_validation import validate_gates
reviewed|=validate_rooms()|validate_services()|validate_gates()
from validate_hgss_violet import validate as validate_violet
reviewed|=validate_violet()
reviewed|=validate_olivine_graph()
def behavior(n,x,y):
 w,h=sizes[n]
 if not(0<=x<w and 0<=y<h):return None
 t=raw[n][y*w+x]&1023;l=layouts[maps[n]['layout']]
 return lookup[l['primary_tileset'] if t<512 else l['secondary_tileset']][t%512]&255
# Traversal graph includes the explicitly labeled session-only survey Surf mode.
start=('OlivineCity',16,34) if olivine_active() else ('OlivineCity',12,13);q=deque([start]);seen={start}
while q:
 n,x,y=q.popleft();w,h=sizes[n];m=maps[n]
 moves=extra_edges(n,x,y)
 for dx,dy,d in [(1,0,'right'),(-1,0,'left'),(0,1,'down'),(0,-1,'up')]:
  step=next_position(x,y,dx,dy,lambda a,b:behavior(n,a,b))
  if step is None:continue
  xx,yy=step;dst=n
  if not(0<=xx<w and 0<=yy<h):
   c=next((c for c in m['connections'] or [] if c['direction']==d),None)
   if c is None:continue
   dst=ids[c['map']];dw,dh=sizes[dst]
   if d=='up':xx,yy=xx-c['offset'],dh-1
   elif d=='down':xx,yy=xx-c['offset'],0
   elif d=='left':xx,yy=dw-1,yy-c['offset']
   else:xx,yy=0,yy-c['offset']
  moves.append((dst,xx,yy))
 for index,e in enumerate(m['warp_events']):
  if (n,index) in arrival_only:continue
  if (x,y)==(e['x'],e['y']):
   dynamic=dynamic_destinations(n,e,maps)
   if dynamic is not None:moves.extend((dst,back['x'],back['y']) for dst,back in dynamic)
   else:
    dst=ids[e['dest_map']];back=maps[dst]['warp_events'][int(e['dest_warp_id'])];moves.append((dst,back['x'],back['y']))
 for dst,xx,yy in moves:
  dw,dh=sizes[dst];p=(dst,xx,yy)
  if not(0<=xx<dw and 0<=yy<dh) or p in seen or (xx,yy) in actors[dst]:continue
  t=raw[dst][yy*dw+xx]
  if t&0xc00 and not any((xx,yy)==(e['x'],e['y']) for e in maps[dst]['warp_events']):continue
  seen.add(p);q.append(p)
for n in names:
 assert any(s[0]==n for s in seen),('Unreachable map',n)
 for e in maps[n]['warp_events']:assert (n,e['x'],e['y']) in seen,('Unreachable exit',n,e)
 for e in maps[n]['object_events']+maps[n]['bg_events']:
  assert any((n,e['x']+dx,e['y']+dy) in seen for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(2,0),(-2,0),(0,2),(0,-2)]),('Unreachable interaction',n,e)
# A global warp graph can conceal a trapped cave-mouth pocket. Require local
# exits to connect without leaving/re-entering the same map through another floor.
for n,m in maps.items():
 if n in reviewed:continue # Canonical branched floors checked by exact graph and every-tile escape.
 if not m['warp_events']:continue
 w,h=sizes[n];start=(m['warp_events'][0]['x'],m['warp_events'][0]['y']);local={start};todo=deque([start]);doors={(e['x'],e['y']) for e in m['warp_events']}
 while todo:
  x,y=todo.popleft()
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   point=next_position(x,y,dx,dy,lambda a,b:behavior(n,a,b))
   if point is None:continue
   xx,yy=point
   if not(0<=xx<w and 0<=yy<h) or (xx,yy) in local or (xx,yy) in actors[n]:continue
   if raw[n][yy*w+xx]&0xc00 and (xx,yy) not in doors:continue
   local.add((xx,yy));todo.append((xx,yy))
 assert doors<=local,('Locally trapped entrance',n,doors-local)
heals=load('src/data/heal_locations.json')['heal_locations']
for h in heals:
 if h['map'] in ids:
  assert (ids[h['map']],h['x'],h['y']) in seen,('Unsafe heal',h)
  center=ids[h['respawn_map']];assert 'CableClub_OnResume' in (R/f'data/maps/{center}/scripts.inc').read_text()
  assert any(o.get('local_id')==h['respawn_npc'] for o in maps[center]['object_events'])
  assert (center,h.get('respawn_x',7),h.get('respawn_y',4)) in seen,('Unsafe nurse arrival',h)
for p in manifest['planned']:
 if p['name'] in names:assert locations[p['name']]==(p['map_group'],p['map_num']),('ID shifted',p)
ops=(R/'include/constants/opponents.h').read_text();assert '#define MAX_TRAINERS_COUNT_EMERALD 864' in ops
runtime=(R/'crossroads/scripts/johto_runtime.inc').read_text();assert all(t not in runtime for t in ['setflag','setvar VAR_CROSSROADS','givemon','giveitem'])
if a.built:
 header=(R/'data/maps/headers.inc').read_text();group=(R/'data/maps/groups.inc').read_text()
 for n in names:
  assert f'data/maps/{n}/header.inc' in header
  assert re.search(r'^\s*\.4byte '+n+r'\s*$',group,re.M)
 sec=(R/'include/constants/region_map_sections.h').read_text();values=re.findall(r'^\s*(MAPSEC_\w+),',sec,re.M)
 assert values.index('MAPSEC_NONE')==213 and len(values)==253
 assert len((R/'pokeemerald.gba').read_bytes())<=32*1024*1024
report=dict(maps=len(names),reachable_tiles=len(seen),warps=sum(len(m['warp_events']) for m in maps.values()),connections=sum(len(m['connections'] or []) for m in maps.values()),centers=sum(n.endswith('PokemonCenter_1F') for n in names),mode='structural survey-water-enabled graph; not emulator playtesting')
(R/'build').mkdir(exist_ok=True);(R/'build/johto-topology-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('Johto valid IDs, whole tile/warp/border graph, interaction access, services and safe respawns: PASS',report)

# Owner-requested persistent kit is separate from reversible survey assistance.
qa=(R/'crossroads/scripts/qa_kit.inc').read_text()
assert qa.count('givemon ')==1 and 'givemon SPECIES_PIDGEOT, 100,' in qa
assert 'move1=MOVE_FLY' in qa
assert 'goto_if_set FLAG_BLACK_LEDGER_QA_FLYER' in qa
assert 'goto_if_ge VAR_RESULT, PARTY_SIZE' in qa
assert 'goto_if_eq VAR_RESULT, MON_CANT_GIVE' in qa
assert qa.index('givemon ')<qa.index('    setflag FLAG_BLACK_LEDGER_QA_FLYER')
assert [l.strip() for l in qa.splitlines() if l.strip().startswith('setflag ')]==['setflag FLAG_SYS_B_DASH','setflag FLAG_BLACK_LEDGER_QA_FLYER']
assert 'setvar ' not in qa and 'FLAG_BADGE' not in qa
assert 'special Johto_QAKitRequested' in runtime
assert '\t.include "crossroads/scripts/qa_kit.inc"' in (R/'data/event_scripts.s').read_text()
print('Explicit QA kit: one guarded level100 flyer, shoes only, no badge/starter changes: PASS')
