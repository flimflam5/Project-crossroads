#!/usr/bin/env python3
"""Convert pinned HNS Union Cave floors to isolated Emerald-indexed preview.

Outputs only to an explicit external directory. Does not register live maps,
copy donor events, modify saves, or claim collision/visual correctness.
"""
from pathlib import Path
import argparse, hashlib, json, struct
from collections import Counter
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'crossroads/donor/hns-union-cave'
REV = '167aa6d537b109bb229c231ddce4616974c4da71'
FLOORS = {'UnionCave_1F_hns':(48,60), 'UnionCave_B1F_hns':(48,48), 'UnionCave_B2F_hns':(40,50)}

def words(p):
    b=p.read_bytes()
    assert len(b)%2==0
    return list(struct.unpack('<%dH'%(len(b)//2),b))
def pack(x): return struct.pack('<%dH'%len(x),*x)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args(); target=args.output.resolve()
    assert not target.is_relative_to(ROOT), 'Preview must stay outside game source'
    manifest=json.loads((SOURCE/'source-sha256.json').read_text())
    assert manifest['revision']==REV
    for path,expected in manifest['files'].items():
        assert len(expected)==64 and hashlib.sha256((SOURCE/path).read_bytes()).hexdigest()==expected, path
    root=SOURCE/'data'; pri=root/'tilesets/primary/johto_general_hns'; sec=root/'tilesets/secondary/cave_default_hns'
    ma=[words(pri/'metatiles.bin'),words(sec/'metatiles.bin')];attrs=[words(pri/'metatile_attributes.bin'),words(sec/'metatile_attributes.bin')]
    assert len(ma[0])==640*8 and len(ma[1])==306*8
    floors={n:words(root/'layouts'/n/'map.bin') for n in FLOORS}
    for name,(w,h) in FLOORS.items(): assert len(floors[name])==w*h
    allids=sorted({v&1023 for values in floors.values() for v in values})
    assert len(allids)==89 and len(allids)<512
    def srcmeta(i):
        k=int(i>=640); n=i-640 if k else i
        assert n < len(attrs[k]);return ma[k][8*n:8*n+8],attrs[k][n]
    refs=[v for i in allids for v in srcmeta(i)[0]]
    tileids=sorted({v&1023 for v in refs});banks=sorted({v>>12 for v in refs})
    assert len(tileids)==161 and len(tileids)<512 and banks==[0,4,6,8,9,10]
    imap={v:i for i,v in enumerate(allids)}; tmap={v:i for i,v in enumerate(tileids)}; pmap={v:i for i,v in enumerate(banks)}
    sheets=[Image.open(pri/'tiles.png'),Image.open(sec/'tiles.png')]
    assert all(im.mode=='P' for im in sheets)
    target.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('P',(128,((len(tileids)+15)//16)*8));sheet.putpalette(sheets[0].getpalette())
    for old,new in tmap.items():
        k=int(old>=640); n=old-640 if k else old; s=sheets[k];assert n < (s.width//8)*(s.height//8)
        tile=s.crop(((n%16)*8,(n//16)*8,(n%16)*8+8,(n//16)*8+8));sheet.paste(tile,((new%16)*8,(new//16)*8))
        assert sheet.crop(((new%16)*8,(new//16)*8,(new%16)*8+8,(new//16)*8+8)).tobytes()==tile.tobytes()
    sheet.save(target/'tiles.png',optimize=False)
    palettes=target/'palettes';palettes.mkdir(exist_ok=True)
    for source,dest in pmap.items():
        path=(pri if source<7 else sec)/f'palettes/{source:02}.pal';(palettes/f'{dest:02}.pal').write_bytes(path.read_bytes())
    newmeta=[tmap[v&1023]|(v&0xc00)|(pmap[v>>12]<<12) for v in refs];newattrs=[srcmeta(i)[1] for i in allids]
    (target/'metatiles.bin').write_bytes(pack(newmeta));(target/'metatile_attributes.bin').write_bytes(pack(newattrs))
    reports={}
    for name,(w,h) in FLOORS.items():
        floor=floors[name];out=[(v&0xfc00)|imap[v&1023] for v in floor];(target/(name+'.bin')).write_bytes(pack(out))
        assert all((a&0xfc00)==(b&0xfc00) and srcmeta(a&1023)[1]==newattrs[b&1023] for a,b in zip(floor,out))
        mapjson=json.loads((root/'maps'/name/'map.json').read_text())
        warps=[]
        for event in mapjson['warp_events']:
            x,y=event['x'],event['y'];assert 0<=x<w and 0<=y<h
            v=floor[y*w+x];warps.append(dict(x=x,y=y,destination=event['dest_map'],destination_warp=event['dest_warp_id'],behavior=srcmeta(v&1023)[1]&255,collision=(v>>10)&3,elevation=v>>12))
        reports[name]=dict(width=w,height=h,cell_count=len(floor),warp_events=warps,collision_histogram=dict(Counter(str((x>>10)&3) for x in floor)),elevation_histogram=dict(Counter(str(x>>12) for x in floor)))
    result=dict(revision=REV,tiles=len(tileids),metatiles=len(allids),palette_banks=banks,floors=reports,behavior_codes=sorted({x&255 for x in newattrs}),limitations=['Preview only; no live map or warp registration.', 'Donor geography, warp placement and old save migration not validated in engine.', 'Does not include animation callbacks or map events.', 'Offline pixel checks do not prove graphics priority or collision.'])
    (target/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Converted three Union Cave floors:',sum(len(v) for v in floors.values()),'cells;',len(allids),'metatiles,',len(tileids),'graphics,',len(banks),'palette banks. PREVIEW ONLY.')
if __name__=='__main__':main()
