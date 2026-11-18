#!/usr/bin/env python3
"""Stage a Route 32 donor conversion that preserves the Violet north seam.

This creates experimental files outside the repository; it does not install a
map or establish that encounters, H&S behavior, water or old saves are safe.
"""
from pathlib import Path
import argparse
import hashlib
import json
from collections import deque
from PIL import Image
from stage_hns_route32 import ROOT, SOURCE, PRIMARY, SECONDARY, image_tile, pack, words

SEAM_METATILES = (1, 198, 468, 469, 476, 477, 511)
PAL_MAP = {0: 1, 1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 9, 12: 10}


def stage(output):
    out = Path(output).resolve()
    assert out != ROOT and ROOT not in out.parents, 'Output must be outside repository'
    assert not out.exists() or not any(out.iterdir()), 'Output directory must be empty'
    out.mkdir(parents=True, exist_ok=True)
    for rec in json.loads((SOURCE / 'provenance.json').read_text())['source_manifest']:
        assert hashlib.sha256((SOURCE / rec['path']).read_bytes()).hexdigest() == rec['sha256']
    raw = words(SOURCE / 'data/layouts/Route32_hns/map.bin')
    old = words(ROOT / 'data/layouts/JohtoRoute32/map.bin')
    assert len(raw) == 42 * 103 and len(old) == 28 * 64
    m = [words(PRIMARY / 'metatiles.bin'), words(SECONDARY / 'metatiles.bin')]
    a = [words(PRIMARY / 'metatile_attributes.bin'), words(SECONDARY / 'metatile_attributes.bin')]
    # Six western source columns are cropped; this retains the full gate.
    cropped = [raw[y * 42 + x] for y in range(103) for x in range(6, 42)]
    mids = sorted({v & 1023 for v in cropped})
    entries = {mid: m[mid >= 640][(mid if mid < 640 else mid - 640) * 8:][:8] for mid in mids}
    assert all(len(x) == 8 for x in entries.values())
    violet_meta = words(ROOT / 'data/tilesets/primary/hgss_violet/metatiles.bin')
    violet_attr = words(ROOT / 'data/tilesets/primary/hgss_violet/metatile_attributes.bin')
    seam_refs = [v for mid in SEAM_METATILES for v in violet_meta[mid * 8:mid * 8 + 8]]
    reserved_tiles = {v & 1023 for v in seam_refs}
    assert {v >> 12 for v in seam_refs} == {0, 2, 3}
    donor_tiles = sorted({v & 1023 for entry in entries.values() for v in entry})
    free_tiles = [n for n in range(512) if n not in reserved_tiles]
    free_metas = [n for n in range(512) if n not in SEAM_METATILES]
    assert donor_tiles[0] == 0 and len(donor_tiles) - 1 <= len(free_tiles) and len(mids) <= len(free_metas)
    tmap = {0: 0}
    tmap.update({old_id: new for old_id, new in zip(donor_tiles[1:], free_tiles)})
    mmap = dict(zip(mids, free_metas))
    donor_images = [Image.open(PRIMARY / 'tiles.png'), Image.open(SECONDARY / 'tiles.png')]
    sheet = Image.open(ROOT / 'data/tilesets/primary/general/tiles.png').copy()
    assert sheet.mode == 'P' and sheet.size == (128, 256)
    assert set(image_tile(donor_images[0], 0).tobytes()) == {0}
    for old_id, new_id in tmap.items():
        if not old_id:
            continue
        src = image_tile(donor_images[old_id >= 640], old_id if old_id < 640 else old_id - 640)
        sheet.paste(src, (new_id % 16 * 8, new_id // 16 * 8))
    meta = [0] * (512 * 8)
    attrs = [0] * 512
    for mid in SEAM_METATILES:
        meta[mid * 8:mid * 8 + 8] = violet_meta[mid * 8:mid * 8 + 8]
        attrs[mid] = violet_attr[mid]
    for old_id, new_id in mmap.items():
        refs = entries[old_id]
        assert all(v >> 12 in PAL_MAP for v in refs)
        meta[new_id * 8:new_id * 8 + 8] = [tmap[v & 1023] | v & 0xc00 | (PAL_MAP[v >> 12] << 12) for v in refs]
        donor_attr = a[old_id >= 640][old_id if old_id < 640 else old_id - 640]
        # This engine has no H&S headbutt behavior 0xf0. Preserve the tree's
        # collision and render while removing that unsupported interaction.
        attrs[new_id] = donor_attr & ~255 if donor_attr & 255 == 0xf0 else donor_attr
    # Existing north edge is kept byte-for-byte at its original coordinates.
    top = [old[y * 28 + min(x, 27)] for y in range(7) for x in range(36)]
    cells = top + [(v & 0xfc00) | mmap[v & 1023] for v in cropped]
    assert len(cells) == 36 * 110
    assert all(cells[y * 36 + x] == old[y * 28 + x] for y in range(7) for x in range(28))
    assert all(not (cells[6 * 36 + x] & 0xc00) and not (cells[7 * 36 + x] & 0xc00) for x in (14, 15))
    for mid in SEAM_METATILES:
        assert meta[mid * 8:mid * 8 + 8] == violet_meta[mid * 8:mid * 8 + 8] and attrs[mid] == violet_attr[mid]
    general = Image.open(ROOT / 'data/tilesets/primary/general/tiles.png')
    for tile in reserved_tiles:
        assert image_tile(sheet, tile).tobytes() == image_tile(general, tile).tobytes()
    # Collision-only connectivity is a useful alarm, not proof: this ignores
    # directional behaviors, field moves, NPCs and animation/door scripts.
    visited = {(14, 6)}
    queue = deque(visited)
    while queue:
        x, y = queue.popleft()
        for xx, yy in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= xx < 36 and 0 <= yy < 110 and (xx, yy) not in visited and not cells[yy * 36 + xx] & 0xc00:
                visited.add((xx, yy)); queue.append((xx, yy))
    assert (7, 10) in visited and (11, 98) in visited and (19, 92) in visited
    assert attrs[cells[91 * 36 + 19] & 1023] & 255 == 0x69 # donor animated Center door
    for old_id, new_id in tmap.items():
        src = image_tile(donor_images[old_id >= 640], old_id if old_id < 640 else old_id - 640)
        assert src.tobytes() == image_tile(sheet, new_id).tobytes()
    for bank in range(16):
        source = ROOT / f'data/tilesets/primary/general/palettes/{bank:02}.pal'
        old_bank = next((k for k, v in PAL_MAP.items() if v == bank), None)
        if old_bank is not None:
            source = (PRIMARY if old_bank <= 6 else SECONDARY) / f'palettes/{old_bank:02}.pal'
        (out / f'palette-{bank:02}.pal').write_bytes(source.read_bytes())
        assert (out / f'palette-{bank:02}.pal').read_bytes() == source.read_bytes()
    (out / 'map.bin').write_bytes(pack(cells))
    (out / 'metatiles.bin').write_bytes(pack(meta))
    (out / 'metatile_attributes.bin').write_bytes(pack(attrs))
    sheet.save(out / 'tiles.png')
    assert Image.open(out / 'tiles.png').tobytes() == sheet.tobytes()
    assert words(out / 'map.bin') == cells and words(out / 'metatiles.bin') == meta
    assert words(out / 'metatile_attributes.bin') == attrs
    (out / 'mapping.json').write_text(json.dumps({'width': 36, 'height': 110, 'crop_left': 6,
        'top_rows': 7, 'metatiles': mmap, 'tiles': tmap, 'palettes': PAL_MAP,
        'candidate_only': True}, indent=2) + '\n')
    print(f'PASS Violet seam prototype: {len(mids)} donor metatiles, {len(donor_tiles)} graphics; exact Violet seam IDs, pixels and palette references retained; collision-only flood reaches gate, Center approach and cave.')
    print('Not installed or playtested. Behavior mapping, full seam movement, Ruins gate, Center, cave and old-save migration remain.')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--output', required=True)
    stage(p.parse_args().output)
