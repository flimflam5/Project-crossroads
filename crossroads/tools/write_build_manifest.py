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
    'version': 'black-ledger-ecruteak-qa08-doorways',
    'source_commit': sha,
    'dirty_tracked_sources': dirty,
    'rom': rom.name,
    'rom_sha256': hashlib.sha256(rom.read_bytes()).hexdigest(),
    'rom_bytes': rom.stat().st_size,
    'ci_run_id': os.environ.get('GITHUB_RUN_ID'),
    'summary': 'Repair both Theater/Barrier leaves and all three rows of both Ecruteak gate aisles. Preserve accepted exterior pixels, owner Gym, stable IDs and saves. Independent segment trials plus city/landmark/service/save regressions.',
    'known_limitations': 'See crossroads/hgss/ECRUTEAK_QA08.md and CITY_BUILDING_INVENTORY_QA08.json. Doorway repair checkpoint, not final city acceptance. Green-roof report remains unmatched; full HGSS interior raster matching and gate exterior placement are unfinished. Olivine is authorized next but is not reconstructed by this checkpoint. DS online desks are offline; story/rewards/badges remain deferred. No expansion elsewhere.',
    'testing': 'Compilation is not playtesting. Follow crossroads/TESTING.md.',
}
(root / 'build-info.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps(manifest, indent=2))
