#!/usr/bin/env python3
"""Check title song wiring, immutable old IDs, audio bounds and provenance."""
import hashlib,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[2]
m=json.loads((R/'crossroads/audio/title-music.json').read_text())
p=(R/'sound/direct_sound_samples/crossroads/black_ledger_title.pcm').read_bytes()
assert len(p)==m['samples']==1280000 and m['sample_rate']==16000
assert hashlib.sha256(p).hexdigest()==m['sample_sha256']
assert hashlib.sha256((R/'crossroads/audio'/m['source']).read_bytes()).hexdigest()==m['source_sha256']
assert p[0]==p[-1]==0 and len(set(p))>128
songs=re.findall(r'^\s*song\s+(\w+),',(R/'sound/song_table.inc').read_text(),re.M)
assert len(songs)==611 and songs[609]=='ph_nurse_solo' and songs[610]=='mus_black_ledger_title'
assert 'PlayBGM(MUS_BLACK_LEDGER_TITLE);' in (R/'src/black_ledger_title.c').read_text()
assert '#define MUS_BLACK_LEDGER_TITLE        610' in (R/'include/constants/songs.h').read_text()
print('Title music source/hash, PCM limits, appended song ID and actual title wiring: PASS')
