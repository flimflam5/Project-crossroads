import os,ctypes as C,hashlib,json,struct,subprocess,sys
from pathlib import Path
from PIL import Image
R=Path.cwd();rom_sha=sys.argv[1];mapname=sys.argv[2];snapshot=Path(sys.argv[3]);assert snapshot.with_suffix('.sha256').read_text().strip()==rom_sha,('snapshot ROM identity mismatch',snapshot);rom=(R/'pokeemerald.gba').read_bytes();assert hashlib.sha256(rom).hexdigest()==rom_sha
syms={}
for line in subprocess.check_output(['arm-none-eabi-nm','-an',str(R/'pokeemerald.elf')],text=True).splitlines():
 f=line.split()
 if len(f)==3:
  try:syms[f[2]]=int(f[0],16)
  except ValueError:pass
lib=C.CDLL(os.environ.get('MGBA_BRIDGE','/tmp/johto-bridge.so'))
for fn,types in [('emu_init',[C.c_char_p]),('emu_state',[C.c_char_p,C.c_int]),('emu_read',[C.c_uint,C.c_int])]:getattr(lib,fn).argtypes=types
lib.emu_read.restype=C.c_uint
read=lambda x,n=4:lib.emu_read(syms.get(x,x),n)
assert lib.emu_init(str(R/'pokeemerald.gba').encode()) and lib.emu_state(str(snapshot).encode(),1)
groups=json.load(open(R/'data/maps/map_groups.json'));names=groups['gMapGroup_CrossroadsOlivine'];other=groups['gMapGroup_CrossroadsJohtoExpansion'];expect=(75,names.index(mapname)) if mapname in names else (76,other.index(mapname));sb=read('gSaveBlock1Ptr');assert (read(sb+4,1),read(sb+5,1))==expect
m=json.load(open(R/'data/maps'/mapname/'map.json'));layouts=json.load(open(R/'data/layouts/layouts.json'))['layouts'];layout=next(x for x in layouts if x['id']==m['layout']);cfg={
'UnionCave_1F':('HgssUnionCave','primary/hgss_union_cave',False),
'RuinsOfAlph':('HgssRuinsPublic','secondary/hgss_ruins_public',True),
'RuinsOfAlph_NorthwestPocket':('HgssRuinsPocket','primary/hgssruinspocket',False),
'RuinsOfAlph_NorthwestChamber':('HgssRuinsChamber','primary/hgssruinschamber',False),
'RuinsOfAlph_HallEntrance':('HgssRuinsHall','primary/hgssruinshall',False)}
key,folder,secondary=cfg[mapname];p=R/'data/tilesets'/folder;raw=(R/layout['blockdata_filepath']).read_bytes();vals=struct.unpack('<'+str(len(raw)//2)+'H',raw);ids={v&1023 for v in vals if bool((v&1023)>=512)==secondary};meta=(p/'metatiles.bin').read_bytes();tiles=set();banks=set()
for id in ids:
 for t in struct.unpack_from('<8H',meta,(id%512)*16):
  if bool((t&1023)>=512)==secondary:tiles.add(t&1023)
  if bool((t>>12)>=6)==secondary:banks.add(t>>12)
sheet=Image.open(p/'tiles.png');assert sheet.mode=='P';errors=[]
for tile in sorted(tiles):
 idx=tile-(512 if secondary else 0);pix=sheet.crop((idx%16*8,idx//16*8,(idx%16+1)*8,(idx//16+1)*8)).tobytes();assert len(pix)==64 and max(pix)<16
 exp=bytes(pix[i]|pix[i+1]<<4 for i in range(0,64,2));actual=bytes(read(0x06000000+tile*32+i,1) for i in range(32))
 if exp!=actual:errors.append(tile)
palerrors=[]
for bank in sorted(banks):
 lines=(p/f'palettes/{bank:02}.pal').read_text().splitlines();rgb=[tuple(map(int,line.split())) for line in lines[3:19]];exp=[(r>>3)|((g>>3)<<5)|((b>>3)<<10) for r,g,b in rgb];actual=[read(syms['gPlttBufferUnfaded']+bank*32+i*2,2)for i in range(16)]
 if actual[1:]!=exp[1:]:palerrors.append(bank)
print(json.dumps(dict(map=mapname,tileset=key,metatiles=len(ids),tiles=len(tiles),bad_tiles=errors,banks=sorted(banks),bad_banks=palerrors),indent=2),flush=True);assert not errors and not palerrors,('Live graphics/palette mismatch',errors,palerrors)
