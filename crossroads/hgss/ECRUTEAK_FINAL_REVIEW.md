# Ecruteak QA09 reference and completion review

This independently reviews the27-map Ecruteak scope against actual HGSS sources.
The accepted exterior, custom Ghost Gym, stable IDs and B2 doorway fixes remain.
This document does not grant owner acceptance or turn unverified work into100%.

## Building inventory

All ten canonical enterable city destinations are present: Burned Tower, Barrier
Station, southwest home, Dowsing home, Theater, Gym, Center, Mart and both road
gatehouses. Five house facades occur in the HGSS city mosaic but source075_T27
has only two house entrance destinations. The other three are genuinely closed
background homes, not inaccessible replacements for missing intended interiors.
The unused house header in the original engine has no city entrance and is not
evidence of a third accessible canonical house.

The inventory and27 individual map records are in
[ecruteak-qa09-building-checklist.json](ecruteak-qa09-building-checklist.json).
CITY_BUILDING_INVENTORY_QA08.json now corrects the stale west-gate entrancex0 to
actualx6, and removes the obsolete assertion that the gate facades are missing.
Return-only outside anchors are not falsely counted as visible entry doors.

## Actual reference inspections and concrete fixes

Reference image URLs, SHA256 values and cache paths are in
[ecruteak-qa09-raster-references.json](ecruteak-qa09-raster-references.json).
No reference screenshots or HGSS textures are embedded in the ROM.

The two cities do not share one house template. Ecruteak uses matrix0066
(SHA c41931ad02b8576b73929e84389f185d95c04213), whose wide model64 cabinet is
centered9.0,3.5 and has no rear potted plant. Olivine uses matrix0097
(SHA5e28ceacf076da9c4e81fe9376530d4aaa96ba5d): its model66 bookcase is centered
8.0,3.5 and model23 plant9.5,3.5. Keep Ecruteak's cabinet origin8,2; the Olivine
origin7,2 and plant9,2/3 must not be copied into Ecruteak. The actual shared0066
Route30 house screenshot confirms this distinction. A positive semantic
regression now requires the Ecruteak source positions and absence of model23.

- Houses: an actual Route30 Apricorn-house screenshot uses the same0066 matrix
  and areaData25 as both Ecruteak houses, confirmed in the pinned pret headers.
  It shows a rear-left refrigerator/sink/stove, rear-center framed window,
  rear-right bookcase and center-right dining table with four stools. QA09
  replaces the wrong television with the existing bookcase and restores the
  native sink/stove and a centered window. The kitchen uses existing GBA pixels
  converted into the fixed temple palette. These are furniture corrections,
  not newly invented story content or a hardware excuse for the wrong prop.
- Center: the actual common HGSS interior mosaic shares matrix0073 with
  Ecruteak/Olivine. Three source model23 objects are potted plants:15,4 and
  14/15,15. QA09 restores those three plants with native Center tiles.
- Mart: actual common HGSS interior mosaic shares matrix0104. The western
  counter, rear merchandise and stock-island layout are source-derived; native
  shelves/counters replace3D models. Existing inventory and purchasing remain.
- Theater: source model56 occurs at13 actual bench anchors. The former generic
  projector drew wide tables one row below, then the room generator painted
  additional rows over them. This duplicated the audience furniture, blocked
  the front aisle and extended seating into the right wall. QA09 suppresses
  the generic model56 projection and draws exactly13 single-cell benches at
  the source positions. Source front passage8/9,10 is open;6/7,10 remains the
  real partition. The existing five-performer show is retained.
- Station/corridor: actual HGSS1F/B1F full mosaics show the two tatami alcoves,
  three monks, side staircase and long return corridor. The source topology,
  all three monks, staircase and paired outer threshold are implemented.
- Bell1F–10F/roof and Burned1F/B1F: all cached actual source mosaics were reviewed
  alongside the27 native B2 frames. Dedicated source geometry retains the
  central structures, per-floor branching, joists, stairs, jumps and warp pads.
  The10F/roof and Burned basement are present; no floor is replaced by a sign.

## Preserved adaptations and design boundaries

Flat16px metatiles replace DS perspective models. Palette/shadow simplification
and compressed model height are GBA art adaptations; they do not justify a wrong
building footprint or missing door. Three-row horizontal gate tunnels have solid
front walls/ridges and intentional overhanging roofs. The west entry follows
sourcex6,y38, while the east model crosses the stable city/Route42 seam. Source
geography and the owner-liked city plan remain; GateBuffer primary sharing keeps
neighbouring route/farm graphics intact.

Center's upper reception is flattened into a connected GBA service deck. DS
internet desks are ambient offline reception; nurse, PC, Mart and stairs are the
working local services. The native floor motif differs from HGSS's large logo.
The tall Gym bridge uses the two existing map IDs; source path/fall topology is
retained with safe returns, optional practice battles and no badge/story gate.
Bellchime's four-tile southern allowance fits the tall flat tower. Original3D
railings, interior walls and furniture use original/native GBA art. Unapproved
legendary events, canonical rewards, Bill/Team Rocket plots and Gym badge
progression are intentionally outside this map milestone.

## Verification and remaining requirements

Historical B2 evidence is exact-ROM controller gameplay, not just connectivity:
27maps,308transitions,73round-trip pairs,161 executed doorway approaches and13
physically unavailable lateral cases explicitly skipped. It includes services,
Gym falls/whiteout, normal Save/cold Continue, Joe actions and all three starters.

QA09 source checks run by this review agent:

- validate_theater_seating.py: exactly13 source anchors, no duplicate furniture,
  source front aisle open and no seating over the room wall — PASS.
- validate_ecruteak_furniture.py: source house furniture/three Center plants and
  every historical temple graphic/metatile unchanged — PASS.
- hgss_room_validation.py and hgss_service_validation.py: actors, function paths,
  performance lanes and every-public-tile escape — PASS.
- Temple/room/service generator --check — PASS.

The temple adds resources at the end:488→507 graphics and383→392 metatiles;
historical resource IDs and pixels are unchanged. Exact migration contracts list
53 Theater cells,12 cells in each house and6 Center cells. Tests must require
those precise deltas and retain all unrelated immutable assertions.

The final combined QA09 ROM still needs the root agent's fresh build and actual
controller tests of these changed rooms. This review agent did not build or run
an emulator. Native B2 frames are historical evidence, not new QA09 captures.

Separate complete actual HGSS raster references for Theater and route gate interiors remain unavailable. The candidate PeakD Theater image could not be
downloaded (403); an Archives image with a similar name was inspected and rejected
because it depicts the anime. Modified ROM-hack maps, GenerationII interiors and
prerelease images were not substituted as authoritative final HGSS references.
The source matrix/permission/prop/warp facts for these rooms remain available and
checked. These gaps and the original unmatched green-roof phone report must stay
explicit, alongside owner Delta visual acceptance. No missing canonical accessible
Ecruteak destination was found; this is not a claim of pixel-identical HGSS art.

## Controller checkpoint after BUILD5

On ROM SHA256c2f30ef04d3890e9ac947ee1f6f28a04b7e6e2d08c1a7f5e77a68fc7c697f658:
26 actual controller furniture trials pass, including all13 source benches, the
reopened front aisle, both houses and all three exposed Center plant faces. Six
240x160 movement MP4s and before/after PNGs are in
build/qa09-ecruteak-furniture-v5. Native room frames were visually inspected.

The initial BUILD4 trial stopped when the test requested14,16, a source-blocked
Center riser. Its logs/partial frames are preserved as BUILD4-interrupted; it is
not a gameplay pass. The corrected trial tests14,15 from the reachable western
face13,15, and the enclosed second plant's exposed upper face from15,13. No
architecture was opened and no collision assertion was removed.

BUILD5 also passed19 recorded ground/facade/tree cases,36 trunk approaches and
zero stray-arrow samples. All423 expected foreground-leaf pixels match exactly;
the immutable QA07 validator also passes. Reports/clips are in
build/qa09-ecruteak-ground-v5. These are BUILD5 results, not claims about the later
Olivine boardwalk correction or its forthcoming final ROM.

A later actual HGSS CenterB1F mosaic was acquired from Pokewiki and inspected.
It confirms three northern reception desks, western waiting area and eastern
stairs. Sourceblue floor/counters become the existing warm GBA service palette,
and the large floor logo differs; these are documented art substitutions rather
than hardware requirements or claims of literal visual identity. This removes
CenterB1F from the missing-raster list.

The same BUILD5 ROM subsequently passed the full27-map controller tour:
308transitions,73explicit round-trip pairs and296 warp trials, plus actual nurse
healing/local respawn and retained starter/party. All27 fresh native frames were
inspected. Coverage/screenshots: build/qa09-ecruteak-tour-v5. Later final binaries
remain separate and must carry their own actual test identity.
