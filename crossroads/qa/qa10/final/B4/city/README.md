# QA10 B4 city evidence

Game source: `df8c4598d88c7770626be4621a5f39cf60dadb95`.
ROM SHA256: `4fb28fe64fc44c0546462a935655346a61f13b644bc3040468146d136cd6d656`.

[Native before/after comparisons](comparisons.html) · [Native images and movement recordings](gallery.html) · [exact results](results.json) ·
[script hashes and reproducible commands](runner-mapping.json) · [checksums](evidence-manifest.json).

All six city suites ran fresh on the frozen B4 candidate ROM, sequentially in one
emulator lane. This is scripted emulator gameplay and independent image review,
separate from source validators, compilation and the owner's Delta acceptance.
No claim that all Olivine or Ecruteak requirements are100% accepted is made.
The overall B4 candidate FAILED a separate intended-facing audit: four Ecruteak
gate links faced south rather than west/east, and one Trail corridor arrival
faced north rather than south. A later B5 correction/retest is pending; these
scoped city passes do not waive or contradict those failures.

## Verified on these bytes

- Eight lighthouse maps,76 real transitions,19 roundtrip edge pairs,73 warp trials.
-199 ordinary dry building/tree bumps and24 separately disclosed native Surf
  port-body bumps, all four sides and all eight closed rear bases; no dry skips.
- Both actual terminal exit leaves arrive at23/24,52, face north and show all192
  opaque Joe pixels. The next landings23/24,51 also show192/192 before walking away.
-59 material cases retain12 table cells,43 fence cases and four boulder groups.
  Thirty-seven physically unavailable fence starts are reported, not passed.
- Six real front-counter conversations require the actual intended NPC/text.
-12 normal lighthouse menu Save/cold Continue cases, five window/lift journeys,
  both destination selections surviving cold Continue and walking away after load.
- Two complete ordinary6F circuits around the optical enclosure, in opposite
  directions and one uninterrupted recording; no XY/map/warp positioning writes.
-39 corrected court cells with full composed Joe visibility, all four directory
  sign approaches and a normal Save/cold Continue followed by walking away.

## Visual findings and adaptations

The6F inner optical housing now reads as cyan and is distinct from the diagonal
outer glass ring. All eight tour images and ten centered contexts were inspected
against seven actual HGSS individual-floor images. The angular2D projection,
flat U core and small northern cap are explicit art adaptations, not literal DS
geometry or an assertion that better artwork is impossible on GBA. The Elevator
cabin has no separately verified HGSS reference. See LIGHTHOUSE_VISUAL_REVIEW.md.
The first two owner screenshots show Ecruteak's canonical open directory court,
not a missing Olivine building; this pass improves its soil/curb art without
inventing a structure or altering its collision, events or saves.

Before images in comparisons/ are explicitly QA09 or B3, while all phase outputs
are fresh B4. The gallery preserves native240x160 images; no paint-over is used.

## Fixtures and limits

ROM/ELF and original/copied battery hashes were checked before and after every
phase. Source battery SHA256 is `b03ff1ef488fbd25de016e828483bc3001787b84e450a45eaa0ac12a11de30ab`.
The owner's newest private save was not supplied; it is not represented as tested.
Normal menu Save/cold Continue writes private output batteries and compares exact
party, boxes, starter, flags, decoded bag and currency. No private saves, snapshots,
ROM/ELF files, dumps or raw frame directories are included in this evidence.

The shared harness suppresses encounters in test RAM and enables RAM-only Survey
assistance via the public desk. Focused dry phases explicitly turn Survey OFF;
water tests turn it ON through the actual desk, use native Surf, disembark and
turn it OFF. Shared generic tour/counter setup assistance is disclosed rather
than mislabelled dry. The corrected port metadata0x61 lands exactly at52 without
an automatic animated-door step; tests verify that exact cell and the following
51 landing rather than waiving visibility. No assertions were weakened.

Reproduce using the versioned commands in runner-mapping.json with a COPY of a
normal battery, the exact ROM checksum and the project native bridge:

```sh
cc -shared -fPIC crossroads/tools/mgba_bridge.c -lmgba -o /tmp/johto-bridge.so
```

The lighthouse test-only runner adds two strict circuits after the frozen game
commit. Its executed SHA and source copy are archived; it does not change game
inputs. Owner visual acceptance and interregional sailing decisions are pending.
