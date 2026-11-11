#!/usr/bin/env python3
"""HGSS-derived Olivine homes/cafe/services/Gym; original GBA furniture and steel art.

This owns interiors only. Canonical shape/prop facts are immutable reference input;
all IDs are preserved or appended. Accepted Black Ledger office/home rooms remain
untouched. Rewards, trades, seals, badges and source story actors are not imported.
"""
import argparse,copy,hashlib,json,re,struct
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[2]
FACT_PATH='crossroads/hgss/canonical_events/olivine-interior-geometry.json'
NEW=['OlivineCity_FishingHouse','OlivineCity_TradeHouse','OlivineCity_SealHouse','OlivineCity_Cafe','OlivineCity_PokemonCenter_B1F']
OWNED=set(NEW+['OlivineCity_PokemonCenter_1F','OlivineCity_Mart','OlivineCity_Gym','OlivineCity_Gym_Arena'])
TARGETS=[('MAP_OLIVINE_NORTHWEST_HOUSE',NEW[0],9),('MAP_OLIVINE_NORTH_HOUSE',NEW[1],10),('MAP_OLIVINE_NORTHEAST_HOUSE',NEW[2],11),('MAP_OLIVINE_CAFE',NEW[3],12)]
def load(p):return json.loads((R/p).read_text())
def unpack(p):b=p.read_bytes();return list(struct.unpack('<'+str(len(b)//2)+'H',b))
def mid(n):return 'MAP_HGSS_'+n.upper()
def generate(check=False):
 from PIL import Image
 from hgss_room_projection import project,ART
 facts=load(FACT_PATH);reviews=[]
 def write(p,b):
  p=R/p
  if isinstance(b,str):b=b.encode()
  if p.suffix=='.pal':b=b.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
  if check:assert p.exists() and p.read_bytes()==b,('Regenerate Olivine rooms',str(p))
  elif not p.exists() or p.read_bytes()!=b:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 def js(p,v):write(p,json.dumps(v,indent=2)+'\n')
 # Isolate and repack only house furniture; no temple/tower art in the new rooms.
 td=R/'data/tilesets/secondary/hgss_temple';tm=unpack(td/'metatiles.bin');ta=unpack(td/'metatile_attributes.bin');ts=Image.open(td/'tiles.png');home_sheet=Image.new('P',(128,256));home_sheet.putpalette(ts.getpalette());home_words=[];home_attrs=[];home_art={};unique={};cursor=0
 def tile_alloc(im):
  nonlocal cursor
  key=im.tobytes()
  if key not in unique:
   assert cursor<512;unique[key]=512+cursor;home_sheet.paste(im,(cursor%16*8,cursor//16*8));cursor+=1
  return unique[key]
 for name in ['void','wood','house_wall','fridge','cabinet','television','dining_table','chair','prayer_table','exit','house_kitchen','house_window']:
  a=ART[name];home_art[name]=dict(a,start=512+len(home_attrs))
  for n in range(a['start'],a['start']+a['width']*a['height']):
   row=[]
   for v in tm[(n-512)*8:(n-511)*8]:
    k=v&1023
    if k<512:row.append(v);continue
    i=k-512;im=ts.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8));row.append((v&~1023)|tile_alloc(im))
   home_words.extend(row);home_attrs.append(ta[n-512])
 # HGSS cafe has one3x3 round table; resample the native furniture footprint,
 # preserving its palette. This is tile conversion, not a generic room pattern.
 a=ART['dining_table'];piece=Image.new('P',(32,32));piece.putpalette(ts.getpalette())
 for yy in range(2):
  for xx in range(2):
   n=a['start']+yy*2+xx
   for j,v in enumerate(tm[(n-512)*8:(n-511)*8]):
    i=(v&1023)-512
    if i<0:continue
    im=ts.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8))
    if v&0x400:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if v&0x800:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    if j>=4:piece.paste(im,(xx*16+(j%2)*8,yy*16+(j%4//2)*8))
 piece=piece.resize((48,48),Image.Resampling.NEAREST);home_art['cafe_table']=dict(start=512+len(home_attrs),width=3,height=3)
 for y in range(3):
  for x in range(3):
   top=[tile_alloc(piece.crop((x*16+dx,y*16+dy,x*16+dx+8,y*16+dy+8)))|0x6000 for dx,dy in [(0,0),(8,0),(0,8),(8,8)]];home_words.extend(home_words[home_art['wood']['start']%512*8:home_art['wood']['start']%512*8+4]+top);home_attrs.append(0x1000)
 # Explicit native counter variants retain graphics and make service interaction
 # work across the one-cell serving counter at sourcex10.
 home_art['counter']=dict(start=512+len(home_attrs),width=1,height=1);n=home_art['prayer_table']['start']-512;home_words.extend(home_words[n*8:n*8+8]);home_attrs.append(0x1080)
 # Actual cafe raster uses cream/checkered tiles. Reuse native GBA Center
 # floor pixels in a private spare palette, never HGSS reference pixels.
 pc=R/'data/tilesets/secondary/pokemon_center';pm=unpack(pc/'metatiles.bin');ps=Image.open(pc/'tiles.png');floorrefs=[]
 for v in pm[16:20]:
  i=(v&1023)-512;floorrefs.append(tile_alloc(ps.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8)))|0x7000)
 home_art['cafe_floor']=dict(start=512+len(home_attrs),width=1,height=1);home_words.extend(floorrefs+[0]*4);home_attrs.append(0x1000)
 for name in ['cafe_table','chair','counter','house_kitchen']:
  a=home_art[name];home_art['cafe_'+name]=dict(a,start=512+len(home_attrs))
  for n in range(a['start']-512,a['start']-512+a['width']*a['height']):home_words.extend(floorrefs+home_words[n*8+4:n*8+8]);home_attrs.append(home_attrs[n])
 # Actual HGSS model23 potted plants. Foreground glyphs use their native
 # private green/purple palette8; house/cafe ground remains its own texture.
 pa=unpack(pc/'metatile_attributes.bin')
 for title,ground in [('house_plant',home_words[(home_art['wood']['start']-512)*8+4:(home_art['wood']['start']-512)*8+8]),('cafe_plant',floorrefs)]:
  home_art[title]=dict(start=512+len(home_attrs),width=1,height=2)
  for source_id in [0x20a,0x212]:
   top=[]
   for v in pm[(source_id-512)*8+4:(source_id-512)*8+8]:
    i=(v&1023)-512;top.append(tile_alloc(ps.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8)))|(v&0xc00)|0x8000)
   home_words.extend(ground+top);home_attrs.append(pa[source_id-512])
 home_root='data/tilesets/secondary/hgss_olivine_home';Path(R/home_root).mkdir(parents=True,exist_ok=True)
 if check:assert Image.open(R/home_root/'tiles.png').tobytes()==home_sheet.tobytes()
 else:home_sheet.save(R/home_root/'tiles.png',bits=4)
 write(home_root+'/metatiles.bin',struct.pack('<'+str(len(home_words))+'H',*home_words));write(home_root+'/metatile_attributes.bin',struct.pack('<'+str(len(home_attrs))+'H',*home_attrs))
 for i in range(16):write(home_root+f'/palettes/{i:02}.pal',(pc/'palettes/06.pal').read_bytes() if i==7 else (pc/'palettes/08.pal').read_bytes() if i==8 else (td/f'palettes/{i:02}.pal').read_bytes())
 # New original, reference-directed silver/salmon/hexagonal gym components.
 artdir=R/'crossroads/hgss/art/olivine-rooms';src=Image.open(artdir/'gym-source.png').convert('RGBA');pal=[0,0,0]+[v for c in [(239,237,234),(211,211,214),(177,176,183),(139,141,152),(99,103,117),(65,64,76),(193,143,130),(225,175,155),(237,202,169),(154,112,107),(90,88,102),(223,197,87),(253,230,141),(119,117,134),(43,42,54)] for v in c];ref=Image.new('P',(1,1));ref.putpalette(pal+[0]*720);gym_sheet=Image.new('P',(128,256));gym_sheet.putpalette(pal);gw=[];ga=[];gs={};gcache={};gc=0
 def alloc(im):
  nonlocal gc
  k=im.tobytes()
  if k not in gcache:
   assert gc<512;gcache[k]=512+gc;gym_sheet.paste(im,(gc%16*8,gc//16*8));gc+=1
  return gcache[k]
 empty=alloc(Image.new('P',(8,8)))|0x6000
 sizes=[('hex',(32,32)),('runway',(16,16)),('wall',(32,32)),('pillar',(16,64)),('rail',(48,16)),('stairs',(32,32)),('canopy',(80,64)),('pylon',(16,32))]
 for i,(name,size) in enumerate(sizes):
  x,y=i%4,i//4;im=src.crop((round(x*src.width/4+12),round(y*src.height/2+12),round((x+1)*src.width/4-12),round((y+1)*src.height/2-12)));alpha=im.getchannel('A').point(lambda n:255 if n>=200 else 0);im.putalpha(alpha);bbox=alpha.getbbox();assert bbox;im=im.crop(bbox).resize(size,Image.Resampling.NEAREST);q=im.convert('RGB').quantize(palette=ref,dither=Image.Dither.NONE);v=bytearray(q.tobytes());alpha=im.getchannel('A').tobytes()
  for k in range(len(v)):v[k]=0 if alpha[k]<128 else v[k] or 1
  q=Image.frombytes('P',size,bytes(v));q.putpalette(pal);q.info['transparency']=0
  if not check:q.save(artdir/(name+'-native.png'),bits=4)
  w,h=size[0]//16,size[1]//16;gs[name]=dict(start=512+len(ga),width=w,height=h)
  for yy in range(h):
   for xx in range(w):
    top=[alloc(q.crop((xx*16+dx,yy*16+dy,xx*16+dx+8,yy*16+dy+8)))|0x6000 for dx,dy in [(0,0),(8,0),(0,8),(8,8)]]
    floor='runway' if name in ['stairs','canopy','rail'] else 'hex';ground=[empty]*4 if name in ['hex','runway'] else gw[(gs[floor]['start']-512)*8+4:(gs[floor]['start']-512)*8+8];gw.extend(ground+top);ga.append(0x1000)
 gs['void']=dict(start=512+len(ga),width=1,height=1);gw.extend([empty]*8);ga.append(0x1000)
 gs['warp']=dict(start=512+len(ga),width=1,height=1);j=gs['runway']['start']-512;gw.extend(gw[j*8:j*8+8]);ga.append(0x1061)
 gs['exit']=dict(start=512+len(ga),width=1,height=1);gw.extend(gw[j*8:j*8+8]);ga.append(0x1065)
 gym_root='data/tilesets/secondary/hgss_olivine_gym';(R/gym_root).mkdir(parents=True,exist_ok=True)
 if check:assert Image.open(R/gym_root/'tiles.png').tobytes()==gym_sheet.tobytes()
 else:gym_sheet.save(R/gym_root/'tiles.png',bits=4)
 write(gym_root+'/metatiles.bin',struct.pack('<'+str(len(gw))+'H',*gw));write(gym_root+'/metatile_attributes.bin',struct.pack('<'+str(len(ga))+'H',*ga))
 for i in range(16):write(gym_root+f'/palettes/{i:02}.pal','JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,pal[j:j+3])) for j in range(0,48,3))+'\n')
 js('crossroads/hgss/art/olivine-rooms/manifest.json',dict(home=home_art,gym=gs,home_gfx=cursor,gym_gfx=gc,source_sha256=hashlib.sha256((artdir/'gym-source.png').read_bytes()).hexdigest(),source='Original generated silver gym modules directed by actual HGSS screenshot; repacked native GBA furniture at actual HGSS matrix footprints'))
 # Resource declarations owned by this generator.
 blocks={k:[] for k in ['graphics','metatiles','headers','externs']}
 for sym,path in [('HgssOlivineHome',home_root),('HgssOlivineGym',gym_root)]:
  blocks['graphics'].append(f'const u32 gTilesetTiles_{sym}[] = INCGFX_U32("{path}/tiles.png", ".4bpp.fastSmol");\nconst u16 gTilesetPalettes_{sym}[][16] = {{\n'+''.join(f' INCGFX_U16("{path}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n');blocks['metatiles'].append(f'const u16 gMetatiles_{sym}[] = INCBIN_U16("{path}/metatiles.bin");\nconst u16 gMetatileAttributes_{sym}[] = INCBIN_U16("{path}/metatile_attributes.bin");\n');blocks['headers'].append(f'const struct Tileset gTileset_{sym} = {{.isCompressed=TRUE,.isSecondary=TRUE,.tiles=gTilesetTiles_{sym},.palettes=gTilesetPalettes_{sym},.metatiles=gMetatiles_{sym},.metatileAttributes=gMetatileAttributes_{sym},.callback=NULL}};\n');blocks['externs'].append(f'extern const struct Tileset gTileset_{sym};\n')
 for key,path in [('graphics','src/data/tilesets/graphics.h'),('metatiles','src/data/tilesets/metatiles.h'),('headers','src/data/tilesets/headers.h'),('externs','include/tilesets.h')]:
  s=(R/path).read_text();start='// BEGIN HGSS OLIVINE ROOMS';end='// END HGSS OLIVINE ROOMS';b=start+'\n#if !IS_FRLG\n'+''.join(blocks[key])+'#endif\n'+end
  if start in s:s=re.sub(re.escape(start)+'.*?'+re.escape(end),lambda _:b,s,flags=re.S)
  elif key=='externs':i=s.rfind('#endif');s=s[:i]+b+'\n'+s[i:]
  else:s+='\n'+b+'\n'
  write(path,s)
 layouts=load('data/layouts/layouts.json');ls={l['id']:l for l in layouts['layouts']};groups=load('data/maps/map_groups.json');manifest=load('crossroads/johto/manifest.json');city=load('data/maps/OlivineCity/map.json');allmaps={}
 # The published Olivine Center ID is also used by seven other Johto cities.
 # Preserve its original module exactly; only Olivine switches to an appended
 # dedicated layout. The shared Mart template is likewise never reconstructed.
 for c in load('crossroads/hgss/contracts/olivine-common-services-qa08.json')['_shared_templates']:
  l=c['layout'];ls[l['id']].clear();ls[l['id']].update(copy.deepcopy(l));write(l['blockdata_filepath'],bytes.fromhex(c['raw_hex']));write(l['border_filepath'],bytes.fromhex(c['border_hex']))
 def warp(x,y,dest,index):return dict(x=x,y=y,elevation=0,dest_map=dest,dest_warp_id=str(index))
 def obj(x,y,script,gfx='MAN_3'):
  return dict(graphics_id='OBJ_EVENT_GFX_'+gfx,x=x,y=y,elevation=3,movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script=script,flag='0')
 def newmap(n):
  m=copy.deepcopy(load('data/maps/OlivineCity_NeighborHouse/map.json'));m.update(name=n,id=mid(n),layout='LAYOUT_HGSS_'+n.upper(),object_events=[],warp_events=[],coord_events=[],bg_events=[],music='MUS_LITTLEROOT');return m
 def save(m,t,w,h,secondary,header,adapt):
  n=m['name'];l=dict(id=m['layout'],name=n+'_Layout',width=w,height=h,primary_tileset='gTileset_Building',secondary_tileset=secondary,border_filepath=f'data/layouts/{n}/border.bin',blockdata_filepath=f'data/layouts/{n}/map.bin',layout_version='emerald')
  if l['id'] in ls:ls[l['id']].clear();ls[l['id']].update(l)
  else:layouts['layouts'].append(l);ls[l['id']]=l
  assert len(t)==w*h
  for o in m['object_events']:assert not t[o['y']*w+o['x']]&0xc00,(n,'blocked actor',o)
  border=0x601 if secondary=='gTileset_PokemonCenter' else 0x401 if secondary=='gTileset_Shop' else 0x400|(gs['void']['start'] if secondary=='gTileset_HgssOlivineGym' else home_art['void']['start'])
  write(l['blockdata_filepath'],struct.pack('<'+str(w*h)+'H',*t));write(l['border_filepath'],struct.pack('<4H',*([border]*4)));js(f'data/maps/{n}/map.json',m);allmaps[n]=m
  reviews.append(dict(name=n,source_header=header,source=facts[header]['source'],dimensions=[w,h],adaptations=adapt,runtime='requires delivery-ROM controller tests',owner_visual_acceptance='pending'))
 for header,n,outside in TARGETS:
  m=newmap(n);p=project(header,facts=facts);w,h=p['width'],p['height'];seen=p['walkable'];t=[(0x3000|home_art['cafe_floor' if n.endswith('_Cafe') else 'wood']['start']) if (x,y) in seen else (0x400|home_art['void']['start']) for y in range(h) for x in range(w)]
  def stamp(part,x,y,solid=None):
   a=home_art.get('cafe_'+part,home_art[part]) if n.endswith('_Cafe') else home_art[part]
   for yy in range(a['height']):
    for xx in range(a['width']):
     X,Y=x+xx,y+yy
     if 0<=X<w and 0<=Y<h:t[Y*w+X]=(0x400 if solid is True or solid is None and (X,Y) not in seen else 0x3000)|a['start']+yy*a['width']+xx
  for y in (1,2):
   for x in range(1,w-1):t[y*w+x]=0x400|home_art['house_wall']['start']+(y-1)*4+x%4
  if n.endswith('House'):
   stamp('fridge',1,2,True);stamp('house_kitchen',2,2,True);stamp('house_window',5,1,True);stamp('cabinet',7,2,True);stamp('house_plant',9,2,True);stamp('dining_table',6,5,True)
   for x in [5,8]:
    for y in [5,6]:stamp('chair',x,y,False)
   kind={'FishingHouse':('Hgss_OlivineFishingResident','FISHERMAN'),'TradeHouse':('Hgss_OlivineTradeResident','FISHERMAN'),'SealHouse':('Hgss_OlivineSealResident','GIRL_1')}[n.split('_')[-1]]
   m['object_events']=[obj(5,5,*kind)]
   if n.endswith('_SealHouse'):m['object_events'] += [obj(8,5,'Hgss_OlivineSealResident','MAN_3'),obj(2,6,'Hgss_OlivineHouseChild','LITTLE_GIRL')]
  else:
   # Counter/staff alcove and communal table follow actual source permissions.
   for y in range(4,8):
    for x in [11,12]:t[y*w+x]=0x3000|home_art['cafe_floor']['start']
   # One-cell GBA staff aisle: the source3D counter's enclosed NPC alcove
   # becomes safely escapable, with a visible floor at the counter's far end.
   t[8*w+12]=0x3000|home_art['cafe_floor']['start']
   for y in range(3,9):stamp('counter',10,y,True)
   stamp('counter',11,8,True) # Source L-counter return;12,8 remains the GBA service aisle
   stamp('house_kitchen',11,2,True);stamp('house_window',2,1,True);stamp('house_window',6,1,True);stamp('cafe_plant',1,2,True);stamp('cafe_plant',1,9,True);stamp('cafe_table',3,5,True)
   # Source table's centre is structural; no standable hole under the tabletop.
   for x,y in [(2,5),(2,7),(6,5),(6,7),(4,4),(4,8)]:stamp('chair',x,y,False)
   m['object_events']=[obj(11,4,'Hgss_OlivineCafeHost','FISHERMAN'),obj(2,6,'Hgss_OlivineCafeSailor','SAILOR'),obj(6,7,'Hgss_OlivineCafeVisitor','MAN_3')]
   # Closed cells next to public floor form the actual room perimeter.
  for y in range(3,h-1):
   for x in range(1,w-1):
    if t[y*w+x]&1023==home_art['void']['start'] and any((x+dx,y+dy) in seen for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]):t[y*w+x]=0x400|home_art['house_wall']['start']+4+x%4
  d=facts[header]['warps'][0];m['warp_events']=[warp(d['x']+i,d['z'],city['id'],outside) for i in range(2)]
  for e in m['warp_events']:t[e['y']*w+e['x']]=home_art['exit']['start']
  save(m,t,w,h,'gTileset_HgssOlivineHome',header,['HGSS room extent/table/counter footprints in native GBA furnishings; cafe12,8 adds one visible staff escape aisle','Source rewards/trades/Seal Case and plot actors are deferred by owner scope','Paired interior exit leaves both work; exterior house/cafe has its canonical single door'])
 # Services use the same actual HGSS matrices as Ecruteak, not an arbitrary room.
 stock=load('crossroads/hgss/contracts/olivine-common-services-qa08.json');ef=load('crossroads/hgss/canonical_events/ecruteak-interior-geometry.json')
 for suffix,header,esrc in [('PokemonCenter_1F','MAP_OLIVINE_POKECENTER_1F','EcruteakCity_PokemonCenter_1F'),('PokemonCenter_B1F','MAP_OLIVINE_POKECENTER_B1F','EcruteakCity_PokemonCenter_B1F'),('Mart','MAP_OLIVINE_POKEMART','EcruteakCity_Mart')]:
  other=header.replace('OLIVINE','ECRUTEAK');assert facts[header]['chunks']==ef[other]['chunks'],'Service matrix no longer identical; individual redesign required'
  n='OlivineCity_'+suffix;c=stock[esrc];srcmap=c['map'];old=load(f'data/maps/{n}/map.json') if (R/f'data/maps/{n}/map.json').exists() else newmap(n);m=copy.deepcopy(srcmap);m.update(name=n,id=old['id'],layout='LAYOUT_HGSS_'+n.upper(),region_map_section='MAPSEC_OLIVINE_CITY');w,h=c['layout']['width'],c['layout']['height'];t=list(struct.unpack('<'+str(w*h)+'H',bytes.fromhex(c['raw_hex'])))
  if suffix=='PokemonCenter_1F':
   m['object_events'][0].update(script='Olivine_Nurse',local_id='LOCALID_OLIVINE_NURSE');m['object_events'][1]['script']='Olivine_CenterVisitor';m['warp_events']=[warp(8,19,city['id'],3),warp(9,19,city['id'],14),warp(14,17,mid('OlivineCity_PokemonCenter_B1F'),0)]
   # Model23 source plants: upper right wall and the paired lower pots.
   for x,y in [(15,3),(14,14),(15,14)]:t[y*w+x]=0x60a;t[(y+1)*w+x]=0x612
  elif suffix=='PokemonCenter_B1F':m['warp_events']=[warp(14,10,'MAP_OLIVINE_CITY_POKEMON_CENTER_1F',2)]
  else:
   m['object_events'][0].update(script='Olivine_Clerk',local_id='LOCALID_SLATEPORT_MART_CLERK');m['object_events'][1]['script']='Olivine_MartVisitor';m['object_events'][2]['script']='Olivine_Clerk';m['warp_events']=[warp(4,11,city['id'],4),warp(5,11,city['id'],4)]
  save(m,t,w,h,c['layout']['secondary_tileset'],header,['Actual HGSS matrix identical to Ecruteak service room; pinned tested native adaptation','Olivine nurse ID/shop stock/scripts preserved; native PC/counter/escalators','Raised DS reception flattened; communication desks explicitly offline'])
 # The long HGSS steel hall is split at sourcey17 over the two stable native IDs.
 p=project('MAP_OLIVINE_GYM',facts=facts,bounds=(11,29));seen=p['walkable'];whole=[]
 for y in range(29):
  for x in range(11):
   n=gs['hex']['start']+(y%2)*2+x%2
   if x<2 or x>10 or y<1:n=gs['void']['start']
   whole.append((0x3000 if (x,y) in seen else 0x400)|n)
 def g_stamp(part,x,y,block=True):
  a=gs[part]
  for yy in range(a['height']):
   for xx in range(a['width']):
    X,Y=x+xx,y+yy
    if 0<=X<11 and 0<=Y<29:whole[Y*11+X]=(0x400 if block else 0x3000)|a['start']+yy*a['width']+xx
 for y in range(5,28):
  for x in range(3,10):
   if (x,y) in seen:whole[y*11+x]=0x3000|gs['runway']['start']
 for y in range(3,29,4):g_stamp('pillar',2,y);g_stamp('pillar',10,y)
 for x in [3,5,7,9]:g_stamp('wall',x,1)
 g_stamp('canopy',4,1);g_stamp('stairs',6,7,False)
 for x,y in [(4,24),(8,24)]:g_stamp('pylon',x,y)
 for n,oy,height in [('OlivineCity_Gym',17,12),('OlivineCity_Gym_Arena',0,17)]:
  m=load(f'data/maps/{n}/map.json');m['music']='MUS_GYM';t=whole[oy*11:(oy+height)*11];w=11;h=height
  if n=='OlivineCity_Gym':
   m['warp_events']=[warp(6,10,city['id'],2),warp(7,10,city['id'],8),warp(6,0,'MAP_OLIVINECITY_GYM_ARENA',0),warp(5,0,'MAP_OLIVINECITY_GYM_ARENA',1),warp(7,0,'MAP_OLIVINECITY_GYM_ARENA',2)];m['object_events']=m['object_events'][:1];m['object_events'][0].update(x=3,y=6)
  else:
   m['warp_events']=[warp(6,16,'MAP_OLIVINE_CITY_GYM',2),warp(5,16,'MAP_OLIVINE_CITY_GYM',3),warp(7,16,'MAP_OLIVINE_CITY_GYM',4)];m['object_events']=m['object_events'][:2];m['object_events'][0].update(x=6,y=5);m['object_events'][1].update(x=9,y=15)
  for e in m['warp_events']:t[e['y']*w+e['x']]=gs['exit']['start'] if e['dest_map']==city['id'] else 0x3000|gs['warp']['start']
  for o in m['object_events']:t[o['y']*w+o['x']]=0x3000|gs['runway']['start']
  save(m,t,w,h,'gTileset_HgssOlivineGym','MAP_OLIVINE_GYM',['Canonical HGSS long central steel runway/platform/pylons/source actor positions','Original silver/salmon/hex modules replace 3D perspective; owner exterior Gym unchanged','Sourcey17 split across two stable map IDs; all three corridor segments reciprocal','Accepted Jasmine/apprentice optional practice scripts retained, no rewards/badges/gates'])
 # Append only new map/group/layout IDs; no published room IDs are replaced.
 for n in NEW:
  if n not in groups['gMapGroup_CrossroadsJohtoExpansion']:groups['gMapGroup_CrossroadsJohtoExpansion'].append(n)
  if not any(p['name']==n for p in manifest['planned']):manifest['planned'].append(dict(name=n,kind='hgss',parent='OlivineCity',cluster='west',status='reference-room-runtime-review-pending'))
  write(f'data/maps/{n}/scripts.inc',n+'_MapScripts::\n    .byte 0\n')
 js('data/layouts/layouts.json',layouts);js('data/maps/map_groups.json',groups);js('crossroads/johto/manifest.json',manifest);js('crossroads/hgss/olivine-room-review.json',reviews)
 # Center heal arrival follows the existing nurse ID, not a new heal slot.
 heals=load('src/data/heal_locations.json');next(v for v in heals['heal_locations'] if v['id']=='HEAL_LOCATION_OLIVINE_CITY').update(x=16,y=34,respawn_x=8,respawn_y=13);js('src/data/heal_locations.json',heals)
 inc=(R/'data/event_scripts.s').read_text()
 for path in [*(f'data/maps/{n}/scripts.inc' for n in NEW),'crossroads/scripts/hgss_olivine_rooms.inc']:
  line='\t.include "'+path+'"'
  if line not in inc:inc+='\n'+line+'\n'
 write('data/event_scripts.s',inc)
 print('HGSS Olivine3homes/cafe, canonical services/basement and split steel Gym generated; runtime/visual acceptance pending')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');generate(p.parse_args().check)
