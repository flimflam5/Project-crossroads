#!/usr/bin/env python3
"""Independent HGSS Theater furniture/aisle regression, not visual acceptance."""
import json,struct
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def load(p):return json.loads((R/p).read_text())
def validate():
 facts=load('crossroads/hgss/canonical_events/ecruteak-interior-geometry.json')['MAP_ECRUTEAK_DANCE_THEATER']
 m=load('data/maps/EcruteakCity_DanceTheater/map.json');l=next(l for l in load('data/layouts/layouts.json')['layouts'] if l['id']==m['layout']);w,h=l['width'],l['height'];b=(R/l['blockdata_filepath']).read_bytes();t=struct.unpack('<'+str(w*h)+'H',b);art=load('crossroads/hgss/art/temple/manifest.json')['specs'];a=art['theater_bench'];assert (a['width'],a['height'])==(1,1)
 source={(int(p['tile_x'])+i%facts['matrix_dimensions'][0]*32,int(p['tile_z'])+i//facts['matrix_dimensions'][0]*32) for i,c in enumerate(facts['chunks']) for p in c['props'] if p['model']==56}
 # Explicit expected source pattern is independent of the generator's loop.
 assert source=={(4,10),(10,10),(12,10)}|{(x,y) for x in [4,6,8,10,12] for y in [12,14]}
 actual={(i%w,i//w) for i,v in enumerate(t) if v&1023==a['start']}
 assert actual==source,('Missing/extra Theater audience benches',actual^source)
 for x,y in actual:assert t[y*w+x]&0xc00 and x<w-1 and y<h-1,('Seat ground footprint/room wall',x,y)
 # Every former duplicate lower row and the source front center aisle remain
 # real walking floor; old rectangular stamping must never be reintroduced.
 for x,y in {(x,y) for x in range(3,w-1) for y in [11,13,15]}|{(6,10),(7,10),(8,10),(9,10)}:
  # Source6/7,10 are the fixed stage/audience partition, not open floor.
  if (x,y) in {(6,10),(7,10)}:continue
  assert not t[y*w+x]&0xc00 and t[y*w+x]>>12==3,('Duplicated seat or blocked aisle',x,y)
 old=art['prayer_table'];assert not any(old['start']<=v&1023<old['start']+old['width']*old['height'] for v in t),'Wide table duplicates remain'
 print('HGSS Theater13 exact one-cell bench anchors, no duplicated rows, open source front aisle and intact room bounds: PASS')
 return {'EcruteakCity_DanceTheater'}
if __name__=='__main__':validate()
