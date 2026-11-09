#!/usr/bin/env python3
"""Structural checks for the isolated pre-title prototype and preserved boot setup."""
import json,struct,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2]
subprocess.run(['python3',str(R/'crossroads/tools/build_black_ledger_intro.py'),'--check'],check=True)
src=(R/'src/black_ledger_intro.c').read_text();boot=(R/'src/intro.c').read_text();meta=json.loads((R/'graphics/intro/black_ledger/metadata.json').read_text())
for token in ['VOIDSTAR','INTERACTIVE','PRESENTS','OLIVINE CITY','JOHTO','POKéMON','BLACK LEDGER','A / START: SKIP']:
 assert token in src,token
for forbidden in ['SetVar(','FlagSet(','givemon','PlayBGM(','m4aSoundMode(','CB2_NewGame','Birch','Brendan','May']:
 assert forbidden not in src,forbidden
assert 'JOY_NEW(A_BUTTON | B_BUTTON | START_BUTTON)' in src
assert 'FreeAllWindowBuffers();' in src
assert 'SetMainCallback2(CB2_InitBlackLedgerTitleScreen);' in src
assert 'ResetPaletteFadeControl();' in src,'Skipping an active fade must not be ignored'
start=boot.index('void CB2_InitCopyrightScreenAfterBootup(void)')
custom=boot[start:boot.index('    if (!SetUpCopyrightScreen())',start)]
for command in ['SetSaveBlocksPointers(GetSaveBlocksPointersBaseOffset());','ResetMenuAndMonGlobals();','Save_ResetSaveCounters();','LoadGameSave(SAVE_NORMAL);','Sav2_ClearSetDefault();','SetPokemonCryStereo(gSaveBlock2Ptr->optionsSound);','InitHeap(gHeap, HEAP_SIZE);']:
 assert command in custom,command
assert 'if (!IS_FRLG)' in custom
assert custom.index('LoadGameSave')<custom.index('CB2_InitBlackLedgerIntro')
assert meta['visible_source_y']==[70,138]
mapdata=(R/'graphics/intro/black_ledger/tilemap.bin').read_bytes();tiles=(R/'graphics/intro/black_ledger/tiles.bin').read_bytes()
assert len(tiles)==600*32 and len(mapdata)==2048
assert max(v&1023 for v in struct.unpack('<1024H',mapdata))==599
assert 32768+601*32<30*2048,'Window glyphs must not overlap either tilemap'
print('Pre-title branding, skip/fade cleanup, preserved save initialization and isolated assets: PASS')
