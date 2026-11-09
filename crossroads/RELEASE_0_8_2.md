# Black Ledger 0.8.2 — title-audio listening candidate

Owner accepted 0.8/0.8.1 gameplay, title music and looping, but reported static.
This audio-only candidate preserves the source track, full 80-second repeat,
artwork, world content, starter system, summary and save structures.

## Changed

The prior 16 kHz recording used the normal 13.4 kHz mixer. This version uses a
31,536 Hz sample with a matching title-only mixer and fixed-rate voice, avoiding
a second sample-rate conversion. Title uses 9-bit DAC output, full song volume
and master level 15 to reduce unnecessary attenuation. Normal frequency, DAC and
master level are restored before all title destinations. Sample adds about
1.24 MB over 0.8.1; linked ROM is 29,398,600 bytes (32 MiB padded). No engine
replacement, new RAM audio buffers, original MP3 edits or gameplay changes.

## Verified

Emerald BUILD PASS. Source/sample hash and format checks pass. Actual mGBA audio
output is non-silent and not digitally clipped; 96-second playback crosses the
full sample loop with its pointer in bounds. Start stops/fades the sample and
restores 13.4 kHz, 8-bit DAC and master 12. Reset restarts custom music. Title
VRAM, lighting, main menu and New Game handoff regressions pass. Normal Continue
from an actual 0.8 battery save preserves position, starter choice and all 100
party Pokémon bytes, with normal audio settings restored in the field.

These checks establish playback and state safety, not a subjective static fix.
Owner listening QA is pending. Frequency/render differences make simple waveform
comparison insufficient to claim the reported noise is eliminated.

## Delta comparison

Back up your battery save. Extract the ZIP and import Black Ledger 0.8.2.gba.
If Continue is absent, import your backed-up battery save into the new ROM in
Delta; do not load an old ROM's emulator save state. Keep 0.8.1 for comparison.

1. Listen at normal speed, using the same phone/headphone volume as 0.8.1.
   Compare the opening, quiet passages and louder percussion. Is the static
   reduced, unchanged or worse? The track may sound louder in this version.
2. Remain at the title at least two minutes. Verify the accepted loop remains
   intact and no crackle occurs specifically at the repeat.
3. Press Start mid-track; confirm a clean fade, Continue, correct party/location
   and normal map/battle audio. Reset and verify music restarts normally.

Original introduction, Joe special movement art, badges and further regional/story
work retain their prior status. This increment does not add cities or routes.
