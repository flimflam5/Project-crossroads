#!/usr/bin/env python3
"""Narrow BUILD10 gate-layer repair, independently pinned to7d92.

Old map/layout IDs, movement, elevation, attributes, actors, events and aliases
are immutable. Only the reviewed four north-plant art IDs and specified private
metatile drawing words may change. Normal-controller proof is a separate test.
"""
import argparse,functools,hashlib,io,json,struct,subprocess
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2]
BASE='7d92f79357b744dddb706bba121d7bd5e6fc4254'
ROOT='data/tilesets/secondary/hgss_gate_interior/'
def load(p):return json.loads((R/p).read_text())
def words(b):return struct.unpack('<'+str(len(b)//2)+'H',b)
@functools.lru_cache(None)
def get(p,old=False):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R)if old else(R/p).read_bytes()
def resource(old=False):
 roots=['data/tilesets/primary/building',ROOT.rstrip('/')]
 sheets=[Image.open(io.BytesIO(get(p+'/tiles.png',old)))for p in roots]
 metas=[words(get(p+'/metatiles.bin',old))for p in roots]
 attrs=[words(get(p+'/metatile_attributes.bin',old))for p in roots]
 pals=[[tuple(int(v)//8 for v in row.split())for row in get(roots[int(i>=6)]+f'/palettes/{i:02}.pal',old).decode().splitlines()[3:]]for i in range(16)]
 @functools.lru_cache(None)
 def glyph(v):
  k=v&1023;i=k%512;part=sheets[k>=512].crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8))
  if v&0x400:part=part.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if v&0x800:part=part.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  rgba=Image.new('RGBA',(8,8));rgba.putdata([tuple((c<<3)|(c>>2)for c in pals[v>>12][index])+(255,)if index else(0,0,0,0)for index in part.tobytes()]);return rgba
 @functools.lru_cache(None)
 def layers(n):
  raw=metas[n>=512][n%512*8:n%512*8+8];images=[]
  for z in range(2):
   im=Image.new('RGBA',(16,16))
   for j,v in enumerate(raw[z*4:z*4+4]):im.paste(glyph(v),(j%2*8,j//2*8))
   images.append(im)
  return images
 @functools.lru_cache(None)
 def render(n):
  im=Image.new('RGBA',(16,16))
  for v in layers(n):im.alpha_composite(v)
  return im
 return sheets,metas,attrs,pals,layers,render

def validate():
 c=load('crossroads/hgss/contracts/gate-ground-layers-qa10.json');assert c['source_commit']==BASE
 a=load('crossroads/hgss/art/gate-interior/manifest.json');old_a=json.loads(get('crossroads/hgss/art/gate-interior/manifest.json',True))
 assert a['placements']==old_a['placements'],'Historical3f935 gate-art migration changed'
 assert a['layer_fixes']==c['raw_changes']and old_a['tiles']==140
 assert c['maps']==['EcruteakCity_WestGate','EcruteakCity_EastGate']
 old_s,old_m,old_attrs,old_p,old_layers,old_render=resource(True);new_s,new_m,new_attrs,new_p,new_layers,new_render=resource(False)
 assert old_attrs[1]==new_attrs[1][:len(old_attrs[1])],'Existing metatile behaviors/layers changed'
 assert a['tiles']<=512 and a['metatiles']<=512
 # Existing packed glyphs are immutable; corrected surfaces reuse them or
 # append new glyphs. Palette8 was genuinely unused in the old gate.
 for i in range(old_a['tiles']):
  box=(i%16*8,i//16*8,i%16*8+8,i//16*8+8)
  assert old_s[1].crop(box).tobytes()==new_s[1].crop(box).tobytes(),('Old glyph changed',i)
 assert all(v>>12!=8 for v in old_m[1]),'Private black bank8 already used'
 for i in range(16):
  if i!=8:assert old_p[i]==new_p[i],('Unrelated palette changed',i)
 expected_pal8=list(old_p[8]);expected_pal8[1]=(0,0,0)
 assert new_p[8]==expected_pal8,'Only unused bank8 index1 may become opaque black'
 authorized={d['metatile']:d for d in c['metatile_changes']}
 assert set(authorized)=={904,906,915,924,937,938},'Correction scope exceeds void/plants/floor'
 for n in range(len(old_attrs[1])):
  before=list(old_m[1][n*8:n*8+8]);after=list(new_m[1][n*8:n*8+8]);d=authorized.get(n+512)
  if d:assert d['before_words']==before and d['after_words']==after,('Private drawing delta differs',n+512)
  else:assert before==after,('Unrelated private drawing words changed',n+512)
 appended=c['appended_metatiles'];assert len(new_attrs[1])==len(old_attrs[1])+len(appended)
 assert [d['metatile']for d in appended]==[944,945,946,947]
 for d in appended:
  n=d['metatile'];assert n>=512+len(old_attrs[1]);assert list(new_m[1][(n-512)*8:(n-512)*8+8])==d['words'];assert new_attrs[1][n-512]==d['attribute']
 oldlayouts=json.loads(get('data/layouts/layouts.json',True))['layouts'];newlayouts=load('data/layouts/layouts.json')['layouts'];native_maps=0
 authorized_pixels={(p['x'],p['y']):p for p in c['pixel_changes']}
 assert set(authorized_pixels)=={(x,y)for x in(2,10)for y in(1,2,3,10,11)}
 for name in c['maps']:
  m=load(f'data/maps/{name}/map.json');assert m==json.loads(get(f'data/maps/{name}/map.json',True)),(name,'Events/actors/warps changed')
  l=next(q for q in newlayouts if q['id']==m['layout']);old_l=next(q for q in oldlayouts if q['id']==l['id']);assert old_l==l
  assert get(l['border_filepath'])==get(l['border_filepath'],True)
  before=words(get(l['blockdata_filepath'],True));after=words(get(l['blockdata_filepath']));expected=list(before)
  assert len(c['raw_changes'])==4
  for d in c['raw_changes']:
   i=d['y']*12+d['x'];assert(d['x'],d['y'])in{(2,2),(10,2),(2,3),(10,3)};assert expected[i]==d['before'];expected[i]=d['after']
  assert list(after)==expected,(name,'Unreviewed raw map delta')
  for i,(v,w)in enumerate(zip(before,after)):
   xy=(i%12,i//12);assert v&0xfc00==w&0xfc00,(name,'Physics/elevation changed',xy)
   assert old_attrs[v&1023>=512][v%512]==new_attrs[w&1023>=512][w%512],(name,'Behavior/layer changed',xy)
   if xy in authorized_pixels:
    p=authorized_pixels[xy];assert hashlib.sha256(old_render(v&1023).tobytes()).hexdigest()==p['before_rgba_sha256'];assert hashlib.sha256(new_render(w&1023).tobytes()).hexdigest()==p['after_rgba_sha256'],(name,'Unexpected corrected pixels',xy)
   else:assert old_render(v&1023).tobytes()==new_render(w&1023).tobytes(),(name,'Unrelated rendered pixels changed',xy)
  floor_cells=[p for p in a['placements']if p['kind']=='floor'];assert len(floor_cells)==50
  for p in floor_cells:
   n=after[p['y']*12+p['x']]&1023;bottom,top=new_layers(n)
   assert bottom.getchannel('A').getextrema()==(255,255)and top.getchannel('A').getbbox()is None,('Floor not opaque ground/blank foreground',p['x'],p['y'])
  for x in(2,10):
   n=after[12+x]&1023;bottom,top=new_layers(n)
   assert bottom.getchannel('A').getextrema()==(255,255)and bottom.convert('RGB').getextrema()==((0,0),(0,0),(0,0))and top.getchannel('A').getbbox()is None,('Void not opaque black',x)
   for y in(2,3,10,11):
    bottom,top=new_layers(after[y*12+x]&1023);assert bottom.getchannel('A').getextrema()==(255,255),('Plant underlay transparent',x,y)
   alias_x=10 if x==10 else 1
   for y in(6,7,8):assert new_attrs[1][(after[y*12+alias_x]&1023)-512]&255==0x61
  native_maps+=1
 for path in ['tiles.png','metatiles.bin','metatile_attributes.bin']+[f'palettes/{i:02}.pal'for i in range(16)]:
  p='data/tilesets/secondary/hgss_temple/'+path;v,w=get(p),get(p,True)
  if path.endswith('.pal'):v,w=v.replace(b'\r\n',b'\n'),w.replace(b'\r\n',b'\n')
  assert v==w,('Shared Temple changed',path)
 result=dict(source_commit=BASE,maps=native_maps,unchanged_physics_cells=144*native_maps,raw_art_only_changes=4*native_maps,source_floor_ground_cells=50*native_maps,opaque_plant_underlays=8*native_maps,opaque_black_voids=2*native_maps,unchanged_visible_cells_per_gate=144-len(authorized_pixels),authorized_pixel_changes_per_gate=len(authorized_pixels),old140_glyphs_preserved=True,shared_temple_unchanged=True)
 print('Gate exact7d92 layer repair:50opaque-ground floors,8opaque plant underlays,2blackvoids;all144physics/attrs/aliases/events+oldglyphs/sharedTemple unchanged: PASS')
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--report');a=p.parse_args();r=validate()
 if a.report:Path(a.report).write_text(json.dumps(r,indent=2)+'\n')
