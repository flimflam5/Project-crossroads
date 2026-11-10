#!/usr/bin/env python3
"""Original GBA adaptations of inspected Violet architecture; native terrain kept.

PNG operations are atlas cropping/palette/engine conversion, not screenshot art.
No DS graphics enter the tileset. Gym art is fitted separately from owner's ZIP.
"""
import argparse,json,struct,re
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2];A=R/'crossroads/hgss/art/violet'
def generate(check=False):
 def write(p,b):
  if isinstance(b,str):b=b.encode()
  p=R/p
  if p.suffix=='.pal':b=b.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
  if check:assert p.exists() and p.read_bytes()==b,('Regenerate Violet assets',str(p))
  elif not p.exists() or p.read_bytes()!=b:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 P=R/'data/tilesets/primary/hgss_violet';S=R/'data/tilesets/secondary/hgss_violet';general=R/'data/tilesets/primary/general';native=json.loads((R/'crossroads/hgss/art/native-manifest.json').read_text());gm=list(struct.unpack('<4096H',(general/'metatiles.bin').read_bytes()));ga=list(struct.unpack('<512H',(general/'metatile_attributes.bin').read_bytes()));gm[0x1ff*8:0x200*8]=[0x30aa,0x30ab,0x30aa,0x30ab,0,0,0,0];ga[0x1ff]=0x1000;terrain=set(native['terrain'])|{0x1ff,0x170,0x171,0x1d4,0x1d5,0x1dc,0x1dd,0x24,0x71,0x75,0xc6,0xa7};protected=set(range(432,512))|{v&1023 for id in terrain for v in gm[id*8:id*8+8]};free=[i for i in range(512,1024)]+[i for i in range(432) if i not in protected];sheets=[Image.open(general/'tiles.png').copy(),Image.new('P',(128,256))];sheets[1].putpalette(sheets[0].getpalette());images={};meta=[];attrs=[];spec={};unique={};cursor=0
 def cut(im,box,size):
  c=im.crop(box);alpha=c.getchannel('A').point(lambda n:255 if n>=230 else 0);c.putalpha(alpha);bb=alpha.getbbox();assert bb;c=c.crop(bb).resize(size,Image.Resampling.NEAREST);return c
 src=Image.open(A/'source.png');jobs=[('sprout',(96,192),7,3),('school',(128,80),10,3),('house',(48,64),7,1)]
 for i,(name,size,bank,door) in enumerate(jobs):images[name]=cut(src,(round(i*src.width/3+12),12,round((i+1)*src.width/3-12),src.height-12),size)
 school=Image.open(A/'school-source.png');images['school']=cut(school,(0,0,school.width,school.height),(128,80))
 gate=Image.open(A/'gate-source.png');images['gate']=cut(gate,(0,0,gate.width,gate.height),(96,64));jobs.append(('gate',(96,64),6,5))
 bridge=Image.open(A/'bridge-source.png');images['bridge']=cut(bridge,(0,0,bridge.width,bridge.height),(80,80));jobs.append(('bridge',(80,80),9,-1))
 # Use the same verified stone texture as the accepted Ecruteak adaptation.
 # General0x24 is flowers, not paving; metatile names/behavior are not colors.
 slate=R/'data/tilesets/secondary/slateport';stone=Image.open(slate/'tiles.png').crop((48,32,56,40));colors=[tuple(map(int,l.split())) for l in (slate/'palettes/06.pal').read_text().splitlines()[3:]]
 stone.putpalette([v for rgb in colors for v in (int(sum(rgb)/3*.8),int(sum(rgb)/3*.84),int(sum(rgb)/3*.73))]);floor=Image.new('RGBA',(16,16))
 for dx,dy in [(0,0),(8,0),(0,8),(8,8)]:floor.paste(stone.convert('RGBA'),(dx,dy))
 images['paving']=floor;jobs.append(('paving',(16,16),12,-1))
 # Existing center/mart are original project adaptations, not Emerald warehouse
 # stand-ins. Share school/Center palette; house and tower share temple colors.
 for name,bank in [('center',10),('mart',11)]:
  e=native['specs'][name];im=Image.open(R/f'crossroads/hgss/art/{name}-native.png').convert('RGBA');images[name]=im;jobs.append((name,im.size,bank,e['door_x']))
 pals={}
 for bank in sorted({b for _,_,b,_ in jobs}):
  group=[images[n] for n,_,b,_ in jobs if b==bank];strip=Image.new('RGB',(sum(i.width for i in group),max(i.height for i in group)));x=0
  for im in group:strip.paste(im,(x,0),im.getchannel('A'));x+=im.width
  pal=strip.quantize(colors=15,method=Image.Quantize.MEDIANCUT).getpalette()[:45];pals[bank]=([0,0,0]+[v//8*8 for v in pal]+[0]*48)[:48]
 def tile(im,bank):
  nonlocal cursor
  key=im.tobytes()
  if key not in unique:
   assert cursor<len(free),('Violet graphics capacity',cursor,len(free));i=free[cursor];cursor+=1;unique[key]=i;part=i%512;sheets[i//512].paste(im,(part%16*8,part//16*8))
  return unique[key]|bank<<12
 # Reserve the transparent pixel source explicitly; palette0 is never inferred.
 empty=tile(Image.new('P',(8,8)),6)
 for name,size,bank,door in jobs:
  im=images[name];ref=Image.new('P',(1,1));ref.putpalette(pals[bank]+[0]*720);indexed=im.convert('RGB').quantize(palette=ref,dither=Image.Dither.NONE);values=bytearray(indexed.tobytes());mask=im.getchannel('A').tobytes()
  for i in range(len(values)):
   if mask[i]<128:values[i]=0
   elif values[i]==0:values[i]=1
  indexed=Image.frombytes('P',im.size,bytes(values));indexed.putpalette(pals[bank]);w,h=im.width//16,im.height//16;start=512+len(attrs)
  for y in range(h):
   for x in range(w):
    top=[tile(indexed.crop((x*16+dx,y*16+dy,x*16+dx+8,y*16+dy+8)),bank) for dx,dy in [(0,0),(8,0),(0,8),(8,8)]];under=0x170 if name=='bridge' else 1;meta.extend(list(gm[under*8:under*8+4])+top);attrs.append((0x1000 if name=='bridge' or y>=h-2 else 0)|(0x60 if (x,y)==(door,h-1) else 0))
  if name=='school':attrs[(h-1)*w+2+start-512]|=0x60
  spec[name]=dict(start=start,width=w,height=h,door_x=door,door_y=h-1,palette=bank)
  if not check:indexed.save(A/(name+'.png'),bits=4,transparency=0)
 # Roofs preserve the source pond/road below them instead of painting grass
 # rectangles over Violet's bridges. Variants share every foreground tile.
 source=json.loads((R/'crossroads/hgss/canonical_events/johto-outdoor-geometry.json').read_text())['areas']['MAP_VIOLET'];perms=[0x8000]*4096
 for c in source['cells']:
  for y in range(32):
   for x in range(32):perms[(c['y']*32+y)*64+c['x']*32+x]=c['permissions'][y*32+x]
 doors={'sprout':(39,4),'school':(47,33),'house':(36,53),'gate':(6,22),'center':(49,47),'mart':(21,33)}
 for name,(dx,dy) in doors.items():
  a=spec[name];a['stamps']=[]
  for y in range(a['height']):
   for x in range(a['width']):
    sx,sy=dx-a['door_x']+x,dy-a['door_y']+y;p=perms[sy*64+sx] if 0<=sx<64 and 0<=sy<64 else 0
    under=0x170 if p&255 in [16,17,19,21] else 0x24 if p&0x600 else 1;id=a['start']+y*a['width']+x
    if under!=1:
     a['stamps'].append(512+len(attrs));base=meta[(spec['paving']['start']-512)*8+4:(spec['paving']['start']-512)*8+8] if under==0x24 else list(gm[under*8:under*8+4]);meta.extend(base+meta[(id-512)*8+4:(id-512)*8+8]);attrs.append(attrs[id-512])
    else:a['stamps'].append(id)
 # Ordinary paving, flower tufts and bridge decking do not grant encounters.
 for name,id in [('flowers',4),('water',0x170)]:spec[name]=dict(start=512+len(attrs),width=1,height=1);meta.extend(gm[id*8:id*8+8]);attrs.append(ga[id] if name=='water' else 0x1000)
 spec['portal']=dict(start=512+len(attrs),width=1,height=1);m=spec['paving']['start']-512;meta.extend(meta[m*8:m*8+8]);attrs.append(0x1060)
 assert len(attrs)<=512 and cursor<=len(free)
 for k,path in enumerate([P,S]):
  path.mkdir(parents=True,exist_ok=True)
  if check:assert Image.open(path/'tiles.png').tobytes()==sheets[k].tobytes()
  else:sheets[k].save(path/'tiles.png',bits=4)
  for i in range(16):write(str((path/f'palettes/{i:02}.pal').relative_to(R)),('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,pals[i][j:j+3])) for j in range(0,48,3))+'\n') if k==1 and i in pals else (general/f'palettes/{i:02}.pal').read_bytes())
 write('data/tilesets/primary/hgss_violet/metatiles.bin',struct.pack('<4096H',*gm));write('data/tilesets/primary/hgss_violet/metatile_attributes.bin',struct.pack('<512H',*ga));write('data/tilesets/secondary/hgss_violet/metatiles.bin',struct.pack('<'+str(len(meta))+'H',*meta));write('data/tilesets/secondary/hgss_violet/metatile_attributes.bin',struct.pack('<'+str(len(attrs))+'H',*attrs))
 write('crossroads/hgss/art/violet/manifest.json',json.dumps(dict(specs=spec,allocated_tiles=cursor,available_tiles=len(free),metatiles=len(attrs),reserved_primary=sorted(protected),source='Original GBA asset study from inspected HGSS Violet reference; owner Gym fitted separately'),indent=2)+'\n')
 blocks={k:[] for k in ['graphics','metatiles','headers','externs']}
 for primary in [True,False]:
  kind='primary' if primary else 'secondary';word='Primary' if primary else 'Secondary';symbol='HgssViolet'+word;path=f'data/tilesets/{kind}/hgss_violet'
  blocks['graphics'].append(f'const u32 gTilesetTiles_{symbol}[] = INCGFX_U32("{path}/tiles.png", ".4bpp.fastSmol");\nconst u16 gTilesetPalettes_{symbol}[][16] = {{\n'+''.join(f'    INCGFX_U16("{path}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n')
  blocks['metatiles'].append(f'const u16 gMetatiles_{symbol}[] = INCBIN_U16("{path}/metatiles.bin");\nconst u16 gMetatileAttributes_{symbol}[] = INCBIN_U16("{path}/metatile_attributes.bin");\n');blocks['headers'].append(f'const struct Tileset gTileset_{symbol} = {{\n .isCompressed=TRUE, .isSecondary={"FALSE" if primary else "TRUE"}, .tiles=gTilesetTiles_{symbol},\n .palettes=gTilesetPalettes_{symbol}, .metatiles=gMetatiles_{symbol}, .metatileAttributes=gMetatileAttributes_{symbol}, .callback={"InitTilesetAnim_General" if primary else "NULL"},\n}};\n');blocks['externs'].append(f'extern const struct Tileset gTileset_{symbol};\n')
 # Route32 uses original General pixels/palettes, with only unused metatile1ff
 # repointed to existing concrete tiles. No shared General data is edited.
 blocks['headers'].append('const struct Tileset gTileset_HgssVioletRoutePrimary = {\n .isCompressed=TRUE, .isSecondary=FALSE, .tiles=gTilesetTiles_General, .palettes=gTilesetPalettes_General, .metatiles=gMetatiles_HgssVioletPrimary, .metatileAttributes=gMetatileAttributes_HgssVioletPrimary, .callback=InitTilesetAnim_General,\n};\n');blocks['externs'].append('extern const struct Tileset gTileset_HgssVioletRoutePrimary;\n')
 for key,path in [('graphics','src/data/tilesets/graphics.h'),('metatiles','src/data/tilesets/metatiles.h'),('headers','src/data/tilesets/headers.h'),('externs','include/tilesets.h')]:
  text=(R/path).read_text();start='// BEGIN HGSS VIOLET ORIGINAL ART';end='// END HGSS VIOLET ORIGINAL ART';block=start+'\n#if !IS_FRLG\n'+''.join(blocks[key])+'#endif\n'+end
  if start in text:text=re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda m:block,text,flags=re.S)
  elif key=='externs':i=text.rfind('#endif');text=text[:i]+block+'\n'+text[i:]
  else:text+='\n'+block+'\n'
  write(path,text)
 print('Original Violet architecture:',cursor,'graphics;',len(attrs),'metatiles; no map-completion assertion.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');generate(p.parse_args().check)
