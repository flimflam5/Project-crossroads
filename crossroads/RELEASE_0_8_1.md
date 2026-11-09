# Black Ledger 0.8.1 — custom title music QA

Adds the owner-supplied Black_Ledger_Title_Demo_v5.mp3 to the existing accepted
nighttime harbor title. No artwork, maps, encounters, trainers, starter logic,
summary UI, story flags or save layout changes. This preserves the 0.8 area QA
candidate; owner acceptance of that area is still pending.

The full 80-second recording plays through a dedicated existing-engine sound
voice, converted to signed 8-bit mono at 16 kHz. Adds 1,280,000 sample bytes.
GBA playback has lower fidelity than the original stereo MP3. Full-track looping
is provisional, with 20 ms edge ramps to reduce clicks; final musical loop points
can be adjusted from owner feedback. Original MP3 and conversion provenance kept.

## Verified

- BUILD PASS: Emerald; linked ROM 28,155,648 bytes, padded output 32 MiB.
- Static audio source/hash, sample limits, appended song ID 610 and actual title
  wiring checks passed; existing song IDs and instruments are unchanged.
- mGBA cold boot: actual music header/sample selected; non-silent audio capture
  with no digital clipping, 96 seconds continued playback and observed sample
  pointer wrapping inside bounds. Start stops/fades sample and opens menu; real
  soft reset restarts the custom music.
- Existing title VRAM, lighting, Start and New Game handoff regression passed.
- Actual 0.8 Bell Tower summit battery save loaded through the music title using
  normal Continue in a fresh core. Position, starter choice and all 100 party
  Pokémon bytes matched. No raw snapshot was used for that Continue check.
- Existing area, starter and Joe structural checks passed. No new full-area tour
  is claimed for this audio-only change; see 0.8 QA documentation.

## Delta QA

Back up your battery save. Extract the supplied ZIP and import the new .gba.
Use your battery save with the new ROM; emulator save states remain ROM-specific.

1. Cold boot and listen to the title. Check volume, pitch, distortion and whether
   the mono GBA conversion retains the intended feel.
2. Stay at the title for at least two minutes. Listen across the full-track
   repeat; report preferred loop timestamps if the transition needs adjustment.
3. Press Start partway through music. Confirm a clean fade, readable main menu
   and normal Continue into your existing saved location with party intact.
4. Reset and confirm music begins again. Test New Game only with a disposable
   save or after backing up your main save.
5. Continue the 0.8 city/route/landmark checklist; this audio increment does not
   automatically accept any untested 0.8 content.

MANUAL AUDIO QUALITY/LOOP QA PENDING. Original Birch introduction, Joe special
movement art, badges and later regional/story work remain deferred as before.
