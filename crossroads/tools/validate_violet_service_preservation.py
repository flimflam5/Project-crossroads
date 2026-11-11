#!/usr/bin/env python3
"""Pin untouched Violet service maps to their actual pre-change source."""
import json, subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2]
BASE='3f935d5e8600c5a280b9172b555edb35ca52b6c0'
def validate():
    def old(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R)
    c=json.loads((R/'crossroads/hgss/contracts/violet-services-qa09.json').read_text())
    assert c['source_commit']==BASE
    before={l['id']:l for l in json.loads(old('data/layouts/layouts.json'))['layouts']}
    after={l['id']:l for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
    assert {r['map']['name'] for r in c['rooms']}=={'VioletCity_PokemonCenter_1F','VioletCity_PokemonCenter_B1F','VioletCity_Mart'}
    for row in c['rooms']:
        m,l=row['map'],row['layout'];p=f"data/maps/{m['name']}/map.json"
        assert m==json.loads(old(p))==json.loads((R/p).read_text())
        assert l==before[m['layout']]==after[m['layout']]
        for path,key in [(l['blockdata_filepath'],'raw_hex'),(l['border_filepath'],'border_hex')]:
            assert bytes.fromhex(row[key])==old(path)==(R/path).read_bytes(),(m['name'],path)
    print('Unrelated Violet services: exact immutable map/layout/actor/warp/room/border preservation PASS')
if __name__=='__main__':validate()
