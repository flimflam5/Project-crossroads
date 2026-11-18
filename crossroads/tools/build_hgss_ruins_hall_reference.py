#!/usr/bin/env python3
"""Reference-shaped GBA Underground Hall with a distinct saved layout ID.

Geometry comes from pinned HGSS permission facts and existing HNS stone art.
The caller installs its map/layout and separately handles old-save migration.
No items, story flags, or new NPCs are introduced here.
"""
from collections import deque
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OLD_LAYOUT='LAYOUT_RUINS_OF_ALPH_UNDERGROUND_HALL'
NEW_LAYOUT='LAYOUT_HGSS_RUINS_HALL_EXPANDED'
MASK_PATH='data/layouts/RuinsOfAlph_UndergroundHall/safe_continue_expanded.bin'
WIDTH,HEIGHT=32,64


def source_component(perms,seed):
    queue=deque([seed]);seen=set(queue)
    while queue:
        x,y=queue.popleft()
        for p in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            a,b=p
            if 0<=a<WIDTH and 0<=b<HEIGHT and p not in seen and not perms[b*WIDTH+a]&0x8000:
                seen.add(p);queue.append(p)
    return seen


def build(write):
    facts=json.loads((ROOT/'crossroads/hgss/canonical_events/ruins-hidden-geometry.json').read_text())
    assert facts['revision']=='6bf138d6035aa6b43d6f8f4132a12df70f86dcec'
    hall=facts['hall'];assert hall['matrix_dimensions']==[1,2] and hall['models']==[470,471]
    assert hall['exits']==[[18,24,1],[18,23,1]]
    perms=hall['permissions'][0]+hall['permissions'][1]
    assert len(perms)==WIDTH*HEIGHT
    component=source_component(perms,(18,24));assert len(component)==816
    assert {(5,42),(5,24),(18,24),(18,23)}<=component
    # Blank donor tile 0 draws the same black void as the previous HNS hall.
    values=[0x0400]*(WIDTH*HEIGHT)
    for x,y in component:values[y*WIDTH+x]=0x3001
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (x,y) in component:continue
            if (x,y+1) in component:values[y*WIDTH+x]=0x040c
            elif (x,y-1) in component:values[y*WIDTH+x]=0x040f
            elif (x+1,y) in component or (x-1,y) in component:values[y*WIDTH+x]=0x0409
    # The reference has 30 wall inscriptions on impassable statue bases.
    # The existing HNS tiles contribute a compatible stone statue and top.
    for x,y in hall['background_positions']:
        assert (x,y) not in component and (x,y-1) in component
        values[y*WIDTH+x]=0x0402
        values[(y-1)*WIDTH+x]=0x3017
    # Preserve old warp index 0 and append the second paired entrance.
    for x,y,_ in hall['exits']:values[y*WIDTH+x]=0x3019
    occupied={(x,y) for x,y,_ in hall['exits']}|{tuple(p) for p in hall['object_positions']}
    mask=bytearray(WIDTH*HEIGHT)
    for x,y in component:
        if (x,y) not in occupied and values[y*WIDTH+x]==0x3001:
            mask[y*WIDTH+x]=5
    assert sum(v==5 for v in mask)>500
    assert all(mask[y*WIDTH+x]==0 for x,y in occupied)
    assert all(mask[y*WIDTH+x]==5 for x,y in [(5,42),(5,24)])
    write(MASK_PATH,bytes(mask))
    return values,bytes(mask),component
