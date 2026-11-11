# Ecruteak and Olivine — QA09 city completion

Owner scope: finish these two cities only. Branch
`feature/olivine-ecruteak-completion-qa09` preserves QA08 `fda32b7ed0` and source
checkpoint `3f935d5e8600c5a280b9172b555edb35ca52b6c0`. No master merge.

## City inventory

| City | Native maps | Intended accessible content |
| --- | ---: | --- |
| Ecruteak |27|Two homes, Theater, Center/B1F, Mart, optional-practice Gym, west/east gates, Barrier Station/corridor, Bellchime Trail, Bell1–10F/roof, Burned1F/B1F|
| Olivine |24|Nine canonical destinations: Gym, Center/B1F, Mart, three homes, Cafe, lighthouse six floors/balcony/elevator, port terminal/quay; four preserved Black Ledger buildings|

The Ecruteak exterior and both owner-supplied Gyms remain the accepted designs.
Three Ecruteak background homes are actually closed in HGSS event data; no
intended accessible home is concealed behind a private sign. Olivine's Joe home,
neighbour home, Silph subsidiary and Harbor Office remain explicit additions;
canonical houses are separate, not replaced by them.

Per-building/per-floor requirements, source references and individual results:

- [Ecruteak review](ECRUTEAK_FINAL_REVIEW.md) and
  [27-map checklist](ecruteak-qa09-building-checklist.json).
- [Olivine inventory](OLIVINE_COMPLETION_QA09.md) and
  [machine-readable checklist](OLIVINE_COMPLETION_QA09.json).
- [All118 visible doorway segments](doorways-qa09.json).

## Reference and visual corrections

The audit uses actual HGSS images and SHA-pinned public pret geometry, permissions,
props and events. Original native GBA art replaces DS models; reference textures,
ROMs and raw commercial archives are not integrated. Each adaptation has its own
record instead of a blanket claim of exact HGSS art.

Ecruteak's correction pass includes13 source-position Theater benches/aisle,
source0066 home kitchens/windows/bookcases, Center plants, private gold-crest/red-
lantern Theater stage, four source plants and blue-gray furnishing in each gate,
restored Center basement lower waiting row/furniture, source Mart displays/plants/
stools/rack, Bell5/6/7 wall lamps and the visible Burned Tower collapsed shaft.
The full27-map source-public-floor audit found only the B1F crop; its height14
restores that floor without renumbering its map or layout.

Olivine has the canonical64x64 ground plan, dedicated facades, source0097 homes,
source0136 Cafe, source-backed services/Steel Gym, all lighthouse floors, window/
balcony return, actual two-stop paired-door elevator and furnished port/quay.
The final visual pass corrects white fences, timber terrace/railing/parasol
underlays, gray offshore rocks, two missing lighthouse2F plants, beacon housing,
source port chairs, home/Cafe wall finishes and the actual common-service fixes.

HGSS uses the same blocked flag for cliffs, fences and model footprints. The
converter now classifies these using exact reference-specific masks. Twelve
obsolete table blockers open on the timber terrace;65 blocked cells of the old
DS port model become sea after the documented GBA facade relocation. No unrelated
city wall flags are relaxed. Every accepted Black Ledger facade cell is pinned
to its old per-layer pixels/attributes/collision/elevation.

## GBA adaptations and explicit boundaries

- DS perspective/height becomes a flat GBA projection. Long Gym halls retain their
  existing two native maps. Center reception heights flatten but remain functional.
- Owner Gym art and the four Black Ledger buildings are deliberate additions.
  Small infill plots preserve the canonical homes; moved terrace props accommodate
  the accepted offices. Their exact changes are documented in the inventories.
- Olivine's flat port facade faces south. Its dry east boardwalk connects both
  arrival leaves to the city; the retained source inspection pier is a documented
  dock adaptation. The old DS model collision is removed, not disguised as rocks.
- Passenger sailing to another region, DS online services and unapproved story,
  trades/rewards/Seal/badge events are outside this city exploration assignment.
  Docked ships are visible; these services are not falsely claimed to work.
- The historical green-roof report was not tied to an identifiable ROM/location.
  Current facades are independently audited and controller-tested; this is not a
  fabricated reproduction of that unidentified historical binary.

## Verification states

Source visual corrections are undergoing final coordinated generation/build.
Final delivery checksum and fresh emulator results will replace this paragraph
before delivery. Historical Build7/EcruteakE1 uses source `3f935d5e86`, ROM SHA256
`0734501b031d05156a28e685dc1c2748153cb065222bd67b0d2e7cea47fefbca`.
Its passed gameplay evidence is retained, explicitly labelled historical; it is
not a substitute for testing the corrected final bytes.

Independent validators preserve immutable baselines with named, exact deltas for
the intentional changes. B1F additions, model-collision fixes and private art
packing have positive source/pixel/behavior checks. Existing assertions are not
removed to obtain a pass. See [validation changes](OLIVINE_VALIDATION_QA09.md).

Owner Delta/visual acceptance remains a separate state. No full-game or whole-
Johto completion claim is made. Source/build/test status cannot grant acceptance.

## Delta instructions

See [release and practical checklist](../RELEASE_CITIES_QA09.md). Back up your
normal save and test a COPY via Continue, never an older cross-ROM save state.
Test both leaves/fronts/accessible sides of each doorway and walk away after
arrival. Visit all floors and return, use services and practice battles, then
save/reset/Continue. Recheck Joe Fly/Surf and your party, starter and bag.
