#!/usr/bin/env python3
"""HGSS-shaped Glitter Lighthouse and Olivine port; append-only map identities.

Uses stripped, SHA-backed source permissions/props/warps, never DS textures or
story scripts. Original native furniture and a private maritime floor palette
adapt the perspective rooms to GBA layers. The six historical lighthouse maps
retain IDs/warp ordinals. The working two-stop lift uses the engine dynamic warp,
not new permanent variables. Run only as part of the coordinated city generator.
"""
import argparse,copy,json,re,struct,hashlib
from pathlib import Path
from hgss_room_projection import project,ART,warp_tile
R=Path(__file__).resolve().parents[2]
FACT_PATH='crossroads/hgss/canonical_events/olivine-interior-geometry.json'
LH=[f'OlivineCity_Lighthouse_{i}F' for i in range(1,7)]
BAL='OlivineCity_Lighthouse_Balcony';LIFT='OlivineCity_Lighthouse_Elevator'
PORT='OlivineCity_PortTerminal';QUAY='OlivineCity_PortQuay'
OWNED=set(LH+[BAL,LIFT,PORT,QUAY])
NEW_IDS={BAL:'MAP_OLIVINE_CITY_LIGHTHOUSE_BALCONY',LIFT:'MAP_OLIVINE_CITY_LIGHTHOUSE_ELEVATOR',PORT:'MAP_OLIVINE_CITY_PORT_TERMINAL',QUAY:'MAP_OLIVINE_CITY_PORT_QUAY'}
HEADERS={**{n:'MAP_OLIVINE_LIGHTHOUSE_'+(str(i)+'F' if i<6 else 'LIGHT_ROOM') for i,n in enumerate(LH,1)},BAL:'MAP_OLIVINE_LIGHTHOUSE_EXTERIOR',LIFT:'MAP_OLIVINE_LIGHTHOUSE_ELEVATOR',PORT:'MAP_SS_AQUA_OLIVINE_PORT_INTERIOR',QUAY:'MAP_SS_AQUA_OLIVINE_PORT_EXTERIOR'}
def load(p):return json.loads((R/p).read_text())
def generate(check=False):
 def write(p,b):
  dest=R/p
  if isinstance(b,str):b=b.encode()
  if dest.suffix=='.pal':b=b.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
  if check:assert dest.exists() and dest.read_bytes()==b,('Regenerate Olivine landmark',p)
  elif not dest.exists() or dest.read_bytes()!=b:dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
 def js(p,v):write(p,json.dumps(v,indent=2)+'\n')
 from PIL import Image
 import io
 facts=load(FACT_PATH);layouts=load('data/layouts/layouts.json');ls={l['id']:l for l in layouts['layouts']};groups=load('data/maps/map_groups.json');manifest=load('crossroads/johto/manifest.json');review=[]
 # A private copy changes ONLY the maritime under-floor palette. The original
 # temple art/metas/animations remain immutable for Ecruteak and other maps.
 source=R/'data/tilesets/secondary/hgss_temple';resource='data/tilesets/secondary/hgss_olivine_landmarks'
 raw=(source/'metatiles.bin').read_bytes();metas=list(struct.unpack('<'+str(len(raw)//2)+'H',raw))
 # Native floor glyph201 is not a wall/character texture. Colour its references
 # in palette7 while all furniture remains in its original palette6.
 metas=[(v&0xfff)|0x7000 if v&1023==0x201 else v for v in metas]
 # Source HGSS maritime walls are pale masonry with cool window accents, not
 # Ecruteak's red-curtained timber panels. Recolour only wall foreground words;
 # floor references, other furniture, map cells and collision stay identical.
 for part in ['house_wall','house_wall_stone']:
  a=ART[part]
  for n in range(a['start'],a['start']+a['width']*a['height']):
   for j in range(4,8):
    i=(n-512)*8+j;metas[i]=(metas[i]&0xfff)|0xb000
 # Derive new indices from the current original temple resource. Never assume
 # the previous488-glyph/383-metatile version: Ecruteak may append its own art.
 attributes=list(struct.unpack('<'+str((source/'metatile_attributes.bin').stat().st_size//2)+'H',(source/'metatile_attributes.bin').read_bytes()))
 lift_metas=[512+len(attributes),513+len(attributes)]
 metas.extend([0x7201]*4+[0x8200]*4+[0x7201]*4+[0x8200]*4);attributes.extend([0x1061,0x1061])
 secondary_image_bytes=(source/'tiles.png').read_bytes()
 # Original seating props follow the actual terminal screenshot, not generic
 # cabinets. They live in private compatible primary sheets; shared Building
 # and General graphics/palettes remain untouched. No engine capacity change.
 furniture_source=R/'crossroads/hgss/art/olivine/port-furniture-source.png'
 furniture_image=Image.open(furniture_source).convert('RGBA');furniture={}
 specs=[('table',(0,0,512,512),(32,32)),('narrow_table',(0,0,512,512),(16,32)),('stool',(512,0,1024,512),(16,16)),('bench',(1024,0,1536,512),(16,16)),('corner',(0,512,512,1024),(16,16)),('bollard',(512,512,1024,1024),(16,16)),('ring',(1024,512,1536,1024),(16,16))]
 ims={}
 for name,box,size in specs:
  im=furniture_image.crop(box);alpha=im.getchannel('A').point(lambda v:255 if v>=190 else 0);im.putalpha(alpha);ims[name]=im.crop(alpha.getbbox()).resize(size,Image.Resampling.NEAREST)
 strip=Image.new('RGB',(sum(im.width for im in ims.values()),32));ox=0
 for im in ims.values():strip.paste(im,(ox,0),im.getchannel('A'));ox+=im.width
 furniture_pal=[0,0,0]+strip.quantize(colors=15,method=Image.Quantize.MEDIANCUT).getpalette()[:45]
 primaries={n:Image.open(R/f'data/tilesets/primary/{n}/tiles.png').copy() for n in ['building','general']}
 used_general=set(v&1023 for v in struct.unpack('<8H',(R/'data/tilesets/primary/general/metatiles.bin').read_bytes()[0x170*16:0x171*16]))
 brefs=(R/'data/tilesets/primary/building/metatiles.bin').read_bytes();used_general.update(v&1023 for v in struct.unpack('<'+str(len(brefs)//2)+'H',brefs))
 free=[n for n in range(432) if n not in used_general];glyphs={}
 def glyph(im):
  key=im.tobytes()
  if key not in glyphs:
   assert free,'Private maritime furniture graphics capacity';n=free.pop(0);glyphs[key]=n
   for sheet in primaries.values():sheet.paste(im,(n%16*8,n//16*8))
   for flags,flipped in [(0x400,im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)),(0x800,im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)),(0xc00,im.transpose(Image.Transpose.FLIP_LEFT_RIGHT).transpose(Image.Transpose.FLIP_TOP_BOTTOM))]:glyphs.setdefault(flipped.tobytes(),n|flags)
  return glyphs[key]
 # Both real lift panels are drawn and encoded at their derived indices.
 door=Image.open(R/'crossroads/hgss/art/olivine/port-native.png')
 for leaf,n in enumerate(lift_metas):
  top=[0x8000|glyph(door.crop((48+leaf*16+dx,80+dy,56+leaf*16+dx,88+dy))) for dx,dy in [(0,0),(8,0),(0,8),(8,8)]]
  metas[(n-512)*8:(n-511)*8]=[0x7201]*4+top
 def add_meta(row,behavior=0):
  n=512+len(attributes);metas.extend(row);attributes.append(0x1000|behavior);return n
 for name,im in ims.items():
  ref=Image.new('P',(1,1));ref.putpalette(furniture_pal+[0]*720);q=im.convert('RGB').quantize(palette=ref,dither=Image.Dither.NONE);values=bytearray(q.tobytes());alpha=im.getchannel('A').tobytes()
  for j in range(len(values)):values[j]=0 if alpha[j]<128 else values[j] or 1
  q=Image.frombytes('P',im.size,bytes(values));q.putpalette(furniture_pal);ids=[]
  for y in range(im.height//16):
   for x in range(im.width//16):
    top=[0x9000|glyph(q.crop((x*16+dx,y*16+dy,x*16+dx+8,y*16+dy+8))) for dx,dy in [(0,0),(8,0),(0,8),(8,8)]]
    ids.append(add_meta([0x6201]*4+top))
  furniture[name]=dict(width=im.width//16,height=im.height//16,metatiles=ids)
  output=io.BytesIO();q.save(output,format='PNG',bits=4);write(f'crossroads/hgss/art/olivine/port-{name}-native.png',output.getvalue())
 port_floor=add_meta([0x6201]*8);port_warp=add_meta([0x6201]*8,0x61)
 building_metas=(R/'data/tilesets/primary/building/metatiles.bin').read_bytes();rug_words=list(struct.unpack('<8H',building_metas[6*16:7*16]));rug_words=[(v&0xfff)|0xa000 for v in rug_words];port_rug=add_meta(rug_words)
 # The complete maritime model inventory: rear terminal167, ferry168 and both
 # model119 sailboats. Sailing remains a separate, clearly bounded service.
 def quant(im,palette,size):
  im=im.convert('RGBA');alpha=im.getchannel('A').point(lambda v:255 if v>=180 else 0);im.putalpha(alpha);im=im.crop(alpha.getbbox()).resize(size,Image.Resampling.NEAREST);ref=Image.new('P',(1,1));ref.putpalette(palette+[0]*(768-len(palette)));q=im.convert('RGB').quantize(palette=ref,dither=Image.Dither.NONE);v=bytearray(q.tobytes());a=im.getchannel('A').tobytes()
  for i in range(len(v)):v[i]=0 if a[i]<128 else v[i] or 1
  q=Image.frombytes('P',size,bytes(v));q.putpalette(palette);return q
 bluepal=[int(v) for line in (R/'data/tilesets/secondary/hgss_olivine/palettes/11.pal').read_text().splitlines()[3:] for v in line.split()]
 general_meta=list(struct.unpack('<4096H',(R/'data/tilesets/primary/general/metatiles.bin').read_bytes()));general_attrs=list(struct.unpack('<512H',(R/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()));water=general_meta[0x170*8:0x170*8+4];scenes={}
 rear_source=Image.open(R/'crossroads/hgss/art/olivine/port-native.png');rear=Image.new('P',(192,96));rear.putpalette(rear_source.getpalette())
 for y in range(6):
  for x,sx in enumerate([0,1,1,2,2,3,4,5,5,6,6,7]):rear.paste(rear_source.crop((sx*16,y*16,sx*16+16,y*16+16)),(x*16,y*16))
 for y,sy in [(3,4),(4,5)]:rear.paste(rear_source.crop((48,sy*16,64,sy*16+16)),(0,y*16))
 vessels=Image.open(R/'crossroads/hgss/art/olivine/port-vessels-source.png');vw,vh=vessels.size
 ship=quant(vessels.crop((0,0,int(vw*.78),vh)),bluepal,(192,80));sail=quant(vessels.crop((int(vw*.8),0,vw,vh)),bluepal,(48,48))
 # Repeating only the new ferry's central upper-deck panels makes its clean
 # window/railing rhythm tileable. Funnel, bridge, bow, stern and hatch retain
 # their original silhouettes. No accepted city or Gym art is simplified.
 ship_original=ship.copy()
 for yy in range(3):
  for xx in range(4,8):ship.paste(ship_original.crop((80,yy*16,96,yy*16+16)),(xx*16,yy*16))
 # Extend the passenger hull with repeatedmid-deck columns so it reads as a
 # full ferry beside the terminal, keeping its source-aligned hatch unchanged.
 expanded_ship=Image.new('P',(256,80));expanded_ship.putpalette(ship.getpalette())
 for yy in range(5):
  for xx,sx in enumerate([0,1,2,3,4,5,6,7,7,7,7,7,8,9,10,11]):expanded_ship.paste(ship.crop((sx*16,yy*16,sx*16+16,yy*16+16)),(xx*16,yy*16))
 ship=expanded_ship
 for name,q,primary in [('rear_terminal',rear,True),('ferry',ship,False),('sailboat',sail,False)]:
  ids=[];visible=[];ww,hh=q.width//16,q.height//16
  for y in range(hh):
   for x in range(ww):
    top=[0x8000|glyph(q.crop((x*16+dx,y*16+dy,x*16+dx+8,y*16+dy+8))) for dx,dy in [(0,0),(8,0),(0,8),(8,8)]];shown=any(q.crop((x*16,y*16,x*16+16,y*16+16)).tobytes());visible.append(shown)
    if primary:
     n=0x100+y*ww+x;general_meta[n*8:n*8+8]=water+top;general_attrs[n]=(0x1000 if y>=hh-2 else 0)|(0x61 if (x,y) in [(5,5),(6,5),(0,3),(0,4)] else 0);ids.append(n)
    else:ids.append(add_meta(water+top))
  scenes[name]=dict(width=ww,height=hh,metatiles=ids,visible=visible)
  output=io.BytesIO();q.save(output,format='PNG',bits=4);write(f'crossroads/hgss/art/olivine/{name}-native.png',output.getvalue())
 planter_source=Image.open(R/'crossroads/hgss/art/olivine/lighthouse-planter-source.png');templepal=[int(v) for line in (source/'palettes/06.pal').read_text().splitlines()[3:] for v in line.split()];planter=quant(planter_source,templepal,(16,32));plant_ids=[]
 for y in range(2):plant_ids.append(add_meta([0x7201]*4+[0x6000|glyph(planter.crop((dx,y*16+dy,dx+8,y*16+dy+8))) for dx,dy in [(0,0),(8,0),(0,8),(8,8)]]))
 output=io.BytesIO();planter.save(output,format='PNG',bits=4);write('crossroads/hgss/art/olivine/lighthouse-planter-native.png',output.getvalue())
 purple_floor=add_meta([0xc201]*8);purple_warp=add_meta([0xc201]*8,0x61)
 assert len(attributes)<=512,('Maritime secondary metatile capacity',len(attributes))
 capacity=dict(primary_graphics=len({v&1023 for v in glyphs.values()}),primary_free=len(free),secondary_metatiles=len(attributes),secondary_free=512-len(attributes),rear_terminal_primary_ids=[0x100,0x147],source_secondary_glyphs='unchanged exact original image')
 write('crossroads/hgss/art/olivine/landmark-capacity.json',json.dumps(capacity,indent=2)+'\n')
 attr=struct.pack('<'+str(len(attributes))+'H',*attributes)
 assert Image.open(io.BytesIO(secondary_image_bytes)).size==(128,256),'Maritime secondary must retain full glyph sheet'
 assert len(metas)==len(attributes)*8,'Maritime metatile/attribute count mismatch'
 write(resource+'/tiles.png',secondary_image_bytes);write(resource+'/metatiles.bin',struct.pack('<'+str(len(metas))+'H',*metas));write(resource+'/metatile_attributes.bin',attr)
 for pal in range(16):
  b=(source/f'palettes/{pal:02}.pal').read_bytes()
  if pal==11:
   colors=[[0,0,0],[222,229,225],[174,188,185],[132,153,154],[91,114,117],[60,78,83],[32,46,52],[144,150,151],[83,95,101],[52,60,66],[104,142,114],[154,181,139],[71,107,91],[95,142,152],[57,94,108],[196,216,209]]
   b='JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n'
  if pal==12:
   colors=[list(map(int,l.split())) for l in (source/'palettes/06.pal').read_text().splitlines()[3:]];colors[2]=[120,104,157];colors[3]=[85,70,121];colors[5]=[49,39,84]
   b='JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n'
  if pal==8:b=(R/'data/tilesets/secondary/hgss_olivine/palettes/11.pal').read_bytes()
  if pal==9:b='JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,furniture_pal[j:j+3])) for j in range(0,48,3))+'\n'
  if pal==10:
   colors=[list(map(int,l.split())) for l in (R/'data/tilesets/primary/building/palettes/00.pal').read_text().splitlines()[3:]]
   colors=[[min(255,int(sum(c)/3*.55)),min(255,int(sum(c)/3*.85)),min(255,int(sum(c)/3*1.1))] for c in colors]
   b='JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n'
  if pal==7:
   colors=[list(map(int,l.split())) for l in (source/'palettes/06.pal').read_text().splitlines()[3:]]
   colors[2]=[115,151,137];colors[3]=[81,118,109];colors[5]=[49,79,77]
   b='JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n'
  write(resource+f'/palettes/{pal:02}.pal',b)
 sym='HgssOlivineLandmarks';blocks={
 'src/data/tilesets/graphics.h':f'const u32 gTilesetTiles_{sym}[] = INCGFX_U32("{resource}/tiles.png", ".4bpp.fastSmol");\nconst u16 gTilesetPalettes_{sym}[][16] = {{\n'+''.join(f' INCGFX_U16("{resource}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n',
 'src/data/tilesets/metatiles.h':f'const u16 gMetatiles_{sym}[] = INCBIN_U16("{resource}/metatiles.bin");\nconst u16 gMetatileAttributes_{sym}[] = INCBIN_U16("{resource}/metatile_attributes.bin");\n',
 'src/data/tilesets/headers.h':f'const struct Tileset gTileset_{sym} = {{ .isCompressed=TRUE, .isSecondary=TRUE, .tiles=gTilesetTiles_{sym}, .palettes=gTilesetPalettes_{sym}, .metatiles=gMetatiles_{sym}, .metatileAttributes=gMetatileAttributes_{sym}, .callback=NULL }};\n',
 'include/tilesets.h':f'extern const struct Tileset gTileset_{sym};\n'}
 for kind,symbol in [('building','HgssOlivineLandmarkIndoor'),('general','HgssOlivineLandmarkOutdoor')]:
  p=f'data/tilesets/primary/hgss_olivine_landmark_{kind}';output=io.BytesIO();primaries[kind].save(output,format='PNG',bits=4);write(p+'/tiles.png',output.getvalue())
  base='InsideBuilding' if kind=='building' else 'General';blocks['src/data/tilesets/graphics.h']+=f'const u32 gTilesetTiles_{symbol}[] = INCGFX_U32("{p}/tiles.png", ".4bpp.fastSmol");\n'
  meta_base=base
  if kind=='general':
   meta_base=symbol;write(p+'/metatiles.bin',struct.pack('<4096H',*general_meta));write(p+'/metatile_attributes.bin',struct.pack('<512H',*general_attrs));blocks['src/data/tilesets/metatiles.h']+=f'const u16 gMetatiles_{symbol}[] = INCBIN_U16("{p}/metatiles.bin");\nconst u16 gMetatileAttributes_{symbol}[] = INCBIN_U16("{p}/metatile_attributes.bin");\n'
  blocks['src/data/tilesets/headers.h']+=f'const struct Tileset gTileset_{symbol} = {{ .isCompressed=TRUE, .isSecondary=FALSE, .tiles=gTilesetTiles_{symbol}, .palettes=gTilesetPalettes_{base}, .metatiles=gMetatiles_{meta_base}, .metatileAttributes=gMetatileAttributes_{meta_base}, .callback={"InitTilesetAnim_General" if kind=="general" else "NULL"} }};\n'
  blocks['include/tilesets.h']+=f'extern const struct Tileset gTileset_{symbol};\n'
 for path,body in blocks.items():
  text=(R/path).read_text();start='// BEGIN OLIVINE LANDMARK INTERIORS';end='// END OLIVINE LANDMARK INTERIORS';block=start+'\n#if !IS_FRLG\n'+body+'#endif\n'+end
  if start in text:text=re.sub(re.escape(start)+'.*?'+re.escape(end),lambda _:block,text,flags=re.S)
  elif path=='include/tilesets.h':i=text.rfind('#endif');text=text[:i]+block+'\n'+text[i:]
  else:text+='\n'+block+'\n'
  write(path,text)
 maps={};rooms={}
 for n in LH+[BAL,LIFT,PORT,QUAY]:
  existing=(R/f'data/maps/{n}/map.json').exists()
  m=load(f'data/maps/{n}/map.json') if existing else copy.deepcopy(load(f'data/maps/{LH[0]}/map.json'))
  if n in NEW_IDS:m.update(name=n,id=NEW_IDS[n],layout='LAYOUT_'+NEW_IDS[n][4:],object_events=[],bg_events=[],coord_events=[])
  bounds=(17,20) if n==LH[2] else (17,19) if n in LH else (17,17) if n==BAL else (8,8) if n==LIFT else (15,13) if n==PORT else (40,27)
  room=project(HEADERS[n],theme='wood',bounds=bounds,facts=facts);rooms[n]=room;maps[n]=m
  m.update(music='MUS_LILYCOVE',weather='WEATHER_SUNNY' if n in [BAL,QUAY] else 'WEATHER_NONE',map_type='MAP_TYPE_ROUTE' if n in [BAL,QUAY] else 'MAP_TYPE_INDOOR',show_map_name=False,allow_cycling=False,allow_running=True,connections=None,coord_events=[])
  # The native projection crops unused southeast DS model space, preserving
  # each actual room's origin, blocked shafts and source staircase coordinates.
  w,h=bounds;t=room['tiles'];seen=room['walkable']
  def furniture_stamp(name,x,y,mirror=False):
   a=furniture[name]
   for yy in range(a['height']):
    for xx in range(a['width']):
     X,Y=x+xx,y+yy
     if 0<=X<w and 0<=Y<h:t[Y*w+X]=0x400|a['metatiles'][yy*a['width']+xx]
  if n in [BAL,QUAY]:
   for y in range(h):
    for x in range(w):
     if (x,y) not in seen:t[y*w+x]=0x1170
   if n==BAL:
    # Masonry tower core; only the low south facade has an open doorway.
    for y in range(0,12):
     for x in range(4,13):t[y*w+x]=0x400|ART['house_wall_stone']['start']+(y%2)*4+x%4
    for x in range(5,12):t[12*w+x]=0x400|ART['house_wall_stone']['start']+4+x%4
    # Native rail along the outside of both sidewalks; no invisible freefall.
    for x,y in [(0,y) for y in range(2,16)]+[(16,y) for y in range(2,16)]+[(x,16) for x in range(17)]:t[y*w+x]=0x400|ART['rail_h_stone']['start']+x%4
    # Sea is far below this high balcony. Every source-blocked cell touching
    # its public walkway remains a solid railing/core wall, including the inner
    # x3/x13 strips and north ends; Survey Surf must not launch off the tower.
    for y in range(h):
     for x in range(w):
      if t[y*w+x]==0x1170 and (x,y) not in seen and any((a,b) in seen for a,b in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):t[y*w+x]=0x400|ART['rail_h_stone']['start']+x%4
   else:
    for x,y in seen:
     if 0<=x<w and 0<=y<h:t[y*w+x]=0x3000|ART['stone']['start']
    # White quay railing follows source ground, not a rectangular island.
    for y in range(h):
     for x in range(w):
      if (x,y) not in seen and any((a,b) in seen for a,b in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):t[y*w+x]=0x400|ART['rail_h_stone']['start']+x%4
    for x,y in [(15,21),(17,21),(22,21),(25,21),(30,21),(15,26),(18,26),(24,26),(28,26)]:
     if 0<=x<w and 0<=y<h and (x,y) not in seen:furniture_stamp('bollard',x,y)
    for kind,ox,oy in [('sailboat',8,1),('sailboat',22,1),('rear_terminal',11,10),('ferry',21,15)]:
     a=scenes[kind]
     for yy in range(a['height']):
      for xx in range(a['width']):
       j=yy*a['width']+xx;X,Y=ox+xx,oy+yy
       if a['visible'][j] and 0<=X<w and 0<=Y<h:t[Y*w+X]=0x400|a['metatiles'][j]
  elif n in LH:
   # Stone rear window wall and round timber rail match source silhouettes.
   # Only blocked source cells are covered: no decor silently fills an aisle.
   for y in range(2,h-1):
    for x in range(1,w-1):
     if (x,y) not in seen and ((x,y+1) in seen or (x,y-1) in seen):t[y*w+x]=0x400|ART['house_wall_stone']['start']+(y%2)*4+x%4
   if n==LH[0]:
    # Original GBA bench/planter motifs at the DS tourist deck's actual blocked
    # footprints, not generic pillars scattered over walkable ground.
    for x,y in [(3,8),(3,9),(13,8),(13,9),(3,13),(3,14),(13,13),(13,14)]:t[y*w+x]=0x400|ART['chair']['start']
    for x,y in [(6,7),(10,7),(6,10),(10,10),(6,13),(10,13)]:
     for j in range(2):t[(y+j)*w+x]=0x400|plant_ids[j]
   if n==LH[5]:
    for x,y in seen:
     if 0<=x<w and 0<=y<h:t[y*w+x]=0x3000|purple_floor
    for y in range(6,8):
     for x in range(7,10):
      if (x,y) not in seen:t[y*w+x]=0x400|ART['stone']['start']
  elif n==PORT:
   # Actual HGSS image: tan plank floor, central blue rug, white/yellow dining
   # places and aqua waiting seats forming the source's south U-shaped lanes.
   for x,y in seen:
    if 0<=x<w and 0<=y<h:t[y*w+x]=0x3000|port_floor
   for y in range(3,8):
    for x in range(6,9):
     if (x,y) in seen:t[y*w+x]=0x3000|port_rug
   for y in [1,2]:
    for x in range(1,w-1):
     if (x,y) not in seen:t[y*w+x]=0x400|ART['house_wall_stone']['start']+(y%2)*4+x%4
   furniture_stamp('narrow_table',3,4);furniture_stamp('table',11,5)
   for x,y in [(4,4),(4,5),(10,5),(10,6)]:furniture_stamp('stool',x,y)
   for x in [4,5,6,8,9,10]:furniture_stamp('bench',x,9)
   for x in [4,10]:furniture_stamp('corner',x,10)
   for x in [4,10]:furniture_stamp('ring',x,1)
  elif n==LIFT:
   for y in [1,2]:
    for x in range(1,6):t[y*w+x]=0x400|ART['house_wall_stone']['start']+(y%2)*4+x%4
   t[2*w+2]=t[2*w+5]=0x400|ART['panel']['start']
   m['bg_events']=[dict(type='sign',x=x,y=2,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=label) for x,label in [(2,'Hgss_OlivineLift1F'),(5,'Hgss_OlivineLift6F')]]
 # Actual stair models144/145 use a vertical two-cell ladder in the native
 # perspective. Preserve each source blocked footprint while drawing both parts.
 for n in LH:
  room=rooms[n];w=room['width'];h=room['height'];t=room['tiles']
  for chunk in facts[HEADERS[n]]['chunks']:
   for p in chunk['props']:
    if p['model'] not in [4,144,145]:continue
    x,y=int(p['tile_x']),int(p['tile_z'])
    for j in range(2):
     if 0<=x<w and 0<=y-1+j<h:
      q=(y-1+j)*w+x;t[q]=(t[q]&0xfc00)|ART['ladder']['start']+j
 def warp(x,y,n,i):return dict(x=x,y=y,elevation=0,dest_map=maps[n]['id'] if n in maps else n,dest_warp_id=str(i))
 plans={
  LH[0]:[(8,17,'MAP_OLIVINE_CITY',7),(9,17,'MAP_OLIVINE_CITY',7),(2,3,LH[1],0),(8,4,LIFT,0),(9,4,LIFT,1)],
  LH[1]:[(5,3,LH[0],2),(13,6,LH[2],0),(13,5,LH[2],0)],
  LH[2]:[(13,7,LH[1],1),(10,7,LH[3],0),(10,6,LH[3],0),(6,7,LH[3],3),(6,6,LH[3],3),(8,18,BAL,0),(9,18,BAL,1)],
  LH[3]:[(10,7,LH[2],1),(3,5,LH[4],0),(3,4,LH[4],0),(6,7,LH[2],3)],
  LH[4]:[(4,5,LH[3],1),(10,10,LH[5],0),(10,9,LH[5],0)],
  LH[5]:[(9,10,LH[4],1),(8,4,LIFT,0),(9,4,LIFT,1)],
  BAL:[(8,12,LH[2],5),(9,12,LH[2],6)],
  LIFT:[(3,6,'MAP_DYNAMIC','WARP_ID_DYNAMIC'),(4,6,'MAP_DYNAMIC','WARP_ID_DYNAMIC')],
  PORT:[(7,2,'MAP_OLIVINE_CITY',13),(7,11,QUAY,0),(1,7,QUAY,1),(8,2,'MAP_OLIVINE_CITY',15),(8,11,QUAY,2),(1,8,QUAY,3)],
  QUAY:[(16,15,PORT,1),(11,13,PORT,2),(17,15,PORT,4),(11,14,PORT,5)]}
 def actor(x,y,label,gfx='EXPERT_M'):
  return dict(graphics_id='OBJ_EVENT_GFX_'+gfx,x=x,y=y,elevation=3,movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script=label,flag='0')
 # Existing actor identities/scripts are retained; only collision-safe positions
 # move. These are ambient visitors, never source trainer/story battles.
 actorpos={LH[0]:[(8,15)],LH[2]:[(4,13)],LH[5]:[(11,14),(8,6)]}
 for n,positions in actorpos.items():
  for o,(x,y) in zip(maps[n]['object_events'],positions):o.update(x=x,y=y)
 maps[PORT]['object_events']=[actor(11,4,'Hgss_OlivinePortDesk','SAILOR'),actor(5,7,'Hgss_OlivinePortVisitor','WOMAN_3')]
 maps[QUAY]['object_events']=[actor(24,24,'Hgss_OlivinePortDesk','SAILOR')]
 for n in LH:
  x,y=(0,16) if n in LH[:2] else (4,16) if n==LH[5] else (3,16)
  maps[n]['bg_events']=[dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=f'Area_Floor_{n}')]
  rooms[n]['tiles'][y*rooms[n]['width']+x]=0x400|ART['panel']['start']
 maps[BAL]['bg_events']=[dict(type='sign',x=5,y=16,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='Area_LighthouseView')]
 maps[QUAY]['bg_events']=[dict(type='sign',x=27,y=21,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='Hgss_OlivineShipBoundary')]
 rooms[QUAY]['tiles'][21*rooms[QUAY]['width']+27]=0x400|ART['panel']['start']
 rooms[QUAY]['tiles'][20*rooms[QUAY]['width']+27]=0x400|ART['rail_h_stone']['start']+3
 rooms[BAL]['tiles'][16*17+5]=0x400|ART['panel']['start']
 maps[LH[3]]['coord_events']=[dict(type='trigger',x=16,y=9,elevation=0,var='VAR_TEMP_0',var_value='0',script='Hgss_OlivineWindowDrop')]
 # Close the void beyond the window; stepping on the marked window immediately
 # performs the source one-way drop, and the balcony has a full return journey.
 rooms[LH[3]]['tiles'][9*17+16]=0x3000|ART['stone']['start']
 # Lift mouths are two visible panels. The second panel's source cell is model
 # floor outside the DS single-tile warp; its GBA landing is explicitly opened.
 for n in [LH[0],LH[5]]:
  room=rooms[n];w=room['width'];room['tiles'][4*w+8]=0x3000|lift_metas[0];room['tiles'][4*w+9]=0x3000|lift_metas[1]
  room['tiles'][5*w+8]=room['tiles'][5*w+9]=0x3000|(purple_floor if n==LH[5] else ART['wood']['start'])
 for n in LH+[BAL,LIFT,PORT,QUAY]:
  m=maps[n];room=rooms[n];w,h=room['width'],room['height'];t=room['tiles'];m['warp_events']=[warp(*v) for v in plans[n]]
  for i,e in enumerate(m['warp_events']):
   x,y=e['x'],e['y']
   if n==QUAY:t[y*w+x]=0x3000|(t[y*w+x]&1023) # native rear-façade doors carry real warp behavior
   elif n==LH[5] and i==0:t[y*w+x]=0x3000|purple_warp
   elif n==PORT:t[y*w+x]=0x3000|port_warp
   elif t[y*w+x]&1023 not in lift_metas:t[y*w+x]=warp_tile(t[y*w+x])
  # South-facing public thresholds use the native exit behavior and show every
  # open panel; interior north/side gates are step warps, not directional arrows.
  for x,y in ([(8,17),(9,17)] if n==LH[0] else [(3,6),(4,6)] if n==LIFT else [(7,11),(8,11)] if n==PORT else []):t[y*w+x]=ART['exit']['start']
  for o in m['object_events']:
   x,y=o['x'],o['y']
   if n==LH[5] and o['graphics_id']=='OBJ_EVENT_GFX_AREA_LANTERN':
    # The solid object owns this footprint, just like native heal-machine NPCs.
    # A second map-wall flag strands the saved object and fails object spawning.
    t[y*w+x]=0x3000|ART['stone']['start']
   assert 0<=x<w and 0<=y<h and t[y*w+x]&0xc00==0,(n,'Actor intersects source furniture',o)
  lid=m['layout'];out=n in [BAL,QUAY];l=dict(id=lid,name=ls[lid]['name'] if lid in ls else n+'_Layout',width=w,height=h,primary_tileset='gTileset_HgssOlivineLandmarkOutdoor' if out else 'gTileset_HgssOlivineLandmarkIndoor',secondary_tileset='gTileset_HgssOlivineLandmarks',border_filepath=f'data/layouts/{n}/border.bin',blockdata_filepath=f'data/layouts/{n}/map.bin',layout_version='emerald')
  if lid in ls:ls[lid].clear();ls[lid].update(l)
  else:layouts['layouts'].append(l);ls[lid]=l
  if n in NEW_IDS and n not in groups['gMapGroup_CrossroadsJohtoExpansion']:
   groups['gMapGroup_CrossroadsJohtoExpansion'].append(n);assert groups['gMapGroup_CrossroadsJohtoExpansion'].index(n)<127
  if n in NEW_IDS and not any(v['name']==n for v in manifest['planned']):manifest['planned'].append(dict(name=n,kind='hgss',parent='OlivineCity',cluster='west',status='implemented-runtime-review-pending'))
  write(l['blockdata_filepath'],struct.pack('<'+str(w*h)+'H',*t));write(l['border_filepath'],struct.pack('<4H',*([0x1170 if out else 0x400|ART['void']['start']]*4)));js(f'data/maps/{n}/map.json',m)
  code=f'{n}_MapScripts::\n'
  if n in [LH[0],LH[5]]:
   code+=f'    map_script MAP_SCRIPT_ON_TRANSITION, {n}_LiftReturn\n    .byte 0\n{n}_LiftReturn:\n    setdynamicwarp {m["id"]}, {3 if n==LH[0] else 1}\n    end\n'
  else:code+='    .byte 0\n'
  write(f'data/maps/{n}/scripts.inc',code)
  review.append(dict(name=n,source_header=HEADERS[n],source=facts[HEADERS[n]]['source'],dimensions=[w,h],warps=m['warp_events'],source_warp_count=len(facts[HEADERS[n]]['warps']),adaptations=['Original native GBA props/palettes replace DS perspective models; source coordinate origin retained','No source trainer/story/reward flags imported','Wide GBA door/stair aliases append without removing historical warp indices'],runtime='PENDING actual delivery-ROM testing',visual='PENDING owner acceptance'))
 review.append(dict(window_drop=dict(map=LH[3],from_xy=[16,9],script='Hgss_OlivineWindowDrop',destination=BAL,arrival=[14,9],classification='intentional HGSS one-way drop; return via balcony door and western3F staircase'),dynamic_elevator=dict(map=LIFT,door_indices=[0,1],panels=[dict(x=2,y=2,target=LH[0],warp=3),dict(x=5,y=2,target=LH[5],warp=1)],state='existing native dynamicWarp only; no new permanent progress'),transport_boundary=dict(map=QUAY,source_ship_warp=[27,20],native_sign=[27,21],status='S.S. Aqua sailing/ship outside this map pass; accepted Harbor Office travel retained separately')))
 js('crossroads/hgss/olivine-landmark-review.json',review);js('data/layouts/layouts.json',layouts);js('data/maps/map_groups.json',groups);js('crossroads/johto/manifest.json',manifest)
 inc=(R/'data/event_scripts.s').read_text()
 paths=[f'data/maps/{n}/scripts.inc' for n in LH+[BAL,LIFT,PORT,QUAY]]+['crossroads/scripts/hgss_olivine_landmarks.inc']
 # Existing includes use spaces while newer generators use tabs. Identify the
 # quoted path, preserving the first original line and every unrelated include.
 kept=[];seen_includes=set()
 for line in inc.splitlines():
  match=re.search(r'\.include\s+"([^"]+)"',line)
  if match and match.group(1) in paths:
   if match.group(1) in seen_includes:continue
   seen_includes.add(match.group(1))
  kept.append(line)
 for path in paths:
  if path not in seen_includes:kept.append(f'\t.include "{path}"')
 inc='\n'.join(kept)+'\n'
 write('data/event_scripts.s',inc)
 write('crossroads/scripts/hgss_olivine_landmarks.inc',SCRIPTS)
 print('HGSS lighthouse six floors/balcony/lift and port terminal/quay generated; delivery-ROM testing required')
SCRIPTS='''@ Ambient exploration only. No badge, reward, encounter or plot flags.
Hgss_OlivineWindowDrop::
    lockall
    playse SE_FALL
    delay 16
    warp MAP_OLIVINE_CITY_LIGHTHOUSE_BALCONY, 14, 9
    waitstate
    releaseall
    end
Hgss_OlivineLift1F::
    lockall
    msgbox Hgss_OlivineLift1FText, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Hgss_OlivineLiftCancel
    setdynamicwarp MAP_OLIVINECITY_LIGHTHOUSE_1F, 3
    playse SE_ELEVATOR
    delay 45
    msgbox Hgss_OlivineLiftArrived, MSGBOX_DEFAULT
    releaseall
    end
Hgss_OlivineLift6F::
    lockall
    msgbox Hgss_OlivineLift6FText, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Hgss_OlivineLiftCancel
    setdynamicwarp MAP_OLIVINECITY_LIGHTHOUSE_6F, 1
    playse SE_ELEVATOR
    delay 45
    msgbox Hgss_OlivineLiftArrived, MSGBOX_DEFAULT
    releaseall
    end
Hgss_OlivineLiftCancel:
    releaseall
    end
Hgss_OlivineLift1FText:
    .string "1F - VISITOR DECK\\nTake the lift to the ground floor?$"
Hgss_OlivineLift6FText:
    .string "6F - LANTERN ROOM\\nTake the lift to the top floor?$"
Hgss_OlivineLiftArrived:
    .string "The lift settles at the landing.$"
Hgss_OlivinePortDesk::
    msgbox Hgss_OlivinePortDeskText, MSGBOX_NPC
    end
Hgss_OlivinePortDeskText:
    .string "The quays are open to visitors.\\nThe HARBOR OFFICE handles travel.$"
Hgss_OlivinePortVisitor::
    msgbox Hgss_OlivinePortVisitorText, MSGBOX_NPC
    end
Hgss_OlivinePortVisitorText:
    .string "The side passage leads back to\\nthe older inspection pier.$"
Hgss_OlivineShipBoundary::
    msgbox Hgss_OlivineShipBoundaryText, MSGBOX_SIGN
    end
Hgss_OlivineShipBoundaryText:
    .string "S.S. AQUA BOARDING\\nPassenger sailings are not operating.$"
'''
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');generate(p.parse_args().check)
