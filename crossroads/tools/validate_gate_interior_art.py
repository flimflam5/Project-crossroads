#!/usr/bin/env python3
"""Exact V7 gate-art migration; source plants; optional native pixel evidence."""
import argparse,json,struct,sys
from pathlib import Path
from PIL import Image,ImageChops
from validate_theater_stage import data,words,renderer
R=Path(__file__).resolve().parents[2];BASE='3f935d5e8600c5a280b9172b555edb35ca52b6c0'
def load(p):return json.loads((R/p).read_text())
def validate(screenshot=None):
 c=load('crossroads/hgss/contracts/gate-interior-art-qa09.json');assert c['source_commit']==BASE
 a=load('crossroads/hgss/art/gate-interior/manifest.json');assert a['source_commit']==BASE and a['tiles']<=512 and a['metatiles']<=512
 before_layouts=json.loads(data('data/layouts/layouts.json',True))['layouts'];after_layouts=load('data/layouts/layouts.json')['layouts'];expected=list(c['before_words']);changed=set()
 for p in c['changes']:
  i=p['y']*12+p['x'];assert expected[i]==p['before'];expected[i]=p['after'];changed.add(i)
 oldrender,oldattr=renderer('hgss_temple',True);newrender,newattr=renderer('hgss_gate_interior')
 layer=load('crossroads/hgss/contracts/gate-ground-layers-qa10.json');assert layer['source_commit']=='7d92f79357b744dddb706bba121d7bd5e6fc4254'
 for d in layer['raw_changes']:
  i=d['y']*12+d['x'];assert expected[i]==d['before'];expected[i]=d['after'];changed.add(i)
 for name in c['maps']:
  m=load(f'data/maps/{name}/map.json');assert m==json.loads(data(f'data/maps/{name}/map.json',True)),(name,'Events/actors/warps changed')
  old=next(l for l in before_layouts if l['id']==m['layout']);new=next(l for l in after_layouts if l['id']==m['layout']);assert new==dict(old,secondary_tileset='gTileset_HgssGateInterior'),(name,'Unexpected layout change')
  before=words(data(old['blockdata_filepath'],True));after=words(data(new['blockdata_filepath']));assert list(before)==c['before_words'] and list(after)==expected
  for i,(v,w)in enumerate(zip(before,after)):
   assert v&0xfc00==w&0xfc00,(name,'Movement/elevation changed',i%12,i//12)
   assert oldattr(v&1023)==newattr(w&1023),(name,'Behavior/layer changed',i%12,i//12)
   if i not in changed:assert oldrender(v&1023).tobytes()==newrender(w&1023).tobytes(),(name,'Unrelated pixel changed',i%12,i//12)
  props=load('crossroads/hgss/canonical_events/ecruteak-interior-geometry.json')['MAP_ROUTE_'+('38'if'West'in name else'42')+'_ECRUTEAK_GATEHOUSE']['chunks'][0]['props'];bases={(int(p['tile_x']),int(p['tile_z']))for p in props if p['model']==114};assert bases=={(2,3),(10,3),(2,11),(10,11)}
  cells={(p['x'],p['y']):p for p in a['placements']}
  for x,y in bases:
   assert cells[x,y]['kind']==cells[x,y-1]['kind']=='plant'
   assert cells[x,y]['source_tile']==[0,1]and cells[x,y-1]['source_tile']==[0,0]
   assert after[y*12+x]&0xc00,(name,'Walkable plant pot',x,y)
  assert len([p for p in cells.values()if p['kind']=='plant'])==8
  # Alias cells retain real warp behavior on each of the three road rows.
  for x in (1,10):
   for y in (6,7,8):assert newattr(after[y*12+x]&1023)&255==0x61
 for path in ['tiles.png','metatiles.bin','metatile_attributes.bin']+[f'palettes/{i:02}.pal'for i in range(16)]:
  p='data/tilesets/secondary/hgss_temple/'+path;v,w=data(p),data(p,True)
  if path.endswith('.pal'):v,w=v.replace(b'\r\n',b'\n'),w.replace(b'\r\n',b'\n')
  assert v==w,('Shared Temple changed',path)
 result=dict(source_commit=BASE,maps=c['maps'],authorized_art_cells_per_map=len(changed),unchanged_visible_cells_per_map=144-len(changed),unchanged_physics_cells_per_map=144,source_plant_bases=sorted(bases),all_six_alias_behaviors_preserved=True,shared_temple_unchanged=True)
 if screenshot:
  frame=Image.open(screenshot).convert('RGB');assert frame.size==(240,160)
  plant=Image.new('RGB',(16,32));p=next(p for p in a['placements']if p['kind']=='plant'and p['source_tile']==[0,0]);q=next(p for p in a['placements']if p['kind']=='plant'and p['source_tile']==[0,1]);plant.paste(newrender(p['metatile']).convert('RGB'),(0,0));plant.paste(newrender(q['metatile']).convert('RGB'),(0,16))
  hits=[]
  for y in range(129):
   for x in range(225):
    if ImageChops.difference(frame.crop((x,y,x+16,y+32)),plant).getbbox()is None:hits.append([x,y])
  assert len(hits)>=2,('Expected at least two fully visible compiled gate plants',hits)
  result.update(native_size=[240,160],compiled_complete_plant_matches=hits,matched_plant_pixels=512*len(hits));Path(screenshot).with_suffix('.gate-pixels.json').write_text(json.dumps(result,indent=2)+'\n')
 from validate_gate_ground_layers import validate as validate_layers
 validate_layers()
 print('Gate art exact reviewed cells; both144-cell physics/layers, six alias behaviors, four source plants and shared Temple preserved: PASS')
 if screenshot:print('Native compiled gate plant pixels: PASS',len(hits),'complete plants')
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--screenshot');a=p.parse_args();validate(a.screenshot)
