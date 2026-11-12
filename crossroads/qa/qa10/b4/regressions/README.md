# QA10 B4 accepted-function regression evidence

Source `df8c4598d88c7770626be4621a5f39cf60dadb95`; frozen B4 checkpoint ROM
`4fb28fe64fc44c0546462a935655346a61f13b644bc3040468146d136cd6d656`.

All eight fresh serial stages exited0. These are fresh final B4 runs, with no B3 result relabelled. [Exact results](results.json) and the
[file hashes](evidence-manifest.json) identify the tested B4 bytes.

- Actual cold title and pre-title, title pixels/lighting/audio pointer, Start,
  New Game handoff and real soft reset passed. The existing New Game opening is
  preserved, not presented as a newly completed prologue.
- All three starter rescues, Olivine met origin/level, duplicate prevention,
  16 city facade returns and Joe directional walking passed. The test now uses
  the actual north port approach instead of the obsolete southern body tile.
- Actual Jasmine first loss/local healing passed; the [battle frame](first-loss/joe-battle-back.png)
  and hardware OBJ VRAM/palette identify Joe's actual trainer-back artwork.
- Fly to all ten existing QA destinations, cancellation, Joe's field pose and
  normal postflight Save/cold Continue/party-position integrity passed.
- Joe Mach/Acro Bike/wheelie, all four Surf directions, rod casting/return and
  disembark passed with actual graphics IDs and VRAM checks.
- Equal32-frame road trials moved2 tiles walking and3 running, both with Joe's
  authored frames. Native recordings are in `running/`.
- All51 accepted service checks passed: heal, PC, actual purchase, home rest,
  six staff counter fronts, canonical homes/Cafe/signs, Silph/Harbor/neighbor,
  lighthouse fixtures/plaque components, port/quay messages and Jasmine loss.

Battery-backed tests use copied historical batteries; starter/first-loss tests use disclosed fresh-game initialization. The original and lane input copy
remain hash-identical. Fresh-game, HP/status, temporary gear and encounter
suppression fixtures are disclosed; no map/player-coordinate writes replace
movement. No private battery, state, ROM or memory dump is public here.

Independent read-only review inspected all 116 fresh B4 PNGs: 3 title,
4 pre-title, 24 starters, 7 battle/standing, 13 Fly, 8 Joe field actions,
2 running and 55 services. No new visible corruption or inconsistent Joe artwork
was observed in those views. The lighthouse6F central housing is visibly cyan;
unchanged perimeter glass remains subject to owner visual assessment.

Bike state/VRAM
checks do not establish a convincing mounted/wheelie artwork pose: those authored
assets remain an existing art limitation. The inherited New Game introduction
remains deferred. Inactive field states and unused story Joe NPC scenes remain
explicitly unplayed. This is automated
controller gameplay, not the owner's Delta/visual acceptance.
