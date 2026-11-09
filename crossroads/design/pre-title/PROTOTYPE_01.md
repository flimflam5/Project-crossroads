# Black Ledger pre-title prototype 1

Requested replacement: the inherited Emerald Game Freak/bicycle/Pokémon movie
before the title. This is a boot presentation, **not** the New Game story prologue.
No new robbery dialogue, named relationships, factions or story flags are added.
Appearance and pacing remain a prototype for the owner's review.

## Storyboard

1. **Voidstar Interactive presents.** Quiet navy background, native GBA white
   wordmark, muted teal secondary text and a restrained burgundy divider. Hold
   about two seconds after the fade. No claim of a finalized illustrated logo.
2. **Olivine City / Johto.** A cinematic strip of the existing accepted harbor
   composition, including corporate port buildings and the lighthouse. The full
   source is format-converted to an isolated 4bpp palette; a hardware window
   displays only source rows 70–137, excluding title lettering and Press Start.
   A small palette-only harbor light pulse gives the otherwise still scene life.
   Hold about three and a half seconds.
3. **Pokémon / Black Ledger.** A clean native title card and short pause, then
   fade into the existing accepted harbor title. Custom title music starts there.

A, B or Start skips any card or fade. Holding the skip key through the handoff
must not also trigger the title's main-menu action; release and press Start again.
Normal fades plus holds total roughly eight seconds. No new intro music is added
while the title recording's separate audio refinement is being verified.

## Implementation

- `src/black_ledger_intro.c` owns the isolated BG/window/card state machine.
- `src/intro.c` selects it only for Emerald, retaining the original boot save
  pointer/default/options/heap setup before entering the new presentation.
- Original inherited intro functions/assets and FRLG paths remain available.
- `build_black_ledger_intro.py --check` reproduces the accepted-art conversion.
- `validate_black_ledger_intro.py` checks branding, boot setup and VRAM isolation.
- `pre_title_smoke.py` checks normal cold boot, all three card captures, nine
  controller skip cases, early-fade skip, held-key behavior and a real reset.

BG1 character data occupies bytes 0–19,199. BG0 window glyphs start in character
block 2 and end before screen blocks 30/31; palettes 0 and 1 are independent. The
window buffers are freed before handing off to the existing title. No music mode,
Pokémon data, save fields or story progress is written by the presentation.

## Owner review checklist

Cold boot: confirm the new branded cards replace the Emerald movie, read clearly
and look appropriate for Black Ledger. Watch the full sequence, skip each part,
hold Start during a skip and then press it fresh on the title. Reset while the
movie is running. Continue your existing save and confirm location/party intact.
The original Birch New Game presentation is a separate unfinished project task.

## Verification performed for the combined 0.8.3 candidate

Emerald compilation passed. Actual mGBA cold boot displayed all three cards in
order, verified isolated character data and text glyphs in VRAM, and entered the
existing title with its custom music starting only at the title. All nine A/B/
Start skip cases across the three cards passed, including holding the input
through handoff and then pressing Start fresh. Initial-fade skip and the real
A+B+Start+Select reset chord also passed. Native screenshots were inspected.

The existing title visual/New Game handoff test and 96-second music continuity
check passed on the same combined binary. Owner appearance/pacing QA remains
pending. The New Game Birch story introduction is unchanged and not claimed fixed.

Screenshots: ignored build/black-ledger-boot-083/scene-0.png, scene-1.png,
scene-2.png and title-handoff.png. The prototype adds no new illustration or
illustrated Voidstar logo; it is a native text-and-harbor presentation for review.
