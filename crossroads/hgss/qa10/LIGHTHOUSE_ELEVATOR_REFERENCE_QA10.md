# Lighthouse elevator — focused reference follow-up

**A separate HGSS cabin and its ride mechanics are verified. Its independent
visual raster was not located in this focused search.** Current GBA cabin decor
must remain labelled original/native adaptation, not HGSS-reference matched.
No game inputs, generator outputs, ROM or emulator were changed by this audit.

## Actual HGSS room and mechanics

Pinned pret reference commit
`6bf138d6035aa6b43d6f8f4132a12df70f86dcec` defines
`MAP_OLIVINE_LIGHTHOUSE_ELEVATOR` as an interior with areaData 44, moveModelBank 15,
camera 4, matrix 0262_D31R0202 / terrain chunk 372 and event 401_D27R0108. It is a
separate room, not simply a menu or animation rendered on Lighthouse 1F/6F.

Actual source floor permissions contain 20 reachable cells: x1–5 / y3–6. The
minimal origin-preserving crop is 7×8 within a 1×1 / 32×32 source matrix. There are
no NPC actors and one dynamic exit at (3,6), with header 4095 / anchor 256. Source
prop anchors are model 1 at (3.5,6.5625) and model 208 at (16,15.875).

The checked source script `scr_seq_0067_D27R0108.s` walks the player north two
steps and faces south. It reads `GetDynamicWarpFloorNo`, selects the **opposite**
1F/light-room destination, displays departure text, calls `ElevatorAnim` with
five-floor travel, then displays arrival text. There is no two-floor chooser in
this script. Script, message and event Git blob hashes were independently
verified; URLs/hashes and stripped facts are in
[the follow-up manifest](lighthouse-elevator-reference-followup.json).

The same matrix, area bank, movement bank and camera are used by other HGSS
lifts, including Goldenrod/Celadon stores and the Battle Tower. This confirms
shared base geometry/resource identifiers; it does not replace an actual
location-identified visual reference or prove every script renders identically.

## Deliberate preserved GBA adaptations

The functioning 8×8 Black Ledger cabin remains unchanged in this pass. Its two
floor panels and Yes/No destination choice are a **deliberate functional
adaptation**, not an unavoidable GBA limitation and not a reproduction of the
source automatic ride. Its two visible dynamic exit leaves (3/4,6) are likewise
an explicit native full-width-door choice. Existing accepted lift functionality
and saves are preserved; actual leaf/destination/save results are recorded by the
coordinator's emulator evidence, separately from this source audit.

The present wooden/maritime cabin decoration is original GBA art. No
independently identified HGSS cabin screenshot was recovered here to verify
its materials, furnishing or colors. Do not call that appearance canonical,
pixel matched or visually accepted merely because the ride works.

## What was searched and what remains unknown

The actual Glitter Lighthouse and Goldenrod store layout galleries omit a cabin
map. The WikiDex Faro de Olivo article also supplied no identified cabin image.
Six precise Bulbagarden Archive filename candidates were missing; archive
image-namespace searches for HGSS elevator/Goldenrod elevator returned none.
A broader search found 17 elevator images, but none identified an HGSS cabin.
WikiDex's correct `/api.php` search returned no `ascensor HGSS` image and nine
unrelated results for `ascensor`. The initial wrong `/w/api.php` route returned 404;
that is not treated as blocked access or proof that WikiDex had no results.

`Vista Lighthouse elevator DPPt` is Sinnoh, not Olivine, and was explicitly
excluded. `Battle Tower C Elevator` is Generation II and was also excluded.
These failed focused searches do **not** prove that an HGSS cabin image exists
nowhere; they establish that this audit did not obtain an authoritative visual.
A directly identified HGSS Lighthouse ride capture remains the missing reference.

The old inference that model 208 was an off-room machine safely cropped is also
unverified. Its anchor lies outside the public 7×8 crop, but a 3D prop can extend
far from its anchor. Without model extents or an actual cabin view, that origin
alone does not establish its identity, visibility or safe cropping. No raw model
asset, new NARC or commercial ROM was downloaded to fill this gap.

This is an explicit reference/appearance limitation. It does not justify a
late unreferenced redesign or a new build while the verified ROM is frozen.
Owner visual approval remains pending.
