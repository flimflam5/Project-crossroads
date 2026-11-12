#!/usr/bin/env python3
"""Compose the preserved city inventory with reviewed north-port/ship openings.

The immutable QA09 inventory remains historical. QA10 changes only the port's
physical approach and appends new ship groups; it never discards old door leaves.
"""
import argparse
import copy
import json
from pathlib import Path
import subprocess

R=Path(__file__).resolve().parents[2]
BASE='285cfa4ebddcb390a8a5bde6116748cbb5eaba6b'
DEST='crossroads/hgss/doorways-qa10.json'


def generate(check=False):
    original=json.loads(subprocess.check_output(
        ['git','show',BASE+':crossroads/hgss/doorways-qa09.json'],cwd=R))
    value=copy.deepcopy(original)
    for group in value['groups']:
        if group['label']=='olivine-port-city-entrance':
            group['outside'].update(anchor=[23,50],press=[0,1],
                arrivals=[[23,52],[24,52]],expected_facing=2)
            group['inside'].update(expected_facing=1)
        elif group['label']=='olivine-port-quay-main':
            group['outside']['expected_facing']=1
            group['inside']['expected_facing']=2
        elif group['label']=='olivine-port-inspection-side':
            group['outside']['expected_facing']=3
            group['inside']['expected_facing']=4
    ship=json.loads((R/'crossroads/hgss/qa10/ss-aqua-doorways.json').read_text())
    new=ship['groups']
    assert all(g['label']not in {v['label']for v in value['groups']}for g in new)
    value['groups']+=new
    # Independently reviewed physical intentions exist for ALL45 groups,
    # including legacy city/route gates. Never infer these from runtime output.
    intent_path=R/'crossroads/hgss/qa10/doorway-intended-facing-b4.json'
    intentions={g['label']:g for g in json.loads(intent_path.read_text())['groups']}
    assert set(intentions)=={g['label']for g in value['groups']}
    for group in value['groups']:
        physical=intentions[group['label']]
        for side in ['outside','inside']:
            expected=physical['sides'][side]
            assert group[side]['map']==expected['map']
            assert group[side]['segments']==expected['segments']
            group[side]['expected_facing']=expected['intended_arrival_facing']
    value['qa10']={
        'immutable_city_inventory_source':BASE,
        'preserved_city_groups':len(original['groups']),
        'new_ship_groups':len(new),
        'facing_numbers':{'south':1,'north':2,'west':3,'east':4},
        'all_arrival_facing_basis':'crossroads/hgss/qa10/doorway-intended-facing-b4.json',
        'note':'North-entry port changes approach/facing only; every old leaf and warp ordinal remains. Docked ship returns to Olivine; no sailing destination is added.'}
    data=(json.dumps(value,indent=2)+'\n').encode()
    path=R/DEST
    if check:
        assert path.read_bytes()==data,'Regenerate QA10 visible doorway inventory'
    elif not path.exists()or path.read_bytes()!=data:
        path.write_bytes(data)
    return value


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    v=generate(a.check)
    print('QA10 preserved city + docked ship doorway inventory:',len(v['groups']),'groups; controller/facing verification remains separate')
