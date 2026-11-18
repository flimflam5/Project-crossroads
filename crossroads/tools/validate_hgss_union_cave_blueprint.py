#!/usr/bin/env python3
"""Exercise the isolated HGSS Union Cave layout generation without linking it.

Checks in-memory map output, references and continue masks. Real Ruins maps,
compiled gameplay, rendering, actions and old-save testing remain required.
"""
import json, sys
from pathlib import Path
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'crossroads/tools'))
import build_hgss_union_cave as g

groups=json.loads((R/'data/maps/map_groups.json').read_text())
names=groups['gMapGroup_CrossroadsOlivine']+groups['gMapGroup_CrossroadsJohtoExpansion']
maps={n:json.loads((R/'data/maps'/n/'map.json').read_text()) for n in names}
old={n:json.loads(json.dumps(maps[n]['warp_events'])) for n in g.FLOORS}
# Stubs are deliberately in-memory: user-facing pockets are not installed.
maps['RuinsOfAlph_SouthwestPocket']={'id':'MAP_RUINS_OF_ALPH_SOUTHWEST_POCKET'}
maps['RuinsOfAlph_NorthwestPocket']={'id':'MAP_RUINS_OF_ALPH_NORTHWEST_POCKET'}
layouts={x['id']:x for x in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
outputs={};tiles={};sizes={}
def write(path,data):outputs[path]=data.encode() if isinstance(data,str) else data
g.apply(maps,tiles,sizes,layouts,write)
for path,content in outputs.items():
    disk=R/path
    assert disk.is_file() and disk.read_bytes()==content, ('Packed resource differs; regenerate',path)
assert sizes=={'UnionCave_1F':(32,96),'UnionCave_2F':(32,64),'UnionCave_3F':(32,96)}
for name in g.FLOORS:
    w,h=sizes[name];m=maps[name];assert len(tiles[name])==w*h
    for i,event in enumerate(old[name]):
        newer=m['warp_events'][i]
        assert (newer['dest_map'],newer['dest_warp_id'])==(event['dest_map'],event['dest_warp_id'])
    mask=outputs[f'data/layouts/{name}/safe_continue.bin'];assert len(mask)==w*h
    occupied={(e['x'],e['y']) for e in m['warp_events']+m['object_events']+m['bg_events']}
    assert all(mask[y*w+x]==0 for x,y in occupied)
    assert all(not(v&4) or v&1 for v in mask) and sum(bool(v&4) for v in mask)>10
    assert all(not(v&1) or tiles[name][i]==0x3001 for i,v in enumerate(mask))
    assert all(not(v&2) or tiles[name][i]>>12==1 for i,v in enumerate(mask))
    on_disk=R/f'data/layouts/{name}/safe_continue.bin'
    assert on_disk.read_bytes()==mask,('Run isolated mask generator',name)
    print(name, 'dimensions',w,h,'warps',len(m['warp_events']),'dry',sum(bool(v&1) for v in mask),'Surf',sum(bool(v&2) for v in mask),'fallback',sum(bool(v&4) for v in mask))
# Every proposed reference anchor must retain its dry and water-permissive
# component relationships after placing the preserved actors and signs. This
# catches artificial shortcuts and interactions that block a narrow passage.
facts=json.loads((R/'crossroads/hgss/canonical_events/union-cave-geometry.json').read_text())
for name,refname in g.FLOORS.items():
    w,h=sizes[name];fact=facts[refname];generated=[0 if v&0xc00 else 2 if v>>12==1 else 1 for v in tiles[name]]
    for event in maps[name]['object_events']:generated[event['y']*w+event['x']]=0
    _,_,permissions=g.reference_planes(fact)
    reference=[0 if v&0x8000 else 2 if v&255==0x15 else 1 for v in permissions]
    for i,e in enumerate(fact['warps']):
        seed=(e['x'],e['z'])
        for allow_water in (False,True):
            got=g.flood(w,h,generated,seed,allow_water);want=g.flood(w,h,reference,seed,allow_water)
            anchors=lambda region:{j for j,z in enumerate(fact['warps']) if (z['x'],z['z']) in region}
            assert anchors(got)==anchors(want),(name,i,allow_water,anchors(got),anchors(want))
for name in g.FLOORS:
    m=maps[name]
    for e in m['warp_events']:
        dst=next((n for n in g.FLOORS if maps[n]['id']==e['dest_map']),None)
        if dst:
            target=maps[dst]['warp_events'][int(e['dest_warp_id'])]
            assert target['dest_map']==m['id'] and int(target['dest_warp_id'])==m['warp_events'].index(e)
print('PASS: isolated reference-shaped floor blueprint, retained warp indices, reciprocal internal ladders and explicit save masks. Not linked or emulator-tested.')
