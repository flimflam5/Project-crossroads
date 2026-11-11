#!/usr/bin/env python3
"""Native16px-metatile static overview, explicitly separate from emulator footage."""
import argparse,functools,struct
from pathlib import Path
from PIL import Image
from validate_ecruteak_family import js,data,resource
p=argparse.ArgumentParser();p.add_argument('--map',default='EcruteakCity');p.add_argument('--baseline',action='store_true');p.add_argument('--output',required=True);a=p.parse_args()
m=js(f'data/maps/{a.map}/map.json',a.baseline);ls={l['id']:l for l in js('data/layouts/layouts.json',a.baseline)['layouts']};l=ls[m['layout']];w,h=l['width'],l['height'];raw=data(l['blockdata_filepath'],a.baseline);raw=struct.unpack('<'+str(w*h)+'H',raw)
primary,secondary=('bl_gym_ecruteak','bl_gym_ecruteak') if a.map=='EcruteakCity' else ('hgss_ecruteak_buffer' if a.baseline else 'hgss_ecruteak_gate_buffer','western_city');sheets,metas,attrs,pals=resource(primary,secondary,a.baseline)
@functools.lru_cache(None)
def tile(n):
 out=Image.new('RGBA',(16,16))
 for j,v in enumerate(metas[n>=512][n%512*8:n%512*8+8]):
  k=v&1023;i=k%512;source=sheets[k>=512].crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8))
  if v&0x400:source=source.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if v&0x800:source=source.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  pix=Image.new('RGBA',(8,8));pix.putdata([tuple((c<<3)|(c>>2) for c in pals[v>>12][index])+(255,) if index else (0,0,0,0) for index in source.tobytes()]);out.alpha_composite(pix,((j%4)%2*8,(j%4)//2*8))
 return out
image=Image.new('RGB',(w*16,h*16))
for i,v in enumerate(raw):image.paste(tile(v&1023),(i%w*16,i//w*16),tile(v&1023))
dest=Path(a.output);dest.parent.mkdir(parents=True,exist_ok=True);image.save(dest)
print('Static daytime layout overview',a.map,image.size,'not emulator gameplay:',dest)
