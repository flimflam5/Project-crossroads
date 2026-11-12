#!/usr/bin/env python3
"""Original HGSS-directed lighthouse surfaces, independent of maritime/Port art.

The parent landmark generator calls patch() before its final writes. All six floors and the existing balcony
keep their exact QA09 geometry, attrs, behaviors, actors, scripts and IDs.
Only private drawing references change. No source screenshot pixels are used.
"""
import argparse, functools, io, json, re, struct, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
from tileset_registration import upsert

R = Path(__file__).resolve().parents[2]
BASE = '285cfa4ebddcb390a8a5bde6116748cbb5eaba6b'
NAMES = [f'OlivineCity_Lighthouse_{i}F' for i in range(1, 7)]
BAL = 'OlivineCity_Lighthouse_Balcony'
NAMES.append(BAL)
SOURCE = 'data/tilesets/secondary/hgss_olivine_landmarks'
DEST = 'data/tilesets/secondary/hgss_olivine_lighthouse'
SYMBOL = 'gTileset_HgssOlivineLighthouse'
MARKER = 'HGSS OLIVINE LIGHTHOUSE VISUALS'
MANIFEST = 'crossroads/hgss/qa10/lighthouse-art-manifest.json'
INNER_CORE_CONTRACT = 'crossroads/hgss/qa10/lighthouse-inner-core-b4-contract.json'

@functools.lru_cache(None)
def baseline(path):
    return subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=R)

def words(b):
    return list(struct.unpack('<' + str(len(b) // 2) + 'H', b))

def packed(v):
    return struct.pack('<' + str(len(v)) + 'H', *v)

PALETTES = {
    7: [(0,0,0),(128,128,152),(160,160,176),(96,104,128),(104,112,136),
        (136,144,160),(72,80,96),(32,64,160),(72,96,200),(24,40,120),
        (112,64,48),(160,104,64),(88,96,112),(192,184,192),(16,24,32),(208,208,216)],
    9: [(0,0,0),(72,128,144),(96,152,168),(56,104,120),(136,80,96),
        (160,104,112),(176,192,184),(200,208,200),(152,168,160),
        (80,104,96),(96,120,112),(64,80,72),(152,128,64),(48,64,56),
        (184,200,192),(216,224,216)],
    10: [(0,0,0),(216,216,216),(176,184,184),(128,144,144),(152,192,200),
         (208,224,224),(168,144,80),(112,72,40),(160,112,64),(72,40,24),
         (200,96,48),(240,160,96),(160,56,40),(200,88,56),(96,40,32),
         (240,240,224)],
    12: [(0,0,0),(176,136,152),(192,152,168),(144,104,120),(160,120,136),
         (64,208,224),(32,144,176),(160,240,240),(32,96,136),
         (120,176,192),(192,216,216),(224,240,232),(112,144,144),
         (200,176,96),(48,64,72),(160,184,184)]
}

def indexed(size, color, bank):
    im = Image.new('P', size, color)
    im.putpalette([v for c in PALETTES[bank] for v in c] + [0] * 720)
    return im

def floor_image(kind, x=0, y=0):
    """New opaque native motifs: every drawn floor pixel has a nonzero index."""
    bank = 7 if kind == 'paving' else 12 if kind == 'pink' else 9
    im = indexed((16,16), 1 if kind in ('teal','pink','paving') else 6 if kind == 'pale' else 9, bank)
    d = ImageDraw.Draw(im)
    if kind == 'pale':
        # Light diamond patterned stone outside the visitor-deck runner.
        for a,b in [(0,0),(8,8),(16,0),(0,16),(16,16)]:
            d.line([(a,b-6),(a+6,b),(a,b+6),(a-6,b),(a,b-6)], fill=7)
        d.point((7,0), fill=8); d.point((15,8), fill=8)
    elif kind == 'teal':
        d.line((0,0,15,0),fill=3);d.line((0,8,15,8),fill=3)
        d.line((0,1,15,1),fill=2);d.line((0,9,15,9),fill=2)
        d.line((7 if y%2 else 3,1,7 if y%2 else 3,7),fill=3)
        d.line((3 if y%2 else 11,9,3 if y%2 else 11,15),fill=3)
    elif kind == 'boards':
        # Vertical weathered boards and restrained original cracked seams.
        d.line((0,0,0,15),fill=11);d.line((8,0,8,15),fill=11)
        d.line((1,0,1,15),fill=10);d.line((9,0,9,15),fill=10)
        if (x+2*y)%7==0:
            d.line([(5,1),(4,5),(6,8),(5,12),(6,15)],fill=13)
        if (x+3*y)%5==0:d.line((9,7,15,7),fill=11)
    elif kind == 'paving':
        for yy in range(-16,32,8):
            d.line((0,yy,15,yy+15),fill=3)
            d.line((0,yy+1,15,yy+16),fill=2)
        for xx in range(-8,24,8):d.line((xx,0,xx-7,7),fill=3)
    elif kind == 'pink':
        for a,b in [(0,0),(8,8)]:
            d.rectangle((a+1,b+1,a+6,b+6),outline=3)
            d.line((a+2,b+2,a+5,b+2),fill=2)
            d.line((a+2,b+3,a+2,b+5),fill=2)
        d.point((8,0),fill=4);d.point((0,8),fill=4)
    return bank, im

def runner(n, x, y):
    if n == NAMES[0]: return 3 <= x <= 13 and 5 <= y <= 16
    if n == NAMES[1]: return ((2 <= x <= 4 and 5 <= y <= 16)
                              or (2 <= x <= 14 and 14 <= y <= 16)
                              or (12 <= x <= 14 and 8 <= y <= 16))
    return False

def floor_at(n, x, y):
    if n==BAL:return floor_image('paving',x,y)
    if n in NAMES[:2]:
        inside = runner(n,x,y);bank,im = floor_image('teal' if inside else 'pale',x,y)
        if inside:
            d=ImageDraw.Draw(im)
            # Two burgundy lines on the actual exposed edge, no collision change.
            for dx,dy,box1,box2 in [(-1,0,(0,0,0,15),(2,0,2,15)),(1,0,(15,0,15,15),(13,0,13,15)),(0,-1,(0,0,15,0),(0,2,15,2)),(0,1,(0,15,15,15),(0,13,15,13))]:
                if not runner(n,x+dx,y+dy):d.line(box1,fill=4);d.line(box2,fill=5)
        return bank,im
    return floor_image('pink' if n==NAMES[5] else 'boards',x,y)

def wall_image(n, x, y):
    if n==BAL:
        parapet=x in (0,16) or y==16
        im=indexed((16,16),7 if parapet else 4,7);d=ImageDraw.Draw(im)
        if parapet:
            d.line((0,0,15,0),fill=8);d.line((0,8,15,8),fill=9)
            d.line((0,1,0,7),fill=9);d.line((8,9,8,15),fill=9)
            d.line((1,1,15,1),fill=8);d.line((0,9,15,9),fill=8)
        else:
            d.line((0,0,15,0),fill=6);d.line((0,15,15,15),fill=5)
            d.line((0,1,0,14),fill=6);d.line((1,1,1,14),fill=5)
            if y in(2,6,10):d.line((2,13,15,13),fill=6);d.line((2,14,15,14),fill=5)
            # The actual outside shell has one framed east-facing window,
            # not a repeated indoor window wall around every course.
            if x==12 and y==9:
                d.rectangle((2,3,13,13),fill=10,outline=6);d.rectangle((4,5,11,11),fill=12)
                d.line((4,6,10,6),fill=11)
        return 7,im
    if n==NAMES[5]:
        im=indexed((16,16),9,12);d=ImageDraw.Draw(im)
        d.rectangle((0,0,15,2),fill=12);d.rectangle((0,13,15,15),fill=12)
        d.polygon([(0,2),(3,2),(15,12),(15,15),(12,15),(0,5)],fill=11)
        d.line((5,3,14,11),fill=10);d.point((8,1),fill=13)
        return 12,im
    im=indexed((16,16),1,10);d=ImageDraw.Draw(im)
    d.line((0,0,15,0),fill=3);d.line((0,1,15,1),fill=2)
    d.line((0,12,15,12),fill=3);d.rectangle((0,13,15,15),fill=2)
    d.line((0,2,0,11),fill=2);d.line((15,2,15,11),fill=2)
    outer = x<=3 or x>=13 or y<=4 or y>=17
    if n in NAMES[2:5] and outer:
        d.rectangle((0,13,15,15),fill=6);d.line((0,12,15,12),fill=9)
        # Pale arched windows repeat only on exposed upper/perimeter wall.
        if (x+y)%3==0:
            d.pieslice((3,1,12,9),180,360,fill=5,outline=3)
            d.rectangle((3,5,12,11),fill=5,outline=3)
            d.line((7,3,7,10),fill=4);d.line((4,7,11,7),fill=4)
    elif n in NAMES[:2] and y<=4 and x%4==0:
        d.ellipse((4,3,11,10),fill=4,outline=3);d.line((5,4,9,4),fill=5)
    return 10,im

def table_image(facing):
    # DS source gives each two-seat table a one-by-two solid footprint. A native
    # combined motif keeps that footprint rather than creating walkable chairs.
    im=indexed((16,32),0,10);d=ImageDraw.Draw(im)
    table=(7,2,15,29) if facing=='west' else (0,2,8,29)
    d.rectangle(table,fill=7,outline=9);d.line((table[0]+1,3,table[2]-1,3),fill=8)
    d.line((table[0]+1,16,table[2]-1,16),fill=9)
    x0=0 if facing=='west' else 10
    for yy in [3,19]:
        d.rectangle((x0,yy,x0+5,yy+9),fill=10,outline=9)
        d.line((x0+1,yy+1,x0+4,yy+1),fill=11)
        d.line((x0+1,yy+6,x0+4,yy+6),fill=11)
    return im

def lift_image():
    im=indexed((32,32),1,10);d=ImageDraw.Draw(im)
    d.rectangle((0,0,31,31),fill=3);d.rectangle((2,2,29,30),fill=14)
    for a,b in [(3,14),(17,28)]:
        d.rectangle((a,5,b,29),fill=12);d.line((a,5,b,5),fill=13)
        d.rectangle((a+2,8,b-2,12),fill=5,outline=6)
        d.line((a+2,18,b-2,18),fill=13);d.rectangle((a+2,21,b-2,26),outline=14)
    d.line((15,4,15,30),fill=9);d.line((16,4,16,30),fill=9)
    d.line((3,2,28,2),fill=15)
    return im

def stair_image():
    im=indexed((16,32),2,10);d=ImageDraw.Draw(im)
    d.rectangle((0,0,2,31),fill=12);d.rectangle((13,0,15,31),fill=12)
    d.line((1,0,1,31),fill=13);d.line((14,0,14,31),fill=13)
    for yy in range(3,31,5):
        d.line((3,yy,12,yy),fill=3);d.line((3,yy-1,12,yy-1),fill=15)
    return im

def housing_image():
    im=indexed((48,48),0,12);d=ImageDraw.Draw(im)
    d.ellipse((1,1,46,46),fill=6,outline=8)
    d.ellipse((3,2,44,43),fill=5,outline=7)
    d.ellipse((10,9,37,36),fill=0,outline=8)
    d.arc((3,2,44,43),185,315,fill=11,width=2)
    d.arc((5,4,42,41),30,160,fill=6,width=3)
    for box in [(6,10,11,12),(16,3,20,5),(32,7,36,9),(36,31,40,33),(9,35,13,37)]:d.rectangle(box,fill=7)
    return im

def inner_housing_panel(x, y, occupied):
    """A stitched cyan optical wall, distinct from OUTER diagonal glass.

    Rims/plinths occur only where the complete housing has an exposed boundary;
    there are no repeated horizontal bright/gold bands at every metatile row.
    """
    im = indexed((16, 16), 5, 12)
    d = ImageDraw.Draw(im)
    north = (x, y - 1) in occupied
    south = (x, y + 1) in occupied
    west = (x - 1, y) in occupied
    east = (x + 1, y) in occupied
    if not north:
        d.rectangle((0, 0, 15, 1), fill=7)
        d.line((0, 2, 15, 2), fill=6)
    if not south:
        d.rectangle((0, 13, 15, 15), fill=13)
        d.line((0, 12, 15, 12), fill=8)
    # A continuous vertical edge gradient suggests the curved source casing.
    # Neighbouring columns share plain cyan at their join, without brick seams.
    if not west:
        if x <= 7:
            d.line((0, 0, 0, 15), fill=8)
            d.rectangle((1, 0, 2, 15), fill=6)
        else:
            d.rectangle((0, 0, 1, 15), fill=7)
    if not east:
        if x >= 9:
            d.line((15, 0, 15, 15), fill=8)
            d.rectangle((13, 0, 14, 15), fill=6)
        else:
            d.rectangle((14, 0, 15, 15), fill=7)
    # Only the two real end posts at the southern access have vertical gold.
    if y == 13 and x in (7, 9):
        edge = 15 if x == 7 else 0
        d.line((edge, 2, edge, 12), fill=13)
    return im

def patch(rooms, maps, check=False):
    def write(path,b):
        p=R/path
        if isinstance(b,str):b=b.encode()
        if p.suffix=='.pal':b=b.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
        if check:assert p.exists() and p.read_bytes()==b,('Regenerate lighthouse visual asset',path)
        elif not p.exists() or p.read_bytes()!=b:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    def js(path,value):write(path,json.dumps(value,indent=2)+'\n')
    oldmeta=words(baseline(SOURCE+'/metatiles.bin'));oldattrs=words(baseline(SOURCE+'/metatile_attributes.bin'))
    meta=words((R/SOURCE/'metatiles.bin').read_bytes());attrs=words((R/SOURCE/'metatile_attributes.bin').read_bytes())
    assert len(attrs)<=512 and len(meta)==len(attrs)*8
    meta.extend([0]*(4096-len(meta)));attrs.extend([0]*(512-len(attrs)))
    sheet=Image.open(R/SOURCE/'tiles.png').copy();assert sheet.mode=='P' and sheet.size==(128,256)
    base_maps={n:words(baseline(f'data/layouts/{n}/map.bin'))for n in NAMES}
    used={v&1023 for n in NAMES for v in base_maps[n]}
    for n in NAMES:used.update(v&1023 for v in words(baseline(f'data/layouts/{n}/border.bin')))
    base_refs=list(meta)
    for m in used:
        if m>=512:assert attrs[m-512]==oldattrs[m-512],('Base LH attribute changed',m)
    usedglyph={v&1023 for m in used if m>=512 for v in base_refs[(m-512)*8:(m-511)*8] if (v&1023)>=512}
    freeglyph=[x for x in range(512,1024) if x not in usedglyph]
    freemeta=[x for x in range(512,1024) if x not in used]
    glyphs={};aliases={};added=[]
    def glyph(im):
        key=im.tobytes()
        if key not in glyphs:
            assert freeglyph,'Lighthouse private glyph capacity';v=freeglyph.pop(0);glyphs[key]=v
            sheet.paste(im,((v-512)%16*8,(v-512)//16*8))
        return glyphs[key]
    blank=glyph(indexed((8,8),0,9))
    def drawing(im,bank):return [bank<<12|glyph(im.crop((dx,dy,dx+8,dy+8)))for dx,dy in [(0,0),(8,0),(0,8),(8,8)]]
    def alloc(refs,attr,kind):
        key=(tuple(refs),attr)
        if key not in aliases:
            assert freemeta,'Lighthouse private metatile capacity';v=freemeta.pop(0);aliases[key]=v
            meta[(v-512)*8:(v-511)*8]=refs;attrs[v-512]=attr;added.append(dict(id=v,attribute=attr,kind=kind))
        return aliases[key]
    art=json.loads(baseline('crossroads/hgss/art/temple/manifest.json'))['specs']
    walls=set()
    for part in ['house_wall_stone','rail_h_stone','rail_v_stone','rail_h','rail_v']:
        a=art[part];walls.update(range(a['start'],a['start']+a['width']*a['height']))
    lift=lift_image();stairs=stair_image();housing=housing_image();deltas={};floor_samples={}
    for n in NAMES:
        q=rooms[n];w,h=q['width'],q['height'];t=q['tiles'];assert t==base_maps[n],('Unexpected previsual lighthouse change',n)
        rows=[]
        for y in range(h):
            for x in range(w):
                i=y*w+x;v=t[i];old=v&1023
                if old<512:continue  # Balcony's original sea/General resources stay exact.
                attr=oldattrs[old-512];refs=base_refs[(old-512)*8:(old-511)*8];kind=None
                bank,floor=floor_at(n,x,y);under=drawing(floor,bank)
                if n==NAMES[0] and (x,y)in[(3,8),(3,9),(13,8),(13,9),(3,13),(3,14),(13,13),(13,14)]:
                    facing='west' if x==3 else'east';basey=8 if y<12 else 13;im=table_image(facing).crop((0,(y-basey)*16,16,(y-basey+1)*16))
                    refs=under+drawing(im,10);kind='table with two orange seats, compressed source footprint'
                elif n==BAL and x in(8,9) and y in(11,12):
                    im=indexed((16,16),14,7)
                    if y==12:ImageDraw.Draw(im).rectangle((0,14,15,15),fill=3)
                    refs=drawing(im,7)+[9<<12|blank]*4;kind='balcony paired dark tower entrance'
                elif y in (2,3) and ((n==NAMES[0] and x==2) or(n==NAMES[1] and x==5)):
                    im=stairs.crop((0,(y-2)*16,16,(y-1)*16));refs=drawing(im,10)+[9<<12|blank]*4;kind='red handrail and metal visitor stair'
                elif y in (2,3) and ((n==NAMES[0] and x==3) or(n==NAMES[1] and x==6)):
                    if v&0x400:
                        im=indexed((16,16),2,10);ImageDraw.Draw(im).rectangle((0,0,2,15),fill=12);refs=drawing(im,10)+[9<<12|blank]*4
                    else:
                        im=indexed((16,16),0,10);ImageDraw.Draw(im).rectangle((0,0,2,15),fill=12);refs=under+drawing(im,10)
                    kind='visitor stair red side rail or solid support'
                elif x in (8,9) and y in(3,4) and n in(NAMES[0],NAMES[5]):
                    im=lift.crop(((x-8)*16,(y-3)*16,(x-7)*16,(y-2)*16));refs=drawing(im,10)+[9<<12|blank]*4;kind='red paired lift hatch'
                elif n==NAMES[5] and 7<=x<=9 and 5<=y<=7:
                    im=housing.crop(((x-7)*16,(y-5)*16,(x-6)*16,(y-4)*16));refs=under+drawing(im,12);kind='cyan optical housing with intentional original overlap'
                elif old in walls:
                    bank2,im=wall_image(n,x,y);refs=drawing(im,bank2)+[9<<12|blank]*4;kind='pale windows and wall, glass or perimeter trim'
                elif n==BAL and old==art['stone']['start']:
                    refs=under+[9<<12|blank]*4;kind='balcony diagonal paving'
                elif any(r&1023==513 for r in refs):
                    # Native wood glyph0x201 is the old underfloor. New floors
                    # are always opaqueBOTTOM, blankTOP when otherwise empty.
                    refs=[under[j%4] if j<4 and(r&1023 in(512,513))else (9<<12|blank) if j>=4 and r&1023==513 else r for j,r in enumerate(refs)]
                    if all(r&1023 in(512,513)for r in base_refs[(old-512)*8:(old-511)*8]):refs=under+[9<<12|blank]*4
                    kind='floor or preserved furniture over corrected opaque floor'
                if kind:
                    new=alloc(refs,attr,kind);t[i]=(v&0xfc00)|new
                    assert (t[i]&0xfc00)==(v&0xfc00) and attrs[new-512]==attr
                    if new!=old:rows.append(dict(x=x,y=y,before=old,after=new,attribute=attr,kind=kind))
        deltas[n]=rows
        floor_samples[n]=dict(width=w,height=h,changed_cells=len(rows),raw_before_sha256=__import__('hashlib').sha256(packed(base_maps[n])).hexdigest(),raw_after_sha256=__import__('hashlib').sha256(packed(t)).hexdigest())
    # B4 correction is intentionally late: first reproduce the reviewed B3
    # packing, then append aliases. This keeps all other map IDs/drawings exact.
    review=json.loads((R/INNER_CORE_CONTRACT).read_text())
    for n in NAMES:
        digest=__import__('hashlib').sha256(packed(rooms[n]['tiles'])).hexdigest()
        assert digest==review['baseline_raw_sha256'][n],('B3 lighthouse art prefix changed before scoped B4 fix',n,digest)
    core_deltas=[]
    occupied={(r['x'],r['y'])for r in review['cells']} | {(x,y)for y in range(5,8)for x in range(7,10)}
    n=NAMES[5];q=rooms[n];t=q['tiles'];w=q['width']
    for r in review['cells']:
        x,y=r['x'],r['y'];i=y*w+x;v=t[i]
        assert v==r['before_word'] and(v&0x400),('Unexpected6F optical housing source cell',x,y,v)
        attribute=attrs[(v&1023)-512];assert attribute==r['attribute']
        bank,floor=floor_at(n,x,y)
        refs=drawing(floor,bank)+drawing(inner_housing_panel(x,y,occupied),12)
        new=alloc(refs,attribute,'cyan inner optical housing, distinct from outer window ring')
        t[i]=(v&0xfc00)|new
        assert t[i]&0xfc00==v&0xfc00 and attrs[new-512]==attribute
        core_deltas.append(dict(x=x,y=y,before=v&1023,after=new,attribute=attribute,reason=r['reason']))
        existing=next((d for d in deltas[n]if d['x']==x and d['y']==y),None)
        if existing:
            existing['after']=new;existing['kind']='cyan inner optical housing, distinct from outer window ring'
        else:deltas[n].append(dict(x=x,y=y,before=v&1023,after=new,attribute=attribute,kind='opaque cyan model-corner housing instead of projector void'))
    assert len(core_deltas)==28
    floor_samples[n]['changed_cells']=len(deltas[n])
    floor_samples[n]['raw_after_sha256']=__import__('hashlib').sha256(packed(t)).hexdigest()
    assert max(sheet.tobytes())<16 and len(meta)==4096 and len(attrs)==512
    output=io.BytesIO();sheet.save(output,format='PNG',bits=4);write(DEST+'/tiles.png',output.getvalue());write(DEST+'/metatiles.bin',packed(meta));write(DEST+'/metatile_attributes.bin',packed(attrs))
    for i in range(16):
        b=(R/SOURCE/f'palettes/{i:02}.pal').read_bytes()
        if i in PALETTES:b=('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c))for c in PALETTES[i])+'\n').encode()
        write(DEST+f'/palettes/{i:02}.pal',b)
    sections={
        'src/data/tilesets/graphics.h':f'const u32 gTilesetTiles_HgssOlivineLighthouse[] = INCGFX_U32("{DEST}/tiles.png", ".4bpp.fastSmol");\nconst u16 gTilesetPalettes_HgssOlivineLighthouse[][16] = {{\n'+''.join(f' INCGFX_U16("{DEST}/palettes/{i:02}.pal", ".gbapal"),\n'for i in range(16))+'};',
        'src/data/tilesets/metatiles.h':f'const u16 gMetatiles_HgssOlivineLighthouse[] = INCBIN_U16("{DEST}/metatiles.bin");\nconst u16 gMetatileAttributes_HgssOlivineLighthouse[] = INCBIN_U16("{DEST}/metatile_attributes.bin");',
        'src/data/tilesets/headers.h':f'const struct Tileset {SYMBOL} = {{ .isCompressed=TRUE, .isSecondary=TRUE, .tiles=gTilesetTiles_HgssOlivineLighthouse, .palettes=gTilesetPalettes_HgssOlivineLighthouse, .metatiles=gMetatiles_HgssOlivineLighthouse, .metatileAttributes=gMetatileAttributes_HgssOlivineLighthouse, .callback=NULL }};',
        'include/tilesets.h':f'extern const struct Tileset {SYMBOL};'
    }
    for p,body in sections.items():
        begin='// BEGIN '+MARKER;end='// END '+MARKER;section=begin+'\n#if !IS_FRLG\n'+body+'\n#endif\n'+end
        write(p,upsert((R/p).read_text(),begin,end,section,externs=p=='include/tilesets.h'))
    manifest=dict(version='qa10-lighthouse-original-native-surfaces',baseline=BASE,symbol=SYMBOL,resource=DEST,source_reference_manifest='lighthouse-reference-manifest.json',maps=floor_samples,cell_deltas=deltas,allocated_metatiles=added,new_glyphs=len(glyphs),preserved_original_used_glyphs=len(usedglyph),reclaimed_only_unreferenced_metatile_ids=True,palette_banks=[7,9,10,12],geometry_ids_attributes_events_unchanged=True,adaptations=['Original16px GBA motifs follow inspected actualHGSS floor/fixture references; source screenshot pixels are never imported.','Four one-column/two-row source table solids contain combined table/two-seat motifs; no new chair blockers are introduced into the public walking lane.','The original3x3 native optical housing footprint and overlap are retained; cyan enclosure replaces its old blue/gray motif.','DS curved masonry/windows use original native16px panels along the existing physical wall footprint.', 'Balcony retains its stable physical shell/17x17 map while adopting the actual gray-purple masonry, diagonal paving, east window and blue parapet colors.'])
    manifest['b4_inner_housing_fix']=dict(contract=INNER_CORE_CONTRACT,baseline=review['baseline'],cells=core_deltas,changed_cells=28,outer_glass_and_old_cap_unchanged=True,all_other_map_raw_unchanged=True)
    js(MANIFEST,manifest)
    return SYMBOL

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true',required=True);a=p.parse_args()
    rooms={};maps={};layouts={l['id']:l for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
    for n in NAMES:
        maps[n]=json.loads((R/f'data/maps/{n}/map.json').read_text());l=layouts[maps[n]['layout']]
        rooms[n]=dict(width=l['width'],height=l['height'],tiles=words(baseline(f'data/layouts/{n}/map.bin')))
    patch(rooms,maps,check=True)
    for n in NAMES:
        l=layouts[maps[n]['layout']];assert l['secondary_tileset']==SYMBOL;assert (R/l['blockdata_filepath']).read_bytes()==packed(rooms[n]['tiles'])
    print('Private HGSS lighthouse original surfaces, exact geometry/attrs and deterministic generator: PASS')
