#!/usr/bin/env python3
"""Validate generated Ruins door approaches and reciprocal targets statically.

Normal movement, visuals, map transitions and old saves require an emulator.
"""
import json
import struct
from pathlib import Path
from stage_hgss_ruins_network import NAMES, IDS

R=Path(__file__).resolve().parents[2]
def load(path):return json.loads((R/path).read_text())
def words(path):
    data=(R/path).read_bytes();assert len(data)%2==0
    return struct.unpack('<%dH'%(len(data)//2),data)

layouts={x['id']:x for x in load('data/layouts/layouts.json')['layouts']}
maps={n:load(f'data/maps/{n}/map.json') for n in (*NAMES,'RuinsOfAlph','UnionCave_1F')}
assert [maps[n]['id'] for n in NAMES]==list(IDS)
assert load('data/maps/map_groups.json')['gMapGroup_CrossroadsJohtoExpansion'][51:57]==list(NAMES)
by_id={m['id']:m for m in maps.values()}
for name in NAMES:
    m=maps[name]
    for i,w in enumerate(m['warp_events']):
        target=by_id[w['dest_map']]['warp_events'][int(w['dest_warp_id'])]
        assert target['dest_map']==m['id'] and int(target['dest_warp_id'])==i,(name,i,target)

def tileinfo(name,x,y,attribute_path):
    m=maps[name];layout=layouts[m['layout']];w,h=layout['width'],layout['height']
    assert 0<=x<w and 0<=y<h
    tiles=words(layout['blockdata_filepath']);attrs=words(attribute_path)
    raw=tiles[y*w+x];index=raw&1023
    if index>=512:index-=512
    assert 0<=index<len(attrs),(name,x,y,hex(raw))
    return raw,attrs[index]&255

def doorway(name,number,attr_path,expected_behavior,approaches):
    event=maps[name]['warp_events'][number];x,y=event['x'],event['y']
    raw,behavior=tileinfo(name,x,y,attr_path)
    assert not raw&0xc00 and behavior==expected_behavior,(name,number,hex(raw),hex(behavior))
    height=raw>>12
    for dx,dy in approaches:
        nx,ny=x+dx,y+dy;other,_=tileinfo(name,nx,ny,attr_path)
        assert not other&0xc00 and (other>>12 in (0,height) or height==0),(name,number,nx,ny,hex(other),height)
        assert event['elevation'] in (0,height),(name,number,'incompatible event elevation')

outside='data/tilesets/primary/hgssruinspocket/metatile_attributes.bin'
interior='data/tilesets/primary/hgssruinschamber/metatile_attributes.bin'
hall='data/tilesets/primary/hgssruinshall/metatile_attributes.bin'
public='data/tilesets/secondary/hgss_ruins_public/metatile_attributes.bin'
for n in NAMES[:2]:
    for i in (0,1):doorway(n,i,outside,0x60,[(0,1)])
for n in NAMES[2:4]:doorway(n,0,interior,0x65,[(0,-1)])
doorway(NAMES[4],0,hall,0x61,[(0,-1),(0,1)])
doorway(NAMES[5],0,hall,0x61,[(0,-1)])
doorway(NAMES[5],1,hall,0x61,[(0,-1),(0,1)])
doorway('RuinsOfAlph',2,public,0x60,[(0,1)])
print('Generated IDs, reciprocal targets, door behavior, elevations and approaches pass. Emulator playtest and owner QA remain pending.')
