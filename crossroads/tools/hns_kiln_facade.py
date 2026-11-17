"""Pack the pinned HNS Azalea charcoal-kiln facade into unused private city slots.

The donor's 640-index metatile/graphic split is translated to Emerald's 512
split. The town's prior tiles and owner Gym resources are reserved by the caller.
"""
from pathlib import Path
from PIL import Image
import hashlib,json,struct

R=Path(__file__).resolve().parents[2]
D=R/'crossroads/donor/hns_azalea_exterior/data'
ORIGIN=(19,30)
DOOR=(20,33)

def _u16(path):
    b=path.read_bytes()
    return struct.unpack('<%dH'%(len(b)//2),b)

def augment(metas, attrs, sheets, protected, banks, secondary_ids, gym_meta):
    root=D.parent
    manifest=json.loads((root/'provenance.json').read_text())
    for item in manifest['source_manifest']:
        assert hashlib.sha256((root/item['path']).read_bytes()).hexdigest()==item['sha256'],item['path']
    source_paths=[D/'tilesets/primary/johto_south_hns',D/'tilesets/secondary/azalea_town_hns']
    source_sheets=[Image.open(p/'tiles.png') for p in source_paths]
    source_metas=[_u16(p/'metatiles.bin') for p in source_paths]
    source_attrs=[_u16(p/'metatile_attributes.bin') for p in source_paths]
    source_map=_u16(D/'layouts/AzaleaTown_hns/map.bin')
    values=[source_map[y*62+x] for y in range(20,24) for x in range(37,41)]
    source_words=[]
    for v in values:
        i=v&1023; k=int(i>=640); j=i-(640 if k else 0)
        source_words.append(source_metas[k][j*8:j*8+8])
    used_banks=sorted({v>>12 for row in source_words for v in row if (v&1023)!=0})
    free_banks=[i for i in range(6,13) if i not in banks]
    assert len(free_banks)>=len(used_banks),(used_banks,free_banks)
    bankmap=dict(zip(used_banks,free_banks))
    palettes={bankmap[i]:(source_paths[int(i>=6)]/f'palettes/{i:02}.pal').read_bytes() for i in used_banks}
    free_meta=[i for i in range(512,1024) if i not in secondary_ids and i not in gym_meta]
    assert len(free_meta)>=16
    free_tiles=[i for i in list(range(512,1024))+list(range(432)) if i not in protected]
    mapping={}
    def translate(v):
        src=v&1023
        if not src: return 0
        if src not in mapping:
            assert free_tiles, 'Insufficient private graphics slots for kiln facade'
            dest=free_tiles.pop(0); protected.add(dest); mapping[src]=dest
            k=int(src>=640); old=src-(640 if k else 0); im=source_sheets[k]
            tile=im.crop(((old%16)*8,(old//16)*8,(old%16)*8+8,(old//16)*8+8))
            j=dest%512;sheets[dest//512].paste(tile,((j%16)*8,(j//16)*8))
        return mapping[src] | (v&0xc00) | (bankmap[v>>12]<<12)
    stamps=[]
    for i,(v,words) in enumerate(zip(values,source_words)):
        ident=v&1023;k=int(ident>=640);j=ident-(640 if k else 0);d=free_meta[i]
        metas[1][(d-512)*8:(d-511)*8]=[translate(w) for w in words]
        a=source_attrs[k][j]
        # HNS door behavior 0x69 differs from Emerald's ordinary door 0x60.
        if i==13:a=(a&~255)|0x60; v=(v&~0xc00)|0x3000
        attrs[1][d-512]=a
        stamps.append((v&~1023)|d)
    return {'origin':list(ORIGIN),'door':list(DOOR),'stamp':stamps,'metatile_ids':free_meta[:16],
            'donor_commit':'167aa6d537b109bb229c231ddce4616974c4da71',
            'donor_map_rect':[37,20,4,4],'palette_mapping':bankmap,'tile_mapping':mapping},palettes

def overlay(t,w,h,plan):
    if not plan:return t
    assert (w,h)==(48,44)
    x,y=plan['origin']
    for i,value in enumerate(plan['stamp']):t[(y+i//4)*w+x+i%4]=value
    return t

def patch_event(m):
    entry={'x':DOOR[0],'y':DOOR[1],'elevation':0,'dest_map':'MAP_AZALEA_TOWN_CHARCOAL_KILN','dest_warp_id':'0'}
    if len(m['warp_events'])==7:m['warp_events'].append(entry)
    else:assert m['warp_events'][7]==entry,('Unexpected Azalea warp slot 7',m['warp_events'][7])
    return m
