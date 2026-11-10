# Ecruteak QA05 — scope, references and actual verification

This continues QA04's exterior; it does not certify an HGSS1:1 region or owner
visual acceptance. Source SHA/checksum accompanies the delivered build-info.json.
Native evidence and machine-readable counts: ../qa/hgss-qa05/results.json.

## Per-area review

| Area | Reference / implementation | GBA adaptation or remaining work |
|---|---|---|
| Ecruteak City | QA04 facade/street composition retained; all15 current entrance aliases tested | Only the second house door opens in ground data. Three-tile gate aliases use existing road openings; DS perspective/elevation is flattened. Owner visual acceptance pending. |
| Southwest residence | Source house matrix/door; fridge, cabinet, TV, table/chairs and residents | Native original furniture; original neighbor dialogue retained. No new plot. |
| Second / Dowsing house | Same canonical house matrix, its actual city plot/door | Ambient residents; HGSS Dowsing reward/story omitted deliberately. |
| Dance Theater | Source room/stage/seat positions and door; five kimono performers | Original GBA performers/bench art. Existing short show extended to five, no story battle. |
| Pokemon Center1F | Source room dimensions/service positions; nurse, PC, public reception | Flat rear service deck replaces DS vertical reception. Native GBA heal/PC/counter tiles retain engine behavior. Stair landings widened for sideways native escalator arrival. |
| CenterB1F | Source basement/stair/staff coordinates | DS online desks explicitly offline; no DS Wi-Fi support. Bench fills source partition/stair footprint. |
| Mart | Source dimensions/door, stock shelves and clerks | Native shop art/counter behavior; accepted stock unchanged; delivery plot actors omitted. |
| Gym / Gym arena | Source raised bridge ground traced; Morty/student practice scripts retained | Tall DS room split at existing two map IDs. Stepping off returns to entrance. Candles stay lit; no mandatory battle/candle gate or badges. Student moved beside narrow path to keep battle optional. |
| West / East gatehouses | Canonical room dimensions and west/east endpoints | Flat GBA pillars; three ground aliases per road. Existing border IDs/offsets/buffer terrain retained. |
| Barrier Station | Source public floor/tatami/prayer tables and stair coordinates | Guard moved(15,7)->(16,6), off the source's story choke point. No story gate imported. |
| Barrier corridor | Source floor/stair positions | Flat native timber/rails instead of DS camera heights. |
| Bellchime Trail | Canonical permission footprint/bends; autumn grove and broken paving | Whole reference translated south4 tiles for the tall2D tower facade; no relative endpoint change. Native autumn ground/tree texture is an adaptation, not pixel-identical DS foliage. |
| Bell Tower1F | Source floor/props/entrance/stairs; old outside-door alias retained | Original timber/statue/column art; DS coordinates cropped by(4,4), preserving relative geometry. |
| Bell Tower2F | Source floor/stair geometry | Same crop/art adaptation; native ledge behavior where source calls for it. |
| Bell Tower3F | Source branching paths/jumps/stairs | GBA two-tile directional jumps replace DS plank movement. |
| Bell Tower4F | Source branching paths/jumps/stairs | Same native jump adaptation; all stair branches checked. |
| Bell Tower5F | Source branches/jumps/stairs | Old primary up/down warp indices retained through explicit source/native mapping. |
| Bell Tower6F | Source branches/jumps/stairs | Original GBA timber/rails; same relative geometry. |
| Bell Tower7F | Source branches and same-map pads | Native teleport-pad behavior; entry-position-aware test planner required. |
| Bell Tower8F | Source linked pads/stairs | Native pads/wooden structure; no HGSS rewards imported. |
| Bell Tower9F | Source linked pads/stairs | Accepted bell interaction moved to actual rooftop; old saved map ID remains. |
| Bell Tower10F | Source floor/stairs, newly appended missing floor | Native timber/rails, no new story. |
| Bell Tower roof | Source platform/ladder; accepted bell interaction at finial | Flat blue roof/gold finial instead of3D roof/skybox. Native walking ladder, no legendary event. |
| Burned Tower1F | Source charred floor/pit/statues/ladder | Flat GBA lower-floor view instead of DS3D depth; old door alias retained. |
| Burned TowerB1F | Source lower room/ladder/pillar/rubble footprint | No legendary actors or plot imported. |

Source events, public permission grids, props and provenance are recorded in
canonical_events/ecruteak-interior-geometry.json; canonical_events/extraction-selection.json
lists the25 source headers. Raw reference archive/story scripts are not committed
or embedded in the ROM. The extractor verifies public Git blob SHAs and the actual
loader's extended-header offset before exporting geometry facts. Map screenshots
are references, never graphics imported into the game. Original GBA art conversions
and all generators are versioned.

Raster references for all tower floors, Gym, Trail, city and station were inspected.
Matching native HGSS raster captures for the houses, Theater, Center/Mart and gate
interiors are not available in this workspace; their geometry/props were checked
against canonical source facts. Their visual fidelity remains unverified beyond
GBA render inspection. Do not label those raster comparisons complete.

Detailed contracts: interior-review.json, room-review.json, service-review.json,
gate-review.json. These record adaptations and retain visual acceptance as pending.
The reference file preserves older notes as history; this document supersedes their
"unimplemented" descriptions for the above increment only.

## Checks actually performed

**Real Emerald build:** PASS. ROM used29,626,960 of33,554,432bytes; padded32MiB.
EWRAM226,448/262,144; IWRAM28,392/32,768. No engine upgrade or save-structure change.

**Automated:** opening, Olivine/interiors, Route39, western Johto, intro, Joe normal
and special assets, title music, visual repair contracts, area completion, Fly,
Ecruteak reference contracts, mapjson outputs, full network/build inclusion and
native generator checks. Full network158 maps/344 warps/70 border connections;
this is structural coverage, not a claim those other maps are visually finished.
Tower checks include exact stair anchors, directed jumps and escape from every
public tile. New room checks retain services/actors and detect isolated floor or
blocked performance paths. Test migrations are explained in VALIDATION_MIGRATION.md.

**Controller-driven mGBA:** PASS for27 reviewed maps/246 transitions, all their
current reciprocal doors/stairs/pads and connections, return to Olivine;509 city
blocked-edge probes plus four recorded trunk directions; all five performers move
and return; Center healing; both bridge fall returns; actual Morty battle loss,
local respawn and healing; normal house/Center Save -> cold boot -> Continue with
exact party/position retention. A separate copied fixture exercises the old shared
layout cache. Actual old0.8 battery Continue also passed, as did QA04-versus-QA05
normal Continue captures at the same Bell9F location.

Joe: actual party-menu Fly/cancel/all ten cities, departure/arrival Joe pixels in
VRAM, Save/Continue/reopen Fly; survey Surf four directions/disembark; registered
Mach/Acro mount/dismount, wheelie and rod casting/return to Surf. Existing Joe
walking frames and all three starter rescues/met origins/duplicate guards passed;
the latter also ran with the saved female gender value. Starter tests use disclosed
debugger initialization to skip the unchanged old introduction, then actual script
and controller checks. Normal cold boot/title/Start/New Game handoff/reset passed;
this does not mean the old introduction was replaced or playtested.

Tests use private copies only. Random encounters are suppressed in test RAM;
bike/rod gear,1HP healing/loss and stale-layout fixtures are disclosed RAM setup,
not production grants. No owner save or private save is committed/distributed.

## Deliberately incomplete / not asserted

- Owner Delta visual/collision acceptance remains pending; the city exterior's
  positive review is not blanket acceptance of these new interiors.
- DS online reception is offline. Gym candle-extinguishing story/battle gates,
  badges and source plot/reward/legendary events are deliberately absent.
- Some Joe bike/fishing/watering phases reuse directional poses. Dive/watering
  activation, advanced bike tricks, decoration, contests and linked multiplayer
  are wired/audited but not normally playtested here. See JOE_FIELD_AUDIT.md.
- Collision sweep covers reachable exterior blocked edges; every furniture edge
  on every interior floor was not individually controller-probed. Structural
  public-floor escape checks and the complete doorway/stair tour are separate.
- The rest of Johto and the original New Game prologue remain separate unfinished
  work. No additional city/route expansion occurred in this pass.
