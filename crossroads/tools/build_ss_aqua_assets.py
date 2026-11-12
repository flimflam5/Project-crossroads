#!/usr/bin/env python3
"""Original GBA pixel motifs for the source-shaped, docked S.S. Aqua.

The actual HGSS room mosaics are visual references only. No pixels, palettes,
textures, models or scripts are sampled from them. Named patterns and furniture
are drawn directly in indexed native pixels, then packed into TWO private native
512-glyph sheets. Every actual map metatile lives in the private secondary pool.

``--output-root /tmp/... --no-register`` makes a review-only prototype without
touching game inputs. The coordinated city build calls generate() after the
baseline emulator is closed. Collision/door positions belong to build_ss_aqua.
"""
import argparse
import io
import json
import struct
from pathlib import Path

from PIL import Image, ImageDraw
from tileset_registration import upsert

R = Path(__file__).resolve().parents[2]
PRIMARY = 'data/tilesets/primary/hgss_ss_aqua'
SECONDARY = 'data/tilesets/secondary/hgss_ss_aqua'
ART = 'crossroads/hgss/art/ss_aqua'
SYMBOL_PRIMARY = 'HgssSSAquaPrimary'
SYMBOL_SECONDARY = 'HgssSSAqua'
REFERENCE_NAMES = ['SS_Aqua_1F_Rooms_HGSS.png', 'SS_Aqua_B1F_HGSS.png',
                   'SS_Aqua_Captain_Cabin_HGSS.png', 'SS_Aqua_1F_HGSS.png']

# Index zero is always transparent; all ground drawings use nonzero indices.
# Only the engine's actually loaded secondary banks6..12 are referenced.
PALETTES = {
    6: [(0,0,0),(43,28,22),(88,51,30),(131,70,31),(170,99,38),
        (201,139,53),(225,175,76),(246,214,128),(102,52,35),(156,75,43),
        (118,28,48),(171,45,67),(72,20,39),(206,75,96),(250,236,186),(58,34,28)],
    7: [(0,0,0),(26,36,63),(38,54,88),(54,76,114),(75,102,144),
        (108,139,172),(151,177,197),(204,218,220),(51,68,91),(78,105,132),
        (112,145,166),(169,198,206),(223,235,225),(45,70,84),(80,122,132),(20,29,45)],
    8: [(0,0,0),(30,35,39),(55,62,64),(80,88,88),(110,119,114),
        (144,151,138),(178,183,162),(214,216,190),(64,76,74),(97,111,105),
        (133,145,129),(182,192,166),(94,99,77),(197,174,70),(236,213,104),(238,239,216)],
    9: [(0,0,0),(31,40,46),(60,79,92),(99,126,136),(141,163,168),
        (184,199,190),(222,220,187),(247,237,207),(77,53,38),(122,84,53),
        (173,126,78),(112,123,126),(48,93,116),(136,194,210),(218,235,234),(0,0,0)],
    10:[(0,0,0),(35,34,34),(71,47,33),(107,68,42),(151,100,54),
        (190,141,80),(223,183,112),(245,221,170),(235,231,202),(69,109,94),
        (57,95,118),(138,180,188),(146,41,43),(205,74,57),(247,241,218),(126,170,92)],
    11:[(0,0,0),(31,43,62),(46,64,97),(66,93,143),(98,126,174),
        (148,174,205),(210,225,229),(115,132,142),(236,232,202),(105,93,133),
        (176,136,154),(103,72,48),(155,166,167),(48,57,72),(215,184,108),(65,111,117)],
    12:[(0,0,0),(29,48,38),(47,69,45),(64,88,47),(87,108,55),
        (116,135,72),(155,166,96),(200,204,138),(50,78,69),(74,111,93),
        (103,143,115),(150,177,139),(210,223,180),(46,70,59),(86,106,77),(230,229,188)],
}


def indexed(size, bank, color=0):
    im = Image.new('P', size, color)
    im.putpalette(sum((list(c) for c in PALETTES[bank]), []) + [0]*720)
    return im


def artwork():
    """Return original indexed images, palette banks and foreground-row hints."""
    art = {}

    def put(name, im, bank, fore=()):
        art[name] = dict(image=im, bank=bank, foreground_rows=list(fore))
        return ImageDraw.Draw(im)

    # Native sixteen-pixel patterns preserve distinct HGSS room identities.
    im=indexed((32,32),6,4);d=put('floor_orange',im,6)
    for x in (0,16):
        for y in (0,16):
            light=(x+y)%32==0;d.rectangle((x,y,x+15,y+15),fill=5 if light else 4)
            d.rectangle((x,y,x+15,y+15),outline=4 if light else 3)
            d.ellipse((x+1,y+1,x+14,y+14),fill=6 if light else 5,outline=7 if light else 6)
            d.ellipse((x+4,y+4,x+11,y+11),fill=5 if light else 4,outline=7 if light else 6)
            d.point((x+7,y+7),fill=7);d.point((x+8,y+8),fill=7)
    im=indexed((16,16),6,3);d=put('floor_officer',im,6)
    d.line((0,0,15,0),fill=4);d.line((0,0,0,15),fill=4)
    d.polygon([(8,4),(11,8),(8,11),(4,8)],fill=2);d.point((8,7),fill=6)
    im=indexed((32,32),6,5);d=put('floor_gold',im,6)
    d.rectangle((0,0,15,15),fill=6);d.rectangle((16,16,31,31),fill=6)
    for x in (0,16):
        for y in (0,16):
            d.ellipse((x+3,y+3,x+12,y+12),outline=7)
            d.line((x+7,y+1,x+7,y+14),fill=5)
            d.line((x+1,y+7,x+14,y+7),fill=5)
    im=indexed((16,16),6,12);d=put('floor_red',im,6)
    d.ellipse((0,0,15,15),outline=10);d.ellipse((3,3,12,12),outline=11)
    d.line((0,8,15,8),fill=10);d.line((8,0,8,15),fill=10)
    for x,y in ((3,3),(12,3),(3,12),(12,12)):d.point((x,y),fill=13)
    im=indexed((16,16),7,2);d=put('floor_blue',im,7)
    d.rectangle((0,0,15,15),outline=3)
    for x,y in ((4,4),(12,12)):
        d.line((x-1,y,x+1,y),fill=6);d.line((x,y-1,x,y+1),fill=6)
    d.point((12,4),fill=4);d.point((4,12),fill=4)
    im=indexed((16,16),6,3);d=put('floor_mustard',im,6)
    d.rectangle((1,1,14,14),outline=4);d.rectangle((3,3,12,12),outline=5)
    d.rectangle((5,5,10,10),outline=4)
    im=indexed((16,16),8,3);d=put('floor_metal',im,8)
    for x in (0,8):
        for y in (0,8):
            d.rectangle((x,y,x+7,y+7),fill=4,outline=2)
            d.line((x+1,y+1,x+6,y+1),fill=6);d.point((x+2,y+3),fill=5)
    im=indexed((16,16),12,3);d=put('floor_green',im,12)
    for x in range(0,16,4):d.line((x,0,x,15),fill=4)
    d.line((0,0,15,0),fill=2);d.line((0,15,15,15),fill=5)
    im=indexed((48,48),12);d=put('rug_green',im,12)
    d.rounded_rectangle((1,1,46,46),radius=3,fill=7)
    d.rectangle((3,3,44,44),fill=5);d.rectangle((5,5,42,42),fill=9)
    for x in range(7,42,4):d.line((x,6,x,41),fill=10)
    for y in range(7,42,8):d.line((6,y,41,y),fill=8)
    d.line((4,4,43,4),fill=12);d.line((4,43,43,43),fill=3)
    im=indexed((16,16),12,8);d=put('floor_crew',im,12)
    for x in range(0,16,4):d.line((x,0,x,15),fill=9)
    for y in range(0,16,4):d.line((0,y,15,y),fill=9)
    d.rectangle((0,0,15,15),outline=4)
    im=indexed((16,16),10,2);d=put('floor_wood',im,10)
    for y in (0,5,10,15):d.line((0,y,15,y),fill=1)
    d.line((0,1,15,1),fill=3);d.line((3,6,13,6),fill=3)
    d.line((4,1,4,4),fill=3);d.line((11,11,11,14),fill=3)
    im=art['floor_metal']['image'].copy();d=put('hazardfloor',im,8)
    d.rectangle((0,0,3,15),fill=1)
    for y in range(-4,16,6):d.polygon([(0,y+4),(0,y+6),(3,y+3),(3,y+1)],fill=14)
    im=indexed((16,16),9,15);put('void',im,9)

    # Walls are drawn below Joe; fixtures' top row alone can be an overhang.
    for name,blue in [('wall_ship',True),('wall_cabin',False)]:
        im=indexed((64,32),9,6);d=put(name,im,9)
        d.rectangle((0,0,63,2),fill=8 if blue else 4)
        d.line((0,3,63,3),fill=7)
        for x in range(0,64,16):
            d.line((x,4,x,23),fill=9 if blue else 5)
            d.line((x+1,4,x+1,23),fill=10 if blue else 7)
        d.rectangle((0,24,63,31),fill=3);d.line((0,24,63,24),fill=5)
        d.line((0,30,63,30),fill=1)
    im=indexed((64,32),8,5);d=put('wall_metal',im,8)
    d.rectangle((0,0,63,3),fill=2);d.line((0,4,63,4),fill=7)
    for x in range(0,64,16):d.line((x,4,x,28),fill=3)
    d.rectangle((0,25,63,31),fill=3);d.line((0,26,63,26),fill=6)
    im=indexed((16,32),9,6);d=put('porthole',im,9)
    d.rectangle((0,0,15,2),fill=4);d.line((0,3,15,3),fill=7)
    d.ellipse((2,7,13,18),fill=1);d.ellipse((3,8,12,17),fill=11)
    d.ellipse((5,9,11,15),fill=12);d.line((6,10,10,10),fill=13)
    d.point((4,11),fill=14);d.rectangle((0,24,15,31),fill=3)
    d.line((0,24,15,24),fill=5);d.line((0,30,15,30),fill=1)
    im=indexed((16,32),9,6);d=put('window',im,9)
    d.rectangle((2,5,13,22),fill=8);d.rectangle((3,6,12,20),fill=12)
    d.line((4,7,11,7),fill=14);d.line((8,7,8,20),fill=13)
    d.line((3,13,12,13),fill=11);d.rectangle((0,24,15,31),fill=3)
    im=indexed((16,16),9);d=put('painting',im,9)
    d.rectangle((1,2,14,12),fill=8);d.rectangle((2,3,13,11),fill=14)
    d.rectangle((3,4,12,10),fill=12);d.polygon([(3,9),(7,5),(10,8),(12,6),(12,10),(3,10)],fill=3)
    im=indexed((16,16),8);d=put('clock',im,8)
    d.ellipse((3,1,12,10),fill=1);d.ellipse((4,2,11,9),fill=14)
    d.line((8,3,8,6),fill=2);d.line((8,6,10,6),fill=2)

    def bed(name, bank, horizontal=False):
        W,H=(48,32)if horizontal else(32,48)
        im=indexed((W,H),bank);d=put(name,im,bank,(0,))
        d.rounded_rectangle((3,2,W-4,H-3),radius=3,fill=1)
        d.rectangle((4,3,W-5,H-5),fill=7 if bank==11 else 3)
        d.line((5,3,W-6,3),fill=6 if bank==11 else 6)
        if horizontal:
            d.rectangle((6,6,18,H-9),fill=8);d.rectangle((7,7,17,H-10),fill=6)
            d.rectangle((20,6,W-7,H-8),fill=4);d.line((22,7,W-8,7),fill=5)
            d.line((20,7,20,H-9),fill=2);d.line((23,H-10,W-8,H-10),fill=3)
        else:
            d.rectangle((6,6,W-7,16),fill=8);d.rectangle((7,7,W-8,14),fill=6 if bank==11 else 7)
            d.rectangle((6,18,W-7,H-8),fill=4);d.line((7,19,W-8,19),fill=5)
            d.line((7,20,7,H-9),fill=5);d.line((9,H-10,W-8,H-10),fill=3)
            d.line((9,21,W-9,21),fill=6 if bank==11 else 7)
            d.polygon([(7,18),(15,18),(7,25)],fill=6 if bank==11 else 7)
            d.line((10,H-12,W-9,H-12),fill=5)
        d.line((5,H-5,W-6,H-5),fill=2);d.rectangle((5,H-3,8,H-1),fill=1)
        d.rectangle((W-9,H-3,W-6,H-1),fill=1)
    bed('bed_blue',11);bed('bed_brown',10)

    for name,bank,fill in [('sofa_yellow',6,6),('sofa_orange',10,13),('bench_blue',11,4)]:
        if name=='sofa_orange':
            # The Captain mosaic has a vertical two-by-three sofa, not a
            # horizontal reception bench. Its six metatile IDs remain stable.
            im=indexed((32,48),bank);d=put(name,im,bank,(0,))
            d.rounded_rectangle((2,2,29,44),radius=3,fill=1)
            d.rectangle((4,4,26,41),fill=12)
            d.rectangle((8,5,25,39),fill=fill)
            d.line((9,6,24,6),fill=6)
            d.rectangle((3,4,7,42),fill=4);d.line((4,5,4,40),fill=6)
            for y in (20,35):d.line((9,y,24,y),fill=12)
            d.rectangle((3,3,27,7),fill=fill);d.line((4,4,26,4),fill=6)
            d.rectangle((3,39,27,43),fill=4);d.line((4,39,26,39),fill=6)
            d.rectangle((5,44,8,46),fill=1);d.rectangle((23,44,26,46),fill=1)
        else:
            im=indexed((48,32),bank);d=put(name,im,bank,(0,))
            d.rounded_rectangle((1,4,46,28),radius=3,fill=1)
            d.rectangle((4,5,43,20),fill=fill);d.line((5,6,42,6),fill=7 if bank==6 else 6)
            d.rectangle((5,18,42,25),fill=5 if bank==6 else 3)
            for x in (16,31):d.line((x,8,x,24),fill=4 if bank==6 else 2)
            d.rectangle((1,14,4,27),fill=fill);d.rectangle((43,14,46,27),fill=fill)
            d.rectangle((5,28,8,30),fill=1);d.rectangle((39,28,42,30),fill=1)

    im=indexed((16,48),11);d=put('bench_vertical',im,11,(0,))
    d.rounded_rectangle((1,2,14,45),radius=2,fill=1)
    d.rectangle((3,4,10,42),fill=4);d.line((3,4,10,4),fill=6)
    d.rectangle((11,3,13,43),fill=2);d.line((10,5,10,42),fill=5)
    for y in (16,30):d.line((3,y,10,y),fill=2)
    d.rectangle((2,43,13,46),fill=3);d.rectangle((3,46,5,47),fill=1)
    im=indexed((48,64),6);d=put('sofa_vertical',im,6,(0,))
    d.rounded_rectangle((3,2,44,61),radius=3,fill=1)
    d.rectangle((6,3,41,57),fill=6);d.line((7,4,40,4),fill=7)
    d.rectangle((30,5,41,55),fill=5)
    for y in (20,38):d.line((7,y,40,y),fill=4)
    d.rectangle((3,3,8,59),fill=7);d.rectangle((3,54,44,60),fill=5)
    d.rectangle((7,61,11,63),fill=1);d.rectangle((36,61,40,63),fill=1)

    def table(name,size,wood=False):
        W,H=size;im=indexed(size,10);d=put(name,im,10,(0,))
        d.rectangle((3,4,W-4,H-6),fill=2);d.rectangle((2,2,W-3,H-9),fill=5)
        d.rectangle((4,3,W-5,H-11),fill=6 if wood else 11)
        if not wood:
            for y in range(5,H-11,4):
                for x in range(5,W-5,4):d.rectangle((x,y,x+1,y+1),fill=8 if(x+y)%8 else 14)
        d.line((4,3,W-5,3),fill=8);d.line((3,H-8,W-4,H-8),fill=3)
        d.rectangle((5,H-6,8,H-2),fill=1);d.rectangle((W-9,H-6,W-6,H-2),fill=1)
    table('table',(32,32));table('table_wood',(32,32),True);table('galley_table',(48,80))
    table('table_wide',(64,32));table('table_square',(48,48))
    for name,bank,top,side in [('chair_red',10,13,12),('chair_green',12,6,4),
                               ('chair_yellow',6,7,5),('chair_orange',10,6,4)]:
        im=indexed((16,16),bank);d=put(name,im,bank)
        d.rounded_rectangle((3,3,12,12),radius=2,fill=1)
        d.rectangle((4,4,11,9),fill=top);d.rectangle((4,10,11,12),fill=side)
        d.line((5,4,10,4),fill=7 if bank!=10 else 14)
        d.rectangle((4,13,5,14),fill=1);d.rectangle((10,13,11,14),fill=1)

    im=indexed((32,32),10);d=put('cabinet',im,10,(0,))
    d.rectangle((3,1,28,30),fill=1);d.rectangle((4,2,27,28),fill=4)
    d.rectangle((6,4,25,14),fill=2);d.rectangle((6,17,25,26),fill=3)
    for x,c in [(7,6),(11,12),(15,10),(19,8),(23,6)]:
        d.rectangle((x,5,x+2,12),fill=c);d.line((x,17,x,25),fill=5)
    d.line((5,15,26,15),fill=6);d.line((5,28,26,28),fill=2)
    im=indexed((32,32),8);d=put('locker_crew',im,8,(0,))
    d.rectangle((2,1,29,30),fill=1);d.rectangle((3,2,28,28),fill=4)
    for x in (4,17):
        d.rectangle((x,4,x+10,26),outline=2);d.line((x+1,5,x+9,5),fill=6)
        for y in (8,11,14):d.line((x+2,y,x+8,y),fill=2)
        d.rectangle((x+7,19,x+8,22),fill=14)
    im=indexed((16,16),12);d=put('bin',im,12)
    d.ellipse((3,2,12,6),fill=1);d.rectangle((3,5,12,12),fill=8)
    d.ellipse((3,9,12,14),fill=8);d.ellipse((3,2,12,7),fill=5)
    d.ellipse((5,3,10,5),fill=1);d.line((4,8,4,11),fill=6)

    im=indexed((48,32),10);d=put('captain_desk',im,10,(0,))
    d.rectangle((1,9,46,29),fill=2);d.rectangle((2,3,45,22),fill=4)
    d.line((2,3,45,3),fill=6);d.line((2,23,45,23),fill=1)
    d.rectangle((7,6,35,18),fill=8)
    d.line([(9,14),(15,9),(21,11),(29,8),(33,12)],fill=9,width=2)
    d.rectangle((37,9,41,14),fill=11);d.line((38,8,40,8),fill=14)
    d.rectangle((5,27,9,31),fill=1);d.rectangle((38,27,42,31),fill=1)
    im=indexed((32,16),10);d=put('map_board',im,10)
    d.rectangle((1,1,30,14),fill=2);d.rectangle((3,3,28,12),fill=8)
    d.line([(4,10),(9,5),(16,8),(22,4),(27,9)],fill=9,width=2)
    d.rectangle((20,9,24,10),fill=4)

    # Desks, galley and engine controls retain distinct visual functions.
    for name,W,kind in [('desk_white',48,'white'),('tv_counter',80,'tv'),
                         ('galley_sink',32,'sink'),('galley_stove',32,'stove'),
                         ('galley_counter',32,'counter')]:
        im=indexed((W,32),8);d=put(name,im,8,(0,))
        d.rectangle((1,6,W-2,29),fill=2);d.rectangle((2,7,W-3,27),fill=5)
        d.rectangle((1,4,W-2,16),fill=7);d.line((2,5,W-3,5),fill=15)
        for x in range(8,W-4,16):d.line((x,18,x,26),fill=3)
        d.line((3,28,W-4,28),fill=1)
        if kind=='tv':
            d.rectangle((W//2-10,0,W//2+9,14),fill=1)
            d.rectangle((W//2-8,2,W//2+7,11),fill=8)
            d.line((W//2-7,3,W//2+6,3),fill=10)
            d.rectangle((W-18,8,W-14,13),fill=15);d.rectangle((W-11,10,W-8,13),fill=6)
        elif kind=='sink':
            d.rectangle((8,7,24,14),fill=2);d.rectangle((10,8,22,13),fill=4)
            d.line((15,4,15,10),fill=15);d.line((15,4,19,4),fill=15)
        elif kind=='stove':
            for x in (8,21):d.ellipse((x-4,7,x+3,13),fill=1);d.ellipse((x-2,8,x+1,11),fill=3)
            d.rectangle((5,18,26,26),fill=1);d.rectangle((7,20,24,24),fill=3)
        elif kind=='white':
            d.rectangle((3,6,W-4,14),fill=15)
            d.rectangle((W-13,1,W-7,7),fill=13);d.rectangle((W-11,0,W-9,3),fill=10)
    im=indexed((16,48),8);d=put('fridge',im,8,(0,))
    d.rectangle((1,1,14,46),fill=2);d.rectangle((2,2,13,44),fill=6)
    d.line((2,17,13,17),fill=3);d.line((3,3,12,3),fill=15)
    d.rectangle((10,8,11,13),fill=3);d.rectangle((10,23,11,33),fill=3)
    d.line((2,45,13,45),fill=1)

    im=indexed((128,96),8);d=put('engine',im,8,(0,))
    d.rounded_rectangle((1,1,126,94),radius=4,fill=1)
    d.rectangle((4,3,123,89),fill=3);d.line((4,3,123,3),fill=7)
    # Repeated mechanical cells pack once. This is an original pixel drawing,
    # not a shrunken 3D screenshot or a single undifferentiated gray rectangle.
    for x in range(8,120,16):
        d.rectangle((x,7,x+13,28),fill=2);d.line((x+1,8,x+12,8),fill=5)
        for y in range(11,27,4):d.line((x+2,y,x+11,y),fill=1)
        d.rectangle((x,35,x+13,59),fill=5);d.line((x+1,36,x+12,36),fill=7)
        d.ellipse((x+2,40,x+11,51),fill=2);d.ellipse((x+4,42,x+9,49),fill=4)
        d.rectangle((x+3,61,x+10,80),fill=2);d.line((x+4,62,x+4,77),fill=6)
    d.rectangle((5,82,122,89),fill=2);d.line((6,83,121,83),fill=6)
    for x in range(7,121,8):d.rectangle((x,85,x+3,88),fill=4)
    im=indexed((16,16),8,3);d=put('machine_panel',im,8)
    d.rectangle((0,0,15,15),outline=1);d.line((1,1,14,1),fill=6)
    for y in (4,7,10,13):d.line((3,y,12,y),fill=1)
    im=indexed((48,48),8);d=put('control_cabinet',im,8,(0,))
    d.rectangle((1,2,46,46),fill=1);d.rectangle((2,3,45,44),fill=4)
    for x in (4,19,34):
        d.rectangle((x,5,x+10,17),fill=2);d.rectangle((x+2,7,x+8,13),fill=8)
        d.line((x+2,8,x+7,8),fill=11)
        for y,c in ((22,14),(27,13),(32,6)):d.rectangle((x+2,y,x+4,y+2),fill=c)
        d.rectangle((x+6,22,x+8,35),fill=2)
    d.line((3,43,44,43),fill=2)
    im=indexed((16,32),8);d=put('engine_pipe',im,8,(0,))
    d.rectangle((5,0,11,31),fill=2);d.rectangle((6,0,9,31),fill=5)
    for y in (3,15,27):d.rectangle((3,y,13,y+2),fill=3);d.line((4,y,12,y),fill=7)

    for name,down in [('stairs_up',False),('stairs_down',True)]:
        im=indexed((32,32),8);d=put(name,im,8)
        d.rectangle((1,1,30,30),fill=1)
        for i in range(5):
            y=3+i*5;c=3+i//2 if not down else 5-i//2
            d.rectangle((3,y,28,y+3),fill=c);d.line((3,y,28,y),fill=7)
        d.rectangle((0,0,2,31),fill=3);d.rectangle((29,0,31,31),fill=3)
    im=indexed((16,32),8);d=put('ladder',im,8)
    d.rectangle((2,0,4,31),fill=2);d.rectangle((11,0,13,31),fill=2)
    for y in (2,10,18,26):d.rectangle((3,y,12,y+2),fill=6);d.line((3,y,12,y),fill=15)
    im=indexed((32,32),9);d=put('door_ship',im,9)
    d.rectangle((1,0,30,31),fill=1);d.rectangle((3,2,28,31),fill=8)
    d.rectangle((5,4,26,31),fill=15);d.line((3,2,28,2),fill=10)
    d.rectangle((1,27,30,31),fill=3);d.line((3,28,28,28),fill=5)
    im=indexed((32,16),9);d=put('life_ring',im,9)
    for cx in (8,24):
        d.ellipse((cx-6,1,cx+5,12),fill=1);d.ellipse((cx-5,2,cx+4,11),fill=7)
        d.ellipse((cx-2,5,cx+1,8),fill=0)
        d.line((cx-4,3,cx-2,5),fill=10,width=2);d.line((cx+1,8,cx+3,10),fill=10,width=2)
    # Source 1F model23 is a potted plant, never the round cabin wastebin.
    # Palette10 index15 was unused by every previous fixture; it now supplies
    # the leaf highlight without changing any existing drawing's colors.
    im=indexed((16,32),10);d=put('plant',im,10,(0,))
    d.line((7,10,7,23),fill=2);d.line((8,9,8,22),fill=9)
    for box in ((1,5,8,13),(6,1,13,10),(7,8,14,17),(1,11,9,19)):
        d.ellipse(box,fill=1)
        x,y,X,Y=box;d.ellipse((x+1,y+1,X-1,Y-1),fill=9)
        d.line((x+2,y+2,X-2,y+2),fill=15)
    d.rectangle((3,20,12,27),fill=12)
    d.rectangle((2,19,13,22),fill=13);d.line((3,19,12,19),fill=6)
    d.line((4,23,4,26),fill=13);d.line((5,28,10,28),fill=1)
    return art


# Only actual room/theme combinations receive private metatile aliases. These
# share glyphs; duplicating art arrays would exhaust a native resource pool.
BACKGROUND_THEMES = {
    'bed_blue':['blue','gold','red','mustard','crew'],
    'bed_brown':['green'],
    'sofa_yellow':['gold'], 'sofa_vertical':['gold'], 'sofa_orange':['green'], 'bench_blue':['orange','officer'], 'bench_vertical':['orange','officer'], 'rug_green':['green','blue'],
    'table':['blue','gold','mustard','metal'], 'table_wide':['blue'], 'table_square':['mustard'], 'table_wood':['gold'], 'galley_table':['metal'],
    'chair_red':['blue','green'], 'chair_green':['gold'], 'chair_yellow':['mustard'],
    'chair_orange':['metal'], 'cabinet':['blue','gold','red','mustard','green'],
    'locker_crew':['crew'], 'bin':['blue','gold','red','mustard','metal','green','crew'],
    'captain_desk':['green'], 'map_board':['green'], 'painting':['blue','gold','red','mustard'],
    'clock':['metal','crew'], 'desk_white':['red'], 'tv_counter':['red'],
    'galley_sink':['metal','mustard'], 'galley_stove':['metal'],
    'galley_counter':['metal','green'], 'fridge':['metal','green'],
    'engine':['metal'], 'control_cabinet':['metal'], 'engine_pipe':['metal'],
    'ladder':['metal','mustard'], 'stairs_up':['wood','metal'],
    'stairs_down':['wood','metal'], 'door_ship':['orange','officer','blue','gold','red','mustard','green'],
    'life_ring':['orange'],
}


def generate(check=False, output_root=None, register=True):
    out = Path(output_root).resolve() if output_root else R
    register = register and out == R
    art = artwork()
    sheets=[indexed((128,256),6),indexed((128,256),6)]
    sheets[0].paste(Image.new('P',(8,8),1),(8,0))
    sheets[0].paste(Image.new('P',(8,8),1),(32,8))  # engine BG3 filler glyph20
    glyphs={bytes(64):0,bytes([1])*64:1};cursor=2

    def pack(im,bank):
        nonlocal cursor
        key=im.tobytes()
        if key not in glyphs:
            if cursor==20:cursor+=1
            assert cursor<1024,('S.S.Aqua native two-sheet glyph capacity',cursor)
            n=cursor;cursor+=1;glyphs[key]=n
            sheets[n//512].paste(im,(n%16*8,n%512//16*8))
            for flags,part in ((0x400,im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                               (0x800,im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)),
                               (0xc00,im.transpose(Image.Transpose.FLIP_LEFT_RIGHT).transpose(Image.Transpose.FLIP_TOP_BOTTOM))):
                glyphs.setdefault(part.tobytes(),n|flags)
        return glyphs[key]|bank<<12

    metas=[];attrs=[];specs={};variants={};warp_variants={};south_facing_warp_variants={}

    def refs(im,x,y,bank):
        return [pack(im.crop((x+dx,y+dy,x+dx+8,y+dy+8)),bank)
                for dx,dy in ((0,0),(8,0),(0,8),(8,8))]

    def append(name,entry,theme=None):
        im=entry['image'];w,h=im.width//16,im.height//16
        spec=dict(start=512+len(attrs),width=w,height=h,
                  palette_bank=entry['bank'],foreground_rows=entry['foreground_rows'])
        floor=art['floor_'+theme]if theme else None
        for y in range(h):
            for x in range(w):
                a=refs(im,x*16,y*16,entry['bank'])
                if floor:
                    f=floor['image'];b=refs(f,(x*16)%f.width,(y*16)%f.height,floor['bank'])
                    # Body rows draw below Joe; upper overhang rows alone can
                    # cover him. Ground remains fully opaque in either case.
                    if y in entry['foreground_rows']:words=b+a
                    else:
                        # COVERED draws the original overlay plus its matching
                        # opaque floor below Joe, without palette remapping.
                        words=b+a
                    layer=0 if y in entry['foreground_rows'] else 0x1000
                else:
                    # Opaque original ground/wall glyphs belong below Joe.
                    words=a+[0]*4;layer=0
                metas.extend(words);attrs.append(layer)
        assert len(attrs)<=512,('S.S.Aqua private metatile capacity',len(attrs),name,theme)
        if theme:variants.setdefault(name,{})[theme]=spec
        specs.setdefault(name,spec)
        return spec

    for name,entry in art.items():
        if name=='plant':continue  # append after existing IDs and warp aliases
        if name in BACKGROUND_THEMES:
            for theme in BACKGROUND_THEMES[name]:append(name,entry,theme)
        else:append(name,entry)
    specs['hazard']=specs['hazardfloor']
    # All floor/ladder/door aliases retain the exact drawing/layer, changing only
    # the native non-directional warp behavior. No arrow is painted on ordinary
    # ground. Map scripts choose the actual source threshold positions.
    warp_specs=[spec for name,spec in specs.items()if name.startswith('floor_')]
    for name in ['stairs_up','stairs_down','ladder','door_ship']:
        warp_specs.extend(variants[name].values())
    for s in warp_specs:
        for i in range(s['width']*s['height']):
            n=s['start']+i
            if str(n)in warp_variants:continue
            new=512+len(attrs);attrs.append(attrs[n-512]|0x61)
            metas.extend(metas[(n-512)*8:(n-512)*8+8]);warp_variants[str(n)]=new
    # North-side destination mouths need native NON_ANIMATED_DOOR's south
    # facing/autostep, whereas LADDER retains the incoming direction. Only the
    # visible open bottom row of a door is a threshold; its solid lintel never
    # receives a fake warp merely to fill this mapping.
    south_ids=[]
    for name,spec in specs.items():
        if name.startswith('floor_'):south_ids.extend(range(spec['start'],spec['start']+spec['width']*spec['height']))
    for name in ('stairs_up','stairs_down'):
        for spec in variants[name].values():south_ids.extend(range(spec['start'],spec['start']+spec['width']*spec['height']))
    for spec in variants['door_ship'].values():
        south_ids.extend(range(spec['start']+(spec['height']-1)*spec['width'],spec['start']+spec['height']*spec['width']))
    for n in south_ids:
        new=512+len(attrs);attrs.append((attrs[n-512]&0xf000)|0x60)
        metas.extend(metas[(n-512)*8:(n-512)*8+8]);south_facing_warp_variants[str(n)]=new
        if str(n)in warp_variants:south_facing_warp_variants[str(warp_variants[str(n)])]=new
    append('plant',art['plant'],'orange')
    assert len(attrs)<=512,('S.S.Aqua including warp aliases exceeds native metas',len(attrs))
    manifest=dict(specs=specs,background_variants=variants,warp_variants=warp_variants,south_facing_warp_variants=south_facing_warp_variants,
        glyphs=cursor,primary_glyphs=min(cursor,512),secondary_glyphs=max(0,cursor-512),
        metatiles=len(attrs),primary_symbol='gTileset_'+SYMBOL_PRIMARY,
        secondary_symbol='gTileset_'+SYMBOL_SECONDARY,palette_banks=list(PALETTES),
        source='Original hand-authored indexed GBA pixel motifs after actual HGSS S.S.Aqua full-map references; no reference pixels imported',
        reference_names=REFERENCE_NAMES,layer_rule='Opaque ground beneath every fixture. Only named upper overhang rows draw above Joe; body rows use COVERED below him.',
        movement_contract='This asset generator changes no collision, map ID, event, warp position or story state. Source-shaped map generator owns those.')

    def write(path,content):
        p=out/path
        if isinstance(content,str):content=content.encode()
        if p.suffix=='.pal':content=content.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
        if check:assert p.exists()and p.read_bytes()==content,('Regenerate S.S.Aqua assets',str(p))
        elif not p.exists()or p.read_bytes()!=content:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(content)

    black=[(0,0,0)]*16
    for is_secondary,pool in enumerate([PRIMARY,SECONDARY]):
        b=io.BytesIO();sheets[is_secondary].save(b,format='PNG',bits=4);write(pool+'/tiles.png',b.getvalue())
        if is_secondary:
            write(pool+'/metatiles.bin',struct.pack('<'+str(len(metas))+'H',*metas))
            write(pool+'/metatile_attributes.bin',struct.pack('<'+str(len(attrs))+'H',*attrs))
        else:
            write(pool+'/metatiles.bin',struct.pack('<4096H',*([1]*4+[0]*4)*512))
            write(pool+'/metatile_attributes.bin',struct.pack('<512H',*([0]*512)))
        for bank in range(16):
            colors=PALETTES.get(bank,black)
            write(pool+f'/palettes/{bank:02}.pal','JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c))for c in colors)+'\n')
    write(ART+'/manifest.json',json.dumps(manifest,indent=2)+'\n')
    for name,entry in art.items():
        b=io.BytesIO();entry['image'].save(b,format='PNG',bits=4,transparency=0)
        write(ART+'/'+name+'.png',b.getvalue())
    # This atlas is a source-material preview, not a screenshot or a playtest.
    atlas=Image.new('RGB',(640,1024),'#1a202a');draw=ImageDraw.Draw(atlas)
    x=y=0;row=0
    for name,entry in art.items():
        im=entry['image'].convert('RGBA');W=max(112,im.width+8);H=im.height+22
        if x+W>640:x=0;y+=row;row=0
        atlas.paste(im,(x+4,y+4),im);draw.text((x+3,y+im.height+6),name,fill='white')
        x+=W;row=max(row,H)
    b=io.BytesIO();atlas.crop((0,0,640,y+row)).save(b,format='PNG');write(ART+'/source-material-preview.png',b.getvalue())

    if register:
        graphics='';metatiles='';headers='';externs=''
        for symbol,pool,secondary in [(SYMBOL_PRIMARY,PRIMARY,False),(SYMBOL_SECONDARY,SECONDARY,True)]:
            graphics+=f'const u32 gTilesetTiles_{symbol}[] = INCGFX_U32("{pool}/tiles.png", ".4bpp.fastSmol");\n'
            graphics+=f'const u16 gTilesetPalettes_{symbol}[][16] = {{\n'+''.join(f' INCGFX_U16("{pool}/palettes/{i:02}.pal", ".gbapal"),\n'for i in range(16))+'};\n'
            metatiles+=f'const u16 gMetatiles_{symbol}[] = INCBIN_U16("{pool}/metatiles.bin");\nconst u16 gMetatileAttributes_{symbol}[] = INCBIN_U16("{pool}/metatile_attributes.bin");\n'
            headers+=f'const struct Tileset gTileset_{symbol} = {{.isCompressed=TRUE,.isSecondary={"TRUE"if secondary else"FALSE"},.tiles=gTilesetTiles_{symbol},.palettes=gTilesetPalettes_{symbol},.metatiles=gMetatiles_{symbol},.metatileAttributes=gMetatileAttributes_{symbol},.callback=NULL}};\n'
            externs+=f'extern const struct Tileset gTileset_{symbol};\n'
        begin='// BEGIN HGSS SS AQUA';end='// END HGSS SS AQUA'
        for path,body in [('src/data/tilesets/graphics.h',graphics),('src/data/tilesets/metatiles.h',metatiles),('src/data/tilesets/headers.h',headers),('include/tilesets.h',externs)]:
            text=(R/path).read_text();section=begin+'\n#if !IS_FRLG\n'+body+'#endif\n'+end
            write(path,upsert(text,begin,end,section,externs=path=='include/tilesets.h'))
    print('Original private S.S.Aqua:',cursor,'combined glyphs;',len(attrs),'secondary metatiles; output',out)
    return manifest


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--output-root',type=Path);p.add_argument('--no-register',action='store_true');a=p.parse_args()
    generate(a.check,a.output_root,not a.no_register)
