"""Exact HGSS common-Mart props; four solid stool bases, no event/progress changes."""
import json
from pathlib import Path

R = Path(__file__).resolve().parents[2]
CONTRACT = 'crossroads/hgss/contracts/mart-props-qa09.json'
SECONDARY = 'gTileset_HgssMart'


def apply_mart_furnishings(m, tiles, width, height):
    """Apply reviewed native art and solid stool bases without changing identity.

    Called on the complete original common-Mart layout before it is saved. The
    identical HGSS Olivine service module subsequently clones this result.
    """
    c = json.loads((R / CONTRACT).read_text())
    assert m['name'] == 'EcruteakCity_Mart'
    assert (width, height) == (14, 13)
    assert list(tiles) == c['before_words'], 'Common Mart source changed before prop conversion'
    for p in c['changes']:
        i = p['y'] * width + p['x']
        assert tiles[i] == p['before']
        expected_bits = p['before'] & 0xfc00
        if (p['x'], p['y']) in {(7, 9), (7, 10), (10, 9), (10, 10)}:
            expected_bits |= 0x400  # Actual source stool model ground footprint.
        assert p['after'] & 0xfc00 == expected_bits
        tiles[i] = p['after']
    return SECONDARY
