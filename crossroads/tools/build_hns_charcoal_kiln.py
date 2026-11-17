#!/usr/bin/env python3
"""Convert a pinned Heart & Soul room into an isolated Emerald tileset.

Only used room metatiles and graphics are packed. Source geometry/collision is
retained; donor story, objects, flags and events are not imported. The exterior
is authored independently and must bind the unchanged local return warp.
"""
import argparse, hashlib, io, json, struct
from pathlib import Path
from PIL import Image, ImageDraw
from tileset_registration import upsert

R = Path(__file__).resolve().parents[2]
SRC = R / 'crossroads/donor/hns-charcoal-kiln/data'
OUT = 'data/tilesets/primary/hns_charcoal_kiln'
MARK = 'HNS CHARCOAL KILN PRIVATE'
REV = '167aa6d537b109bb229c231ddce4616974c4da71'

def words(path):
    data = path.read_bytes()
    return list(struct.unpack('<' + str(len(data)//2) + 'H', data))

def pack(values):
    return struct.pack('<' + str(len(values)) + 'H', *values)

def generate(check=False):
    def write(path, data):
        path = R / path
        if isinstance(data, str): data = data.encode()
        if check:
            assert path.exists() and path.read_bytes() == data, ('Regenerate', str(path))
        elif not path.exists() or path.read_bytes() != data:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    provenance = json.loads((SRC.parent/'source-sha256.json').read_text())
    assert provenance['revision'] == REV
    for path, digest in provenance['files'].items():
        assert hashlib.sha256((SRC.parent/path).read_bytes()).hexdigest() == digest, ('Donor source mismatch', path)
    donor = words(SRC / 'layouts/AzaleaTown_House1_hns/map.bin')
    assert len(donor) == 110
    pri = SRC / 'tilesets/primary/johto_building_hns'
    sec = SRC / 'tilesets/secondary/barn_hns'
    meta = words(pri / 'metatiles.bin') + words(sec / 'metatiles.bin')
    attrs = words(pri / 'metatile_attributes.bin') + words(sec / 'metatile_attributes.bin')
    assert len(meta) == (640+180)*8 and len(attrs) == 640+180
    used = sorted(set(v & 1023 for v in donor))
    assert len(used) == 37 and max(used) < len(attrs)
    refs = [v for k in used for v in meta[8*k:8*k+8]]
    tileids = sorted(set(v & 1023 for v in refs))
    banks = sorted(set(v >> 12 for v in refs))
    assert len(tileids) == 79 and banks == [0,3,5,7,8]
    tilemap = {old:new for new,old in enumerate(tileids)}
    metamap = {old:new for new,old in enumerate(used)}
    palmap = {old:new for new,old in enumerate(banks)}
    sheets = [Image.open(pri/'tiles.png'),Image.open(sec/'tiles.png')]
    assert all(im.mode == 'P' for im in sheets)
    # Add 36 8x8 graphics for an original 3x3 brick kiln, after the donor tiles.
    image = Image.new('P',(128,128))
    image.putpalette(sheets[0].getpalette())
    for old,new in tilemap.items():
        index=old if old<640 else old-640
        sheet=sheets[0 if old<640 else 1]
        assert index < (sheet.width//8)*(sheet.height//8)
        x,y=(index%16)*8,(index//16)*8
        image.paste(sheet.crop((x,y,x+8,y+8)),((new%16)*8,(new//16)*8))
    kiln=Image.new('P',(48,48),2)
    kiln.putpalette(sheets[0].getpalette())
    draw=ImageDraw.Draw(kiln)
    draw.rectangle((0,0,47,47),fill=2,outline=1,width=2)
    for y in range(3,48,8):
        draw.line((2,y,45,y),fill=1)
        for x in range(2 + (5 if (y//8)%2 else 0),46,10):
            draw.line((x,y,x,y+7),fill=1)
    draw.rectangle((12,20,35,45),fill=1,outline=3,width=2)
    draw.rectangle((16,26,31,42),fill=15)
    draw.polygon([(18,41),(20,32),(23,37),(26,29),(29,41)],fill=13)
    draw.polygon([(21,41),(24,35),(27,41)],fill=14)
    for row in range(6):
        for col in range(6):
            idx=len(tileids)+row*6+col
            image.paste(kiln.crop((col*8,row*8,col*8+8,row*8+8)),((idx%16)*8,(idx//16)*8))
    for i in range(16):
        if i < len(banks):
            b=banks[i]; source=(pri if b<7 else sec)/f'palettes/{b:02}.pal'
        else: source=pri/'palettes/00.pal'
        write(OUT+f'/palettes/{i:02}.pal',source.read_bytes())
    outmeta=[]
    for v in refs:
        outmeta.append(tilemap[v&1023] | (v&0x0c00) | (palmap[v>>12]<<12))
    outattrs=[attrs[i] for i in used]
    # Keep donor ground beneath the new kiln and place its sprite-free art on
    # the upper layer. Only these nine documented cells change collision.
    for y in range(3):
        for x in range(3):
            original=donor[(y+2)*11+(x+7)]&1023
            base=metamap[original]*8
            outmeta.extend(outmeta[base:base+4])
            outmeta.extend([len(tileids)+(y*2+yy)*6+(x*2+xx) for yy in range(2) for xx in range(2)])
            outattrs.append(attrs[original])
    # HGSS reference also has a pale work floor, raised wooden platform,
    # shelving, bench and chimney. These are newly drawn GBA adaptations.
    blank=115
    nexttile=116
    def art(kind):
        im=Image.new('P',(16,16),0);im.putpalette(sheets[0].getpalette());d=ImageDraw.Draw(im)
        if kind=='stone':
            d.rectangle((0,0,15,15),fill=3)
            for x,y in ((1,2),(8,3),(13,7),(4,10),(11,13),(2,15)):d.point((x,y),fill=15)
        elif kind=='edge':
            d.rectangle((0,11,15,15),fill=1);d.line((0,11,15,11),fill=3)
            d.rectangle((1,12,5,15),fill=2);d.rectangle((9,12,13,15),fill=2)
        elif kind=='shelf':
            d.rectangle((0,0,15,15),fill=1);d.rectangle((2,2,13,13),fill=2)
            for y in (5,10):d.line((2,y,13,y),fill=7)
            for x in (3,6,9,12):d.line((x,2,x,4),fill=13 if x==6 else 5)
            for x in (4,7,10):d.line((x,7,x,9),fill=6)
        elif kind=='bench':
            d.rectangle((0,0,15,15),fill=2)
            d.rectangle((0,3,15,10),fill=7,outline=1);d.line((1,4,14,4),fill=4)
            d.rectangle((2,11,4,14),fill=1);d.rectangle((11,11,13,14),fill=1)
        elif kind=='chimney':
            d.rectangle((0,0,15,15),fill=2)
            d.rectangle((2,0,13,15),fill=2,outline=1);d.line((4,0,4,15),fill=3);d.line((11,0,11,15),fill=15)
            d.line((2,3,13,3),fill=1);d.line((2,13,13,13),fill=1)
        return im
    artrefs={}
    for kind in ('stone','edge','shelf','bench','chimney'):
        im=art(kind); ids=[]
        for row in range(2):
            for col in range(2):
                idx=nexttile;nexttile+=1;ids.append(idx)
                image.paste(im.crop((col*8,row*8,col*8+8,row*8+8)),((idx%16)*8,(idx//16)*8))
        artrefs[kind]=ids
    assert nexttile < 256
    artcells={}
    for y in range(3,9):
        for x in range(1,10):
            if ((x>=6 or y>=7) and not (7<=x<=9 and 2<=y<=4)
                and not (y==8 and x in (4,5,6))): artcells[x,y]='stone'
    for x in range(1,6): artcells[x,6]='edge'
    for x in (1,2):artcells[x,1]='shelf'
    for x in (3,4,5):artcells[x,1]='bench'
    for y in (0,1):artcells[8,y]='chimney'
    extra={}
    for (x,y),kind in sorted(artcells.items(),key=lambda item:(item[0][1],item[0][0])):
        original=donor[y*11+x]&1023
        donorbase=metamap[original]*8
        # A transparent edge motif overlays the donor wooden floor. Other
        # motifs replace the visible donor surface, not its movement flags.
        if kind=='edge': outmeta.extend(outmeta[donorbase:donorbase+4]+artrefs[kind])
        else: outmeta.extend(artrefs[kind]+[blank]*4)
        extra[x,y]=len(outattrs);outattrs.append(attrs[original])
    buf=io.BytesIO();image.save(buf,format='PNG',optimize=False)
    write(OUT+'/tiles.png',buf.getvalue())
    write(OUT+'/metatiles.bin',pack(outmeta))
    write(OUT+'/metatile_attributes.bin',pack(outattrs))
    # Preserve donor cells outside the explicitly authored kiln footprint.
    cells=[(v&0xfc00)|metamap[v&1023] for v in donor]
    for y in range(3):
        for x in range(3):
            cells[(y+2)*11+(x+7)]=0x3400 | (len(used)+y*3+x)
    for (x,y),new in extra.items():cells[y*11+x]=(donor[y*11+x]&0xfc00)|new
    write('data/layouts/AzaleaTown_CharcoalKiln/map.bin',pack(cells))
    donor_border=words(SRC/'layouts/AzaleaTown_House1_hns/border.bin')
    assert all((v&1023) in metamap for v in donor_border)
    write('data/layouts/AzaleaTown_CharcoalKiln/border.bin',pack([(v&0xfc00)|metamap[v&1023] for v in donor_border]))
    assert donor[8*11+5]&1023==676 and attrs[676]&255==0x65
    sym='HnsCharcoalKiln'
    sections={
      'graphics': f'const u32 gTilesetTiles_{sym}[] = INCGFX_U32("{OUT}/tiles.png", ".4bpp.fastSmol");\nconst u16 gTilesetPalettes_{sym}[][16] = {{\n'+''.join(f' INCGFX_U16("{OUT}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n',
      'metatiles':f'const u16 gMetatiles_{sym}[] = INCBIN_U16("{OUT}/metatiles.bin");\nconst u16 gMetatileAttributes_{sym}[] = INCBIN_U16("{OUT}/metatile_attributes.bin");\n',
      'headers':f'const struct Tileset gTileset_{sym} = {{ .isCompressed=TRUE, .isSecondary=FALSE, .tiles=gTilesetTiles_{sym}, .palettes=gTilesetPalettes_{sym}, .metatiles=gMetatiles_{sym}, .metatileAttributes=gMetatileAttributes_{sym}, .callback=NULL }};\n',
      'externs':f'extern const struct Tileset gTileset_{sym};\n'}
    for kind,path in [('graphics','src/data/tilesets/graphics.h'),('metatiles','src/data/tilesets/metatiles.h'),('headers','src/data/tilesets/headers.h'),('externs','include/tilesets.h')]:
        begin='// BEGIN '+MARK;end='// END '+MARK
        body=begin+'\n#if !IS_FRLG\n'+sections[kind]+'#endif\n'+end
        original=(R/path).read_text()
        write(path,upsert(original,begin,end,body,externs=kind=='externs'))
    # Map ID/layout are append-only. The town-side generator adds exterior warp 7.
    name='AzaleaTown_CharcoalKiln'
    layout=dict(id='LAYOUT_AZALEA_TOWN_CHARCOAL_KILN',name=name+'_Layout',width=11,height=10,
        primary_tileset='gTileset_HnsCharcoalKiln',secondary_tileset='gTileset_WesternInteriors',
        border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin',layout_version='emerald')
    m=dict(id='MAP_AZALEA_TOWN_CHARCOAL_KILN',name=name,layout=layout['id'],music='MUS_LITTLEROOT',
        region='REGION_HOENN',region_map_section='MAPSEC_AZALEA_TOWN',requires_flash=False,weather='WEATHER_NONE',
        map_type='MAP_TYPE_INDOOR',allow_cycling=False,allow_escaping=False,allow_running=True,show_map_name=False,
        battle_scene='MAP_BATTLE_SCENE_NORMAL',connections=None,
        object_events=[dict(graphics_id='OBJ_EVENT_GFX_EXPERT_M',x=2,y=4,elevation=3,
            movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',
            trainer_sight_or_berry_tree_id='0',script='AzaleaTown_CharcoalKiln_EventScript_Worker',flag='0')],
        warp_events=[dict(x=5,y=8,elevation=0,dest_map='MAP_AZALEA_TOWN',dest_warp_id='7')],coord_events=[],bg_events=[])
    write(f'data/maps/{name}/map.json',json.dumps(m,indent=2)+'\n')
    write(f'data/maps/{name}/scripts.inc',name+'_MapScripts::\n    .byte 0\n\n'
        'AzaleaTown_CharcoalKiln_EventScript_Worker::\n'
        '    msgbox AzaleaTown_CharcoalKiln_Text_Worker, MSGBOX_NPC\n    end\n'
        'AzaleaTown_CharcoalKiln_Text_Worker:\n'
        '    .string "We keep the kiln fed with dry wood.\\nIt takes patience to make charcoal.$"\n')
    layouts=json.loads((R/'data/layouts/layouts.json').read_text())
    found=[i for i in layouts['layouts'] if i['id']==layout['id']]
    if found: assert found == [layout], 'Existing kiln layout changed unexpectedly'
    else: layouts['layouts'].append(layout)
    write('data/layouts/layouts.json',json.dumps(layouts,indent=2)+'\n')
    groups=json.loads((R/'data/maps/map_groups.json').read_text())
    entries=groups['gMapGroup_CrossroadsJohtoExpansion']
    if name in entries: assert entries.index(name)==50
    else: assert len(entries)==50; entries.append(name)
    write('data/maps/map_groups.json',json.dumps(groups,indent=2)+'\n')
    manifest=json.loads((R/'crossroads/johto/manifest.json').read_text())
    if not any(p['name']==name for p in manifest['planned']):
        manifest['planned'].append(dict(name=name,kind='hgss',parent='AzaleaTown',cluster='west'))
    write('crossroads/johto/manifest.json',json.dumps(manifest,indent=2)+'\n')
    print(f'Heart & Soul Charcoal Kiln: {len(used)} donor metatiles, {len(tileids)} donor tiles, {len(banks)} palettes; 9 original kiln cells added.')

if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');generate(p.parse_args().check)
