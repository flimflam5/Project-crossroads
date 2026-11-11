#!/usr/bin/env python3
"""HGSS Olivine migration/doorway/service contracts, not visual acceptance.

The old48x48 blockout validator remains available for historical revisions. This
validator pins IDs to the actual QA08 B2 revision and checks the new canonical
entrances independently from the mutable facade/generator manifests.
"""
import argparse,json,re,struct,subprocess,shutil
from collections import deque
from pathlib import Path
R=Path(__file__).resolve().parents[2]
BASE='fd151242458efe5759b18650f35a5e5b2fa47e45'
def load(path):return json.loads((R/path).read_text())
def old(path):return json.loads(subprocess.check_output(['git','show',BASE+':'+path],cwd=R))
def words(path):b=(R/path).read_bytes();return struct.unpack('<'+str(len(b)//2)+'H',b)
def validate(built=False):
 from hgss_olivine_preservation import validate as validate_accepted_exteriors
 validate_accepted_exteriors()
 groups=load('data/maps/map_groups.json');prior=old('data/maps/map_groups.json')
 assert groups['group_order']==prior['group_order'],'Existing map groups must not shift'
 for name in prior['group_order']:assert groups[name][:len(prior[name])]==prior[name],('Map IDs shifted',name)
 ls=load('data/layouts/layouts.json')['layouts'];before=old('data/layouts/layouts.json')['layouts']
 assert [x['id'] for x in ls[:len(before)]]==[x['id'] for x in before],'Layout IDs shifted'
 layouts={l['id']:l for l in ls};names=groups['gMapGroup_CrossroadsOlivine']+groups['gMapGroup_CrossroadsJohtoExpansion']
 maps={n:load(f'data/maps/{n}/map.json') for n in names};ids={m['id']:n for n,m in maps.items()};city=maps['OlivineCity'];l=layouts[city['layout']]
 assert (l['width'],l['height'])==(64,64),'HGSS city footprint must retain the reference64x64 extent'
 previous_city=old('data/maps/OlivineCity/map.json')
 for field in ['id','name','layout','music','region','region_map_section','requires_flash','weather','map_type','allow_cycling','allow_escaping','allow_running','show_map_name','battle_scene']:
  assert city[field]==previous_city[field],('Unapproved city engine/story configuration change',field)
 assert city['connections']==[dict(map='MAP_JOHTO_ROUTE39',offset=12,direction='up'),dict(map='MAP_JOHTO_ROUTE40',offset=10,direction='left')]
 assert city['coord_events']==previous_city['coord_events'],'No new story triggers in the city reconstruction'
 assert len(city['object_events'])==len(previous_city['object_events'])
 for before_actor,after_actor in zip(previous_city['object_events'],city['object_events']):
  assert {k:v for k,v in after_actor.items() if k not in ['x','y']}=={k:v for k,v in before_actor.items() if k not in ['x','y']},'Accepted ambient actors/scripts must retain identity'
 for before_sign,after_sign in zip(previous_city['bg_events'],city['bg_events']):
  assert {k:v for k,v in after_sign.items() if k not in ['x','y']}=={k:v for k,v in before_sign.items() if k not in ['x','y']},'Accepted signs/scripts must retain identity'
 added_signs=city['bg_events'][len(previous_city['bg_events']):]
 assert {(e['x'],e['y']) for e in added_signs}=={(16,24),(30,18),(35,18),(8,34),(22,53)} and len(added_signs)==5,'Each new physical building sign needs its own interaction'
 assert all(e['type']=='sign' and e['elevation']==0 and e['player_facing_dir']=='BG_EVENT_PLAYER_FACING_ANY' for e in added_signs)
 expected_legacy_doors=[(8,23),(8,28),(13,14),(16,33),(29,33),(31,40),(8,40),(45,39),(14,14)]
 assert len(city['warp_events'])==16
 for i,(before_warp,position) in enumerate(zip(previous_city['warp_events'],expected_legacy_doors)):
  assert city['warp_events'][i]==dict(before_warp,x=position[0],y=position[1]),('Accepted destination/warp identity changed',i)
 tile={n:words(layouts[m['layout']]['blockdata_filepath']) for n,m in maps.items() if n.startswith('OlivineCity')}
 current=load('src/data/heal_locations.json')['heal_locations'];previous=old('src/data/heal_locations.json')['heal_locations']
 assert [h['id'] for h in current[:len(previous)]]==[h['id'] for h in previous]
 for i,h in enumerate(previous):
  if h['id']!='HEAL_LOCATION_OLIVINE_CITY':assert current[i]==h,('Unrelated heal changed',h['id'])
 heal=next(h for h in current if h['id']=='HEAL_LOCATION_OLIVINE_CITY')
 assert heal['map']=='MAP_OLIVINE_CITY' and (heal['x'],heal['y'])==(16,34)
 assert heal['respawn_map']=='MAP_OLIVINE_CITY_POKEMON_CENTER_1F' and (heal['respawn_x'],heal['respawn_y'])==(8,13)
 # Actual HGSS entrance coordinates, independently pinned from074_T26/source.
 expected={'OlivineCity_Gym':(13,14),'OlivineCity_PokemonCenter_1F':(16,33),'OlivineCity_Mart':(29,33),'OlivineCity_Lighthouse_1F':(45,39),'OlivineCity_FishingHouse':(17,23),'OlivineCity_TradeHouse':(31,17),'OlivineCity_SealHouse':(36,17),'OlivineCity_Cafe':(9,33),'OlivineCity_PortTerminal':(23,52)}
 for name,position in expected.items():
  assert name in maps,('Missing intended canonical building/interior',name)
  assert any((e['x'],e['y'])==position and e['dest_map']==maps[name]['id'] for e in city['warp_events']),('Canonical entrance absent/moved',name,position)
 for name in ['OlivineCity_Residence','OlivineCity_NeighborHouse','OlivineCity_SilphOffice','OlivineCity_HarborOffice']:
  assert name in maps and any(e['dest_map']==maps[name]['id'] for e in city['warp_events']),('Accepted Black Ledger addition removed',name)
 # Existing source actors/scripts, starter location, furniture and exits remain
 # governed by their original interior validator. This check adds exact identity.
 for name in ['OlivineCity_Residence','OlivineCity_NeighborHouse','OlivineCity_SilphOffice','OlivineCity_HarborOffice']:
  m=maps[name];previous_map=old(f'data/maps/{name}/map.json')
  for field in ['id','object_events','coord_events','bg_events']:assert m[field]==previous_map[field],('Accepted interior script/object contract changed',name,field)
  ol=next(x for x in before if x['id']==previous_map['layout']);was=subprocess.check_output(['git','show',BASE+':'+ol['blockdata_filepath']],cwd=R);now=(R/ol['blockdata_filepath']).read_bytes()
  if name in ['OlivineCity_SilphOffice','OlivineCity_HarborOffice']:
   expected=list(struct.unpack('<80H',was))
   for x in ((1,2,7,8) if name.endswith('SilphOffice') else (7,8)):expected[x]|=0x400
   assert now==struct.pack('<80H',*expected),('Only six declared ceiling-cap collision bits may change; pixels and all other tiles remain exact',name)
  else:assert now==was,('Accepted interior layout changed',name)
 allscripts='\n'.join(p.read_text() for p in (R/'crossroads/scripts').glob('*.inc'))
 linked=(R/'data/event_scripts.s').read_text();headers=(R/'data/maps/headers.inc').read_text() if built else '';table=(R/'data/maps/groups.inc').read_text() if built else ''
 for name,m in maps.items():
  if not name.startswith('OlivineCity'):continue
  assert m['region']=='REGION_HOENN' and m['region_map_section']=='MAPSEC_OLIVINE_CITY',('Emerald inclusion/met section',name)
  assert f'data/maps/{name}/scripts.inc' in linked,('Missing script include',name)
  ml=layouts[m['layout']];w,h=ml['width'],ml['height'];tt=tile[name];assert len(tt)==w*h
  actors={(e['x'],e['y']) for e in m['object_events']};assert len(actors)==len(m['object_events'])<=16,(name,'Overlapping/too many actors')
  for o in m['object_events']:
   assert 0<=o['x']<w and 0<=o['y']<h and not tt[o['y']*w+o['x']]&0xc00,(name,'Actor in wall',o)
  for e in m['warp_events']:
   assert 0<=e['x']<w and 0<=e['y']<h,(name,'Warp outside map',e)
   if e['dest_map']=='MAP_DYNAMIC':
    assert name=='OlivineCity_Lighthouse_Elevator',('Unexpected dynamic warp',name,e)
    continue
   assert e['dest_map'] in ids,(name,'Missing warp destination',e)
   dst=maps[ids[e['dest_map']]];j=int(e['dest_warp_id']);assert 0<=j<len(dst['warp_events']),(name,'Invalid destination warp ID',e)
   if name=='OlivineCity':
    back=dst['warp_events'][j];assert back['dest_map']==city['id'] and int(back['dest_warp_id'])==m['warp_events'].index(e),('Door leaf does not return to corresponding outside segment',name,e,back)
  for e in m['object_events']+m['bg_events']:
   assert 0<=e['x']<w and 0<=e['y']<h,(name,'Interaction outside map',e)
   assert re.search(r'^'+re.escape(e['script'])+r'(?:::|:)',allscripts,re.M) or re.search(r'^'+re.escape(e['script'])+r'(?:::|:)',(R/f'data/maps/{name}/scripts.inc').read_text(),re.M),(name,'Unknown interaction script',e)
  if built:
   assert f'data/maps/{name}/header.inc' in headers and re.search(r'^\s*\.4byte '+re.escape(name)+r'\s*$',table,re.M),('Map excluded from Emerald build',name)
 # Dry-ground connectivity is essential: Surf must not mask a missing town road.
 tt=tile['OlivineCity'];actors={(o['x'],o['y']) for o in city['object_events']};start=(heal['x'],heal['y']);seen={start};q=deque([start]);w,h=64,64
 while q:
  x,y=q.popleft()
  for n in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   a,b=n
   if n in seen or n in actors or not(0<=a<w and 0<=b<h):continue
   v=tt[b*w+a]
   if v&0xc00 or v>>12!=3:continue
   seen.add(n);q.append(n)
 for e in city['warp_events']:assert (e['x'],e['y']+1) in seen,('City threshold has no pedestrian front approach',e)
 for e in city['object_events']+city['bg_events']:assert any((e['x']+dx,e['y']+dy) in seen for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]),('Unreachable city interaction',e)
 # A door leaf is an active transition, not a pedestrian path. Counting it
 # as ordinary floor concealed the first port forecourt's one-way trap: Joe
 # could enter from the north but was stranded south after the native exit.
 # Every actual outside landing must return to the Center apron without
 # crossing ANY active threshold or using Surf/another interior as a bypass.
 thresholds={(e['x'],e['y']) for e in city['warp_events']};safe_return={start};todo=deque([start])
 while todo:
  x,y=todo.popleft()
  for point in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   a,b=point
   if point in safe_return or point in thresholds or point in actors or not(0<=a<w and 0<=b<h):continue
   v=tt[b*w+a]
   if v&0xc00 or v>>12!=3:continue
   safe_return.add(point);todo.append(point)
 for e in city['warp_events']:
  outside=(e['x'],e['y']+1)
  assert outside in safe_return,('Outside door arrival trapped behind active thresholds/no dry return',e,outside)
 assert all((x,0) in seen for x in range(21,26)),'North road aperture incomplete'
 assert (23,53) in seen and (24,53) in seen,'Both south-facing GBA port leaves need pedestrian front approaches'
 center=(R/'data/maps/OlivineCity_PokemonCenter_1F/scripts.inc').read_text();assert 'map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume' in center,'Preserve nurse initialization'
 assert 'givemon' not in (R/'crossroads/scripts/olivine.inc').read_text()
 if built:
  # Inclusion alone cannot detect a stale compiled layout after generators
  # changed it. Compare every delivered city/interior map's actual ROM bytes.
  nm=shutil.which('arm-none-eabi-nm') or '/workspace/toolchain/root/usr/bin/arm-none-eabi-nm'
  symbols={parts[2]:int(parts[0],16) for line in subprocess.check_output([nm,'-an',str(R/'pokeemerald.elf')],text=True).splitlines() if len(parts:=line.split())==3}
  rom=(R/'pokeemerald.gba').read_bytes();checked=0
  for name,m in maps.items():
   if not name.startswith('OlivineCity'):continue
   l=layouts[m['layout']];symbol=l['name']+'_Blockdata';assert symbol in symbols,('Compiled layout symbol missing',name,symbol)
   offset=symbols[symbol]-0x08000000;expected=(R/l['blockdata_filepath']).read_bytes()
   assert 0<=offset<len(rom) and rom[offset:offset+len(expected)]==expected,('Delivery ROM contains stale/different map data',name)
   checked+=1
  print('Exact compiled delivery-ROM blockdata matches authored outputs:',checked,'Olivine maps PASS')
 print('HGSS Olivine stable IDs/heals, canonical buildings, preserved additions, per-segment reciprocity, dry returns avoiding active doorways, scripts and Emerald inclusion: PASS')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--built',action='store_true');validate(p.parse_args().built)
