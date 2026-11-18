# Union Cave / Ruins emulator test harnesses

This separately staged, sanitized follow-up preserves the test code used for source revision `00f5742b2cdb48a2256e79e796849dea8f070d1c` and ROM SHA-256 `a320fc5947e7b207e5d496008e3593ef68a403fd5dbba7e73fd2830ccc4539d5`. No ROM, battery saves, baselines, snapshots or personal data are included. The harnesses generate private copies and snapshots: keep output outside the repository and never commit those files.

## Dependencies and limitations

Run from the project root with matching built `pokeemerald.gba` and `pokeemerald.elf` from the same source revision. Required host tools are Python 3, Pillow, `arm-none-eabi-nm`, mGBA 0.10 and its development headers, and `ffmpeg` for movement clips. For example, with mGBA development files installed:

```sh
cc -shared -fPIC crossroads/tools/mgba_bridge.c -lmgba -o /tmp/johto-bridge.so
```

The project scripts `johto_network_smoke.py`, `johto_movement.py` and `hgss_gate_arrivals.py` are also required. Set the runtime linker path if your mGBA library is not on the default system path. These scripts do not include a base ROM or private test battery. They are tailored to this revision's map IDs, collision and expected save migration positions; re-evaluate those expectations for later revisions.

`tour.py` and `border_repeat.py` adapt the existing network planner in memory to admit the engine's elevation-0 transition tiles and use dry walking before enabling Survey access. They require exact source anchors and now fail if those anchors change. They do not rewrite project files. These guarded copies are syntax-checked but were not rerun after adding the guard; the corresponding unguarded versions completed the exact-ROM tests in the companion evidence. The adapted command-line wrappers and configurable paths below were not rerun as a complete 12-save suite. The copied single-save test is the same test logic used in that suite. Portable `compiled_assets.py`, `live_vram.py` and `border_check.py` were re-executed on the exact ROM; the latter two require a snapshot with adjacent `.sha256` identifying the same ROM.

## Run examples

The examples use private paths and require a compatible real old battery. Preserve your original save and use a copy. They assume `ROM_SHA` is set to the actual build hash and that this directory's path is stored in `HARNESS`.

```sh
python3 "$HARNESS/tour.py" --rom-sha256 "$ROM_SHA" --save /private/input.sav --output /private/union-tour --library /tmp/johto-bridge.so
python3 "$HARNESS/border_repeat.py" --rom-sha256 "$ROM_SHA" --save /private/input.sav --output /private/union-borders --library /tmp/johto-bridge.so
python3 "$HARNESS/compiled_assets.py" "$ROM_SHA" /private/compiled-assets.json
MGBA_BRIDGE=/tmp/johto-bridge.so python3 "$HARNESS/live_vram.py" "$ROM_SHA" UnionCave_1F /private/union-tour/UnionCave_1F.snapshot
MGBA_BRIDGE=/tmp/johto-bridge.so python3 "$HARNESS/border_check.py" "$ROM_SHA" UnionCave_3F /private/union-borders/UnionCave_3F.snapshot
```

The 12-case old-save runner accepts a private fixture directory. For each named case in `all_old_positions.py`, it expects `<name>.sav` and `<name>-baseline.json` containing the battery SHA-256, old map and position, party/box/flags/decoded-inventory payload hashes, starter value and last-heal-location bytes. These baselines were measured on the original QA10 ROM and remain private; do not fabricate them or commit them. Pass an independent output directory:

```sh
python3 "$HARNESS/all_old_positions.py" --rom-sha256 "$ROM_SHA" --fixtures /private/qa10-fixtures --output /private/old-save-run --library /tmp/johto-bridge.so
```

The tour and border capture enable Survey access through the actual development desk; the network harness disables random encounters only in test-process RAM. The old-save test disables random encounters and uses normal controller Save/Continue. Some other cross-game tests in the companion checkpoint use temporary RAM gear or skip the opening; see that report. Runtime assertions and examples are sampled emulator tests, not visual acceptance or proof that every save and map works.
