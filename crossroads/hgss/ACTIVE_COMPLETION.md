# ACTIVE QA10 — owner visual corrections and docked S.S. Aqua

Latest owner feedback rejects a visual-completion claim for QA09. Continue only
identified Ecruteak/Olivine corrections, port and physical S.S. Aqua interiors.
Branch `feature/olivine-port-ship-qa10` starts clean at source285cfa4ebd / game489.
No reset/merge/engine upgrade; keep saves, all map/layout/heal prefixes, accepted
buildings/Gyms, Joe, starter rescue, encounters, title/V5 music and story canon.
Physical docked ship is now authorized; voyages/destination/story/rewards are not.

Owner images D187C84F identify Ecruteak Directory36,45's canonical vacant court,
not a missing Olivine house. Actual HGSS mosaic confirms it has no building.
Source fix adds native soil/curb detail on39 cells only. Other images show the
Olivine port/quay, terminal, Lighthouse1F, Cafe/Center and Ecruteak Center.

BEFORE gameplay is COMPLETE on exactdf69 ROM: all16 Olivine signs, six terminal
leaves, correct Ecruteak court and genuine residence contrast, closed gangway,
contexts. Two genuine old normal batteries privately saved/cold-Continued at
walkingcity23,53 and Surf23,55, without position seeds; originalbattery unchanged.
All emulator processes ended. Public-safe proof: `qa/qa10/before`.

Implementation is IN PROGRESS, not a release:
- Root centrally generated Ecruteak/Olivine exterior assets/maps+owner Gyms;
  capacity fits. North port keepsdoor indices13/15 at23/24,52, now approached
  fromnorth; sign moves off newbody to22,50. Source2lowerhalf tricks forbidden.
- Root maritime builder: two operative gangway leaves27/28,20 to new ship,
  original4quay warps stable, signoffwalkway25,21, native61 opaque ground.
  Old south cityPNG is pinned separately for rear-quay facade and elevator art.
- New private LH helper integrated before final writes; all6floors keep physical
  bits/warps/events and get actual reference carpets/tables/windows/pink lantern
  room. Exactsource/globalground/resource validators pass; owner visual pending.
- Port agent owns seven new SSAqua maps/8cabins+private art/generation. Source
  geometry and all full HGSS floor/cabin rasters recovered. Append group76 IDs
  only, private0–12palettes/512bounds. No imported S.S.Tidal plot or fake sailing.
- Validation agent owns independent QA10 validators and named legacy-port test
  migrations. Runtime agent owns strict facing/fullwidth/controller/oldsave tests.

Build2 compiled successfully: ROM73b82a53ec237f531877f31aabdb76bb5ba56691f9de85d60a868446e4fc9e3a,
payload30,322,400, EWRAM226448/IWRAM28392 unchanged. All66 workflow commands
passed individually after explicit test migrations; final clean ledger pending.
Actual genuine old walking and Surf saves on the new body safely relocate onto
dry ground as walking Joe; unchanged-water Surf remains Surf. Their party/boxes/
bag/money/flags and original batteries remain unchanged. Build1's real Surf-state
failure remains recorded, not reclassified as a pass.

Build2 native review found Joe's torso/legs hidden by two north-port canopy
cells on the public landing. Runtime lanes are stopping before central correction
of ONLY those layer flags, keeping art/physics/warps. All partial Build2 results
remain diagnostic. Do not package until corrected Build3 is built, frozen and
actually tested. Never regenerate or swap ROM/ELF/resources while emulators run.

Remaining: fresh519door approaches, all12shipcomponents/eightcabins/fullwalls/
furniture, berthrest, allLHfloors/lift/window, services/collision/materials, oldsave
fixtures, all3starters/Joe/actions/Fly and normal Save/cold Continue. Native PNGs
and movement clips must identify the exact final binary; owner visual pending.

Final delivery needs unique QA10 ROM, exact source/SHA, per-location comparison/
change/test/limitation report, clean feature push/PR and resumable checkpoint.
Sailing remains separately unavailable because no Vermilion destination/approved
travel progression/first-trip quest/rewards exist; explain rather than invent.
Owner Delta/visual acceptance remains PENDING. QA09 history below is superseded.

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
