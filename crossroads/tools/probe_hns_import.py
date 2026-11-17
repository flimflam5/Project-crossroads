#!/usr/bin/env python3
"""Inspect a donor map without importing assets or changing the game.

Fetches pinned public Heart & Soul source into memory only. The JSON report
is written to an explicitly supplied path outside the repository. A passing
probe validates binary shape, not art provenance, playability or HGSS fidelity.
"""
import argparse
from collections import Counter, deque
from hashlib import sha256
import json
from pathlib import Path
import struct
import urllib.request

REV = '167aa6d537b109bb229c231ddce4616974c4da71'
ROOT = Path(__file__).resolve().parents[2]
BASE = f'https://raw.githubusercontent.com/PokemonHnS-Development/pokehns-expansion/{REV}/'
FILES = {
    'layouts': 'data/layouts/layouts.json',
    'map': 'data/maps/AzaleaTown_House1_hns/map.json',
    'blocks': 'data/layouts/AzaleaTown_House1_hns/map.bin',
    'primary_metatiles': 'data/tilesets/primary/johto_building_hns/metatiles.bin',
    'primary_attributes': 'data/tilesets/primary/johto_building_hns/metatile_attributes.bin',
    'secondary_metatiles': 'data/tilesets/secondary/barn_hns/metatiles.bin',
    'secondary_attributes': 'data/tilesets/secondary/barn_hns/metatile_attributes.bin',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path, help='JSON report path outside the repository')
    output = parser.parse_args().output.resolve()
    if output.is_relative_to(ROOT):
        parser.error('report must be outside the game repository')
    data = {}
    for name, path in FILES.items():
        req = urllib.request.Request(BASE + path, headers={'User-Agent': 'BlackLedger-donor-probe'})
        with urllib.request.urlopen(req, timeout=30) as response:
            data[name] = response.read()
    donor_map = json.loads(data['map'])
    layouts = json.loads(data['layouts'])['layouts']
    layout = next(x for x in layouts if x['id'] == donor_map['layout'])
    assert layout['blockdata_filepath'] == FILES['blocks']
    assert len(data['blocks']) == 2 * layout['width'] * layout['height']
    cells = struct.unpack(f"<{len(data['blocks']) // 2}H", data['blocks'])
    # Expansion and this project's fieldmap use 10-bit ID, 2-bit collision,
    # 4-bit elevation. This checks shape and bounds, not behavioral equivalence.
    assert all(len(data[n]) % 16 == 0 for n in ('primary_metatiles', 'secondary_metatiles'))
    primary = len(data['primary_metatiles']) // 16
    secondary = len(data['secondary_metatiles']) // 16
    assert primary == 640
    assert len(data['primary_attributes']) == primary * 2
    assert len(data['secondary_attributes']) == secondary * 2
    ids = [v & 0x3ff for v in cells]
    invalid = sorted({x for x in ids if x >= primary and x - primary >= secondary})
    assert not invalid, f'out-of-range donor metatile IDs: {invalid}'
    destinations = json.loads((ROOT / 'data/layouts/layouts.json').read_text())['layouts']
    dest = next(x for x in destinations if x['id'] == 'LAYOUT_AZALEA_TOWN_WORKSHOP')
    existing_map = json.loads((ROOT / 'data/maps/AzaleaTown_Workshop/map.json').read_text())
    warps = []
    for warp in donor_map['warp_events']:
        x, y = warp['x'], warp['y']
        assert 0 <= x < layout['width'] and 0 <= y < layout['height']
        value = cells[y * layout['width'] + x]
        warps.append({'x': x, 'y': y, 'dest_map': warp['dest_map'],
                      'dest_warp_id': warp['dest_warp_id'], 'metatile': value & 0x3ff,
                      'collision': (value >> 10) & 3, 'elevation': value >> 12})
    # Normalize into separate fields rather than treating the raw donor map as
    # destination-ready. Walkability here is a conservative grid approximation:
    # special movement behaviors, events and layered graphics are not modeled.
    normalized = [{'x': i % layout['width'], 'y': i // layout['width'],
                   'id': v & 0x3ff, 'collision': (v >> 10) & 3,
                   'elevation': v >> 12} for i, v in enumerate(cells)]
    start = (warps[0]['x'], warps[0]['y'])
    queue, seen = deque([start]), {start}
    while queue:
        x, y = queue.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if not (0 <= nx < layout['width'] and 0 <= ny < layout['height']):
                continue
            n = normalized[ny * layout['width'] + nx]
            if (nx, ny) not in seen and n['collision'] == 0 and n['elevation'] == 3:
                seen.add((nx, ny))
                queue.append((nx, ny))
    result = {
        'donor_commit': REV,
        'source_sha256': {name: sha256(content).hexdigest() for name, content in data.items()},
        'donor_layout': layout,
        'donor_metatile_counts': {'primary': primary, 'secondary': secondary, 'used': len(set(ids)), 'invalid': invalid, 'in_incompatible_512_to_639_range': len([x for x in ids if 512 <= x < 640])},
        'normalized_cells': normalized,
        'simple_warp_connected_collision0_elevation3_cells': len(seen),
        'destination_tileset_split': 'Emerald uses 512 primary metatiles; HNS uses 640, so direct IDs cannot be interpreted in an Emerald layout.',
        'collision_histogram': dict(sorted(Counter(str((x >> 10) & 3) for x in cells).items())),
        'elevation_histogram': dict(sorted(Counter(str(x >> 12) for x in cells).items())),
        'warps': warps,
        'foreign_object_references': [{'graphics_id': x['graphics_id'], 'flag': x['flag'], 'script': x['script']} for x in donor_map['object_events']],
        'donor_music': donor_map['music'],
        'candidate_existing_layout': dest,
        'candidate_existing_map': {'id': existing_map['id'], 'layout': existing_map['layout'], 'warp_events': existing_map['warp_events']},
        'limitations': ['No game data or assets imported.', 'No art provenance, HGSS fidelity, visual layers, behavior, reachability or emulator verification.', 'Existing candidate is not asserted to be the same canonical building.', 'Donor scripts, object IDs, flags and warps require independent adaptation; do not copy blindly.'],
    }
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(f'Probe passed: {layout["width"]}x{layout["height"]}, {len(cells)} cells, '
          f'{primary}+{secondary} donor metatiles, {len(invalid)} invalid IDs. Report: {output}')


if __name__ == '__main__':
    main()
