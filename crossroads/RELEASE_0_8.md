# Black Ledger western area 0.8 — Delta QA candidate

Scope: Olivine, Route 39, Route 38 and Ecruteak. No additional cities or routes.
This is the current-area completion candidate, not the finished Johto region or
story. Source commit and ROM SHA-256 are recorded in the bundled build-info.json.

## Implemented

- Recognizable lighthouse exterior, six climbable floors and lantern observation.
- Nine Bell Tower floors and bell interaction; Burned Tower basement and memorial.
- Distinctive landmark exteriors, theater stage and repeatable dance performance.
- Route 39 farmhouse, barn, Miltank and working Moomoo Milk shop (600 each).
- Route 39 Sentret/Hoothoot/Mareep/rare Miltank, levels 4–7; Route 38
  Meowth/Farfetch’d/Magnemite/Hoothoot, levels 5–9. Clear roads avoid tall grass.
- Two optional route trainers, Gym students and repeatable Jasmine/Morty practice
  battles. No badge awards, mandatory battle gates or permanent story restrictions.
- New leader trainer/overworld art and isolated city/interior tilesets. Existing
  Joe, title, summary UI, starter case, met data and saved starter choice preserved.
- Continue refreshes changed map tiles/NPC templates. Saves on newly blocked tiles
  move to a nearby clear tile. Existing valid positions and Pokémon data remain.
- A first loss before visiting any Center now returns to Olivine Center; genuine
  existing Center respawns remain unchanged. Save structures/flag offsets unchanged.

## Verification

BUILD PASS: Emerald, ARM GCC 14.2.1, 32 MiB padded ROM. Structural/regression and
layout reproducibility checks pass. mGBA controller tours cover both saved genders,
all starter rescue branches/duplicate guards, services, connected route returns,
every tower floor, farm, Gym halls and repeatable theater performance. A fresh
player's actual battle loss returns to Olivine and heals correctly.

Seven optional battle flows (six opponents plus leader rematch) were checked with
a RAM-only boosted starter fixture. This verifies battle entry/return and unchanged
badge flags, not normal-team balance. Live route encounters, a normal Poké Ball
catch with Route 39 met data, and an actual milk purchase were separately checked.
Earlier 0.7 save recovery was tested on newly occupied farm ground without changing
the saved starter's 100 bytes. See TESTING.md for final save-check coverage.

MANUAL QA PENDING: owner Delta testing of this candidate. Prior owner PASS applies
to 0.6 and earlier checkpoints, not automatically to 0.8.

## Delta checklist

Back up your existing .sav first. Import this .gba and use Continue with a copy of
your battery save; old emulator save states belong to their original ROM.

1. Continue: check Joe, party, starter choice, money and bag; walk both directions
   Olivine → Route 39 → Route 38 → Ecruteak and back. Enter every building.
2. Climb all six lighthouse floors and nine Bell Tower floors. Interact at the
   top, save normally, close/reopen and Continue; descend without getting trapped.
3. Visit Burned Tower basement, read the memorial, return; watch the theater dance
   twice and confirm actors return to their places and Joe can leave.
4. Visit the farm/barn and both Miltank. Buy one milk: 600 deducted, one item added.
5. Walk grass on both routes; check approved species/level bands. Catch a Pokémon,
   confirm route met location, then save/reload. Roads should remain safe to walk.
6. Decline each optional trainer/Gym offer, then accept. Try Jasmine, Morty and
   their students; rematch a leader. Confirm no badge is granted and Joe returns.
   Report normal-level difficulty separately for Elgyem, Seedot and Trubbish.
7. On a disposable fresh save, lose a battle before using a Center. Confirm an
   Olivine Center return with healed party. Later visit Ecruteak Center and verify
   a loss uses that registered Center instead.
8. Recheck original Silph starter rescue/duplicate prevention, home rest, offices,
   signs, healing, Mart, summary, title/Continue and save/reload.

## Deferred / known limitations

Permanent Gym badges/progression, legendary/story tower events and additional
regional exits are deliberately deferred. The original Emerald introductory
sequence and Joe's special movement graphics remain; ordinary Joe walking and
accepted Black Ledger harbor title are preserved. No claim of full prologue or
full Joe graphics completion. Architecture/leader art is new and needs visual QA.
No known crash or traversal blocker remains in the checked current-area flows.
