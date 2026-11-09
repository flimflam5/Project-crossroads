# Black Ledger 0.8.3 — boot prototype and dry title-audio QA

Two independently developed increments: inherited title-audio effect correction,
and a Black Ledger pre-title presentation replacing the Emerald/Game Freak movie.
Owner accepted 0.8/0.8.1 content and looping; 0.8.2 sounded somewhat better but
still had reported static and skips. Neither new visual appearance nor final
sound quality is owner accepted yet. No new map/story/prologue changes.

## Audio

Title now explicitly disables an inherited reverb=50 effect. A song header value
of zero had left this effect active on the already mixed MP3 recording. Prior
reverb is captured/restored alongside frequency, master level and DAC settings
before all title destinations. Source MP3, accepted full 80-second loop and the
31.5 kHz native recording remain unchanged. See AUDIO_REFINEMENT.md for limited
source-comparison evidence and what remains unverified on Delta.

## Pre-title prototype

A roughly nine-second skippable presentation: VOIDSTAR INTERACTIVE PRESENTS,
OLIVINE CITY / JOHTO with the accepted nighttime harbor artwork and subtle light
pulse, then POKéMON / BLACK LEDGER before the existing title screen. A, B or Start
skips from any card; holding the skip button does not accidentally enter the menu.
The boot prototype is intentionally silent; custom title music begins on the
actual title. The existing New Game/Birch introduction is separate and unchanged.
No new characters, plot scenes or approved story canon are invented. Original
Emerald movie assets remain in source for other uses; Emerald boot bypasses them.
Normal save/heap initialization and FRLG path remain intact.

## Verified

- Emerald BUILD PASS; linked ROM 29,250,240 bytes, padded to 32 MiB.
- Native-art conversion/reproducibility, VRAM/palette isolation, branding and boot
  save-initialization structural checks pass.
- Cold boot renders all three cards and automatically reaches the accepted title.
  Screenshots inspected. Actual harbor palette pulse, fonts/masking and no old
  title/Press Start pixels inside the harbor viewport were checked.
- All nine card/button skip cases (A/B/Start on each card), held-key behavior,
  skip during initial palette fade and actual reset back through the sequence pass.
- Actual mGBA title output non-silent/no digital clipping; full-loop playback and
  all 5,760 per-frame sample-pointer advances exact, without skipped/repeated
  source sample blocks. Start/fade, previous audio restoration and reset pass.
- Existing title VRAM/lighting, Start, main menu and New Game handoff pass.
- Actual 0.8 battery save loaded via normal Continue in a fresh emulator core
  through the new boot/title, retaining exact map/coordinates, saved starter
  choice and all 100 party Pokémon bytes. Normal mixer/DAC restored in gameplay.
- Existing starter/Joe/area structural checks pass. No fresh full city/battle tour
  is claimed for this boot/audio-only increment.

These establish tested playback/state behavior, not proof that the owner's
perceived static/skips are resolved. Device audio quality and appearance/pacing
still require owner Delta QA. No full Johto, new prologue, badges or new Joe special
movement art is claimed. No merge into master is authorized/performed.

## Delta checklist

Back up the battery save. Extract the ZIP and import Black Ledger 0.8.3.gba.
If Continue is missing, import your battery save into the new ROM in Delta;
old raw emulator save states belong to their original ROM.

1. Cold boot and watch the new branding/harbor/title cards. Confirm no Emerald
   movie/Game Freak scene appears. Review appearance, text, timing and silent
   pre-title pacing; this is a prototype for your review.
2. Skip from each card with A or Start. Hold the button through the transition:
   it should stop at the title. Release, then press Start again to enter the menu.
3. Listen at normal speed for two minutes (fast-forward off), preferably using
   the same headphones/phone volume as 0.8.2. Compare static, repeated hits and
   any skips, including the loop boundary. If one occurs, note approximate track
   seconds and whether it repeats at the same time on the next playback.
4. Start mid-track: confirm clean fade and Continue. Check party, location and
   ordinary map/battle music, then save/reload and reset back through the boot.
5. Existing 0.8 areas/encounters/battles retain their accepted state; report any
   newly observed regression. No regional expansion is included here.
