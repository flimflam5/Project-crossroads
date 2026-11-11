#!/usr/bin/env python3
"""Static native16px-metatile room renders, not emulator screenshots/gameplay."""
import argparse,json,struct,functools
from pathlib import Path
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--output',default='build/qa09-olivine-room-review');a=p.parse_args();out=R/a.output;out.mkdir(parents=True,exist_ok=True)
ls={x['id']:x for x in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']};names=[v['name'] for v in json.loads((R/'crossroads/hgss/olivine-room-review.json').read_text())]
paths={'gTileset_HgssOlivineHome':'hgss_olivine_home','gTileset_HgssOlivineGym':'hgss_olivine_gym','gTileset_PokemonCenter':'pokemon_center','gTileset_Shop':'shop','gTileset_HgssCenterBasement':'hgss_center_basement','gTileset_HgssCenterReception':'hgss_center_reception','gTileset_HgssMart':'hgss_mart'}
for n in names:
 m=json.loads((R/f'data/maps/{n}/map.json').read_text());l=ls[m['layout']];w,h=l['width'],l['height'];p1=R/'data/tilesets/primary/building';p2=R/'data/tilesets/secondary'/paths[l['secondary_tileset']];sheets=[Image.open(d/'tiles.png') for d in [p1,p2]];metas=[];pals=[]
 for d in [p1,p2]:
  b=(d/'metatiles.bin').read_bytes();metas.append(struct.unpack('<'+str(len(b)//2)+'H',b))
 for bank in range(13):
  d=p1 if bank<6 else p2;pals.append([tuple(map(int,x.split())) for x in (d/f'palettes/{bank:02}.pal').read_text().splitlines()[3:]])
 @functools.lru_cache(None)
 def tile(n):
  im=Image.new('RGBA',(16,16))
  for j,v in enumerate(metas[n//512][(n%512)*8:(n%512)*8+8]):
   k=v&1023;i=k%512;part=sheets[k//512].crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8));patch=Image.new('RGBA',(8,8));patch.putdata([pals[v>>12][c]+(255,) if c else (0,0,0,0) for c in part.tobytes()])
   if v&0x400:patch=patch.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
   if v&0x800:patch=patch.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
   im.alpha_composite(patch,((j%2)*8,(j%4//2)*8))
  return im
 b=(R/l['blockdata_filepath']).read_bytes();t=struct.unpack('<'+str(w*h)+'H',b);im=Image.new('RGB',(w*16,h*16),(0,0,0))
 for i,v in enumerate(t):q=tile(v&1023);im.paste(q,(i%w*16,i//w*16),q)
 im.save(out/(n+'.png'))
 # Separate annotated collision/actor/warp view. Decorative image remains clean.
 debug=im.copy();d=ImageDraw.Draw(debug)
 for i,v in enumerate(t):
  if v&0xc00:d.rectangle((i%w*16,i//w*16,i%w*16+15,i//w*16+15),outline=(120,40,40))
 for i,e in enumerate(m['warp_events']):d.rectangle((e['x']*16,e['y']*16,e['x']*16+15,e['y']*16+15),outline='cyan');d.text((e['x']*16,e['y']*16),str(i),fill='cyan')
 for e in m['object_events']:d.ellipse((e['x']*16+3,e['y']*16+3,e['x']*16+13,e['y']*16+13),fill='yellow')
 debug.save(out/(n+'-collision.png'))
print('Static native16px room/collision renders; not emulator screenshots:',out)
