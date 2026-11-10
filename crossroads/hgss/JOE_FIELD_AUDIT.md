# Joe player-state audit — active Ecruteak completion

The owner's accepted walking/running sheet remains byte-identical. Gender and
save layout are unchanged. Custom 16-bit graphics IDs0x3f04–0x3f0b append beside
existing custom NPC IDs; NUM_OBJ_EVENT_GFX/dynamic IDs never move. Rival/remote
player art is retained. All converted action sheets use Joe's original palette.

| State | Wiring/art | Current verification |
|---|---|---|
| Walking/running/spin | Original owner frames/finite spin loops retained | Existing asset validation; normal emulator traversal |
| Fly/Cut/Strength/Rock Smash/Flash pose | Five new full-body corporate Joe poses | Actual Fly ID and VRAM; all ten flights, normal Save/Continue PASS before final integration |
| Surf/Waterfall boarding | Joe seated four views; authored east art, no mirrored satchel | Actual boarding, four-direction VRAM and return to walking PASS |
| Mach Bike | Joe bike frames, engine timing, authored east | Actual registered-item mount/dismount and VRAM PASS |
| Acro Bike | Joe bike/wheelie frames, engine timing, authored east | Actual mount/wheelie/dismount and VRAM PASS; advanced tricks not all exercised |
| Fishing | Joe rod views; engine's W/N/S four-frame groups + authored east | Actual registered-rod casting on water, VRAM and return to Surf PASS |
| Dive | Joe goggles/flippers views; same frame contract | Wired/packed; normal Dive activation not tested in Johto |
| Watering | Joe can poses, correct paired D/N/W grouping + east | Wired/packed; normal berry watering not yet tested |
| Decoration camera | Original Joe walking pose0 in old16x32 preview | Wired; menu not exercised |
| VS Seeker | Joe field-action state in Emerald; FRLG unchanged | Wired; unavailable/unexercised in current Johto |
| Contest local trainer | Joe normal250 fits existing8-bit field | Wired; no contest playtest |
| Link-room local avatar | Joe normal; remote/rival version art preserved | Wired; no multi-emulator link test |
| Battle/Trainer Card | Existing dedicated Joe front/back/Card retained | Existing validation; actual Morty practice loss/return now passed; no fresh trainer-Card interaction test |

Animation timing/frame bounds are preserved. Several bike/fishing/watering phases
currently reuse their directional pose rather than separate limb/rod drawings;
these are functional identity fixes, not a claim of final animation polish.
Source generated art and conversion tools are versioned. Raw HGSS screenshots
are references only, never game graphics. Tests use copied battery saves; bike/
rod items exist only as private emulator fixtures, not production inventory grants.

A test initially sampled VRAM on the graphics-ID-change frame, before the queued
VBlank DMA. The corrected check waits one frame on a mismatch, then still requires
an exact Joe frame. This is not permission to accept wrong or missing sprites.
