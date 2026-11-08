# Black Ledger 0.7 — existing-area detail pass 1

The owner accepted 0.6 and paused new cities/routes until the current area is
fleshed out. This is the first detail increment, not completion of that larger
assignment. The footprint remains Olivine, Routes 39/38 and Ecruteak.

## Changes in this build

- Silph office: dedicated corporate layout, computer desks, visible digital staff
  notice, freight checklist and terminal records. The starter case remains at
  (4,4); the employee and both exits retain their accepted coordinates.
- Harbor office: dedicated reception/dispatch layout with readable freight ledger
  and dispatch terminal. Existing clerk and travel restrictions remain intact.
- Joe's home: interact with the bed to decline or accept a short rest. Accepting
  uses the engine's party heal; it does not advance story flags, change the saved
  starter, grant items/Pokémon, force a save or overwrite the last Center respawn.
  The interaction also works before a starter is acquired. Books and the existing
  home notes are readable; the Alpha return remains available.

Office rooms stay 10×8 with unchanged map IDs and door coordinates; dedicated
layout IDs append. Existing valid save coordinates have a path out even where
new furniture replaces previously walkable tiles. Existing Pokémon origins,
summary UI, approved harbor title and Joe graphics remain unchanged.

## Verification

BUILD PASS: Emerald linked ROM 26,826,348 bytes; EWRAM 226,424; IWRAM 28,392.
Source/asset/map inclusion, cross-map reachability and layout reproduction checks
passed. New office checks cover interaction access, south-arrow exit behavior,
unchanged starter coordinates and escape paths from previously walkable positions.
Both saved player genders passed the final mGBA regression suite, including all
three starter choices/met-location/duplicate guards, the Olivine/39/38/Ecruteak
round trip, all existing city doors and Center healing. Added checks passed for
empty-party rest, decline without healing, HP/poison recovery on acceptance,
unchanged starter/Center respawn, and home/office/harbor record interactions.
These use debugger-assisted initial fixtures and real controller movement/events.

Normal UI/SRAM checks passed separately: a 0.6 Route 38 save loaded through the
title and Continue with position, choice and all 100 Pokémon bytes unchanged.
A new save inside the remodeled Silph office reloaded in a fresh emulator core
with position/choice/Pokémon data intact, then exited normally with Joe visible.
These are development fixtures, not the owner's private Delta save. Harbor/home
SRAM reload and audio listening remain owner QA; they were not separately claimed
as tested here.

## Delta checklist — manual QA pending for 0.7

1. Back up your accepted 0.6 save, then Continue with this build. Inspect your
   party, inventory, saved starter and origin metadata.
2. Visit the Silph office. Inspect the desks and staff computer; read the terminal,
   notice and freight checklist. Speak to the employee and enter/leave normally.
3. On an already chosen save, interact with the rescue case and confirm no second
   starter. On separate unchosen saves, recheck each starter and its Olivine origin.
4. Visit the harbor office. Read the ledger and dispatch screen, speak to the
   clerk, and check both normal door exits. External passenger travel stays closed.
5. At Joe's bed, decline rest with an injured party and confirm HP does not change.
   Accept rest and confirm HP/status recovery, normal controls and menu behavior.
   Read the books and home notes; the Alpha return should still work.
6. Save and fully close/reopen Delta inside each remodeled office and at home.
   Continue, check position/party/items, and leave the building normally. Recheck
   the Olivine/39/38/Ecruteak round trip and both Centers.

## Remaining completion work

This does not finish Olivine or Ecruteak. The lighthouse, tower/Gym/theater
progression, farm/route content, encounters/trainers, distinctive exterior art and
more developed neighborhoods remain on AREA_COMPLETION.md. Major roster, Gym and
story decisions remain for creative review. Original Birch introduction and Joe
special movement artwork remain unfinished. No new city or route was added.

## Primary changed files

- data/maps/OlivineCity_SilphOffice/map.json
- data/maps/OlivineCity_HarborOffice/map.json
- data/maps/OlivineCity_Residence/map.json
- data/layouts/OlivineSilphOffice and OlivineHarborOffice plus layouts.json
- crossroads/scripts/olivine_interiors.inc and olivine.inc
- crossroads/tools/build_olivine_interiors.py, validate_olivine_interiors.py,
  olivine_detail_smoke.py and the existing regression runner/validators
- AGENTS.md, AREA_COMPLETION.md, ROADMAP.md, status/build/CI documentation
