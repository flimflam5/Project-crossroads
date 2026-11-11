# Ecruteak QA09 reference and completion review

This reviews all 27 Ecruteak maps against actual HGSS sources.

**Current delivery candidate: V8 source implemented; combined build and fresh
controller/visual tests pending.** V7 tests below belong only to ROM
`0734501b031d05156a28e685dc1c2748153cb065222bd67b0d2e7cea47fefbca`.
Later fidelity corrections must pass on their own final ROM. Owner acceptance
remains pending.
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

The final combined QA09 ROM has now passed the fresh controller checks below.
Native B2 and BUILD5 frames remain historical evidence; final delivery tests and
new captures are separately identified by the BUILD7 ROM checksum.

Further targeted reference searches found actual final HGSS Theater stage
screenshots on Pokébip/Poképédia and the complete common HGSS road-gate interior
on Bulbagarden Archives. The common gate matches Ecruteak's matrix0070,
areaData63 and moveModel15, independently checked in the original headers.
The whole audience-room Theater mosaic is still unavailable; its 13 seats and
walkable geometry remain pinned to actual source model/permission coordinates.
Anime, prerelease and modified ROM-hack images were rejected as game authority.
The original phone green-roof position remains unmatched; independently tested
gate/door/wall cases are identified by their actual coordinates rather than
claimed as an exact historical screenshot reproduction.

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


## Historical controller checkpoint: BUILD7

The last tested V7 Emerald ROM is SHA256
`0734501b031d05156a28e685dc1c2748153cb065222bd67b0d2e7cea47fefbca`.
The root agent built this binary successfully. This review agent ran the following
mGBA controller tests on that frozen ROM; none of these tests was a static
connectivity simulation:

- Full 27-map city/interior/landmark tour: 308 executed transitions, 73 explicit
  round-trip pairs and 296 warp trials. Bell Tower floors, warp pads, Burned
  Tower stairs, both road gates, Station/corridor and Trail were traversed.
- Detailed gameplay: all five Theater performers return correctly; Mart Buy and
  a real 200-money Poké Ball purchase work; the PC menu returns without changing
  party or box data; nurse healing and the local respawn work. Both Gym falls
  return safely, and an actual Morty practice loss returns to the local Center.
- Normal in-game Save followed by a fresh core/title/Continue passes in both a
  house and the Center. A separate old shared-layout save fixture also passes
  normal save/cold Continue. The original copied battery was not modified.
- Furniture: 26 controller trials pass, including each of the 13 source benches,
  the open front aisle, both kitchens/bookcases and the three reachable Center
  plant faces. Six native-resolution movement MP4s accompany before/after PNGs.
- Ground/clipping: 19 recorded normal-controller cases, 36 tree-trunk approaches
  and zero stray-arrow samples. All 423 expected foreground-leaf pixels match.
  The immutable QA07 checks still pass; the precise approved furniture deltas
  are applied without relaxing other source assertions.

Evidence directories are `build/qa09-ecruteak-tour-v7`,
`build/qa09-ecruteak-details-v7`, `build/qa09-ecruteak-furniture-v7` and
`build/qa09-ecruteak-ground-v7`. All 27 final native 240×160 tour frames were
visually inspected, along with focused Theater, house and canopy frames. The
controller harness uses copied normal battery data, temporary RAM-only survey
access and encounter suppression. Detailed healing/loss tests explicitly set a
copied party member to 1 HP; the legacy-layout test deliberately injects that
fixture layout ID. These are disclosed fixtures, not owner-save testing.

An attempted warm-snapshot shortcut failed its survey-access precondition before
any focused trial: the saved RAM flag was already on and the survey interaction
turned it off. Its logs remain in the `*-v7-resume-fixture` directories. The
shortcut was removed, and the final focused tests above passed from a fresh cold
Continue. No collision or map assertion was removed to obtain a pass.

These are successful automated controller gameplay tests and a native-frame
review. They do not grant the owner's Delta acceptance, establish a pixel-exact
HGSS claim, supply the still-missing complete Theater audience raster, or identify
the original unmatched green-roof phone position. No new unresolved Ecruteak
gameplay defect was found in these final tests. Other agents' doorway/field-action
checks and the final delivery manifest provide their own exact-ROM evidence.


## V8 fidelity corrections discovered by the full reference audit

These source changes are **not covered by the earlier V7 passes**:

- Theater: actual stage captures revealed a missing gold crest/red lantern
  backdrop, wooden stage floor and front rope. Original GBA drawings now use a
  private secondary pool. Exactly 69 stage cells change visually; all 266 room
  physics cells and all 197 other visible cells remain exact against immutable
  source commit `3f935d5e8600c5a280b9172b555edb35ca52b6c0`. The 13 source benches,
  performers, show, entrances and IDs remain.
- Road gates: actual common HGSS art revealed four missing potted plants and
  incorrect generic temple walls/counters. Both interiors now use source-position
  plants, blue-gray counters, a window wall and diamond flooring. Exact migration
  contracts retain all gate physics, actors, aliases and accepted exterior art.
- Center 1F: the actual reference is warm yellow/cream, so the warm palette is
  retained. A private original green floor emblem and blue rear service panels
  restore recognizable source details without changing movement or services. The
  emblem is flattened onto the exact native floor and stored only in bottom
  glyphs, with a blank top layer so it cannot mask Joe.
  The source emblem is adapted to an 80×64 GBA floor composition, centered on
  the nurse/door axis; this is an art projection, not a newly invented feature.
- Center B1F: source row12 had been incorrectly cropped by h12. The same map and
  layout IDs now have h14, retaining all previous positions and the escalator.
  The restored row contains two source plants and six stools; the left waiting
  area has its actual glass table/four stools, and the right communication
  terminal, two rear blue panels and three distinct blue reception booths are present.
  Booth side/front cells keep their old collision and layer attributes; staff
  center/head floor remains unchanged. A private cool-blue palette
  matches the actual basement. Four new stool footprints become solid as an
  explicit GBA furniture choice, not a claimed measurement of HGSS runtime
  model collision. Shared Center assets stay unchanged.
- Mart: three source plants, the southern glass display/stools and eastern wall
  rack are now individually represented in private native artwork. Accepted
  stock, services, doorway aliases and save identities remain.

All Center source instances, including composite reception modules and explicit
DS network-service adaptations, are listed in
[ecruteak-service-prop-coverage-qa09.json](ecruteak-service-prop-coverage-qa09.json).
The independent region audit checks public source extents rather than relying
on one arrival screenshot. No ordinary accessible house or tower floor is being
replaced with an offline-service explanation: that adaptation applies only to
DS communications functions.

Public V7 regression evidence is curated under
[../qa/qa09/ecruteak/v7](../qa/qa09/ecruteak/v7/README.md): all27 native viewports,
25 movement clips, service screenshots and sanitized controller results. It
contains no ROM, battery saves or emulator snapshots. Static full-map renders
are labelled static, not emulator screenshots. Documentary source references
retain published resolution, URLs and SHA256 values; their pixels are never ROM
assets. Fresh V8 evidence must accompany the final combined delivery.


The final service audit also found that front communications desks used ordinary
behavior0 instead of native `MB_COUNTER`. A distance-two static accessibility
check had not proved front interaction. Six precise private counter centers now
use behavior0x80: 1F(2/6/11,3), B1F(4/8/12,5). Their collision, elevation, layer
and pixels remain unchanged. The final controller suite must press A at each
normal front approach, verify the actual receptionist selected and return control;
this correction is not counted as tested until that suite runs on the delivery
ROM. Other metatile behaviors remain under exact regression contracts.
