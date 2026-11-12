# Build 5 — actual old saves and full portal visibility

Source `cc643ffe711204f3ef38e34e7aa1eb8c9558720f`.
ROM SHA-256 `ee2d81d5d0b55b7f1f9d36d1c9b055700164da439f51af7a66b5fb2d2147f90b`.

**Emulator PASS:** genuine old walking (23,53) and Surf (23,55) normal battery
saves cold-Continue to safe dry (23,51), naturally restore Joe walking, walk away
to (23,50), and pass new native Save / fresh-core Continue. Actual walking
OBJ graphics and VRAM match Joe. Party, boxes, starter, flags and decoded
inventory remain exact. The test writes no avatar, map or position state.

The valid historical Surf save at water (19,47) keeps Surf, moves normally to
(19,48), and Saves / cold-Continues while retaining Joe Surf graphics. Every
private input battery remains hash-identical. The targeted migration therefore
does not force valid water saves into walking.

The continuous controller recording approaches and enters both visible terminal
leaves, walks away inside, exits both leaves and walks north. All six native
approach / exit / landing views retain every opaque Joe pixel: 187/187 at
south-facing approaches and 192/192 at north-facing exits and landings. This
uses actual hardware OAM, OBJ VRAM, palette and framebuffer checks, not a source
renderer. There are no exact debug-magenta pixels.

Images and video are native 240×160; MP4 uses H.264/yuv420p. No private battery,
snapshot, numbered frame cache, ROM, ELF or memory dump is exported. This is a
specific emulator regression; the separate all-width door suite and owner Delta
visual review remain distinct requirements.
