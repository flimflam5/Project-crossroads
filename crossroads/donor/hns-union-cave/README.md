# Union Cave donor conversion prototype

This is a data-only conversion for planning three Union Cave floors; it does not
register any gameplay map, alter IDs or establish working doors or stairs. Run:

```
python3 crossroads/tools/prepare_hns_union_cave.py --output /tmp/hns-union-cave-preview
```

It verifies SHA256 hashes of selected donor files, compacts 7,184 cells across
1F, B1F and B2F into 89 Emerald-indexed metatiles, 161 graphics and six palette
banks, and verifies preserved collision/elevation and pixel-index inputs. The
output is explicitly outside the checkout; an offline map is not a playtest.
Tileset animations, water, NPCs, layers, directional mechanics, live warps and
old-save migration remain untested. The background/foreground layer must be
inspected in mGBA before these graphics are linked.

Donor: [Pokémon Heart & Soul](https://github.com/PokemonHnS-Development/pokehns-expansion/tree/167aa6d537b109bb229c231ddce4616974c4da71),
commit `167aa6d537b109bb229c231ddce4616974c4da71`; exact selected file paths
and SHA256 values are in `source-sha256.json`. The donor requests credit for
Pokémon Heart and Soul and its full upstream chain. Its aggregate credits list
map work by Crystal Advance/Kertra, Fire Gold/blackfragrant and SkidMarc25, and
tilesets by Crystal Advance/Kertra, Ekat99, TheDeadHeroAlistair, Johto Redrawn
Team, zatavares852, lbsbezerra, WesleyFG and Kalarie. Specific authorship of
these files and asset-specific redistribution terms remain unverified.

## HGSS reference and migration constraints

The [actual HGSS Union Cave 1F map](https://archives.bulbagarden.net/wiki/File:Union_Cave_1F_HGSS.png)
shows a long, mostly north–south layout with pools and two separate descending
staircases. The donor 1F has (32,7) Route 32 exit, (32,45) Route 33 exit,
(10,30) northern B1F stairs and (6,47) southern B1F stairs. Donor B1F has two
1F stairs, two Ruins of Alph exits and a B2F staircase. These facts are source
inspection, not proof of an HGSS match. Reference comparison of each cave floor,
water and entrances is still required.

Black Ledger's existing `UnionCave_1F`, `UnionCave_2F` and `UnionCave_3F`
are all 28×22. Existing 1F warp indices **0** (2F), **1** (Route 32) and **2**
(Route 33) and their reciprocal destination indices must remain stable if the
48×60 donor 1F is adapted. Existing 2F/3F warp indices must likewise be retained.
The donor's second 1F/B1F staircase and both B1F/Ruins connections must be
represented through appended reciprocal warps and actual correct destination
maps. Connecting both stairs to one generic room would misrepresent the real
geography; silently blocking either staircase is also not an acceptable finish.
Do not copy Heart & Soul's story scripts, rewards, trainers, event flags or IDs.

Resizing floors and changing cave geometry can strand or hide old players or
convert a saved dry tile into water; generic collision-only relocation cannot
prove a visible, reachable and safe landing. Capture genuine prior-version cave
saves; audit all formerly reachable positions against walkable connected zones,
player rendering and Surf state; introduce narrowly scoped migration only when
needed. Preserve party, boxes, bag, starter variable and saves. Test all exits,
stairs, water/Surf, NPCs and Continue using real controller input; measure ROM
and RAM and run actual compiled-map and regression validators. Do not describe
Union Cave as complete until all floors, references, interactions and owner
visual QA are finished.

`warp-mapping.json` enumerates a proposed mapping preserving all six existing
warp indices across the three floors. `validate_hns_union_cave_plan.py` checks
those current reciprocal destinations and inventories every donor floor warp.
The two Ruins exits remain unresolved: the existing Ruins map is one connected
generic area, while [HGSS reference](https://bulbapedia.bulbagarden.net/wiki/Union_Cave)
places the cave exits in distinct Ruins subareas; connecting them directly would
open an incorrect route. Reconstruct those subareas before wiring the cave.
A source comparison of previously walkable old-save coordinates found 68, 44
and 132 positions on new donor elevation-1 water on floors 1F, B1F and B2F
respectively. Existing water recovery covers Violet and Olivine only. Even a
collision-clean save can thus need safe relocation, without changing actual Surf
saves; all positions require reachability/render checks in the finished layouts.

The isolated prototype also extends `Crossroads_PrepareContinue`'s existing
water landing guard to the three exact donor floor dimensions and existing
Union Cave IDs. The current 28×22 playable rooms do not meet that guard; the
change therefore does not alter their current water recovery. When and only when
those donor-sized floors are installed, a saved walking avatar at elevation 1
uses the existing dry-tile relocation, while an actual Surf avatar keeps its
water position. The isolated C file passed ARM GCC syntax checking with the
project's modern settings. This is **not** a build or gameplay verification;
all prior safe-landing visibility, component reachability, and copied walking
and Surf save requirements remain open. Future saves in those donor-sized maps
are also subject to the guard, not only legacy saves.

A pinned donor Ruins exterior map and event list are included to verify the two
B1F exits against their actual reciprocal entries. A constrained static dry-grid
check places the Route 32 public gate and the two cave entries in three distinct
components. It does not model Surf, elevation transitions, ledges or event logic;
actual HGSS geometry and normal emulator movement must verify accessibility.

## HGSS connector correction — source plan only

The donor's two direct B1F exits to the Ruins omit real HGSS connector pockets.
Pinned pret/pokeheartgold revision `6bf138d6035aa6b43d6f8f4132a12df70f86dcec`
contains the actual four event records under `hgss-reference/`; individual
SHA256 hashes are in `hgss-reference/sha256.json`. The full 18-anchor mapping,
old warp-index contract, matrix dimensions and reference URLs are recorded in
`hgss-corrected-warp-plan.json`. `validate_hgss_union_cave_connections.py`
checks source anchors and reciprocal pairs without altering a playable map.

HGSS 1F is 32×96, B1F 32×64, B2F 32×96, and Ruins outside is 32×64. Two
separate B1F stairs lead via distinct B2F connector segments to isolated 1F
pockets and then to the two western Ruins entrances. One B2F connection may
require Surf and needs engine verification. HGSS reference source terrain
permissions indicate the pockets are distinct, but are not a gameplay test.
Directly binding the donor's B1F exits to the current generic Ruins map opens a
misleading shortcut. Existing cave maps, saves, route links and guide/notes
interactions must be retained while the floor geometries, all six current warp
indices, new reciprocal connectors and distinct Ruins regions are constructed.

The existing dimension-scoped water recovery prototype remains **untested** and
is insufficient by itself for passable cliffs, active warps or obscured old
positions. Capture real copied old saves and verify dry/Surf states, visual
priority, full component reachability and event interaction in an actual ROM.
