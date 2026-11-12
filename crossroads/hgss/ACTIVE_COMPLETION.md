# ACTIVE QA10 — final tested B5 handoff

Owner scope remains Ecruteak/Olivine/physical docked Aqua only; no further regional
expansion until review. Preserve all current IDs/saves/designs/additions, Joe,
starters/encounters/battles/title/V5 music and story canon. No master merge,
reset/force push, engine upgrade, arbitrary rewards or voyage/story invention.

Branch feature/olivine-port-ship-qa10; game source
cc643ffe711204f3ef38e34e7aa1eb8c9558720f; generator-only successor
ed375e9f382cafc8f225136876778534ac111a17. Draft PR17 targets QA09.
Tested ROM ee2d81d5d0b55b7f1f9d36d1c9b055700164da439f51af7a66b5fb2d2147f90b;
ELF a950a6fd77e4320c3bb864c3b96e981a1da24cb63727f8151e2124c6577f90eb.
Payload30,322,784; EWRAM226448/IWRAM28392 unchanged. All emulator lanes ENDED.

Completed: seven-map/eight-cabin/12-component physical Aqua; coherent north port
and full two-leaf landing; source-referenced LHfloors/28-cell cyan enclosure fix;
39-cell canonical vacant Ecruteak court;25-cell/6-map nativeOnWarp+OnReturn facing
fix. Every other B4 game input remains exact apart from those six native scripts.
All45groups have independently fixed intended facings; no arrowbehavior/art/
collision/warp/ID/saveflag/C/criticalconstant change for the facing repair.

B5 PASS:68actualstaticcommands;18scheduledphases(17actualmGBA+1independentrecord
postcheck); seven genuine old-gate/control coldContinue cases; old-port walking/
Surf migration and valid-water control. All173doorfronts/482executedapproaches
PASS;37unavailablelaterals(35solid+2sea),0fails/missing. All67B4facefailuresfixed.
FullAqua1169bumps/12roomsaves/14interactions/2berthhealthfixtures; sixcitysuites
including199dry+24Surf/59materials/6counters/LH12saves+5journeys+2circuits/court39;
eightacceptedfunctionstages incl51services/3starters/battles/Fly/Joefields/running.
Original b03ff1ef488fbd25de016e828483bc3001787b84e450a45eaa0ac12a11de30ab battery
unchanged. Copies only; no private save/state/ROM belongs inGit.

Evidence qa/qa10/final/B5; raw reports keep real identities, not relabelled B4/B3.
Historical failures and source/test migration explanations remain archived.
Latest exact scope: verification-summary.json, RELEASE_OLIVINE_AQUA_QA10.md,
LOCATION_CHECKLIST.md. Native240x160frames/MP4s plus labelled contact sheets are
separate from source/static layouts. Owner visual/Delta approval remains PENDING.

Delivery identity is recorded by the final artifact build-info.json and
BlackLedger-Olivine-Aqua-QA10-A1-Delivery.json. Distribution names are
BlackLedger-Olivine-Aqua-QA10-A1.gba / .zip / -Evidence.zip / -SHA256.txt.
The verified local ROM is authoritative; CI artifacts can differ by compiler.
Older QA09 deliveries and all diagnostic proof remain preserved. The packaging
script refuses stale checksums, uncommitted source, private evidence and overwrites.
All engineering checks are complete; next action is owner Delta/visual review.

Known limits: sailing/destination/story/rewards; DS online/Seal/trade/rod decisions;
original HGSS elevator visual unavailable (preserved chooser is deliberateGBA
adaptation); mountedbike silhouettes/legacyNewGame cinematic; cropped visual
reviews do not certify all unseen decoration. No city100%/1:1 statement.
After delivery: owner Delta checklist/visual review before expanding elsewhere.

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
