#!/usr/bin/env python3
"""Office collision/interaction/old-save escape and home rest contract checks."""
import json
import struct
from collections import deque
from pathlib import Path
from build_olivine_interiors import generate
root=Path(__file__).resolve().parents[2]
old=struct.unpack('<80H',(root/'data/layouts/HouseWithBed/map.bin').read_bytes())
attrs=(root/'data/tilesets/secondary/facility/metatile_attributes.bin').read_bytes()
for suffix,data in generate().items():
    assert (root/f'data/layouts/{suffix}/map.bin').read_bytes()==data
    name='OlivineCity_'+('SilphOffice' if suffix=='OlivineSilphOffice' else 'HarborOffice')
    m=json.loads((root/f'data/maps/{name}/map.json').read_text())
    tiles=struct.unpack('<80H',data)
    blocked={(o['x'],o['y']) for o in m['object_events']}
    seen={(3,6)};q=deque(seen)
    while q:
        x,y=q.popleft()
        for p in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
            a,b=p
            if p in seen or p in blocked or not(0<=a<10 and 0<=b<8):continue
            t=tiles[b*10+a]
            if t&0xc00 or t>>12!=3:continue
            seen.add(p);q.append(p)
    for event in m['object_events']+m['bg_events']:
        assert any((event['x']+dx,event['y']+dy) in seen for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]),(name,event)
    for warp in m['warp_events']:
        x,y=warp['x'],warp['y'];assert (x,y-1) in seen
        tile=tiles[y*10+x]&0x3ff
        assert struct.unpack_from('<H',attrs,(tile-512)*2)[0]&255==0x65, 'Preserve south-arrow exit behavior'
    for i,tile in enumerate(old):
        if tile&0xc00 or tile>>12!=3:continue
        x,y=i%10,i//10
        if (x,y) not in seen:
            assert any((x+dx,y+dy) in seen for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]),('Trapped legacy save coordinate',name,x,y)
case=json.loads((root/'data/maps/OlivineCity_SilphOffice/map.json').read_text())['object_events'][1]
assert (case['x'],case['y'],case['script'])==(4,4,'Crossroads_EventScript_ChooseStarter')
s=(root/'crossroads/scripts/olivine_interiors.inc').read_text()
assert 'special HealPlayerParty' in s and 'goto_if_eq VAR_RESULT, NO' in s
assert not any(op in s for op in ['givemon ','setrespawn ','setflag ','setvar ','giveitem ']), 'No grants, story state or respawn override in home rest'
print('Office interactions/exit behaviors, starter coordinates, legacy escape paths and nonpersistent home rest: PASS')
