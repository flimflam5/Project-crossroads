# Title recording refinement after 0.8.2 listening QA

Owner accepted 0.8 and 0.8.1 gameplay/music loop, reporting static. 0.8.2 sounded
“a bit better” but owner reported skips at places and remaining static; audio
quality was not accepted. Continue investigating; no new audio QA PASS inferred.

## Verified additional cause and change

The inherited Emerald movie left gSoundInfo.reverb = 50. Song header reverb 0
means do not override the effect, rather than explicitly disable it. Both prior
recording integrations therefore applied reverb to an already mixed recording.
The title now explicitly clears reverb with SOUND_MODE_REVERB_SET and captures
its prior value alongside mixer frequency, master level and DAC settings for
restoration before every title destination. No global mixer or save changes.

Audio-only candidate compiled before the new pre-title source was linked.
Actual mGBA cold boot, 96 seconds of playback/full loop, Start/fade, normal audio
restoration and reset checks passed. The strengthened check inspects all 5,760
individual frame advances: each moved by exactly 528 source samples, including
wrap, with no skipped/repeated sample blocks. Separate 0.8.2 audit also found
6,000 exact advances, so the reported skips were not reproduced as source-pointer
jumps in mGBA. Do not equate that with absence of audible skips in Delta.

A three-second actual emulator output segment, aligned against the original MP3
at about 17 seconds, matched the source more closely after clearing reverb:
correlation 0.952 (0.8.1) to 0.989 (dry candidate); gain-normalized waveform error
SNR 9.84 to 16.62 dB. This is limited waveform evidence, not a whole-track noise
score or owner listening acceptance. Native 8-bit GBA conversion still has finite
resolution; subjective static and device-specific playback remain for Delta QA.

Final combined boot/audio build requires new runtime checks after linking the
pre-title prototype. See its release notes for final commit, artifact and QA.
