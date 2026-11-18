# Heart & Soul Underground Hall conversion source

This contains pinned input files for an **offline-only** Underground Hall
conversion, not a playable map. Run:

```
python3 crossroads/tools/prepare_hns_ruins_hall.py --output /tmp/hns-hall-preview
```

The converter checks the source hashes, packs a 29-by-32 donor map into 54
metatiles, 142 graphics tiles and three palette banks, and inventories the
original five warps. It preserves each converted source cell's collision,
elevation and metatile attributes. A future gameplay implementation must
adapt the map to the HGSS hall, add the separate HGSS Hall Entrance and its
reciprocal public exterior doorway, and validate the tiles in-game. HGSS has
puzzle falls into the hall; the donor's four direct chamber exits do not model
that and must not be blindly wired. No story, items, flags or map IDs are
changed by this preparation.

Donor source is [Pokémon Heart and Soul](https://github.com/PokemonHnS-Development/pokehns-expansion/tree/167aa6d537b109bb229c231ddce4616974c4da71),
revision `167aa6d537b109bb229c231ddce4616974c4da71`. The source list and hashes
are recorded in `source-sha256.json`. Its README asks for full credits and its
aggregate credits name map contributors Crystal Advance / Kertra, Fire Gold /
blackfragrant and SkidMarc25, and tileset contributors Crystal Advance /
Kertra, Ekat99, TheDeadHeroAlistair, Johto Redrawn Team, zatavares852,
lbsbezerra, WesleyFG and Kalarie. These are aggregate acknowledgements, not
individual file attribution; explicit file-specific licensing remains unverified.
