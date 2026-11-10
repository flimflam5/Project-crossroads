"""Behavior-free terrain shared by Ecruteak and its three scrolling neighbors.

General 0x24 looks like ground but has SOUTH_ARROW_WARP behavior. It must never
be used as ordinary seam paving. Only unused metatile 0x1ff is overridden here;
the original General tileset and real arrow-warp tiles are left intact.
"""
import re
import struct
from pathlib import Path

R = Path(__file__).resolve().parents[2]
PAVING = 0x1ff
PAVING_GRAPHIC = 1  # unused by every original General metatile, below animation slots
NEIGHBORS = {'JohtoRoute37', 'JohtoRoute38', 'JohtoRoute42'}


def neutral_metadata(metas, attrs):
    metas = list(metas)
    attrs = list(attrs)
    metas[PAVING*8:(PAVING+1)*8] = [0x3000|PAVING_GRAPHIC]*4+[0]*4
    attrs[PAVING] = 0x1000  # covered ground, MB_NORMAL
    return metas, attrs


def neutral_graphics():
    """Existing project's brick texture in the unchanged General gray palette."""
    from PIL import Image
    general = R/'data/tilesets/primary/general'
    original = struct.unpack('<4096H', (general/'metatiles.bin').read_bytes())
    assert PAVING_GRAPHIC not in {v & 1023 for v in original}
    assert PAVING_GRAPHIC < 432
    stone = Image.open(R/'data/tilesets/secondary/slateport/tiles.png').crop((48,32,56,40))
    assert set(stone.tobytes()) == {2,3}
    stone = Image.frombytes('P',(8,8),bytes({2:3,3:4}[v] for v in stone.tobytes()))
    sheet = Image.open(general/'tiles.png').copy()
    sheet.paste(stone, (PAVING_GRAPHIC%16*8,PAVING_GRAPHIC//16*8))
    return sheet


def generate(check=False):
    def write(path, data):
        p = R/path
        if isinstance(data, str):
            data = data.encode()
        if check:
            assert p.read_bytes() == data, ('Regenerate neutral Ecruteak terrain', path)
        elif not p.exists() or p.read_bytes() != data:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)

    p = R/'data/tilesets/primary/general'
    gm, ga = neutral_metadata(struct.unpack('<4096H', (p/'metatiles.bin').read_bytes()),
                              struct.unpack('<512H', (p/'metatile_attributes.bin').read_bytes()))
    root = 'data/tilesets/primary/hgss_ecruteak_buffer'
    sheet = neutral_graphics()
    if check:
        from PIL import Image
        assert Image.open(R/root/'tiles.png').tobytes()==sheet.tobytes()
    else:
        (R/root).mkdir(parents=True,exist_ok=True)
        sheet.save(R/root/'tiles.png',bits=4)
    write(root+'/metatiles.bin', struct.pack('<4096H', *gm))
    write(root+'/metatile_attributes.bin', struct.pack('<512H', *ga))
    start = '// BEGIN ECRUTEAK NEUTRAL BUFFER'
    end = '// END ECRUTEAK NEUTRAL BUFFER'
    declarations = {
        'src/data/tilesets/graphics.h': f'const u32 gTilesetTiles_HgssEcruteakBuffer[] = INCGFX_U32("{root}/tiles.png", ".4bpp.fastSmol");\n',
        'src/data/tilesets/metatiles.h': f'const u16 gMetatiles_HgssEcruteakBuffer[] = INCBIN_U16("{root}/metatiles.bin");\nconst u16 gMetatileAttributes_HgssEcruteakBuffer[] = INCBIN_U16("{root}/metatile_attributes.bin");\n',
        'src/data/tilesets/headers.h': 'const struct Tileset gTileset_HgssEcruteakBuffer = {\n .isCompressed=TRUE, .isSecondary=FALSE,\n .tiles=gTilesetTiles_HgssEcruteakBuffer, .palettes=gTilesetPalettes_General,\n .metatiles=gMetatiles_HgssEcruteakBuffer, .metatileAttributes=gMetatileAttributes_HgssEcruteakBuffer,\n .callback=InitTilesetAnim_General,\n};\n',
        'include/tilesets.h': 'extern const struct Tileset gTileset_HgssEcruteakBuffer;\n',
    }
    for path, body in declarations.items():
        text = (R/path).read_text()
        block = start+'\n#if !IS_FRLG\n'+body+'#endif\n'+end
        if start in text:
            text = re.sub(re.escape(start)+r'.*?'+re.escape(end), lambda _: block, text, flags=re.S)
        elif path == 'include/tilesets.h':
            i = text.rfind('#endif')
            text = text[:i]+block+'\n'+text[i:]
        else:
            text += '\n'+block+'\n'
        write(path, text)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--check', action='store_true')
    generate(p.parse_args().check)
