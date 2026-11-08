#!/usr/bin/env python3
"""Identify the exact source and ROM in a development artifact."""
import hashlib
import json
import os
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[2]
rom = root / 'pokeemerald.gba'
sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
dirty = bool(subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=root))
manifest = {
    'version': 'black-ledger-olivine-detail-0.7',
    'source_commit': sha,
    'dirty_tracked_sources': dirty,
    'rom': rom.name,
    'rom_sha256': hashlib.sha256(rom.read_bytes()).hexdigest(),
    'rom_bytes': rom.stat().st_size,
    'ci_run_id': os.environ.get('GITHUB_RUN_ID'),
    'summary': 'Detail the existing Olivine workplace and harbor offices; add home rest and records interactions while preserving the accepted 0.6 area.',
    'known_limitations': 'See crossroads/RELEASE_0_7.md. First existing-area detail pass; lighthouse/tower/Gym and route content remain unfinished. New cities/routes paused. Delta QA pending.',
    'testing': 'Compilation is not playtesting. Follow crossroads/TESTING.md.',
}
(root / 'build-info.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps(manifest, indent=2))
