# Heart & Soul Charcoal Kiln donor data

The files under `data/` are selected, unmodified donor files from
[Pokémon Heart & Soul](https://github.com/PokemonHnS-Development/pokehns-expansion/tree/167aa6d537b109bb229c231ddce4616974c4da71),
revision `167aa6d537b109bb229c231ddce4616974c4da71`. `source-sha256.json`
records exact source-file hashes. The deterministic converter
`crossroads/tools/build_hns_charcoal_kiln.py` uses the Azalea House1 map,
Johto Building primary and Barn secondary tilesets; it packs only used tiles,
metatiles and palette banks into an independent Emerald-mode private tileset.
It retains donor collision/elevation and display attributes outside nine blocked
cells with an original brick kiln overlay. Original stone floor, raised platform
edge, shelves, bench and chimney adapt the remaining donor artwork toward the
HGSS reference without changing collision. Donor object/warp/story scripts are
replaced with Black Ledger's own worker and exit.

The donor's README requests credit for Pokémon Heart and Soul and the full credit
chain. Its aggregate in-game credits list map work from Crystal Advance / Kertra,
Fire Gold / blackfragrant and SkidMarc25, and tileset work from Crystal Advance /
Kertra, Ekat99, TheDeadHeroAlistair, Johto Redrawn Team, zatavares852, lbsbezerra,
WesleyFG and Kalarie. These are aggregate credits; the particular authors of
these files and individual redistribution terms are not established. See
`crossroads/hgss/DONOR_EVALUATION.md` for linked source references and limits.

HGSS's Charcoal Kiln interior differs from this donor's house layout, including
its brick kiln, raised wooden work area, and furnishings. This is an interim GBA
adaptation, not a claim of HGSS fidelity. Its exterior must be compared and
corrected in the larger Azalea reconstruction. The donor's Rocket / Farfetch'd
progression and Charcoal reward have not been introduced.
