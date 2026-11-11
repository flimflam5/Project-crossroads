#!/usr/bin/env python3
"""Check the actual engine resource pointers for every two-city map cell.

Palette files existing on disk does not mean the engine loads their banks.
This regression catches the unsupported bank13 Mart prototype before a build.
"""
import functools,json,re,struct
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2]
def load(p):return json.loads((R/p).read_text())
headers=(R/'src/data/tilesets/headers.h').read_text()
meta_source=(R/'src/data/tilesets/metatiles.h').read_text()
graphic_source=(R/'src/data/tilesets/graphics.h').read_text()
limit=int(re.search(r'#define\s+NUM_PALS_TOTAL\s+(\d+)',(R/'include/fieldmap.h').read_text())[1])
@functools.lru_cache(None)
def resource(symbol):
    body=re.search(r'const struct Tileset\s+'+re.escape(symbol)+r'\s*=\s*\{(.*?)\};',headers,re.S)[1]
    meta=re.search(r'\.metatiles\s*=\s*(\w+)',body)[1]
    sheet=re.search(r'\.tiles\s*=\s*(\w+)',body)[1]
    p=re.search(re.escape(meta)+r'\[\]\s*=\s*INCBIN_U16\("([^"]+)"',meta_source)[1]
    q=re.search(re.escape(sheet)+r'\[\]\s*=\s*INCGFX_U32\("([^"]+)"',graphic_source)[1]
    b=(R/p).read_bytes();im=Image.open(R/q)
    assert im.mode=='P' and im.size==(128,256) and max(im.tobytes())<16,(symbol,'Invalid native graphic sheet')
    return struct.unpack('<'+str(len(b)//2)+'H',b)
def validate():
    names={r['map'] for r in load('crossroads/hgss/ecruteak-qa09-building-checklist.json')['maps']}
    names|={p.parent.name for p in (R/'data/maps').glob('OlivineCity*/map.json')}
    assert len(names)==51
    layouts={l['id']:l for l in load('data/layouts/layouts.json')['layouts']};checked=0
    for name in sorted(names):
        m=load(f'data/maps/{name}/map.json');l=layouts[m['layout']]
        pool=[resource(l[k]) for k in ['primary_tileset','secondary_tileset']]
        for path in [l['blockdata_filepath'],l['border_filepath']]:
            b=(R/path).read_bytes()
            for cell in struct.unpack('<'+str(len(b)//2)+'H',b):
                n=cell&1023;refs=pool[n>=512][n%512*8:n%512*8+8]
                assert len(refs)==8,(name,'Unallocated metatile',n)
                for v in refs:assert v>>12<limit,(name,'Palette bank is never loaded by engine',n,v>>12)
                checked+=1
    print('Actual two-city tileset pointers, native4bpp bounds and loaded palette banks0–12: PASS',len(names),'maps,',checked,'cells')
if __name__=='__main__':validate()
