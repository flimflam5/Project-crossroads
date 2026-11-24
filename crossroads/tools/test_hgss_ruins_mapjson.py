#!/usr/bin/env python3
"""Run the actual Emerald map generator for the four new rooms and gates.

Requires the project's built mapjson binary; checks build inclusion and event
JSON parsing, not game linking, rendering or gameplay.
"""
import argparse,json,subprocess,tempfile
from pathlib import Path
from stage_hgss_ruins_hidden_graph import NAMES,IDS

R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--mapjson',type=Path,default=R/'tools/mapjson/mapjson');a=p.parse_args()
assert a.mapjson.is_file(),f'Build mapjson first: {a.mapjson}'
all_groups=json.loads((R/'data/maps/map_groups.json').read_text())
paths=[R/'data/maps'/name/'map.json' for g in all_groups['group_order'] for name in all_groups[g]]
assert all(p.is_file() for p in paths)
with tempfile.TemporaryDirectory(prefix='ruins-mapjson-') as temp:
 root=Path(temp);asm=root/'asm';c=root/'c';asm.mkdir();c.mkdir()
 def call(*args):subprocess.run([str(a.mapjson),*map(str,args)],cwd=R,check=True)
 call('groups','emerald',R/'data/maps/map_groups.json',*paths,str(asm)+'/',str(c)+'/')
 call('layouts','emerald',R/'data/layouts/layouts.json',str(asm)+'/',str(c)+'/')
 groupdata=(asm/'groups.inc').read_text();mapids=(c/'map_groups.h').read_text()
 for n,i in zip(NAMES,IDS):
  assert f'.4byte {n}' in groupdata and i in mapids,(n,'missing Emerald map group')
 for n in (*NAMES,'RuinsOfAlph_SouthwestChamber','RuinsOfAlph_NorthwestChamber'):
  folder=root/n;folder.mkdir()
  call('map','emerald',R/f'data/maps/{n}/map.json',R/'data/layouts/layouts.json',str(folder)+'/')
  assert (folder/'events.inc').is_file() and (folder/'header.inc').is_file()
print('Actual mapjson: 4 Emerald group IDs, layouts, 4 fall-room and 2 first-chamber event files PASS; no full ROM or emulator test.')
