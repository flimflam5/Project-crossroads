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
    # Private source-backed stage art is authorized only by the exact immutable
    # V7 delta. Its independent validator preserves all room physics, all other
    # visible cells, actors/warps and every shared Temple resource byte.
    stage_contract=load('crossroads/hgss/contracts/theater-stage-qa09.json')
    from validate_theater_stage import validate as validate_stage
    validate_stage()
    gate_contract=load('crossroads/hgss/contracts/gate-interior-art-qa09.json')
    from validate_gate_interior_art import validate as validate_gate_art
    validate_gate_art()
    basement_contract=load('crossroads/hgss/contracts/center-basement-qa09.json')
    reception_contract=load('crossroads/hgss/contracts/center-reception-qa09.json')
    from validate_center_basement import validate as validate_basement
    validate_basement()
    mart_contract=load('crossroads/hgss/contracts/mart-props-qa09.json')
    from validate_hgss_mart_props import validate as validate_mart
    validate_mart()
    from hgss_ecruteak_tower_details import validate as validate_details,HEADERS as detail_headers,patch as detail_patch,SYMBOL as detail_symbol
    validate_details();detail_maps={n:h for h,n in detail_headers.items()}
    groups=load('data/maps/map_groups.json')
    for key,values in BASE['groups'].items():
        if key=='gMapGroup_CrossroadsJohtoExpansion':
            assert groups[key][:len(values)]==values,'Existing map IDs changed'
            assert groups[key][len(values):]==['OlivineCity_FishingHouse','OlivineCity_TradeHouse','OlivineCity_SealHouse','OlivineCity_Cafe','OlivineCity_PokemonCenter_B1F','OlivineCity_Lighthouse_Balcony','OlivineCity_Lighthouse_Elevator','OlivineCity_PortTerminal','OlivineCity_PortQuay'],'Unexpected appended map IDs'
        else:assert groups[key]==values,'Map group/order changed'
    ls=load('data/layouts/layouts.json')['layouts']
    assert [l['id'] for l in ls[:len(BASE['all_layout_ids'])]]==BASE['all_layout_ids'],'Existing layout IDs changed'
    assert len({l['id'] for l in ls})==len(ls),'Duplicate layout ID'
    expected_heals=json.loads(json.dumps(BASE['heals']))
    next(h for h in expected_heals['heal_locations'] if h['id']=='HEAL_LOCATION_OLIVINE_CITY').update(x=16,y=34,respawn_x=8,respawn_y=13)
    assert load('src/data/heal_locations.json')==expected_heals,'Heal/save IDs changed beyond exact Olivine arrival'
    layouts={l['id']:l for l in ls}
    for n,m in BASE['maps'].items():
        expected=json.loads(json.dumps(m))
        if n=='EcruteakCity':
            expected['bg_events'] += [dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='Hgss_PrivateResidence') for x,y in [(23,36),(35,36),(54,55)]]
            expected['bg_events'][8].update(x=59,y=52) # Outside the completed east facade.
            expected['bg_events'][7].update(x=9,y=40) # Clear the upper west exit's outward step.
            # QA08 owner-authorized paired leaves. Explicit migration, not a
            # blanket allowance for event changes or a new mutable baseline.
            expected['warp_events'][1]['dest_warp_id']='2'
            expected['warp_events'][3]['dest_warp_id']='1'
            alias=dict(expected['warp_events'][3],x=44,y=45,dest_warp_id='0')
            expected['warp_events'].append(alias)
            for start in [9,12]:
                for j,index in enumerate([2,0,3]):expected['warp_events'][start+j]['dest_warp_id']=str(index)
            for e in expected['warp_events'][9:12]:e['x']=6
            for ax,ys,mid in [(7,range(37,40),'MAP_ECRUTEAK_CITY_WEST_GATE'),(59,range(46,49),'MAP_ECRUTEAK_CITY_EAST_GATE')]:
                for y,index in zip(ys,[2,0,3]):expected['warp_events'].append(dict(x=ax,y=y,elevation=0,dest_map=mid,dest_warp_id=str(index)))
            for direction in ['West','East']:
                es=[e for e in expected['coord_events'] if e['script']=='Hgss_'+direction+'CityGateEnter']
                for j,e in enumerate(es):
                    e['script']+=str(j)
                    if direction=='West':e['x']=6
        elif n=='EcruteakCity_BarrierStation':
            expected['warp_events'][0]['dest_warp_id']='7'
            expected['warp_events'].append(dict(x=10,y=11,elevation=0,dest_map='MAP_ECRUTEAK_CITY',dest_warp_id='1'))
        elif n=='EcruteakCity_DanceTheater':
            expected['warp_events'][0]['dest_warp_id']='16'
        elif n=='EcruteakCity_PokemonCenter_B1F':
            expected['bg_events']=basement_contract['new_bg_events']
        elif n in ('EcruteakCity_WestGate','EcruteakCity_EastGate'):
            for e,index in zip(expected['warp_events'],[18,4] if n.endswith('WestGate') else [21,7]):e['dest_warp_id']=str(index)
            for e in list(expected['warp_events']):
                for delta in [-1,1]:
                    expected['warp_events'].append(dict(e,x=e['x'],y=e['y']+delta,dest_warp_id=str(int(e['dest_warp_id'])+delta)))
        assert load(f'data/maps/{n}/map.json')==expected,(n,'Events differ beyond exact QA07/QA08 authorized migration')
        expected_layout=dict(BASE['layouts'][m['layout']])
        if n=='EcruteakCity_DanceTheater':
            assert expected_layout['secondary_tileset']==stage_contract['before_secondary']
            expected_layout['secondary_tileset']=stage_contract['after_secondary']
        if n in gate_contract['maps']:
            assert expected_layout['secondary_tileset']==gate_contract['before_secondary']
            expected_layout['secondary_tileset']=gate_contract['after_secondary']
        if n==basement_contract['map']:
            assert [expected_layout['width'],expected_layout['height']]==basement_contract['before_dimensions']
            assert expected_layout['secondary_tileset']==basement_contract['before_secondary']
            expected_layout.update(height=basement_contract['after_dimensions'][1],secondary_tileset=basement_contract['after_secondary'])
        if n in mart_contract['maps']:
            assert expected_layout['secondary_tileset']==mart_contract['before_secondary']
            expected_layout['secondary_tileset']=mart_contract['after_secondary']
        if n==reception_contract['map']:
            assert expected_layout['secondary_tileset']==reception_contract['before_secondary']
            expected_layout['secondary_tileset']=reception_contract['after_secondary']
        if n in detail_maps:
            assert expected_layout['secondary_tileset']=='gTileset_HgssTemple'
            expected_layout['secondary_tileset']=detail_symbol
        assert layouts[m['layout']]==expected_layout,(n,'QA06 dimensions/IDs changed beyond exact Theater secondary')
        if n!='EcruteakCity':
            expected_raw=list(words(bytes.fromhex(BASE['raw_maps'][n])))
            if n=='EcruteakCity_BarrierStation':
                art=load('crossroads/hgss/art/temple/manifest.json')['specs']
                expected_raw[11*20+10]=art['exit']['start']
            elif n in ('EcruteakCity_WestGate','EcruteakCity_EastGate'):
                art=load('crossroads/hgss/art/temple/manifest.json')['specs']
                for e in m['warp_events']:
                    for delta in [-1,1]:expected_raw[(e['y']+delta)*12+e['x']]=0x3000|art['stone_warp']['start']
            for contract in (R/'crossroads/hgss/contracts').glob('*-furniture-qa09.json'):
                c=json.loads(contract.read_text())
                for change in c.get('maps',[]):
                    if change['map']!=n:continue
                    assert c['source_commit']=='fd151242458efe5759b18650f35a5e5b2fa47e45'
                    for d in change['changes']:
                        i=d['y']*layouts[m['layout']]['width']+d['x'];assert expected_raw[i]==d['before'];expected_raw[i]=d['after']
            if n=='EcruteakCity_DanceTheater':
                c=load('crossroads/hgss/contracts/theater-seating-qa09.json');assert c['source_commit']=='fd151242458efe5759b18650f35a5e5b2fa47e45'
                for d in c['changes']:
                    i=d['y']*layouts[m['layout']]['width']+d['x'];assert expected_raw[i]==d['before'];expected_raw[i]=d['after']
                assert stage_contract['source_commit']=='3f935d5e8600c5a280b9172b555edb35ca52b6c0'
                for d in stage_contract['changes']:
                    i=d['y']*layouts[m['layout']]['width']+d['x'];assert expected_raw[i]==d['before'];expected_raw[i]=d['after']
                # Actual final-HGSS audience material correction, after the
                # exact seating and69stage-cell migrations above. Retain every
                # before-value assertion; this is not a mutable new baseline.
                c=load('crossroads/hgss/contracts/theater-audience-qa10.json');assert c['source_commit']=='5664fecee4337c5bdd442583e24cc91c09c0a0cd'
                for d in c['raw_changes']:
                    i=d['y']*layouts[m['layout']]['width']+d['x'];assert expected_raw[i]==d['before'];expected_raw[i]=d['after']
            if n in gate_contract['maps']:
                assert gate_contract['source_commit']=='3f935d5e8600c5a280b9172b555edb35ca52b6c0'
                assert expected_raw==gate_contract['before_words']
                for d in gate_contract['changes']:
                    i=d['y']*layouts[m['layout']]['width']+d['x'];assert expected_raw[i]==d['before'];expected_raw[i]=d['after']
            if n==basement_contract['map']:
                assert basement_contract['source_commit']=='3f935d5e8600c5a280b9172b555edb35ca52b6c0'
                for d in basement_contract['changes']:
                    i=d['y']*layouts[m['layout']]['width']+d['x'];assert expected_raw[i]==d['before'];expected_raw[i]=d['after']
                expected_raw+=basement_contract['appended_words']
            if n in mart_contract['maps']:
                assert mart_contract['source_commit']=='3f935d5e8600c5a280b9172b555edb35ca52b6c0'
                assert expected_raw==mart_contract['before_words']
                for d in mart_contract['changes']:
                    i=d['y']*layouts[m['layout']]['width']+d['x'];assert expected_raw[i]==d['before'];expected_raw[i]=d['after']
            if n in detail_maps:
                expected_raw=detail_patch(detail_maps[n],expected_raw,expected_layout['width'],expected_layout['height'])
            if n==reception_contract['map']:
                assert reception_contract['source_commit']=='3f935d5e8600c5a280b9172b555edb35ca52b6c0'
                for d in reception_contract['changes']:
                    i=d['y']*layouts[m['layout']]['width']+d['x'];assert expected_raw[i]==d['before'];expected_raw[i]=d['after']
            assert words((R/layouts[m['layout']]['blockdata_filepath']).read_bytes())==tuple(expected_raw),(n,'Unrelated interior/floor changed')
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
                door=opened and yy==a['door_y'] and (xx==a['door_x'] or kind in ('barrier','theater') and xx==a['door_x']-1)
                assert bool(raw[(y+yy)*64+x+xx]&0xc00)!=door,('Wall/door ground footprint',kind,x+xx,y+yy,door)
    # Static art is unchanged, including custom Gym pixels. Only the broken road
    # buffer (flowers with arrow behavior) may become the documented neutral brick.
    checked=changed=0
    for n,primary,secondary in [('EcruteakCity','bl_gym_ecruteak','bl_gym_ecruteak'),('BellchimeTrail','hgss_bell','hgss_bell')]:
        m=BASE['maps'][n];l=layouts[m['layout']];before=words(bytes.fromhex(BASE['raw_maps'][n]));after=words((R/l['blockdata_filepath']).read_bytes());ats=resource(primary,secondary)[2]
        for i,(a,b) in enumerate(zip(before,after)):
            x,y=i%l['width'],i//l['width']
            # Source-backed gate models: west returns to canonical x6, east
            # model crosses the unchanged Route42 seam. Other art stays exact.
            gate=(0,36) if n=='EcruteakCity' and 0<=x<7 and 36<=y<43 else (60,45) if n=='EcruteakCity' and 60<=x<64 and 45<=y<52 else None
            if gate:
                dx,dy=x-gate[0],y-gate[1];spec=specs['gate'];wanted=spec['start']+dy*7+dx+(0x3000 if 1<=dy<=3 else 0x400)
                assert b==wanted,('Gate physical roof/tunnel/front wall contract',x,y)
                continue
            if n=='EcruteakCity' and (x,y) in {(59,52),(9,40)}:assert b==0x403;continue
            if n=='EcruteakCity' and (x,y)==(8,37):assert b==0x3000|specs['paving'];continue
            if n=='EcruteakCity' and i==45*64+44:
                assert a&0xfc00==0x400 and b&0xfc00==0x3000,'Theater left threshold is not open'
            else:assert a&0xfc00==b&0xfc00,(n,'Collision/elevation changed',i)
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
    def compare(path,active_palette=None):
        shot=Image.open(path).convert('RGB');assert shot.size==(240,160)
        colors=palette
        if active_palette is not None:
            assert len(active_palette)==16 and any(active_palette)
            colors=[tuple(((c<<3)|(c>>2)) for c in [v&31,(v>>5)&31,(v>>10)&31]) for v in active_palette]
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
                    total+=1;matched+=int(shot.getpixel((112+half*16+x,72+y))==colors[c])
        return matched,total
    canopy=next(r for r in result['records'] if r['label']=='canopy-entry')
    after=compare(folder/'canopy-entry.png',canopy.get('tree_palette_rgb555'));assert after[0]==after[1],('Joe still drawn over leaf foreground',after)
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
