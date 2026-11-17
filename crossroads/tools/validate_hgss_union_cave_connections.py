#!/usr/bin/env python3
"""Verify proposed HGSS connector graph and preserve existing cave warp IDs.

Reference facts from pinned pret/pokeheartgold event data. This is a source
plan; it neither installs gameplay maps nor proves Surf or runtime movement.
"""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[2]
D=R/'crossroads/donor/hns-union-cave'
def read(path):return json.loads(path.read_text())
plan=read(D/'hgss-corrected-warp-plan.json')
manifest=read(D/'hgss-reference/sha256.json')
assert plan['pret_revision']==manifest['revision']=='6bf138d6035aa6b43d6f8f4132a12df70f86dcec'
for name,expected in manifest['files'].items():assert hashlib.sha256((D/'hgss-reference'/name).read_bytes()).hexdigest()==expected,name
files={'UnionCave_1F':'096_D25R0101.json','UnionCave_2F':'148_D25R0102.json','UnionCave_3F':'149_D25R0103.json'}
headers={'UnionCave_1F':'MAP_UNION_CAVE_1F','UnionCave_2F':'MAP_UNION_CAVE_B1F','UnionCave_3F':'MAP_UNION_CAVE_B2F','JohtoRoute32':'MAP_ROUTE_32','JohtoRoute33':'MAP_ROUTE_33','RuinsOfAlph':'MAP_RUINS_OF_ALPH'}
proposed={(e['existing_map'],e['proposed_index']):e for e in plan['warps']}
assert len(proposed)==18
for name,filename in files.items():
    ref=read(D/'hgss-reference'/filename)['warps'];p=[e for e in plan['warps'] if e['existing_map']==name]
    assert sorted(e['hgss_anchor'] for e in p)==list(range(len(ref)))
    for e in p:
        src=ref[e['hgss_anchor']]
        assert (e['hgss_x'],e['hgss_y'],headers[e['destination']])==(src['x'],src['z'],src['header']),e
        if e['destination'] in files:
            dest=proposed[(e['destination'],e['destination_index'])]
            assert src['anchor']==dest['hgss_anchor'],e
            assert (dest['destination'],dest['destination_index'])==(name,e['proposed_index']),e
# Three donor baselines: existing six map-index destinations stay exact.
baseline=read(D/'warp-mapping.json')
for floor in baseline['floors']:
    current=read(R/'data/maps'/floor['existing_map']/'map.json')
    for e in floor['warp_mapping']:
        if e.get('new'):continue
        old=current['warp_events'][e['existing_index']]
        assert (old['dest_map'],int(old['dest_warp_id']))==(e['destination'],e['destination_index'])
        new=proposed[(floor['existing_map'],e['existing_index'])]
        assert new['destination_index']==e['destination_index']
        assert new['destination'] in headers
outside=read(D/'hgss-reference/110_D24R0101.json')['warps']
for anchor,local,ret in [(15,(3,52),6),(16,(3,33),7)]:
    e=outside[anchor];assert (e['x']-416,e['z']-256)==local
    assert (e['header'],e['anchor'])==('MAP_UNION_CAVE_1F',ret)
# Connector components established by pinned HGSS terrain inspection. The
# second B2F segment includes water and requires real Surf verification.
assert proposed[('UnionCave_2F',3)]['destination_index']==1
assert proposed[('UnionCave_3F',3)]['destination_index']==5
assert proposed[('UnionCave_1F',7)]['hgss_anchor']==7
assert proposed[('UnionCave_2F',4)]['destination_index']==2
assert proposed[('UnionCave_3F',4)]['destination_index']==4
assert proposed[('UnionCave_1F',6)]['hgss_anchor']==6
# Test HGSS terrain components conservatively, treating permission bit 0x8000
# as blocked and 0x15 as water. This is not a movement/Surf implementation:
# ledges, elevations, collision objects and event scripts are not simulated.
from collections import deque
geometry=read(R/'crossroads/hgss/canonical_events/union-cave-geometry.json')
def component(mapname,anchor,allow_water):
    a=geometry[mapname];cols,rows=a['matrix_dimensions'];w,h=cols*32,rows*32
    plane=[0]*(w*h)
    for k,c in enumerate(a['chunks']):
        ox=(k%cols)*32;oy=(k//cols)*32
        for i,value in enumerate(c['permissions']):plane[(oy+i//32)*w+ox+i%32]=value
    e=a['warps'][anchor];start=(e['x'],e['z']);q=deque([start]);seen={start}
    while q:
        x,y=q.popleft()
        for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if not (0<=nx<w and 0<=ny<h) or (nx,ny) in seen:continue
            value=plane[ny*w+nx]
            if value&0x8000 or (not allow_water and value&255==0x15):continue
            seen.add((nx,ny));q.append((nx,ny))
    return {i for i,e in enumerate(a['warps']) if (e['x'],e['z']) in seen}
assert component('MAP_UNION_CAVE_1F',4,False)=={4,6}
assert component('MAP_UNION_CAVE_1F',5,False)=={5,7}
assert component('MAP_UNION_CAVE_B2F',2,False)=={2,4}
assert component('MAP_UNION_CAVE_B2F',1,False)=={1}
assert component('MAP_UNION_CAVE_B2F',1,True)=={1,3}
assert component('MAP_UNION_CAVE_B2F',0,True)=={0}
print('PASS: pinned HGSS anchors, 18 proposed indexed exits, 6 preserved old indices and distinct 1F/B2F connector components. Static graph only; actual Surf/visual/emulator untested.')
