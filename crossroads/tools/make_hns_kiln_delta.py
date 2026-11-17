#!/usr/bin/env python3
"""Make a small, verified delta between QA10 and an already-tested ROM.

Only a binary patch is written. ROM blobs are staged solely in a temporary Git
repository, which is destroyed; nothing is added to the project Git index.
"""
import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
import tempfile

BASE_HASH = 'ee2d81d5d0b55b7f1f9d36d1c9b055700164da439f51af7a66b5fb2d2147f90b'
MAX_DELTA_BYTES = 4 * 1024 * 1024


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-rom', required=True, type=Path)
    parser.add_argument('--tested-rom', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    assert not args.output.exists(), 'Refusing to overwrite a prior delta'
    assert digest(args.base_rom) == BASE_HASH and args.base_rom.stat().st_size == 33554432
    assert args.tested_rom.stat().st_size == 33554432
    tested_hash = digest(args.tested_rom)
    assert tested_hash != BASE_HASH, 'Candidate is identical to QA10'
    with tempfile.TemporaryDirectory(prefix='hns-kiln-delta-') as temp:
        folder = Path(temp)
        subprocess.run(['git', 'init', '--quiet', str(folder)], check=True)
        rom = folder / 'pokeemerald.gba'
        shutil.copyfile(args.base_rom, rom)
        subprocess.run(['git', 'add', '--', rom.name], cwd=folder, check=True)
        shutil.copyfile(args.tested_rom, rom)
        patch = subprocess.check_output(['git', 'diff', '--binary', '--full-index', '--', rom.name], cwd=folder)
        assert patch.startswith(b'diff --git ') and b'GIT binary patch' in patch, 'No Git binary patch'
        assert len(patch) <= MAX_DELTA_BYTES, 'Delta exceeds 4 MiB; use a verified CI artifact instead'
        shutil.copyfile(args.base_rom, rom)
        subprocess.run(['git', 'apply', '--binary', '-'], cwd=folder, input=patch, check=True)
        assert digest(rom) == tested_hash, 'Reconstructed candidate differs'
    args.output.write_bytes(patch)
    print(f'Delta: {len(patch)} bytes; SHA256 {hashlib.sha256(patch).hexdigest()}')
    print(f'Exact tested ROM SHA256: {tested_hash}')


if __name__ == '__main__':
    main()
