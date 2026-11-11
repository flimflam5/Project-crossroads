# Ecruteak and Olivine QA09

Owner scope: finish these two cities; no expansion elsewhere. Work continues on
feature/olivine-ecruteak-completion-qa09 from QA08 fda32b7ed0. No master merge.

## Implemented city scope

Ecruteak retains its accepted exterior/custom Ghost Gym, all27 city/landmark maps,
paired entrances, road gates, Station/corridor, Bellchime Trail, Bell1–10F/roof,
Burned floors, homes, Theater and services. QA09 corrects13 source-position
Theater benches/aisle, both home kitchens/windows/bookcases, three Centerplants.
Source comparison and individual records: ECRUTEAK_FINAL_REVIEW.md and
 ecruteak-qa09-building-checklist.json. Three canonical background homes are
closed in HGSS; they are not omitted accessible interiors.

Olivine has the canonical64x64 ground plan and all nine intended city buildings:
Gym, Center, Mart, lighthouse, three homes, cafe and port. Four accepted original
locations remain separate additions: Joe's home, neighbour home, Silph subsidiary,
harbor office. Services, six lighthouse floors, balcony/native two-stop elevator,
branched window route, port terminal/quay and two-map optional Steel Gym retain
existing IDs; nine maps and dedicated layouts append. Original shared service
layouts remain byte-identical for other cities. Starter case/terminal/rest/travel,
approved encounters/teams, title/music/Joe/save structures remain intact.

## Reference and GBA adaptations

Actual HGSS city mosaics and SHA-pinned public pret geometry/events/props are
recorded in canonical_events and individual room/landmark reference manifests.
Original native art replaces DS perspective models. Owner-supplied Gym exteriors
are deliberate Black Ledger additions. Tall Gym halls span existing map IDs;
raised Center reception is flattened; DS online reception is offline. No new
main story, badge progression, reward/trade distribution or curated encounters.

The port's flat facade needs a bounded east boardwalk to connect its south
landing back to the city. This corrects a V5 one-way component exposed by actual
door approach testing; the canonical northern covered approach remains. Harbor
terrace parasols shift to fit the preserved Harbor Office. Original forest infill
accommodates Joe and his neighbour without deleting canonical homes; the offices
occupy the commercial promenade. All additions/deviations require owner review.

## Verification checkpoint — awaiting final combined binary

BUILD5 compiled with payload30,156,580/33,554,432 bytes, EWRAM226,448 and IWRAM28,392.
Its exact SHA is c2f30ef04d3890e9ac947ee1f6f28a04b7e6e2d08c1a7f5e77a68fc7c697f658.
V5 is an intermediate diagnostic build, not the delivery ROM.

V5 actual controller-driven mGBA (not owner playtesting): Ecruteak27-map tour,
308transitions/73roundtrip pairs;26furniture trials/6clips;19ground cases/36trunk
approaches/423exactleafpixels. Olivine8Save/cold Continue cases preserve exact
party/boxes/decodedbag/money/flags/starter;219drycollision bumps at13buildings/
3trees. Both cities' doorway run stopped after112executedPASS/5unavailable side
approaches to repair the independently detected port return defect. Starter run
reached that defect before rescue trials; no false starter-pass claim for V5.

## Final candidate — controller verification in progress

All identified city/landmark models are now implemented, including the port rear
facade/docked ferry/sailboats, city boats/pennants, lighthouse plants/purple top
floor/masonry and balcony rails. Both port leaves keep their canonical coordinates;
its GBA facade faces south, so the east boardwalk is the dry public approach and
return. Its body/glass is solid; thin eaves over sea retain native Surf semantics.
Six office ceiling caps are blocked while their exact pixels/scripts remain.

BUILD7 payload30,170,932 bytes; EWRAM226,448; IWRAM28,392. Actual delivery-candidate
SHA256:0734501b031d05156a28e685dc1c2748153cb065222bd67b0d2e7cea47fefbca.
All24 actual compiled Olivine blockdata arrays match authored map outputs.
Source is being checkpointed and final controller suites are running on these
frozen bytes. Final completion/acceptance is not claimed from compilation alone.
Passenger sailings, DS online communication and unapproved story/rewards/badges
remain deliberately outside this city exploration pass; no new regions built.

## Delta test procedure

Export/back up the normal save; import a COPY into the uniquely named ROM and use
Continue. Never restore an emulator state created by an older ROM. Test every
visible doorway leaf independently, front and available lateral approaches,
then walk away after arrival. Check city exits both ways, heal/PC/shop/practice
battles, every lighthouse/tower stair, elevator leaves, window/balcony return,
port return journey, Joe's Surf/Fly, then normal Save/reset/Continue. Report the
ROM filename, building/nearest landmark and normal save versus state on a defect.
