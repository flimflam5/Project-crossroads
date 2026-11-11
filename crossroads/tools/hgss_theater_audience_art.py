"""Original indexed GBA audience floor/cushion drawings for HGSS Theater.

Inspection reference (not imported as texture/pixel data): the published final
HGSS frame at https://images.wikidexcdn.net/mwuploads/wikidex/0/09/latest/20100424181308/Teatro_de_Danza_HGSS.jpg
SHA256 05a655b8cc52f311c8660a1fb4dfeee3eeae5cf7e253a4651ae02e53b013421e.
It shows a light-green checker audience floor and thirteen purple floor cushions;
the raised wooden stage is a separate surface. These drawings compress the DS
perspective into square16px native metatiles and retain no source-image pixels.

Integration contract: use private Theater palette bank8. Both returned images
are fully opaque16x16 index drawings, including the floor under each cushion.
Pack all four image quadrants in the BOTTOM metatile layer and four blank/zero
glyphs in the TOP layer. They have no roof/canopy/foreground overhang. Preserve
existing source bench anchors, collision/elevation/behavior and actor/event data.
This module creates no project output and imports no mutable game generators.
"""
from pathlib import Path
from PIL import Image,ImageDraw

PALETTE_BANK=8
COLORS=[
    (0,0,0),          #0 reserved blank/transparent glyph; never an opaque pixel
    (152,176,136),    #1 pale green floor
    (136,160,120),    #2 alternating muted green floor
    (120,144,104),    #3 fine grid / floor seam
    (168,192,152),    #4 sparse floor highlight
    (144,168,128),    #5 fine floor grain
    (104,128,96),     #6 cushion contact shadow
    (72,40,104),      #7 purple cushion outer seam
    (104,56,136),     #8 purple shaded cushion edge
    (128,80,168),     #9 cushion fabric
    (152,104,192),    #10 upper fabric highlight
    (176,128,208),    #11 folded upper edge
    (112,64,152),     #12 lower fabric seam
    (136,88,176),     #13 fabric center variation
    (160,112,192),    #14 small fabric highlight
    (88,112,80),      #15 deepest contact shadow
]

def artwork():
    """Return {audience_floor, audience_cushion}: opaque indexed16x16 images."""
    floor=Image.new('P',(16,16),1)
    floor.putpalette(sum((list(c)for c in COLORS),[])+[0]*720)
    d=ImageDraw.Draw(floor)
    # Four subtle squares per metatile keep the source checker legible at GBA
    # resolution without dense noise or alternating entire16px floor slabs.
    d.rectangle((8,0,15,7),fill=2);d.rectangle((0,8,7,15),fill=2)
    d.line((0,7,15,7),fill=3);d.line((7,0,7,15),fill=3)
    d.line((0,15,15,15),fill=3);d.line((15,0,15,15),fill=3)
    for x,y in ((2,2),(10,10),(4,12),(12,4)):d.point((x,y),fill=4)
    for x,y in ((4,4),(12,12),(2,10),(10,2)):d.point((x,y),fill=5)
    cushion=floor.copy();d=ImageDraw.Draw(cushion)
    # A low square cushion, not a wooden bench/table or tall chair. Small floor
    # margins and a contact shadow remain inside the one source grid cell.
    d.rounded_rectangle((1,3,14,14),radius=2,fill=6)
    d.line((3,14,12,14),fill=15)
    d.rounded_rectangle((1,1,14,12),radius=2,fill=7)
    d.rounded_rectangle((2,2,13,11),radius=1,fill=9)
    d.line((3,2,12,2),fill=11);d.line((2,3,2,9),fill=10)
    d.line((3,3,12,3),fill=10);d.line((3,10,12,10),fill=12)
    d.line((3,11,12,11),fill=8);d.line((13,3,13,10),fill=8)
    d.line((5,5,10,5),fill=13);d.line((5,6,5,8),fill=13)
    d.point((10,7),fill=14);d.point((4,4),fill=14)
    assert 0 not in floor.tobytes() and 0 not in cushion.tobytes()
    return dict(audience_floor=floor,audience_cushion=cushion)

def preview(path):
    """Write an isolated example; this does not modify any game resources."""
    a=artwork();im=Image.new('RGB',(160,112))
    for y in range(7):
        for x in range(10):im.paste(a['audience_floor'].convert('RGB'),(x*16,y*16))
    # Same13-anchor arrangement viewed as a furniture material study only;
    # placement in actual map remains the source generator's responsibility.
    for x,y in [(1,1),(7,1),(9,1)]+[(x,y)for y in (3,5)for x in (1,3,5,7,9)]:
        im.paste(a['audience_cushion'].convert('RGB'),(x*16,y*16))
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);im.save(p)
    return p

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--preview',required=True)
    print('Original native audience checker/cushion study; not emulator gameplay:',preview(p.parse_args().preview))
