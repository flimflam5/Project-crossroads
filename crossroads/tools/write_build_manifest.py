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
    'version': 'black-ledger-ecruteak-olivine-qa09',
    'source_commit': sha,
    'dirty_tracked_sources': dirty,
    'rom': rom.name,
    'rom_sha256': hashlib.sha256(rom.read_bytes()).hexdigest(),
    'rom_bytes': rom.stat().st_size,
    'ci_run_id': os.environ.get('GITHUB_RUN_ID'),
    'summary': 'HGSS-directed Olivine city, canonical homes/cafe/services/Steel Gym, lighthouse stairs/balcony/native lift and port. Ecruteak source-correct furniture and full-width doors retained. Saves/IDs, owner Gyms, title/music/Joe/starters preserved.',
    'known_limitations': 'See crossroads/hgss/CITIES_QA09.md and per-city inventories for scope, exact tests and reference adaptations. Owner visual acceptance remains required. Original green-roof report is not positively matched to its source binary. DS online communication, unapproved rewards/story/badges and travel to other regions are deferred; the SS Aqua ship boundary is safe and explicit. No expansion elsewhere.',
    'testing': 'Compilation is not playtesting. Follow crossroads/TESTING.md.',
}
(root / 'build-info.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps(manifest, indent=2))
