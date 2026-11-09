#!/usr/bin/env python3
"""Convert original architecture/leader sources to native, bounded GBA assets."""
import json,struct,hashlib,argparse
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2]
ART=R/'crossroads/art/western'
CITY=R/'data/tilesets/secondary/western_city'

def crop(im,box):
    im=im.crop(box);a=im.getchannel('A').point(lambda v:255 if v>=160 else 0)
    # Ignore disconnected generation specks by using the dominant alpha component.
    w,h=im.size;b=bytearray(a.tobytes());best=[]
    for i in range(w*h):
        if not b[i]:continue
        q=[i];b[i]=0;xs=[];ys=[]
        while q:
            n=q.pop();x=n%w;y=n//w;xs.append(x);ys.append(y)
            for z in (n-1 if x else -1,n+1 if x<w-1 else -1,n-w if y else -1,n+w if y<h-1 else -1):
                if z>=0 and b[z]:b[z]=0;q.append(z)
        if len(xs)>len(best):best=xs;bounds=(min(xs),min(ys),max(xs)+1,max(ys)+1)
    im.putalpha(a);return im.crop(bounds)

def palette(images):
    strip=Image.new('RGB',(sum(i.width for i in images),max(i.height for i in images)),(0,0,0));x=0
    for im in images:strip.paste(im.convert('RGB'),(x,0));x+=im.width
    p=strip.quantize(colors=15,method=Image.Quantize.MEDIANCUT).getpalette()[:45]
    return [0,0,0]+p

def indexed(im,pal):
    ref=Image.new('P',(1,1));ref.putpalette(pal+[0]*(768-len(pal)))
    q=im.convert('RGB').quantize(palette=ref,dither=Image.Dither.NONE)
    vals=bytearray(q.tobytes());alpha=im.getchannel('A').tobytes()
    # Zero is reserved for transparency; remap visible black to nearest nonzero.
    colors=[pal[i:i+3] for i in range(3,48,3)]
    rgb=im.convert('RGB').tobytes()
    for n in range(len(vals)):
        if alpha[n]<128:vals[n]=0
        elif vals[n]==0:
            c=rgb[n*3:n*3+3];vals[n]=1+min(range(15),key=lambda j:sum((c[k]-colors[j][k])**2 for k in range(3)))
    out=Image.frombytes('P',im.size,bytes(vals));out.putpalette(pal);return out

def palfile(path,p):
    path.write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,p[i:i+3])) for i in range(0,48,3))+'\n')

def build():
    CITY.mkdir(parents=True,exist_ok=True)
    meta_path=ART/'preserved-city-metatiles.json'
    base=R/'data/tilesets/secondary/slateport'
    if not meta_path.exists():
        ids=set()
        for n in ['OlivineCity','EcruteakCity','JohtoRoute38','JohtoRoute39']:
            b=(R/f'data/layouts/{n}/map.bin').read_bytes();ids.update(x&1023 for x in struct.unpack('<'+str(len(b)//2)+'H',b))
        meta_path.write_text(json.dumps(sorted(ids))+'\n')
    preserved=json.loads(meta_path.read_text());old=(base/'metatiles.bin').read_bytes();words=list(struct.unpack('<'+str(len(old)//2)+'H',old))
    refs={v&1023 for i in preserved if i>=512 for v in words[(i-512)*8:(i-511)*8]}
    free=[i for i in range(512) if i+512 not in refs and i not in range(224,228)]
    tiles=Image.open(base/'tiles.png').copy();attrs=list(struct.unpack('<406H',(base/'metatile_attributes.bin').read_bytes()))
    source=Image.open(ART/'architecture-source.png').convert('RGBA');W,H=source.size
    specs=[('lighthouse',(0,0,600,450),(48,80),8),('burned',(600,0,W,450),(64,64),9),('bell',(0,450,600,990),(48,96),8),('barn',(600,450,W,990),(64,48),9),('theater',(0,990,600,H),(64,48),11),('house',(600,990,W,H),(48,48),11)]
    ims={n:crop(source,b).resize(size,Image.Resampling.LANCZOS) for n,b,size,p in specs}
    pals={p:palette([ims[n] for n,b,s,bank in specs if bank==p]) for p in (8,9,11)}
    for i in range(16):
        (CITY/'palettes').mkdir(exist_ok=True)
        if i in pals:palfile(CITY/f'palettes/{i:02}.pal',pals[i])
        else:(CITY/f'palettes/{i:02}.pal').write_bytes((base/f'palettes/{i:02}.pal').read_bytes())
    manifest={};cursor=0
    under=words[2*8:2*8+4] # Existing promenade bottom layer.
    for name,box,size,bank in specs:
        im=indexed(ims[name],pals[bank]);im.save(ART/f'{name}-native.png',bits=4)
        start=512+len(attrs);w,h=size[0]//16,size[1]//16
        for y in range(h):
            for x in range(w):
                top=[]
                for dx,dy in [(0,0),(8,0),(0,8),(8,8)]:
                    assert cursor<len(free),'City tile capacity exceeded'
                    slot=free[cursor];cursor+=1
                    piece=im.crop((x*16+dx,y*16+dy,x*16+dx+8,y*16+dy+8))
                    tiles.paste(piece,(slot%16*8,slot//16*8));top.append((slot+512)|(bank<<12))
                words.extend(under+top)
                attrs.append((0x1000 if y>=h-2 else 0) | (0x60 if y==h-1 and x==w//2 else 0))
        manifest[name]={'start':start,'width':w,'height':h,'door_x':w//2,'door_y':h-1}
    # Johto-only tree roots: same native graphics, ground layer behind sprites.
    general=(R/'data/tilesets/primary/general/metatiles.bin').read_bytes()
    assert 512+len(attrs)==0x3e8
    for root in (0x1e6,0x1e7):
        words.extend(struct.unpack('<8H',general[root*16:(root+1)*16]));attrs.append(0x1000)
    assert len(attrs)<=512
    tiles.save(CITY/'tiles.png',bits=4)
    (CITY/'metatiles.bin').write_bytes(struct.pack('<'+str(len(words))+'H',*words))
    (CITY/'metatile_attributes.bin').write_bytes(struct.pack('<'+str(len(attrs))+'H',*attrs))
    manifest['tile_slots']=free[:cursor]
    manifest['source_sha256']=hashlib.sha256((ART/'architecture-source.png').read_bytes()).hexdigest()
    (ART/'architecture.json').write_text(json.dumps(manifest,indent=2)+'\n')
    # Shared GenericBuilding graphics with dedicated ladder behaviors, no old ID changes.
    dest=R/'data/tilesets/secondary/western_interiors';dest.mkdir(exist_ok=True)
    g=R/'data/tilesets/secondary/generic_building';m=bytearray((g/'metatiles.bin').read_bytes());a=bytearray((g/'metatile_attributes.bin').read_bytes())
    for target,src in [(0x3fc,0x20b),(0x3fd,0x219)]:
        m[(target-512)*16:(target-511)*16]=m[(src-512)*16:(src-511)*16]
        struct.pack_into('<H',a,(target-512)*2,0x61)
    (dest/'metatiles.bin').write_bytes(m);(dest/'metatile_attributes.bin').write_bytes(a)
    # Trainer portraits and fixed front-facing arena NPCs share each character palette.
    src=Image.open(ART/'leaders-source.png').convert('RGBA')
    for name,frontbox,owbox in [('jasmine',(30,20,580,860),(100,880,500,1312)),('morty',(610,20,1199,860),(690,880,1199,1312))]:
        front=crop(src,frontbox);front.thumbnail((62,62),Image.Resampling.LANCZOS)
        f=Image.new('RGBA',(64,64));f.alpha_composite(front,((64-front.width)//2,64-front.height))
        ow=crop(src,owbox);ow.thumbnail((16,28),Image.Resampling.LANCZOS)
        o=Image.new('RGBA',(16,32));o.alpha_composite(ow,((16-ow.width)//2,32-ow.height))
        p=palette([f,o]);d=R/f'graphics/trainers/crossroads_{name}';d.mkdir(exist_ok=True)
        indexed(f,p).save(d/'front.png',bits=4);indexed(o,p).save(d/'overworld.png',bits=4);palfile(d/'leader.pal',p)
    print('Native architecture/leader conversion: PASS;',cursor,'new tile slots,',len(attrs),'total metatiles')

if __name__=='__main__':build()
