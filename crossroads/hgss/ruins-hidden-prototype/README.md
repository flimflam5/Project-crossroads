# Ruins hidden-room trigger prototype (not linked to the game)

This is a source-level prototype, not an implementation or a playable feature.
No production map, game source, save or persistent flag is changed. Compile and
run its local fixture with `cc -std=c99 -Wall -Wextra -Werror crossroads/hgss/ruins-hidden-prototype/test_trigger.c -o /tmp/alph-trigger-test && /tmp/alph-trigger-test`.

## Reference and adaptation

The pinned HGSS source is pret/pokeheartgold revision
`6bf138d6035aa6b43d6f8f4132a12df70f86dcec`. `src/alph_checks.c` checks
southwest first room, `(6,3)` and north; `src/field_use_item.c` queues the
water-stone reaction and returns without taking the item; script
`0043_D24R0206` sets a persistent opening flag. This project's 10x11 chamber
crop has a proposed wall at `(5,1)`, hence `(5,2)` north is the corresponding
standing coordinate. The wall geometry and accessible path still need to be
implemented and verified by movement; this is not established from a playtest.

Script `0045_D24R0208` runs the Ho-Oh condition after inspecting the wall and
sets a separate persistent open flag. `src/scrcmd_party.c` excludes eggs when
checking party species; it does not reject fainted Pokémon. The engine's generic
`CheckPartyHasSpecies` does not filter eggs, so a future caller must use an
explicit per-slot egg check. Both checks are distinct from the picture puzzles.
No Ho-Oh, stone, rewards or story events are granted here.

## Integration blockers

The hidden walls, second rooms, drops and return routes do not exist in the
candidate. Hook the water-stone branch at `ItemUseOutOfBattle_EvolutionStone`
only after ensuring ordinary evolution-stone use on other maps/positions remains
unchanged; use the game's field callback and scripts to render a real opening.
The Ho-Oh wall interaction must check the actual party, not boxes or Pokédex.
Verify both paths, reopening, save/Continue, entrances, exits and floor drops in
the delivery emulator before claiming the feature.

HGSS openings persist. Two candidate Emerald system flag bits, `0x8FE` and
`0x8FF`, appear unused in the current source and were clear in 12 supplied QA
fixture copies, but that does not establish safety across every old save or all
historical engine configurations. In particular FRLG compatibility aliases for
the same `FLAG_UNUSED` names are zero. No slots are allocated here. Establish a
verified migration and flag-allocation proof before linking persistent state; do not add save fields, reuse unknown bits, or expose a fake opened door.
