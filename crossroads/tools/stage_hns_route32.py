#!/usr/bin/env python3
"""Stage Route 32 donor graphics in Emerald's 512/512 split.

This is not an installed map. It preserves donor pixels, palettes, map bits
and attributes, but does not establish that donor behavior codes, crossings,
elevations, the Violet seam or old save positions are safe. Output must be
outside the repository so it cannot overwrite a working map.
"""
from pathlib import Path
import argparse
import hashlib
import json
import struct
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'crossroads/donor/hns-route32'
PRIMARY = SOURCE / 'data/tilesets/primary/johto_general_hns'
SECONDARY = SOURCE / 'data/tilesets/secondary/route_32_hns'


def words(path):
    data = path.read_bytes()
    assert len(data) % 2 == 0
    return list(struct.unpack('<%dH' % (len(data) // 2), data))


def pack(values):
    return struct.pack('<%dH' % len(values), *values)


def image_tile(image, number):
    x, y = number % 16 * 8, number // 16 * 8
    assert y + 8 <= image.height
    return image.crop((x, y, x + 8, y + 8))


def stage(out):
    out = Path(out).resolve()
    assert out != ROOT and ROOT not in out.parents, 'Staging output must be outside the repository'
    assert not out.exists() or not any(out.iterdir()), 'Staging output must be empty'
    out.mkdir(parents=True, exist_ok=True)
    manifest = json.loads((SOURCE / 'provenance.json').read_text())
    for record in manifest['source_manifest']:
        path = SOURCE / record['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256'], path
    raw = words(SOURCE / 'data/layouts/Route32_hns/map.bin')
    assert len(raw) == 42 * 103
    metatiles = [words(PRIMARY / 'metatiles.bin'), words(SECONDARY / 'metatiles.bin')]
    attributes = [words(PRIMARY / 'metatile_attributes.bin'), words(SECONDARY / 'metatile_attributes.bin')]
    assert len(metatiles[0]) == 640 * 8
    mids = sorted({v & 1023 for v in raw})
    assert len(mids) <= 512
    entries = {}
    for mid in mids:
        bank, index = (0, mid) if mid < 640 else (1, mid - 640)
        assert index < len(attributes[bank]) and index * 8 + 8 <= len(metatiles[bank])
        entries[mid] = metatiles[bank][index * 8:index * 8 + 8]
    tids = sorted({v & 1023 for entry in entries.values() for v in entry})
    palettes = sorted({v >> 12 for entry in entries.values() for v in entry})
    assert len(tids) <= 512 and all(p <= 6 or p == 12 for p in palettes)
    tmap = {old: new for new, old in enumerate(tids)}
    mmap = {old: new for new, old in enumerate(mids)}
    images = [Image.open(PRIMARY / 'tiles.png'), Image.open(SECONDARY / 'tiles.png')]
    rows = (len(tids) + 15) // 16
    tiles = Image.new('P', (128, rows * 8))
    tiles.putpalette(images[0].getpalette())
    for old, new in tmap.items():
        tile = image_tile(images[old >= 640], old if old < 640 else old - 640)
        tiles.paste(tile, ((new % 16) * 8, (new // 16) * 8))
    converted = []
    for mid in mids:
        converted.extend((v & ~1023) | tmap[v & 1023] for v in entries[mid])
    attrs = [attributes[mid >= 640][mid if mid < 640 else mid - 640] for mid in mids]
    blocks = [(v & ~1023) | mmap[v & 1023] for v in raw]
    (out / 'map.bin').write_bytes(pack(blocks))
    (out / 'metatiles.bin').write_bytes(pack(converted))
    (out / 'metatile_attributes.bin').write_bytes(pack(attrs))
    tiles.save(out / 'tiles.png')
    for bank in palettes:
        source = (PRIMARY if bank <= 6 else SECONDARY) / f'palettes/{bank:02}.pal'
        (out / f'palette-{bank:02}.pal').write_bytes(source.read_bytes())
    assert words(out / 'map.bin') == blocks
    assert words(out / 'metatiles.bin') == converted
    assert words(out / 'metatile_attributes.bin') == attrs
    saved_tiles = Image.open(out / 'tiles.png')
    assert saved_tiles.size == tiles.size and saved_tiles.tobytes() == tiles.tobytes()
    for bank in palettes:
        source = (PRIMARY if bank <= 6 else SECONDARY) / f'palettes/{bank:02}.pal'
        assert (out / f'palette-{bank:02}.pal').read_bytes() == source.read_bytes()
    (out / 'mapping.json').write_text(json.dumps({'source_width': 42, 'source_height': 103,
        'metatiles': mmap, 'tiles': tmap, 'palette_banks': palettes,
        'installed': False, 'collision_behavior_verified': False,
        'note': 'Palette 12 needs a compatible secondary palette. Violet seam and engine behaviors are not adapted.'}, indent=2) + '\n')
    return raw, entries, attributes, images, blocks, converted, attrs, tiles, mmap, tmap


def verify(data):
    raw, entries, attributes, images, blocks, converted, attrs, tiles, mmap, tmap = data
    assert len(blocks) == len(raw)
    for old, new in zip(raw, blocks):
        assert old & ~1023 == new & ~1023 and new & 1023 == mmap[old & 1023]
    for mid, out_id in mmap.items():
        bank, index = (0, mid) if mid < 640 else (1, mid - 640)
        assert attrs[out_id] == attributes[bank][index]
        for old, new in zip(entries[mid], converted[out_id * 8:out_id * 8 + 8]):
            assert old & ~1023 == new & ~1023 and new & 1023 == tmap[old & 1023]
    for old, new in tmap.items():
        source = image_tile(images[old >= 640], old if old < 640 else old - 640)
        assert source.tobytes() == image_tile(tiles, new).tobytes()
    print(f'PASS non-installed donor staging: {len(raw)} cells, {len(mmap)} metatiles, {len(tmap)} 8x8 graphics; map bits, attributes, palette selectors, flips and indexed pixels retained.')
    print('NOT verified: Violet/Ruins seams, cave warp, Center, engine behavior, collision, saves, build or gameplay.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, help='Empty directory outside the project')
    verify(stage(parser.parse_args().output))
