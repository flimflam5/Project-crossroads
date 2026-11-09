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
    'version': 'black-ledger-title-audio-0.8.2',
    'source_commit': sha,
    'dirty_tracked_sources': dirty,
    'rom': rom.name,
    'rom_sha256': hashlib.sha256(rom.read_bytes()).hexdigest(),
    'rom_bytes': rom.stat().st_size,
    'ci_run_id': os.environ.get('GITHUB_RUN_ID'),
    'summary': 'Refine title audio with a matching native playback rate and title-only DAC/mixer settings; preserve accepted 0.8/0.8.1 gameplay and loop.',
    'known_limitations': 'See crossroads/RELEASE_0_8_2.md. Badges and story gates deferred; original intro and Joe special movement art remain. Delta audio-quality comparison pending.',
    'testing': 'Compilation is not playtesting. Follow crossroads/TESTING.md.',
}
(root / 'build-info.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps(manifest, indent=2))
