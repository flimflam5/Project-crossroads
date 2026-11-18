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
for name,new_id in g.NEW_LAYOUTS.items():
    old_layout=layouts[maps[name]['layout']];new_layout=layouts[new_id]
    assert (old_layout['width'],old_layout['height'])==(28,22),(name,'Legacy layout changed')
    assert old_layout['blockdata_filepath']!=new_layout['blockdata_filepath']
    assert len((R/old_layout['blockdata_filepath']).read_bytes())==28*22*2
    assert len((R/new_layout['blockdata_filepath']).read_bytes())==new_layout['width']*new_layout['height']*2
outputs={};tiles={};sizes={}
def write(path,data):outputs[path]=data.encode() if isinstance(data,str) else data
g.apply(maps,tiles,sizes,layouts,write)
for path,content in outputs.items():
    disk=R/path
    assert disk.is_file() and disk.read_bytes()==content, ('Packed resource differs; regenerate',path)
assert sizes=={'UnionCave_1F':(32,96),'UnionCave_2F':(32,64),'UnionCave_3F':(32,96)}
for name in g.FLOORS:
    w,h=sizes[name];m=maps[name];assert len(tiles[name])==w*h
    assert m['layout']==g.NEW_LAYOUTS[name]
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
    # Emerald's south-arrow warps only trigger when entered facing south,
    # and the avatar arrives facing north. Ensure the approach/return tile
    # remains ordinary unoccupied dry floor; connectivity alone would not
    # catch an arrow placed against a wall or behind a guide/sign.
    for event in maps[name]['warp_events']:
        x,y=event['x'],event['y'];raw=tiles[name][y*w+x]
        assert raw in (0x3005,0x3006),(name,'unexpected warp tile',x,y,hex(raw))
        if raw==0x3006:
            assert y>0 and tiles[name][(y-1)*w+x]==0x3001,(name,'blocked south-arrow approach',x,y)
            assert (x,y-1) not in {(z['x'],z['y']) for z in maps[name]['object_events']+maps[name]['bg_events']},(name,'occupied arrow approach',x,y)
        else:
            # Ladders are omnidirectional but need at least one walkable way
            # off the destination tile after arrival.
            adjacent=[(x+dx,y+dy) for dx,dy in ((0,-1),(1,0),(0,1),(-1,0))]
            assert any(0<=xx<w and 0<=yy<h and generated[yy*w+xx]==1 and tiles[name][yy*w+xx]==0x3001 for xx,yy in adjacent),(name,'ladder has no dry exit',x,y)
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
# Legacy B2F saves migrate to B1F's public component because B2F's own
# fallback can require Surf to escape. Verify the dry B1F ladder lands in the
# 1F component containing both outside exits. Runtime movement still matters.
b1=maps['UnionCave_2F'];one=maps['UnionCave_1F'];b1w,b1h=sizes['UnionCave_2F'];onew,oneh=sizes['UnionCave_1F']
b1warp=b1['warp_events'][0];assert (b1warp['dest_map'],b1warp['dest_warp_id'])==(one['id'],'0')
classes=lambda n:[0 if v&0xc00 else 2 if v>>12==1 else 1 for v in tiles[n]]
landing=one['warp_events'][0];reachable=g.flood(onew,oneh,classes('UnionCave_1F'),(landing['x'],landing['y']),False)
assert all((one['warp_events'][i]['x'],one['warp_events'][i]['y']) in reachable for i in (1,2)), 'B1F migration cannot reach both land exits'
# Exercise both positive and negative pocket contract: no one-sided entrance,
# unknown destination, unpaired warp, or missing distinct chamber is accepted.
for suffix,warp in [('Southwest',6),('Northwest',7)]:
    pocket=maps['RuinsOfAlph_'+suffix+'Pocket'];pid=pocket['id'];cid='MAP_TEST_'+suffix.upper()+'_CHAMBER'
    pocket['warp_events']=[dict(dest_map=maps['UnionCave_1F']['id'],dest_warp_id=str(warp)),dict(dest_map=cid,dest_warp_id='0')]
    maps['Test'+suffix+'Chamber']={'id':cid,'warp_events':[dict(dest_map=pid,dest_warp_id='1')]}
g.validate_pocket_warps(maps)
for pocket_name in ('RuinsOfAlph_SouthwestPocket','RuinsOfAlph_NorthwestPocket'):
    events=maps[pocket_name]['warp_events'];saved=events.pop()
    try:
        try:g.validate_pocket_warps(maps)
        except AssertionError:pass
        else:raise AssertionError(('Missing chamber was accepted',pocket_name))
    finally:events.append(saved)
    saved=events[1]['dest_warp_id'];events[1]['dest_warp_id']='99'
    try:
        try:g.validate_pocket_warps(maps)
        except AssertionError:pass
        else:raise AssertionError(('Invalid chamber return was accepted',pocket_name))
    finally:events[1]['dest_warp_id']=saved
# Even fully reciprocal entrances cannot use one shared accessible chamber,
# because that would join the two intentionally isolated outside pockets.
sw=maps['RuinsOfAlph_SouthwestPocket'];nw=maps['RuinsOfAlph_NorthwestPocket'];shared=maps['TestSouthwestChamber']
saved=dict(nw['warp_events'][1]);shared['warp_events'].append(dict(dest_map=nw['id'],dest_warp_id='1'))
nw['warp_events'][1].update(dest_map=shared['id'],dest_warp_id='1')
try:
    try:g.validate_pocket_warps(maps)
    except AssertionError as e:assert 'share a directly accessible chamber' in str(e)
    else:raise AssertionError('Shared chamber shortcut was accepted')
finally:nw['warp_events'][1]=saved;shared['warp_events'].pop()
print('PASS: isolated reference-shaped floor blueprint, retained warp indices, reciprocal ladders, safe masks and pocket guard negative cases. Not linked or emulator-tested.')
