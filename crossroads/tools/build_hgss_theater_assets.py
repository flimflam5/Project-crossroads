#!/usr/bin/env python3
"""Original GBA Theater stage art; inspected HGSS captures are references only.

A private secondary repacks the 25 historical Temple metatiles used by this
room. Their visible pixels/attributes/IDs stay fixed. No shared Temple graphics
or engine capacity is changed. New backdrop and rope art append after them.
"""
import argparse, functools, io, json, struct
from pathlib import Path
from tileset_registration import upsert
from PIL import Image, ImageDraw

R=Path(__file__).resolve().parents[2]
D=R/'data/tilesets/secondary/hgss_theater'
A=R/'crossroads/hgss/art/theater'
USED=[512,513,516,533,534,535,536,537,538,539,540,545,546,547,548,558,559,560,561,562,563,564,565,888,895]
COLORS=[(0,0,0),(44,24,23),(71,38,29),(105,61,31),(144,91,35),(190,137,46),(227,185,71),(249,223,125),(255,242,182),(92,20,31),(144,31,39),(195,45,47),(231,74,56),(248,123,73),(241,225,189),(126,113,89)]

def artwork():
    # Hand-authored indexed pixels, not sampled/resized HGSS image data. Gold
    # stage crest, red hanging lanterns, timber beams and cream front ropes.
    bg=Image.new('P',(192,32),2); bg.putpalette(sum((list(c) for c in COLORS),[])+[0]*720)
    q=ImageDraw.Draw(bg)
    q.rectangle((0,0,191,3),fill=1);q.line((0,4,191,4),fill=5)
    for x in range(0,192,16):q.line((x,5,x,31),fill=3)
    q.rectangle((0,25,191,31),fill=5);q.line((0,26,191,26),fill=8);q.line((0,30,191,30),fill=3)
    q.pieslice((56,-3,135,48),180,360,fill=4,outline=7,width=2)
    q.arc((61,1,130,44),180,360,fill=6,width=2)
    q.rectangle((75,18,116,24),fill=3);q.line((76,18,115,18),fill=6)
    q.rectangle((89,4,102,16),fill=6);q.rectangle((91,5,100,15),fill=4)
    q.ellipse((92,6,99,13),outline=8,width=1);q.line((95,7,95,12),fill=7);q.line((93,10,98,10),fill=7)
    for cx in (12,36,60,132,156,180):
        q.line((cx,2,cx,5),fill=7);q.rectangle((cx-5,6,cx+5,21),fill=9)
        q.rectangle((cx-4,7,cx+4,20),fill=11);q.line((cx-3,8,cx-3,19),fill=13)
        q.line((cx,7,cx,20),fill=12);q.line((cx+3,8,cx+3,19),fill=10)
        q.line((cx-4,6,cx+4,6),fill=7);q.line((cx-4,21,cx+4,21),fill=6)
        q.line((cx-4,9,cx+4,9),fill=10);q.line((cx-4,18,cx+4,18),fill=10)
        q.line((cx,22,cx,24),fill=6)
    # Repeated rope section keeps every source gap/step open. Only the blocked
    # riser cells use this drawing; it never changes the collision footprint.
    rope=Image.new('P',(16,16),2);rope.putpalette(bg.getpalette());q=ImageDraw.Draw(rope)
    q.rectangle((0,11,15,15),fill=3);q.line((0,11,15,11),fill=5)
    q.line([(0,4),(3,6),(7,7),(11,6),(15,4)],fill=14,width=2)
    q.rectangle((0,1,2,14),fill=15);q.rectangle((13,1,15,14),fill=15)
    q.ellipse((0,0,3,3),fill=8);q.ellipse((12,0,15,3),fill=8)
    return bg,rope

def build(check=False,preview=None):
    temple=R/'data/tilesets/secondary/hgss_temple'
    original=Image.open(temple/'tiles.png');meta=list(struct.unpack('<'+str((temple/'metatiles.bin').stat().st_size//2)+'H',(temple/'metatiles.bin').read_bytes()))
    oldattrs=list(struct.unpack('<'+str((temple/'metatile_attributes.bin').stat().st_size//2)+'H',(temple/'metatile_attributes.bin').read_bytes()))
    sheet=Image.new('P',(128,256));sheet.putpalette(original.getpalette());glyphs={bytes(64):0};cursor=1
    def pack(pix,bank=6,flips=0):
        nonlocal cursor
        key=pix.tobytes()
        if key not in glyphs:
            assert cursor<512,('Private Theater graphics capacity',cursor)
            glyphs[key]=cursor;sheet.paste(pix,(cursor%16*8,cursor//16*8));cursor+=1
        return (512+glyphs[key])|(bank<<12)|flips
    words=[0x6200]*len(meta);attrs=[0x1000]*len(oldattrs)
    for n in USED:
        k=n-512;attrs[k]=oldattrs[k]
        for j,v in enumerate(meta[k*8:k*8+8]):
            tile=v&1023
            if tile<512:words[k*8+j]=v;continue
            i=tile-512;pix=original.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8));words[k*8+j]=pack(pix,v>>12,v&0xc00)
    backdrop,rope=artwork();specs={}
    for name,im in [('stage_backdrop',backdrop),('stage_rope',rope)]:
        specs[name]=dict(start=512+len(attrs),width=im.width//16,height=im.height//16)
        for y in range(im.height//16):
            for x in range(im.width//16):
                refs=[pack(im.crop((x*16+dx,y*16+dy,x*16+dx+8,y*16+dy+8)),7) for dx,dy in [(0,0),(8,0),(0,8),(8,8)]]
                words.extend([0x6200]*4+refs);attrs.append(0x1000)
    assert len(attrs)<=512
    manifest=dict(specs=specs,tiles=cursor,metatiles=len(attrs),retained_temple_metatiles=USED,palette_bank=7,source='Original indexed GBA pixel drawing guided by inspected final HGSS Theater screenshots; no source image pixels imported',reference_urls=['https://www.pokepedia.fr/images/f/f6/Salle_de_Danse_Rosalia_HGSS.png','https://www.pokebip.com/pages/jeux-video/pokemon-heartgold-soulsilver/soluce-du-jeu/images/figure83.png'])
    if preview:
        target=Path(preview);target.parent.mkdir(parents=True,exist_ok=True);rgb=Image.new('RGB',(192,64));rgb.paste(backdrop.convert('RGB'),(0,0))
        for x in range(12):rgb.paste(rope.convert('RGB'),(x*16,48))
        rgb.save(target);print('Original native Theater stage preview:',target);return manifest
    def write(p,b):
        if isinstance(b,str):b=b.encode()
        if check:assert p.exists() and p.read_bytes()==b,('Regenerate private Theater',str(p))
        elif not p.exists() or p.read_bytes()!=b:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    if check:assert Image.open(D/'tiles.png').tobytes()==sheet.tobytes()
    else:D.mkdir(parents=True,exist_ok=True);sheet.save(D/'tiles.png',bits=4)
    write(D/'metatiles.bin',struct.pack('<'+str(len(words))+'H',*words));write(D/'metatile_attributes.bin',struct.pack('<'+str(len(attrs))+'H',*attrs))
    for i in range(16):
        src=temple/f'palettes/{i:02}.pal';content=src.read_bytes()
        if i==7:content=('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in COLORS)+'\n').replace('\n','\r\n').encode()
        write(D/f'palettes/{i:02}.pal',content)
    write(A/'manifest.json',json.dumps(manifest,indent=2)+'\n')
    for n,im in [('stage_backdrop',backdrop),('stage_rope',rope)]:
        b=io.BytesIO();im.save(b,format='PNG',bits=4,transparency=0);write(A/(n+'.png'),b.getvalue())
    begin='// BEGIN ECRUTEAK THEATER STAGE';end='// END ECRUTEAK THEATER STAGE'
    blocks={
      'headers.h':'const struct Tileset gTileset_HgssTheater = { .isCompressed=TRUE, .isSecondary=TRUE, .tiles=gTilesetTiles_HgssTheater, .palettes=gTilesetPalettes_HgssTheater, .metatiles=gMetatiles_HgssTheater, .metatileAttributes=gMetatileAttributes_HgssTheater, .callback=NULL };',
      'graphics.h':'const u32 gTilesetTiles_HgssTheater[] = INCGFX_U32("data/tilesets/secondary/hgss_theater/tiles.png", ".4bpp.fastSmol");\nconst u16 gTilesetPalettes_HgssTheater[][16] = {\n'+''.join(f' INCGFX_U16("data/tilesets/secondary/hgss_theater/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};',
      'metatiles.h':'const u16 gMetatiles_HgssTheater[] = INCBIN_U16("data/tilesets/secondary/hgss_theater/metatiles.bin");\nconst u16 gMetatileAttributes_HgssTheater[] = INCBIN_U16("data/tilesets/secondary/hgss_theater/metatile_attributes.bin");'}
    for n,block in blocks.items():
        p=R/'src/data/tilesets'/n;text=p.read_text();section=begin+'\n#if !IS_FRLG\n'+block+'\n#endif\n'+end
        text=upsert(text,begin,end,section)
        write(p,text)
    p=R/'include/tilesets.h';text=p.read_text();section=begin+'\n#if !IS_FRLG\nextern const struct Tileset gTileset_HgssTheater;\n#endif\n'+end
    text=upsert(text,begin,end,section,externs=True)
    write(p,text)
    print('Private Theater stage:',cursor,'graphics;',len(attrs),'metatiles; shared Temple unchanged')
    return manifest

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--preview');a=p.parse_args();build(a.check,a.preview)
