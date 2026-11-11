"""Independent per-layer RGB555/physics preservation for the four accepted facades.

Hardware flips/packing and palette indices may differ, displayed pixels and tile
attributes may not. Reference bytes come from immutable delivered QA08 B2, never
the mutable new authoring contract or generated facade spec.
"""
import functools,io,json,struct,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2];BASE='fd151242458efe5759b18650f35a5e5b2fa47e45'
@functools.lru_cache(None)
def data(path,old):return subprocess.check_output(['git','show',BASE+':'+path],cwd=R) if old else (R/path).read_bytes()
def words(b):return struct.unpack('<'+str(len(b)//2)+'H',b)
@functools.lru_cache(None)
def resources(old):
 from PIL import Image
 roots=['data/tilesets/primary/bl_gym_olivine','data/tilesets/secondary/bl_gym_olivine']
 sheets=[Image.open(io.BytesIO(data(p+'/tiles.png',old))) for p in roots];metas=[words(data(p+'/metatiles.bin',old)) for p in roots];attrs=[words(data(p+'/metatile_attributes.bin',old)) for p in roots]
 pals=[[tuple(int(c)//8 for c in line.split()) for line in data(roots[k>=6]+f'/palettes/{k:02}.pal',old).decode().splitlines()[3:]] for k in range(16)]
 return sheets,metas,attrs,pals
@functools.lru_cache(None)
def signature(tile,old):
 from PIL import Image
 sheets,metas,attrs,pals=resources(old);parts=[]
 for v in metas[tile>=512][tile%512*8:tile%512*8+8]:
  k=v&1023;i=k%512;patch=sheets[k>=512].crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8))
  if v&0x400:patch=patch.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if v&0x800:patch=patch.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  parts.append(tuple(pals[v>>12][index] if index else None for index in patch.tobytes()))
 return attrs[tile>=512][tile%512],tuple(parts)
def validate():
 city=json.loads(data('data/maps/OlivineCity/map.json',False));before_city=json.loads(data('data/maps/OlivineCity/map.json',True));current_ls=json.loads(data('data/layouts/layouts.json',False))['layouts'];old_ls=json.loads(data('data/layouts/layouts.json',True))['layouts'];l=next(l for l in current_ls if l['id']==city['layout']);old_l=next(l for l in old_ls if l['id']==before_city['layout']);assert (l['width'],l['height'])==(64,64) and (old_l['width'],old_l['height'])==(48,48)
 before=words(data(old_l['blockdata_filepath'],True));after=words(data(l['blockdata_filepath'],False));count=0
 for name,(sx,sy),(dx,dy),(w,h) in [('Joe',(10,6),(7,20),(4,4)),('neighbour',(20,6),(7,25),(4,4)),('Silph',(35,17),(29,36),(5,5)),('harbor',(11,29),(7,37),(4,4))]:
  for y in range(h):
   for x in range(w):
    a=before[(sy+y)*48+sx+x];b=after[(dy+y)*64+dx+x]
    assert a&0xfc00==b&0xfc00,(name,'Accepted exterior collision/elevation changed',x,y,hex(a),hex(b))
    assert signature(a&1023,True)==signature(b&1023,False),(name,'Accepted exterior layer RGB555/attribute changed',x,y,hex(a),hex(b))
    count+=1
 print('All four accepted Black Ledger exterior facades: exact immutable per-layer RGB555/attributes/collision/elevation PASS',count,'metatiles')
if __name__=='__main__':validate()
