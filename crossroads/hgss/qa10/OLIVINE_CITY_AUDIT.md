# Olivine city audit — QA10 owner correction pass

This is a read-only source/reference audit, not a new emulator playtest or owner
visual acceptance. Baseline source is
`285cfa4ebddcb390a8a5bde6116748cbb5eaba6b`; its tested delivery game checkpoint
was `489c404346f572aefb6856b3dd48a9b364a08ceb`, ROM SHA256
`df69e014e706168c56180828487a9ab12709a9bccd3dff063fee5f7af5d4f2f4`.

## Screenshot provenance and positive mapping

Ten new images in `D187C84F-2C49-449D-834F-8AFD0AB1F099` subsequently arrived.
They replace the initial absence of current photographs:

- Photos1–2 are **Ecruteak**, not Olivine. The blue Dance Theater is on the right;
  the central directory court/sign is36,45. House23,45 stands one plot farther
  west and is present/enterable. Actual HGSS also has a vacant dirt court here.
- Photos3/9: Olivine PortQuay S.S.Aqua boarding; previous vessel is scenery only.
- Photo4: Olivine lighthouse interior; exact floor remains root-runtime matching.
- Photo5: Olivine Cafe/Center street.
- Photo6: Olivine city-facing port with forced east-boardwalk approach.
- Photo7: Olivine quay-facing terminal facade.
- Photo8: Olivine terminal interior, not a ship room.
- Photo10: Ecruteak Center exterior.

Earlier99BA photographs show old Ecruteak/Mahogany, not current Olivine. The
new source-backed lot correction is soil/curb artwork for a genuinely open court,
not an invented building.

## Actual references used

- Actual full-city HGSS mosaic cached at
  `/workspace/scratch/hgss-reference/Olivine_City_HGSS.png`; source URL is
  `https://archives.bulbagarden.net/wiki/File:Olivine_City_HGSS.png`.
- Pinned source facts:
  `crossroads/hgss/canonical_events/johto-outdoor-geometry.json`, area
  `MAP_OLIVINE`: 64x64 city, all nine source warp destinations and source signs.
- Actual house/cafe/service images and source room matrices documented in
  `OLIVINE_ROOM_DESIGN_QA09.md` and `OLIVINE_COMPLETION_QA09.json`.
- Actual port terminal/quay images and source facts documented in
  `olivine-landmark-visual-references.json` and
  `canonical_events/olivine-interior-geometry.json`.

## Building inventory versus HGSS

All nine canonical enterable city destinations have native physical facades,
warps and rooms in this baseline. Their existence does not establish correct
appearance, complete maritime content or owner acceptance.

| Location | HGSS source city door | Current physical content | Audit finding |
| --- | --- | --- | --- |
| Gym |13,14|Owner Steel Gym facade; two-map hall/arena|Deliberate approved facade exception; present. Preserve optional battles/no new badges.|
| Center |16,33|Facade, reception, B1F|Present; original DS service-deck height flattened; network functionality offline.|
| Mart |29,33|Facade, source-backed shop furnishing|Present; shop services remain.|
| Lighthouse |45,39|Facade, six floors, balcony, lift|Present. Original GBA lantern housing/flat masonry are art adaptations requiring owner visual review.|
| Northwestern fishing house |17,23|Green-roof house; common0097 room/resident|Present; rod reward deliberately not granted in previous map-only scope.|
| Cafe |9,33|Cafe facade;0136 source-backed room/counter|Present; current counter access/furniture require actual before/after visual inspection if changed.|
| Northern trade house |31,17|Green-roof house;0097 room/resident|Present; source trade not implemented.|
| Northeastern Seal house |36,17|Green-roof house;0097 room/family|Present; DS seals unsupported.|
| Port terminal |23,52|City facade, terminal, quay/reverse facade|Present, but previous ship interior absent; current orientation/boardwalk adaptation needs review.|
| Joe residence |8,23|Accepted original facade and furnished residence|Intentional Black Ledger addition; preserve rest/Alpha bridge and identity.|
| Neighbour residence |8,28|Accepted original facade/interior|Intentional addition; do not replace a canonical room with it.|
| Silph subsidiary |31,40|Accepted office and starter case|Intentional addition; preserve rescue, uniqueness/met origin, terminal and existing story state.|
| Harbor Office |8,40|Accepted office/dispatch/Survey travel|Intentional addition; keep separate from S.S. Aqua boarding.|

The source selection contains the above nine canonical warp destinations; no
additional canonical enterable city building is established by the current
source facts or actual city mosaic. An unverified owner report must not be
answered by inventing a tenth building and calling it HGSS accurate.

## Empty signed lot — resolved by new photographs

The reported lot is Ecruteak's directory court, rectangle31..38,42..46, sign36,45.
Pinned075_T27 and outdoor facts identify a source background at36,45 and no
building/warp at this plot. Actual HGSS city imagery depicts brown soil and a
narrow pale curb. The previous plain gray fill looked like a placeholder.
Only39 soil art cells change; the sign, physical bits and events remain exact.
The source residence at23,45 is a separate existing enterable building.

Olivine's13 building labels identify present facades; non-building signs are
Directory24,42, NorthBoundary28,7 and Route40Sea7,36. Actual HGSS Olivine also
has a standalone directory on its harbor terrace. The earlier Route40/Battle
Frontier speculation did not match the owner's photographs; do not expand there.

## Concrete visual/structural review needs

1. City ground authoring currently derives most ground from permission bits,
   then stamps rectangular paving corridors. Permissions do not encode all
   HGSS grass/stone textures. Compare the full native city render and normal
   viewports against the actual mosaic: court edges, paved areas, small ledges,
   cliff transitions and facade approaches need image-based review, not merely
   walkability checks. Do not redesign the accepted original buildings.
2. The port city door coordinates match the actual source warp23,52, but the
   GBA port facade faces south and uses an east boardwalk. The DS entry/model
   is perspectival. Reconcile visible doors, passenger flow and native terminal
   exits as a single design; do not preserve an awkward detour solely because
   the old graph is connected.
3. The previous S.S. Aqua is16x5 scenery in `OlivineCity_PortQuay`, model168 at
   native origin21,15. There is no physical ship interior map. The boarding
   notice is an explicit deferred boundary, not a story-complete sailing system.
   The latest owner now authorizes physical ship construction. Actual source
   decks/cabins/engine/captain references should determine that new content.
4. The port desk currently says Harbor Office handles travel, while the Harbor
   dispatch says no passenger tickets and the ship says sailings are not
   operating. Separate accepted Survey/Alpha transport from passenger service
   in the wording; do not imply an implemented destination.
5. Current city/house/service map IDs and all16 city warp indices must stay
   stable. Any new ship/landmark IDs append. If a facade/door changes, preserve
   old-save safe spawns and independently test both leaves/full visible widths,
   each return destination and facing, furniture/water layering and ordinary
   walking away after arrival.

## Proposed corrective increment

- Preserve native-ROM before captures. The positively identified Ecruteak lot
  receives only source-backed soil/curb art; its canonical vacancy remains.
- Build the now-authorized S.S. Aqua physical map network from verified HGSS
  references, integrating the quay/gangway and terminal coherently.
- Keep unapproved sailing destinations, ticket/progression/story dependencies
  and source reward events explicitly unresolved; do not remove the boundary
  message by inventing a Kanto destination or story prerequisite.
- Reinspect city paving/courts/facades and all furnished interiors as images,
  retain accepted additions, then test normal movement/services/save copies.
- Deliver location-specific before/after gameplay views and an explicit
  reference-matched/adaptation/unfinished report. Prior QA09 automated passes
  are historical evidence, not current visual acceptance.

## Source implementation prepared for root generation

- Court helper:39 art-only cells, excluding sign36,45; nine high unused metas
  0x3F0..0x3F8, opaque bottom ground/blank foreground, original General palette3.
  Original glyph/metadata prefixes, collision, behaviors, events and IDs stay.
  Virtual source asset run754/871 glyphs before115-glyph owner Gym; final combined
  packing still needs root generation/verification.
- New original north-entry blue-vault port art has a visible portal atrow1 below
  a high row0 canopy. Facade origin20,51 preserves warp23/24,52 and extends south
  toy56. Two native non-animated north leaves and dry opaque deck underlays replace
  the old south-facing door; closed rear windows create no fake open south exit.
- Existing maritime palette11 is pinned in `port-qa09-palette11.pal` so the new
  port does not recolor lighthouse/Mart/boats/parasol. Dry measurement673 glyphs,
  128 free before owner Gym, versus680/121 in QA09.
- A central terrace pier leads directly south into the visible north portal;
  the old required east U-turn is removed. Warp indices/coordinates and four
  accepted original facades stay exact. Root owns terminal/quay integration and
  the old dry-apron/Surf position fixtures and any proven safety migration.

This agent edited source code/original art only. Actual game resource/map
 generation, final build and emulator after-tests are root-owned.

### Follow-up: preserve the terminal sign on its real forecourt

Independent reachability review found that keeping the old added port sign at
22,53 buried it inside the relocated solid terminal. The same sign event now
moves to22,50 on the northern pier/apron. It does not occupy either doorway or
its dry canopy approach. Old22,53 correctly returns to the facade body.

A single high private metatile0x3EF places the unchanged native sign foreground
on timber deck: exactly46 edge-connected gray backdrop pixels are made transparent,
with original palette0/1 sign colors over opaque palette12 timber. Every other
sign is unchanged. High allocation preserves the custom Gym's old first-free
metatile range. Updated asset dry measure is677 glyphs,124 free before the owner
Gym; actual integration/normal-controller sign interaction remain root checks.

### Test-only migration for the changed waterfront geometry

`olivine_collision_smoke.py` retains the original12 land-building and3-tree dry
case enumeration. The terminal's independently pinned box is now20,51,8,6;
all8 closed rear bases aty56 and named north/side walls must block. It does not
exclude the former doorway columns23/24 from that rear-base assertion.

The old5 dry terminal cases no longer have dry approaches, so they are replaced
by a separate, disclosed actual-Surf body phase, not a silent coverage removal.
The harness restores its original water-capable safe predicate, enables session
assistance through the real Harbor desk, uses native A/YES Surf, attempts all
accessible water-side bumps, records all four sides and requires all8 rear bases
actually checked from the south. It then disembarks normally and disables Survey
at the actual desk. No position, warp, map or permanent-flag writes are used.
Pure source enumeration predicts199 original land/tree cases and24 new Surf
body cases; those are planning counts, not emulator results.

`olivine_materials_smoke.py` preserves the original12 table,43 fence and4 boulder
cases. The old southern model-water traversal aty57/58 remains required, while
old dry apron24,54 is positively required to be solid new terminal body. Actual
disembark/return now uses the north pier24,50. Real desk OFF/ON/OFF separates
ordinary dry movement from water testing. Source syntax checks pass; actual
normal-controller execution waits for root's frozen delivery ROM.


## B3 runtime checkpoint — functional passes and visual finding

On exact ROM `af59dff1b06b99a9599c6f98b6fb6bd1e765cc52c0838a2dec5c79a6c1f88373`,
all six city phases completed: eight-map lighthouse all-edge tour;199 normal dry
building/tree bumps and24 actual-Surf terminal-body bumps with all four sides;
full192/192 composed Joe pixels at both exact portals and both north landings;
59 materials cases; six real counters;12 lighthouse normal Save/cold Continue
cases and five special journeys;39 court cells with full Joe visibility, four
exact directory-message approaches and a normal Save/cold Continue. Original
and copied batteries remained unchanged. These are scripted normal-controller
mGBA checks, not the owner's Delta visual acceptance.

One independent visual review found a genuine6F reference-art mismatch despite
those functional passes:26 inner optical-enclosure U-core cells used the outer
window/glass motif. Actual HGSS puts cyan machinery/enclosure there. The geometry
and collisions are correct; an art-only distinction is required. The final
correction scope is28 cells:26 glass-motif cells plus two missing/void enclosure
segments identified by the reference audit. All eight tour
and ten centered frames were inspected against the actual individual floor
references. Other floors' recognized features and flat GBA adaptations are
recorded, but6F is explicitly not reference-matched on B3. The actual diagnostic
frame is `qa/qa10/before/lighthouse-6F-b3-inner-glass.png` with separate identity.
B3 does not certify a future corrected binary; final checks must record its
own checksum. My emulator lane has ended so root can coordinate a later build.

## B4 city runtime checkpoint — scoped passes, separate facing failure

Frozen game source is `df8c4598d88c7770626be4621a5f39cf60dadb95`; ROM SHA256 is
`4fb28fe64fc44c0546462a935655346a61f13b644bc3040468146d136cd6d656`.
The overall B4 candidate failed a separate independent intended-facing audit:
four Ecruteak gate links faced south rather than the intended west/east, and
one Trail corridor arrival faced north rather than south. Root is coordinating
a minimal correction and B5 retest. The scoped passes below do not waive those
defects, claim overall acceptance or certify the pending B5 build.

All six city suites ran again on these bytes and passed. The lighthouse tour
covered eight maps,76 real transitions,19 roundtrip edge pairs and73 warp trials.
The199 dry and24 actual-Surf collision cases,59 materials cases, six front
counters,12 lighthouse normal Save/cold Continue cases, five window/lift journeys
and39 court cells/four directory approaches/one normal save all passed fresh.
Both actual port arrivals23/24,52 and following landings23/24,51 display all192
opaque Joe pixels before walking away. Original and copied batteries are exact.

The final lighthouse runner adds two strict ordinary walking circuits around
both sides of the6F enclosure in opposite directions, recorded continuously in
one native-resolution clip. This is an added regression check, not a change to
game inputs or a replacement for any existing save, journey or collision test.

Independent image review compared eight actual B4 tour views and ten centered
views against seven individual HGSS lighthouse images. The inner cyan optical
housing is now distinct from the outer glass ring; no new obvious corruption
was found in those views. The angular flat2D tower/core projection, simplified
wall/rail art and small northern cap are chosen adaptations, not pixel-identical
DS geometry or proven hardware necessities. A separate HGSS elevator cabin
raster remains unavailable. Stills, controller tests and owner visual acceptance
remain separate; this checkpoint does not declare either city100% complete.

The physical S.S.Aqua's full default runtime suite is a separate phase after
these city suites. It must finish its own source-derived wall bumps, all12 room
components, interactions and normal Save/cold Continue checks before it is
reported as passed. Public final evidence and exact test hashes belong under
`crossroads/qa/qa10/final/B4/`; no private batteries or emulator states are public.

The subsequent full B4 S.S.Aqua default suite completed:1,169 actual
source-derived solid-target bumps, all seven maps/twelve physical components,
twelve normal Save/cold Continue cases, fourteen NPC/sign interactions, two
actual berth NO/YES healing fixtures and eight furnishing contexts passed.
Independent image review inspected all twelve component and eight context
frames against four complete HGSS mosaics plus eight cached gameplay images.
The viewed ship art is coherent; simplified furnishings and off-camera details
remain qualified in its review. Original/copied batteries and the B4 ROM/ELF
hashes stayed exact. These ship passes are historical B4 scoped evidence: the
separate Ecruteak facing failures still prevent overall B4 acceptance, and B5
requires its own fresh gameplay results.

## B5 fresh city and ship verification

Game source `cc643ffe711204f3ef38e34e7aa1eb8c9558720f` built ROM
`ee2d81d5d0b55b7f1f9d36d1c9b055700164da439f51af7a66b5fb2d2147f90b`.
After the six gate/trail script corrections, all seven serial city/ship suites
ran fresh on these exact bytes and completed successfully. Nothing from B4 was
relabelled. The same strict assertions remain, including all199 dry/24 native
Surf bumps, full192/192 Joe at both port thresholds and landings,59 materials,
six counters, all eight lighthouse maps,12 lighthouse normal Save/cold Continue
cases, five special journeys, both continuous6F circuits and all39 court cells.
The court's four exact sign approaches and normal save/walk-away also passed.

The full default B5 ship suite again exercised1,169 source-derived solid-target
bumps, seven maps/twelve physical components, twelve normal Save/cold Continue
cases, fourteen actual NPC/sign interactions, two actual native berth NO/YES
health fixtures and eight furnished contexts, followed by the real city return.
Each phase guarded ROM/ELF and the unchanged original/copied battery. Private
save outputs and same-ROM health snapshots remain excluded from public proof.

Fresh independent image inspection opened eight B5 lighthouse tour images plus
eleven centered/inner-stair views, and all twelve B5 ship component views plus
eight furnishing contexts, against the actual cached HGSS references. No new
obvious rendering defect appeared in those views. Chosen flat2D art, simplified
furnishings, off-camera details and the missing separate HGSS elevator-cabin
raster remain explicit limits. This image review is separate from controller
tests and the owner's visual acceptance.

Exact commands, executed script hashes, native screenshots/recordings and
comparison galleries are under `crossroads/qa/qa10/final/B5/{city,aqua}/`.
Separate parent-owned intended-facing, old-save migration, doorway and existing
system regressions determine the overall candidate status. These scoped passes
do not certify the owner's newest private save, unimplemented interregional
sailings, whole-city visual acceptance or a100% completion claim.
