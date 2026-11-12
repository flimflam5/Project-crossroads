# QA10 B5 accepted-function regression evidence

Source `cc643ffe711204f3ef38e34e7aa1eb8c9558720f`; frozen B5 checkpoint ROM
`ee2d81d5d0b55b7f1f9d36d1c9b055700164da439f51af7a66b5fb2d2147f90b`.

All eight fresh serial stages exited0. These are fresh final B5 runs, with no earlier checkpoint result relabelled. [Exact results](results.json) and the
[file hashes](evidence-manifest.json) identify the tested B5 bytes.

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

Independent read-only review inspected all 116 fresh B5 PNGs (3 title,
4 pre-title, 24 starters, 7 battle/standing, 13 Fly, 8 Joe field actions,
2 running and 55 services), plus the separately curated 9 B4/B5 native arrival
comparisons. No new visible corruption or inconsistent Joe artwork was observed
in these views. Corrected facing is visible in all nine pairs, with no added
ground arrows apparent. [Exact review scope and hashes](native-visual-review.json)
remain separate from the actual controller results and owner acceptance. Bike state/VRAM
checks do not establish a convincing mounted/wheelie artwork pose: those authored
assets remain an existing art limitation. The inherited New Game introduction
remains deferred. Inactive field states and unused story Joe NPC scenes remain
explicitly unplayed. This is automated
controller gameplay, not the owner's Delta/visual acceptance.
