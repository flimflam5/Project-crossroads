#!/usr/bin/env python3
"""Independent exact crop/furniture migration and source-instance coverage."""
import argparse,json,struct,subprocess
from pathlib import Path
from build_hgss_center_basement_assets import USED
R=Path(__file__).resolve().parents[2];BASE='3f935d5e8600c5a280b9172b555edb35ca52b6c0'
def load(p):return json.loads((R/p).read_text())
def old(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R)
def words(b):return list(struct.unpack('<'+str(len(b)//2)+'H',b))
def validate(reception_screenshot=None):
 c=load('crossroads/hgss/contracts/center-basement-qa09.json');assert c['source_commit']==BASE
 m=load('data/maps/EcruteakCity_PokemonCenter_B1F/map.json');before=json.loads(old('data/maps/EcruteakCity_PokemonCenter_B1F/map.json'));before['bg_events']=c['new_bg_events'];assert m==before,'B1F actors/warps/scripts changed outside exact terminal sign'
 l=next(x for x in load('data/layouts/layouts.json')['layouts']if x['id']==m['layout']);before_l=next(x for x in json.loads(old('data/layouts/layouts.json'))['layouts']if x['id']==m['layout']);expected=dict(before_l,height=14,secondary_tileset='gTileset_HgssCenterBasement');assert l==expected
 original=words(old(l['blockdata_filepath']));expected=original.copy()
 for d in c['changes']:
  i=d['y']*17+d['x'];assert expected[i]==d['before'];expected[i]=d['after']
 expected+=c['appended_words'];t=words((R/l['blockdata_filepath']).read_bytes());assert t==expected,'Unexpected B1F cell change'
 f=load('crossroads/hgss/canonical_events/ecruteak-interior-geometry.json')['MAP_ECRUTEAK_POKECENTER_B1F'];props=f['chunks'][0]['props'];perms=f['chunks'][0]['permissions'];art=load('crossroads/hgss/art/center-basement/manifest.json')['specs']
 assert [(p['tile_x'],p['tile_z'])for p in props if p['model']==23]==[(12.5,12.5),(4.5,12.5)]
 for x in (4,12):assert t[11*17+x]==0x60a and t[12*17+x]==0x612,('Source lower plant missing',x)
 table=art['waiting_table'];assert (table['width'],table['height'])==(2,2)
 for dy in range(2):
  for dx in range(2):assert t[(8+dy)*17+2+dx]==0x400|table['start']+dy*2+dx
 for p in props:
  if p['model']not in(57,58):continue
  x,y=int(p['tile_x']),int(p['tile_z']);name='blue_stool'if p['model']==57 else'yellow_stool';assert t[y*17+x]==0x400|art[name]['start'],('Missing source stool',p)
 for i in range(2):assert t[(4+i)*17+15]==0x400|art['communication_terminal']['start']+i
 for x in (5,9):
  for dy in range(2):assert t[(1+dy)*17+x]==0x400|art['communication_back_panel']['start']+dy
 for center in (4,8,12):
  for dy in range(3):
   for dx in range(3):
    i=(3+dy)*17+center-1+dx
    if dx==1 and dy<2:assert t[i]==original[i],('Booth hides original staff standing/head floor',center,dy)
    else:assert t[i]&1023==art['communication_booth']['start']+dy*3+dx and t[i]&0xfc00==original[i]&0xfc00,('Source booth body/physics missing',center,dx,dy)
 assert not t[12*17+8]&0xc00 and not perms[12*32+8]&0x8000,'Canonical lower public floor still cropped'
 assert all(v&0xc00 for v in t[13*17:14*17]),'Missing southern boundary'
 # Upper reception and original escalator/arrival stay unchanged. Newly
 # restored source stools explicitly own four former floor collision cells.
 collision_changes={(d['x'],d['y'])for d in c['changes']if d['before']&0xfc00!=d['after']&0xfc00}
 assert collision_changes=={(2,7),(3,7),(4,8),(4,9)},('Unexpected old-area ground footprint',collision_changes)
 assert m['warp_events']==json.loads(old('data/maps/EcruteakCity_PokemonCenter_B1F/map.json'))['warp_events']
 # Native floor art can be recolored privately; every shared resource remains
 # exact, normalizing only the repository's documented LF/CRLF text filter.
 for path in ['tiles.png','metatiles.bin','metatile_attributes.bin']+[f'palettes/{i:02}.pal'for i in range(16)]:
  p='data/tilesets/secondary/pokemon_center/'+path;a=(R/p).read_bytes();b=old(p)
  if path.endswith('.pal'):a,b=a.replace(b'\r\n',b'\n'),b.replace(b'\r\n',b'\n')
  assert a==b,('Shared Center changed',path)
 pals=(R/'data/tilesets/secondary/hgss_center_basement/palettes/06.pal').read_text().splitlines()[3:];colors=[tuple(map(int,x.split()))for x in pals];assert colors[9]==(105,160,184)and colors[12]==(214,241,243)
 for p in props:assert p['model']in{4,12,23,33,41,42,57,58,109,110},('Unhandled source prop model',p)
 assert len(props)==23
 # The1F keeps the actual warm palette, adds its identifying green floor
 # emblem and blue rear portals, and preserves every other rendered pixel.
 from validate_theater_stage import renderer
 _,old_b1f_attr=renderer('pokemon_center',True);_,new_b1f_attr=renderer('hgss_center_basement')
 for d in c['changes']:
  if art['communication_booth']['start']<=d['after']&1023<art['communication_booth']['start']+9 or art['communication_back_panel']['start']<=d['after']&1023<art['communication_back_panel']['start']+2:
   before_attr=old_b1f_attr(d['before']&1023);expected_attr=before_attr|(0x80 if(d['x'],d['y'])in{(4,5),(8,5),(12,5)}else 0)
   assert new_b1f_attr(d['after']&1023)==expected_attr,('Booth/panel changed source layer/behavior outside three real counter fronts',d['x'],d['y'])
 assert c['counter_behavior_cells']==[dict(x=x,y=5,before_attribute=0x1000,after_attribute=0x1080)for x in(4,8,12)]
 c1=load('crossroads/hgss/contracts/center-reception-qa09.json');assert c1['source_commit']==BASE
 name='EcruteakCity_PokemonCenter_1F';m1=load('data/maps/'+name+'/map.json');assert m1==json.loads(old('data/maps/'+name+'/map.json'))
 l1=next(x for x in load('data/layouts/layouts.json')['layouts']if x['id']==m1['layout']);oldl=next(x for x in json.loads(old('data/layouts/layouts.json'))['layouts']if x['id']==m1['layout']);assert l1==dict(oldl,secondary_tileset='gTileset_HgssCenterReception')
 before1=words(old(l1['blockdata_filepath']));expected=before1.copy();changed=set()
 for d in c1['changes']:
  i=d['y']*17+d['x'];assert expected[i]==d['before'];expected[i]=d['after'];changed.add(i)
 actual=words((R/l1['blockdata_filepath']).read_bytes());assert actual==expected and len(changed)==27
 oldrender,oldattr=renderer('pokemon_center',True);newrender,newattr=renderer('hgss_center_reception')
 private_meta=words((R/'data/tilesets/secondary/hgss_center_reception/metatiles.bin').read_bytes());emblem=load('crossroads/hgss/art/center-reception/manifest.json')['specs']['floor_emblem']
 for n in range(emblem['start'],emblem['start']+20):assert private_meta[(n-512)*8+4:(n-512)*8+8]==[0]*4,('Opaque emblem foreground can hide Joe',n)
 for i,(a,b)in enumerate(zip(before1,actual)):
  is_counter=(i%17,i//17)in{(2,3),(6,3),(11,3)}
  assert a&0xfc00==b&0xfc00 and (oldattr(a&1023)|(0x80 if is_counter else 0))==newattr(b&1023),('1F physics/layers changed outside exact three counter behaviors',i%17,i//17)
  if i not in changed or is_counter:assert oldrender(a&1023).tobytes()==newrender(b&1023).tobytes(),('Unrelated1F visible pixels changed',i%17,i//17)
 assert c1['counter_behavior_cells']==[dict(x=x,y=3,before_attribute=0x1000,after_attribute=0x1080)for x in(2,6,11)]
 if reception_screenshot:
  from PIL import Image,ImageChops
  frame=Image.open(reception_screenshot).convert('RGB');assert frame.size==(240,160)
  a=load('crossroads/hgss/art/center-reception/manifest.json')['specs']['floor_emblem'];patch=Image.new('RGB',(80,64))
  for y in range(4):
   for x in range(5):patch.paste(newrender(a['start']+y*5+x).convert('RGB'),(x*16,y*16))
  matches=[]
  for y in range(97):
   for x in range(161):
    if ImageChops.difference(frame.crop((x,y,x+80,y+64)),patch).getbbox()is None:matches.append([x,y])
  assert len(matches)==1,('Compiled1F floor emblem does not match5120 native pixels',matches)
  Path(reception_screenshot).with_suffix('.emblem-pixels.json').write_text(json.dumps(dict(native_size=[240,160],compiled_emblem_pixels_matched=5120,emblem_top_left=matches[0]),indent=2)+'\n')
  print('Compiled native green floor emblem5120/5120 pixels: PASS')
 print('B1F14-row source floor/complete furnishings; exact37old+34new cells;1F24visual+3pixel-identical counter cells;333othercells pixel-exact; exactly6counter behaviors fixed; shared Center unchanged: PASS')
 return {'EcruteakCity_PokemonCenter_B1F'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--reception-screenshot');a=p.parse_args();validate(a.reception_screenshot)
