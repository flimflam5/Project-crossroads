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
  if n=='AzaleaTown':
   # The separately attributed donor kiln is the only authorised non-Gym
   # change. Verify its source pixels and attributes before excluding its
   # sixteen tiles from the unchanged-baseline comparison below.
   from hns_kiln_facade import D
   kp=p['kiln'];assert kp['origin']==[19,30] and kp['door']==[20,33]
   paths=[D/'tilesets/primary/johto_south_hns',D/'tilesets/secondary/azalea_town_hns'];sm=[];sa=[];sheets=[]
   for q in paths:
    z=(q/'metatiles.bin').read_bytes();sm.append(struct.unpack('<'+str(len(z)//2)+'H',z))
    z=(q/'metatile_attributes.bin').read_bytes();sa.append(struct.unpack('<'+str(len(z)//2)+'H',z));sheets.append(Image.open(q/'tiles.png'))
   dm=(D/'layouts/AzaleaTown_hns/map.bin').read_bytes();dm=struct.unpack('<'+str(len(dm)//2)+'H',dm)
   donor_pal={i:[tuple(int(v)//8 for v in line.split()) for line in (paths[int(i>=6)]/f'palettes/{i:02}.pal').read_text().splitlines()[3:]] for i in [0,2,7,10,11]}
   for i,dest in enumerate(kp['metatile_ids']):
    x,y=i%4,i//4;source=dm[(20+y)*62+37+x];ident=source&1023;k=int(ident>=640);j=ident-(640 if k else 0)
    raw=after[(30+y)*w+19+x];assert raw==kp['stamp'][i] and raw&1023==dest
    expected_attr=sa[k][j];expected_collision=source&0xc00
    if i==13:expected_attr=(expected_attr&~255)|0x60;expected_collision=0
    assert newres[2][1][dest-512]==expected_attr and raw&0xc00==expected_collision
    words=sm[k][j*8:j*8+8];target=newres[1][1][(dest-512)*8:(dest-511)*8]
    for sv,dv in zip(words,target):
     sid=sv&1023;dk=dv&1023
     if sid==0:assert dk==0;continue
     sk=int(sid>=640);sid-=640 if sk else 0;di=dk%512
     src=sheets[sk].crop((sid%16*8,sid//16*8,sid%16*8+8,sid//16*8+8)).tobytes()
     dst=newres[0][dk>=512].crop((di%16*8,di//16*8,di%16*8+8,di//16*8+8)).tobytes()
     assert src==dst and sv&0xc00==dv&0xc00
     assert donor_pal[sv>>12]==newres[3][dv>>12]
    allowed.add((19+x,30+y))
   door=m['warp_events'][7];assert (door['x'],door['y'],door['dest_map'],door['dest_warp_id'])==(20,33,'MAP_AZALEA_TOWN_CHARCOAL_KILN','0')
   kiln=load('data/maps/AzaleaTown_CharcoalKiln/map.json');assert kiln['warp_events'][0]['dest_map']==m['id'] and kiln['warp_events'][0]['dest_warp_id']=='7'
   anim=(R/'graphics/door_anims/hns_johto_general.png').read_bytes()
   assert anim==(D.parent/'graphics/door_anims/johtogeneral_hns.png').read_bytes()
   assert Image.open(R/'graphics/door_anims/hns_johto_general.png').size==(16,48)
   header=(R/'include/constants/azalea_kiln_door.h').read_text()
   assert f"METATILE_AZALEA_KILN_DOOR {kp['metatile_ids'][13]}" in header
   assert f"AZALEA_KILN_DOOR_PALETTE {kp['palette_mapping']['2']}" in header
   assert f"AZALEA_KILN_ORIGIN_X {kp['origin'][0]}" in header
   assert f"AZALEA_KILN_ORIGIN_Y {kp['origin'][1]}" in header
   assert 'AZALEA_KILN_WIDTH 4' in header and 'AZALEA_KILN_HEIGHT 4' in header
   source=(R/'src/field_door.c').read_text()
   entry=source.split('.metatileNum = METATILE_AZALEA_KILN_DOOR,',1)[1].split('},',1)[0]
   assert '.tileset = &gTileset_BlGymAzaleaSecondary' in entry and '.size = DOOR_SIZE_1x1' in entry and '.tiles = sDoorAnimTiles_AzaleaKiln' in entry
   # A preexisting save can stand on any old walkable tile of the new facade.
   # Prove at least a conservative non-warp escape from each; runtime Continue
   # tests are still required because this graph does not model object behavior.
   from collections import deque
   for yy in range(30,34):
    for xx in range(19,23):
     was=before[yy*w+xx]
     if was&0xc00 or was>>12!=3:continue
     queue=deque([(xx,yy)]);seen={(xx,yy)};escaped=False
     while queue:
      X,Y=queue.popleft()
      if not (19<=X<23 and 30<=Y<34):escaped=True;break
      for nx,ny in [(X-1,Y),(X+1,Y),(X,Y-1),(X,Y+1)]:
       if not (0<=nx<w and 0<=ny<h) or (nx,ny) in seen or (nx,ny)==(20,33):continue
       value=after[ny*w+nx]
       if value&0xc00 or value>>12!=3:continue
       seen.add((nx,ny));queue.append((nx,ny))
     assert escaped,('Old Azalea save cannot escape kiln footprint',xx,yy)
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
 print('Eight owner Gym assets, unchanged legacy pixels/events and reciprocal doors: PASS',count,'legacy metatiles; Azalea kiln has separately validated donor pixels/collision and old-cell escape')
 return set(plans)
if __name__=='__main__':validate()
