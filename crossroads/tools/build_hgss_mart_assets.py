#!/usr/bin/env python3
"""Private common-Mart art: native plant motifs and original glass/rack/stools.

All existing Shop metatiles retain decoded pixels, layers and attributes. Only
explicit source props receive appended metatiles; shared Shop/Building resources
stay unchanged. Only four actual stool bases gain collision; every other movement
and elevation bit remains exact. No HGSS pixels are imported.
"""
import argparse
import io
import json
import struct
from pathlib import Path
from tileset_registration import upsert

from PIL import Image, ImageDraw

R = Path(__file__).resolve().parents[2]
D = R / 'data/tilesets/secondary/hgss_mart'
A = R / 'crossroads/hgss/art/mart'
BASE = '3f935d5e8600c5a280b9172b555edb35ca52b6c0'
COLORS = [(0, 0, 0), (40, 64, 80), (73, 100, 116), (110, 145, 156),
          (205, 189, 197), (224, 241, 235), (32, 120, 152), (72, 178, 200),
          (137, 219, 228), (240, 218, 104), (181, 149, 64), (121, 95, 40),
          (59, 118, 42), (106, 164, 41), (197, 238, 148), (238, 222, 164)]


def words(path):
    b = path.read_bytes()
    return list(struct.unpack('<' + str(len(b) // 2) + 'H', b))


def artwork():
    def image(size):
        q = Image.new('P', size)
        q.putpalette(sum((list(c) for c in COLORS), []) + [0] * 720)
        return q
    glass = image((32, 32)); p = ImageDraw.Draw(glass)
    # Original GBA glass display at the actual source model42 footprint.
    p.rectangle((2, 3, 29, 23), fill=1); p.rectangle((3, 4, 28, 21), fill=5)
    p.rectangle((5, 6, 26, 19), fill=6); p.rectangle((6, 7, 25, 17), fill=7)
    p.polygon([(7, 16), (17, 7), (22, 7), (12, 17), (7, 17)], fill=8)
    p.line((6, 7, 25, 7), fill=5); p.line((4, 22, 27, 22), fill=3)
    p.rectangle((4, 24, 8, 29), fill=10); p.rectangle((23, 24, 27, 29), fill=10)
    p.line((5, 24, 5, 28), fill=9); p.line((24, 24, 24, 28), fill=9)
    rack = image((16, 32)); p = ImageDraw.Draw(rack)
    p.rectangle((1, 2, 14, 30), fill=1); p.rectangle((3, 3, 13, 28), fill=5)
    for y in (5, 15):
        p.rectangle((4, y, 7, y + 6), fill=7)
        p.line((5, y + 1, 6, y + 1), fill=5)
        p.rectangle((9, y + 1, 11, y + 6), fill=10)
        p.line((9, y, 11, y), fill=15)
        p.line((3, y + 8, 13, y + 8), fill=2)
    p.line((2, 29, 13, 29), fill=3)
    stool = image((16, 16)); p = ImageDraw.Draw(stool)
    p.rectangle((3, 2, 12, 10), fill=1); p.rectangle((4, 3, 11, 9), fill=10)
    p.rectangle((4, 3, 11, 6), fill=9); p.line((5, 3, 10, 3), fill=15)
    p.line((4, 11, 4, 14), fill=2); p.line((11, 11, 11, 14), fill=2)
    return dict(glass=glass, rack=rack, stool=stool)


def placements():
    out = []
    for x, base in [(12, 3), (12, 11), (1, 11)]:
        out += [(x, base - 1, 'plant', 0, 0), (x, base, 'plant', 0, 1)]
    out += [(12, y, 'rack', 0, y - 6) for y in (6, 7)]
    out += [(x, y, 'glass', x - 8, y - 9) for y in (9, 10) for x in (8, 9)]
    out += [(x, y, 'stool', 0, 0) for y in (9, 10) for x in (7, 10)]
    return sorted(out, key=lambda p: (p[1], p[0]))


def build_payload():
    shop = R / 'data/tilesets/secondary/shop'
    pc = R / 'data/tilesets/secondary/pokemon_center'
    original = Image.open(shop / 'tiles.png')
    sm, sa, pm = words(shop / 'metatiles.bin'), words(shop / 'metatile_attributes.bin'), words(pc / 'metatiles.bin')
    assert len(sa) == 289 and not any(v >> 12 >= 12 for v in sm)
    sheet = Image.new('P', (128, 256)); sheet.putpalette(original.getpalette())
    cache = {}; cursor = 0
    def glyph(im):
        nonlocal cursor
        k = im.tobytes()
        if k not in cache:
            assert cursor < 512, 'Private Mart graphics capacity exceeded'
            cache[k] = cursor; sheet.paste(im, (cursor % 16 * 8, cursor // 16 * 8)); cursor += 1
        return 512 + cache[k]
    plant_colors = [tuple(map(int, row.split())) for row in (pc / 'palettes/08.pal').read_text().splitlines()[3:]]
    plant_remap = [0] + [min(range(1, 16), key=lambda j: sum((plant_colors[i][k] // 8 - COLORS[j][k] // 8) ** 2 for k in range(3))) for i in range(1, 16)]
    def copy_ref(v, source=original, bank=None):
        i = (v & 1023) - 512
        if i < 0:
            assert bank is None
            return v
        q = source.crop((i % 16 * 8, i // 16 * 8, i % 16 * 8 + 8, i // 16 * 8 + 8))
        if bank is not None:
            assert bank == 12 and v >> 12 == 8
            q.putdata([plant_remap[index] for index in q.tobytes()])
        return glyph(q) | (v & 0xc00) | ((v >> 12 if bank is None else bank) << 12)
    metas = [copy_ref(v) for v in sm]; attrs = list(sa)
    floor = metas[8:12]
    art = artwork(); ps = Image.open(pc / 'tiles.png'); specs = []; changes = []
    c = json.loads((R / 'crossroads/hgss/contracts/mart-props-qa09.json').read_text())
    assert c['source_commit'] == BASE
    for x, y, kind, dx, dy in placements():
        before = c['before_words'][y * 14 + x]
        if kind == 'plant':
            n = [0x20a, 0x212][dy]
            overlay = [copy_ref(v, ps, 12) for v in pm[(n - 512) * 8 + 4:(n - 512) * 8 + 8]]
            attribute = 0 if dy == 0 else 0x1000
        else:
            q = art[kind]
            overlay = [glyph(q.crop((dx * 16 + X, dy * 16 + Y, dx * 16 + X + 8, dy * 16 + Y + 8))) | 0xc000
                       for X, Y in [(0, 0), (8, 0), (0, 8), (8, 8)]]
            attribute = 0x1000
        underlay = floor
        if (x, y, kind) == (12, 2, 'plant'):
            # Upper leaves overhang the existing rear window/wall; copying
            # floor here punched a visible green gap in the north facade.
            assert before == 0x61b
            underlay = metas[(0x21b - 512) * 8:(0x21b - 512) * 8 + 4]
        n = 512 + len(attrs); metas.extend(underlay + overlay); attrs.append(attribute)
        after = (before & 0xfc00) | (0x400 if kind == 'stool' else 0) | n
        changes.append(dict(x=x, y=y, before=before, after=after))
        specs.append(dict(x=x, y=y, kind=kind, source_tile=[dx, dy], metatile=n, attribute=attribute))
    assert len(attrs) <= 512
    assert changes == [{k: d[k] for k in ('x', 'y', 'before', 'after')} for d in c['changes']], 'Immutable reviewed Mart delta differs'
    palettes = [(shop / f'palettes/{i:02}.pal').read_bytes() for i in range(16)]
    palettes[12] = ('JASC-PAL\n0100\n16\n' + '\n'.join(' '.join(map(str, c)) for c in COLORS) + '\n').replace('\n', '\r\n').encode()
    manifest = dict(source_commit=BASE, native_shop_metatiles=len(sa), metatiles=len(attrs), graphics=cursor,
                    placements=specs, palette_bank=12, plant_palette_remap=plant_remap,
                    source='Actual HGSS common Mart matrix0104 props/raster; native GBA Center plant silhouettes quantized into the same sole free loaded bank12 as original glass display, rack and stools. No reference pixels imported.',
                    raster_reference='https://archives.bulbagarden.net/media/upload/0/08/Pok%C3%A9_Mart_interior_HGSS.png')
    assert max(v >> 12 for v in metas) <= 12, 'Fieldmap loads BG palette banks0..12 only'
    return sheet, metas, attrs, palettes, art, manifest


def preview(payload, path):
    sheet, metas, attrs, palettes, art, manifest = payload
    primary = R / 'data/tilesets/primary/building'
    sheets = [Image.open(primary / 'tiles.png'), sheet]
    ms = [words(primary / 'metatiles.bin'), metas]
    pals = [[tuple(int(v) // 8 for v in row.split()) for row in
             ((primary / f'palettes/{i:02}.pal').read_text().splitlines()[3:] if i < 6
              else palettes[i].decode().splitlines()[3:])] for i in range(16)]
    c = json.loads((R / 'crossroads/hgss/contracts/mart-props-qa09.json').read_text()); tiles = list(c['before_words'])
    for d in c['changes']: tiles[d['y'] * 14 + d['x']] = d['after']
    out = Image.new('RGB', (224, 208))
    for i, n in enumerate(tiles):
        n &= 1023; im = Image.new('RGBA', (16, 16))
        for j, v in enumerate(ms[n >= 512][n % 512 * 8:n % 512 * 8 + 8]):
            k = v & 1023; q = sheets[k >= 512].crop((k % 512 % 16 * 8, k % 512 // 16 * 8, k % 512 % 16 * 8 + 8, k % 512 // 16 * 8 + 8))
            if v & 0x400: q = q.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if v & 0x800: q = q.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            patch = Image.new('RGBA', (8, 8)); patch.putdata([tuple((z << 3) | (z >> 2) for z in pals[v >> 12][p]) + (255,) if p else (0, 0, 0, 0) for p in q.tobytes()])
            im.alpha_composite(patch, (j % 2 * 8, j % 4 // 2 * 8))
        out.paste(im, (i % 14 * 16, i // 14 * 16), im)
    Path(path).parent.mkdir(parents=True, exist_ok=True); out.save(path)


def build(check=False, preview_path=None):
    payload = build_payload()
    if preview_path:
        preview(payload, preview_path)
        print('Static full-room Mart prop preview; not emulator gameplay:', preview_path)
        return
    sheet, metas, attrs, palettes, art, manifest = payload
    def write(p, b):
        if isinstance(b, str): b = b.encode()
        if check: assert p.exists() and p.read_bytes() == b, ('Regenerate private Mart', str(p))
        elif not p.exists() or p.read_bytes() != b: p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(b)
    if check: assert Image.open(D / 'tiles.png').tobytes() == sheet.tobytes()
    else: D.mkdir(parents=True, exist_ok=True); sheet.save(D / 'tiles.png', bits=4)
    write(D / 'metatiles.bin', struct.pack('<' + str(len(metas)) + 'H', *metas))
    write(D / 'metatile_attributes.bin', struct.pack('<' + str(len(attrs)) + 'H', *attrs))
    for i, b in enumerate(palettes): write(D / f'palettes/{i:02}.pal', b)
    write(A / 'manifest.json', json.dumps(manifest, indent=2) + '\n')
    for n, im in art.items():
        b = io.BytesIO(); im.save(b, format='PNG', bits=4, transparency=0); write(A / (n + '.png'), b.getvalue())
    begin = '// BEGIN HGSS COMMON MART PROPS'; end = '// END HGSS COMMON MART PROPS'; name = 'HgssMart'
    blocks = {
        'src/data/tilesets/headers.h': f'const struct Tileset gTileset_{name} = {{ .isCompressed=TRUE,.isSecondary=TRUE,.tiles=gTilesetTiles_{name},.palettes=gTilesetPalettes_{name},.metatiles=gMetatiles_{name},.metatileAttributes=gMetatileAttributes_{name},.callback=NULL }};',
        'src/data/tilesets/graphics.h': f'const u32 gTilesetTiles_{name}[] = INCGFX_U32("data/tilesets/secondary/hgss_mart/tiles.png", ".4bpp.fastSmol");\nconst u16 gTilesetPalettes_{name}[][16] = {{\n' + ''.join(f' INCGFX_U16("data/tilesets/secondary/hgss_mart/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16)) + '};',
        'src/data/tilesets/metatiles.h': f'const u16 gMetatiles_{name}[] = INCBIN_U16("data/tilesets/secondary/hgss_mart/metatiles.bin");\nconst u16 gMetatileAttributes_{name}[] = INCBIN_U16("data/tilesets/secondary/hgss_mart/metatile_attributes.bin");',
        'include/tilesets.h': f'extern const struct Tileset gTileset_{name};'}
    for path, body in blocks.items():
        p = R / path; text = p.read_text(); section = begin + '\n#if !IS_FRLG\n' + body + '\n#endif\n' + end
        text = upsert(text, begin, end, section, externs=path == 'include/tilesets.h')
        write(p, text)
    print('Private HGSS common Mart:', manifest['graphics'], 'graphics,', len(attrs), 'metatiles;16 exact prop-art cells; all native Shop pixels retained')


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--check', action='store_true'); p.add_argument('--preview'); a = p.parse_args(); build(a.check, a.preview)
