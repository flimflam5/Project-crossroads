#!/usr/bin/env python3
"""Check source packing and incompatibility handling without writing game files."""
import struct
import subprocess
import sys
import tempfile
from pathlib import Path
from build_hgss_ruins_assets import prepare


def run():
    files = {}
    def write(path, data):
        assert path not in files, path
        files[path] = data
    maps = prepare(write)
    assert len(files) == 61
    assert all(len(maps[n]) == count for n, count in {
        'NorthwestPocket': 16*17, 'SouthwestPocket': 22*14,
        'NorthwestChamber': 10*11, 'SouthwestChamber': 10*11,
        'UndergroundHall': 29*32}.items())
    for name in ('hgssruinspocket','hgssruinschamber','hgssruinshall'):
        path='data/tilesets/primary/'+name
        meta=files[path+'/metatiles.bin'];attrs=files[path+'/metatile_attributes.bin']
        assert len(meta)==8*len(attrs) and len(attrs)<=1024
        assert files[path+'/tiles.png'][:8]==b'\x89PNG\r\n\x1a\n'
        assert all(files[path+f'/palettes/{i:02}.pal'] for i in range(16))
    attrs=files['data/tilesets/primary/hgssruinspocket/metatile_attributes.bin']
    with tempfile.TemporaryDirectory(prefix='ruins-behavior-test-') as temp:
        subprocess.run([sys.executable, str(Path(__file__).with_name('prepare_hns_ruins_pockets.py')),
                        '--output', temp], check=True, stdout=subprocess.DEVNULL)
        original=(Path(temp)/'outside/metatile_attributes.bin').read_bytes()
        assert len(attrs)==len(original)
        changes=[(original[i],attrs[i]) for i in range(len(attrs)) if original[i]!=attrs[i]]
        assert changes and all(pair==(0xf0,0) for pair in changes)
    assert all(attrs[i]!=0xf0 for i in range(0,len(attrs),2))
    for path in ('src/data/tilesets/graphics.h','src/data/tilesets/metatiles.h',
                 'src/data/tilesets/headers.h','include/tilesets.h'):
        text=files[path]
        assert text.count('// BEGIN HGSS RUINS PRIVATE')==1
        assert text.count('// END HGSS RUINS PRIVATE')==1
        for name in ('HgssRuinsPocket','HgssRuinsChamber','HgssRuinsHall'):
            assert name in text
    for k, data in files.items():
        if not isinstance(data, bytes): files[k]=data.encode()
    return files, maps


if __name__ == '__main__':
    a, amap=run()
    b, bmap=run()
    assert a==b and amap==bmap, 'Ruins asset output is not deterministic'
    print('Ruins private assets: source hashes, five sizes, attributes, registrations and determinism pass; no game maps tested.')
