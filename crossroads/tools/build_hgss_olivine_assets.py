#!/usr/bin/env python3
"""Original HGSS-directed Olivine facade conversion, isolated from accepted art.

Three shared facade palettes leave the original Black Ledger buildings and one
owner Gym bank intact. Native trees/water and neighbouring route glyphs retain
their existing graphics. No engine limits or save data are changed.
"""
import argparse,json,struct,hashlib,re
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2];A=R/'crossroads/hgss/art/olivine'
P=R/'data/tilesets/primary/hgss_olivine';S=R/'data/tilesets/secondary/hgss_olivine'
SPECS=[('parasol','parasol',(0,0,1024,1536),(32,48),11,-1),('house','facades',(0,0,670,480),(64,64),8,1),('cafe','facades',(680,0,1377,470),(64,64),9,1),('lighthouse','facades',(0,470,670,1142),(112,144),11,3),('port','port-north-entry',(0,0,1448,1086),(128,96),11,3),('center','services',(0,0,870,887),(96,80),9,2),('mart','services',(870,0,1774,887),(80,64),11,1),('sailboat','harbor-decor',(0,0,1100,724),(96,80),11,-1),('pennant_arch','harbor-decor',(1100,0,2172,724),(112,48),9,-1)]
def words(p):b=p.read_bytes();return list(struct.unpack('<'+str(len(b)//2)+'H',b))
def legacy_ids():
 source=words(R/'data/layouts/SlateportCity/map.bin');ids={0x202,0x32e,0x32f,0x336,0x337}
 for sy,sx,w,h in [(16,4,4,4),(22,2,5,5)]:
  for y in range(sy,sy+h):ids.update(v&1023 for v in source[y*40+sx:y*40+sx+w])
 return ids
def primary_ids():
 ids={0x1ff,0,1,3,4,0x15,0x19,0x24,0x71,0x75,0x76,0x79,0x7c,0x7d,0xa7,0xc6,0x170,0x1d4,0x1d5,0x1dc,0x1dd,0x1e4,0x1e5}
 ls={l['id']:l for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
 for n in ['JohtoRoute39','JohtoRoute40']:
  m=json.loads((R/f'data/maps/{n}/map.json').read_text());ids.update(v&1023 for v in words(R/ls[m['layout']]['blockdata_filepath']) if v&1023<512)
 return ids|{n for n in legacy_ids() if n<512}
def generate(check=False,measure=False):
 def write(p,b):
  if measure:return
  if isinstance(b,str):b=b.encode()
  if p.suffix=='.pal':b=b.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
  if check:assert p.read_bytes()==b,('Regenerate Olivine assets',str(p))
  elif not p.exists() or p.read_bytes()!=b:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 dirs=[R/'data/tilesets/primary/general',R/'data/tilesets/secondary/western_city'];sheets=[Image.open(d/'tiles.png').copy() for d in dirs];metas=[words(d/'metatiles.bin') for d in dirs];attrs=[words(d/'metatile_attributes.bin') for d in dirs]
 for i in range(2):metas[i]+=[0]*(4096-len(metas[i]));attrs[i]+=[0]*(512-len(attrs[i]))
 from hgss_ecruteak_terrain import neutral_metadata,neutral_graphics
 metas[0],attrs[0]=neutral_metadata(metas[0],attrs[0]);sheets[0]=neutral_graphics()
 keep=[primary_ids(),{n for n in legacy_ids() if n>=512}];refs=[v for k in range(2) for n in keep[k] for v in metas[k][n%512*8:n%512*8+8]]
 used={v&1023 for v in refs}|set(range(432,512));free=[i for i in range(1024) if i not in used];fm=[i for i in range(512,1024) if i not in keep[1]];cursor=0;cache={};out={};ims={}
 for n,src,box,size,bank,door in SPECS:
  im=Image.open(A/(src+'-source.png')).convert('RGBA').crop(box);alpha=im.getchannel('A').point(lambda v:255 if v>=200 else 0);im.putalpha(alpha);im=im.crop(alpha.getbbox()).resize(size,Image.Resampling.NEAREST);ims[n]=im
 pals={}
 for bank in [8,9,11]:
  group=[ims[n] for n,src,b,size,k,d in SPECS if k==bank];strip=Image.new('RGB',(sum(im.width for im in group),max(im.height for im in group)));x=0
  for im in group:strip.paste(im,(x,0),im.getchannel('A'));x+=im.width
  pals[bank]=[0,0,0]+strip.quantize(colors=15,method=Image.Quantize.MEDIANCUT).getpalette()[:45]
 # QA10 changes only the port drawing, not the shared maritime color bank.
 # The immutable QA09 palette keeps lighthouse/Mart/boats/parasol pixels exact.
 pals[11]=[int(v) for line in (A/'port-qa09-palette11.pal').read_text().splitlines()[3:] for v in line.split()]
 assert len(pals[11])==48
 def alloc(tile):
  nonlocal cursor
  key=tile.tobytes()
  if key not in cache:
   assert cursor<len(free),('Olivine facade graphics capacity',cursor,len(free));n=free[cursor];cursor+=1;cache[key]=n;i=n%512;sheets[n//512].paste(tile,(i%16*8,i//16*8))
   for flags,im in [(0x400,tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)),(0x800,tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)),(0xc00,tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT).transpose(Image.Transpose.FLIP_TOP_BOTTOM))]:cache.setdefault(im.tobytes(),n|flags)
  return cache[key]
 empty=alloc(Image.new('P',(8,8)))
 # Small, explicit material modules use the free private bank12. They replace
 # the incorrect assumption that every blocked HGSS tile is an earth cliff.
 general_gray=[int(v) for l in (dirs[0]/'palettes/03.pal').read_text().splitlines()[3:] for v in l.split()];gray_ref=Image.new('P',(1,1));gray_ref.putpalette(general_gray+[0]*720)
 material_pal=[0,0,0,232,235,229,189,197,193,141,151,151,96,112,115,58,74,79,204,185,153,158,137,111,112,94,76,76,65,55,246,240,219,212,219,216,71,120,197,58,106,181,32,81,157,102,153,216]
 pals[12]=material_pal;ref=Image.new('P',(1,1));ref.putpalette(material_pal+[0]*720);src=Image.open(A/'city-materials-source.png').convert('RGBA');module={}
 for i,name in enumerate(['fence_h','fence_v','deck','sea_boulder']):
  x,y=i%2,i//2;im=src.crop((x*src.width//2,y*src.height//2,(x+1)*src.width//2,(y+1)*src.height//2));alpha=im.getchannel('A').point(lambda v:255 if v>=200 else 0);im.putalpha(alpha);im=im.crop(alpha.getbbox());size=(4,16) if name=='fence_v' else (16,10) if name=='fence_h' else (16,14) if name=='sea_boulder' else (16,16);im=im.resize(size,Image.Resampling.NEAREST);canvas=Image.new('RGBA',(16,16));canvas.alpha_composite(im,((16-size[0])//2,16-size[1]));q=canvas.convert('RGB').quantize(palette=gray_ref if name.startswith('fence_') else ref,dither=Image.Dither.NONE);v=bytearray(q.tobytes());alpha=canvas.getchannel('A').tobytes()
  for j in range(len(v)):v[j]=0 if alpha[j]<128 else v[j] or 1
  q=Image.frombytes('P',(16,16),bytes(v));q.putpalette(general_gray if name.startswith('fence_') else material_pal);module[name]=q
  if not check and not measure:q.save(A/(name+'-native.png'),bits=4)
 # Shared fence resources occupy previously unused PRIMARY IDs. Their gray
 # palette/glyphs decode identically from Route40 while the city is scrolling.
 corner=module['fence_h'].copy();cv=bytearray(corner.tobytes());vv=module['fence_v'].tobytes()
 for i,v in enumerate(vv):
  if v:cv[i]=v
 corner=Image.frombytes('P',(16,16),bytes(cv));corner.putpalette(general_gray);module['fence_corner']=corner
 shared_names=['fence_h','fence_v','fence_corner'];assert not set(range(0x100,0x103))&keep[0]
 def material(name,ground,top,behavior=0):
  primary=name in shared_names;n=0x100+shared_names.index(name) if primary else fm.pop(0);k=0 if primary else 1;metas[k][n%512*8:n%512*8+8]=ground+top;attrs[k][n%512]=0x1000|behavior;out[name]=dict(width=1,height=1,metatiles=[n],palette=3 if primary else 12);return n
 glyph={}
 for name,q in module.items():glyph[name]=[alloc(q.crop((dx,dy,dx+8,dy+8)))|(0x3000 if name.startswith('fence_') else 0xc000) for dx,dy in [(0,0),(8,0),(0,8),(8,8)]]
 material('deck',glyph['deck'],[empty]*4)
 material('fence_h',metas[0][0x1ff*8:0x1ff*8+4],glyph['fence_h']);material('fence_v',metas[0][0x1ff*8:0x1ff*8+4],glyph['fence_v']);material('fence_corner',metas[0][0x1ff*8:0x1ff*8+4],glyph['fence_corner']);material('sea_boulder',metas[0][0x170*8:0x170*8+4],glyph['sea_boulder'])
 # Opaque blue/white backing permits a boat sail in the foreground over the
 # quay railing without a third graphics layer or a black/grass rectangle.
 water=Image.new('RGB',(16,16));sheet=Image.open(dirs[0]/'tiles.png');wp=[tuple(map(int,l.split())) for l in (dirs[0]/'palettes/04.pal').read_text().splitlines()[3:]]
 for j,v in enumerate(metas[0][0x170*8:0x170*8+4]):
  k=v&1023;q=sheet.crop((k%16*8,k//16*8,k%16*8+8,k//16*8+8));rgb=Image.new('RGB',(8,8));rgb.putdata([wp[i] for i in q.tobytes()]);water.paste(rgb,(j%2*8,j//2*8))
 fg=module['fence_h'].convert('RGBA');fg.putalpha(Image.frombytes('L',(16,16),bytes(255 if v else 0 for v in module['fence_h'].tobytes())));water=water.convert('RGBA');water.alpha_composite(fg);q=water.convert('RGB').quantize(palette=ref,dither=Image.Dither.NONE);quay=[alloc(q.crop((dx,dy,dx+8,dy+8)))|0xc000 for dx,dy in [(0,0),(8,0),(0,8),(8,8)]];material('quay_fence',quay,[empty]*4)
 for name,src,box,size,bank,door in SPECS:
  im=ims[name];ref=Image.new('P',(1,1));ref.putpalette(pals[bank]+[0]*720);q=im.convert('RGB').quantize(palette=ref,dither=Image.Dither.NONE);v=bytearray(q.tobytes());alpha=im.getchannel('A').tobytes()
  for j in range(len(v)):v[j]=0 if alpha[j]<128 else v[j] or 1
  q=Image.frombytes('P',size,bytes(v));q.putpalette(pals[bank]);w,h=size[0]//16,size[1]//16
  # Bilateral upper-roof modules on NEW Olivine art fit the hardware pool.
  # The approved owner Gym and all four accepted Black Ledger buildings are
  # independent protected input and never normalized/recolored.
  mirror_height=112 if name=='lighthouse' else 64 if name=='port' else 0
  if mirror_height:
   left=q.crop((0,0,size[0]//2,mirror_height));q.paste(left.transpose(Image.Transpose.FLIP_LEFT_RIGHT),(size[0]//2,0))
  door_y=1 if name=='port' else h-1
  doors=([] if name in ['parasol','sailboat','pennant_arch'] else [[door,door_y]])+([[door+1,door_y]] if name in ['center','port'] else [])
  canopy=[[door,0],[door+1,0]] if name=='port' else []
  ids=[]
  for y in range(h):
   for x in range(w):
    n=fm.pop(0);ids.append(n);top=[alloc(q.crop((x*16+dx,y*16+dy,x*16+dx+8,y*16+dy+8)))|(bank<<12) for dx,dy in [(0,0),(8,0),(0,8),(8,8)]]
    ground=glyph['deck'] if name=='port' and ([x,y] in canopy or [x,y] in doors) else metas[0][0x170*8:0x170*8+4] if name in ['sailboat','port'] else metas[1][2*8:2*8+4] if name=='pennant_arch' else glyph['deck'] if name=='parasol' else metas[0][8:12]
    metas[1][n%512*8:n%512*8+8]=ground+top
    covered=(y>=h-2) if name=='sailboat' else (y==h-1 and x in [0,w-1]) if name=='pennant_arch' else (y==h-1 if name=='parasol' else y>=h-2)
    # Two north-side public landing cells must draw below Joe, like the
    # threshold; keep all other roof/eave foreground layers unchanged.
    port_eave=name=='port' and (y==0 or (y<h-2 and x in [0,w-1])) and [x,y] not in canopy
    attrs[1][n%512]=(0x1000 if covered or name=='port' and ([x,y] in doors or [x,y] in canopy) else 0)|(0x15 if name=='sailboat' or port_eave else (0x61 if name=='port' else 0x60) if [x,y] in doors else 0)
  out[name]=dict(width=w,height=h,metatiles=ids,door_x=door,door_y=door_y,doors=doors,solid=([[0,h-1],[w-1,h-1]] if name=='pennant_arch' else [[x,y] for y in range(h-2,h) for x in range(w)] if name=='sailboat' else [[x,h-1] for x in range(w)] if name=='parasol' else [[x,y] for y in range(1,h) for x in range(w) if (y>=h-2 or x not in [0,w-1]) and [x,y] not in doors]),palette=bank)
  if name=='port':out[name].update(canopy=canopy,entry_direction='south',approach=[0,-1],design='North-entry visible portal below high canopy; closed south windows, no second false doorway')
  if not check and not measure:q.save(A/(name+'-native.png'),bits=4)
 # The sail extends over both quay paving and sea. Use separate underlays
 # without consuming any new glyphs: water keeps native water behavior/elevation.
 a=out['sailboat'];ids=[]
 for n in a['metatiles']:
  new=fm.pop(0);ids.append(new);row=metas[1][n%512*8:n%512*8+8];metas[1][new%512*8:new%512*8+8]=glyph['deck']+row[4:8];attrs[1][new%512]=attrs[1][n%512]&~255
 out['sailboat_paving']=dict(a,metatiles=ids)
 # Only the row crossing the actual seawall needs its original cliff ground.
 # The DS ship collision footprint below it is water under the native hull.
 shore={}
 for ground in [0x71,0x7c,out['quay_fence']['metatiles'][0]]:
  for cell in range(a['width'],a['width']*2):
   n=a['metatiles'][cell];new=fm.pop(0);shore[f'{ground}:{cell}']=new;row=metas[1][n%512*8:n%512*8+8];metas[1][new%512*8:new%512*8+8]=(metas[0][ground*8:ground*8+4] if ground<512 else metas[1][ground%512*8:ground%512*8+4])+row[4:8];attrs[1][new%512]=0
 out['sailboat']['shore_variants']=shore
 # Reuse exact native tree art, but lift leaves above Joe and keep roots solid.
 for title in ['tree']:
  ids=[]
  for j,n in enumerate([0x1d4,0x1d5,0x1dc,0x1dd]):
   k=fm.pop(0);ids.append(k);row=metas[0][n*8:n*8+8].copy()
   if j<2:
    for a,v in enumerate(row[:4]):
     i=v&1023;im=sheets[0].crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8))
     if v&0x400:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
     if v&0x800:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
     mask=Image.frombytes('P',(8,8),bytes(t if 1<=t<=4 else 0 for t in im.tobytes()));row[4+a]=alloc(mask)|(v&0xf000)
   metas[1][k%512*8:k%512*8+8]=row;attrs[1][k%512]=0 if j<2 else 0x1000
  out[title]=dict(width=2,height=2,metatiles=ids)
 # Relocated port notice stands on timber, not an unrelated grass/stone tile.
 # Preserve every original sign pixel except the edge-connected gray backing
 # between/above its posts. Native palette0/1 foreground overlays opaque deck12.
 # A high unused metatile keeps the owner Gym's old first-free IDs unchanged.
 sign_words=metas[0][3*8:3*8+4];sign=Image.new('P',(16,16))
 for j,v in enumerate(sign_words):
  n=v&1023;tile=sheets[n//512].crop((n%512%16*8,n%512//16*8,n%512%16*8+8,n%512//16*8+8))
  if v&0x400:tile=tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if v&0x800:tile=tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  sign.paste(tile,(j%2*8,j//2*8))
 pixels=bytearray(sign.tobytes());background=set();pending=[(x,y) for y in range(16) for x in range(16) if x in (0,15) or y in (0,15)]
 while pending:
  x,y=pending.pop();i=y*16+x
  if i in background or pixels[i]!=5:continue
  background.add(i)
  pending.extend((X,Y) for X,Y in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] if 0<=X<16 and 0<=Y<16)
 for i in background:pixels[i]=0
 assert len(background)==46,('Unexpected native sign backing',len(background))
 sign=Image.frombytes('P',(16,16),bytes(pixels));top=[]
 for j,v in enumerate(sign_words):top.append(alloc(sign.crop((j%2*8,j//2*8,j%2*8+8,j//2*8+8)))|(v&0xf000))
 n=0x3ef;assert n in fm;fm.remove(n);metas[1][n%512*8:n%512*8+8]=glyph['deck']+top;attrs[1][n%512]=0x1000
 out['port_sign']=dict(width=1,height=1,metatiles=[n],palette=12,overlay_palettes=[0,1],native_sign_backing_pixels_removed=len(background),source='Unchanged native General sign foreground over timber deck; north apron22,50')
 for k,d in enumerate([P,S]):
  d.mkdir(parents=True,exist_ok=True)
  if check:assert Image.open(d/'tiles.png').tobytes()==sheets[k].tobytes()
  elif not measure:sheets[k].save(d/'tiles.png',bits=4)
  write(d/'metatiles.bin',struct.pack('<4096H',*metas[k]));write(d/'metatile_attributes.bin',struct.pack('<512H',*attrs[k]))
  for pal in range(16):
   b=(dirs[k]/f'palettes/{pal:02}.pal').read_bytes()
   if k==1 and pal in pals:b='JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,pals[pal][j:j+3])) for j in range(0,48,3))+'\n'
   write(d/f'palettes/{pal:02}.pal',b)
 # Only3 new fence metatiles/glyphs are shared; every other native route
 # graphic/meta/attribute remains the existing neutral General resource.
 coast_sheet=neutral_graphics();coast_metas,coast_attrs=neutral_metadata(words(dirs[0]/'metatiles.bin'),words(dirs[0]/'metatile_attributes.bin'));shared_refs=set()
 for n in range(0x100,0x103):
  row=metas[0][n*8:n*8+8];coast_metas[n*8:n*8+8]=row;coast_attrs[n]=attrs[0][n];shared_refs.update(v&1023 for v in row)
 assert max(shared_refs)<432,'Coast fence glyphs must stay primary, outside animation slots'
 for n in shared_refs:
  box=(n%16*8,n//16*8,n%16*8+8,n//16*8+8);coast_sheet.paste(sheets[0].crop(box),box[:2])
 coast=R/'data/tilesets/primary/hgss_olivine_coast_buffer';coast.mkdir(parents=True,exist_ok=True)
 if check:assert Image.open(coast/'tiles.png').tobytes()==coast_sheet.tobytes()
 elif not measure:coast_sheet.save(coast/'tiles.png',bits=4)
 write(coast/'metatiles.bin',struct.pack('<4096H',*coast_metas));write(coast/'metatile_attributes.bin',struct.pack('<512H',*coast_attrs))
 manifest=dict(specs=out,protected_primary_ids=sorted(keep[0]),protected_secondary_ids=sorted(keep[1]),facade_graphics=cursor,remaining_graphics=len(free)-cursor,provenance='Original generated HGSS-directed facades; no HGSS textures imported',source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(A.glob('*-source.png'))})
 write(A/'manifest.json',json.dumps(manifest,indent=2)+'\n')
 blocks={key:[] for key in ['graphics','metatiles','headers','externs']}
 for primary,path,sym in [(True,P,'HgssOlivinePrimary'),(False,S,'HgssOlivineSecondary')]:
  rel=path.relative_to(R).as_posix();blocks['graphics'].append(f'const u32 gTilesetTiles_{sym}[] = INCGFX_U32("{rel}/tiles.png", ".4bpp.fastSmol");\nconst u16 gTilesetPalettes_{sym}[][16] = {{\n'+''.join(f' INCGFX_U16("{rel}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n');blocks['metatiles'].append(f'const u16 gMetatiles_{sym}[] = INCBIN_U16("{rel}/metatiles.bin");\nconst u16 gMetatileAttributes_{sym}[] = INCBIN_U16("{rel}/metatile_attributes.bin");\n');blocks['externs'].append(f'extern const struct Tileset gTileset_{sym};\n');blocks['headers'].append(f'const struct Tileset gTileset_{sym} = {{ .isCompressed=TRUE, .isSecondary={"FALSE" if primary else "TRUE"}, .tiles=gTilesetTiles_{sym}, .palettes=gTilesetPalettes_{sym}, .metatiles=gMetatiles_{sym}, .metatileAttributes=gMetatileAttributes_{sym}, .callback={"InitTilesetAnim_General" if primary else "NULL"} }};\n')
 rel='data/tilesets/primary/hgss_olivine_coast_buffer';sym='HgssOlivineCoastBuffer'
 blocks['graphics'].append(f'const u32 gTilesetTiles_{sym}[] = INCGFX_U32("{rel}/tiles.png", ".4bpp.fastSmol");\n');blocks['metatiles'].append(f'const u16 gMetatiles_{sym}[] = INCBIN_U16("{rel}/metatiles.bin");\nconst u16 gMetatileAttributes_{sym}[] = INCBIN_U16("{rel}/metatile_attributes.bin");\n');blocks['externs'].append(f'extern const struct Tileset gTileset_{sym};\n');blocks['headers'].append(f'const struct Tileset gTileset_{sym} = {{.isCompressed=TRUE,.isSecondary=FALSE,.tiles=gTilesetTiles_{sym},.palettes=gTilesetPalettes_General,.metatiles=gMetatiles_{sym},.metatileAttributes=gMetatileAttributes_{sym},.callback=InitTilesetAnim_General}};\n')
 for key,path in [('graphics','src/data/tilesets/graphics.h'),('metatiles','src/data/tilesets/metatiles.h'),('headers','src/data/tilesets/headers.h'),('externs','include/tilesets.h')]:
  p=R/path;s=p.read_text();start='// BEGIN HGSS OLIVINE EXTERIORS';end='// END HGSS OLIVINE EXTERIORS';block=start+'\n#if !IS_FRLG\n'+''.join(blocks[key])+'#endif\n'+end
  if start in s:s=re.sub(re.escape(start)+'.*?'+re.escape(end),lambda m:block,s,flags=re.S)
  elif key=='externs':i=s.rfind('#endif');s=s[:i]+block+'\n'+s[i:]
  else:s+='\n'+block+'\n'
  write(p,s)
 print('Olivine original facade conversion',cursor,'graphics; free',len(free)-cursor,'before owner Gym; native art review required')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--measure',action='store_true');a=p.parse_args();generate(a.check,a.measure)
