#!/usr/bin/env python3
"""Original HGSS-reference gate interior pixels in a private GBA tile pool.

No HGSS screenshot pixels are imported. All changes are per-cell art replacements
with the V7 collision, elevation and metatile behavior/layer attributes retained.
"""
import argparse,io,json,struct
from pathlib import Path
from tileset_registration import upsert
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];D=R/'data/tilesets/secondary/hgss_gate_interior';A=R/'crossroads/hgss/art/gate-interior'
BASE='3f935d5e8600c5a280b9172b555edb35ca52b6c0'
COLORS=[(0,0,0),(45,57,64),(83,103,113),(127,148,155),(169,187,189),(217,224,212),(245,235,196),(165,146,107),(105,155,189),(155,215,242),(218,244,249),(37,92,62),(57,132,74),(126,182,89),(177,95,35),(235,156,52)]
def indexed(size,color=0):
 im=Image.new('P',size,color);im.putpalette(sum((list(c)for c in COLORS),[])+[0]*720);return im
def artwork():
 floor=indexed((16,16),4);q=ImageDraw.Draw(floor);q.polygon([(8,0),(15,8),(8,15),(0,8)],fill=5,outline=3);q.line((0,0,0,15),fill=3);q.line((0,0,15,0),fill=3)
 wall=indexed((160,32),6);q=ImageDraw.Draw(wall);q.rectangle((0,0,159,3),fill=7);q.line((0,4,159,4),fill=5)
 for x in range(0,160,16):q.line((x,4,x,31),fill=7)
 for x in (24,52,80,108):
  q.rectangle((x,7,x+24,22),fill=2);q.rectangle((x+2,9,x+22,20),fill=8);q.polygon([(x+2,18),(x+11,9),(x+19,9),(x+8,20),(x+2,20)],fill=9);q.line((x+3,10,x+21,10),fill=10)
 q.line((0,28,159,28),fill=7);q.rectangle((0,29,159,31),fill=3)
 counter=indexed((96,32),3);q=ImageDraw.Draw(counter);q.rounded_rectangle((0,0,95,31),radius=5,fill=1);q.rounded_rectangle((2,1,93,29),radius=4,fill=8);q.rounded_rectangle((5,3,90,25),radius=3,fill=9)
 q.rectangle((12,3,83,18),fill=2);q.rectangle((15,4,80,16),fill=4)
 for x in range(15,81,8):q.line((x,4,x+12,16),fill=3)
 q.line((4,27,91,27),fill=10);q.rectangle((4,29,91,30),fill=2)
 plant=indexed((16,32));q=ImageDraw.Draw(plant);q.ellipse((1,3,14,17),fill=11)
 for x,y in [(3,4),(7,2),(10,6),(5,9),(10,11),(2,11)]:q.ellipse((x-2,y-1,x+3,y+4),fill=12);q.point((x,y),fill=13)
 q.rectangle((3,18,12,28),fill=14);q.rectangle((2,18,13,21),fill=15);q.line((4,23,4,27),fill=15);q.line((4,29,11,29),fill=1)
 side=indexed((16,16),3);q=ImageDraw.Draw(side);q.rectangle((0,0,6,15),fill=6);q.line((6,0,6,15),fill=7);q.line((12,0,12,15),fill=2);q.rectangle((13,0,15,15),fill=1)
 return dict(floor=floor,wall=wall,counter=counter,plant=plant,side=side,void=indexed((16,16)))
def plan(before):
 out={}
 # Gray floor includes old transparent pillar overhangs. It keeps every native
 # ground/warp attribute, rather than changing source walkability for plants.
 for i,v in enumerate(before):
  x,y=i%12,i//12
  if not v&0xc00:out[(x,y)]=('floor',0,0)
 for y in (2,3):
  for x in range(1,11):out[(x,y)]=('wall',x-1,y-2)
 for x in (2,10):out[(x,1)]=('void',0,0)
 for top in (4,9):
  for y in (top,top+1):
   for x in range(3,9):out[(x,y)]=('counter',x-3,y-top)
 for y in range(4,11):
  for x in (0,11):out[(x,y)]=('floor' if 6<=y<=8 else 'side',0,0)
 for x in (1,9):out[(x,11)]=('side',0,0)
 for x in (2,10):
  for base in (3,11):out[(x,base-1)]=('plant',0,0);out[(x,base)]=('plant',0,1)
 return out
def build(check=False,preview=None):
 contract=json.loads((R/'crossroads/hgss/contracts/gate-interior-art-qa09.json').read_text());assert contract['source_commit']==BASE;before=contract['before_words'];assert len(before)==144
 temple=R/'data/tilesets/secondary/hgss_temple';original=Image.open(temple/'tiles.png');meta=list(struct.unpack('<'+str((temple/'metatiles.bin').stat().st_size//2)+'H',(temple/'metatiles.bin').read_bytes()));oldattrs=list(struct.unpack('<'+str((temple/'metatile_attributes.bin').stat().st_size//2)+'H',(temple/'metatile_attributes.bin').read_bytes()))
 sheet=indexed((128,256));sheet.putpalette(original.getpalette());glyphs={bytes(64):0};cursor=1
 def pack(pix,bank,flips=0):
  nonlocal cursor
  k=pix.tobytes()
  if k not in glyphs:assert cursor<512;glyphs[k]=cursor;sheet.paste(pix,(cursor%16*8,cursor//16*8));cursor+=1
  return 512+glyphs[k]|bank<<12|flips
 words=[0x6200]*len(meta);attrs=[0x1000]*len(oldattrs);used=sorted({v&1023 for v in before})
 for n in used:
  assert n>=512;k=n-512;attrs[k]=oldattrs[k]
  for j,v in enumerate(meta[k*8:k*8+8]):
   t=v&1023
   if t<512:words[k*8+j]=v;continue
   i=t-512;words[k*8+j]=pack(original.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8)),v>>12,v&0xc00)
 art=artwork();placements=[];newids={}
 for (x,y),(kind,dx,dy)in sorted(plan(before).items(),key=lambda q:(q[0][1],q[0][0])):
  a=oldattrs[(before[y*12+x]&1023)-512];key=(kind,dx,dy,a)
  if key not in newids:
   newids[key]=512+len(attrs);im=art[kind];refs=[pack(im.crop((dx*16+X,dy*16+Y,dx*16+X+8,dy*16+Y+8)),7)for X,Y in [(0,0),(8,0),(0,8),(8,8)]];words.extend([0x6200]*4+refs);attrs.append(a)
  placements.append(dict(x=x,y=y,kind=kind,source_tile=[dx,dy],metatile=newids[key],before=before[y*12+x],after=before[y*12+x]&0xfc00|newids[key]))
 assert len(attrs)<=512
 assert [{k:p[k]for k in ('x','y','before','after')}for p in placements]==contract['changes'],'Exact reviewed gate-art contract differs'
 manifest=dict(source_commit=BASE,tiles=cursor,metatiles=len(attrs),retained_temple_metatiles=used,placements=placements,plant_bases=[[2,3],[10,3],[2,11],[10,11]],source='Original indexed GBA artwork after actual final HGSS Gate inside raster; same matrix0070 and areaData63 as Ecruteak gates, no reference pixels imported',reference_url='https://archives.bulbagarden.net/media/upload/2/2f/Gate_inside_HGSS.png')
 if preview:
  im=Image.new('RGB',(192,192));
  for p in placements:
   kind=p['kind'];dx,dy=p['source_tile'];q=art[kind].crop((dx*16,dy*16,dx*16+16,dy*16+16));im.paste(q.convert('RGB'),(p['x']*16,p['y']*16))
  Path(preview).parent.mkdir(parents=True,exist_ok=True);im.save(preview);print('Native gate material preview:',preview);return manifest
 def write(p,b):
  if isinstance(b,str):b=b.encode()
  if check:assert p.exists()and p.read_bytes()==b,('Regenerate gate interior',str(p))
  elif not p.exists()or p.read_bytes()!=b:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 if check:assert Image.open(D/'tiles.png').tobytes()==sheet.tobytes()
 else:D.mkdir(parents=True,exist_ok=True);sheet.save(D/'tiles.png',bits=4)
 write(D/'metatiles.bin',struct.pack('<'+str(len(words))+'H',*words));write(D/'metatile_attributes.bin',struct.pack('<'+str(len(attrs))+'H',*attrs))
 for i in range(16):
  b=(temple/f'palettes/{i:02}.pal').read_bytes()
  if i==7:b=('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c))for c in COLORS)+'\n').replace('\n','\r\n').encode()
  write(D/f'palettes/{i:02}.pal',b)
 write(A/'manifest.json',json.dumps(manifest,indent=2)+'\n')
 for n,im in art.items():b=io.BytesIO();im.save(b,format='PNG',bits=4,transparency=0);write(A/(n+'.png'),b.getvalue())
 begin='// BEGIN ECRUTEAK GATE INTERIOR ART';end='// END ECRUTEAK GATE INTERIOR ART';name='HgssGateInterior';blocks={
 'src/data/tilesets/headers.h':f'const struct Tileset gTileset_{name} = {{ .isCompressed=TRUE,.isSecondary=TRUE,.tiles=gTilesetTiles_{name},.palettes=gTilesetPalettes_{name},.metatiles=gMetatiles_{name},.metatileAttributes=gMetatileAttributes_{name},.callback=NULL }};',
 'src/data/tilesets/graphics.h':f'const u32 gTilesetTiles_{name}[] = INCGFX_U32("data/tilesets/secondary/hgss_gate_interior/tiles.png", ".4bpp.fastSmol");\nconst u16 gTilesetPalettes_{name}[][16] = {{\n'+''.join(f' INCGFX_U16("data/tilesets/secondary/hgss_gate_interior/palettes/{i:02}.pal", ".gbapal"),\n'for i in range(16))+'};',
 'src/data/tilesets/metatiles.h':f'const u16 gMetatiles_{name}[] = INCBIN_U16("data/tilesets/secondary/hgss_gate_interior/metatiles.bin");\nconst u16 gMetatileAttributes_{name}[] = INCBIN_U16("data/tilesets/secondary/hgss_gate_interior/metatile_attributes.bin");',
 'include/tilesets.h':f'extern const struct Tileset gTileset_{name};'}
 for path,body in blocks.items():
  p=R/path;text=p.read_text();section=begin+'\n#if !IS_FRLG\n'+body+'\n#endif\n'+end
  text=upsert(text,begin,end,section,externs=path=='include/tilesets.h')
  write(p,text)
 print('Private gate interior:',cursor,'graphics;',len(attrs),'metatiles;',len(placements),'art cells per gate; unchanged shared Temple')
 return manifest
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--preview');a=p.parse_args();build(a.check,a.preview)
