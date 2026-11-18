# Route 33 candidate — emulator run summary

Source commit `5c308d1fbc66e202ee6da0c4de712079955851b0`; tested ROM SHA-256 `d78f533b7cbc67d69a7eba333bc95595ba14747e1669ee3516b5e0fc070f0faf`. This is an experimental area checkpoint, not a complete Johto build.

Controller-driven mGBA tests passed for a genuine QA10 save originally at Route 33 `(22,7)`, recovery to `(22,8)`, normal movement across the Azalea seam in both directions, entrance and return through Union Cave, 39 sampled solid-boundary approaches, four directional ledge jumps, the existing resident and two signs, and an in-game Save followed by cold Continue. Exact party, boxes, flags, starter and decoded inventory survived the old-save Continue and the new Save/Continue; the original battery was not changed. The harness used a RAM-only wild-encounter suppression fixture and the normal Survey desk interaction.

Independent tests matched the actual candidate ROM to source for 56 map-used metatiles and attributes, all 16 secondary palette banks, and the shared Azalea seam metatile and palette. They also checked 103 live secondary graphics in VRAM and live palette banks 6, 7 and 8. Primary animation graphics were outside the static VRAM check.

Joe's saved arrival was on native short grass: five of 192 sprite pixels on the bottom two rows were masked by grass. After walking onto ordinary ground, all 183 opaque sprite pixels were visible. The grass-specific check requires behavior `0x07`, limits masking to the bottom two rows and does not relax the ordinary-ground check. Ledge checks assert the actual modeled landing rather than treating a normal jump as walking through a wall.

Remaining: the owner has not reviewed the visuals in Delta; Heart & Soul geometry is blended and needs continued comparison with HGSS. The area is not represented as an exact HGSS recreation. Collision coverage was sampled, not exhaustive, and other old-save positions were modeled statically rather than individually cold-continued. No battle or field-move regression was performed on this Route 33 candidate. Other Johto areas, interiors and transport remain unfinished or unverified. The prototype has not been published as a release.
