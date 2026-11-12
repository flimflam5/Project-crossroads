# Black Ledger — Olivine / docked S.S. Aqua QA10 A1

This is an owner-review checkpoint, not a claim that either city or Johto has
passed visual acceptance. Feature branch: `feature/olivine-port-ship-qa10`.
Exact delivery revision, checksums and final results accompany the delivery.

## Changes

- Corrected north-facing Olivine port entrance, both visible leaves and arrivals.
- Added seven source-referenced S.S. Aqua maps: eight cabins, passenger hall,
  captain room and furnished crew/galley/engine lower deck; physical boarding and
  return only. No voyage destination, story rule, ticket or reward was invented.
- Reworked all six lighthouse floors and balcony surfaces/furniture from actual
  HGSS references, keeping their IDs, collision, events and connections.
- Textured Ecruteak's directory courtyard. HGSS has an open plot here; no canonical
  building is missing from that plot. See the location checklist and comparisons.
- Fixed old Surf saves displaced by the new port body: relocate to safe dry floor
  as walking Joe. Actual old water Surf remains unchanged.
- Fixed two port-landing layer cells that hid Joe's torso/legs. The building art,
  solid footprint and two opening leaves remain intact.

## Verification boundary

Build3 compiles: payload30,322,400 bytes; EWRAM226,448; IWRAM28,392.
ROM SHA256: `af59dff1b06b99a9599c6f98b6fb6bd1e765cc52c0838a2dec5c79a6c1f88373`.
Fresh exact-ROM automated emulator lanes are in progress at this source checkpoint.
Build1 Surf-state failure and Build2 portal visibility/partial suites remain
explicit diagnostics. Do not treat their partial results as final-ROM passes.
No private batteries or states are included in source or delivery.

## Delta review

Back up your battery save. Import a COPY into this build and use normal Continue,
not an older save state. Test Joe's port landing and both entrance leaves; proceed
through the terminal and quay, board through both gangway halves, inspect all eight
cabins and both lower-deck stairs, rest in the berth and return to Olivine. Visit
all lighthouse floors, lift, window/balcony route and both city services. Save,
restart and Continue. Inspect furniture, Joe overlap, doors, water and land edges.

Sailings remain separately unfinished: Vermilion and approved Black Ledger travel,
quest/progression and reward rules do not exist. The docked ship is explorable;
this pass does not fake a destination or import HGSS's plot.
