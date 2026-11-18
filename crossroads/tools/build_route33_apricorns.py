#!/usr/bin/env python3
"""Generate reference-coloured decorative Apricorn trees, without rewards.

The 16x16 base image is the existing expansion Apricorn tree, byte-identical
with Pokémon Heart & Soul commit 167aa6d537b109bb229c231ddce4616974c4da71.
The two fruits and six formerly unused palette colours are original edits.
"""
import argparse
import hashlib
import io
from pathlib import Path
from PIL import Image
R = Path(__file__).resolve().parents[2]
SOURCE = R / 'graphics/object_events/pics/misc/apricorn_tree.png'
EXPECTED = 'b231bd4dec027304b6b0c7b758e9cc76e76830ab06d6cf1724a789d1a2bfaaa1'
COLORS = {1:(248,192,216), 2:(232,104,160), 3:(160,48,104),
          5:(128,136,160), 6:(64,72,88), 7:(16,24,40)}
MASK = ((None,2,2,None),(2,0,1,2),(2,1,1,2),(None,2,2,None))

def generate(check=False):
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
    source = Image.open(SOURCE)
    assert source.mode == 'P' and source.size == (16,16)
    assert not (set(COLORS) & set(source.tobytes())), 'Base uses a new fruit palette slot'
    palette = source.getpalette()
    for index, rgb in COLORS.items():
        palette[index*3:index*3+3] = rgb
    for name, shades in [('pink',(1,2,3)),('black',(5,6,7))]:
        sprite=source.copy()
        sprite.putpalette(palette)
        for y,row in enumerate(MASK):
            for x,index in enumerate(row):
                if index is not None:
                    sprite.putpixel((6+x,5+y), shades[index])
        stream=io.BytesIO()
        sprite.save(stream, format='PNG', optimize=False)
        path=SOURCE.with_name(f'route33_apricorn_{name}.png')
        if check:
            assert path.read_bytes() == stream.getvalue(), ('Regenerate',str(path))
        elif not path.exists() or path.read_bytes()!=stream.getvalue():
            path.write_bytes(stream.getvalue())
    print('Route 33 pink/black Apricorn sprites: upstream tree + original fruit pixels; no item/flag behavior.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');generate(p.parse_args().check)
