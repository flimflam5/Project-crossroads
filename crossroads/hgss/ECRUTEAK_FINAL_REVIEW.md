# Ecruteak completion and reference review

The city contains all ten canonical enterable destinations and all27 native
city/interior/landmark maps. The accepted exterior and custom Ghost Gym remain.
Final gate-layer repair is implemented; **the frozen BUILD11 ROM passes all
source/build/local static and automated controller/pixel regression checks.**
Owner Delta/visual acceptance remains pending. This document makes no100% or
pixel-identical HGSS claim.

## Inventory and reference coverage

The per-building/per-floor inventory is
[ecruteak-qa09-building-checklist.json](ecruteak-qa09-building-checklist.json).
Actual raster URLs, hashes, dimensions and source-data provenance are in
[ecruteak-qa09-raster-references.json](ecruteak-qa09-raster-references.json).
HGSS screenshots are documentary references, never imported ROM textures.

| Destination | Implemented contents and reference comparison |
| --- | --- |
| City | Accepted street plan, source building placement, two enterable homes, three genuinely closed house façades, custom Ghost Gym, services and all three road approaches. Source city events075_T27 distinguish the closed façades from missing interiors. |
| Southwest home; Dowsing home | Actual matrix0066 kitchen, rear-center window, rear-right bookcase, table and four stools. Both intended interiors exist. Ecruteak0066 has no rear plant; Olivine0097 differs and is not copied over it. |
| Theater | Both stage stairways, five performers/show, source13-seat audience, gold crest/red lanterns, brown stage, green checker audience and purple cushions from actual finalHGSS references. Southern doorway/margins lack a complete raster view; their geometry is verified against source events/permissions and actual movement. |
| Gym and Arena | Two stable map IDs reproduce the tall source bridge/path/fall layout, with safe returns and retained optional Morty/student practice battles. |
| Center1F | Nurse, PC, stairs, three plants, warm native source palette, blue rear panels and original green floor emblem. All three service fronts have working counter behavior. |
| CenterB1F | Full source public floor through row12, three distinct blue booths and staff, glass waiting table, ten stools, two plants, terminal and rear panels. Native height14 restores previously cropped public floor without moving old stairs/actors or changing IDs. |
| Mart | Accepted shop service/stock; all three plants, rear merchandise, western counter, southern glass display/four stools and right wall rack. Each source prop has an explicit native counterpart. |
| Barrier Station and Corridor | Two tatami alcoves, three monks, public stairs and long return corridor, leading to Bellchime. |
| Bellchime Trail | Source path/terrain/entrances, autumn planting and tower approach; source footprint shifted four cells south to fit the existing tall2D tower. |
| Bell Tower1F–10F and roof | All11 maps, source public paths/joists, stairs, jumps, warp pads, central structures, nine original lamp fixtures and roof access. |
| Burned Tower1F/B1F | Both floors, source stair/shaft layout and original collapsed-shaft artwork. |
| West/East road gates | Source matrix0070/areaData63 counters, window wall and four corner plants; three-wide aisle aliases and outside return anchors; accepted green-roof façades retained. Layer repair described below. |

An independent public-bounds review covered all27 Ecruteak maps. It found and
corrected the CenterB1F cropped southern row; no other missing public source
floor or intended enterable building was identified. Exact geometry checks are
complemented by actual controller traversal, rather than inferred from existence
of map files.

## Concrete defects corrected

- Door openings retain all visible walkable segments and reciprocal arrivals;
  source IDs, saved positions, starter data and accepted travel are preserved.
- Houses have their actual kitchen/window/bookcase layout instead of a wrongly
  placed television. Exactly13 source Theater seats replace duplicated tables;
  the front aisle is open and seating no longer extends into walls.
- CenterB1F includes the actual bottom public floor and full source furnishings.
  Its waiting table replaces an incorrect mirror stand-in. Six service-front
  metatiles in the two Center floors gain the exact required counter behavior,
  allowing the player to speak to all six staff members from the public front.
- Center and Mart source furniture instances have explicit native footprints.
  Four new source stool footprints in each affected room become solid as a
  documented GBA furniture decision; this is not a measured claim about HGSS
  runtime collision.
- Theater stage/audience, tower lamps/shaft and gate furnishings now use private
  original GBA-compatible resources. Shared Temple/Center/Shop resources and
  unrelated cities remain immutable.
- Tree trunks and wall bodies block movement; intentional canopy/roof overhangs
  retain foreground behavior. Stray-arrow road behavior is neutralized only in
  the precisely contracted scrolling-buffer cells.

### Gate foreground/garbage defect: reproduced before repair

Actual normal-controller BUILD10 tests reproduced a rendering bug in both gates:
600 exact magenta debug pixels at camera(6,6),210 at(6,7), and Joe obscured while
walking onto ordinary floor(2,9)/(10,9). His adjacent control positions showed
all opaque sprite pixels; the faulty cells hid171/192 and147/165 respectively.
Native before frames, four short movement recordings and exact ROM identity are
in [the diagnostic evidence](../qa/qa09/ecruteak/gate-layers-before/README.md).
A correctly matching source renderer had not proved visual quality: its old
criteria accidentally allowed the same garbage as the game. These diagnostic
results are explicitly not a visually accepted release.

The underlying NORMAL-layer metatiles had transparent bottom surfaces and
opaque floor art on the foreground. All50 gate floor cells now draw opaque
bottom/blank top; voids draw opaque black using nonzero private palette index1;
plant overlays have opaque matching wall/floor backgrounds. Four append-only
north-plant art variants distinguish the different wall backgrounds without
renumbering existing art. Exactly four art IDs per gate change; every movement,
elevation, behavior/layer attribute, actor, event, entrance alias and map/layout
ID is preserved. The old140-glyph prefix and shared Temple stay exact.

The source contract is pinned to immutable revision
`7d92f79357b744dddb706bba121d7bd5e6fc4254`. It permits only six existing drawing
metatile changes, four appended variants and ten visible pixel-cell deltas.
Independent all51-city-map validation inspects27,062 composed map/border cells and rejects
debug magenta and missing ground below foreground art. Actual after-repair
normal movement passes on the final delivery bytes: both gates have zero debug
magenta and all192/192 or165/165 opaque Joe pixels visible at the two previously
faulty cells. The four controls are fully visible too. All27 fresh tour frames
also contain zero debug-magenta pixels.

## Necessary adaptations and preserved design boundaries

- Flat16px GBA art replaces DS perspective/models and simplifies shadows/height;
  source relative geography, public floors and doorway positions remain the
  reference. This is an adaptation, not a claim of literal visual identity.
- The custom Ghost Gym is an owner-supplied Black Ledger addition. The Gym's
  tall source room uses two existing maps and scripted safe falls; optional
  practice battles remain. Badge/story order and candle progression are not
  invented during this map pass.
- Center rear service decks are flattened. DS network services are explicitly
  offline; their staff/furniture/public floor are present. Ordinary rooms and
  doors are not replaced with unavailable-service signs.
- The80×64 original green Center emblem is projected onto the source nurse/door
  axis; source-blue B1F booths use original GBA art. The Theater's original stage,
  checker floor and cushions follow inspected HGSS appearances without ripping
  source pixels.
- Three-row gate tunnels and outside return anchors fit accepted flat façades
  and the stable city/Route42 seam. Unrelated neighbouring route art is retained.
- Existing story decisions, optional battles and services remain. No legendary
  event, canonical item reward, Bill/Rocket plot, badge reward or new encounter
  is invented to fill an otherwise completed location.

## Verification and delivery status

Historical V7/V9 reports and recordings retain their own exact ROM identities.
V9 completed all27 controller maps, detailed services/save tests,43 furniture
cases and ground regression, but subsequent visual review found the gate defect.
BUILD10 completed the27-map tour; its next suite was deliberately interrupted
when the gate defect was confirmed. Unstarted/interrupted suites are not passes.

Final source is `489c404346f572aefb6856b3dd48a9b364a08ceb`; ROM SHA256
`df69e014e706168c56180828487a9ab12709a9bccd3dff063fee5f7af5d4f2f4`.
The source compiled successfully, with payload30,261,028bytes, EWRAM226,448bytes
and IWRAM28,392bytes. All60 local CI regression commands passed on that source
and ROM. A workflow start is not claimed as a completed remote test.

Fresh automated controller gameplay on these exact frozen bytes passed:

- All27 maps,308 transitions,73 round-trip pairs and296 actual warp trials.
  All27 unmodified native240×160 frames and all27 full static source layouts
  were visually reviewed; an independent agent also reviewed the native frames.
- All six actual service-counter A interactions and correct NPCs, real Mart
  purchase, PC/party/box integrity, nurse/heal ID and five-performer show.
- Four normal Save/fresh-core Continue cases: Center1F, restored B1F public
  row12, home and explicit old shared-layout fixture. Restored B1F walking away
  and stairs both ways pass. Both Gym falls and actual Morty loss/whiteout
  return safely to the local Center.
- 43 controller furniture cases, covering all13 cushions, front aisle, houses,
  source plants and restored basement furniture. Actual compiled stage6144/6144,
  audience3584/3584, emblem5120/5120 and gate3072/3072 pixels per gate match.
  Normal continuous movement across all20 logo cells was recorded; every native
  Joe frame was visually inspected and he remains visible.
- Focused8-case gate layer regression: both original faulty floor cells in both
  gates now show every opaque Joe pixel; all four camera views show zero magenta.
  Four native before/after recordings preserve the reproduced old defect.
- 19 recorded ground/clipping cases,36 actual trunk approaches, zero stray-arrow
  samples and423/423 expected foreground leaf pixels. Intentional canopy overlap
  remains while trunks/wall bodies block normal movement.

These are automated emulator gameplay and source/pixel checks, not manual owner
Delta acceptance. Test fixtures use copies of historical battery data, temporary
RAM-only survey/encounter controls and explicit1HP/old-layout cases. No player
coordinate/map/warp writes substitute for movement. The original battery remains
SHA256 `b03ff1ef488fbd25de016e828483bc3001787b84e450a45eaa0ac12a11de30ab`.
The owner's latest private Delta save was not supplied and has not been touched.

Public final frames, short movement recordings, source comparisons, exact
identity and sanitized results are in
[the BUILD11 evidence folder](../qa/qa09/ecruteak/v11/README.md). Black around some
arrival frames is the ordinary camera view past a nearby room boundary, after
180 settled frames; centered contextual service/furniture views are separately
provided. Static full-map views are labelled static and contain no actors.

No known reproduced Ecruteak gameplay/rendering defect remains after these
checks. Owner visual/Delta review is pending. The Theater southern threshold's
exact DS appearance is the remaining raster-reference limitation; source
events/permissions and runtime verify its geometry, not literal pixel identity.
Unapproved story, network services, badges, legendary events and rewards remain
explicit design boundaries rather than invented map-completion content.
