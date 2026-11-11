"""Share only gate primary graphics; preserve original route/farm resources."""
import json,re,struct
from pathlib import Path
from hgss_ecruteak_terrain import neutral_metadata,neutral_graphics
R=Path(__file__).resolve().parents[2]
NEIGHBORS={'JohtoRoute37','JohtoRoute38','JohtoRoute42'}
GATE_PRIMARY=0x100
RESERVED_SECONDARY=set()
def protection():return json.loads((R/'crossroads/hgss/contracts/ecruteak-route-buffers-qa08.json').read_text())
def route_primary_ids():return set(protection()['primary_ids'])|set(range(GATE_PRIMARY,GATE_PRIMARY+49))
def route_primary_graphics():return set(protection()['primary_graphics'])
def relocate_layout(n,l):
 if n in NEIGHBORS:l.update(primary_tileset='gTileset_HgssEcruteakGateBuffer',secondary_tileset='gTileset_WesternCity')
 return l
def gate_cell(spec,x,y):return spec['start']+y*spec['width']+x+(0x3000 if 1<=y<=3 else 0x400)
def stamp_gate(tiles,w,h,origin,spec,source_x=0):
 ox,oy=origin
 for y in range(spec['height']):
  for x in range(source_x,spec['width']):
   X,Y=ox+x-source_x,oy+y
   if 0<=X<w and 0<=Y<h:tiles[Y*w+X]=gate_cell(spec,x,y)
def route_data(n,data,w,h):
 if n not in NEIGHBORS:return data
 t=list(struct.unpack('<'+str(w*h)+'H',data))
 # Remove the unshipped full-family candidate's alias; keep original road pixels.
 for i,v in enumerate(t):
  if v&1023==0x3ea:t[i]=(v&~1023)|0x202
 if n=='JohtoRoute42':
  a=json.loads((R/'crossroads/hgss/art/native-manifest.json').read_text())['specs']['gate'];stamp_gate(t,w,h,(0,12),a,source_x=4)
 return struct.pack('<'+str(w*h)+'H',*t)
def generate(check=False):
 from PIL import Image
 def write(path,b):
  if isinstance(b,str):b=b.encode()
  p=R/path
  if check:assert p.read_bytes()==b,('Regenerate gate buffer',path)
  elif not p.exists() or p.read_bytes()!=b:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 def words(b):return struct.unpack('<'+str(len(b)//2)+'H',b)
 base=R/'data/tilesets/primary/general';source=R/'data/tilesets/primary/hgss_ecruteak';gm,ga=neutral_metadata(words((base/'metatiles.bin').read_bytes()),words((base/'metatile_attributes.bin').read_bytes()));ms=words((source/'metatiles.bin').read_bytes());at=words((source/'metatile_attributes.bin').read_bytes());start=GATE_PRIMARY;end=start+49
 assert not set(range(start,end))&set(protection()['primary_ids'])
 gm[start*8:end*8]=ms[start*8:end*8];ga[start:end]=at[start:end]
 refs={v&1023 for v in gm[start*8:end*8]};assert max(refs)<432,'Gate graphics must be primary and outside animation slots'
 sheet=neutral_graphics();original=sheet.copy();src=Image.open(source/'tiles.png')
 for n in refs:
  box=(n%16*8,n//16*8,n%16*8+8,n//16*8+8)
  if n in route_primary_graphics():assert original.crop(box).tobytes()==src.crop(box).tobytes(),('Gate overwrites neighboring native graphics',n)
  sheet.paste(src.crop(box),box[:2])
 root='data/tilesets/primary/hgss_ecruteak_gate_buffer'
 if check:assert Image.open(R/root/'tiles.png').tobytes()==sheet.tobytes()
 else:(R/root).mkdir(parents=True,exist_ok=True);sheet.save(R/root/'tiles.png',bits=4)
 write(root+'/metatiles.bin',struct.pack('<4096H',*gm));write(root+'/metatile_attributes.bin',struct.pack('<512H',*ga))
 begin='// BEGIN ECRUTEAK GATE BUFFER';finish='// END ECRUTEAK GATE BUFFER'
 blocks={
 'src/data/tilesets/graphics.h':f'const u32 gTilesetTiles_HgssEcruteakGateBuffer[] = INCGFX_U32("{root}/tiles.png", ".4bpp.fastSmol");\n',
 'src/data/tilesets/metatiles.h':f'const u16 gMetatiles_HgssEcruteakGateBuffer[] = INCBIN_U16("{root}/metatiles.bin");\nconst u16 gMetatileAttributes_HgssEcruteakGateBuffer[] = INCBIN_U16("{root}/metatile_attributes.bin");\n',
 'src/data/tilesets/headers.h':'const struct Tileset gTileset_HgssEcruteakGateBuffer = {\n .isCompressed=TRUE,.isSecondary=FALSE,.tiles=gTilesetTiles_HgssEcruteakGateBuffer,\n .palettes=gTilesetPalettes_General,.metatiles=gMetatiles_HgssEcruteakGateBuffer,\n .metatileAttributes=gMetatileAttributes_HgssEcruteakGateBuffer,.callback=InitTilesetAnim_General,\n};\n',
 'include/tilesets.h':'extern const struct Tileset gTileset_HgssEcruteakGateBuffer;\n'}
 for path,body in blocks.items():
  text=(R/path).read_text();block=begin+'\n#if !IS_FRLG\n'+body+'#endif\n'+finish
  if begin in text:text=re.sub(re.escape(begin)+r'.*?'+re.escape(finish),lambda _:block,text,flags=re.S)
  elif path=='include/tilesets.h':i=text.rfind('#endif');text=text[:i]+block+'\n'+text[i:]
  else:text+='\n'+block+'\n'
  write(path,text)
 print('Gate-only primary buffer:',len(refs),'graphics; original road/farm secondary resources retained')
