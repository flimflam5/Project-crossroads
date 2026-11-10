#!/usr/bin/env python3
"""Register standalone Gym secondary tilesets. Does not edit any map or save IDs."""
import argparse,json,shutil,struct
from pathlib import Path
P=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('repo',type=Path);ap.add_argument('--apply',action='store_true');a=ap.parse_args();r=a.repo.resolve()
for f in ['include/fieldmap.h','src/data/tilesets/graphics.h','src/data/tilesets/metatiles.h','src/data/tilesets/headers.h','include/tilesets.h']:
 if not (r/f).is_file():raise SystemExit('Not supported project: missing '+f)
s=(r/'include/fieldmap.h').read_text()
for line in ['#define NUM_TILES_IN_PRIMARY 512','#define NUM_METATILES_IN_PRIMARY 512','#define NUM_PALS_IN_PRIMARY 6']:
 if line not in s:raise SystemExit('Unsupported tile allocation: '+line)
changes={};headers={k:[] for k in ['graphics','metatiles','headers','externs']}
for ent in json.loads((P/'manifest.json').read_text())['entries']:
 name=ent['name'];symbol='BLGym'+name.title();path='data/tilesets/secondary/bl_gym_'+name;dest=r/path
 for src in (P/'assets'/name).iterdir():
  if src.name not in ['tiles.png','tiles.4bpp','metatiles.bin','metatile_attributes.bin','palette.pal','palette.gbapal']:continue
  target=dest/src.name
  if target.exists() and target.read_bytes()!=src.read_bytes():raise SystemExit('Refusing to replace changed asset '+str(target))
  changes[target]=src.read_bytes()
 # Palette files 00..15 facilitate Porymap. Runtime loads secondary slots6..12.
 for n in range(16):
  changes[dest/'palettes'/f'{n:02}.pal']=(P/'assets'/name/'palette.pal').read_bytes()
 headers['graphics'].append(f'const u32 gTilesetTiles_{symbol}[] = INCBIN_U32("{path}/tiles.4bpp");\nconst u16 ALIGNED(4) gTilesetPalettes_{symbol}[16][16] = {{\n'+''.join(f'    INCBIN_U16("{path}/palette.gbapal"),\n' for n in range(16))+'};\n')
 headers['metatiles'].append(f'const u16 gMetatiles_{symbol}[] = INCBIN_U16("{path}/metatiles.bin");\nconst u16 gMetatileAttributes_{symbol}[] = INCBIN_U16("{path}/metatile_attributes.bin");\n')
 headers['headers'].append(f'const struct Tileset gTileset_{symbol} = {{\n .isCompressed = FALSE, .isSecondary = TRUE, .tiles = gTilesetTiles_{symbol},\n .palettes = gTilesetPalettes_{symbol}, .metatiles = gMetatiles_{symbol},\n .metatileAttributes = gMetatileAttributes_{symbol}, .callback = NULL,\n}};\n')
 headers['externs'].append(f'extern const struct Tileset gTileset_{symbol};\n')
for key,f in [('graphics','src/data/tilesets/graphics.h'),('metatiles','src/data/tilesets/metatiles.h'),('headers','src/data/tilesets/headers.h'),('externs','include/tilesets.h')]:
 target=r/f;s=target.read_text();block='\n// BEGIN BLACK LEDGER GYM ASSETS V1\n#if !IS_FRLG\n'+''.join(headers[key])+'#endif\n// END BLACK LEDGER GYM ASSETS V1\n'
 if 'BEGIN BLACK LEDGER GYM ASSETS V1' in s:
  if block not in s:raise SystemExit('Registration was modified; manual merge needed: '+f)
 else:
  if 'gTileset_BLGymViolet' in s:raise SystemExit('Symbol collision: '+f)
  if key=='externs':
   p=s.rfind('#endif');assert p>=0;s=s[:p]+block+s[p:]
  else:s+=block
 changes[target]=s.encode()
print(('APPLY' if a.apply else 'DRY RUN')+': register eight unused standalone secondary tilesets; no map assignments/warps/saves are edited.')
for target,data in changes.items():
 if a.apply:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
print(f'{len(changes)} paths inspected. Read README before assigning a tileset to a city.')
