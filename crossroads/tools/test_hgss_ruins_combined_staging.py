#!/usr/bin/env python3
"""Ensure in-memory staging composes private tileset registrations."""
import json
from pathlib import Path
from stage_hgss_ruins_facade import stage as facade, readwords
from stage_hgss_ruins_network import stage as network

ROOT=Path(__file__).resolve().parents[2]
HEADERS=('src/data/tilesets/graphics.h','src/data/tilesets/metatiles.h',
         'src/data/tilesets/headers.h','include/tilesets.h')


def run():
    files={}
    def write(path,data):files[path]=data.encode() if isinstance(data,str) else data
    def read(path):return files[path].decode() if path in files else (ROOT/path).read_text()
    m=json.loads((ROOT/'data/maps/RuinsOfAlph/map.json').read_text())
    tiles=readwords(ROOT/'data/layouts/RuinsOfAlph/map.bin')
    border=readwords(ROOT/'data/layouts/RuinsOfAlph/border.bin')
    network(write,read)
    facade(write,m,tiles,border,read)
    for path in HEADERS:
        out=files[path].decode()
        for mark in ('HGSS RUINS PRIVATE','HGSS RUINS PUBLIC PRIVATE'):
            assert out.count('// BEGIN '+mark+'\n')==1,(path,mark)
            assert out.count('// END '+mark+'\n')==1,(path,mark)
    baseline=files.copy()
    # Model --check after both complete generated sections already exist.
    network(write,read)
    facade(write,m,tiles,border,read)
    assert files==baseline,'Combined --check would not reproduce generated sections'
    return files


if __name__=='__main__':
    assert run()==run()
    print('Combined private registrations compose and reproduce deterministically.')
