# Olivine foundation 0.1 testing

## Verification status

Implemented on the feature branch. Structural checks cover the linked and staged
starter scripts, city registration, reciprocal exits, pedestrian access to every
doorway/interaction, object placement, reproducible layout and healing data.
These checks do not execute game scripts.

Compilation and emulator results will be updated after the corresponding checks.
Owner playtesting: pending. Owner acceptance: pending.

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
