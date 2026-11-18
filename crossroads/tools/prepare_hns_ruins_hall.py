#!/usr/bin/env python3
"""Pack the pinned Heart & Soul underground hall as a non-playable preview.

This is a source conversion probe, not a registered map or a gameplay test.
The donor's four direct chamber exits and its scripts are intentionally not
ported: HGSS chamber puzzles fall into the hall instead of providing exits.
"""
from pathlib import Path
import argparse
import hashlib
import json
import prepare_hns_ruins_pockets as packer

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'crossroads/donor/hns-ruins-hall'
REVISION = '167aa6d537b109bb229c231ddce4616974c4da71'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    target = ap.parse_args().output.resolve()
    assert not target.is_relative_to(ROOT), 'Preview must not alter game sources'
    source = json.loads((SOURCE / 'source-sha256.json').read_text())
    assert source['revision'] == REVISION
    for path, digest in source['files'].items():
        assert hashlib.sha256((SOURCE / path).read_bytes()).hexdigest() == digest, path
    packer.SOURCE = SOURCE
    group = {'source': 'RuinsOfAlph_B1F_hns', 'width': 29, 'height': 32,
             'primary': 'johto_building_hns', 'secondary': 'ruins_of_alph_b1_f_hns',
             'crops': {'UndergroundHall': (0, 0, 29, 32)}}
    report = packer.convert(group, target)
    report['limitations'] = [
        'No playable map, game event, direct chamber warp or hall entry is registered.',
        'The donor has four chamber exits, whereas HGSS uses puzzle falls; do not copy them.',
        'Source geometry and converted attributes have not been tested in the engine.',
        'HGSS has a separate hall-entrance map; it still needs implementation.',
    ]
    (target / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print('Packed unregistered donor Underground Hall; no game content changed.')


if __name__ == '__main__':
    main()
