# QA09 final two-city checkpoint — implementation and verification complete

Owner scope: Ecruteak and Olivine only. Preserve the accepted exteriors/Gyms,
map/layout/heal/save identities, Joe, title/V5 music, starters/met/uniqueness,
approved encounters/practice battles and existing travel. No master merge,
reset/force push, engine upgrade, new regions/story/rewards/badges.

Branch `feature/olivine-ecruteak-completion-qa09`; game-source checkpoint
`489c404346f572aefb6856b3dd48a9b364a08ceb` is pushed; draft PR16 targets QA08
`fda32b7ed0c68251ffa594d8496495854d3ff26e`, not master. Final documentation/evidence
commit is identified by Git and the delivery build-info.json.

## Frozen final binary and actual results

BUILD11 ROM SHA256:
`df69e014e706168c56180828487a9ab12709a9bccd3dff063fee5f7af5d4f2f4`.
Payload30,261,028bytes; EWRAM226,448; IWRAM28,392. Log `/tmp/qa09-build11.log`.
All60 actual local CI commands PASS. All21 fresh serial stages PASS; all emulator
lanes have ended. Ecruteak27maps/308transitions; Olivine24maps/180transitions.
All118 front segments/329 executable doorway approaches PASS;25 lateral starts
physically unavailable. Full services/landmarks/collision/furniture/field actions,
all3 starters, actual practice whiteouts and Save/cold Continue pass. Final full
source ground checks cover27,062 map+border cells; all51 native frames are zero
magenta and visually reviewed. See `qa/qa09/verification-summary.json` and each
city's building checklist, not historical intermediate results.

Original battery remains
`b03ff1ef488fbd25de016e828483bc3001787b84e450a45eaa0ac12a11de30ab`.
Only copies/disclosed fixtures were tested. The owner's newest private Delta
battery was not supplied. No ROM/battery/state/dump belongs in Git.

## Changes since the historical checkpoints

Source3f935d5e: canonical Olivine reconstruction and Ecruteak source interiors.
Source5664fece: furnished/source-backed city finish, safe furniture/service fronts,
private palette/resource/registration fixes and preserved old service templates.
Source7d92f793: actual HGSS Theater green audience floor/purple cushions, exact
physics/geometry preserved. Source489c4043: gate floor/void/plant underlayer fix.

B10 normal movement actually reproduced600 magenta pixels and hidden Joe on
ordinary gate floors. B11 after-tests show zero magenta and192/192 or165/165
Joe pixels visible. Four appended north-plant art IDs preserve every original
attribute/event/alias/physics/save identity. Independent global source/frame
checks reject the historical bad frame as a negative control. B9/B10 tour/probe
passes alone did not constitute visual quality; retain their diagnostic evidence.

Olivine historical O1 source5664/ROMd5ab is archived as a distinct checkpoint;
its Olivine work passed but its Ecruteak gates share the later-found defect.
Ecruteak E2 / current combined E2-O1 uses the final df69 bytes, retesting both
cities. Never distribute an old B9/B10/CI binary as the final tested build.
Current CI run43015464700 successfully built Emerald/60 regressions and a real
artifact; its synthetic merge tree equals489, but ROMe535 differs from localdf69.
`qa/qa09/ci-build11.json` records this explicitly. Local runtime results apply
only to df69, not that other binary.

## Final delivery / next step

Local delivery names are `BlackLedger-Cities-QA09-E2-O1.zip`, the matching
evidence ZIP and directGBA in /workspace. The package build-info and PR16 record
the exact delivery-source/ROM checksum. Before recreating anything, inspect those
existing files and their Delivery.json/SHA256 reports. Final packaging requires
a clean documentation/evidence commit, identical-byte rebuild and verified ZIP
CRC/embedded hash. PR16 remains draft/unmerged; the next owner step is Delta QA.

The two-city physical map/interior scope has no known reproduced functional
defect after this pass. Owner Delta/visual acceptance is still PENDING; do not
expand elsewhere before that review. Remaining comparison limits are the Theater
south margin, complete reverse-quay and separate lift-cabin raster views; actual
source geometry/props and traversal are verified. Flat GBA projection, custom
Gyms and original Black Ledger additions are explicit adaptations. DS online
services, S.S.Aqua voyages/ship interiors/other-region arrivals and unapproved
story/trades/rewards/Seal Case/badges remain separate scope boundaries, never
invented during this map pass. Inactive Dive/watering/decor/VSSeeker/contest/link
states were source-audited, not normally activated here. See CITIES_QA09.md,
RELEASE_CITIES_QA09.md and both city inventories for the practical review.
