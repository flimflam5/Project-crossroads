# Heart & Soul Route 33 prototype — not yet playtested

Source: https://github.com/PokemonHnS-Development/pokehns-expansion at
`167aa6d537b109bb229c231ddce4616974c4da71`. `map.bin` is the unmodified
`data/layouts/Route33_hns/map.bin`, SHA-256
`8db5583d404249adf60d2271a790412af0692cae041a682127b733787ca4630a`.
Tiles and palettes come from `johto_south_hns`, already pinned with exact hashes
in `crossroads/donor/hns_azalea_exterior/provenance.json`. Donor map and graphics
credits and unresolved individual origins are recorded in
`crossroads/hgss/DONOR_EVALUATION.md` and must accompany any distribution.

The project baseline `black-ledger-baseline.bin` comes from QA10 source commit
`3138de89d9e57b816d3b7d03e727f04d69c2d168`, SHA-256
`60e8ccacebe713c060fde8bd652d275cdbfae8676bd3847f0700118a2bf97f26`.
It preserves the original western seven-column seamless connection to Azalea.

The donor 44 × 40 region is cropped to 32 × 24 at (3,10) so the existing cave
warp (24,7), map/layout IDs, events and town border offset are retained. Compared
with the actual HGSS route (32 × 32) this is a deliberate initial adaptation:
see `crossroads/hgss/ROUTE33_DONOR_CHECKLIST.md` and the HGSS visual reference
https://media.pokemoncentral.it/wiki/thumb/7/70/Percorso_33_HGSS.png/513px-Percorso_33_HGSS.png .
The westmost seven columns keep old tiles to preserve seamless town rendering;
this visibly differs from the donor and needs an HGSS-aligned Azalea/route pass.
The donor-only Headbutt-tree behavior is mapped to normal, with no new rewards,
trainer or story. Two existing Black Ledger sign tiles/behaviors are preserved.
Elevation-zero tree canopies are blocked because this engine otherwise treats
zero as a traversable transition.

`build_hns_route33.py` converts 55 metatiles and 107 8×8 graphics into a private
secondary resource, using the actual Azalea primary tileset and retaining its
boundary metatile 514, 8×8 graphic 582 and palette 6. The donor's 640-primary
indexing is remapped into the Emerald secondary 512-index space. The route keeps
existing events and uses donor crop geometry only beyond the town buffer.

Run `python3 crossroads/tools/build_johto_network.py --through west --check` and
`python3 crossroads/tools/validate_hns_route33.py` from a worktree that has the
pinned project history. Source-only checks have passed, including a conservative
327-cell route graph and a model of the existing Continue relocation logic for
530 formerly collision-free positions; 203 become blocked/occupied. This is not
proof of real movement, collision/layers, scrolling palette/VRAM behavior, old
saves or HGSS fidelity. A genuine QA10 save normally saved at old Route33 (22,7)
is stored outside the repository for testing; never commit private saves.

**Prototype only:** do not merge or distribute as QA until a real isolated build,
controller-driven town/route/cave traversal, visible edge/roof/tree inspection,
old-save cold Continue with payload comparison, native normal Save/Continue,
existing functionality regressions and owner visual review have been completed.
