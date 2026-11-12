# Black Ledger — Olivine / docked S.S. Aqua QA10 A1

Owner-review build on `feature/olivine-port-ship-qa10`, draft PR17. Game-source
checkpoint: `cc643ffe711204f3ef38e34e7aa1eb8c9558720f`. The artifact's
`build-info.json` identifies the exact final documentation/test revision and tree.
No merge to master, engine upgrade, save-format change or regional expansion.

ROM SHA256: `ee2d81d5d0b55b7f1f9d36d1c9b055700164da439f51af7a66b5fb2d2147f90b`.
32 MiB padded ROM; payload 30,322,784 bytes, EWRAM 226,448, IWRAM 28,392. RAM unchanged.

## What changed

- Olivine port: north-facing two-leaf entrance, direct dry pier, correctly oriented
  terminal arrivals/returns and solid building body. Two landing layer cells now
  draw beneath Joe, keeping his entire body visible. The accepted building art
  and both open leaves are retained.
- Terminal/quay: main and inspection exits connect coherently; signs no longer
  obstruct boarding. Both visible hatch/gangway leaves board a physical S.S. Aqua.
- Ship: seven new append-only maps with 12 physical components/eight cabins,
  captain's room, passenger lounge, crew berths, galley/kitchen and engine deck.
  All cabins are furnished individually. Native rest supports Yes/No without
  starting a voyage or changing story/progress. No arbitrary trainers/encounters.
- Lighthouse: all six floors and balcony receive actual-HGSS-referenced floors,
  rugs, furnishings, windows and lantern-room materials. Final 28-cell correction
  separates the cyan inner enclosure from outer glass and fills two false black
  corners. Other six maps/old used drawings/full attributes remain exact to B3.
- Ecruteak: 39 directory-court cells gain soil/curb detail. The photographed signed
  lot is west of the Dance Theater; actual HGSS leaves it open. No building belongs
  on this plot. Accepted exterior/Gym and real western residence remain.
- Gate and corridor arrivals: native post-spawn and return-to-field scripts correct
  facing at 25 precise landing cells in six existing maps. East/west gates now face
  into the landing; the Barrier Corridor entrance faces south. Graphics, collision,
  open widths, warps and IDs stay exact. No arrow tile behavior is added. The same
  correction applies to normal Continue/menu return only at those landing cells;
  other positions and persistent data are untouched. All 45 doorway groups have
  independent intended-facing expectations.
- Save compatibility: genuine old port walking/Surf saves obstructed by the new
  facade relocate to verified dry floor with walking Joe. A valid old water Surf
  save remains Surf. No Pokémon metadata, party, boxes, bag or permanent flags are
  rewritten. Existing map/layout/heal prefixes and starter uniqueness remain.

Primary changes: native Olivine/Ecruteak/landmark/ship generators and generated
layouts, private tilesets, ship scripts, `src/crossroads_continue.c`, append-only
map registrations/atlas, workflow and focused validators/emulator runners. The PR
contains the full file diff; generators reproduce the authored outputs.

## Actual verification

BUILD PASS. All 68 actual workflow commands pass (initial generator-check failure and exact rerun are retained). All 18 scheduled B5 phases pass: 17 fresh mGBA suites plus the independent facing-record audit. The separate seven-case old-save Continue pilot also passes. All 173 doorway fronts and 482 executable approaches pass; 37 lateral starts are physically unavailable and separately recorded (519 total attempts, zero failures).

All seven ship maps/12 physical components/eight cabins were visited; 12 normal Save/cold Continue checks, 14 NPC/sign interactions, both real NO/YES berth-rest checks, and all 1,169 independently enumerated source-wall/furniture approaches pass. Lighthouse 8-map traversal/lift/window/stairs and 12 normal Save/Continue checks pass, including both-direction 6F enclosure circuits.

City collision: 199 dry building/tree approaches plus 24 actual Surf approaches around all four port sides; both port leaves require every opaque Joe pixel visible at the actual exit and north landing. All 59 ground/material cases, six front-counter conversations and 39 Ecruteak courtyard cells pass. Genuine old port walking/Surf saves and valid-water Surf control pass without mutating their original batteries.

Title, boot, all three starters/met/uniqueness, first-loss/respawn and actual Joe battle graphics, Fly to all 10 cities/cancel/post-flight Save/Continue, Joe field states/running and 51 Olivine services were exercised on this same ROM. See the exact summary for fixture scopes and individually recorded results.

Every one of 45 doorway groups passes strict arrival-facing checks plus the independent reference-based audit. Historical B4 failed 67 facing trials despite its old phase passes; those results remain diagnostic and are not called accepted.

These are automated checks and scripted controller input in a real mGBA core,
plus inspection of actual native 240×160 frames. They are separate from the
owner's Delta playtest and visual acceptance, which remain PENDING. No private
battery, state, ROM or memory dump is committed. Only copies/disclosed test
fixtures were exercised; the owner's newest private Delta battery was not supplied.

[Per-location reference/change/test checklist](hgss/qa10/LOCATION_CHECKLIST.md),
[comparisons and movement recordings](qa/qa10/index.html),
[exact verification summary](qa/qa10/verification-summary.json) and
[test migrations/negative controls](hgss/qa10/VALIDATION_CHANGES.md).

Earlier candidates remain explicitly labelled. Build1's actual Surf-state failure,
Build2's portal body-occlusion, B3's incorrect 6F material, and premature berth-menu
probe are diagnostic history. None is relabelled as final-ROM verification.

## Limits and adaptations

Sailing is separately unfinished: no Vermilion destination, approved Black Ledger
travel/ticket/progression rules, first-trip quest or rewards exist. HGSS's original
sailing dependencies are documented; this build opens the docked ship without
inventing them. Existing Harbor Office travel/Alpha bridges are preserved.

GBA walls/furniture/palettes are original orthographic adaptations of actual HGSS
references. The top-floor optical enclosure uses the retained angular/U footprint
and small northern cap, not a literal DS cylinder. Table/seat groups compress into
existing solid footprints. Ship hatch widths project five inside cells to two
outside leaves. These include deliberate art choices, not universal hardware
limits. Little cabin rugs/tablecloth shading and some colors differ. The HGSS lighthouse lift has an automatic opposite-floor ride; the retained GBA
floor chooser is a deliberate functional adaptation. Its cabin decor is original
and lacks an independently verified HGSS raster; see the elevator reference audit.
DS online and Seal functions remain unsupported. The canonical species trade and
rod reward are deferred progression/content decisions, not implemented services.
Owner visual review is required; no 1:1 or 100% claim.

Existing scope outside this pass remains unfinished: bike art shows Joe but lacks
convincing mounted poses; the New Game cinematic still retains inherited content.
Title art, V5 music, Joe's field identity, accepted starters/battles, homes/offices
and intentional additions were preserved. No new main-story decision was made.

## Delta on iPhone

1. Export and back up your existing battery save from Delta. Import a COPY into
   this uniquely named ROM. Use normal **Continue**, not an older save state.
2. Approach the port from the city pier. Enter each half separately; exit both
   leaves, check Joe's full body/facing and walk back to the promenade. Test the
   terminal's main and side exits both ways and read the relocated boarding sign.
3. Board through both gangway halves. Visit all eight cabins, the captain, lounge,
   crew berths, galley and engine deck; use both lower-deck stairs. Decline rest,
   then accept it. Save aboard, restart/Continue and return to Olivine normally.
4. Visit every lighthouse floor, the4F window/balcony return and lift. Try both lift
   leaves for both destinations; save/Continue in the lift and a tower room. Check
   the cyan top-floor enclosure, furniture overlap and movement around its walls.
5. Recheck Center/healing/PC, Mart, Cafe, three canonical houses, Joe's residence,
   Silph office and Harbor Office. Try every visible doorway segment from front
   and accessible sides; inspect buildings, trees, water and signs.
6. Visit Ecruteak's textured directory courtyard, surrounding buildings, Theater
   and Gym. Recheck starter refusal, summary, Fly/Surf and normal save/Continue.
   Report any clipping with the location and a screenshot. Visual acceptance is yours.
