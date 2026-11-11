#!/usr/bin/env python3
"""Private native Center basement palette/furniture; shared Center stays exact."""
import argparse,io,json,struct
from pathlib import Path
from tileset_registration import upsert
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];S=R/'data/tilesets/secondary/pokemon_center';D=R/'data/tilesets/secondary/hgss_center_basement';A=R/'crossroads/hgss/art/center-basement'
USED=[513,514,522,523,530,545,573,574,581,582,673]
PAL=[(0,0,0),(32,52,68),(69,98,117),(113,151,170),(166,199,214),(214,233,241),(248,254,255),(42,117,157),(75,170,213),(143,219,244),(245,198,72),(255,231,134),(157,117,43),(111,137,146),(69,88,98),(217,217,205)]
LOGOPAL=[(0,0,0),(238,222,164),(246,238,189),(255,255,197),(0,0,0),(38,133,88),(63,168,117),(22,92,66),(85,190,139),(202,231,211),(245,250,235)]+[(0,0,0)]*5
def artwork(reception=False):
 def make(size):
  q=Image.new('P',size);q.putpalette(sum((list(x)for x in PAL),[])+[0]*720);return q,ImageDraw.Draw(q)
 table,d=make((32,32));d.rectangle((4,5,27,27),fill=1);d.rectangle((5,6,26,23),fill=3);d.rectangle((7,7,24,21),fill=7);d.polygon([(8,8),(22,8),(8,20)],fill=9);d.line((9,21,24,9),fill=8,width=2);d.line((7,24,7,29),fill=13,width=2);d.line((24,24,24,29),fill=13,width=2);d.rectangle((5,6,26,23),outline=5,width=2)
 stools=[]
 for color in (10,7):
  im,d=make((16,16));d.rectangle((3,10,4,14),fill=13);d.rectangle((11,10,12,14),fill=13);d.rounded_rectangle((1,2,14,11),radius=3,fill=1);d.rounded_rectangle((2,2,13,10),radius=2,fill=color);d.line((4,3,11,3),fill=11 if color==10 else 9);d.line((4,10,11,10),fill=12 if color==10 else 2);stools.append(im)
 terminal,d=make((16,32));d.rectangle((4,19,11,30),fill=2);d.rectangle((2,28,13,31),fill=3);d.rounded_rectangle((0,1,15,23),radius=3,fill=1);d.rectangle((2,3,13,15),fill=3);d.rectangle((3,4,12,14),fill=7);d.ellipse((5,5,11,12),outline=9);d.line((8,5,8,12),fill=8);d.line((5,8,11,8),fill=9);d.rectangle((3,18,12,20),fill=5);d.point((12,22),fill=10)
 door,d=make((16,32));d.rectangle((0,0,15,31),fill=1);d.rectangle((2,2,13,29),fill=3);d.rectangle((3,3,12,26),fill=7);d.rectangle((4,4,11,14),fill=9);d.line((4,4,11,4),fill=6);d.rectangle((4,17,11,25),fill=8);d.rectangle((2,29,13,31),fill=13)
 if reception:
  logo,d=make((80,64));logo.putpalette(sum((list(c)for c in LOGOPAL),[])+[0]*720)
  d.ellipse((5,8,74,55),outline=7,width=2);d.ellipse((8,10,71,53),outline=5,width=4);d.line((9,31,70,31),fill=5,width=5);d.ellipse((30,22,49,41),fill=0,outline=5,width=4);d.arc((13,14,67,50),190,264,fill=8,width=2)
  return [('communication_back_panel',door),('floor_emblem',logo)]
 booth,d=make((48,48))
 for x0,x1 in [(1,6),(41,46)]:
  d.rectangle((x0,0,x1,43),fill=2);d.line((x0,1,x0,42),fill=5,width=2);d.line((x1,1,x1,42),fill=7,width=2)
 d.rounded_rectangle((1,32,46,47),radius=3,fill=1);d.rectangle((3,32,44,42),fill=7);d.line((4,32,43,32),fill=6,width=2);d.line((4,43,43,43),fill=2,width=2);d.rectangle((3,45,44,47),fill=3);d.rectangle((36,34,43,38),fill=5)
 return [('waiting_table',table),('yellow_stool',stools[0]),('blue_stool',stools[1]),('communication_terminal',terminal),('communication_back_panel',door),('communication_booth',booth)]
def build(check=False,preview=None,reception=False):
 D=R/('data/tilesets/secondary/hgss_center_reception' if reception else 'data/tilesets/secondary/hgss_center_basement');A=R/('crossroads/hgss/art/center-reception' if reception else 'crossroads/hgss/art/center-basement')
 source=Image.open(S/'tiles.png');m=list(struct.unpack('<'+str((S/'metatiles.bin').stat().st_size//2)+'H',(S/'metatiles.bin').read_bytes()));attrs=list(struct.unpack('<'+str((S/'metatile_attributes.bin').stat().st_size//2)+'H',(S/'metatile_attributes.bin').read_bytes()));words=[0x6200]*len(m);at=[0x1000]*len(attrs);sheet=Image.new('P',(128,256));sheet.putpalette(source.getpalette());unique={bytes(64):0};cursor=1
 def tile(im,bank,flips=0):
  nonlocal cursor
  b=im.tobytes()
  if b not in unique:assert cursor<512;unique[b]=cursor;sheet.paste(im,(cursor%16*8,cursor//16*8));cursor+=1
  return(512+unique[b])|(bank<<12)|flips
 used=[513, 514, 515, 516, 517, 518, 522, 523, 530, 544, 545, 546, 547, 548, 554, 555, 564, 584, 585, 586, 587, 592, 593, 594, 595, 600, 601, 603, 608, 620, 621, 622, 623, 649] if reception else USED
 for n in used:
  k=n-512;at[k]=attrs[k]
  for j,v in enumerate(m[k*8:k*8+8]):
   z=v&1023
   if z<512:words[k*8+j]=v;continue
   i=z%512;words[k*8+j]=tile(source.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8)),v>>12,v&0xc00)
 art=artwork(reception);spec={}
 if reception:
  # The emblem is real ground, not an opaque foreground overlay. Flatten its
  # transparent holes onto the unchanged native floor, then use bottom glyphs
  # with a blank top layer so Joe always renders naturally above it.
  floor=Image.new('P',(16,16));floor.putpalette(sum((list(c)for c in LOGOPAL),[])+[0]*720)
  for j,v in enumerate(m[2*8:2*8+4]):
   i=(v&1023)%512;part=source.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8));assert set(part.tobytes())<={10,11,12};part=Image.frombytes('P',(8,8),bytes(z-9 for z in part.tobytes()));floor.paste(part,(j%2*8,j//2*8))
  converted=[]
  for name,im in art:
   if name=='floor_emblem':
    im=Image.frombytes('P',im.size,bytes(v or floor.getpixel((i%80%16,i//80%16))for i,v in enumerate(im.tobytes())));im.putpalette(floor.getpalette())
   converted.append((name,im))
  art=converted
 for name,im in art:
  spec[name]=dict(start=512+len(at),width=im.width//16,height=im.height//16)
  for y in range(im.height//16):
   for x in range(im.width//16):
    under=words[(514-512)*8:(514-511)*8][:4]
    bank=10 if reception and name=='floor_emblem' else 12 if reception else 9
    refs=[tile(im.crop((x*16+dx,y*16+dy,x*16+dx+8,y*16+dy+8)),bank)for dx,dy in [(0,0),(8,0),(0,8),(8,8)]]
    words.extend(refs+[0]*4 if reception and name=='floor_emblem' else under+refs)
    # Preserve the actual native1F layer type/behavior per replaced cell.
    # Wall top20b and floor202 use layer0; counter221 uses layer1. Uniform
    # layer1 would change Joe/floor overlap even with collision bits intact.
    at.append(attrs[(0x20b if y==0 else 0x221)-512] if reception and name=='communication_back_panel' else attrs[0x202-512] if reception else attrs[(0x221 if y==0 else 0x202)-512] if name=='communication_back_panel' else (attrs[(0x202 if y<2 else 0x221)-512]|(0x80 if y==2 and x==1 else 0)) if name=='communication_booth' else 0x1000)
 if reception:
  # A real front desk must let A reach its receptionist across the counter.
  # Only this pixel-identical private variant gets MB_COUNTER; changing native
  # 0x221 globally would also affect unrelated walls/nurse furniture.
  spec['service_counter']=dict(start=512+len(at),width=1,height=1)
  words.extend(words[(0x221-512)*8:(0x221-511)*8]);at.append(attrs[0x221-512]|0x80)
 assert len(at)<=512
 if preview:
  im=Image.new('RGB',(sum(q.width for n,q in art),max(q.height for n,q in art)));x=0
  for n,q in art:im.paste(q.convert('RGB'),(x,0));x+=q.width
  im.save(preview);print(preview);return
 def write(p,b):
  if isinstance(b,str):b=b.encode()
  if check:assert p.exists()and p.read_bytes()==b,('Regenerate Center basement',str(p))
  elif not p.exists()or p.read_bytes()!=b:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 if check:assert Image.open(D/'tiles.png').tobytes()==sheet.tobytes()
 else:D.mkdir(parents=True,exist_ok=True);sheet.save(D/'tiles.png',bits=4)
 write(D/'metatiles.bin',struct.pack('<'+str(len(words))+'H',*words));write(D/'metatile_attributes.bin',struct.pack('<'+str(len(at))+'H',*at))
 for i in range(16):
  rows=(S/f'palettes/{i:02}.pal').read_text().splitlines();colors=[list(map(int,x.split()))for x in rows[3:]]
  if not reception and i==6:
   for k,c in {5:(38,95,135),6:(65,132,172),7:(111,174,202),8:(160,211,231),9:(105,160,184),10:(153,202,219),11:(181,220,230),12:(214,241,243)}.items():colors[k]=list(c)
  if not reception and i==7:
   for k,c in {5:(90,136,161),6:(138,185,209),7:(193,226,232),8:(87,146,176)}.items():colors[k]=list(c)
  if not reception and i==9:colors=PAL
  if reception and i==10:colors=LOGOPAL
  if reception and i==12:colors=PAL
  write(D/f'palettes/{i:02}.pal',('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c))for c in colors)+'\n').replace('\n','\r\n'))
 write(A/'manifest.json',json.dumps(dict(specs=spec,tiles=cursor,metatiles=len(at),retained_native_metatiles=used,palette_adaptation='Private cool-blue wall/floor/counter palette based on actual HGSS basement; shared native Center palettes unchanged',source='Original native GBA furniture, no HGSS pixels copied'),indent=2)+'\n')
 for name,im in art:
  b=io.BytesIO();im.save(b,format='PNG',bits=4,transparency=0);write(A/(name+'.png'),b.getvalue())
 begin='// BEGIN HGSS CENTER BASEMENT';end='// END HGSS CENTER BASEMENT';blocks={
 'src/data/tilesets/headers.h':'const struct Tileset gTileset_HgssCenterBasement = {.isCompressed=TRUE,.isSecondary=TRUE,.tiles=gTilesetTiles_HgssCenterBasement,.palettes=gTilesetPalettes_HgssCenterBasement,.metatiles=gMetatiles_HgssCenterBasement,.metatileAttributes=gMetatileAttributes_HgssCenterBasement,.callback=NULL};',
 'src/data/tilesets/graphics.h':'const u32 gTilesetTiles_HgssCenterBasement[] = INCGFX_U32("data/tilesets/secondary/hgss_center_basement/tiles.png", ".4bpp.fastSmol");\nconst u16 gTilesetPalettes_HgssCenterBasement[][16] = {\n'+''.join(f' INCGFX_U16("data/tilesets/secondary/hgss_center_basement/palettes/{i:02}.pal", ".gbapal"),\n'for i in range(16))+'};',
 'src/data/tilesets/metatiles.h':'const u16 gMetatiles_HgssCenterBasement[] = INCBIN_U16("data/tilesets/secondary/hgss_center_basement/metatiles.bin");\nconst u16 gMetatileAttributes_HgssCenterBasement[] = INCBIN_U16("data/tilesets/secondary/hgss_center_basement/metatile_attributes.bin");',
 'include/tilesets.h':'extern const struct Tileset gTileset_HgssCenterBasement;'}
 if reception:
  begin=begin.replace('BASEMENT','RECEPTION');end=end.replace('BASEMENT','RECEPTION')
  blocks={path:block.replace('HgssCenterBasement','HgssCenterReception').replace('hgss_center_basement','hgss_center_reception')for path,block in blocks.items()}
 for path,block in blocks.items():
  p=R/path;s=p.read_text();section=begin+'\n#if !IS_FRLG\n'+block+'\n#endif\n'+end
  s=upsert(s,begin,end,section,externs=path=='include/tilesets.h')
  write(p,s)
 print('Private cool Center basement:',cursor,'graphics;',len(at),'metatiles; shared Center unchanged')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--preview');a=p.parse_args();build(a.check,a.preview)
 if not a.preview:build(a.check,reception=True)
