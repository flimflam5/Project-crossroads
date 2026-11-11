# Black Ledger — Ecruteak and Olivine QA09

Scope: these two cities only, building on the accepted exteriors and QA08.
This release does not add story progression, badges, encounter rosters or regions.
Release `BlackLedger-Cities-QA09-E2-O1`, final BUILD11. Game-code checkpoint:
`489c404346f572aefb6856b3dd48a9b364a08ceb`; feature branch
`feature/olivine-ecruteak-completion-qa09`, draft PR16. The artifact build-info.json
records its exact delivery-source commit and confirms the tested binary.

ROM SHA256: `df69e014e706168c56180828487a9ab12709a9bccd3dff063fee5f7af5d4f2f4`.
Payload30,261,028bytes in a32MiB ROM; EWRAM226,448/IWRAM28,392. No capacity or
save-format increase. **Owner Delta/visual acceptance remains pending.**

## Actual verification

- BUILD PASS and60/60 actual local automated CI commands PASS.
- Scripted normal-controller mGBA:21/21 final serial stages PASS on the exact
  delivery bytes; all27 Ecruteak and24 Olivine maps toured,488 transitions.
- Every118 required doorway front PASS;329 actual approaches/arrivals/walk-aways
  PASS,25 lateral starting positions physically unavailable and not called passes.
- Four Ecruteak normal Save/cold Continue cases;25 Olivine save/compatibility cases;
  heal/PC/purchase,51 Olivine services,204 city collision bumps,40 Mart probes,
  Theater show/Gym falls/whiteouts, all lighthouse floors/lift/window and port returns.
- All three starters/met location/duplicate prevention, Fly10/cancel/postflight
  Save/Continue, Joe's walk/run/bikes/Surf4/fishing/disembark and same-ROM Survey resume.
- Actual before/after gate recordings: stray magenta removed and all Joe pixels
  visible. All51 native tour screenshots reviewed and zero debug magenta. Original
  battery hashes unchanged. No private save, ROM or snapshot is committed.

See `crossroads/qa/qa09/verification-summary.json`, the evidence `index.html` and
both per-building inventories for source/pixel checks, recordings and actual
fixture/coverage limitations. This is automated controller gameplay plus native
visual inspection; the owner's Delta playtest is a separate acceptance step.
The separately verified GitHub CI artifact has a different ROM checksum; its
successful build is not relabelled as gameplay testing of those other bytes.

## What the city pass contains

- Ecruteak:27 city/interior/landmark maps, both houses, Theater, Center/B1F,
  Mart, optional-practice Gym, both road gates, Barrier Station/corridor,
  Bellchime Trail, Bell1–10F/roof and both Burned Tower floors.
- Olivine:24 native maps covering nine canonical city destinations and four
  retained Black Ledger buildings. The lighthouse has six floors, balcony/window
  route and working paired-door elevator. The port has its furnished terminal,
  rear quay facade, docked ferry and sailboats; safe return paths remain dry.
- Every visible city doorway segment is independently tested, including both
  leaves of wide openings. Old map/layout/heal identities and the save format
  remain stable. Joe, the starter rescue, approved teams/encounters and title/music
  are preserved.

## Reference adaptations and boundaries

The inventories link actual HGSS geometry, props, events and inspected image
references. DS perspective and raised floors become a flat GBA projection.
Owner-supplied Gyms and the accepted Black Ledger buildings are deliberate
additions. The long Gym halls retain their existing two native map identities.
The port needs a small east boardwalk for a safe south-facing GBA entrance.
These are documented adaptations, not claims of pixel-identical HGSS art.

Passenger sailing into another region, DS online services, unapproved reward/
trade/Seal/badge/story events remain outside this pass. Their boundaries are
explicit. The three Ecruteak background homes are genuinely closed in HGSS;
no intended accessible house was replaced with a private-door label.

## Delta on iPhone

1. Export/back up your normal Delta save. Import a COPY into this uniquely named
   ROM. Use normal **Continue**, never a save state from a different ROM.
2. Visit Ecruteak from Route38, both road gates and every city building. Test each
   visible doorway half separately from the front and each physically accessible
   side. Walk away after each arrival, then return through the other half.
3. Check the Theater stage/show and benches; home furniture; healing, PC and Mart;
   optional Morty practice; Station, corridor and Trail; all Bell floors/roof and
   both Burned floors. Walk against walls/trunks, then behind intentional canopies.
4. Reach Olivine via Route39 and return via Route40. Check each home, Cafe,
   Center/B1F, Mart, Gym and the four original Black Ledger locations.
5. Ascend all lighthouse stairs; take the fourth-floor window to the balcony,
   return through the southern third floor and west fourth-floor stairs. Test both
   elevator exit leaves after selecting both floors. Visit the terminal/quay and
   walk the dry east boardwalk back to the city.
6. Check running, Fly and Surf show Joe. Save normally in each city and a landmark,
   reset, Continue and walk away. Confirm your party, starter and bag remain intact.

Report the ROM filename, map/building/nearest sign, which doorway segment and
approach, and whether it followed Continue or an emulator state. Native movement
recordings and per-building checklists accompany this release. Automated
controller gameplay and owner visual acceptance are separate; only the owner
can record the final Delta/visual verdict.
