#!/usr/bin/env python3
"""Exercise draft Ruins topology; this is not an engine movement test."""
from stage_hgss_ruins_network import stage, NAMES, IDS, SIZES


def run():
    writes={}
    def write(path, value):
        assert path not in writes
        writes[path]=value
    maps,tiles,scripts=stage(write)
    assert tuple(maps)==NAMES
    by_id={m['id']:m for m in maps.values()}
    for name, m in maps.items():
        for i,e in enumerate(m['warp_events']):
            if e['dest_map'] not in by_id:
                assert (name,i,e['dest_map'],int(e['dest_warp_id'])) in (
                    (NAMES[0],0,'MAP_UNION_CAVE_1_F',6),
                    (NAMES[1],0,'MAP_UNION_CAVE_1_F',7),
                    (NAMES[5],0,'MAP_RUINS_OF_ALPH',2))
                continue
            target=by_id[e['dest_map']]['warp_events'][int(e['dest_warp_id'])]
            assert target['dest_map']==m['id'] and int(target['dest_warp_id'])==i
        assert len(tiles[name])==SIZES[NAMES.index(name)][0]*SIZES[NAMES.index(name)][1]
    for n in NAMES[2:4]:
        assert len(maps[n]['bg_events'])==1
        assert scripts[n].count('special DoSlidingPuzzle')==1
        assert 'setflag' not in scripts[n] and 'giveitem' not in scripts[n]
        assert 'warp MAP_RUINS_OF_ALPH_UNDERGROUND_HALL' in scripts[n]
    return writes,maps,tiles,scripts

if __name__=='__main__':
    assert run()==run()
    print('Draft Ruins graph and dry paths pass; public doorway, hidden rooms and emulator behavior remain unverified.')
