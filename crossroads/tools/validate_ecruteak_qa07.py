#!/usr/bin/env python3
"""Independent QA06 preservation and semantic terrain/footprint regressions.

Static checks complement controller recordings. They do not certify visual QA.
The immutable QA06 contract prevents live authoring bases legitimizing regressions.
"""
import functools, io, json, struct, subprocess, hashlib
from pathlib import Path
from PIL import Image
from hgss_ecruteak_terrain import PAVING, PAVING_GRAPHIC, neutral_graphics, neutral_metadata

R = Path(__file__).resolve().parents[2]
BASE = json.loads((R/'crossroads/hgss/contracts/ecruteak-qa06.json').read_text())


def load(path): return json.loads((R/path).read_text())
def words(data): return struct.unpack('<'+str(len(data)//2)+'H',data)


@functools.lru_cache(None)
def old(path):
    return subprocess.check_output(['git','show',BASE['source_commit']+':'+path],cwd=R)


@functools.lru_cache(None)
def resource(primary, secondary, baseline=False):
    roots=[f'data/tilesets/primary/{primary}',f'data/tilesets/secondary/{secondary}']
    get=old if baseline else lambda p:(R/p).read_bytes()
    sheets=[Image.open(io.BytesIO(get(p+'/tiles.png'))) for p in roots]
    ms=[words(get(p+'/metatiles.bin')) for p in roots]
    ats=[words(get(p+'/metatile_attributes.bin')) for p in roots]
    palettes=[[tuple(int(v)//8 for v in row.split()) for row in get(roots[0 if i<6 else 1]+f'/palettes/{i:02}.pal').decode().splitlines()[3:]] for i in range(16)]
    return sheets,ms,ats,palettes


@functools.lru_cache(None)
def rendered(primary,secondary,n,baseline=False):
    sheets,ms,ats,pals=resource(primary,secondary,baseline)
    parts=[]
    for v in ms[n>=512][n%512*8:n%512*8+8]:
        i=v&1023;k=i%512
        tile=sheets[i>=512].crop((k%16*8,k//16*8,k%16*8+8,k//16*8+8))
        if v&0x400:tile=tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if v&0x800:tile=tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        parts.append(tuple(pals[v>>12][c] if c else None for c in tile.tobytes()))
    return tuple(tuple(top if top is not None else bottom for bottom,top in zip(parts[j],parts[j+4])) for j in range(4))


def validate():
    assert load('data/maps/map_groups.json')==BASE['groups'],'Map IDs changed'
    ls=load('data/layouts/layouts.json')['layouts']
    assert [l['id'] for l in ls]==BASE['all_layout_ids'],'Layout IDs changed'
    assert load('src/data/heal_locations.json')==BASE['heals'],'Heal/save IDs changed'
    layouts={l['id']:l for l in ls}
    for n,m in BASE['maps'].items():
        expected=json.loads(json.dumps(m))
        if n=='EcruteakCity':
            expected['bg_events'] += [dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='Hgss_PrivateResidence') for x,y in [(23,36),(35,36),(54,55)]]
        assert load(f'data/maps/{n}/map.json')==expected,(n,'QA06 events/entrance coordinates changed beyond exact three appended private-door labels')
        assert layouts[m['layout']]==BASE['layouts'][m['layout']],(n,'QA06 dimensions/IDs changed')
        if n!='EcruteakCity':
            assert (R/layouts[m['layout']]['blockdata_filepath']).read_bytes()==bytes.fromhex(BASE['raw_maps'][n]),(n,'Unrelated interior/floor changed')
    gm=words((R/'data/tilesets/primary/general/metatiles.bin').read_bytes())
    ga=words((R/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes())
    expected,ea=neutral_metadata(gm,ga)
    p=R/'data/tilesets/primary/hgss_ecruteak_buffer'
    assert list(words((p/'metatiles.bin').read_bytes()))==expected
    assert list(words((p/'metatile_attributes.bin').read_bytes()))==ea
    actual=words((p/'metatiles.bin').read_bytes());attributes=words((p/'metatile_attributes.bin').read_bytes())
    assert actual[PAVING*8:(PAVING+1)*8]==(0x3001,)*4+(0,)*4 and attributes[PAVING]==0x1000
    for i in range(512):
        if i!=PAVING:assert actual[i*8:(i+1)*8]==gm[i*8:(i+1)*8] and attributes[i]==ga[i],('Unrelated buffer metatile changed',i)
    original=Image.open(R/'data/tilesets/primary/general/tiles.png')
    new=Image.open(p/'tiles.png');assert new.tobytes()==neutral_graphics().tobytes()
    for i in range(512):
        if i==PAVING_GRAPHIC:continue
        box=(i%16*8,i//16*8,i%16*8+8,i//16*8+8)
        assert new.crop(box).tobytes()==original.crop(box).tobytes(),('Shared terrain changed',i)
    raw=words((R/'data/layouts/EcruteakCity/map.bin').read_bytes())
    specs=load('crossroads/hgss/art/native-manifest.json')['specs']
    res=resource('bl_gym_ecruteak','bl_gym_ecruteak')
    # Trees have a solid two-cell ground footprint, distinct from the overhang.
    for x,y in [(26,33),(38,33),(26,42),(29,52),(49,52),(58,42)]:
        for dx in range(2):
            assert raw[(y+1)*64+x+dx]&0xc00,('Walkable tree trunk',x+dx,y+1)
            assert raw[y*64+x+dx]>>12==3 and not raw[y*64+x+dx]&0xc00
    for kind in ['tree','autumn_tree']:
        for dx in range(2):
            n=specs[kind]['start']+dx;assert res[2][1][n-512]>>12==0
            refs=res[1][1][(n-512)*8:(n-511)*8]
            for j,v in enumerate(refs[4:]):
                i=v&1023;k=i%512;tile=res[0][i>=512].crop((k%16*8,k//16*8,k%16*8+8,k//16*8+8)).tobytes()
                assert set(tile)<={0,1,2,3,4} and any(tile),('Missing leaf-only foreground',kind,j)
    # Ground-plane walls are defined independently of whatever cells are blocked.
    buildings=[('burned',21,15,True),('barrier',33,21,True),('house',20,42,True),('house',31,52,True),('house',20,33,False),('house',32,33,False),('house',51,52,False),('theater',42,41,True),('center',43,51,True),('mart',52,42,True)]
    for kind,x,y,opened in buildings:
        a=specs[kind]
        for yy in range(a['height']-2,a['height']):
            for xx in range(a['width']):
                door=opened and yy==a['door_y'] and (xx==a['door_x'] or kind=='barrier' and xx==a['door_x']-1)
                assert bool(raw[(y+yy)*64+x+xx]&0xc00)!=door,('Wall/door ground footprint',kind,x+xx,y+yy,door)
    # Static art is unchanged, including custom Gym pixels. Only the broken road
    # buffer (flowers with arrow behavior) may become the documented neutral brick.
    checked=changed=0
    for n,primary,secondary in [('EcruteakCity','bl_gym_ecruteak','bl_gym_ecruteak'),('BellchimeTrail','hgss_bell','hgss_bell')]:
        m=BASE['maps'][n];l=layouts[m['layout']];before=words(bytes.fromhex(BASE['raw_maps'][n]));after=words((R/l['blockdata_filepath']).read_bytes());ats=resource(primary,secondary)[2]
        for i,(a,b) in enumerate(zip(before,after)):
            assert a&0xfc00==b&0xfc00,(n,'Collision/elevation changed',i)
            an,bn=a&1023,b&1023
            if bn==PAVING:
                x,y=i%l['width'],i//l['width'];assert n=='EcruteakCity' and an==0x24 and (x<7 or x>=57 or y>=57),(n,'Undocumented road change',x,y)
                assert ats[0][bn]&255==0;changed+=1;continue
            assert rendered(primary,secondary,an,True)==rendered(primary,secondary,bn),(n,'Liked static art changed',i)
            assert ats[bn>=512][bn%512]&255 not in range(0x62,0x66),(n,'Ordinary terrain still has warp-arrow behavior',i)
            checked+=1
    assert changed>0
    print('QA07 immutable QA06 IDs/events/interiors, static exterior pixels, semantic trunks/walls/doors, leaf foreground and neutral road behavior: PASS',checked,'unchanged cells;',changed,'corrected road cells')


def validate_recordings(folder,baseline=None):
    """Actual native pixels must occlude Joe, rather than only having correct IDs.

    The reproduction walks Joe to26,42. Its fixed camera places the32x16 canopy
    at112,72. Compare every leaf pixel to the untouched General tree reference.
    This catches a wrong layer even when collision probes and asset checks pass.
    """
    folder=Path(folder);result=json.loads((folder/'reproduction.json').read_text())
    assert result['rom_sha256']==hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest()
    assert all(not r['arrow']['visible'] and r['arrow_visible_samples']==0 for r in result['records'])
    general=R/'data/tilesets/primary/general';metas=words((general/'metatiles.bin').read_bytes());sheet=Image.open(general/'tiles.png')
    palette=[tuple(((int(v)>>3)<<3)|((int(v)>>3)>>2) for v in row.split()) for row in (general/'palettes/02.pal').read_text().splitlines()[3:]]
    def compare(path):
        shot=Image.open(path).convert('RGB');assert shot.size==(240,160)
        matched=total=0
        for half,n in enumerate([0x1d4,0x1d5]):
            for y in range(16):
                for x in range(16):
                    ref=metas[n*8+x//8+2*(y//8)];i=ref&1023
                    xx=x%8;yy=y%8
                    if ref&0x400:xx=7-xx
                    if ref&0x800:yy=7-yy
                    c=sheet.getpixel((i%16*8+xx,i//16*8+yy))
                    if not 1<=c<=4:continue
                    total+=1;matched+=int(shot.getpixel((112+half*16+x,72+y))==palette[c])
        return matched,total
    after=compare(folder/'canopy-entry.png');assert after[0]==after[1],('Joe still drawn over leaf foreground',after)
    report=dict(native_size=[240,160],after_leaf_pixels_matched=after[0],after_leaf_pixels_total=after[1],rom_sha256=result['rom_sha256'])
    if baseline:
        baseline=Path(baseline);before=json.loads((baseline/'reproduction.json').read_text());assert before['rom_sha256']==BASE['rom_sha256']
        assert next(r for r in before['records'] if r['label']=='ordinary-paving-south')['arrow']['visible']
        b=compare(baseline/'canopy-entry.png');assert b[0]<b[1]-10,('Baseline failed to reproduce leaf overlap',b)
        report.update(before_leaf_pixels_matched=b[0],before_leaf_pixels_total=b[1],before_rom_sha256=before['rom_sha256'])
    (folder/'visual-regressions.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Recorded normal walking: no unintended arrow samples; actual native leaf occlusion matches original static tree:',after,'PASS')


if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--recordings');p.add_argument('--baseline');a=p.parse_args()
    validate()
    if a.recordings:validate_recordings(a.recordings,a.baseline)
