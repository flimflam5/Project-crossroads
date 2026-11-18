#!/usr/bin/env python3
"""Check four staged rooms against source permissions; no emulator claim."""
import json,struct
from pathlib import Path
from stage_hgss_ruins_hidden import stage,reference_component,NAMES

ROOT=Path(__file__).resolve().parents[2]
facts=json.loads((ROOT/'crossroads/hgss/canonical_events/ruins-hidden-geometry.json').read_text())

def run():
    files={}
    def write(path,data):
        assert path not in files
        files[path]=data
    planes,layouts,borders,transitions=stage(write)
    assert len(files)==57 and tuple(planes)==NAMES
    for name in NAMES:
        width,height,tileset=layouts[name];values=planes[name]
        assert len(values)==width*height and len(borders[name])==4
        assert all(v&0x400 for v in borders[name])
        group='second' if 'SecondRoom' in name else 'southwest' if 'Southwest' in name else 'northwest'
        path='data/tilesets/primary/hgss_ruins_hidden_'+group
        raw=files[path+'/metatile_attributes.bin'];attrs=struct.unpack('<%dH'%(len(raw)//2),raw)
        component=reference_component(facts['second' if group=='second' else group+'_hidden']['permissions'],
                                      facts['second']['exit'] if group=='second' else facts[group+'_hidden']['landing'])
        reachable={(x,y) for y in range(height) for x in range(width) if not values[y*width+x]&0xc00}
        assert reachable==component,(name,'Source footprint changed',reachable^component)
        assert all(values[y*width+x]>>12==3 for x,y in reachable)
        for x,y in reachable:
            tile=values[y*width+x]&1023;assert tile<len(attrs)
            behavior=attrs[tile]&255
            assert behavior in (0,8,0x65),(name,x,y,hex(behavior))
            if behavior==0x65:assert group=='second' and (x,y)==(6,17)
        assert all(v&1023<len(attrs) for v in values)
        assert transitions[name]['events_installed'] is False
    for n in NAMES[:2]:
        assert transitions[n]['ordinary_exit']==[6,17] and transitions[n]['scripted_fall']==[6,3]
        assert transitions[n]['unapproved_reward_positions']==[[4,8],[8,8],[4,12],[8,12]]
    assert transitions[NAMES[2]]['fall_arrival']==[11,7] and transitions[NAMES[2]]['scripted_fall']==[20,13]
    assert transitions[NAMES[2]]['hgss_hall_landing']==[5,42]
    assert transitions[NAMES[3]]['fall_arrival']==[11,14] and transitions[NAMES[3]]['scripted_fall']==[20,21]
    assert transitions[NAMES[3]]['hgss_hall_landing']==[5,24]
    assert NAMES[0]!=NAMES[1] and NAMES[2]!=NAMES[3]
    return files,planes,layouts,borders,transitions

if __name__=='__main__':
    assert run()==run(),'Non-deterministic room staging'
    print('Four unregistered rooms: reference dry components, bounds, elevations, behaviors and transition anchors PASS; no emulator test.')
