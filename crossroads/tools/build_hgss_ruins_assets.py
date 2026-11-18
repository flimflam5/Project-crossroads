#!/usr/bin/env python3
"""Prepare private Emerald-compatible Ruins tilesets without registering maps.

This helper only generates files through its caller's write function. It does
not patch the live network, entrances, map IDs, scripts, or the Continue path.
The chamber and hall still require authored events, fall logic and playtests.
"""
import struct
import subprocess
import sys
import tempfile
from pathlib import Path
from tileset_registration import upsert

ROOT = Path(__file__).resolve().parents[2]
GROUPS = (
    ('HgssRuinsPocket', 'outside', 4),
    ('HgssRuinsChamber', 'chambers', 5),
    ('HgssRuinsHall', 'hall', 3),
)


def prepare(write, read=None):
    """Stage the three private tilesets; return converted map words and reports."""
    if read is None:
        read = lambda path: (ROOT/path).read_text()
    output = {}
    with tempfile.TemporaryDirectory(prefix='hgss-ruins-art-') as temp:
        base = Path(temp)
        for script, target in [('prepare_hns_ruins_pockets.py', base/'pockets'),
                               ('prepare_hns_ruins_hall.py', base/'hall')]:
            subprocess.run([sys.executable, str(ROOT/'crossroads/tools'/script),
                            '--output', str(target)], check=True, stdout=subprocess.DEVNULL)
        sections = {k: [] for k in ('graphics', 'metatiles', 'headers', 'externs')}
        # Append the donor's open-wall tile while retaining all prior indices.
        # Existing chamber cells use palette banks 0..4; the new gate uses 5.
        from stage_hgss_ruins_gate_art import stage as stage_gate_art
        gate_assets={}
        gate_id=stage_gate_art(lambda path,data: gate_assets.__setitem__(path,data))
        assert gate_id==40
        for name, group, palette_count in GROUPS:
            source = base/'hall' if group == 'hall' else base/'pockets'/group
            dest = f'data/tilesets/primary/{name.lower()}'
            meta = (source/'metatiles.bin').read_bytes()
            attrs = bytearray((source/'metatile_attributes.bin').read_bytes())
            assert len(meta) == len(attrs)*8 and len(attrs)//2 <= 512
            # 0xf0 is HNS's headbutt encounter, not an Emerald field behavior.
            # Suppress that unapproved interaction but leave cell collision intact.
            if group == 'outside':
                for i in range(0, len(attrs), 2):
                    if attrs[i] == 0xf0:
                        attrs[i] = 0
            for file,content in [('tiles.png',(source/'tiles.png').read_bytes()),
                                 ('metatiles.bin',meta),('metatile_attributes.bin',bytes(attrs))]:
                path=dest+'/'+file;write(path,gate_assets[path] if group=='chambers' else content)
            for i in range(16):
                palette = source/'palettes'/f'{i if i < palette_count else 0:02}.pal'
                path=dest+f'/palettes/{i:02}.pal';write(path,gate_assets[path] if group=='chambers' else palette.read_bytes())
            sections['graphics'].append(
                f'const u32 gTilesetTiles_{name}[] = INCGFX_U32("{dest}/tiles.png", ".4bpp.fastSmol");\n'
                f'const u16 gTilesetPalettes_{name}[][16] = {{\n' +
                ''.join(f'    INCGFX_U16("{dest}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16)) + '};\n')
            sections['metatiles'].append(
                f'const u16 gMetatiles_{name}[] = INCBIN_U16("{dest}/metatiles.bin");\n'
                f'const u16 gMetatileAttributes_{name}[] = INCBIN_U16("{dest}/metatile_attributes.bin");\n')
            sections['headers'].append(
                f'const struct Tileset gTileset_{name} = {{ .isCompressed=TRUE, .isSecondary=FALSE, '
                f'.tiles=gTilesetTiles_{name}, .palettes=gTilesetPalettes_{name}, '
                f'.metatiles=gMetatiles_{name}, .metatileAttributes=gMetatileAttributes_{name}, .callback=NULL }};\n')
            sections['externs'].append(f'extern const struct Tileset gTileset_{name};\n')
            for path in sorted(source.glob('*.bin')):
                if path.name in ('metatiles.bin', 'metatile_attributes.bin'):
                    continue
                data = path.read_bytes()
                assert len(data) % 2 == 0
                output[path.stem] = list(struct.unpack(f'<{len(data)//2}H', data))
        mark='HGSS RUINS PRIVATE'
        for kind, path in [('graphics','src/data/tilesets/graphics.h'),
                           ('metatiles','src/data/tilesets/metatiles.h'),
                           ('headers','src/data/tilesets/headers.h'),
                           ('externs','include/tilesets.h')]:
            begin, end = '// BEGIN '+mark, '// END '+mark
            body=begin+'\n#if !IS_FRLG\n'+''.join(sections[kind])+'#endif\n'+end
            write(path, upsert(read(path),begin,end,body,externs=kind=='externs'))
    expected={'SouthwestPocket':22*14, 'NorthwestPocket':16*17,
              'SouthwestChamber':10*11, 'NorthwestChamber':10*11,
              'UndergroundHall':29*32}
    assert {k: len(v) for k,v in output.items()} == expected
    return output
