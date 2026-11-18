#!/usr/bin/env python3
"""Package an already-tested Union Cave and Ruins ROM, recovered from our QA10 release.

The delivery spec and binary delta are created only after gameplay verification.
No game is compiled and no ROM is added to the repository. The exact input,
delta, output and immutable source/evidence revisions are SHA256-bound.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / 'crossroads/delivery/hns-union-ruins/spec.json'
PATCH = ROOT / 'crossroads/delivery/hns-union-ruins/qa10-to-tested.patch'
BASE_HASH = 'ee2d81d5d0b55b7f1f9d36d1c9b055700164da439f51af7a66b5fb2d2147f90b'
ALLOWED = {'.png', '.jpg', '.jpeg', '.gif', '.webm', '.mp4', '.md', '.json', '.txt', '.log'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def source(commit, name):
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts and p.suffix.lower() in ALLOWED, name
    return subprocess.check_output(['git', 'show', commit + ':' + name], cwd=ROOT)


def member(z, name, data):
    info = zipfile.ZipInfo(name, date_time=(2026, 11, 17, 0, 0, 0))
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    z.writestr(info, data, compresslevel=9)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-rom', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    spec = json.loads(SPEC.read_text())
    for field in ('source_commit', 'source_tree', 'evidence_commit'):
        assert re.fullmatch(r'[0-9a-f]{40}', spec[field]), field
    for field in ('rom_sha256', 'patch_sha256'):
        assert re.fullmatch(r'[0-9a-f]{64}', spec[field]), field
    assert re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', spec['stem'])
    assert re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]*', spec['tag'])
    for field in ('source_commit', 'evidence_commit'):
        subprocess.run(['git', 'cat-file', '-e', spec[field] + '^{commit}'], cwd=ROOT, check=True)
    tree = subprocess.check_output(['git', 'rev-parse', spec['source_commit'] + '^{tree}'], cwd=ROOT, text=True).strip()
    assert tree == spec['source_tree'], 'Source tree differs from tested source'
    assert digest(args.base_rom.read_bytes()) == BASE_HASH, 'Incorrect QA10 base'
    assert args.base_rom.stat().st_size == 33554432
    assert digest(PATCH.read_bytes()) == spec['patch_sha256'], 'Binary delta differs'
    record = json.loads(source(spec['evidence_commit'], spec['verification_record']))
    assert record['source_commit'] == spec['source_commit'] and record['rom_sha256'] == spec['rom_sha256']
    assert record['automated_checks_passed'] is True and record['runtime_checks_passed'] is True
    files = spec['evidence_files']
    assert isinstance(files, list) and files and len(files) == len(set(files))
    evidence = [(name, source(spec['evidence_commit'], name)) for name in files]
    notes = source(spec['evidence_commit'], spec['release_notes'])
    assert not args.output.exists(), 'Refusing to overwrite an existing delivery'
    assets = args.output / 'assets'
    assets.mkdir(parents=True)
    stem = spec['stem']
    direct = assets / (stem + '.gba')
    with tempfile.TemporaryDirectory(prefix='hns-union-ruins-recover-') as temp:
        folder = Path(temp)
        subprocess.run(['git', 'init', '--quiet', str(folder)], check=True)
        rom = folder / 'pokeemerald.gba'
        shutil.copyfile(args.base_rom, rom)
        subprocess.run(['git', 'apply', '--binary', str(PATCH)], cwd=folder, check=True)
        data = rom.read_bytes()
        assert len(data) == 33554432 and digest(data) == spec['rom_sha256'], 'Recovered ROM differs from tested ROM'
        shutil.move(str(rom), direct)
    rom_zip = assets / (stem + '.zip')
    with zipfile.ZipFile(rom_zip, 'x') as z:
        member(z, direct.name, direct.read_bytes())
        member(z, 'README-DELTA.md', notes)
        member(z, 'verification-summary.json', json.dumps(record, indent=2).encode() + b'\n')
    evidence_zip = assets / (stem + '-Evidence.zip')
    with zipfile.ZipFile(evidence_zip, 'x') as z:
        member(z, 'verification-summary.json', json.dumps(record, indent=2).encode() + b'\n')
        for name, data in evidence:
            member(z, name, data)
    for path in (rom_zip, evidence_zip):
        with zipfile.ZipFile(path) as z:
            assert z.testzip() is None
            if path == rom_zip:
                assert digest(z.read(direct.name)) == spec['rom_sha256']
    downloadable = [direct, rom_zip, evidence_zip]
    sums = {p.name: digest(p.read_bytes()) for p in downloadable}
    (assets / (stem + '-SHA256.txt')).write_text(''.join(f'{h}  {n}\n' for n, h in sums.items()))
    metadata = {'source_commit': spec['source_commit'], 'source_tree': spec['source_tree'],
                'evidence_commit': spec['evidence_commit'], 'rom_sha256': spec['rom_sha256'],
                'assets_sha256': sums, 'owner_visual_acceptance': 'pending',
                'method': 'Hash-verified delta from the previously published QA10 game build.'}
    (assets / (stem + '-Delivery.json')).write_text(json.dumps(metadata, indent=2) + '\n')
    (args.output / 'RELEASE.md').write_bytes(notes)
    print(json.dumps(metadata, indent=2))


if __name__ == '__main__':
    main()
