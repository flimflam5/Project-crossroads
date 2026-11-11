#!/usr/bin/env python3
"""Exact QA08 A1 pixel/layer/physics preservation outside two new gate models.

Read an immutable commit, never the mutable generator authoring input. This
permits hardware tile/flip packing but no collateral recoloring or terrain edit.
"""
import functools,io,json,struct,subprocess
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2];BASE='d3ab461912c51270b84d2eb8d9d7b3ee7a255717'
@functools.lru_cache(None)
def data(p,old=False):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R) if old else (R/p).read_bytes()
def js(p,old=False):return json.loads(data(p,old))
def words(b):return struct.unpack('<'+str(len(b)//2)+'H',b)
@functools.lru_cache(None)
def resource(p,s,old):
 roots=['data/tilesets/primary/'+p,'data/tilesets/secondary/'+s]
 sheets=[Image.open(io.BytesIO(data(d+'/tiles.png',old))) for d in roots];ms=[words(data(d+'/metatiles.bin',old)) for d in roots];ats=[words(data(d+'/metatile_attributes.bin',old)) for d in roots]
 palette_roots=list(roots)
 if p in ('hgss_ecruteak_buffer','hgss_ecruteak_gate_buffer'):palette_roots[0]='data/tilesets/primary/general' # aliases gTilesetPalettes_General
 pals=[[tuple(int(v)//8 for v in line.split()) for line in data(palette_roots[i>=6]+f'/palettes/{i:02}.pal',old).decode().splitlines()[3:]] for i in range(16)]
 return sheets,ms,ats,pals
@functools.lru_cache(None)
def signature(p,s,n,old):
 sheets,ms,ats,pals=resource(p,s,old);parts=[]
 for v in ms[n>=512][n%512*8:n%512*8+8]:
  i=v&1023;k=i%512;tile=sheets[i>=512].crop((k%16*8,k//16*8,k%16*8+8,k//16*8+8))
  if v&0x400:tile=tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if v&0x800:tile=tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  parts.append(tuple(pals[v>>12][c] if c else None for c in tile.tobytes()))
 return ats[n>=512][n%512],tuple(parts)
def validate():
 assert js('data/maps/map_groups.json')==js('data/maps/map_groups.json',True)
 assert js('src/data/heal_locations.json')==js('src/data/heal_locations.json',True)
 oldls=js('data/layouts/layouts.json',True)['layouts'];ls=js('data/layouts/layouts.json')['layouts'];assert [l['id'] for l in ls]==[l['id'] for l in oldls]
 byid={l['id']:l for l in ls};oldbyid={l['id']:l for l in oldls};count=0;gatecells=0
 spec=js('crossroads/hgss/art/native-manifest.json')['specs']['gate']
 for n in ['EcruteakCity','JohtoRoute37','JohtoRoute38','JohtoRoute42']:
  m=js(f'data/maps/{n}/map.json');old=js(f'data/maps/{n}/map.json',True);l=byid[m['layout']];ol=oldbyid[old['layout']];w,h=l['width'],l['height'];assert (w,h)==(ol['width'],ol['height'])
  before=words(data(ol['blockdata_filepath'],True));after=words(data(l['blockdata_filepath']))
  op,os=('bl_gym_ecruteak','bl_gym_ecruteak') if n=='EcruteakCity' else ('hgss_ecruteak_buffer','western_city')
  for i,(a,b) in enumerate(zip(before,after)):
   x,y=i%w,i//w;local=None
   if n=='EcruteakCity' and x<7 and 36<=y<43:local=(x,y-36)
   elif n=='EcruteakCity' and x>=60 and 45<=y<52:local=(x-60,y-45)
   elif n=='JohtoRoute42' and x<3 and 12<=y<19:local=(x+4,y-12)
   if local:
    xx,yy=local;wanted=spec['start']+yy*7+xx+(0x3000 if 1<=yy<=3 else 0x400);assert b==wanted,(n,'Gate roof/tunnel/front wall footprint',x,y)
    gatecells+=1;continue
   if n=='EcruteakCity' and (x,y) in {(59,52),(9,40)}:assert b==0x403;continue # Existing signs, relocated outside door/wall footprints.
   if n=='EcruteakCity' and (x,y)==(8,37):assert b==0x3000|js('crossroads/hgss/art/native-manifest.json')['specs']['paving'];continue
   assert a&0xfc00==b&0xfc00,(n,'Unrelated collision/elevation changed',x,y)
   np,ns=('bl_gym_ecruteak','bl_gym_ecruteak') if n=='EcruteakCity' else ('hgss_ecruteak_gate_buffer','western_city')
   assert signature(op,os,a&1023,True)==signature(np,ns,b&1023,False),(n,'Accepted pixels/layers/behavior changed',x,y,hex(a),hex(b))
   count+=1
  if n!='EcruteakCity':
   assert l['primary_tileset']=='gTileset_HgssEcruteakGateBuffer' and l['secondary_tileset']=='gTileset_WesternCity'
 assert gatecells==98
 protection=js('crossroads/hgss/contracts/ecruteak-route-buffers-qa08.json')
 assert protection['source_commit']==BASE
 for n,r in protection['maps'].items():
  assert js(f'data/maps/{n}/map.json',True)==r['map'] and words(data(r['layout']['blockdata_filepath'],True))==words(bytes.fromhex(r['raw']))
 views=0
 for view in protection['neighbor_views']:
  for tile in set(view['tiles']):
   assert signature('hgss_ecruteak_buffer','western_city',tile&1023,True)==signature('hgss_ecruteak_gate_buffer','western_city',tile&1023,False),(view['host'],view['neighbor'],'Neighbor scrolling pixels changed',hex(tile))
   views+=1
 for i in range(49):
  assert signature('bl_gym_ecruteak','bl_gym_ecruteak',0x100+i,False)==signature('hgss_ecruteak_gate_buffer','western_city',0x100+i,False),('Gate decodes differently across city/route seam',i)
 print('All six adjacent-map scrolling strips preserve their original decoded pixels/attributes:',views,'unique-per-view tiles; all49 gate cells decode identically on both sides: PASS')
 print('Immutable QA08 A1 IDs/heals and exact per-layer pixels/attributes/collision outside98 gate cells: PASS',count,'preserved cells; no engine limits increased')
if __name__=='__main__':validate()
