# Heart & Soul Ruins exterior conversion — reference preview

This directory contains pinned, checksum-verified source data for a **non-playable**
Ruins of Alph exterior conversion. Run `python3 crossroads/tools/prepare_hns_ruins_outside.py --output /tmp/black-ledger-ruins-preview`.
The output is required to be outside the repository and preserves 2,208 donor
cells' collision/elevation and source metatile attributes while packing 189
metatiles, 317 graphics, and eight palette banks into Emerald-indexed data.
The eight banks need an explicit six-primary/two-secondary palette arrangement
when eventually installed. The exporter does **not** register tilesets, maps,
warps or events and does not prove movement, water, layers or animation.

Donor: [Pokémon Heart & Soul](https://github.com/PokemonHnS-Development/pokehns-expansion/tree/167aa6d537b109bb229c231ddce4616974c4da71), revision
`167aa6d537b109bb229c231ddce4616974c4da71`. Exact upstream paths and SHA256
hashes are recorded in `source-sha256.json`. The donor asks for Pokémon Heart
and Soul and the full chain of upstream credits. Its collective credits list
Crystal Advance/Kertra, Fire Gold/blackfragrant, SkidMarc25, Ekat99,
TheDeadHeroAlistair, Johto Redrawn Team, zatavares852, lbsbezerra, WesleyFG and
Kalarie. These are aggregate credits; individual source-file authorship and
asset-specific redistribution terms remain unverified.

The donor's Ruins exterior is 46×48; HGSS's reference world matrix covers 32×64.
The donor's direct B1F-to-Ruins cave links omit HGSS's distinct 1F and B2F
connector pockets. This conversion is a source of compatible pixels and tile
facts, **not** an approved HGSS map. Do not register it unchanged or replace
Black Ledger's current Ruins map without reconstructing geography, events,
old-save positions, chamber interiors and reciprocal connections.

`crossroads/donor/hns-union-cave/hgss-corrected-warp-plan.json` inventories the
actual HGSS cave connector anchors. Run `python3 crossroads/tools/validate_hgss_union_cave_connections.py`
to validate the pinned reference, old warp-index destinations and proposed
reciprocal graph. References and notes are in the Union Cave donor README.
