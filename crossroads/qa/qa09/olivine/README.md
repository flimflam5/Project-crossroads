# Olivine QA09 — final Build11 controller evidence

Source checkpoint: `489c404346f572aefb6856b3dd48a9b364a08ceb`.

Actual frozen Build11 ROM SHA256:
`df69e014e706168c56180828487a9ab12709a9bccd3dff063fee5f7af5d4f2f4`.

These are actual controller-driven mGBA results on those ROM bytes. They do not
assert the owner's Delta acceptance or pixel-identical DS graphics. The
[file manifest](evidence-manifest.json) gives source paths, sizes and SHA256 values
for all selected public files. All PNGs are native240×160. MP4s use native240×160
H264/yuv420p for normal phone playback. No ROMs, batteries or snapshots are included.

| Final report | Actual result |
| --- | --- |
| [24-map all-edges tour](final-v11-tour/results.json) |24 maps,180 actual transitions,53 round-trip pairs,173 warp trials; all24 native frames have zero debug FF00FF pixels |
| [Save/cold Continue](final-v11-saves/results.json) |25 cases PASS, fresh run without snapshots/resumes |
| [Services and ambient interactions](final-v11-services/results.json) |51 checks PASS, including actual purchase and Jasmine practice loss/local respawn |
| [City walls/trees](final-v11-collision/results.json) |204 controller bumps PASS, zero inaccessible-approach skips |
| [Both cities' Mart furniture](final-v11-mart-props/results.json) |40 controller bumps PASS, zero skips |
| [Terrain/material movement](final-v11-materials/results.json) |59 semantic cases PASS,18 native clips;37 physically unavailable fence approaches explicitly skipped; actual Surf and dry return16,34 |
| [Six normal front-counter conversations](final-v11-counters/results.json) |6 exact-message cases PASS, separately recorded; these also occur in the51 service checks |

## What was exercised

The25 Save/Continue cases cover all nine appended maps, isolated southern3F and
top6F, both actual panel-selected elevator floors, Center/home, actual Surf and
explicit legacy/safety fixtures. The restored CenterB1F lower floor is reached by
normal walking to8,12, then Save/cold Continue, walk-away, stairs out and return.
Every new map/component case also exits and returns after Continue. Party, boxes,
starter state, flags and decoded currency/inventory remain unchanged. Both native
cabin destinations survive an actual cold boot and exit onto the selected floor.

Four additional legacy fixtures use positions independently verified as public,
unoccupied, non-door floor in immutable V7:7,9 in both Marts and4,8 in both Center
basements. The new source stools block these locations. The fixtures seed only
those obsolete coordinates in a private test copy, then use normal Save and cold
Continue. All four migrate safely and actually exit and return. The separate
walking-water safety case is explicitly **synthetic**: no historical walking cell
in this baseline became water. Actual Surf retention is tested independently.
The other fixtures cover the exact old heal, stale layout, historical wall and
isolated ceiling-cap cases; none is represented as the owner's actual save.

The51 service checks cover the nurse/local heal, PC menu with unchanged party and
boxes, real200-money Poké Ball purchase, rest decline/accept, house residents,
café counter and visitors, five new signs, accepted office interactions, neighbor,
Center/Mart visitors, six front receptionists and maritime content. Every lighthouse
floor plaque, keeper/visitor/beacon, balcony view, port desk/visitor/quay clerk and
boarding-boundary sign was actually used. The reception tests require the actual
staff local ID, exact expanded message and return of control after front-A across
native MB_COUNTER. They do not substitute a convenient side approach. The final
Jasmine855 practice loss reaches the local nurse8,13 and heals the party.

The204 wall/trunk bumps cover all13 city buildings and all3 free trees, from
accessible sides. Recordings show the fishing-house wall, Silph wall and residence
tree. Separate canopy frames preserve intentional foreground overhangs. The40
Mart trials cover three plants, eastern rack, glass display and all four stools
in **both** cities; four recordings and native screenshots accompany the report.

All seven suites ran serially, each from a fresh normal battery load on the exact
Build11 ROM, with [phase identities and exits](final-v11-lane/completed.json).
There were no resumes from older binaries. These local mGBA results do not
certify a differently compiled GitHub CI ROM.

Private service fixtures reduce HP/set poison to exercise healing, rest and loss;
the purchase uses existing money. The shared harness discloses temporary random
encounter suppression. Walking trials use actual public survey-desk OFF and dry
paths; no position/warp/map writes replace movement. All source batteries remain
hash-identical:
`b03ff1ef488fbd25de016e828483bc3001787b84e450a45eaa0ac12a11de30ab`.

## Before footage and diagnostic honesty

- [V8 counter defect](baseline-v8-center-counters/results.json), ROM
  `24e8c300d564b98e6fdea3216a868dc4c5c920d19721a5de7ef4974387081fab`:
  all six customer-side front-A presses received no message. The native
  [B1F before clip](baseline-v8-center-counters/PokemonCenter_B1F-4.mp4) pairs
  with the [Build11 after clip](final-v11-counters/PokemonCenter_B1F-4.mp4). The before
  report records a successfully reproduced defect, not working services.
- [V6 port defect](baseline-v6-port-clipping/results.json), ROM
  `b9701dcc60a0bcf62cac6bfa177c433eae78dbfa8142b7739881ba839bc266bd`:
  [normal movement walked through the port body](baseline-v6-port-clipping/north-roof-and-glass-walk.mp4).
  Later port repair and return recordings are in the companion
  [doorway evidence](../doorways/README.md), with their own version identities.
- The first V9 extended-service attempt stopped at Lighthouse4F because its test
  selected the real western27-cell component, while the plaque belongs to the
  real eastern106-cell component. The corrected test explicitly reaches native
  warp0 by the normal stair/lift network. It then reran **all51 checks fresh**.
  The original diagnostic folder/log remain separately labelled
  `qa09-olivine-services-v9-staging-fixture`. No map changed and no plaque assertion
  was skipped or relaxed.

Build9 reports/images in `final-v9-*` are historical only. V7 reports/images are preserved in `v7-saves`, `v7-services`, `v7-collision` as
**historical regression evidence**, not final delivery proof. V7 had identified
material/prop omissions and the Save driver resumed a disclosed same-ROM snapshot
after a planner correction. The final Build11 Save25 run uses no such resume.

The [validation notes](../../../hgss/OLIVINE_VALIDATION_QA09.md) describe exact
source/physics migrations, loaded-palette limits and GBA adaptations. Independent
source, compiled-map and gameplay checks complement the owner's visual review.
They do not turn deferred voyages, DS online services, unapproved story events or
legendary/reward/badge content into implemented features.

## Stopped V10 candidate

The V10 candidate (source7d92f79357b744dddb706bba121d7bd5e6fc4254,
ROM3bec0fedbb481cc051c38d719499b584e9a4c219e42b66bef298f6aa0c5ec7a9)
completed the [24-map Olivine all-edges tour](final-v10-tour/results.json):180
actual transitions,53 round-trip pairs and173 warp trials. It was then stopped
after independent native review found actual Ecruteak gate magenta underlays and
opaque foreground floor hiding Joe. This candidate is superseded, not a release.
The partial Save run and all later unstarted suites are not marked passed.
These tour captures remain historical evidence, not proof of corrected gates or
of a later delivery ROM.
