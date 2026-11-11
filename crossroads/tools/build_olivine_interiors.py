#!/usr/bin/env python3
"""Distinct office interiors using existing compatible Facility tiles.

Keep both maps 10x8 and their accepted door/case/NPC coordinates unchanged.
"""
import argparse
import struct
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]


def generate():
    source=struct.unpack('<171H',(ROOT/'data/layouts/RustboroCity_DevonCorp_2F/map.bin').read_bytes())
    def room():
        t=[0x3380]*80
        for x in range(10):
            t[x]=0x0788+(x%2)
            t[10+x]=0x0790+(x%2)
        # Preserve two south-arrow exits at 3,7 and 4,7 in the new tileset.
        t[73],t[74]=0x3206,0x3207
        return t
    def stamp(t,sx,sy,w,h,x,y):
        for row in range(h):
            t[(y+row)*10+x:(y+row)*10+x+w]=source[(sy+row)*19+sx:(sy+row)*19+sx+w]
    office=room()
    # Wall terminal (7,1), two desks, clear central case at (4,4).
    stamp(office,6,3,2,3,7,0)
    stamp(office,6,3,2,3,1,0) # Visible digital staff-notice workstation.
    stamp(office,6,3,2,3,0,3)
    stamp(office,10,3,2,3,7,3)
    # Worker stands immediately below the right-hand desk at the accepted (7,5).
    office[57]=0x3380
    harbor=room()
    stamp(harbor,6,3,2,3,7,0)
    # Reception counter copied from Devon 1F, with readable ledger at (2,4).
    first=struct.unpack('<171H',(ROOT/'data/layouts/RustboroCity_DevonCorp_1F/map.bin').read_bytes())
    for x in range(3):
        harbor[30+x]=first[3*19+4+x]
        harbor[40+x]=first[4*19+4+x]
    stamp(harbor,6,3,2,3,7,3)
    harbor[57]=0x3380
    # The sampled workstation graphic has passable top-cap words. At row0
    # these are ceiling trim, not public floor: keep their pixels/metatile IDs
    # and add only collision so an obsolete saved position cannot land there.
    for x in (1,2,7,8):office[x]|=0x400
    for x in (7,8):harbor[x]|=0x400
    return {'OlivineSilphOffice':struct.pack('<80H',*office),
            'OlivineHarborOffice':struct.pack('<80H',*harbor)}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    for name,data in generate().items():
        path=ROOT/f'data/layouts/{name}/map.bin'
        if args.check:
            assert path.read_bytes()==data,f'Regenerate {name}'
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(data)
            (path.parent/'border.bin').write_bytes(struct.pack('<4H',*([0x0601]*4)))
    if args.check:print('Distinct Olivine offices: reproducible layouts and stable dimensions: PASS')
