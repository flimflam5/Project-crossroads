# Actual gate layer repair: BUILD11

Source `489c404346f572aefb6856b3dd48a9b364a08ceb`, ROM SHA256 `df69e014e706168c56180828487a9ab12709a9bccd3dff063fee5f7af5d4f2f4`. Native framebuffers are240×160; before/after comparison panels place those images side by side without rescaling. MP4s record normal controller movement. No map/player/warp coordinate writes occur.

Both gates now have zero magenta debug pixels at both camera positions. Normal movement onto(2,9) leaves192/192 Joe opaque pixels visible; movement onto(10,9) leaves165/165 visible. Adjacent controls are fully visible too. The same BUILD10 inputs hid171 and147 pixels respectively. All8 focused cases pass.

The pixel visibility assertion independently reads actual current OAM, OBJ VRAM and palettes, then compares every opaque Joe pixel to the actual framebuffer. This complements source collision/layer checks and the51-map composed-background regression; those checks alone were insufficient to prove the old renderer looked correct.

The source contract preserves all physicalbits/attributes/events/warps and existingIDs, permitting only4 north-plant art variants per gate for correct wall backgrounds. Floor drawings are opaqueBOTTOM/blankTOP; plant overlays retain natural overlap over opaque matching backgrounds.

Owner Delta/visual acceptance remains pending. No private saves, snapshots or ROMs are included.
