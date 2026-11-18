#!/usr/bin/env python3
"""Validate installed Union Cave against pinned HGSS anchor components.

This is a static component/elevation check, not normal movement or Surf QA.
"""
import json
import subprocess
from pathlib import Path
import build_hgss_union_cave as g

R=Path(__file__).resolve().parents[2]
def load(path):return json.loads((R/path).read_text())

def validate():
    facts=load('crossroads/hgss/canonical_events/union-cave-geometry.json')
    plan=load('crossroads/donor/hns-union-cave/hgss-corrected-warp-plan.json')
    layouts={e['id']:e for e in load('data/layouts/layouts.json')['layouts']}
    maps={n:load(f'data/maps/{n}/map.json') for n in g.FLOORS}
    groups=load('data/maps/map_groups.json')['gMapGroup_CrossroadsOlivine']
    for index,name in ((53,'RuinsOfAlph'),(89,'UnionCave_1F'),(90,'UnionCave_2F'),(91,'UnionCave_3F')):
        assert groups[index]==name,('Existing map ID changed',name,index)
    legacy={
        'UnionCave_1F':[('MAP_UNION_CAVE_2_F',0),('MAP_JOHTO_ROUTE32',0),('MAP_JOHTO_ROUTE33',0)],
        'UnionCave_2F':[('MAP_UNION_CAVE_1_F',0),('MAP_UNION_CAVE_3_F',0)],
        'UnionCave_3F':[('MAP_UNION_CAVE_2_F',1)]}
    for name,expected in legacy.items():
        actual=[(e['dest_map'],int(e['dest_warp_id'])) for e in maps[name]['warp_events'][:len(expected)]]
        assert actual==expected,('Legacy warp destination/index changed',name,actual)
    old_heals=json.loads(subprocess.check_output(['git','show','822e46164f:src/data/heal_locations.json'],cwd=R,text=True))
    assert load('src/data/heal_locations.json')==old_heals,'Heal IDs or heal definitions changed'
    for name,reference in g.FLOORS.items():
        m=maps[name];layout=layouts[m['layout']]
        assert m['layout']==g.NEW_LAYOUTS[name]
        old=layouts['LAYOUT_UNION_CAVE_'+name[-2]+'_F']
        assert (old['width'],old['height'])==(28,22)
        assert old['blockdata_filepath']!=layout['blockdata_filepath']
        assert len((R/old['blockdata_filepath']).read_bytes())==28*22*2
        fact=facts[reference];w,h,permissions=g.reference_planes(fact)
        assert (layout['width'],layout['height'])==(w,h)
        values=g.read16(R/layout['blockdata_filepath']);assert len(values)==w*h
        classes=[0 if v&0xc00 else 2 if v>>12==1 else 1 for v in values]
        for e in m['object_events']:classes[e['y']*w+e['x']]=0
        expected=[0 if v&0x8000 else 2 if v&255==0x15 else 1 for v in permissions]
        entries=[e for e in plan['warps'] if e['existing_map']==name]
        assert len(entries)==len(m['warp_events'])
        for e in entries:
            event=m['warp_events'][e['proposed_index']]
            assert (event['x'],event['y'])==(e['hgss_x'],e['hgss_y'])
            destination=e['destination'];target_index=e['destination_index']
            if e['proposed_index'] in g.POCKETS.get(name,{}):
                destination,target_index=g.POCKETS[name][e['proposed_index']]
            target=load(f'data/maps/{destination}/map.json')
            assert (event['dest_map'],int(event['dest_warp_id']))==(target['id'],target_index), (name,e['proposed_index'],'destination changed')
            back=target['warp_events'][target_index]
            assert (back['dest_map'],int(back['dest_warp_id']))==(m['id'],e['proposed_index']), (name,e['proposed_index'],'missing reciprocal target')
            raw=values[event['y']*w+event['x']]
            assert raw in (0x3005,0x3006)
            if raw==0x3006:
                assert event['y']>0 and values[(event['y']-1)*w+event['x']]==0x3001
        for i,e in enumerate(fact['warps']):
            p=(e['x'],e['z'])
            for water in (False,True):
                actual=g.flood(w,h,classes,p,water);source=g.flood(w,h,expected,p,water)
                anchors=lambda component:{j for j,v in enumerate(fact['warps']) if (v['x'],v['z']) in component}
                assert anchors(actual)==anchors(source),(name,i,water,anchors(actual),anchors(source))
    print('Installed Union Cave: append-only layouts, all HGSS anchors and exact dry/Surf-permissive reference components PASS; emulator testing pending.')
    return set(g.FLOORS)

if __name__=='__main__':validate()
