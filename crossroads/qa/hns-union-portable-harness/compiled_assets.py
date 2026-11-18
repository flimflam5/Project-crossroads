import hashlib,json,struct,subprocess,sys
from pathlib import Path
R=Path.cwd();expected=sys.argv[1];rom=(R/'pokeemerald.gba').read_bytes();assert hashlib.sha256(rom).hexdigest()==expected
syms={}
for line in subprocess.check_output(['arm-none-eabi-nm','-an',str(R/'pokeemerald.elf')],text=True).splitlines():
 f=line.split()
 if len(f)==3:
  try:syms[f[2]]=int(f[0],16)
  except ValueError:pass
sets=[('HgssUnionCave','primary/hgss_union_cave'),('HgssRuinsPocket','primary/hgssruinspocket'),('HgssRuinsChamber','primary/hgssruinschamber'),('HgssRuinsHall','primary/hgssruinshall'),('HgssRuinsPublic','secondary/hgss_ruins_public')]
result={}
for key,folder in sets:
 p=R/'data/tilesets'/folder
 for stem,sym in [('metatiles.bin','gMetatiles_'),('metatile_attributes.bin','gMetatileAttributes_')]:
  b=(p/stem).read_bytes();o=syms[sym+key]-0x08000000;assert rom[o:o+len(b)]==b,('compiled bytes mismatch',key,stem,o,len(b))
 for bank in range(16):
  lines=(p/f'palettes/{bank:02}.pal').read_text().splitlines();assert lines[:3]==['JASC-PAL','0100','16'];rgb=[tuple(map(int,line.split())) for line in lines[3:19]];b=struct.pack('<16H',*((r>>3)|((g>>3)<<5)|((bl>>3)<<10) for r,g,bl in rgb));o=syms['gTilesetPalettes_'+key]-0x08000000+32*bank;assert rom[o:o+32]==b,('compiled palette mismatch',key,bank)
 result[key]={'metatile_bytes':(p/'metatiles.bin').stat().st_size,'attribute_bytes':(p/'metatile_attributes.bin').stat().st_size,'compiled_palette_banks':16}
 print(key,'full compiled metatiles, attrs and palette PASS',flush=True)
Path(sys.argv[2]).write_text(json.dumps(dict(rom_sha256=expected,tilesets=result,result='PASS'),indent=2)+'\n')
