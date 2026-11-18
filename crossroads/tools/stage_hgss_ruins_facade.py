#!/usr/bin/env python3
"""Stage donor hall facade on a private Ruins layout; never modify live maps.

Integration requires a new appended layout ID, Continue migration and emulator
validation; this function intentionally does not activate any of those changes.
"""
import copy
import hashlib
import io
import json
import struct
from pathlib import Path
from PIL import Image
from tileset_registration import upsert

ROOT=Path(__file__).resolve().parents[2]
DONOR=ROOT/'crossroads/donor/hns-ruins-outside'
WEST=ROOT/'data/tilesets/secondary/western_city'
OUT='data/tilesets/secondary/hgss_ruins_public'
NAME='HgssRuinsPublic'
FOOTPRINT=(13,12,3,4)
DOOR=(14,15)


def readwords(path):
    data=path.read_bytes();assert len(data)%2==0
    return list(struct.unpack('<%dH'%(len(data)//2),data))


def pack(v):return struct.pack('<%dH'%len(v),*v)


def derive_layout(original):
    """Return a distinct layout definition; caller must append it and copy border."""
    assert original['id']=='LAYOUT_RUINS_OF_ALPH'
    new=copy.deepcopy(original)
    new.update(id='LAYOUT_HGSS_RUINS_OF_ALPH',name='HgssRuinsOfAlph_Layout',
               secondary_tileset='gTileset_HgssRuinsPublic',
               border_filepath='data/layouts/HgssRuinsOfAlph/border.bin',
               blockdata_filepath='data/layouts/HgssRuinsOfAlph/map.bin')
    return new


def stage(write, original_map, original_tiles, border, read=None):
    if read is None:
        read = lambda path: (ROOT/path).read_text()
    manifest=json.loads((DONOR/'source-sha256.json').read_text())
    assert manifest['revision']=='167aa6d537b109bb229c231ddce4616974c4da71'
    for path, digest in manifest['files'].items():
        assert hashlib.sha256((DONOR/path).read_bytes()).hexdigest()==digest,path
    assert original_map['name']=='RuinsOfAlph' and len(original_tiles)==40*36
    assert len(original_map['warp_events'])==2
    occupied={(e['x'],e['y']) for group in ('warp_events','object_events','bg_events') for e in original_map[group]}
    x0,y0,w,h=FOOTPRINT
    footprint={(x,y) for y in range(y0,y0+h) for x in range(x0,x0+w)}
    assert not footprint.intersection(occupied), 'Facade covers an existing map event'
    src=DONOR/'data';pri=src/'tilesets/primary/johto_north_east_hns';sec=src/'tilesets/secondary/ruins_of_alph_outside_hns'
    source_map=readwords(src/'layouts/RuinsOfAlph_Outside_hns/map.bin')
    sm=[readwords(pri/'metatiles.bin'),readwords(sec/'metatiles.bin')]
    sa=[readwords(pri/'metatile_attributes.bin'),readwords(sec/'metatile_attributes.bin')]
    crop=[source_map[y*46+x] for y in range(18,22) for x in range(20,23)]
    assert len(set(v&1023 for v in crop))==12
    def donor_meta(i):
        k=int(i>=640); j=i-640*k
        return sm[k][8*j:8*j+8],sa[k][j]
    refs=[a for cell in crop for a in donor_meta(cell&1023)[0]]
    donor_tiles=sorted({a&1023 for a in refs});donor_banks=sorted({a>>12 for a in refs})
    assert len(donor_tiles)==59 and donor_banks==[0,1,5]
    mm=readwords(WEST/'metatiles.bin');ma=readwords(WEST/'metatile_attributes.bin')
    assert len(mm)==len(ma)*8 and len(ma)==490
    used_meta={v&1023 for v in list(original_tiles)+list(border) if v&1023>=512}
    assert all(v-512<len(ma) for v in used_meta)
    used_words=[w for index in used_meta for w in mm[(index-512)*8:(index-512)*8+8]]
    used_tiles={w&1023 for w in used_words if w&1023>=512}
    primary=readwords(ROOT/'data/tilesets/primary/general/metatiles.bin')
    primary_meta={v&1023 for v in list(original_tiles)+list(border) if v&1023<512}
    primary_words=[w for index in primary_meta for w in primary[index*8:index*8+8]]
    used_banks={w>>12 for w in used_words+primary_words}
    assert not used_banks.intersection({7,8,9}),('Occupied BG palette bank',used_banks)
    # Slateport's live callback overwrites secondary slots 224–227.
    used_tiles.update(range(512+224,512+228))
    free_tiles=[i for i in range(512,1024) if i not in used_tiles]
    assert len(free_tiles)>=len(donor_tiles)
    tilemap=dict(zip(donor_tiles,free_tiles));bankmap={0:7,1:8,5:9}
    sheets=[Image.open(pri/'tiles.png'),Image.open(sec/'tiles.png')]
    sheet=Image.open(WEST/'tiles.png').copy();assert sheet.mode=='P' and sheet.size==(128,256)
    for old,new in tilemap.items():
        k=int(old>=640);i=old-640*k; src_image=sheets[k]
        assert src_image.mode=='P' and i//16*8+8<=src_image.height
        image=src_image.crop(((i%16)*8,(i//16)*8,(i%16+1)*8,(i//16+1)*8))
        j=new-512;sheet.paste(image,((j%16)*8,(j//16)*8))
    out=io.BytesIO();sheet.save(out,format='PNG',optimize=False);write(OUT+'/tiles.png',out.getvalue())
    for i in range(16):
        srcpath=(pri/'palettes'/f'{next(k for k,v in bankmap.items() if v==i):02}.pal') if i in bankmap.values() else (WEST/'palettes'/f'{i:02}.pal')
        write(OUT+f'/palettes/{i:02}.pal',srcpath.read_bytes())
    converted=[]
    for n,cell in enumerate(crop):
        words,attr=donor_meta(cell&1023)
        mm += [tilemap[a&1023]|(a&0xc00)|(bankmap[a>>12]<<12) for a in words]
        ma.append(attr)
        converted.append((cell&0xfc00)|(512+490+n))
    write(OUT+'/metatiles.bin',pack(mm));write(OUT+'/metatile_attributes.bin',pack(ma))
    sections={
        'graphics':f'const u32 gTilesetTiles_{NAME}[] = INCGFX_U32("{OUT}/tiles.png", ".4bpp.fastSmol");\n'
        f'const u16 gTilesetPalettes_{NAME}[][16] = {{\n'+''.join(f'    INCGFX_U16("{OUT}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n',
        'metatiles':f'const u16 gMetatiles_{NAME}[] = INCBIN_U16("{OUT}/metatiles.bin");\nconst u16 gMetatileAttributes_{NAME}[] = INCBIN_U16("{OUT}/metatile_attributes.bin");\n',
        'headers':f'const struct Tileset gTileset_{NAME} = {{ .isCompressed=TRUE, .isSecondary=TRUE, .tiles=gTilesetTiles_{NAME}, .palettes=gTilesetPalettes_{NAME}, .metatiles=gMetatiles_{NAME}, .metatileAttributes=gMetatileAttributes_{NAME}, .callback=InitTilesetAnim_Slateport }};\n',
        'externs':f'extern const struct Tileset gTileset_{NAME};\n'}
    for kind,path in [('graphics','src/data/tilesets/graphics.h'),('metatiles','src/data/tilesets/metatiles.h'),('headers','src/data/tilesets/headers.h'),('externs','include/tilesets.h')]:
        begin='// BEGIN HGSS RUINS PUBLIC PRIVATE';end='// END HGSS RUINS PUBLIC PRIVATE'
        body=begin+'\n#if !IS_FRLG\n'+sections[kind]+'#endif\n'+end
        write(path,upsert(read(path),begin,end,body,externs=kind=='externs'))
    newtiles=original_tiles.copy()
    for i,value in enumerate(converted):newtiles[(y0+i//w)*40+x0+i%w]=value
    updated=copy.deepcopy(original_map)
    updated['layout']='LAYOUT_HGSS_RUINS_OF_ALPH'
    updated['warp_events'].append(dict(x=DOOR[0],y=DOOR[1],elevation=0,dest_map='MAP_RUINS_OF_ALPH_HALL_ENTRANCE',dest_warp_id='0'))
    # The exact 12-cell changed footprint is the Continue migration input.
    assert {(i%40,i//40) for i,(a,b) in enumerate(zip(original_tiles,newtiles)) if a!=b}==footprint
    return updated,newtiles,footprint
