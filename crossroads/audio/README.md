# Black Ledger title music

Owner-supplied source: Black_Ledger_Title_Demo_v5.mp3, preserved unchanged.
Source/sample SHA-256 and conversion parameters are in title-music.json. Owner
accepted the music and full 80-second loop in 0.8.1, but reported static.

0.8.2 listening candidate: signed 8-bit mono at 31,536 Hz, fixed-rate direct-sound
voice in the existing m4a engine. The title temporarily selects the matching
31.5 kHz mixer, 9-bit DAC mode and master volume 15. Normal song volume uses the
full 127 range. The previous 16 kHz sample played through the normal 13.4 kHz
mixer; eliminating that rate mismatch avoids a second resampling/aliasing stage.
Higher output precision and less internal attenuation address other possible
noise contributors. This is not proof that all owner-reported static is resolved.

The previous mixer frequency, DAC mode and master volume are captured on entry
and restored on every title exit after stopping its sample. No global audio
settings, mixer code, save layout, old song IDs or stock instruments are replaced.
Native sample is 2,522,880 bytes. No new RAM audio buffer or MP3 decoder. The
20 ms edge ramps and accepted full-track repeat are retained. Listening QA remains.

Regenerate with ffmpeg installed: python3 crossroads/tools/build_title_music.py.
Normal builds consume the committed native PCM and need no ffmpeg. Validate with
validate_title_music.py. Optional mGBA check: compile mgba_bridge.c as a shared
library with libmgba-dev and run title_music_smoke.py --library /path/to/bridge.so.
The test captures emulator audio, checks non-silence/clipping, actual sample wrap,
Start/reset and restoration of the normal mixer/DAC before the main menu.
