#!/usr/bin/env python3
"""Convert pinned donor Ruins tiles to an isolated Emerald-mode preview.

This writes no playable maps and does not copy donor events. It is a packing
probe; HGSS geography, engine behaviors, palette loading and animation need
separate reconstruction and runtime testing.
"""
from pathlib import Path
from collections import Counter
import argparse, hashlib, json, struct
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'crossroads/donor/hns-ruins-outside'
REV='167aa6d537b109bb229c231ddce4616974c4da71'

def words(path):
    data=path.read_bytes(); assert len(data)%2==0, path
    return list(struct.unpack('<%dH'%(len(data)//2),data))
def pack(values): return struct.pack('<%dH'%len(values),*values)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',type=Path,required=True)
    target=ap.parse_args().output.resolve()
    assert not target.is_relative_to(ROOT), 'Output must be outside game source'
    source=json.loads((SOURCE/'source-sha256.json').read_text());assert source['revision']==REV
    for path,expected in source['files'].items():
        assert hashlib.sha256((SOURCE/path).read_bytes()).hexdigest()==expected,path
    data=SOURCE/'data';pri=data/'tilesets/primary/johto_north_east_hns';sec=data/'tilesets/secondary/ruins_of_alph_outside_hns'
    ma=[words(pri/'metatiles.bin'),words(sec/'metatiles.bin')]
    attrs=[words(pri/'metatile_attributes.bin'),words(sec/'metatile_attributes.bin')]
    cells=words(data/'layouts/RuinsOfAlph_Outside_hns/map.bin');assert len(cells)==46*48
    assert len(ma[0])==640*8 and len(ma[1])==186*8
    used=sorted({v&1023 for v in cells}); assert len(used)==189 and len(used)<512
    def source_meta(index):
        k=int(index>=640); j=index-640 if k else index
        assert j<len(attrs[k]);return ma[k][j*8:j*8+8],attrs[k][j]
    refs=[v for index in used for v in source_meta(index)[0]]
    tileids=sorted({v&1023 for v in refs});banks=sorted({v>>12 for v in refs})
    assert len(tileids)==317 and len(tileids)<512 and banks==[0,1,2,3,5,6,7,8]
    imap={v:i for i,v in enumerate(used)};tmap={v:i for i,v in enumerate(tileids)};pmap={v:i for i,v in enumerate(banks)}
    sheets=[Image.open(pri/'tiles.png'),Image.open(sec/'tiles.png')];assert all(im.mode=='P' for im in sheets)
    target.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('P',(128,((len(tileids)+15)//16)*8));sheet.putpalette(sheets[0].getpalette())
    for old,new in tmap.items():
        k=int(old>=640);n=old-640 if k else old;s=sheets[k]
        assert n<(s.width//8)*(s.height//8)
        tile=s.crop(((n%16)*8,(n//16)*8,(n%16)*8+8,(n//16)*8+8));sheet.paste(tile,((new%16)*8,(new//16)*8))
        assert sheet.crop(((new%16)*8,(new//16)*8,(new%16)*8+8,(new//16)*8+8)).tobytes()==tile.tobytes()
    sheet.save(target/'primary-tiles.png',optimize=False)
    palettes=target/'palettes';palettes.mkdir(exist_ok=True)
    for old,new in pmap.items():
        path=(pri if old<7 else sec)/f'palettes/{old:02}.pal';(palettes/f'{new:02}.pal').write_bytes(path.read_bytes())
    newmeta=[tmap[v&1023]|(v&0xc00)|(pmap[v>>12]<<12) for v in refs]
    newattrs=[source_meta(i)[1] for i in used]
    (target/'metatiles.bin').write_bytes(pack(newmeta));(target/'metatile_attributes.bin').write_bytes(pack(newattrs))
    converted=[(v&0xfc00)|imap[v&1023] for v in cells]
    (target/'map.bin').write_bytes(pack(converted))
    assert all((a&0xfc00)==(b&0xfc00) and source_meta(a&1023)[1]==newattrs[b&1023] for a,b in zip(cells,converted))
    m=json.loads((data/'maps/RuinsOfAlph_Outside_hns/map.json').read_text())
    warps=[]
    for i,e in enumerate(m['warp_events']):
        x,y=e['x'],e['y'];assert 0<=x<46 and 0<=y<48
        v=cells[y*46+x];warps.append(dict(index=i,x=x,y=y,dest_map=e['dest_map'],dest_warp_id=e['dest_warp_id'],behavior=source_meta(v&1023)[1]&255,collision=(v>>10)&3,elevation=v>>12))
    report=dict(revision=REV,width=46,height=48,cell_count=len(cells),metatiles=len(used),graphics=len(tileids),source_palette_banks=banks,emerald_palette_banks=pmap,warps=warps,collision_histogram=dict(Counter(str((x>>10)&3) for x in cells)),elevation_histogram=dict(Counter(str(x>>12) for x in cells)),limitations=['Data-only preview; no game content imported.', 'Eight palettes require a primary/secondary palette split at six banks; this exporter does not register tilesets.', 'HGSS outdoor is 32x64; donor is 46x48 and needs geographic reconstruction.', 'Donor direct B1F exits omit HGSS 1F and B2F connector pockets.', 'Animation, water, layers, movement, interiors and emulator untested.'])
    (target/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Ruins outside preview:',len(cells),'cells;',len(used),'metatiles,',len(tileids),'graphics,',len(banks),'palette banks. NO GAME INTEGRATION.')
if __name__=='__main__': main()
