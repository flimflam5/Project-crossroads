# Union Cave: paired emulator visual checks

Baseline ROM SHA-256: `a320fc5947e7b207e5d496008e3593ef68a403fd5dbba7e73fd2830ccc4539d5`  
Candidate source: `04f88ee948c26c8da06d239b8203453147c171d1`  
Candidate ROM SHA-256: `07f2a10ca19e3eb585c1114ce656caa2475f4de487a4d416dc5bef461a2627a5`  
Candidate ELF SHA-256: `ce32b5ba4d016bbb62054c4f97ac40630d461f58a693b4ae96f168eb7c6de92f`

Both sets are native 240×160 captures from scripted normal-controller play on copied QA10 battery data. Encounter checks were disabled in emulator RAM and Surf survey was enabled through the real in-game desk; no fixture, save, snapshot, ROM or memory dump is included.

- `ladder-pocket.png`: 1F (7,27), the owner-reported black square at (5,31); `ladder-pocket-south.png` gives the adjacent viewpoint.
- `two-tile-shelf.png`: 1F (23,69), the enclosed hole at (21,67)–(22,67).
- `eastern-edge.png`: 1F (28,57), the three pictured edge notches at (31,56),(31,57),(31,59). Large exterior negative space remains black, consistent with the reference.
- `ladder-basement-arrival.png`: 1F index 0 ladder into B1F, followed by actual return. `shore-before-surf.png` and `surf-entry.png` show actual Survey Surf entry.
- `arrow-{1,2,6,7}-threshold.png` and after clips show four real south-facing exit thresholds and their animations. Each destination was entered and returned from. Sprite-memory samples establish that visible arrows occurred on south-facing 0x65 exit tiles; they do not establish the owner's visual preference for the cue.

Both `coverage.json` files summarize the scoped runs. The screenshots are representative, not proof of every cave cell or save. The source-to-ROM generator and old-save checks are separate; Delta review and visual acceptance remain with the owner. The other cave floors and broader region remain in progress.
