#!/usr/bin/env python3
"""Test independently staged gated-return/fall graph; no gameplay claim."""
import json,re,struct,subprocess
from collections import deque
from pathlib import Path
from stage_hgss_ruins_hidden_graph import stage,NAMES,IDS,FIRST,LAYOUTS
from stage_hgss_ruins_hidden import reference_component

R=Path(__file__).resolve().parents[2]
def load(p):return json.loads((R/p).read_text())
def words(path):
 b=(R/path).read_bytes();return struct.unpack('<%dH'%(len(b)//2),b)
def local(plane,w,h,start):
 q=deque([start]);seen=set(q)
 while q:
  x,y=q.popleft()
  for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
   if 0<=xx<w and 0<=yy<h and (xx,yy) not in seen and not plane[yy*w+xx]&0xc00:
    seen.add((xx,yy));q.append((xx,yy))
 return seen


def run():
 names=('RuinsOfAlph_SouthwestChamber','RuinsOfAlph_NorthwestChamber')
 first={m['id']:m for m in (json.loads(subprocess.check_output(['git','show',f'ee1042d7ae:data/maps/{n}/map.json'],cwd=R)) for n in names)}
 before=json.dumps(first,sort_keys=True)
 files={}
 def write(path,data):assert path not in files;files[path]=data
 maps,tiles,layouts,borders,scripts,proposed,gates=stage(write,first)
 assert json.dumps(first,sort_keys=True)==before,'Source first-room data was modified'
 assert load('data/maps/map_groups.json')['gMapGroup_CrossroadsJohtoExpansion'][57:61]==list(NAMES)
 assert len(files)==61 and tuple(maps)==NAMES
 for i,first_id in enumerate(FIRST):
  old=first[first_id];room=proposed[first_id];new=maps[NAMES[i]]
  assert room['warp_events'][0]==old['warp_events'][0] and len(room['warp_events'])==2
  arrival=room['warp_events'][1];back=new['warp_events'][0]
  assert (arrival['x'],arrival['y'],arrival['dest_map'],arrival['dest_warp_id'])==(5,2,IDS[i],'0')
  assert (back['x'],back['y'],back['dest_map'],back['dest_warp_id'])==(6,17,first_id,'1')
  gate=gates[first_id];assert gate['wall']==[5,1] and gate['return_floor']==[5,2]
  assert gate['return_only_warp_index']==1 and gate['installed'] is False and gate['condition_pending'] is True
  source=words(f'data/layouts/{names[i]}/map.bin');attrs=words('data/tilesets/primary/hgssruinschamber/metatile_attributes.bin')
  assert source[1*10+5]&0xc00 and not source[2*10+5]&0xc00
  assert attrs[source[2*10+5]&1023]&255==8 and source[2*10+5]>>12==3
  assert (5,3) in local(source,10,11,(5,2)), 'No safe walking exit from return tile'
  plane=tiles[NAMES[i]];l=layouts[LAYOUTS[i]];reachable=local(plane,l['width'],l['height'],(6,17))
  assert (6,3) in reachable and (6,4) in reachable
  assert new['coord_events']==[dict(type='trigger',x=6,y=3,elevation=0,var='VAR_TEMP_0',var_value='0',script=NAMES[i]+'_Fall')]
  assert f'warp {IDS[i+2]}, '+('11, 7' if i==0 else '11, 14') in scripts[NAMES[i]]
 for i in (2,3):
  n=NAMES[i];l=layouts[LAYOUTS[i]];m=maps[n];seed=(11,7) if i==2 else (11,14);edge=(20,13) if i==2 else (20,21)
  assert not m['warp_events'] and edge in local(tiles[n],l['width'],l['height'],seed)
  assert m['coord_events']==[dict(type='trigger',x=edge[0],y=edge[1],elevation=0,var='VAR_TEMP_0',var_value='0',script=n+'_Fall')]
  destination='5, 42' if i==2 else '5, 24'
  assert f'warp MAP_RUINS_OF_ALPH_UNDERGROUND_HALL, {destination}' in scripts[n]
  hall=words('data/layouts/HgssRuinsHallExpanded/map.bin');x,y=(5,42) if i==2 else (5,24)
  assert not hall[y*32+x]&0xc00 and (18,24) in local(hall,32,64,(x,y))
 for n in NAMES:
  m=maps[n];assert not m['object_events'] and not m['bg_events']
  assert all(re.fullmatch(r'\s*(?:\.byte 0|lockall|warp [A-Z_0-9]+, \d+, \d+|waitstate|releaseall|end|[A-Za-z0-9_]+::)\s*',line) for line in scripts[n].splitlines())
  assert not re.search(r'\b(?:setflag|clearflag|setvar|giveitem|removeitem|givemon)\b',scripts[n])
 return files,maps,tiles,layouts,borders,scripts,proposed,gates

if __name__=='__main__':
 assert run()==run()
 print('Staged gated returns and four scripted falls: source cells, reciprocal indices, independent room components and no flags/rewards PASS; no engine/emulator test.')
