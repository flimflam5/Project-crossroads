#!/usr/bin/env python3
"""Narrow immutable stage-art migration and native framebuffer regression.

All source coordinates, movement bits, metatile behavior and non-stage visible
pixels must match the actual 3f935 checkpoint. A packing change is not a license
to alter other furniture. This complements the separate13-bench/source checks.
"""
import argparse,functools,hashlib,io,json,struct,subprocess
from pathlib import Path
from PIL import Image,ImageChops
from build_hgss_theater_assets import COLORS
R=Path(__file__).resolve().parents[2];BASE='3f935d5e8600c5a280b9172b555edb35ca52b6c0'

def load(p):return json.loads((R/p).read_text())
def words(b):return struct.unpack('<'+str(len(b)//2)+'H',b)
@functools.lru_cache(None)
def data(p,old=False):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R) if old else (R/p).read_bytes()
def renderer(secondary,old=False):
 roots=['data/tilesets/primary/building','data/tilesets/secondary/'+secondary]
 sheets=[Image.open(io.BytesIO(data(p+'/tiles.png',old)))for p in roots];metas=[words(data(p+'/metatiles.bin',old))for p in roots];attrs=[words(data(p+'/metatile_attributes.bin',old))for p in roots]
 pals=[[tuple(int(v)//8 for v in line.split())for line in data(roots[int(i>=6)]+f'/palettes/{i:02}.pal',old).decode().splitlines()[3:]]for i in range(16)]
 @functools.lru_cache(None)
 def render(n):
  im=Image.new('RGBA',(16,16))
  for j,v in enumerate(metas[n>=512][n%512*8:n%512*8+8]):
   k=v&1023;i=k%512;part=sheets[k>=512].crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8))
   if v&0x400:part=part.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
   if v&0x800:part=part.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
   rgba=Image.new('RGBA',(8,8));rgba.putdata([tuple((c<<3)|(c>>2)for c in pals[v>>12][index])+(255,)if index else(0,0,0,0)for index in part.tobytes()]);im.alpha_composite(rgba,(j%2*8,j%4//2*8))
  return im
 return render,lambda n:attrs[n>=512][n%512]

def validate(screenshot=None):
 c=load('crossroads/hgss/contracts/theater-stage-qa09.json');assert c['source_commit']==BASE
 layouts=load('data/layouts/layouts.json')['layouts'];l=next(q for q in layouts if q['id']==c['layout_id']);before_layout=next(q for q in json.loads(data('data/layouts/layouts.json',True))['layouts']if q['id']==l['id']);expected=dict(before_layout,secondary_tileset='gTileset_HgssTheater');assert l==expected,('Unexpected Theater layout migration',l)
 before=list(words(data(l['blockdata_filepath'],True)));after=words(data(l['blockdata_filepath']));w,h=l['width'],l['height'];expected=before.copy();changed=set()
 for d in c['changes']:
  i=d['y']*w+d['x'];assert expected[i]==d['before'];expected[i]=d['after'];changed.add(i)
 audience=load('crossroads/hgss/contracts/theater-audience-qa10.json')
 assert audience['source_commit']=='5664fecee4337c5bdd442583e24cc91c09c0a0cd'
 for d in audience['raw_changes']:
  i=d['y']*w+d['x'];assert expected[i]==d['before'];expected[i]=d['after']
 audience_pixels={d['y']*w+d['x']:d for d in audience['pixel_changes']}
 assert list(after)==expected,'Unexpected stage cell or unrelated room change'
 assert len(changed)==69
 oldrender,oldattr=renderer('hgss_temple',True);newrender,newattr=renderer('hgss_theater')
 for i,(a,b)in enumerate(zip(before,after)):
  assert a&0xfc00==b&0xfc00,('Theater collision/elevation changed',i%w,i//w)
  assert oldattr(a&1023)==newattr(b&1023),('Theater behavior/layer changed',i%w,i//w)
  if i not in changed:
   if i in audience_pixels:assert hashlib.sha256(newrender(b&1023).tobytes()).hexdigest()==audience_pixels[i]['after_rgba_sha256'],('Audience pixels differ from exact independent contract',i%w,i//w)
   else:assert oldrender(a&1023).tobytes()==newrender(b&1023).tobytes(),('Unrelated visible pixel changed',i%w,i//w)
 # Every shared byte stays immutable, independently of the new private pool.
 for path in ['tiles.png','metatiles.bin','metatile_attributes.bin']+[f'palettes/{i:02}.pal'for i in range(16)]:
  p='data/tilesets/secondary/hgss_temple/'+path;a,b=data(p),data(p,True)
  # .gitattributes checks JASC text out with CRLF; Git blobs store LF. Keep
  # every character/color exact while ignoring that documented text filter.
  if path.endswith('.pal'):a,b=a.replace(b'\r\n',b'\n'),b.replace(b'\r\n',b'\n')
  assert a==b,('Shared Temple changed',path)
 assert json.loads(data('data/maps/EcruteakCity_DanceTheater/map.json'))==json.loads(data('data/maps/EcruteakCity_DanceTheater/map.json',True)),'Actors/scripts/warps changed'
 manifest=load('crossroads/hgss/art/theater/manifest.json');assert manifest['tiles']<=512 and manifest['metatiles']<=512
 result=dict(source_commit=BASE,authorized_changed_cells=69,audience_authorized_pixel_cells=95,unchanged_visible_cells=len(before)-69-95,collision_elevation_behavior_unchanged_cells=len(before),shared_temple_unchanged=True)
 if screenshot:
  frame=Image.open(screenshot).convert('RGB');assert frame.size==(240,160)
  a=manifest['specs']['stage_backdrop'];expected=Image.new('RGB',(192,32))
  for y in range(2):
   for x in range(12):expected.paste(newrender(a['start']+y*12+x).convert('RGB'),(x*16,y*16))
  matches=[]
  for y in range(129):
   for x in range(49):
    if ImageChops.difference(frame.crop((x,y,x+192,y+32)),expected).getbbox()is None:matches.append([x,y])
  assert len(matches)==1,('Compiled/native Theater backdrop does not match6144 expected pixels',matches)
  result.update(native_size=[240,160],compiled_backdrop_pixels_matched=6144,backdrop_top_left=matches[0])
  dest=Path(screenshot).with_suffix('.stage-pixels.json');dest.write_text(json.dumps(result,indent=2)+'\n')
 from validate_theater_audience import validate as validate_audience
 validate_audience()
 print('Theater stage exact69-cell art migration plus95 explicitly contracted audience pixels;all266physics and remaining102cells preserved;shared Temple unchanged: PASS')
 if screenshot:print('Compiled native stage6144/6144 pixels, gold crest/red lanterns: PASS')
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--screenshot');a=p.parse_args();validate(a.screenshot)
