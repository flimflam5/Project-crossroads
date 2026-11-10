# Black Ledger — preliminary QA 02: Ecruteak access repair

Owner reports that the city looks very good, with boundaries and entrances still
requiring correction. This records positive exterior feedback, not full acceptance.

## Corrected source and generated data

- Ecruteak/adjacent Route 37, 38 and 42 scrolling buffers: replace General 0x114
  (a ledge edge, responsible for repeated horizontal dirt stripes) with neutral
  General 0x024 ground. Shared tilesets and approved encounters are untouched.
- Ecruteak and Bellchime trees: use the correct native two-row assembly, ending
  in 0x1dc/0x1dd, rather than appending a repeated third canopy row. Update graphics reservations and buffer mapping.
- Mart visible left-hand door: move warp 6 from (54,45) to (53,45) and correct
  the facade door column. The building stays in place. This is a one-tile GBA
  projection deviation from the canonical HGSS event position, documented here.
- Barrier Station: both visible door leaves now operate. Original warp 1 stays;
  append alias warp 7 at (39,25), sharing its destination. Return still uses warp1.
- Ecruteak perimeter: solid outer boundary except its three road apertures:
  west y37–39, east y46–48, south x38–40. Existing connection IDs/offsets stay.

All map/layout/save/heal IDs stay stable. No new story, encounters or trainers.
The station and other interiors remain provisional; this is not a full room pass.

## Validator changes

Retain every original warp/script identity and destination comparison, normalizing
only allowed coordinate changes. Require exactly one appended station alias with
its precise destination. Add explicit perimeter-aperture assertions. Existing
whole-map reachability and old-save safety checks remain. No visual acceptance
is inferred from these checks. Generator checks must remain deterministic.

## Delta retest

Back up your battery save; use normal Continue, not an old emulator save state.
Check the east-city road for stripes; approach trees from all four sides; enter
Mart through the visible door; enter Station through either door leaf and return.
Test Route38/42/37 borders both ways, every city doorway, then normal save/reset/
Continue in Ecruteak and Station. Confirm Joe, party, starter and inventory remain.
Screenshot any remaining bad entrance and specify the approach direction.
Full region reconstruction, interiors and remaining clipping audits stay open.

## Verification performed

Fresh Emerald build PASS; ROM used29,539,856bytes (padded32MiB). Existing opening,
Olivine, western Johto, area completion, visual-repair/save-contract and whole
network validators PASS; built-map inclusion and generator reproducibility PASS.
Actual old-battery Continue plus six target maps/67 controller transitions PASS,
including city doors, station alias, regional borders and return chain; retained
starter/party checks PASS. Representative tree trunk blocked all four controller
approaches; native screenshots inspected. Encounters suppressed only inside test
process and survey water helper enabled only in RAM, as in the existing harness.
No fresh all-starter, whiteout or normal new Save/Continue suite in this narrow
repair pass. Owner Delta visual/collision retest remains pending.
