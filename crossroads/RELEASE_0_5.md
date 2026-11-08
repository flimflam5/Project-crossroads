# Pokémon: Black Ledger 0.5 — harbor title and Route 39 checkpoint

Uses the original approved nighttime Olivine harbor composition with the updated
**Pokémon: Black Ledger** title. The subsequently supplied coat/pagoda/book artwork
is not used. Native 240×160 GBA rendering replaces the Emerald title branding.
A gentle palette pulse animates harbor lighting. Start/A open the existing main
menu; existing clear-save/RTC/Berry Fix shortcuts remain routed to their existing
screens. Never test the clear-save shortcut on your only save copy.

Includes the owner-tested Joe 0.3 baseline and the connected Route 39 exploration
blockout from 0.4. The Pokémon summary UI and save format remain unchanged.

## Verification

BUILD PASS: Emerald linked ROM 26,813,772 bytes, EWRAM 226,424, IWRAM 28,392.
Automated asset, script, map, starter and reproducible layout checks passed.
The title smoke runner passed real cold boot, exact native BG VRAM, lighting
animation, Start, New Game handoff and A+B+Start+Select soft reset. Emulator
screenshots confirm the harbor art and Black Ledger title render correctly.

Normal Continue loaded a pre-integration Seedot fixture with Joe visible and all
100 Pokémon bytes preserved. A normal in-game Route 39 save was cloned as SRAM,
loaded by a fresh emulator core through the title and Continue, and preserved
position (12,27), starter choice and all 100 Pokémon bytes. The player returned
south to Olivine on foot. The Joe/city/starter/healing regression runner passed
on the title-code build; both saved genders passed the preceding Route 39 build.
These are development fixtures, not the owner's private Delta save.

## Delta QA

1. Back up your existing save and import this ROM. Confirm the **harbor** artwork
   and **Black Ledger** title, readable text, stable lighting and sensible audio.
2. Press Start. Continue your existing save. Check Joe, your party, items, starter
   and recorded met location. Old partners must retain their previous origin.
3. Walk north from Olivine's central road onto Route 39. Explore to its closed
   northern boundary, read signs, speak to the pedestrian, and return south.
4. Save on Route 39, close/reopen Delta, Continue and return to Olivine. Repeat
   the save/reload on the city side. Recheck doors, Center, Mart and interactions.
5. On a separate save only, check New Game handoff. It still enters the original
   Birch introduction; the replacement story opening is a later increment.
6. Test soft reset using your emulator controls. Confirm the harbor title returns
   and Continue still loads your saved progress. Report wrong art, flicker or hangs.

## Unfinished

Owner Delta QA PASS for the delivered 0.5 build: “Everything works as expected.”
This accepts the tested checkpoint, including Route 39, without completing future
content or inferring additional results for unreported tests.
Original Birch/Hoenn introduction remains. Title music temporarily reuses the
existing Abandoned Ship engine track; no original score is claimed. Clear-save,
RTC and Berry Fix shortcut behavior was preserved in source but not newly exercised.
No original audio listening/hardware test was performed. Route 38/Ecruteak, route
encounters/trainers/farm interiors and the remaining Johto region are unfinished.
Lighthouse/Gym/interior placeholders and Joe special-state art remain. No claim
that Release 1, the opening sequence or the full region is complete.
