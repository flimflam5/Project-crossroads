#!/usr/bin/env python3
"""Static comparison for a staged Ruins entrance; does not claim playtesting."""
import json
import io
import struct
from PIL import Image
from pathlib import Path
from stage_hgss_ruins_facade import stage, readwords, FOOTPRINT, DOOR
from stage_hgss_ruins_network import flood


def check():
    root=Path(__file__).resolve().parents[2]
    original=json.loads((root/'data/maps/RuinsOfAlph/map.json').read_text())
    tiles=readwords(root/'data/layouts/RuinsOfAlph/map.bin')
    border=readwords(root/'data/layouts/RuinsOfAlph/border.bin')
    writes={}
    def write(path, data):
        assert path not in writes
        writes[path]=data
    new, plane, footprint=stage(write,original,tiles,border)
    assert len(writes)==23
    def words(data):return struct.unpack('<%dH'%(len(data)//2),data)
    src=root/'crossroads/donor/hns-ruins-outside/data'
    source_cells=readwords(src/'layouts/RuinsOfAlph_Outside_hns/map.bin')
    primary=src/'tilesets/primary/johto_north_east_hns'
    secondary=src/'tilesets/secondary/ruins_of_alph_outside_hns'
    source_meta=[readwords(primary/'metatiles.bin'),readwords(secondary/'metatiles.bin')]
    source_imgs=[Image.open(primary/'tiles.png'),Image.open(secondary/'tiles.png')]
    output_meta=words(writes['data/tilesets/secondary/hgss_ruins_public/metatiles.bin'])
    output_img=Image.open(io.BytesIO(writes['data/tilesets/secondary/hgss_ruins_public/tiles.png']))
    palette_map={0:7,1:8,5:9}
    for n,(x,y) in enumerate((x,y) for y in range(18,22) for x in range(20,23)):
        i=source_cells[y*46+x]&1023; k=int(i>=640);i-=640*k
        old=source_meta[k][i*8:i*8+8]; rewritten=output_meta[(490+n)*8:(491+n)*8]
        for a,b in zip(old,rewritten):
            assert a&0xc00==b&0xc00 and b>>12==palette_map[a>>12]
            old_tile=a&1023; old_part=int(old_tile>=640);old_tile-=640*old_part
            new_tile=(b&1023)-512
            def crop(im,index):
                return im.crop(((index%16)*8,(index//16)*8,(index%16+1)*8,(index//16+1)*8)).tobytes()
            assert crop(source_imgs[old_part],old_tile)==crop(output_img,new_tile)
    assert new['warp_events'][:2]==original['warp_events']
    assert new['warp_events'][2]==dict(x=DOOR[0],y=DOOR[1],elevation=0,
        dest_map='MAP_RUINS_OF_ALPH_HALL_ENTRANCE',dest_warp_id='0')
    for k in ('object_events','bg_events','coord_events','connections'):
        assert new[k]==original[k],k
    assert len(footprint)==FOOTPRINT[2]*FOOTPRINT[3]
    reach=flood(plane,40,36,(DOOR[0],DOOR[1]+1))
    assert DOOR in reach
    assert all((w['x'],w['y']) in reach for w in original['warp_events'])
    assert any((x,0) in reach for x in range(40))
    assert any((39,y) in reach for y in range(36))
    assert any((x,DOOR[1]+1) in reach for x in (DOOR[0]-1,DOOR[0]+1))
    return writes,new,plane,footprint


if __name__=='__main__':
    assert check()==check()
    print('Staged facade: unchanged events, reciprocal target, dry exit/boundary reachability, deterministic output pass. No movement or rendering test.')
