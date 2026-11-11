# Known gate-layer defects reproduced before repair

Diagnostic BUILD10, source `7d92f79357b744dddb706bba121d7bd5e6fc4254`, ROM SHA256 `3bec0fedbb481cc051c38d719499b584e9a4c219e42b66bef298f6aa0c5ec7a9`. These are native 240×160 emulator framebuffers and normal-controller movement recordings. **This build is not a visually accepted release.**

Both road gates expose 600 magenta debug pixels at camera position (6,6), and 210 at (6,7). Walking normally onto floor (2,9) hides 171 of Joe’s 192 opaque sprite pixels; walking onto (10,9) hides 147 of165. The adjacent control positions show every opaque Joe pixel. The test reads current hardware OAM, OBJ VRAM and palettes to predict Joe’s actual pixels; it does not infer visibility from collision flags.

The defects come from transparent bottom surfaces and opaque foreground floor drawings on NORMAL layer metatiles. The exact before/after regression must reject debug magenta and retain all Joe pixels on ordinary floor.

Tests use a copied old battery save and the disclosed RAM-only survey/encounter fixture. No user save, ROM or emulator snapshot is included. `PASS` in this diagnostic JSON means the reported defect was successfully reproduced, not that the defective game passed QA.
