#!/usr/bin/env python3
"""Validate source-shaped hall, old-layout preservation and migration mask.

Checks are static; movement, rendering, save/Continue and puzzle interactions
must be exercised in the actual emulator build.
"""
import json,struct,subprocess
from pathlib import Path
from build_hgss_ruins_hall_reference import build,OLD_LAYOUT,NEW_LAYOUT,MASK_PATH

R=Path(__file__).resolve().parents[2]
def load(p):return json.loads((R/p).read_text())
def words(path):
    b=(R/path).read_bytes();assert len(b)%2==0
    return struct.unpack('<%dH'%(len(b)//2),b)

layouts={v['id']:v for v in load('data/layouts/layouts.json')['layouts']}
old=layouts[OLD_LAYOUT];new=layouts[NEW_LAYOUT]
assert (old['width'],old['height'])==(29,32) and (new['width'],new['height'])==(32,64)
assert old['blockdata_filepath']!=new['blockdata_filepath'] and old['border_filepath']!=new['border_filepath']
# Pinned predecessor's exact map and border remain in place for legacy saves.
for path in (old['blockdata_filepath'],old['border_filepath']):
    assert (R/path).read_bytes()==subprocess.check_output(['git','show','1752f15e53:'+path],cwd=R),path
writes={};tiles,mask,component=build(lambda path,data:writes.update({path:data}))
assert words(new['blockdata_filepath'])==tuple(tiles)
assert writes[MASK_PATH]==(R/MASK_PATH).read_bytes()==mask
assert len(component)==816 and len(mask)==32*64 and sum(x==5 for x in mask)==776
assert all(v in (0,5) for v in mask)
assert {(x,y) for y in range(64) for x in range(32) if not tiles[y*32+x]&0xc00}==component
assert all(not mask[y*32+x] or tiles[y*32+x]==0x3001 for x,y in component)
assert all(mask[y*32+x]==5 for x,y in ((5,42),(5,24)))
assert all(mask[y*32+x]==0 for x,y in ((18,24),(18,23)))
hall=load('data/maps/RuinsOfAlph_UndergroundHall/map.json')
entry=load('data/maps/RuinsOfAlph_HallEntrance/map.json')
assert hall['id']=='MAP_RUINS_OF_ALPH_UNDERGROUND_HALL' and hall['layout']==NEW_LAYOUT
assert [(e['x'],e['y'],e['dest_warp_id']) for e in hall['warp_events']]==[(18,24,'1'),(18,23,'2')]
assert [(e['x'],e['y'],e['dest_warp_id']) for e in entry['warp_events'][1:]]==[(6,7,'0'),(7,7,'1')]
for name,landing in (('Southwest',(5,42)),('Northwest',(5,24))):
    script=(R/f'data/maps/RuinsOfAlph_{name}Chamber/scripts.inc').read_text()
    assert f'warp MAP_RUINS_OF_ALPH_UNDERGROUND_HALL, {landing[0]}, {landing[1]}' in script
print('Expanded hall: original layout bytes, exact source geometry, 2 paired exits, 2 fall coordinates and 776 migration cells PASS; no emulator test.')
