# Route 33 donor reconstruction checklist

Status: **reference and dependency investigation only**. No Route 33 donor
geometry, graphics or events have been imported; no new build or playtest has
verified this area. It is a candidate for the next geographic increment after
the contained Azalea Charcoal Kiln test.

## Reference, donor and existing game

| Item | HGSS reference | Heart & Soul donor | Current Black Ledger |
|---|---|---|---|
| Extent | 32 × 32 cells in the extracted world matrix | 44 × 40 metatiles | 32 × 24 metatiles |
| West | Azalea Town; short route to Union Cave | Azalea Town connection, offset −1 | Azalea Town connection, offset −10 |
| Cave | Union Cave 1F door at (19, 13), destination anchor 2 | Union Cave 1F warp (27, 17), destination warp 2 | Union Cave 1F warp (24, 7), destination warp 2 |
| Route 32 | Reached through Union Cave, not a direct outdoor connection | Direct north connection to Route 32, offset 1 | No direct outdoor connection |
| Weather | Rain on the HGSS route | `WEATHER_NONE` | `WEATHER_RAIN` |
| Events | HGSS placements and encounters require separate review | Trainer, moving Pokémon, berry tree and Azalea progression triggers | Existing resident, two signs and one cave warp |

Coordinates are local to each implementation and not interchangeable. The
HGSS figures are extracted data facts, not evidence that the existing GBA map
matches HGSS visually. The donor's Route 32 connection is a geography change to
correct, not one to import. Its story, trainer and encounter decisions are not
approved for Black Ledger.

HGSS geometry and destination facts: `crossroads/hgss/canonical_events/johto-outdoor-geometry.json`,
`MAP_ROUTE_33`; the source event is
[pret/pokeheartgold 034_R33.json](https://github.com/pret/pokeheartgold/blob/master/files/fielddata/eventdata/zone_event/034_R33.json),
blob `c3dca281cf04d06125dab34541674fda4cda40be`. The
[HGSS walkthrough](https://bulbapedia.bulbagarden.net/wiki/Walkthrough%3APok%C3%A9mon_HeartGold_and_SoulSilver/Part_4)
describes the short route between Union Cave and Azalea. The
[Route 33 guide](https://www.centropkmn.com/pokemon-hgss/guia/ruta-33/) links
four HGSS in-game screenshots for visual comparison. Those pictures have not yet
been inspected in this pass; an actual route-wide reference comparison remains
required. Do not invent the terrain based solely on dimensions or the donor.

Donor source is pinned to `167aa6d537b109bb229c231ddce4616974c4da71`:

- [Route33_hns/map.json](https://github.com/PokemonHnS-Development/pokehns-expansion/blob/167aa6d537b109bb229c231ddce4616974c4da71/data/maps/Route33_hns/map.json)
- `data/layouts/Route33_hns/map.bin`, SHA-256
  `8db5583d404249adf60d2271a790412af0692cae041a682127b733787ca4630a`,
  3,520 bytes / 1,760 cells.
- `data/layouts/Route33_hns/border.bin` and the `LAYOUT_ROUTE33_HNS` entry
  in `data/layouts/layouts.json`.
- `data/tilesets/primary/johto_south_hns/metatiles.bin`, SHA-256
  `0d3ac83f833b7a0ec38e1054e6499dc9c54d739741d8aab1cf6e92ae75108447`;
  its `metatile_attributes.bin`, SHA-256
  `d027dcbeb6df0805132b2305c141b9229d07c02d903064ca02a265aa2be09e67`.
- Secondary `data/tilesets/secondary/azalea_town_hns/metatiles.bin`, SHA-256
  `22bfc5df0c199a221660e66c12c6a9d244cb6418e7555ebe7a589da8c214f9ec`;
  its `metatile_attributes.bin`, SHA-256
  `8337e0c0a0a94666da52a1cc9f6f3ff7c63e8794177846ee3b60b87a328cf75f`.

The raw donor map uses 76 distinct metatile IDs, all in the donor's primary
range, including IDs above the ordinary Emerald 512-primary split. This does not
prove the secondary tileset, palette assignments, animated tiles or graphics
can be discarded: inspect every referenced tile, palette, layer and behavior.
Convert into private resources or another verified engine-compatible arrangement;
do not overwrite a tileset shared by accepted cities. Kiln interior assets use
different donor tilesets and cannot simply be substituted. The donor's requested
and upstream aggregate credits, with per-file uncertainty, are recorded in
`DONOR_EVALUATION.md`; record exact source files and modifications for this area.

## Existing IDs and generator ownership

- `MAP_JOHTO_ROUTE33` is group 75, index 83;
  `LAYOUT_JOHTO_ROUTE33` and `data/layouts/JohtoRoute33/map.bin` are existing
  saved-map/layout identities. `MAP_AZALEA_TOWN` is 75:64 and
  `MAP_UNION_CAVE_1_F` is 75:89. Preserve the numbered identities and the cave
  destination warp index, and validate the reciprocal cave return.
- `crossroads/tools/johto_world_spec.py` currently defines the route dimensions,
  Azalea edge and cave mouth. `crossroads/tools/build_johto_network.py` regenerates
  its layout, weather, events, connections and associated scripts. A new author
  must explicitly integrate with or take ownership from that generator; a manual
  binary edit alone will be overwritten and `--check` must remain meaningful.
- Preserve existing resident/sign interactions or relocate them with working
  access and a documented reason. Preserve other routes, current scripts, Joe,
  saved party/items, title, Gyms and accepted Route 38/39 encounters.

## Acceptance work, all pending

- [ ] Inspect the actual HGSS visual references: ledges and elevation, cave
      mouth, rain, trees, paths and western town seam; document GBA adaptations.
- [ ] Compare donor terrain and tile art against that reference and inventory
      all used palettes, animation, collision and per-file provenance.
- [ ] Author the route with its HGSS geography and no direct Route 32 seam;
      update the relevant generator and keep map/layout IDs stable.
- [ ] Preserve normal traversal and reciprocal Azalea/Union Cave entrances and
      exit-facing, arrival positions and applicable player interactions.
- [ ] Test copied genuine older saves from this route, its reachable old tile
      positions and cave/town boundaries. A larger 32 × 32 extent keeps old
      coordinates in range but does not by itself prevent spawning inside a
      new obstacle. Devise and test any required narrowly scoped migration.
- [ ] Run map generator checks, opening/Olivine and regional regressions, actual
      Emerald build/inclusion and ROM/RAM measurements. Play the exact produced
      ROM in mGBA using normal controller movement, saving and cold Continue;
      record native frames and movement around ledges, trees, cave and town seam.
- [ ] Report unfinished references and playtesting separately from the owner's
      Delta visual acceptance. Do not count this candidate as completed.
