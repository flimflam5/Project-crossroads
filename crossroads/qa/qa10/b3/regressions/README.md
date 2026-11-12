# QA10 B3 accepted-function regression evidence

Source `e7e2c085a5a61ef727d06f9f682af7d3a954cc06`; frozen B3 checkpoint ROM
`af59dff1b06b99a9599c6f98b6fb6bd1e765cc52c0838a2dec5c79a6c1f88373`.

All eight fresh serial stages exited0. This is the B3 checkpoint; later B4 testing must be reported separately, not relabelled from these results. [Exact results](results.json) and the
[file hashes](evidence-manifest.json) identify the tested B3 bytes.

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

Battery-backed tests use copies of the historical battery; starter/first-loss
tests use disclosed fresh-game initialization. The original and lane input copy
remain hash-identical. Fresh-game, HP/status, temporary gear and encounter
suppression fixtures are disclosed; no map/player-coordinate writes replace
movement. No private battery, state, ROM or memory dump is public here.

An independent read-only review inspected82 native frames:7 title/pre-title,
16 Joe/action/standing/battle/running,55 services and4 accepted-city Fly/menu
frames. No new service/map corruption or inconsistent Joe artwork was found.
The known lighthouse6F glass-stripe art mismatch belongs to this B3 checkpoint;
its later B4 correction and tests must be assessed separately.

The three Bike/wheelie stills are pixel-identical and show a standing silhouette:
the state/VRAM checks passed, but those screenshots do not visually prove the
mounted or wheelie poses. The New Game handoff retains the inherited dim,
green-band introduction frame; the existing Birch introduction remains deferred.
Still screenshots do not verify animations. Inactive field states and unused
story Joe NPC scenes remain explicitly unplayed. This is automated controller
gameplay, not the owner's Delta/visual acceptance.
