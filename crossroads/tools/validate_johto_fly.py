#!/usr/bin/env python3
"""QA Fly destinations are the existing ten safe city heal arrivals, not new IDs."""
import json,struct
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def load(p):return json.loads((R/p).read_text())
atlas=load('crossroads/johto/atlas.json');heals={h['id']:h for h in load('src/data/heal_locations.json')['heal_locations']};layouts={l['id']:l for l in load('data/layouts/layouts.json')['layouts']}
expected={'OlivineCity','EcruteakCity','GoldenrodCity','VioletCity','AzaleaTown','CherrygroveCity','NewBarkTown','MahoganyTown','BlackthornCity','CianwoodCity'}
assert set(atlas['fly_destinations'])==expected
for name,heal in atlas['fly_destinations'].items():
 m=load(f'data/maps/{name}/map.json');l=layouts[m['layout']];h=heals[heal];w,H=l['width'],l['height'];x,y=h['x'],h['y']
 assert h['map']==m['id'] and 0<x<w-1 and 0<y<H-1
 tiles=struct.unpack('<'+str(w*H)+'H',(R/l['blockdata_filepath']).read_bytes())
 def safe(x,y):return not tiles[y*w+x]&0xc00 and tiles[y*w+x]>>12==3
 assert safe(x,y) and any(safe(u,v) for u,v in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
 assert all((o['x'],o['y'])!=(x,y) for o in m['object_events'])
 assert all((e['x'],e['y'])!=(x,y) for e in m['warp_events']),'Landing must not immediately re-enter a door'
print('Johto QA Fly: ten existing heal IDs, safe non-door arrivals, no NPC overlap: PASS')
