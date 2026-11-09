# Black Ledger title music

Owner-supplied source: Black_Ledger_Title_Demo_v5.mp3 (attached 2026-11-09).
Original file preserved; source/sample SHA-256 and conversion parameters are in
title-music.json. Provisionally repeats the full 80-second track; precise musical
loop points remain open to owner feedback. No arrangement or new composition.

The existing m4a engine plays one sustained direct-sound voice: signed 8-bit mono,
16 kHz source, standard mixer/resampling. No MP3 decoder, engine replacement or
new RAM audio buffer. PCM adds 1,280,000 sample bytes to ROM. Native GBA playback
has lower fidelity than the stereo MP3. The sample's 20 ms edge ramps reduce clicks
at the provisional loop. Start uses the existing BGM fade and reset restarts it.
Old song IDs, stock instruments and save structures are unchanged; new ID is 610.

Regenerate with ffmpeg installed: python3 crossroads/tools/build_title_music.py.
Normal builds consume the committed native PCM and need no ffmpeg. Validate with
validate_title_music.py. Optional mGBA audio test: compile mgba_bridge.c as a shared
library with libmgba-dev and run title_music_smoke.py --library /path/to/bridge.so.
The test captures actual emulator audio, checks non-silence/clipping and verifies
sample progression across a full loop and Start/reset behavior. Listening quality
and final loop choice require owner Delta QA.
