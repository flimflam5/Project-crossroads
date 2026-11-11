# QA08 active continuation

Branch feature/ecruteak-olivine-doorways-qa08, from8d13bd62ec. Latest owner scope
is Ecruteak then Olivine only. Read ECRUTEAK_QA08.md and the city building inventory.
Both visible Theater/Barrier leaves and all gate aisle rows are repaired; exact
source/artifact identity is in build-info. Full city acceptance is still open.
Next: identify green-roof report; complete gate exterior/reference comparison;
then reconstruct Olivine canonical buildings/floors/port while preserving four
accepted Black Ledger additions and all stable IDs. Original Olivine geometry
reference files are cached in /workspace/scratch/hgss-reference/olivine-*.json;
original generated facade studies are in /workspace/generated_images. They are
not integrated and must not be described as playable new content. No resets,
engine upgrades, master merge or expansion elsewhere.

# Ecruteak QA07 current checkpoint

Owner scope is Ecruteak only. The active review is ECRUTEAK_QA07.md with per-map
JSON and native qa/ecruteak-qa07 evidence. Reproduced arrows/leaf overlap repaired;
all27 maps/63 round-trip edge pairs checked in an actual Emerald build/mGBA.
Owner visual acceptance and the unmatched current green-roof report remain open.
Do not call the city accepted or resume regional expansion. Older QA05 notes below
remain historical evidence of preserved work.

# Ecruteak QA05 checkpoint

Branch feature/hgss-ecruteak-reconstruction-01. QA04 exterior preserved; Joe field
state checkpoint fe201d2174 precedes the Ecruteak floor/service reconstruction.
Gameplay/evidence checkpoint: a9d0a5fdc3.
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
