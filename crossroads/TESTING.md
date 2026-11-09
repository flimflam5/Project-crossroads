# Visual/collision QA — repair pass0.9.1

Owner reports0.9 network works but has NOT passed visual/collision QA. Expansion
is paused. The first repair pass covers Ecruteak exterior, Mahogany town/workshop,
Routes38/39 and shared ground-layer fixes also affecting Olivine. This is not a
region-wide polish claim. See RELEASE_0_9_1.md and qa/visual-0.9.1/manifest.json.
All other map visual reviews remain open; owner visual acceptance is pending.

---

# Current Johto QA —0.9

Use johto/DELTA_QA.md for iPhone itinerary and old-save precautions. validate_johto_network.py --built checks IDs, reciprocal topology, local access, services and actual Emerald inclusion. build_johto_network.py --through west --check checks deterministic generation. johto_network_smoke.py --all-edges performs actual controller traversal using copies of battery saves; no map/warp debugger writes. Test-only encounter suppression/HP fixtures are disclosed. Final tour112 new maps/622 transitions/141 roundtrip pairs PASS; five representative normal Save/Continue checks PASS. Owner gameplay acceptance remains pending.

---

# Olivine foundation 0.1 testing

## Verification status

Implemented on the feature branch. Structural checks cover the linked and staged
starter scripts, city registration, reciprocal exits, pedestrian access to every
doorway/interaction, object placement, reproducible layout and healing data.
These checks do not execute game scripts.

Compiled locally: baseline master d3ac7cf788 and the corrected city implementation
through d624211868, using ARM GCC 14.2.1. Latest city linked size: 26,762,616 bytes;
EWRAM 226,420 bytes; IWRAM 28,392 bytes. The padded .gba file is 32 MiB.

Emulator: mGBA 0.10.5, HLE BIOS, debugger-assisted initial setup. Actual tested
behavior: all seven entrance/return pairs, both piers on foot, live notebook rescue
of each intended level-5 species, repeated notebook interactions without duplication,
original post-rescue terminal travel with every choice preserved, and nurse healing
from 1 HP without corrupting menu fonts. The optional emulator_smoke.py runner
repeats these tests and saves screenshots in ignored build output.

Separately tested through the normal UI: one Potion purchase (money 3000 to 2800;
bag item 28, quantity 1), and actual Save followed by fresh-emulator normal Continue
outside and inside the Center. Those save/reload checks used Seedot and preserved
map/coordinates, one party member, starter value 2, healed HP and working menu text.
No raw emulator snapshot was used for those Continue checks.

Two runtime integration faults were found and fixed: the map target filter excluded
REGION_JOHTO maps from Emerald; and the Center lacked CableClub_OnResume, leaving
the Union Room name buffer uninitialized when the standard nurse used it. The
regression checks now cover both. Compilation alone had not detected either fault.

Still unverified: normal opening playthrough, actual SRAM reload for Elgyem/Trubbish,
saving in every other interior, PC deposit/withdraw, whiteout/Teleport recovery,
all NPC dialogue, full bags/boxes, prolonged battles and old owner-supplied saves.
Historical Alpha-v2 results remain owner-reported. The owner has now accepted
the tested exploration foundation on Delta/iPhone; detailed coverage is recorded
in STATUS.md. New increments still require their own owner QA.

## Owner checklist

Use a **backup copy** of an Alpha save or a fresh save. Existing Emerald new-game
setup is unchanged. Reach Brendan's upstairs Alpha room.

1. On independent fresh saves rescue Elgyem, Seedot and Trubbish. Confirm level 5
   and exactly one grant. Decline all three once, then choose.
2. Revisit the notebook repeatedly; save, close the emulator, reload and check
   again. Confirm the choice persists and no second Pokémon is granted.
3. Read the Silph terminal before/after rescue. Decline the new exploration prompt
   once, then accept. Confirm control returns on decline and city entry on accept.
4. Walk all streets and both piers. Read every sign and talk to every pedestrian.
   The woman west of the central street reacts to the rescued starter. Check the
   temporary Gym/lighthouse labels and look for invisible walls or sprite overlaps.
5. Enter/leave all seven buildings. Test both interior exit tiles. Check for wrong
   destinations, stuck doorways and missing collision.
6. Heal at the Center, use PC storage and buy/sell a cheap Mart item. Verify money,
   bag and party counts. Upstairs link-club stairs should be absent.
7. Save outside and inside each building. Restart and Continue. Check position,
   party, inventory and dialogue. Include a backed-up old Alpha save.
8. Return to Alpha via the employee in Joe's residence. Revisit the notebook and
   terminal; repeat travel, including before starter rescue.
9. After healing in Olivine, white out in an existing battle test area and verify
   recovery in Olivine's Center. Test Teleport if available. The city adds no battle.

Record source/ROM SHA, emulator/version, starter, starting save, steps and actual
result. Screenshots and a backed-up save help reproduce failures.

## Known limitations

- Temporary geography, house/office/Gym interiors and small beacon; no lighthouse
  tower. Existing music and child player sprite. No full Johto world map.
- Original Emerald introduction and unrelated Hoenn story remain.
- Starter rescue remains in Alpha; final opening-story integration comes later.
  City travel is an explicit testing convenience, not a story scene.
- No new encounters, trainer battles, Gym challenge, external routes, ship travel,
  robbery, difficulty selection or quest system. Existing content is preserved.
- Historical Alpha-v2 gameplay tests are not automatically verified by these checks.


# Western area 0.8 final candidate

Emerald compiled successfully after the room-border polish. All 13 linked-source,
graphics, layout reproducibility, map registration and mapjson timestamp checks
passed. Final-ROM mGBA tour passed all starter branches and duplicate guards,
Olivine/39/38/Ecruteak borders, services, home rest, every lighthouse/Bell Tower
floor, Burned basement, farm/barn, both arenas and repeatable dance performance.

Actual normal menu Save followed by fresh-core battery-save Continue passed at
lighthouse floor 6 and Bell Tower floor 9: exact map/coordinates, starter choice
and all 100 party Pokémon bytes preserved. No snapshot was loaded for Continue.
An archived 0.7 battery save on newly blocked farm ground (4,16) loaded at nearby
clear ground (4,14), retained the starter byte-for-byte and could walk afterward.
A first battle loss before visiting a Center returned to Olivine and healed.

Optional battle-flow tests use a boosted, internally consistent level-50 starter
in RAM, not in the shipped ROM. They cover all six new trainers and a Jasmine
rematch, return control/Joe and unchanged badge flags. Normal-level balance needs
owner QA. Live encounters, Poké Ball catch with correct met data and the milk
shop's 600-price transaction were checked separately before cosmetic border polish.

Repeat the runtime tour with emulator_smoke.py (libmgba-dev + ARM nm), passing
--gender 0 or 1. Exact-ROM output includes area-ready.snapshot and
elgyem-field.snapshot, guarded by ROM SHA checks. Use --area-resume or
--battle-resume plus the matching --gender to repeat those portions.
--first-loss-only checks the uninitialized-respawn fallback. Runtime screenshots
and local logs are ignored build outputs, never committed owner saves.

Owner Delta QA remains pending. See RELEASE_0_8.md for the playtest checklist.
Original introduction, Joe special movements, long-term balance, complete prologue,
all later regions and permanent badge/story progression are not verified here.
