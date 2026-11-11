#!/usr/bin/env python3
"""Exact immutable V9→V10 Theater material delta and compiled pixel check.

The audience image is a reference-backed art correction, never permission to
change source geometry, old stage art, other rooms or shared Temple resources.
"""
import argparse,functools,hashlib,io,json,struct,subprocess
from pathlib import Path
from PIL import Image,ImageChops
from hgss_theater_audience_art import COLORS,PALETTE_BANK
R=Path(__file__).resolve().parents[2]
BASE='5664fecee4337c5bdd442583e24cc91c09c0a0cd'
def load(p):return json.loads((R/p).read_text())
def words(b):return struct.unpack('<'+str(len(b)//2)+'H',b)
@functools.lru_cache(None)
def get(p,old=False):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R)if old else(R/p).read_bytes()
def resource(old=False):
 roots=['data/tilesets/primary/building','data/tilesets/secondary/hgss_theater']
 sheets=[Image.open(io.BytesIO(get(p+'/tiles.png',old)))for p in roots];metas=[words(get(p+'/metatiles.bin',old))for p in roots];attrs=[words(get(p+'/metatile_attributes.bin',old))for p in roots]
 pals=[[tuple(int(v)//8 for v in row.split())for row in get(roots[int(i>=6)]+f'/palettes/{i:02}.pal',old).decode().splitlines()[3:]]for i in range(16)]
 @functools.lru_cache(None)
 def render(n):
  im=Image.new('RGBA',(16,16))
  for j,v in enumerate(metas[n>=512][n%512*8:n%512*8+8]):
   k=v&1023;i=k%512;part=sheets[k>=512].crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8))
   if v&0x400:part=part.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
   if v&0x800:part=part.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
   patch=Image.new('RGBA',(8,8));patch.putdata([tuple((c<<3)|(c>>2)for c in pals[v>>12][index])+(255,)if index else(0,0,0,0)for index in part.tobytes()]);im.alpha_composite(patch,(j%2*8,j%4//2*8))
  return im
 return sheets,metas,attrs,pals,render
def validate(screenshot=None):
 c=load('crossroads/hgss/contracts/theater-audience-qa10.json');assert c['source_commit']==BASE and c['palette_bank']==PALETTE_BANK==8
 m=load('data/maps/EcruteakCity_DanceTheater/map.json');assert m==json.loads(get('data/maps/EcruteakCity_DanceTheater/map.json',True))
 layouts=load('data/layouts/layouts.json')['layouts'];l=next(x for x in layouts if x['id']==m['layout']);before_l=next(x for x in json.loads(get('data/layouts/layouts.json',True))['layouts']if x['id']==l['id']);assert l==before_l
 before=words(get(l['blockdata_filepath'],True));after=words(get(l['blockdata_filepath']));expected=list(before);raw_changed=set()
 for d in c['raw_changes']:
  i=d['y']*14+d['x'];assert expected[i]==d['before'] and d['y']>=9 and d['before']&1023==513 and d['after']&1023==929;expected[i]=d['after'];raw_changed.add(i)
 assert len(raw_changed)==82 and tuple(expected)==after
 old_s,old_m,old_a,old_p,old_render=resource(True);new_s,new_m,new_a,new_p,new_render=resource(False)
 authorized={p['y']*14+p['x']:p for p in c['pixel_changes']};assert len(authorized)==95 and sum(p['kind']=='audience_cushion'for p in authorized.values())==13
 facts=load('crossroads/hgss/canonical_events/ecruteak-interior-geometry.json')['MAP_ECRUTEAK_DANCE_THEATER'];source_seats={(int(p['tile_x']),int(p['tile_z']))for chunk in facts['chunks']for p in chunk['props']if p['model']==56};actual_seats={(i%14,i//14)for i,v in enumerate(after)if v&1023==895};assert source_seats==actual_seats and len(actual_seats)==13
 for i,(a,b)in enumerate(zip(before,after)):
  assert a&0xfc00==b&0xfc00 and old_a[a&1023>=512][a%512]==new_a[b&1023>=512][b%512],('Audience changed collision/elevation/behavior/layer',i%14,i//14)
  if i in authorized:
   p=authorized[i];assert a&1023==p['before_metatile']and b&1023==p['after_metatile'];assert hashlib.sha256(old_render(a&1023).tobytes()).hexdigest()==p['before_rgba_sha256'];assert hashlib.sha256(new_render(b&1023).tobytes()).hexdigest()==p['after_rgba_sha256'],('Unexpected audience pixels',i%14,i//14)
  else:assert old_render(a&1023).tobytes()==new_render(b&1023).tobytes(),('Unrelated room/stage pixels changed',i%14,i//14)
 # New ground/cushion art uses only bottom glyphs. Opaque floor must never be
 # put on the foreground layer, even when raw collision bits are unchanged.
 for n in(895,929):assert new_m[1][(n-512)*8+4:(n-512)*8+8]==(0,0,0,0)
 assert len(new_a[1])==len(old_a[1])+1 and new_a[1][:-1]==old_a[1]and new_a[1][-1]==old_a[1][1]
 for n in range(len(old_a[1])):
  if n!=895-512:assert old_m[1][n*8:n*8+8]==new_m[1][n*8:n*8+8],('Unrelated private metatile changed',n+512)
 manifest=load('crossroads/hgss/art/theater/manifest.json');old_manifest=json.loads(get('crossroads/hgss/art/theater/manifest.json',True));assert manifest['tiles']<=512 and manifest['metatiles']==418
 for i in range(old_manifest['tiles']):
  box=(i%16*8,i//16*8,i%16*8+8,i//16*8+8);assert old_s[1].crop(box).tobytes()==new_s[1].crop(box).tobytes(),('Old private glyph changed',i)
 used_before={v&1023 for v in before};assert all(v>>12!=8 for n in used_before for v in old_m[1][(n-512)*8:(n-511)*8]),'Palette8 was already in use'
 for i in range(16):
  if i!=8:assert old_p[i]==new_p[i],('Unrelated private palette changed',i)
 assert new_p[8]==[tuple(v//8 for v in color)for color in COLORS]
 for p in ['tiles.png','metatiles.bin','metatile_attributes.bin']+[f'palettes/{i:02}.pal'for i in range(16)]:
  path='data/tilesets/secondary/hgss_temple/'+p;a,b=get(path),get(path,True)
  if p.endswith('.pal'):a,b=a.replace(b'\r\n',b'\n'),b.replace(b'\r\n',b'\n')
  assert a==b,('Shared Temple changed',p)
 result=dict(source_commit=BASE,raw_floor_changes=82,source_cushions=13,authorized_pixel_cells=95,unchanged_pixel_cells=171,unchanged_physics_cells=266)
 if screenshot:
  frame=Image.open(screenshot).convert('RGB');assert frame.size==(240,160);checked=0;records=[]
  # Actual controller capture at(8,11): the upper-center row deliberately has
  # no cushion beneath Joe's head, so all13 seats are fully unobscured.
  for x,y in sorted(actual_seats|{(3,11)}):
   xx=(x+7-8)*16;yy=(y+7-11)*16-40;assert 0<=xx<=224 and 0<=yy<=144
   expected_tile=new_render(after[y*14+x]&1023).convert('RGB');assert ImageChops.difference(frame.crop((xx,yy,xx+16,yy+16)),expected_tile).getbbox()is None,('Compiled checker/cushion pixels mismatch',x,y)
   checked+=256;records.append(dict(source_cell=[x,y],screen=[xx,yy],pixels=256))
  assert checked==3584;result.update(native_size=[240,160],compiled_audience_pixels_matched=checked,records=records);Path(screenshot).with_suffix('.audience-pixels.json').write_text(json.dumps(result,indent=2)+'\n')
 print('Theater actual green checker/13purple cushions: exact82raw/95pixel-cell migration;171othercells+all266physics/actors/events/IDs/stage/common resources preserved: PASS')
 if screenshot:print('Compiled checker+all13 cushions3584/3584 native pixels: PASS')
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--screenshot');a=p.parse_args();validate(a.screenshot)
