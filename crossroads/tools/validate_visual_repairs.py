#!/usr/bin/env python3
"""Repair scope/save contracts, collision assembly and ground-layer invariants."""
import json,struct,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];report=json.loads((R/'crossroads/qa/visual-0.9.1/manifest.json').read_text());sha=lambda p:hashlib.sha256((R/p).read_bytes()).hexdigest()
hgss=(R/'crossroads/hgss/contracts/save-contracts.json').exists()
if hgss:
 from validate_hgss_ecruteak import validate
 validate() # Stronger canonical/append-only contracts replace the authorized old geometry only.
replaced={'data/maps/map_groups.json','data/layouts/layouts.json','src/data/heal_locations.json'} if hgss else set()
reconstructed={'EcruteakCity','EcruteakCity_BellTower','JohtoRoute37','JohtoRoute38','JohtoRoute42'} if hgss else set()
for p,h in report['unchanged_contracts'].items():
 if p not in replaced:assert sha(p)==h,('Changed preserved contract',p)
layouts={l['id']:l for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']};changed=[]
for row in report['maps']:
 n=row['name']
 if n not in reconstructed:
  assert sha(f'data/maps/{n}/map.json')==row['map_metadata_sha256'],('Changed events/IDs',n)
  assert sha(layouts[row['layout']]['blockdata_filepath'])==row['after_layout_sha256'],('Unrecorded layout edit',n)
 if row['before_layout_sha256']!=row['after_layout_sha256']:changed.append(n)
assert set(changed)=={'EcruteakCity','MahoganyTown','MahoganyTown_Workshop','JohtoRoute38','JohtoRoute39'}
art=json.loads((R/'crossroads/art/western/architecture.json').read_text());data=(R/'data/tilesets/secondary/western_city/metatile_attributes.bin').read_bytes()
for name,s in art.items():
 if not isinstance(s,dict):continue
 for y in range(s['height']):
  for x in range(s['width']):
   attr=struct.unpack_from('<H',data,(s['start']-512+y*s['width']+x)*2)[0]
   assert attr>>12==(1 if y>=s['height']-2 else 0),(name,'ground art covers player')
   assert attr&255==(0x60 if (x,y)==(s['door_x'],s['door_y']) else 0),(name,'changed door behavior')
assert struct.unpack_from('<2H',data,(0x3e8-512)*2)==(0x1000,0x1000),'Johto root bases must be behind foreground sprite'
l=layouts['LAYOUT_MAHOGANY_TOWN_WORKSHOP'];t=struct.unpack('<168H',(R/l['blockdata_filepath']).read_bytes())
for x,y in [(8,4),(2,7)]:
 assert [t[y*14+x],t[y*14+x+1],t[(y+1)*14+x],t[(y+1)*14+x+1]]==[0x376a,0x376b,0x3772,0x3773]
print('Visual repair scope, stable map/save contracts, complete benches, layers/door behavior: PASS. Owner visual QA remains pending.')
