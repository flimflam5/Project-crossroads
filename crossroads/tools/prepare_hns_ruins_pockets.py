#!/usr/bin/env python3
"""Convert pinned Heart & Soul Ruins pocket art to an isolated GBA preview.

This tool does not register maps or scripts. The donor's conditional puzzle,
hidden-room and underground-hall events require separate implementation. The
rendered crops and mapped bytes are evidence for integration, not a playtest.
"""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import io
import json
import struct

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'crossroads/donor/hns-ruins-pockets'
REVISION = '167aa6d537b109bb229c231ddce4616974c4da71'
GROUPS = {
    'outside': {
        'source': 'RuinsOfAlph_Outside_hns', 'width': 46, 'height': 48,
        'primary': 'johto_north_east_hns', 'secondary': 'ruins_of_alph_outside_hns',
        'crops': {'NorthwestPocket': (0, 19, 16, 17), 'SouthwestPocket': (0, 34, 22, 14)},
    },
    'chambers': {
        'source': 'RuinsOfAlph_PuzzleAndRewardChambers_hns', 'width': 26, 'height': 68,
        'primary': 'johto_building_hns', 'secondary': 'ruins_of_alph_writing_hns',
        'crops': {'NorthwestChamber': (0, 0, 10, 11), 'SouthwestChamber': (0, 17, 10, 11)},
    },
}


def words(path):
    b = path.read_bytes()
    assert len(b) % 2 == 0
    return struct.unpack('<%dH' % (len(b) // 2), b)


def pack(values):
    return struct.pack('<%dH' % len(values), *values)


def convert(group, target):
    root = SOURCE / 'data'
    primary = root / 'tilesets/primary' / group['primary']
    secondary = root / 'tilesets/secondary' / group['secondary']
    metas = [words(primary / 'metatiles.bin'), words(secondary / 'metatiles.bin')]
    attrs = [words(primary / 'metatile_attributes.bin'), words(secondary / 'metatile_attributes.bin')]
    data = words(root / 'layouts' / group['source'] / 'map.bin')
    assert len(data) == group['width'] * group['height']
    crops = {}
    for name, (x, y, width, height) in group['crops'].items():
        assert 0 <= x < x + width <= group['width'] and 0 <= y < y + height <= group['height']
        crops[name] = [data[(y + row) * group['width'] + x + col]
                       for row in range(height) for col in range(width)]
    used = sorted({v & 1023 for cells in crops.values() for v in cells})
    assert len(used) <= 512

    def donor_meta(i):
        section, index = (0, i) if i < 640 else (1, i - 640)
        assert index < len(attrs[section]) and index * 8 + 8 <= len(metas[section])
        return metas[section][index * 8:index * 8 + 8], attrs[section][index]

    refs = [word for i in used for word in donor_meta(i)[0]]
    tile_ids = sorted({word & 1023 for word in refs})
    banks = sorted({word >> 12 for word in refs})
    assert len(tile_ids) <= 512 and len(banks) <= 6
    tile_map = {old: new for new, old in enumerate(tile_ids)}
    meta_map = {old: new for new, old in enumerate(used)}
    palette_map = {old: new for new, old in enumerate(banks)}
    sheets = [Image.open(primary / 'tiles.png'), Image.open(secondary / 'tiles.png')]
    assert all(im.mode == 'P' and im.width == 128 for im in sheets)
    sheet = Image.new('P', (128, ((len(tile_ids) + 15) // 16) * 8))
    sheet.putpalette(sheets[0].getpalette())
    for old, new in tile_map.items():
        part, index = (0, old) if old < 640 else (1, old - 640)
        x, y = (index % 16) * 8, (index // 16) * 8
        assert y + 8 <= sheets[part].height
        tile = sheets[part].crop((x, y, x + 8, y + 8))
        sheet.paste(tile, ((new % 16) * 8, (new // 16) * 8))
        assert sheet.crop(((new % 16) * 8, (new // 16) * 8,
                           (new % 16) * 8 + 8, (new // 16) * 8 + 8)).tobytes() == tile.tobytes()
    target.mkdir(parents=True, exist_ok=True)
    sheet.save(target / 'tiles.png', optimize=False)
    palette_dir = target / 'palettes'
    palette_dir.mkdir(exist_ok=True)
    for bank, mapped in palette_map.items():
        src = (primary if bank < 7 else secondary) / 'palettes' / f'{bank:02}.pal'
        (palette_dir / f'{mapped:02}.pal').write_bytes(src.read_bytes())
    output_meta = [tile_map[v & 1023] | (v & 0xc00) | (palette_map[v >> 12] << 12)
                   for v in refs]
    output_attrs = [donor_meta(i)[1] for i in used]
    (target / 'metatiles.bin').write_bytes(pack(output_meta))
    (target / 'metatile_attributes.bin').write_bytes(pack(output_attrs))
    events = json.loads((root / 'maps' / group['source'] / 'map.json').read_text())
    report = {'source': group['source'], 'metatiles': len(used), 'tiles': len(tile_ids),
              'palette_banks': banks, 'palette_map': palette_map, 'crops': {}}
    for name, cells in crops.items():
        x, y, width, height = group['crops'][name]
        converted = [(v & 0xfc00) | meta_map[v & 1023] for v in cells]
        assert all((a & 0xfc00) == (b & 0xfc00) and donor_meta(a & 1023)[1] == output_attrs[b & 1023]
                   for a, b in zip(cells, converted))
        (target / f'{name}.bin').write_bytes(pack(converted))
        warps = []
        for index, event in enumerate(events['warp_events']):
            if x <= event['x'] < x + width and y <= event['y'] < y + height:
                warps.append({'donor_index': index, 'local_x': event['x'] - x,
                              'local_y': event['y'] - y, 'destination': event['dest_map'],
                              'destination_index': event['dest_warp_id']})
        behaviors = Counter(hex(output_attrs[v & 1023] & 255) for v in converted)
        report['crops'][name] = {'donor_rect': [x, y, width, height], 'warps': warps,
                                 'behavior_counts': dict(sorted(behaviors.items()))}
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    target = args.output.resolve()
    assert not target.is_relative_to(ROOT), 'Preview output must not alter live game sources'
    manifest = json.loads((SOURCE / 'source-sha256.json').read_text())
    assert manifest['revision'] == REVISION
    for name, digest in manifest['files'].items():
        assert hashlib.sha256((SOURCE / name).read_bytes()).hexdigest() == digest, name
    target.mkdir(parents=True, exist_ok=True)
    report = {'donor_revision': REVISION, 'groups': {},
              'limitations': ['Not registered, built or emulator tested.',
                              'Crops preserve donor physics and warp inventory only; edge isolation, water, animation, visible priorities and HGSS correspondence need testing.',
                              'Puzzle, fall-to-hall, hidden-room interactions and conditional destination events are not implemented.',
                              'Do not bind donor cave destinations directly: HGSS uses isolated 1F/B2F connector pockets.']}
    for name, group in GROUPS.items():
        report['groups'][name] = convert(group, target / name)
    (target / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Prepared four unregistered Ruins pockets/chambers; source hashes and remapped cells pass. No game content changed.')


if __name__ == '__main__':
    main()
