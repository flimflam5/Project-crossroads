# Ruins of Alph donor pocket conversion

This source-only prototype prepares the two western exterior pockets and their
distinct Ho-Oh and Omanyte chambers for later Union Cave/Ruins integration. It
does not register any live maps, events, rewards, puzzles or save changes.

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
