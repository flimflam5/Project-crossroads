"""Original native soil/stone modules for HGSS's genuinely vacant town court.

The source Ecruteak mosaic and background36,45 identify an open earthen court,
not a missing house. Only39 existing earth cells change drawing IDs; the sign,
all collision/elevations/behaviors/events/doors and the rest of the city remain.
Palette3 is the existing General terrain palette: no new palette or engine slot.
"""
from PIL import Image

META_BASE=0x3F0
RECT=(31,42,8,5)
SIGN=(36,45)

def drawing(column,row):
    # Byte-authored16px GBA terrain, not imported HGSS texture. A sparse fixed
    # grain avoids the old single-color debug-looking rectangle. Small stone
    # edging follows the light curb around the actual HGSS dirt court.
    pixels=bytearray([12]*256)
    for x,y,v in [(3,4,11),(11,3,13),(7,10,13),(13,13,11),(2,13,13)]:
        pixels[y*16+x]=v
    for y in range(16):
        for x in range(16):
            edge=(column==0 and x<2 or column==2 and x>=14
                  or row==0 and y<2 or row==2 and y>=14)
            if edge:pixels[y*16+x]=3 if x%16 in (0,15) or y%16 in (0,15) else 4
    return Image.frombytes('P',(16,16),bytes(pixels))

def assets(alloc,words,attrs,specs,empty):
    # High previously unused metatile IDs leave the owner Gym's established
    # first-free allocation and all old city metatile IDs intact.
    offset=META_BASE-512
    assert len(attrs)<=offset and len(words)==len(attrs)*8
    words.extend([0]*(offset*8-len(words)));attrs.extend([0]*(offset-len(attrs)))
    for row in range(3):
        for col in range(3):
            im=drawing(col,row)
            ground=[alloc(im.crop((x,y,x+8,y+8)),3) for x,y in [(0,0),(8,0),(0,8),(8,8)]]
            words.extend(ground+[empty]*4);attrs.append(0x1000)
    specs['courtyard_soil']=dict(start=META_BASE,width=3,height=3,palette=3,
                                rectangle=list(RECT),preserved_sign=list(SIGN),
                                public_cells=39,source='HGSS Ecruteak central vacant directory court')

def stamp(tiles,width,height,specs):
    x0,y0,w,h=RECT;assert width==height==64
    for y in range(y0,y0+h):
        for x in range(x0,x0+w):
            if (x,y)==SIGN:continue
            i=y*width+x;old=tiles[i]
            assert old==0x3000|specs['earth'],('Unexpected court cell',x,y,hex(old))
            col=0 if x==x0 else 2 if x==x0+w-1 else 1
            row=0 if y==y0 else 2 if y==y0+h-1 else 1
            tiles[i]=(old&~1023)|specs['courtyard_soil']['start']+row*3+col
