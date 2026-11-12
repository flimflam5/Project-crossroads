# QA10 validation: preserve evidence, replace only superseded assumptions

Baseline: `285cfa4ebddcb390a8a5bde6116748cbb5eaba6b` (QA09 delivery).
The owner now authorizes a physical S.S. Aqua and logically connected port,
while destination/story/progression choices remain unapproved. A previous test
that proved the ship was absent cannot remain the desired positive behavior.
It remains useful as a historical BEFORE reproduction.

## Independent new checks

`crossroads/tools/validate_ss_aqua.py` reads pinned HGSS reference facts and the
actual native outputs, never the new generator. It independently derives floor
reachable from exact source exit seeds, avoiding the misleading zero-filled DS
matrix padding. All seven source maps have fixed dimensions and public floor
counts, and the four paired cabin maps each have two real components.

- Preserve all existing map/group/layout ID prefixes and all heal data.
- Preserve save structures, flag/variable/species/graphics/trainer constants and
  starter acquisition scripts exactly against the immutable QA09 baseline.
- Preserve Joe's residence, neighbour, Silph office and Harbor Office map events,
  native room layouts and scripts exactly; no disguised replacement.
- Require the seven actual ship maps, exact canonical source warp ordinals and
  destinations, all eight cabins and real exits from every walkable component.
- Validate actual C resource pointers, native 4bpp dimensions, loaded palette
  banks0–12, safe layer composition and no visible debug magenta/foreground floor.
- Reject unapproved trainers, reward/flag/progression writes or invented travel
  destination scripts. Ambient room furnishing is separate from canonical HGSS
  plot actors and voyage events.
- With `--built`, require Emerald table/header inclusion and compare actual ROM
  blockdata to all seven authored ship layouts, catching stale compiled maps.

These checks cannot grant visual acceptance. Normal controller movement,
arrival/facing, Save/Continue, reference comparisons and owner Delta review are
still required. Source-positive tests and in-memory negative controls must stay
separate from actual gameplay results.

## Exact historical assumptions requiring a named migration

### City-facing port fronts and arrivals

`validate_hgss_olivine.py` assumes every city doorway has its approach and outside
arrival at `(x,y+1)` and explicitly requires port positions23/24,53. That encoded
the previous south-facing GBA port, whose physical orientation reversed the
canonical north terminal approach. The proposed correction preserves city warp
indices13/15 and their canonical positions23/24,52 but makes their public fronts
north at23/24,51.

A safe update must name only those two exact indices, assert their expected
source positions/destinations, validate the new north-side walkable approaches
and dry returns without crossing active thresholds, and retain every other
building's original south-side assertion. It must also check their opaque body
and actual runtime exit facing. Removing all approach/return assertions or merely
blocking a visible door half would be a regression.

### Boarding boundary versus physical ship access

The old `Hgss_OlivineShipBoundary` message and solid gangway intentionally proved
that no ship map or destination existed. QA10 now requires actual docked boarding
and return. Preserve the old four quay→terminal warp ordinals, append the named
ship hatch leaves, and independently require matching reciprocal ship exits and
full visible width. Source1F has both Olivine and Vermilion story-selected warp
records at24,19; the docked implementation must keep Olivine and explicitly omit
the unimplemented Vermilion voyage rather than silently redirect it elsewhere.
A changed sign must explain the actual destination limitation, not imply a new
unlock or invent a departure schedule.

### Canonical disconnected cabin/floor components

`validate_johto_network.py` already exempts exact, independently verified branched
Ecruteak/Olivine reference floors from its generic one-room local flood. The new
ship contains four paired maps (two cabins each), plus two1F components joined
through B1F. Generic "all local exits connect to warp0 without leaving the map"
is false for those actual HGSS layouts. Do not broaden the generic skip: add only
the seven exact ship names after an independent geometry/component/every-tile-
escape validator has passed. The regional graph must still reach every actual
exit/interaction, including both cabins of every pair.

### Actual graphics coverage

The older `validate_city_graphics_limits.py` and `validate_city_ground_layers.py`
explicitly cover51 named Ecruteak/Olivine maps. They should retain those checks.
`SSAqua_*` names are not captured by the `OlivineCity*` glob, so new ship resource
checks must explicitly include all seven maps rather than interpreting the old
51-map PASS as proof of new art. Independent actual C pointer/layer functions can
be reused without importing the writer or changing engine limits.

### Doorway manifest and movement evidence

The old doorway manifest remains historical, with its south-facing port press
vector. New expected vectors, arrivals and facing must be specifically recorded
for both port leaves and every new ship threshold. A generic behavior allowlist
change is insufficient. Existing exact engine behaviors60/61/65/69 can be reused
where appropriate; if another behavior is needed it requires a narrowly named
positive assertion and normal controller proof. No source check can replace the
before-and-after movement footage requested by the owner.

## Implemented exact QA10 migrations

The four existing validators keep their original assertions except these named
positive replacements:

- City front/return checks recognize only warp13/15 as north-facing at the same
  canonical23/24,52 coordinates; all other building arrivals still use y+1.
  The one existing Port plaque keeps its script/index and moves from22,53 to
 22,50 on the visible north approach. This fixes an actually identified new
  buried-sign defect; the old tile remains solid facade, not a sign in glass.
- Harbor checks now require the hand-reviewed8x6 north-facing body profile,
  exactly two dry leaves and two dry canopy cells, original sea underlays,
  intact solid southern body and a direct dry23/24 passenger approach.
- Material history remains V7→QA09:12 relocated table cells and65 old DS Port
  model cells. A separate SHA-authenticated QA09→QA10 mask names exactly82
  physical/elevation changes. Every other physical cell is immutable. This is
  not an arbitrary rectangle exemption or a discarded original assertion.
- Maritime resources append exactly two gangway metatiles; all510 original
  behavior/layer attributes remain byte-exact. All original glyph-bound, palette,
  shared-Temple and native alias checks remain. The two actual private lighthouse
  hatch leaves retain each old full lift attribute after their drawing IDs change.

The independent lighthouse check now covers all six floors plus the existing
balcony. Header/events/warps, IDs, dimensions and every physical/movement cell
must remain exact against QA09 while artwork changes in a private resource.
Literal reviewed RGB555 motif assertions distinguish pale/teal/burgundy visitor
floors and pink/cyan lantern-room surfaces from the old generic green/purple
surfaces. These source-art checks do not certify owner visual acceptance.

## New ship model projection and full-width openings

The immutable HGSS permission plane is the starting floor geometry, not the full
collision of its separate3D bed/cabinet/table models. Complete actual HGSS mosaics
were inspected before permitting any native change. The independent checker now
contains literal reviewed furniture-body rectangles/points and exactly11 opening
clearances (second hatch leaves and one stair landing), rather than trusting the
writer's list of changes. It rejects every other missing floor/extra void cell.
All body cells must actually be solid, every named leaf/landing must be open,
and every actor/public component needs an accessible real exit.

Twenty-nine appended visible-leaf warp records have independently pinned native
indices, coordinates and destinations. Their source parents retain all24 actual
canonical warp records; the coincident conditional Vermilion record is explicitly
omitted. A separate directed component graph proves every one of the12 physical
ship components, including both1F sections and all eight cabins, is reachable from
and can return to the Olivine dock. A connected map-name graph alone is insufficient.

A real initial source-floor test failure identified the model-body distinction;
it was not changed to a blanket pass. The seven missing-floor/extra-void negative
controls still run, plus the moved-ID negative control. Positive model solids,
full-width alias endpoints, preserved source ordinals and no new plot/reward/
destination writes supplement those exact geometry checks. Actual controller
movement and owner visual review remain separate required evidence.

## Legacy callers corrected after the first real build

The first Build1 source-check ledger retained six failures caused by four old
assumptions. The following three validator-only corrections preserve their
original checks and do not change maps, resources or ROM bytes:

- `validate_hgss_violet.py`: the exact authorized append tail is now the original
  three Violet maps, nine Olivine maps, then seven explicitly named Aqua maps.
  The old ordinals still must be an identical prefix; arbitrary extra maps or
  reordering still fail. This also repairs its regional/visual-check callers.
- `hgss_olivine_validation.py`: first require the independent seven-map/source-
  geometry and all12-component round-trip proof, then incorporate only those
  seven names into its actual tile-level forward/escape graph. All30 interior
  maps/3,968 public nodes must be reachable and escapable. No generic disconnected
  room exemption is added, and only actual city exits are graph boundaries.
- `validate_western_johto.py`: collect the ship's ambient interaction file only
  after proving the exact `.include "crossroads/scripts/ss_aqua.inc"` is linked.
  This retains the missing-label assertions for every map actor and sign.

Direct Violet, Western `--built`, full Johto `--built` and area-completion
rechecks passed after these changes. They remain structural/source evidence.
The separately reproduced legacy Surf relocation bug is a real engine-state
failure owned by the parent, not a failed assertion to remove or reinterpret.

## Actual Build2 port-arrival visibility defect

Independent review of the real Build2 native arrival frame and its enlarged
player region confirmed that Joe's hair remained visible but his torso/legs
disappeared behind the blue entry arch on the public north landing. This was
not accepted as ordinary transient canopy overlap or a source-check pass.

Only the two dry canopy cells at world23/24,51 (local3/4,0) change attribute
from0x0000 to0x1000. Their drawing pixels, under-floor, collision/elevation,
behavior0, source coordinates, palettes and all warps remain unchanged. Native
COVERED1 places the arch/deck below Joe on these exterior arrival cells. Both
actual doors remain0x1061, and every other Port roof/eave/body attribute retains
its previous exact profile. The harbor validator now asserts the full48-cell
layer/behavior profile, so this cannot become a blanket flattening of all roofs.

The strict assertion rejects the recorded Build2 attributes. The parent applies
that narrow repair and produces a new frozen ROM. Actual before/after normal
walking, both exits and Save/Continue require full current Joe sprite visibility
and native-frame review; an attribute assertion alone is not a playtest.

## Final Build3 preview ownership collision

The first66-command Build3 run retained one failure: the landmark `--check`
expected its48×48 quay sailboat preview at `sailboat-native.png`, but the later
city facade generator had correctly written its different96×80 city sailboat
projection to that same path. Neither failure nor filename implied corrupt game
data; the two writers had mistakenly shared a review-only artifact name.

The landmark preview now uses `quay-sailboat-native.png`. The original city
`sailboat-native.png` remains unchanged, and the city generator's `--check` now
also verifies that preview's dimensions/indexed pixels/palette, so the collision
cannot silently recur. Both distinct previews are preserved. The new quay PNG
was produced by executing only the existing pure quantization function in an
isolated scope, followed by a targeted preview-file write; no map/resource/ROM
output generation occurred while emulator lanes were active.

Hashes of all11,030 map/layout/tileset/registration/ROM/ELF input files were
unchanged. Both generator checks were re-executed and passed. The final effective
66-command ledger retains the original failure and the exact replacement check
results rather than deleting the diagnostic history. This fix changes preview
ownership/checking only and requires no new gameplay claim.


## Actual6F material failure: stronger independent B4 check

The B3 positive cyan probe sampled only the original small northern cap. Actual
native/reference review exposed26 inner wall cells still using the outer glass
texture and two source-model corners left black. The stronger validator uses a
literal28-coordinate mask independent of the writer, compares immutable B3 game
commit e7e2c085a5, and requires exactly those art-ID changes. Other six map words,
physical bits and full attributes remain exact; all previously used private
metatile drawings remain unchanged. Every corrected cell needs a substantial
actual cyan body and must contain no outer-window reflection color.

It was run against the known-bad frozen B3 assets and correctly failed with the
named missing28-cell correction; `/tmp/qa10-b3-inner-core-negative-control.log`
retains the negative-control result. B4 positive/built checks are pending central
generation. CI explicitly fetches the immutable e7 source baseline. This adds
coverage after a real visual defect; it does not relax old physics/resource checks.

The first B4 palette-preservation probe compared Git's LF-normalized blob with
CRLF worktree `.pal` bytes and rejected identical colors. It now compares every
header/color line with line-ending normalization, keeping all values exact.
B4 source/built assertions pass, including all28 positive cyan cells and the
other-six-map/old-used-alias/glyph/full-attribute/palette invariants.


## Route42 writer order during B5 verification

The first68-command B5 ledger caught one remaining generator defect: the new-route
script branch compared its bare Route42 header before the later arrival-facing
postprocessor. The writer now renders the scoped native callbacks before that
comparison; the existing-route final pass remains idempotent. The exact original
`build_johto_network.py --through west --check` recheck passed with the B5 ROM
unchanged. No assertion or generated game input was removed or relaxed. The
initial failure and successful recheck are both retained in the final ledger.
