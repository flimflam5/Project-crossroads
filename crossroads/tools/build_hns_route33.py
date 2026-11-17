#!/usr/bin/env python3
"""Prototype H&S Route 33 conversion with a preserved Azalea seam.

Preserve QA10 size, cave events and the existing seven-column town buffer.
The donor interior is selective and requires emulator/save/visual QA.
"""
from pathlib import Path
import hashlib,io,struct
from PIL import Image
from tileset_registration import upsert

R=Path(__file__).resolve().parents[2]
D=R/'crossroads/donor/hns-route33/data/layouts/Route33_hns/map.bin'
B=D.parent/'black-ledger-baseline.bin'
H=R/'crossroads/donor/hns_azalea_exterior/data/tilesets/primary/johto_south_hns'
C=R/'data/tilesets/secondary/bl_gym_azalea'
OUT='data/tilesets/secondary/hns_route33'
EXPECTED='8db5583d404249adf60d2271a790412af0692cae041a682127b733787ca4630a'

def read16(p):
 b=p.read_bytes();return list(struct.unpack('<%dH'%(len(b)//2),b))
def pack(a):return struct.pack('<%dH'%len(a),*a)
def source():
 assert hashlib.sha256(D.read_bytes()).hexdigest()==EXPECTED
 donor=read16(D);assert len(donor)==44*40
 return [donor[(y+10)*44+x+3] for y in range(24) for x in range(32)]
def generate(write):
 cells=source();assert hashlib.sha256(B.read_bytes()).hexdigest()=='60e8ccacebe713c060fde8bd652d275cdbfae8676bd3847f0700118a2bf97f26'
 old=read16(B);assert len(old)==768
 assert {old[y*32+x]&1023 for y in range(24) for x in range(7)}=={1,198,514}
 meta=read16(H/'metatiles.bin');attrs=read16(H/'metatile_attributes.bin')
 used=sorted({v&1023 for v in cells});assert len(used)==55 and max(used)<640
 refs=[v for i in used for v in meta[i*8:i*8+8]]
 ids=sorted({v&1023 for v in refs});banks=sorted({v>>12 for v in refs});assert len(ids)==107 and banks==[0,1] and ids[0]==0
 # Route secondary retains Azalea's shared boundary tile ID 514 and tile 582.
 # Neither donor palette bank may use boundary bank 6.
 reserved_metatile=514; reserved_graphic=582
 free_meta=[i for i in range(512,1024) if i!=reserved_metatile]
 free_gfx=[i for i in range(512,1024) if i!=reserved_graphic]
 metamap={v:free_meta[i] for i,v in enumerate(used)}
 tilemap={0:0};tilemap.update({v:free_gfx[i] for i,v in enumerate(ids[1:])})
 donor=Image.open(H/'tiles.png');im=Image.open(C/'tiles.png').copy();assert donor.mode==im.mode=='P' and im.size==(128,256)
 for oldid,newid in tilemap.items():
  if oldid==0:continue
  tile=donor.crop(((oldid%16)*8,(oldid//16)*8,(oldid%16)*8+8,(oldid//16)*8+8))
  j=newid-512;im.paste(tile,((j%16)*8,(j//16)*8))
 b=io.BytesIO();im.save(b,format='PNG',optimize=False);write(OUT+'/tiles.png',b.getvalue())
 for i in range(16):
  f=(H/f'palettes/{i-7:02}.pal') if i in (7,8) else C/f'palettes/{i:02}.pal'
  write(OUT+f'/palettes/{i:02}.pal',f.read_bytes())
 newmeta=read16(C/'metatiles.bin');newattrs=read16(C/'metatile_attributes.bin')
 assert len(newmeta)==512*8 and len(newattrs)==512
 for oldid,newid in metamap.items():
  newmeta[(newid-512)*8:(newid-511)*8]=[tilemap[v&1023]|(v&0xc00)|((7+(v>>12))<<12) for v in meta[oldid*8:oldid*8+8]]
  # The donor's Headbutt-tree behavior is not present in this engine.
  newattrs[newid-512]=(attrs[oldid]&~255) if attrs[oldid]&255==0xf0 else attrs[oldid]
 write(OUT+'/metatiles.bin',pack(newmeta));write(OUT+'/metatile_attributes.bin',pack(newattrs))
 symbol='HnsRoute33';mark='HNS ROUTE33 PRIVATE SECONDARY'
 sections={'graphics': f'const u32 gTilesetTiles_{symbol}[] = INCGFX_U32("{OUT}/tiles.png", ".4bpp.fastSmol");\nconst u16 gTilesetPalettes_{symbol}[][16] = {{\n'+''.join(f' INCGFX_U16("{OUT}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n',
 'metatiles':f'const u16 gMetatiles_{symbol}[] = INCBIN_U16("{OUT}/metatiles.bin");\nconst u16 gMetatileAttributes_{symbol}[] = INCBIN_U16("{OUT}/metatile_attributes.bin");\n',
 'headers':f'const struct Tileset gTileset_{symbol} = {{ .isCompressed=TRUE, .isSecondary=TRUE, .tiles=gTilesetTiles_{symbol}, .palettes=gTilesetPalettes_{symbol}, .metatiles=gMetatiles_{symbol}, .metatileAttributes=gMetatileAttributes_{symbol}, .callback=NULL }};\n',
 'externs':f'extern const struct Tileset gTileset_{symbol};\n'}
 for kind,path in [('graphics','src/data/tilesets/graphics.h'),('metatiles','src/data/tilesets/metatiles.h'),('headers','src/data/tilesets/headers.h'),('externs','include/tilesets.h')]:
  start='// BEGIN '+mark;end='// END '+mark;body=start+'\n#if !IS_FRLG\n'+sections[kind]+'#endif\n'+end
  write(path,upsert((R/path).read_text(),start,end,body,externs=kind=='externs'))
 out=[(v&0xfc00)|metamap[v&1023] for v in cells]
 # All donor elevation-zero tree canopies are impassable in this engine.
 for i,v in enumerate(out):
  if v>>12==0 and not v&0xc00:out[i]=v|0x400
 # The town-side seven-column graphics/physics remain exactly QA10 source.
 for y in range(24):
  for x in range(7):out[y*32+x]=old[y*32+x]
 # Existing sign locations and cave warp index remain unchanged.
 for x,y in [(13,15),(23,8)]:out[y*32+x]=0x3403
 assert cells[7*32+24]&1023==169 and attrs[169]&255==0x60
 return out
