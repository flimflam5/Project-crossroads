#!/usr/bin/env python3
"""Independent owner asset, legacy pixel/save-contract and two-door validation."""
import hashlib,json,struct,copy
from pathlib import Path
from PIL import Image
from build_eight_gym_integration import BASE,B,A,CODES,SOURCES,normalize_map,overlay,interior_overlay,symbol,source_contract,source_bytes
R=Path(__file__).resolve().parents[2]
def validate():
 def load(p):return json.loads((R/p).read_text())
 plans=load('crossroads/art/eight_gyms_v1/integration.json')['cities'];ls={l['id']:l for l in load('data/layouts/layouts.json')['layouts']};meta_cache={};count=0
 for name,sha in load('crossroads/art/eight_gyms_v1/SHA256SUMS.json').items():assert hashlib.sha256((A/name).read_bytes()).hexdigest()==sha,('Owner archive altered',name)
 def resources(primary,secondary):
  paths=[R/'data/tilesets'/k/d for k,d in [primary,secondary]];ms=[];at=[];pals=[]
  for p in paths:
   b=(p/'metatiles.bin').read_bytes();ms.append(struct.unpack('<'+str(len(b)//2)+'H',b));b=(p/'metatile_attributes.bin').read_bytes();at.append(struct.unpack('<'+str(len(b)//2)+'H',b))
  for i in range(16):pals.append([tuple(int(v)//8 for v in line.split()) for line in (paths[0 if i<6 else 1]/f'palettes/{i:02}.pal').read_text().splitlines()[3:]])
  return [Image.open(p/'tiles.png') for p in paths],ms,at,pals
 def signature(res,id):
  sheets,ms,at,pals=res;out=[]
  for v in ms[id>=512][id%512*8:id%512*8+8]:
   num=v&1023;k=num%512;im=sheets[num>=512].crop((k%16*8,k//16*8,k%16*8+8,k//16*8+8))
   if v&0x400:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
   if v&0x800:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
   out.append(tuple(pals[v>>12][i] if i else None for i in im.tobytes()))
  return at[id>=512][id%512],tuple(out)
 for n,p in plans.items():
  c=source_contract(n);m=load(f'data/maps/{n}/map.json');l=ls[m['layout']];w,h=l['width'],l['height'];assert normalize_map(n,m)==c['map'],(n,'Unrelated city events changed')
  wanted=dict(c['layout'],primary_tileset=symbol(n,True),secondary_tileset=symbol(n));assert l==wanted
  old=source_bytes(n,c);b=(R/l['blockdata_filepath']).read_bytes();assert b==overlay(n,old,w,h),(n,'Undocumented layout change')
  before=struct.unpack('<'+str(w*h)+'H',old);after=struct.unpack('<'+str(w*h)+'H',b);oldres=resources(*[(SOURCES[c['layout'][k]][0],SOURCES[c['layout'][k]][1]) for k in ['primary_tileset','secondary_tileset']]);newres=resources(('primary','bl_gym_'+p['code']),('secondary','bl_gym_'+p['code']))
  allowed=set()
  for x,y,ww,hh in [p['old_footprint'],[*p['origin'],8,7]]:allowed|={(X,Y) for Y in range(y,y+hh) for X in range(x,x+ww)}
  used=set()
  for i,(a,b) in enumerate(zip(before,after)):
   if (i%w,i//w) in allowed:continue
   assert a==b,(n,'Outside Gym footprint changed',i%w,i//w);used.add(a&1023)
  for id in used:assert signature(oldres,id)==signature(newres,id),(n,'Legacy pixels/palette/attributes changed',hex(id))
  assert max((v&1023 for words in newres[1] for v in words),default=0)<1024
  for i,point in zip(p['exterior_warps'],p['doors']):
   e=m['warp_events'][i];assert [e['x'],e['y']]==point;inside=load('data/maps/'+p['interior']+'/map.json');back=inside['warp_events'][int(e['dest_warp_id'])];assert back['dest_map']==m['id'] and int(back['dest_warp_id'])==i
   raw=after[point[1]*w+point[0]];assert raw&0xc00==0 and newres[2][raw&1023>=512][(raw&1023)%512]&255==0x60
  assert normalize_map(p['interior'],inside)==c['interior'],(n,'Unrelated Gym events changed')
  il=ls[inside['layout']];before_inside=(R/f'crossroads/hgss/authoring/{inside["name"]}.bin').read_bytes() if 'raw_path' in c else (B/(inside['name']+'.bin')).read_bytes();assert (R/il['blockdata_filepath']).read_bytes()==interior_overlay(inside['name'],before_inside,il['width'],il['height']),(n,'Unrelated interior terrain changed')
  asset=Image.open(A/'assets'/p['code']/'building.png');_,ms,at,pals=newres
  for cell,id in enumerate(p['metatile_ids']):
   x,y=cell%8,cell//8;words=ms[1][(id-512)*8:(id-511)*8]
   assert at[1][id-512]>>12==(1 if y>=5 else 0)
   for j,v in enumerate(words[4:]):
    tile=v&1023;k=tile%512;actual=newres[0][tile>=512].crop((k%16*8,k//16*8,k%16*8+8,k//16*8+8))
    if v&0x400:actual=actual.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if v&0x800:actual=actual.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    expected=asset.crop((x*16+j%2*8,y*16+j//2*8,x*16+j%2*8+8,y*16+j//2*8+8)).tobytes();assert actual.tobytes()==expected,(n,'Owner Gym pixels changed',cell,j)
  count+=len(used)
 print('Eight owner asset checksums/pixel identity, all non-Gym pixels/collision/events, stable IDs and reciprocal two-door pairs: PASS',count,'legacy metatiles')
 return set(plans)
if __name__=='__main__':validate()
