#!/usr/bin/env python3
"""Install native, coordinate-scoped post-spawn facing for reviewed gate landings.

Run centrally AFTER existing map generators. No tile, collision, warp, identifier,
engine constant, save structure or saved story flag is changed. This uses the
native immediate OnWarp/turnobject mechanism plus a direct post-spawn OnReturn
hook for normal Continue and menu/battle returns at the exact portal landings.
"""
import argparse
import json
from pathlib import Path

R = Path(__file__).resolve().parents[2]
BEGIN = '@ BEGIN QA10 COORDINATE-SCOPED ARRIVAL FACING'
END = '@ END QA10 COORDINATE-SCOPED ARRIVAL FACING'
# Physical landing directions fixed before reading B4 runtime records. These
# are public arrival anchors, not active doors or invented geographic links.
LANDINGS = {
    'EcruteakCity': [(7, y, 'DIR_EAST') for y in range(37, 40)]
        + [(59, y, 'DIR_WEST') for y in range(46, 49)],
    'JohtoRoute38': [(62, y, 'DIR_WEST') for y in range(12, 15)],
    'JohtoRoute42': [(3, y, 'DIR_EAST') for y in range(13, 16)],
    'EcruteakCity_WestGate': [(1, y, 'DIR_EAST') for y in range(6, 9)]
        + [(10, y, 'DIR_WEST') for y in range(6, 9)],
    'EcruteakCity_EastGate': [(1, y, 'DIR_EAST') for y in range(6, 9)]
        + [(10, y, 'DIR_WEST') for y in range(6, 9)],
    'EcruteakCity_BarrierCorridor': [(6, 3, 'DIR_SOUTH')],
}


def render(name, original):
    if name not in LANDINGS:
        return original
    prefix = 'Qa10_' + name + '_ArrivalFacing'
    hook = '    map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, ' + prefix + '_Table\n'
    return_hook = '    map_script MAP_SCRIPT_ON_RETURN_TO_FIELD, ' + prefix + '\n'
    if BEGIN in original:
        assert original.count(BEGIN) == original.count(END) == 1
        before, rest = original.split(BEGIN, 1)
        _, after = rest.split(END, 1)
        original = (before + after.lstrip('\n')).rstrip() + '\n'
        assert hook in original
        original = original.replace(hook, '', 1)
        # Accept the earlier source-only one-hook prototype, but never remove
        # an unrelated existing return callback while adding the reviewed one.
        if return_hook in original:
            original = original.replace(return_hook, '', 1)
    assert 'MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE' not in original, (
        name, 'Existing OnWarp callback must be explicitly composed, never overwritten')
    assert 'MAP_SCRIPT_ON_RETURN_TO_FIELD' not in original, (
        name, 'Existing OnReturn callback must be explicitly composed, never overwritten')
    marker = '    .byte 0'
    assert marker in original and name + '_MapScripts::' in original
    original = original.replace(marker, hook + return_hook + marker, 1).rstrip() + '\n\n'
    rows = LANDINGS[name]
    # MapHeaderCheckScriptTable compares VarGet(first) with VarGet(second).
    # Comparing the same existing temp variable always succeeds without writing it.
    lines = [BEGIN, prefix + '_Table:',
        '    map_script_2 VAR_TEMP_0, VAR_TEMP_0, ' + prefix,
        '    .2byte 0', '', prefix + '::',
        '    getplayerxy VAR_0x8004, VAR_0x8005']
    xs = sorted({x for x, _, _ in rows})
    for x in xs:
        lines.append(f'    goto_if_eq VAR_0x8004, {x}, {prefix}_X{x}')
    lines.append('    end')
    for x in xs:
        lines += ['', f'{prefix}_X{x}:']
        for _, y, direction in [r for r in rows if r[0] == x]:
            lines.append(f'    goto_if_eq VAR_0x8005, {y}, {prefix}_{direction}')
        lines.append('    end')
    for direction in sorted({d for _, _, d in rows}):
        lines += ['', prefix + '_' + direction + ':',
            '    turnobject LOCALID_PLAYER, ' + direction, '    end']
    lines += [END, '']
    return original + '\n'.join(lines)


def generate(check=False, output_root=R):
    review = []
    for name, rows in LANDINGS.items():
        rel = Path(f'data/maps/{name}/scripts.inc')
        data = render(name, (R / rel).read_text()).encode()
        dest = output_root / rel
        if check:
            assert dest.exists() and dest.read_bytes() == data, ('Regenerate native arrival-facing callback', name)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not dest.exists() or dest.read_bytes() != data:
                dest.write_bytes(data)
        review.append(dict(map=name, callbacks=['MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE','MAP_SCRIPT_ON_RETURN_TO_FIELD'],
            coordinate_scratch=['VAR_0x8004', 'VAR_0x8005'],
            table_condition='VAR_TEMP_0 equals itself; read only',
            landings=[dict(x=x, y=y, facing=d) for x, y, d in rows]))
    value = dict(source_failure_checkpoint='df8c4598d88c7770626be4621a5f39cf60dadb95',
        method='Native immediate post-spawn turnobject on normal warp and field return, restricted to25 reviewed landing coordinates in6 maps.',
        changes_to_tiles_collision_warps_ids_save_flags=False,
        continue_behavior='Normal Continue uses ReturnToFieldLocal and InitObjectEventsReturnToField, not OnWarp. The direct OnReturn hook runs after objects spawn and normalizes only the25 portal coordinates, including after menu/battle returns. Other coordinates and persistent data are untouched.',
        maps=review, runtime_qa='PENDING actual repaired build')
    dest = output_root/'crossroads/hgss/qa10/arrival-facing-repair-review.json'
    data = (json.dumps(value, indent=2) + '\n').encode()
    if check:
        assert dest.exists() and dest.read_bytes() == data, 'Regenerate arrival-facing review'
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not dest.exists() or dest.read_bytes() != data:
            dest.write_bytes(data)
    print('Native arrival-facing callback source:', len(review), 'maps;', sum(len(r) for r in LANDINGS.values()), 'landings; actual repaired-build tests pending')
    return value


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--check', action='store_true')
    p.add_argument('--output-root', type=Path, default=R, help='Source-only prototype root; does not modify game resources in the working checkout')
    a = p.parse_args()
    generate(a.check, a.output_root)
