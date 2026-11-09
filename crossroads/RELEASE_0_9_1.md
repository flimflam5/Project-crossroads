# Black Ledger 0.9.1 — first visual/collision repair checkpoint

The owner reports 0.9 connectivity works but visual/collision QA has NOT passed.
Expansion is paused. This is a limited correction build, not a region-wide polish
claim. Exact source commit and ROM checksum accompany the artifact in build-info.json.

Five layouts corrected: Ecruteak City, Mahogany Town, Mahogany Workshop, Route38 and
Route39. Shared custom ground-layer fixes also affect Olivine's existing exterior
art; its layout is unchanged. Johto-only root variants preserve shared Hoenn art.
Connections, map/save/layout/heal IDs, events, encounter tables, starter uniqueness,
Joe, title and V5 music are retained. No new geography/story/trainers/encounters.

See [review manifest/evidence/testing/Delta checklist](qa/visual-0.9.1/README.md).
The manifest lists all 149 maps: five first layout passes, one partial layer pass,
143 awaiting individual visual review. Native before/after PNGs and movement MP4s
are provided. Bell/Burned interiors have regression coverage but no visual redesign.

Build PASS; structural checks PASS; actual controller tour 70 transitions/22 roundtrip
pairs PASS; 126 wall/tree/furniture probes PASS; normal roof overhang/wall distinction
PASS. Two normal Save/fresh-core Continue checks and the existing-area/starter/Joe
regression run PASS. Automated or Codex inspection does not constitute owner visual
acceptance. All old assertions remain; extra checks enforce stable contracts,
recorded repair scope, assembled furniture and ground-layer/door invariants.

Remaining: individual visual/collision review of the rest of the network, broader
route/town level design, other interiors and landmark polish. Previously deferred
story/badges/teams/encounters, special Joe movement art and legacy map interfaces
remain deferred. Reported title-audio quality still needs owner listening QA.
