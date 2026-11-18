# Ruins of Alph donor pocket conversion

This donor-source package supports two western exterior pockets and distinct
Ho-Oh and Omanyte chambers. See the integrated prototype checkpoint below for
the current live-map status and the remaining validation.

`python3 crossroads/tools/prepare_hns_ruins_pockets.py --output /tmp/hns-ruins-preview`
verifies the pinned inputs in `source-sha256.json` and emits compact
Emerald-indexed palettes, graphics, metatiles, attributes, four block arrays,
and a donor warp inventory. The exterior uses 77 metatiles, 172 tile graphics
and four palettes; the chambers use 40 metatiles, 78 tile graphics and five
palettes. Original cell collision/elevation, visual tile indexes, flips,
palette mapping and metatile attributes are checked during conversion. This is
an offline data transformation; it is not a playable build or visual approval.

The NW exterior donor crop is `(0,19,16,17)`, with the cave mouth `(13,6)` and
Ho-Oh chamber `(5,4)` in crop coordinates. The SW crop is `(0,34,22,14)`,
with cave mouth `(14,2)` and Omanyte chamber `(7,6)`. Both chamber crops are
10x11 and expose the outside entry `(4,9)`, two underground hall positions
`(4,5)` and `(5,5)`, and a hidden-room position `(5,1)`. The original donor
warps in `report.json` are a source inventory, **not** approved gameplay warp
targets: the donor connects B1F directly to outdoors while HGSS uses isolated
1F and B2F connector pockets. The cave candidate must adapt those connections.

The SW mouth's dry component and its chamber's dry component are separate in a
simple source-grid analysis; water/Surf, elevations and crop boundaries need
normal gameplay testing. Verify both chamber puzzles, descriptions, hall falls,
hidden rooms and all reciprocal exits against HGSS before registration. Do not
invent rewards or connect separate HGSS pockets through a generic room. Both
the 46x48 donor exterior and the new crop dimensions are GBA adaptations; they
are not exact copies of HGSS's 32x64 world-matrix area. The reference data and
event anchors are recorded in the cave agent's continuation notes.

Donor: [Pokémon Heart and Soul](https://github.com/PokemonHnS-Development/pokehns-expansion/tree/167aa6d537b109bb229c231ddce4616974c4da71),
revision `167aa6d537b109bb229c231ddce4616974c4da71`. Its README requests full
upstream credits. Its aggregate credits list maps by Crystal Advance / Kertra,
Fire Gold / blackfragrant and SkidMarc25; tileset contributors include Crystal
Advance / Kertra, Ekat99, TheDeadHeroAlistair, Johto Redrawn Team, zatavares852,
lbsbezerra, WesleyFG and Kalarie. These are aggregate acknowledgements, not
claims about authorship of individual files. Explicit file-specific terms remain
unverified. Exact input paths and SHA256 hashes are in `source-sha256.json`.

## Sliding-puzzle engine preparation

The HNS 4-by-4 picture puzzle implementation and its two extra staging columns
are ported separately into `src/sliding_puzzle.c`, `src/data/sliding_puzzles.h`,
`include/sliding_puzzle.h`, `include/constants/sliding_puzzles.h`, and
`graphics/sliding_puzzle/`. Their donor paths and original SHA256 hashes are in
`puzzle-source-sha256.json`. The port adds a public declaration, converts asset
references to this project's `INCGFX` build convention, removes an unused
local, and tests empty board slots without reading the cursor sprite; the
special is appended at the end of the existing special table with `waitstate=1`,
keeping all prior special numbers stable.

At the source-only checkpoint the special had no gameplay callers. The two
subsequent draft chamber callers are described below. A scratch component test
ran the actual scaninc-generated asset rules, project's preprocessor, ARM cc1
with project flags, and assembler against the real graphics and palette assets;
all 56 undefined object symbols exist in the prior QA10 ELF. This is **not** a
full project link, emulator run, or minigame test. Validate screen entry/exit,
controls, success/cancellation, field return, and save safety before using it.
Because the project special macro already emits an implicit `waitstate`, do not
copy the donor script's extra explicit `waitstate` after this special.

## Integrated prototype checkpoint

The six Ruins maps are now wired as a **development candidate**, not an
accepted or completed area. The southwest and northwest pockets retain
separate chambers, and the cave connections follow the HGSS 1F/B2F chains.
Both chamber picture boards now call the prepared puzzle special and use a
scripted fade/warp to the underground hall on success. The new 32×64 hall
uses the reference SW (5,42) and NW (5,24) fall landings; its old layout and
map ID are preserved for save migration. No permanent success
flags, item grants, hidden rooms, or story events are implemented; the puzzles
are repeatable. The GBA corridor between the hall and the public surface is
provisional, and the southwest pocket has a two-cell path in the donor ledge
so travel can work in both directions. These are adaptations, not HGSS 1:1
claims. The surface entrance uses a private repacked donor facade; existing
warps 0/1, signs, resident and border connections are retained. An appended
layout ID distinguishes old Ruins saves for migration. No successful puzzle
interaction, map traversal, old-save behavior or rendered facade has yet been
confirmed by a full build and emulator test; owner visual acceptance is pending.
