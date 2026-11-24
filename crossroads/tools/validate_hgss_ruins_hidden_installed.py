#!/usr/bin/env python3
"""Verify installed Ruins gated graph against the staged HGSS-source candidate.

This is a static source/graph check, not normal controller movement, item-use,
old-save or visual verification. The NW/SW gates are nonpersistent prototypes.
"""
import json,re,struct,subprocess
from pathlib import Path
from stage_hgss_ruins_hidden_graph import stage as stage_graph,NAMES,IDS,FIRST,LAYOUTS
from stage_hgss_ruins_gate_events import stage as stage_gates
from stage_hgss_ruins_network import flood

R=Path(__file__).resolve().parents[2]
def load(path):return json.loads((R/path).read_text())
def old(path):return subprocess.check_output(['git','show','ee1042d7ae:'+path],cwd=R)
def words(path):
 b=(R/path).read_bytes();assert len(b)%2==0
 return struct.unpack('<%dH'%(len(b)//2),b)

def validate():
 first={};first_scripts={}
 for name in ('RuinsOfAlph_SouthwestChamber','RuinsOfAlph_NorthwestChamber'):
  m=json.loads(old(f'data/maps/{name}/map.json'));first[m['id']]=m
  first_scripts[m['id']]=old(f'data/maps/{name}/scripts.inc').decode()
 files={}
 def write(path,value):files[path]=value
 maps,tiles,layouts,borders,scripts,proposals,gates=stage_graph(write,first)
 mapped,first_out=stage_gates(proposals,first_scripts,40)
 groups=load('data/maps/map_groups.json')['gMapGroup_CrossroadsJohtoExpansion']
 assert groups[57:61]==list(NAMES),'Hidden map ID ordinals changed'
 registered={e['id']:e for e in load('data/layouts/layouts.json')['layouts']}
 for path,value in files.items():
  expected=value.encode() if isinstance(value,str) else value
  assert (R/path).read_bytes()==expected,('Generated Ruins resource differs',path)
 for name,lid in zip(NAMES,LAYOUTS):
  assert load(f'data/maps/{name}/map.json')==maps[name],(name,'map events changed')
  assert registered[lid]==layouts[lid]
  assert words(layouts[lid]['blockdata_filepath'])==tuple(tiles[name])
  assert words(layouts[lid]['border_filepath'])==tuple(borders[name])
  assert (R/f'data/maps/{name}/scripts.inc').read_text()==scripts[name]
  assert not maps[name]['object_events'] and not maps[name]['bg_events']
  assert not re.search(r'\b(?:setflag|clearflag|giveitem|removeitem|givemon)\b',scripts[name])
 for key in FIRST:
  m=mapped[key];name=m['name'];assert load(f'data/maps/{name}/map.json')==m
  assert (R/f'data/maps/{name}/scripts.inc').read_text()==first_out[key]
  assert m['warp_events'][0]==first[key]['warp_events'][0]
  assert (m['warp_events'][1]['x'],m['warp_events'][1]['y'])==(5,2)
  assert (m['warp_events'][2]['x'],m['warp_events'][2]['y'])==(5,1)
  assert m['warp_events'][1]['dest_map']==m['warp_events'][2]['dest_map']
  assert m['warp_events'][1]['dest_warp_id']==m['warp_events'][2]['dest_warp_id']=='0'
  plane=words(f'data/layouts/{name}/map.bin');attrs=words('data/tilesets/primary/hgssruinschamber/metatile_attributes.bin')
  assert plane[1*10+5]&0xc00 and not plane[2*10+5]&0xc00
  assert attrs[plane[2*10+5]&1023]&255==8 and attrs[40]&255==0x60
  assert (5,3) in flood(plane,10,11,(5,2))
  assert 'setmetatile 5, 1, 40, FALSE' in first_out[key]
  assert not re.search(r'^\s*(?:setflag|clearflag|giveitem|removeitem|givemon)\b',first_out[key],re.M)
 assert 'RuinsOfAlph_SouthwestChamber_WaterStoneUsed::' in first_out[FIRST[0]]
 assert 'specialvar VAR_RESULT, Crossroads_AlphHasNonEggHoOh' in first_out[FIRST[1]]
 assert 'def_special Crossroads_AlphHasNonEggHoOh' in (R/'data/specials.inc').read_text()
 # BG signs are checked only during interaction; step events check coord and
 # warp scripts separately. After metatile 40 is opened, MB_NON_ANIMATED_DOOR
 # must still be recognized as a valid step warp at the same coordinates.
 control=(R/'src/field_control_avatar.c').read_text()
 step=re.search(r'bool8 TryStartStepBasedScript\([^)]*\)\s*\{(.*?)\n\}',control,re.S)
 assert step and 'TryStartCoordEventScript' in step[1] and 'TryStartWarpEventScript' in step[1]
 assert 'GetInteractedBackgroundEventScript' not in step[1]
 warpcheck=re.search(r'static bool8 IsWarpMetatileBehavior\(u16 metatileBehavior\)\s*\{(.*?)\n\}',control,re.S)
 assert warpcheck and 'MetatileBehavior_IsNonAnimDoor' in warpcheck[1]
 temp=(R/'src/event_data.c').read_text()
 assert 'memset(&gSaveBlock1Ptr->vars[TEMP_VARS_START - VARS_START], 0, TEMP_VARS_SIZE)' in temp
 assert not re.search(r'\b(?:FlagSet|FlagClear|RemoveBagItem|AddBagItem)\s*\(', (R/'src/crossroads_alph.c').read_text())
 # Script-triggered falls are modelled explicitly by the network validator;
 # these edges are checked against the exact installed script/coordinate pairs.
 falls={}
 for i in (0,1):
  n=NAMES[i];e=maps[n]['coord_events'][0];seed=(11,7) if i==0 else (11,14)
  assert (e['x'],e['y'])==(6,3) and f'warp {IDS[i+2]}, {seed[0]}, {seed[1]}' in scripts[n]
  falls[(n,6,3)]=[(NAMES[i+2],*seed)]
 for i in (2,3):
  n=NAMES[i];e=maps[n]['coord_events'][0];dest=(5,42) if i==2 else (5,24)
  assert f'warp MAP_RUINS_OF_ALPH_UNDERGROUND_HALL, {dest[0]}, {dest[1]}' in scripts[n]
  falls[(n,e['x'],e['y'])]=[('RuinsOfAlph_UndergroundHall',*dest)]
 print('Ruins hidden: exact staged maps/scripts, nonpersistent gates, return-only aliases and source fall coordinates PASS; normal controller/item use remains untested.')
 return falls

if __name__=='__main__':validate()
