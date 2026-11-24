#!/usr/bin/env python3
"""Verify donor puzzle assets, approved staged calls and existing special ordinals.

This checks source identity and wiring only; it does not test gameplay,
controls, emulator graphics, map return, or the full ROM link.
"""
from pathlib import Path
import hashlib,json,re,subprocess
R=Path(__file__).resolve().parents[2]
manifest=json.loads((R/'crossroads/donor/hns-ruins-pockets/puzzle-source-sha256.json').read_text())
assert manifest['revision']=='167aa6d537b109bb229c231ddce4616974c4da71'
adapted={'src/sliding_puzzle.c','src/data/sliding_puzzles.h','include/sliding_puzzle.h'}
for path,digest in manifest['files'].items():
    assert (R/path).is_file(),path
    if path not in adapted:assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,('Donor asset changed',path)
prior=subprocess.check_output(['git','show','9b97772586:data/specials.inc'],cwd=R,text=True)
current=(R/'data/specials.inc').read_text()
def entries(text):return re.findall(r'^\s*def_special\s+([A-Za-z_][A-Za-z0-9_]*)',text,re.M)
old,new=entries(prior),entries(current)
assert len(old)==624 and new==old+['DoSlidingPuzzle','Crossroads_AlphHasNonEggHoOh'],'An existing special ordinal changed or expected puzzle/party specials missing'
code=(R/'src/sliding_puzzle.c').read_text()
assert 'void DoSlidingPuzzle(void)' in code and 'gSpecialVar_Result' in code
assert not re.search(r'\b(?:FlagSet|FlagClear|GiveItem|AddBagItem|RemoveBagItem)\s*\(',code),'Puzzle must not grant items or set flags'
uses=[]
for root in (R/'data/maps',R/'crossroads/scripts'):
    for path in root.rglob('*.inc'):
        if 'DoSlidingPuzzle' in path.read_text():uses.append(str(path.relative_to(R)))
expected={'data/maps/RuinsOfAlph_SouthwestChamber/scripts.inc',
          'data/maps/RuinsOfAlph_NorthwestChamber/scripts.inc'}
assert set(uses)==expected,('Unexpected puzzle caller or missing chamber',uses)
for path in uses:
    script=(R/path).read_text()
    assert script.count('special DoSlidingPuzzle')==1
    assert 'warp MAP_RUINS_OF_ALPH_UNDERGROUND_HALL' in script
    assert not re.search(r'^\s*(?:setflag|clearflag|giveitem|removeitem)\b',script,re.M),path
print('PASS: pinned puzzle assets, preserved 624 special ordinals, appended puzzle/party specials, two chamber calls and no flags/rewards. Emulator and full link remain unverified.')
