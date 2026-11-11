#!/usr/bin/env python3
"""Regression for exact include-guard insertion and non-destructive replacement."""
import re
from pathlib import Path
from tileset_registration import TILESETS_GUARD_END, upsert

R = Path(__file__).resolve().parents[2]
EXTERNS = {
    'ECRUTEAK THEATER STAGE': 'HgssTheater',
    'ECRUTEAK GATE INTERIOR ART': 'HgssGateInterior',
    'HGSS CENTER BASEMENT': 'HgssCenterBasement',
    'HGSS COMMON MART PROPS': 'HgssMart',
    'HGSS CENTER RECEPTION': 'HgssCenterReception',
    'ECRUTEAK TOWER DETAILS': 'HgssEcruteakTowerDetails',
}


def section(name, body):
    return f'// BEGIN {name}\n#if !IS_FRLG\n{body}\n#endif\n// END {name}'


def validate():
    # The historical bug used the last #endif, which can belong to a generated
    # resource after the real include guard. First insertion must choose the
    # exact guard boundary even when another conditional follows it.
    seed = '#ifndef GUARD_tilesets_H\n#define GUARD_tilesets_H\n' + TILESETS_GUARD_END + '\n#if OTHER\n#endif\n'
    fresh = section('FRESH', 'extern int fresh;')
    inserted = upsert(seed, '// BEGIN FRESH', '// END FRESH', fresh, externs=True)
    assert inserted.index(fresh) < inserted.index(TILESETS_GUARD_END)
    assert upsert(inserted, '// BEGIN FRESH', '// END FRESH', fresh, externs=True) == inserted

    # Reproduce Tower nested inside Reception. Updating Reception must preserve
    # Tower's complete declaration/condition instead of deleting foreign work.
    child = section('CHILD', 'extern int child;')
    nested = section('PARENT', 'extern int old;\n' + child)
    seed = seed.replace(TILESETS_GUARD_END, nested + '\n' + TILESETS_GUARD_END)
    parent = section('PARENT', 'extern int replacement;')
    updated = upsert(seed, '// BEGIN PARENT', '// END PARENT', parent, externs=True)
    assert parent + '\n' + child in updated and updated.count(child) == 1
    assert updated.index(child) < updated.index(TILESETS_GUARD_END)
    assert upsert(updated, '// BEGIN PARENT', '// END PARENT', parent, externs=True) == updated
    for malformed in [seed.replace('// END CHILD', '// END WRONG'), seed.replace(TILESETS_GUARD_END, '#endif')]:
        try:
            upsert(malformed, '// BEGIN PARENT', '// END PARENT', parent, externs=True)
        except (AssertionError, ValueError):
            pass
        else:
            raise AssertionError('Malformed generated/header boundaries accepted')

    # The six actual new blocks must be independent siblings inside the header
    # guard, each retaining its own !IS_FRLG condition and exact declaration.
    text = (R / 'include/tilesets.h').read_text()
    stack = []
    seen = set()
    for line in text.splitlines():
        if line.startswith('// BEGIN '):
            name = line[len('// BEGIN '):]
            if name in EXTERNS:
                assert stack == ['#ifndef GUARD_tilesets_H'], ('Extern section not a guarded sibling', name, stack)
                expected = section(name, 'extern const struct Tileset gTileset_' + EXTERNS[name] + ';')
                assert text.count(expected) == 1, ('Generated extern differs or duplicates', name)
                seen.add(name)
        if re.match(r'^#if(?:n?def)?\b', line):
            stack.append(line)
        elif re.match(r'^#endif\b', line):
            assert stack, ('Unmatched #endif', line)
            if line == TILESETS_GUARD_END:
                assert stack == ['#ifndef GUARD_tilesets_H'], 'Wrong include guard closure'
            stack.pop()
    assert not stack and seen == set(EXTERNS)
    assert text.count(TILESETS_GUARD_END) == 1
    print('Tileset registration: exact guard insertion, foreign-section preservation, idempotence and six guarded sibling externs: PASS')


if __name__ == '__main__':
    validate()
