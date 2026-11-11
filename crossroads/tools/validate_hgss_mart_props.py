#!/usr/bin/env python3
"""Positive HGSS Mart props and immutable native-art/geometry preservation."""
import functools
import hashlib
import io
import json
import struct
import subprocess
from collections import deque
from pathlib import Path

from PIL import Image

R = Path(__file__).resolve().parents[2]
BASE = '3f935d5e8600c5a280b9172b555edb35ca52b6c0'


def load(p): return json.loads((R / p).read_text())
def words(b): return struct.unpack('<' + str(len(b) // 2) + 'H', b)


@functools.lru_cache(None)
def data(path, old=False):
    return subprocess.check_output(['git', 'show', BASE + ':' + path], cwd=R) if old else (R / path).read_bytes()


@functools.lru_cache(None)
def resource(secondary, old=False):
    roots = ['data/tilesets/primary/building', 'data/tilesets/secondary/' + secondary]
    sheets = [Image.open(io.BytesIO(data(p + '/tiles.png', old))) for p in roots]
    metas = [words(data(p + '/metatiles.bin', old)) for p in roots]
    attrs = [words(data(p + '/metatile_attributes.bin', old)) for p in roots]
    pals = [[tuple(int(v) // 8 for v in row.split()) for row in
             data(roots[i >= 6] + f'/palettes/{i:02}.pal', old).decode().splitlines()[3:]] for i in range(16)]
    return sheets, metas, attrs, pals


@functools.lru_cache(None)
def signature(secondary, n, old=False):
    sheets, metas, attrs, pals = resource(secondary, old); parts = []
    for v in metas[n >= 512][n % 512 * 8:n % 512 * 8 + 8]:
        k = v & 1023; i = k % 512
        q = sheets[k >= 512].crop((i % 16 * 8, i // 16 * 8, i % 16 * 8 + 8, i // 16 * 8 + 8))
        if v & 0x400: q = q.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if v & 0x800: q = q.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        parts.append(tuple(pals[v >> 12][p] if p else None for p in q.tobytes()))
    return attrs[n >= 512][n % 512], tuple(parts)


def validate():
    c = load('crossroads/hgss/contracts/mart-props-qa09.json')
    assert c['source_commit'] == BASE and c['before_secondary'] == 'gTileset_Shop' and c['after_secondary'] == 'gTileset_HgssMart'
    facts = load('crossroads/hgss/canonical_events/ecruteak-interior-geometry.json')['MAP_ECRUTEAK_POKEMART']
    props = [(p['model'], p['tile_x'], p['tile_z']) for chunk in facts['chunks'] for p in chunk['props']]
    # Independent source facts, rather than accepting a mutable placement list.
    expected = {(23, 12.5, 3.5), (23, 12.5, 11.5), (23, 1.5, 11.5),
                (42, 9.0, 10.0), (46, 12.5, 7.0),
                (57, 10.5, 9.5), (57, 7.5, 10.5), (58, 10.5, 10.5), (58, 7.5, 9.5)}
    assert {(m, x, z) for m, x, z in props if m in (23, 42, 46, 57, 58)} == expected
    assert {(p['model'], p['x'], p['z']) for p in c['source_props']} == expected
    baseline = list(words(data('data/layouts/EcruteakCity_Mart/map.bin', True)))
    assert c['before_words'] == baseline and len(baseline) == 14 * 13
    exact_cells = {(12, y) for y in (2, 3, 6, 7, 10, 11)} | {(1, 10), (1, 11)} | {(x, y) for x in (7, 8, 9, 10) for y in (9, 10)}
    assert {(d['x'], d['y']) for d in c['changes']} == exact_cells and len(c['changes']) == 16
    final = list(baseline)
    for d in c['changes']:
        i = d['y'] * 14 + d['x']; assert final[i] == d['before']
        expected_bits = d['before'] & 0xfc00
        if (d['x'], d['y']) in {(7, 9), (7, 10), (10, 9), (10, 10)}:
            expected_bits |= 0x400  # Real source stool models need solid bases.
        assert d['after'] & 0xfc00 == expected_bits, 'Changes beyond four actual stool collision bases'
        final[i] = d['after']
    layouts = {l['id']: l for l in load('data/layouts/layouts.json')['layouts']}
    for n in ['EcruteakCity_Mart', 'OlivineCity_Mart']:
        m = load(f'data/maps/{n}/map.json'); before = json.loads(data(f'data/maps/{n}/map.json', True))
        assert m == before, (n, 'Accepted services/events/doors/IDs changed')
        l = layouts[m['layout']]
        oldls = json.loads(data('data/layouts/layouts.json', True))['layouts']; old = next(q for q in oldls if q['id'] == m['layout'])
        assert l == dict(old, secondary_tileset='gTileset_HgssMart'), (n, 'Room changed beyond private secondary')
        assert list(words((R / l['blockdata_filepath']).read_bytes())) == final, (n, 'Changes outside exact sixteen prop cells')
        actors = {(o['x'], o['y']) for o in m['object_events']}
        doors = {(e['x'], e['y']) for e in m['warp_events']}
        public = {(x, y) for y in range(13) for x in range(14) if not final[y * 14 + x] & 0xc00 and (x, y) not in actors}
        seen = set(doors); q = deque(seen)
        while q:
            x, y = q.popleft()
            for p in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
                if p in public and p not in seen: seen.add(p); q.append(p)
        assert public <= seen, (n, 'Furniture created isolated public floor', public - seen)
        assert {(1, 11), (12, 11), (12, 3)}.isdisjoint(public), 'All three real plant bases must block'
    # Shared resources remain byte/pixel exact. The private clone preserves all
    # 289 native metatile signatures, including currently unused source art.
    for root in ['data/tilesets/primary/building', 'data/tilesets/secondary/shop']:
        for name in ['metatiles.bin', 'metatile_attributes.bin', 'tiles.png'] + [f'palettes/{i:02}.pal' for i in range(16)]:
            current, previous = data(root + '/' + name), data(root + '/' + name, True)
            if name.endswith('.pal'):
                # Git's palette text attributes may check out CRLF. Normalize
                # line endings only; every JASC header/value byte still matches.
                current = current.replace(b'\r\n', b'\n')
                previous = previous.replace(b'\r\n', b'\n')
            assert current == previous, ('Shared native resource changed', root, name)
    for n in range(512, 801):
        assert signature('shop', n, True) == signature('hgss_mart', n), ('Private native Shop pixel/layer/attribute changed', hex(n))
    manifest = load('crossroads/hgss/art/mart/manifest.json')
    assert manifest['metatiles'] == 305 and manifest['graphics'] <= 512
    # The real Emerald loader only loads13 BG palettes, despite GBA hardware
    # supporting16. A permissive offline renderer must not conceal bank13+.
    fieldmap = (R / 'include/fieldmap.h').read_text()
    assert '#define NUM_PALS_TOTAL 13' in fieldmap and '#define NUM_PALS_IN_PRIMARY 6' in fieldmap
    _, all_metas, _, palettes = resource('hgss_mart')
    assert all(0 <= v >> 12 <= 12 for entries in all_metas for v in entries), 'Unloaded fieldmap palette reference'
    assert manifest['palette_bank'] == 12
    assert all(v >> 12 <= 12 for v in all_metas[1])
    ps = {(p['x'], p['y']): p for p in manifest['placements']}
    for x, base in [(12, 3), (12, 11), (1, 11)]:
        for dy in (0, 1):
            p = ps[x, base - 1 + dy]; assert p['kind'] == 'plant'
            attr, native = signature('hgss_mart', p['metatile'])
            source = signature('pokemon_center', [0x20a, 0x212][dy], True)[1]
            # Original plant silhouettes/alpha and nearest hardware RGB555
            # colors are independently checked against their native source.
            quantized = tuple(tuple(None if pixel is None else min(palettes[12][1:], key=lambda color: sum((pixel[k] - color[k]) ** 2 for k in range(3))) for pixel in patch) for patch in source[4:])
            assert native[4:] == quantized, ('Native plant silhouette/color quantization differs', x, base, dy)
            assert attr == (0 if dy == 0 else 0x1000)
            expected_ground = signature('shop', 0x21b if (x, base, dy) == (12, 3, 0) else 0x201, True)[1][:4]
            assert native[:4] == expected_ground, 'Plant leaves must overhang the real window/floor without a wall gap'
    for xy in [(12, 6), (12, 7)]: assert ps[xy]['kind'] == 'rack'
    for x in (8, 9):
        for y in (9, 10): assert ps[x, y]['kind'] == 'glass'
    for x in (7, 10):
        for y in (9, 10): assert ps[x, y]['kind'] == 'stool'
    for d in c['changes']:
        a, layers = signature('hgss_mart', d['after'] & 1023)
        assert a & 255 == 0, 'Furniture must not introduce arrow/warp/slide behavior'
        assert hashlib.sha256(repr((a, layers)).encode()).hexdigest() == d['after_signature_sha256'], 'Reviewed per-layer prop pixels differ'
    print('HGSS common Mart:3 actual plants/glass display/4 stools/right rack;16 exact art cells;all289 native Shop signatures;only4 source stool bases gain collision;events/services unchanged: PASS')
    return {'EcruteakCity_Mart', 'OlivineCity_Mart'}


if __name__ == '__main__': validate()
