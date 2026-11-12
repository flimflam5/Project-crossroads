#!/usr/bin/env python3
"""Recover exact tested QA10 bytes for durable downloads; never compile a game.

The input is this repository's own pinned CI artifact, not a commercial base ROM.
A small Git binary delta accounts for compiler differences. Both input and output
are SHA256-bound; the untested CI cartridge is never included in the downloads.
Evidence is read from the immutable tested source, not the current working tree.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / 'crossroads/delivery/qa10-downloads.json'
PATCH = ROOT / 'crossroads/delivery/qa10-ci-to-tested.patch'
FORBIDDEN = {'.gba', '.elf', '.sav', '.srm', '.state', '.snapshot', '.raw',
             '.dump', '.narc', '.nds', '.bios'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def source_file(commit, name):
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts, name
    return git('show', commit + ':' + name)


def member(z, name, data):
    p = PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts, name
    info = zipfile.ZipInfo(name, date_time=(2026, 11, 12, 0, 0, 0))
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    z.writestr(info, data, compresslevel=9)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument('--base-archive', type=Path)
    inputs.add_argument('--base-rom', type=Path,
                        help='Local verification with an already-extracted hash-bound CI base')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    spec = json.loads(SPEC.read_text())
    source = spec['source_commit']
    assert git('rev-parse', source + '^{tree}').decode().strip() == spec['source_tree']
    assert digest(PATCH.read_bytes()) == spec['patch_sha256'], 'Delivery patch changed'
    assert PATCH.stat().st_size < 2 * 1024 * 1024, 'Not a small binary delta'
    if args.base_archive:
        assert digest(args.base_archive.read_bytes()) == spec['base_artifact_sha256'], 'Wrong CI artifact'
        with zipfile.ZipFile(args.base_archive) as z:
            base = z.read('pokeemerald.gba')
    else:
        base = args.base_rom.read_bytes()
    assert len(base) == spec['rom_bytes'] and digest(base) == spec['base_rom_sha256'], 'Wrong CI ROM'
    verification = source_file(source, 'crossroads/qa/qa10/verification-summary.json')
    verified = json.loads(verification)
    assert verified['final_runtime_passed'] and verified['automated_checks_passed']
    assert verified['rom_sha256'] == spec['tested_rom_sha256']
    info = spec['build_info']
    assert info['source_commit'] == source and info['source_tree'] == spec['source_tree']
    assert not info['dirty_tracked_sources'] and info['rom_sha256'] == spec['tested_rom_sha256']
    assert not args.output.exists(), 'Refusing to overwrite a prior delivery'
    args.output.mkdir(parents=True)
    stem = spec['stem']
    direct = args.output / (stem + '.gba')
    # git apply reads the base working file; no ROM is added to an index/commit.
    with tempfile.TemporaryDirectory(prefix='qa10-exact-') as folder:
        folder = Path(folder)
        subprocess.run(['git', 'init', '--quiet', str(folder)], check=True)
        rom = folder / 'pokeemerald.gba'
        rom.write_bytes(base)
        subprocess.run(['git', 'apply', '--binary', str(PATCH)], cwd=folder, check=True)
        data = rom.read_bytes()
        assert len(data) == spec['rom_bytes'] and digest(data) == spec['tested_rom_sha256'], 'Not the exact tested ROM'
        shutil.move(str(rom), direct)
    del base, data
    release = source_file(source, 'crossroads/RELEASE_OLIVINE_AQUA_QA10.md')
    build_info = (json.dumps(info, indent=2) + '\n').encode()
    archive = args.output / (stem + '.zip')
    with zipfile.ZipFile(archive, 'x') as z:
        member(z, direct.name, direct.read_bytes())
        member(z, 'README-DELTA.md', release)
        member(z, 'build-info.json', build_info)
        member(z, 'verification-summary.json', verification)
    evidence = args.output / (stem + '-Evidence.zip')
    roots = ['crossroads/qa/qa10', 'crossroads/hgss/qa10']
    extra = ['crossroads/RELEASE_OLIVINE_AQUA_QA10.md', 'crossroads/STATUS.md',
             'crossroads/hgss/ACTIVE_COMPLETION.md', 'crossroads/TESTING.md']
    paths = git('ls-tree', '-r', '--name-only', source, '--', *roots, *extra).decode().splitlines()
    assert len(paths) > 2000, 'Missing source evidence'
    readme = ('# Black Ledger QA10 evidence\n\nOpen crossroads/qa/qa10/index.html for '
              'actual screenshots, recordings and before/after comparisons.\n\n'
              'Source: ' + source + '\nTested ROM SHA256: ' + spec['tested_rom_sha256'] +
              '\nOwner Delta/visual approval remains pending. Historical failures stay '
              'labelled; only final/B5 applies to this ROM. No private saves are included.\n')
    with zipfile.ZipFile(evidence, 'x') as z:
        member(z, 'README.md', readme.encode())
        member(z, 'build-info.json', build_info)
        for name in paths:
            assert PurePosixPath(name).suffix.lower() not in FORBIDDEN, name
            member(z, name, source_file(source, name))
    for path in (archive, evidence):
        with zipfile.ZipFile(path) as z:
            assert z.testzip() is None, 'Archive CRC failed'
            actual_info = json.loads(z.read('build-info.json'))
            assert actual_info == info
            if path == archive:
                assert digest(z.read(direct.name)) == spec['tested_rom_sha256']
            else:
                assert not any(PurePosixPath(n).suffix.lower() in FORBIDDEN for n in z.namelist())
    files = [direct, archive, evidence]
    sums = {path.name: digest(path.read_bytes()) for path in files}
    (args.output / (stem + '-SHA256.txt')).write_text(''.join(sums[p.name] + '  ' + p.name + '\n' for p in files))
    prefix = 'https://github.com/flimflam5/Project-crossroads/releases/download/' + spec['tag'] + '/'
    names = [p.name for p in files] + [stem + '-SHA256.txt', stem + '-Delivery.json']
    delivery = {'source_commit': source, 'game_source_checkpoint': spec['game_source_checkpoint'],
                'rom_sha256': spec['tested_rom_sha256'], 'rom_bytes': spec['rom_bytes'],
                'downloads': {n: prefix + n for n in names}, 'asset_sha256': sums,
                'base_artifact_id': spec['base_artifact_id'], 'ci_rom_not_distributed': True,
                'method': 'Exact tested ROM recovered from pinned own-source CI build using a hash-bound binary delta; no game rebuild. Archives repackaged from immutable tested source.',
                'archive_crcs_verified': True, 'private_saves_included': False,
                'owner_delta_and_visual_acceptance': 'PENDING'}
    (args.output / (stem + '-Delivery.json')).write_text(json.dumps(delivery, indent=2) + '\n')
    notes = ('# Pokémon: Black Ledger — QA10 A1\n\n'
             'Permanent downloads for the exact Delta QA candidate. **Owner visual review '
             'is pending; this is a QA prerelease, not a finished game.**\n\n'
             '- Download **' + stem + '.zip** for the ROM and Delta checklist.\n'
             '- Download **' + stem + '-Evidence.zip** for screenshots and recordings.\n\n'
             'ROM SHA256: `' + spec['tested_rom_sha256'] + '`\n\n'
             'Source: `' + source + '`\n\n'
             'The cartridge is byte-identical to the verified local B5 build. The separate '
             'CI compilation is not supplied. Archives are repackaged; current archive '
             'checksums accompany these downloads. No private saves or commercial base ROMs '
             'are included. Back up your save and use normal Continue with a copy.\n\n'
             'Sailing, some HGSS services, mounted-bike art and inherited opening content '
             'remain explicit limits. See included per-location notes.\n\n'
             'Source review: https://github.com/flimflam5/Project-crossroads/pull/17\n')
    (args.output / 'RELEASE.md').write_text(notes)
    print(json.dumps({'tested_rom_sha256': spec['tested_rom_sha256'], 'evidence_files': len(paths),
                      'archive_checksums': sums, 'source_commit': source, 'private_saves': False}, indent=2))


if __name__ == '__main__':
    main()
