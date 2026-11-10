#!/usr/bin/env python3
"""Convert the owner-approved title reference into native GBA 8bpp BG assets.

This is format/palette conversion, not replacement artwork. Keeps the full image,
including the updated game title and Press Start prompt.
"""
import argparse
import hashlib
import json
import struct
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / 'graphics/title_screen/black_ledger'


def generate():
    image = Image.open(DIR / 'reference/harbor-black-ledger.png').convert('RGB')
    image = image.resize((240, 160), Image.Resampling.LANCZOS)
    image = image.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    palette = image.getpalette()
    pixels = image.tobytes()
    tiles = b''.join(pixels[(y+row)*240+x:(y+row)*240+x+8]
                     for y in range(0,160,8) for x in range(0,240,8) for row in range(8))
    tilemap = [0] * 1024
    for y in range(20):
        for x in range(30):
            tilemap[y*32+x] = y*30+x
    colors = [(palette[i]>>3) | ((palette[i+1]>>3)<<5) | ((palette[i+2]>>3)<<10)
              for i in range(0,768,3)]
    # Warm lighthouse window color, used for a restrained shared-light pulse.
    light = pixels[87*240+217]
    metadata = dict(title='Pokémon: Black Ledger',
                    source_sha256=hashlib.sha256((DIR/'reference/harbor-black-ledger.png').read_bytes()).hexdigest(),
                    dimensions=[240,160],bpp=8,tiles=600,light_palette_index=light)
    outputs = {'tiles.bin':tiles,'tilemap.bin':struct.pack('<1024H',*tilemap),
               'palette.bin':struct.pack('<256H',*colors),
               'metadata.json':(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n').encode(),
               'light.h':f'#define BLACK_LEDGER_LIGHT_PALETTE_INDEX {light}\n'.encode()}
    return image, outputs


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    image,outputs=generate()
    if args.check:
        for name,data in outputs.items():
            assert (DIR/name).read_bytes()==data, f'Regenerate title {name}'
        assert len(outputs['tiles.bin'])==38400
        assert 38400 < 31*2048, 'Character data must not overlap BG screen block 31'
        print('Black Ledger native title palette, tilemap, VRAM bounds and provenance: PASS')
    else:
        for name,data in outputs.items():
            (DIR/name).write_bytes(data)
        image.save(DIR/'native-preview.png',bits=8)
