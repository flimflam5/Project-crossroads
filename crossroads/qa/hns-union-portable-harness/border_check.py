import os,ctypes as C,hashlib,json,struct,subprocess,sys
from pathlib import Path
from PIL import Image
R=Path.cwd();sha,mapname,snap=sys.argv[1:];assert Path(snap).with_suffix('.sha256').read_text().strip()==sha,('snapshot ROM identity mismatch',snap);rom=(R/'pokeemerald.gba').read_bytes();assert hashlib.sha256(rom).hexdigest()==sha
syms={}
for line in subprocess.check_output(['arm-none-eabi-nm','-an',str(R/'pokeemerald.elf')],text=True).splitlines():
 f=line.split()
 if len(f)==3:
  try:syms[f[2]]=int(f[0],16)
  except ValueError:pass
lib=C.CDLL(os.environ.get('MGBA_BRIDGE','/tmp/johto-bridge.so'))
for f,t in [('emu_init',[C.c_char_p]),('emu_state',[C.c_char_p,C.c_int]),('emu_read',[C.c_uint,C.c_int]),('emu_image',[C.c_char_p])]:getattr(lib,f).argtypes=t
lib.emu_read.restype=C.c_uint;read=lambda x,n=4:lib.emu_read(syms.get(x,x),n)
assert lib.emu_init(str(R/'pokeemerald.gba').encode()) and lib.emu_state(str(Path(snap)).encode(),1)
groups=json.load(open(R/'data/maps/map_groups.json'));sb=read('gSaveBlock1Ptr');assert (read(sb+4,1),read(sb+5,1))==(75,groups['gMapGroup_CrossroadsOlivine'].index(mapname))
m=json.load(open(R/'data/maps'/mapname/'map.json'));layout=next(x for x in json.load(open(R/'data/layouts/layouts.json'))['layouts'] if x['id']==m['layout']);border=(R/layout['border_filepath']).read_bytes();symbol=layout['name']+'_Border';offset=syms[symbol]-0x08000000;assert rom[offset:offset+len(border)]==border,('border source and ROM mismatch',symbol)
ids=[v&1023 for v in struct.unpack('<'+str(len(border)//2)+'H',border)];primary=R/'data/tilesets/primary/hgss_union_cave';secmeta=R/'data/tilesets/secondary/western_interiors';sectiles=R/'data/tilesets/secondary/generic_building';sets=[(primary,'HgssUnionCave'),(secmeta,'WesternInteriors')];graphic=set();banks=set()
for id in ids:
 p,key=sets[id>=512];idx=id%512
 for fn,sym,width in [('metatiles.bin','gMetatiles_',16),('metatile_attributes.bin','gMetatileAttributes_',2)]:
  data=(p/fn).read_bytes();offset=syms[sym+key]-0x08000000+idx*width;assert data[idx*width:(idx+1)*width]==rom[offset:offset+width],('border meta/attrs mismatch',id,fn)
 for t in struct.unpack_from('<8H',(p/'metatiles.bin').read_bytes(),idx*16):graphic.add(t&1023);banks.add(t>>12)
for tile in graphic:
 p=primary if tile<512 else sectiles;idx=tile if tile<512 else tile-512;sheet=Image.open(p/'tiles.png');pix=sheet.crop((idx%16*8,idx//16*8,(idx%16+1)*8,(idx//16+1)*8)).tobytes();exp=bytes(pix[i]|pix[i+1]<<4 for i in range(0,64,2));actual=bytes(read(0x06000000+tile*32+i,1) for i in range(32));assert exp==actual,('border graphic VRAM mismatch',tile)
for bank in banks:
 p=primary if bank<6 else sectiles;lines=(p/f'palettes/{bank:02}.pal').read_text().splitlines();rgb=[tuple(map(int,line.split())) for line in lines[3:19]];exp=[(r>>3)|((g>>3)<<5)|((b>>3)<<10) for r,g,b in rgb];actual=[read(syms['gPlttBufferUnfaded']+bank*32+i*2,2) for i in range(16)];assert actual[1:]==exp[1:],('border palette mismatch',bank)
print(json.dumps(dict(map=mapname,rom_sha256=sha,border_ids=ids,graphic_ids=sorted(graphic),banks=sorted(banks),source_rom_vram='PASS',note='Asset equality only; camera must still be visually inspected.'),indent=2))
