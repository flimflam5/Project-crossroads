# QA10 B3 city functional checkpoint — visual defect still open

Exact ROM SHA256: `af59dff1b06b99a9599c6f98b6fb6bd1e765cc52c0838a2dec5c79a6c1f88373`.
Game source: `e7e2c085a5a61ef727d06f9f682af7d3a954cc06`.

[Native screenshots/recordings](gallery.html), [exact results](results.json),
[artifact checksums](evidence-manifest.json), [phase exits](serial-completion.json)
and [launcher/repository mapping](runner-mapping.json).

All six serial **functional** stages passed using copied normal batteries and
normal controller movement on these bytes. The6F inner optical-core rendering
is still wrong:26 cells use outer-glass panels and two enclosure segments are
void; a separate28-cell art correction is pending. Pink floor/cyan cap are
recognizable, but6F is not reference-matched. This is not owner Delta acceptance,
not final visual completion and not verification of a future corrected binary.

## Actual completed checks

- All eight lighthouse maps toured through real connections, floors and returns.
-199 dry wall/tree bumps across12 land buildings/3 trees, plus24 **separate actual
  native Surf** terminal-body bumps, all four sides/all eight closed rear bases.
- Both north portal arrivals23/24,52 and next landings23/24,51 show192/192 opaque
  Joe pixels in the composed framebuffer; correct north facing and walk-away.
-59 material cases:12 cleared table cells,43 fence approaches and four boulder
  groups;37 physically unavailable fence starts are explicitly excluded. Native
  Surf and actual north-pier disembark replace the now-solid old south apron.
- Six real front-counter interactions require exact displayed text and controls.
-12 normal lighthouse menu Save/cold Continue cases, including both3F/4F source
  components, balcony/cabin and both selected cabin destinations; five special
  journeys cover the actual window return and both lift leaves for both floors.
-39 actual court cells with full composed Joe visibility, four exact directory
  messages and normal Save/cold Continue with walking away. The source court is
  canonically vacant; no invented building replaces its directory sign.

## Fixtures, source guards and reproducibility

Every stage checked exact ROM/ELF plus original/copied battery hashes before and
after. Collision/material/focused-detail dry phases require actual Survey OFF;
the water phases enable it through the public desk, use native Surf and end
with normal disembark/OFF. The generic tour/counter harness enables RAM-only
Survey through the public desk; that setup is disclosed separately rather than
falsely described as OFF.
The shared harness suppresses random encounters only in private test RAM. These
focused helpers do not seed player/map/warp/party/box/bag/flag coordinates.
Normal Save/cold Continue uses private output batteries and compares party,
boxes, decoded inventory/currency, starter and flag state. The owner's newest
private save was not supplied; source copies and prior separate compatibility
fixtures are not claimed to be that user's actual file. No battery, state, ROM,
ELF, raw video-frame directory or memory dump is included here.

The first failed B3 collision expectation assumed an animated-door automatic
exit step. Actual metadata0x61 preserves the exact destination23/24,52. The
corrected contract now checks that exact arrival AND full Joe body pixels there
and on the following51 landing. No game assertion was waived. A B2 materials
fixture had enumerated city water starts while still inside HarborOffice after
the new real desk toggle; it now returns normally to the city first. Original
12table/43fence/4rock assertions remain. Failed/partial earlier outputs remain
ignored diagnostics; no unstarted stage is represented as passed.

Lighthouse/court launchers only delegated to the versioned repository runners;
all exact wrapper, runner and helper hashes and original commands are preserved.
Use `results.json`'s direct repository commands for reproduction: no/tmp launcher
is required. Supply a COPY of a normal battery and the exact ROM checksum. The
existing native bridge can be built with the project's documented command:

```sh
cc -shared -fPIC crossroads/tools/mgba_bridge.c -lmgba -o /tmp/johto-bridge.so
```

The executed source copies under `executed-runners/` preserve this checkpoint;
the normal repository tools are authoritative for later revisions. Full native
240x160 PNGs are unmodified. MP4 files are H264/yuv420p at240x160. These scripted
emulator checks and independent reference/image review remain separate from
owner visual acceptance. See the final corrected build's separate evidence.
