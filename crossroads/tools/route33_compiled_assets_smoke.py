#!/usr/bin/env python3
"""Check real candidate Route33 metatiles, palette ROM data and live BG VRAM.

Cold Continue a copy of a genuine QA10 battery. Compare every used primary and
secondary metatile + attribute in the linked ROM to source. Compare each used
secondary graphic to live VRAM; the shared seam's tile 514 and its source
Azalea representation must match. Palette ROM checks cover all 16 secondary
banks, runtime unfaded colors for loaded banks 7/8. This is not visual QA.
"""
import argparse,ctypes as C,hashlib,json,struct,subprocess
from pathlib import Path
from PIL import Image
R=Path.cwd();p=argparse.ArgumentParser();p.add_argument('--save',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--rom-sha256',required=True);p.add_argument('--library',type=Path,default=Path('/tmp/johto-bridge.so'));a=p.parse_args()
sha=lambda b:hashlib.sha256(b).hexdigest();rom=(R/'pokeemerald.gba').read_bytes();assert sha(rom)==a.rom_sha256;before=sha(a.save.read_bytes())
syms={}
for line in subprocess.check_output(['arm-none-eabi-nm','-an',str(R/'pokeemerald.elf')],text=True).splitlines():
 f=line.split()
 if len(f)==3:
  try:syms[f[2]]=int(f[0],16)
  except ValueError:pass
lib=C.CDLL(str(a.library.resolve()))
for fn,types in [('emu_init',[C.c_char_p]),('emu_save',[C.c_char_p,C.c_int]),('emu_frames',[C.c_int,C.c_int]),('emu_read',[C.c_uint,C.c_int])]:getattr(lib,fn).argtypes=types
lib.emu_read.restype=C.c_uint
read=lambda x,n=4:lib.emu_read(syms.get(x,x),n)
def frames(n,k=0):lib.emu_frames(k,n)
assert lib.emu_init(str(R/'pokeemerald.gba').encode()) and lib.emu_save(str(a.save.resolve()).encode(),1)
frames(4500);assert read(syms['gMain']+4)==syms['CB2_BlackLedgerTitle']|1
frames(1,8);frames(200);frames(1,1);frames(300);assert read(syms['gMain']+4)==syms['CB2_Overworld']|1
sb=read('gSaveBlock1Ptr');groups=json.loads((R/'data/maps/map_groups.json').read_text());assert (read(sb+4,1),read(sb+5,1))==(75,groups['gMapGroup_CrossroadsOlivine'].index('JohtoRoute33'))
layouts=json.loads((R/'data/layouts/layouts.json').read_text())['layouts'];layout=next(l for l in layouts if l['id']=='LAYOUT_JOHTO_ROUTE33');raw=(R/layout['blockdata_filepath']).read_bytes();values=struct.unpack('<'+str(len(raw)//2)+'H',raw);used=sorted({v&1023 for v in values})
primary=R/'data/tilesets/primary/bl_gym_azalea';secondary=R/'data/tilesets/secondary/hns_route33';azalea=R/'data/tilesets/secondary/bl_gym_azalea'
tiles=set()
for id in used:
 idx=id%512; source=primary if id<512 else secondary
 metas=(source/'metatiles.bin').read_bytes();attributes=(source/'metatile_attributes.bin').read_bytes()
 for symbol,rawdata,width in [(('gMetatiles_BlGymAzaleaPrimary' if id<512 else 'gMetatiles_HnsRoute33'),metas,16),(('gMetatileAttributes_BlGymAzaleaPrimary' if id<512 else 'gMetatileAttributes_HnsRoute33'),attributes,2)]:
  offset=syms[symbol]-0x08000000+idx*width
  assert rom[offset:offset+width]==rawdata[idx*width:(idx+1)*width],('Compiled metatile/attribute mismatch',id,symbol)
 for tile in struct.unpack_from('<8H',metas,idx*16):
  if (tile&1023)>=512:tiles.add(tile&1023)
assert 514 in used and 582 in tiles,('Expected actual shared seam tile missing',514,582)
# Shared boundary representation must be identical in both compiled secondary
# metatile and attribute arrays, not merely visually similar in source files.
for names,width in [(('gMetatiles_HnsRoute33','gMetatiles_BlGymAzaleaSecondary'),16),(('gMetatileAttributes_HnsRoute33','gMetatileAttributes_BlGymAzaleaSecondary'),2)]:
 records=[]
 for symbol in names:
  offset=syms[symbol]-0x08000000+(514-512)*width;records.append(rom[offset:offset+width])
 assert records[0]==records[1],('Compiled seam mismatch',names)
sheet=Image.open(secondary/'tiles.png');assert sheet.mode=='P'
for tile in sorted(tiles):
 idx=tile-512;pix=sheet.crop((idx%16*8,idx//16*8,(idx%16+1)*8,(idx//16+1)*8)).tobytes();assert len(pix)==64 and max(pix)<16
 expected=bytes(pix[i]|pix[i+1]<<4 for i in range(0,64,2));actual=bytes(read(0x06000000+tile*32+i,1) for i in range(32))
 assert actual==expected,('Loaded Route33 graphic differs from source',tile)
for bank in range(16):
 lines=(secondary/f'palettes/{bank:02}.pal').read_text().splitlines();assert lines[:3]==['JASC-PAL','0100','16'];rgb=[tuple(map(int,line.split())) for line in lines[3:19]]
 expected=[(r>>3)|((g>>3)<<5)|((b>>3)<<10) for r,g,b in rgb];compiled=[read(syms['gTilesetPalettes_HnsRoute33']+bank*32+i*2,2)for i in range(16)]
 assert compiled==expected,('Compiled palette stale',bank,compiled,expected)
 if bank in (7,8):
  loaded=[read(syms['gPlttBufferUnfaded']+bank*32+i*2,2)for i in range(16)]
  assert loaded[1:]==expected[1:],('Loaded route palette differs',bank,loaded,expected)
# Emerald loads bank 6 from the secondary tileset. The two linked map
# secondaries must carry identical bank 6, and the live route bank must match.
expected=[read(syms['gTilesetPalettes_HnsRoute33']+6*32+i*2,2)for i in range(16)]
azalea_palette=[read(syms['gTilesetPalettes_BlGymAzaleaSecondary']+6*32+i*2,2)for i in range(16)]
loaded=[read(syms['gPlttBufferUnfaded']+6*32+i*2,2)for i in range(16)]
assert azalea_palette==expected,('Compiled shared secondary palette differs',azalea_palette,expected)
assert loaded[1:]==expected[1:],('Runtime seam secondary palette differs',loaded,expected)
assert sha(a.save.read_bytes())==before
result=dict(rom_sha256=a.rom_sha256,metatile_ids=len(used),live_secondary_graphics=len(tiles),compiled_palette_banks=16,live_palette_banks=[7,8],shared_seam_metatile=514,shared_seam_vram_graphic=582,shared_seam_secondary_palette_bank=6,result='PASS',limitations='Real source/ROM/VRAM equality, not visual acceptance; primary animation tiles excluded from static VRAM comparisons.')
a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n');print('Route33 compiled metatile/seam, live secondary VRAM and 7/8 palettes PASS',result,flush=True)
