# Ecruteak QA05 checkpoint

Branch feature/hgss-ecruteak-reconstruction-01. QA04 exterior preserved; Joe field
state checkpoint fe201d2174 precedes the Ecruteak floor/service reconstruction.
Current deliverable scope/tests/known limitations are in ECRUTEAK_QA05.md and
../RELEASE_HGSS_QA05.md. Source commit/checksum are in the artifact build-info.json.

Implemented: two furnished houses, Theater/five-performer show, dedicated
Center/Mart/basement, optional-practice Gym bridge with safe returns, both regional
gatehouses, reference-backed station/corridor, canonical autumn Trail floor,
Bell1–10F/roof and Burned1F/B1F. Appended six map IDs after QA04; old IDs/save format
remain. Native stairs and whiteout arrivals were fixed after actual emulator failures.

Verification: build PASS; structural/generator/build-inclusion checks PASS; actual
27-map/246-transition tour,509 exterior collision probes, five-performer show,
healing/bridge falls/Morty loss/local respawn, normal Save/cold Continue and copied
stale-layout migration PASS. Fly/Surf/bikes/fishing and three starter choices pass.
Native evidence/logs are in ../qa/hgss-qa05/. They do not assert owner visual acceptance.

Next: owner Delta QA and reported fixes. Do not expand geography or replace the
exterior as an incidental cleanup. See JOE_FIELD_AUDIT.md for unavailable/unplayed
states and reused animation poses. DS online/candle story gates/rewards remain
explicit adaptations/omissions, not secretly implemented content. Broader HGSS
Johto and the original prologue remain unfinished. No merge to master is authorized.
