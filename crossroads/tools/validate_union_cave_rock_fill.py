#!/usr/bin/env python3
"""Check cave rock-hole repair; --installed verifies generated map bytes.

This is a shape/collision regression, not an emulator or visual acceptance.
"""
import argparse
import json
from pathlib import Path
import struct
import build_hgss_union_cave as cave

R = Path(__file__).resolve().parents[2]
EXAMPLES = {
    '1F': ((5,31), (21,67), (22,67)),
    '2F': ((16,14), (20,9), (14,39)),
    '3F': ((7,73), (10,81)),
}
EXTERIOR = {'1F': (0,5), '2F': (0,14), '3F': (0,0)}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--installed',action='store_true')
    args=parser.parse_args()
    # A truly enclosed plateau hole closes, while black connected to an edge
    # and an enclosed cell bounded by non-rock remain black.
    b=cave.VOID_BORDER; s=cave.SOLID_ROCK
    sample=[b,b,b,b,b, b,s,s,s,b, b,s,b,s,b, b,s,s,s,b, b,b,b,b,b]
    out=cave.fill_enclosed_void(5,5,sample)
    assert out[12]==s and all(out[i]==sample[i] for i in range(25) if i!=12)
    sample[7]=0x3001
    assert cave.fill_enclosed_void(5,5,sample)[12]==b
    assert (s&0xc00)==(b&0xc00)==0x400
    attrs=cave.read16(R/cave.OUT/'metatile_attributes.bin')
    assert attrs[s&1023]==0x1008 and attrs[b&1023]==0x1000
    for floor,examples in EXAMPLES.items():
        raw=(R/f'data/layouts/HgssUnionCave_{floor}/map.bin').read_bytes()
        vals=list(struct.unpack(f'<{len(raw)//2}H',raw)); w=32; h=len(vals)//w
        result=cave.fill_enclosed_void(w,h,vals)
        for (x,y) in examples:assert result[y*w+x]==s,(floor,x,y)
        x,y=EXTERIOR[floor];assert vals[y*w+x]==result[y*w+x]==b,(floor,x,y)
        for before,after in zip(vals,result):
            assert before==after or (before,after)==(b,s)
        if args.installed:assert vals==result,(floor,'generator has not installed the rock fill')
        events=json.loads((R/f'data/maps/UnionCave_{floor}/map.json').read_text())
        for event in events['warp_events']:
            i=event['y']*w+event['x'];assert vals[i]==result[i],(floor,'warp changed')
    print('PASS cave rock fills, external void, collision and warp preservation; emulator visual QA pending')

if __name__=='__main__':main()
