#!/usr/bin/env python3
"""Prepare an append-only donor gate metatile; never write live files directly.

The caller supplies the writer. Existing chamber cells, graphics and palette
banks 0..4 are unchanged. The resulting art is unused until gated events are
separately integrated and validated.
"""
import hashlib,io,json,struct,tempfile
from pathlib import Path
from PIL import Image
import prepare_hns_ruins_pockets as p

ROOT=Path(__file__).resolve().parents[2]
OUT='data/tilesets/primary/hgssruinschamber'
REV='167aa6d537b109bb229c231ddce4616974c4da71'


def stage(write):
    source=p.SOURCE;manifest=json.loads((source/'source-sha256.json').read_text());assert manifest['revision']==REV
    for path,digest in manifest['files'].items():assert hashlib.sha256((source/path).read_bytes()).hexdigest()==digest,path
    group=p.GROUPS['chambers'];data=source/'data';primary=data/'tilesets/primary'/group['primary'];secondary=data/'tilesets/secondary'/group['secondary']
    with tempfile.TemporaryDirectory(prefix='ruins-gate-art-') as td:
        tmp=Path(td);report=p.convert(group,tmp)
        assert (report['metatiles'],report['tiles'],report['palette_banks'])==(40,78,[0,5,7,8,10])
        source_meta=[p.words(primary/'metatiles.bin'),p.words(secondary/'metatiles.bin')]
        source_attrs=p.words(secondary/'metatile_attributes.bin')
        cells=p.words(data/'layouts'/group['source']/'map.bin');used=set()
        for x,y,w,h in group['crops'].values():
            for yy in range(y,y+h):
                for xx in range(x,x+w):used.add(cells[yy*group['width']+xx]&1023)
        refs=[]
        for index in sorted(used):
            k=int(index>=640);i=index-640*k;refs+=source_meta[k][i*8:i*8+8]
        old_tile_ids=sorted({v&1023 for v in refs});assert len(old_tile_ids)==78
        tilemap={old:new for new,old in enumerate(old_tile_ids)}
        bankmap={int(old):new for old,new in report['palette_map'].items()};assert bankmap=={0:0,5:1,7:2,8:3,10:4}
        gate=0x308-640;gate_refs=source_meta[1][gate*8:gate*8+8]
        assert source_attrs[gate]==0x60 and list(gate_refs)==[0xb2de,0xb2df,0xb2ee,0xb2ef,0,0,0,0]
        needed=sorted({v&1023 for v in gate_refs}-set(tilemap));assert needed==[734,735,750,751]
        tilemap.update({old:80+i for i,old in enumerate(needed)});bankmap[11]=5
        old_sheet=Image.open(tmp/'tiles.png');assert old_sheet.size==(128,40) and old_sheet.mode=='P'
        new_sheet=Image.new('P',(128,48));new_sheet.putpalette(old_sheet.getpalette());new_sheet.paste(old_sheet,(0,0))
        donor_sheet=Image.open(secondary/'tiles.png');assert donor_sheet.mode=='P'
        for old in needed:
            index=old-640;tile=donor_sheet.crop(((index%16)*8,(index//16)*8,(index%16+1)*8,(index//16+1)*8))
            new=tilemap[old];new_sheet.paste(tile,((new%16)*8,(new//16)*8))
        out=io.BytesIO();new_sheet.save(out,format='PNG',optimize=False);write(OUT+'/tiles.png',out.getvalue())
        old_meta=(tmp/'metatiles.bin').read_bytes();old_attrs=(tmp/'metatile_attributes.bin').read_bytes()
        remapped=[tilemap[v&1023]|(v&0xc00)|(bankmap[v>>12]<<12) for v in gate_refs]
        write(OUT+'/metatiles.bin',old_meta+struct.pack('<8H',*remapped))
        write(OUT+'/metatile_attributes.bin',old_attrs+struct.pack('<H',0x60))
        for i in range(16):
            src=secondary/'palettes/11.pal' if i==5 else tmp/'palettes'/f'{i if i<5 else 0:02}.pal'
            write(OUT+f'/palettes/{i:02}.pal',src.read_bytes())
        # This is the metatile ID, with no collision/elevation bits included.
        return 40
