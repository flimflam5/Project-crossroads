#!/usr/bin/env python3
"""Positive source-furniture regressions plus immutable resource preservation."""
import json,struct,subprocess,io
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2];BASE='fd151242458efe5759b18650f35a5e5b2fa47e45'
def load(p):return json.loads((R/p).read_text())
def validate():
 art=load('crossroads/hgss/art/temple/manifest.json')['specs'];facts=load('crossroads/hgss/canonical_events/ecruteak-interior-geometry.json');ls={l['id']:l for l in load('data/layouts/layouts.json')['layouts']}
 def room(n):
  m=load(f'data/maps/{n}/map.json');l=ls[m['layout']];b=(R/l['blockdata_filepath']).read_bytes();return l['width'],struct.unpack('<'+str(len(b)//2)+'H',b)
 for n,h in [('EcruteakCity_Residence','MAP_ECRUTEAK_SOUTHWEST_HOUSE'),('EcruteakCity_DowsingHouse','MAP_ECRUTEAK_DOWSING_MACHINE_HOUSE')]:
  source_props=[p for c in facts[h]['chunks'] for p in c['props']];props={p['model'] for p in source_props};assert {20,21,64,94}<=props,'Source kitchen/fridge/bookcase/dining furniture missing'
  # Ecruteak0066 has the wide model64 cabinet centered9.0 and no rear plant.
  # Olivine0097 instead has model66 centered8.0 plus model23 at9.5; never
  # propagate its different rear-right furniture into these two houses.
  assert 23 not in props and [(p['tile_x'],p['tile_z']) for p in source_props if p['model']==64]==[(9.0,3.5)],'Do not substitute the different Olivine house template'
  w,t=room(n)
  for part,x,y in [('fridge',1,2),('house_kitchen',2,2),('house_window',4,1),('cabinet',8,2),('dining_table',6,5)]:
   a=art[part]
   for dy in range(a['height']):
    for dx in range(a['width']):assert t[(y+dy)*w+x+dx]&1023==a['start']+dy*a['width']+dx,(n,'Wrong source furniture',part,x+dx,y+dy)
  tv=art['television'];assert not any(tv['start']<=v&1023<tv['start']+tv['width']*tv['height'] for v in t),'Wrong TV instead of source bookcase'
 w,t=room('EcruteakCity_PokemonCenter_1F');f=facts['MAP_ECRUTEAK_POKECENTER_1F'];plants={(int(p['tile_x']),int(p['tile_z'])) for c in f['chunks'] for p in c['props'] if p['model']==23};assert plants=={(15,4),(14,15),(15,15)}
 for x,y in plants:assert t[(y-1)*w+x]==0x60a and t[y*w+x]==0x612,('Missing source Center plant',x,y)
 # Existing graphics/metatile ordinals are byte/pixel identical; only appended
 # resources may be referenced by the explicitly migrated room cells.
 path='data/tilesets/secondary/hgss_temple/'
 for name in ['metatiles.bin','metatile_attributes.bin']:
  old=subprocess.check_output(['git','show',BASE+':'+path+name],cwd=R);assert (R/path/name).read_bytes()[:len(old)]==old,('Historical temple metatiles changed',name)
 old_manifest=json.loads(subprocess.check_output(['git','show',BASE+':crossroads/hgss/art/temple/manifest.json'],cwd=R));old=Image.open(io.BytesIO(subprocess.check_output(['git','show',BASE+':'+path+'tiles.png'],cwd=R)));new=Image.open(R/path/'tiles.png')
 for i in range(old_manifest['tiles']):
  box=(i%16*8,i//16*8,i%16*8+8,i//16*8+8);assert new.crop(box).tobytes()==old.crop(box).tobytes(),('Historical temple graphic changed',i)
 assert old.getpalette()[:48]==new.getpalette()[:48]
 print('Ecruteak source kitchen/window/bookcases, three Center plants and append-only historical temple resources: PASS')
 return {'EcruteakCity_Residence','EcruteakCity_DowsingHouse','EcruteakCity_PokemonCenter_1F'}
if __name__=='__main__':validate()
