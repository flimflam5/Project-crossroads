#!/usr/bin/env python3
"""Strictly audit recorded native arrival directions against physical intent.

This reads actual controller-result records. It does not run an emulator, alter
an opening contract, or infer desired directions from observed directions.
"""
import argparse
import hashlib
import json
from pathlib import Path

R = Path(__file__).resolve().parents[2]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--contract', type=Path, default=R/'crossroads/hgss/qa10/doorway-intended-facing-b4.json')
p.add_argument('--results', type=Path, help='Completed doorway-results.json; required for a final PASS')
p.add_argument('--log', type=Path, help='Read line-delimited trial records from an ongoing diagnostic log')
p.add_argument('--output', type=Path, required=True)
p.add_argument('--allow-partial', action='store_true', help='Write an explicitly non-final diagnostic; never labels incomplete coverage PASS')
a = p.parse_args()
assert bool(a.results) != bool(a.log), 'Choose exactly one completed --results file or diagnostic --log'
assert not a.log or a.allow_partial, 'Raw logs lack final ROM/save identity; --log requires --allow-partial'
contract = json.loads(a.contract.read_text())
assert len(contract['groups']) == 45
known = {}
for group in contract['groups']:
    for side, source in group['sides'].items():
        target_side = 'inside' if side == 'outside' else 'outside'
        desired = group['sides'][target_side]['intended_arrival_facing']
        assert desired in [1, 2, 3, 4]
        for i, cell in enumerate(source['segments']):
            for approach in ['front', 'lateral-negative', 'lateral-positive']:
                label = f"{group['label']}-{side}-{i}-{approach}"
                assert label not in known
                known[label] = dict(group=group['label'], side=side,
                    target_side=target_side, source=source['map'], segment=cell,
                    expected_destination=group['sides'][target_side]['map'],
                    intended_arrival_facing=desired, approach=approach)
assert len(known) == 519
identity_errors = []
if a.results:
    report = json.loads(a.results.read_text())
    rows = report['results']
    for key in ['rom_sha256', 'visible_opening_contract_sha256']:
        if report.get(key) != contract[key]:
            identity_errors.append(dict(key=key, actual=report.get(key), expected=contract[key]))
    if not report.get('source_save_unchanged'):
        identity_errors.append(dict(key='source_save_unchanged', actual=report.get('source_save_unchanged'), expected=True))
else:
    rows = []
    for line in a.log.read_text().splitlines():
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row, dict) and 'label' in row:
            rows.append(row)
seen = set()
failures = []
passed = []
unavailable = []
for row in rows:
    label = row['label']
    if label not in known or label in seen:
        failures.append(dict(label=label, problem='Unknown or duplicate trial record'))
        continue
    seen.add(label)
    expected = known[label]
    for key in ['source', 'segment', 'expected_destination']:
        if row.get(key) != expected[key]:
            failures.append(dict(label=label, problem=key, actual=row.get(key), expected=expected[key]))
    if row.get('result') == 'inaccessible lateral approach':
        if expected['approach'] == 'front':
            failures.append(dict(label=label, problem='A required front approach was skipped'))
        else:
            unavailable.append(label)
        continue
    if row.get('result') != 'PASS':
        failures.append(dict(label=label, problem='Actual controller attempt failed', record=row))
        continue
    desired = expected['intended_arrival_facing']
    if row.get('facing') != desired:
        failures.append(dict(label=label, problem='Incorrect actual arrival facing',
            source=row['source'], destination=row['expected_destination'],
            arrival=row.get('arrival'), actual=row.get('facing'), expected=desired))
    else:
        passed.append(label)
missing = sorted(set(known) - seen)
final = bool(a.results and not missing and not identity_errors)
success = bool(final and not failures)
result = dict(contract=str(a.contract),
    contract_sha256=hashlib.sha256(a.contract.read_bytes()).hexdigest(),
    intended_source_revision=contract['source_revision'],
    intended_rom_sha256=contract['rom_sha256'],
    method='Physical-facing expectations existed before reading trial facing results; no emulator or game writes.',
    final_coverage=final, passed=success, groups=45, expected_attempts=len(known),
    recorded_attempts=len(rows), exact_facing_passes=len(passed),
    physically_unavailable_lateral_approaches=len(unavailable),
    missing_attempts=missing, identity_errors=identity_errors, failures=failures,
    no_facing_claim_for_unavailable_approaches=True)
a.output.parent.mkdir(parents=True, exist_ok=True)
a.output.write_text(json.dumps(result, indent=2)+'\n')
print('Native arrival-facing audit:', len(rows), '/', len(known), 'records;',
      len(passed), 'correct facings;', len(unavailable), 'unavailable lateral approaches;',
      len(failures), 'failures;', len(missing), 'missing;', 'FINAL PASS' if success else 'NOT PASS')
if failures or identity_errors or (not final and not a.allow_partial):
    raise SystemExit(1)
