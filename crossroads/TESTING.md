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
Historical Alpha-v2 results remain owner-reported. Owner playtesting and acceptance
are pending. See the checklist below.

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
