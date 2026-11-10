# Johto reconstruction checklist — QA06

The existing161-map exploration network is connected; that is not a completed HGSS reconstruction. Source authority, deviations and unresolved references remain in [reference-manifest.json](reference-manifest.json). Owner visual acceptance remains pending. No new encounter, team, badge or story decisions are included.

| Area | Reference review | Current implementation |
|---|---|---|
| Ecruteak City | Raster inspected | QA05 reconstruction preserved; QA06 owner Gym exterior; visual acceptance pending |
| New Bark Town | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Cherrygrove City | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Violet City | Raster inspected | QA06 source terrain/doors, bridges, houses, school, services, Sprout floors/gates; visual review pending |
| Azalea Town | Raster not inspected | Old exploration layout + owner Gym exterior; full reference reconstruction pending |
| Goldenrod City | Raster not inspected | Old exploration layout + owner Gym exterior; full reference reconstruction pending |
| Olivine City | Raster not inspected | Accepted exploration foundation + owner Gym; HGSS reconstruction pending; original office/residence/harbor plots must be preserved |
| Cianwood City | Raster not inspected | Old exploration layout + owner Gym exterior; full reference reconstruction pending |
| Mahogany Town | Raster not inspected | Old exploration layout + owner Gym exterior; full reference reconstruction pending |
| Blackthorn City | Raster not inspected | Old exploration layout + owner Gym exterior; full reference reconstruction pending |
| Johto Route 29 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 30 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 31 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 32 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 33 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 34 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 35 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 36 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 37 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 38 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 39 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 40 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 41 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 42 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 43 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 44 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 45 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 46 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 47 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Johto Route 48 | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Bellchime Trail | Raster inspected | Ecruteak QA05 source reconstruction; visual acceptance pending |
| Burned Tower | Raster missing/unverified | Ecruteak QA05 source reconstruction; visual acceptance pending |
| Bell Tower | Raster inspected | Ecruteak QA05 source reconstruction; visual acceptance pending |
| National Park | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Ruins of Alph | Raster missing/unverified | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Union Cave | Raster missing/unverified | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Ilex Forest | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Whirl Islands | Raster missing/unverified | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Mt. Mortar | Raster missing/unverified | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Lake of Rage | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Ice Path | Raster missing/unverified | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Dragon's Den | Raster missing/unverified | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Dark Cave | Raster missing/unverified | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Slowpoke Well | Raster not inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |
| Ecruteak Gym Exterior HGSS screenshot | Raster inspected | Existing exploration foundation; reference reconstruction and individual visual/collision review pending |

Canonical world geometry/entrances for all ten towns and Routes29–48 were recovered as reference facts this increment. Those30 source records do not implement30 reconstructions. See canonical_events/johto-outdoor-geometry.json and its extraction selection/provenance.

## Eight owner Gym facades

| City | Owner asset | Actual doors/collision | HGSS deviation |
|---|---|---|---|
| EcruteakCity | ecruteak, original pixels retained | Both door halves and4 facade probes; final logs/evidence in qa/hgss-qa06 | Deliberate owner Black Ledger addition |
| OlivineCity | olivine, original pixels retained | Both door halves and4 facade probes; final logs/evidence in qa/hgss-qa06 | Deliberate owner Black Ledger addition |
| VioletCity | violet, original pixels retained | Both door halves and4 facade probes; final logs/evidence in qa/hgss-qa06 | Deliberate owner Black Ledger addition |
| AzaleaTown | azalea, original pixels retained | Both door halves and4 facade probes; final logs/evidence in qa/hgss-qa06 | Deliberate owner Black Ledger addition |
| GoldenrodCity | goldenrod, original pixels retained | Both door halves and4 facade probes; final logs/evidence in qa/hgss-qa06 | Deliberate owner Black Ledger addition |
| CianwoodCity | cianwood, original pixels retained | Both door halves and4 facade probes; final logs/evidence in qa/hgss-qa06 | Deliberate owner Black Ledger addition |
| MahoganyTown | mahogany, original pixels retained | Both door halves and4 facade probes; final logs/evidence in qa/hgss-qa06 | Deliberate owner Black Ledger addition |
| BlackthornCity | blackthorn, original pixels retained | Both door halves and4 facade probes; final logs/evidence in qa/hgss-qa06 | Deliberate owner Black Ledger addition |

## Violet per-map inventory

| Map | Stable group:number | Reference | Services/coverage |
|---|---|---|---|
| VioletCity | 75:43 | MAP_VIOLET | Both-way doors/stairs in native controller tour; detailed save/collision tests recorded separately |
| VioletCity_Residence | 75:47 | MAP_VIOLET_BELLSPROUT_ONYX_TRADE_HOUSE | Both-way doors/stairs in native controller tour; detailed save/collision tests recorded separately; retained guest rest |
| VioletCity_Workshop | 75:48 | MAP_VIOLET_NORTHWEST_HOUSE | Both-way doors/stairs in native controller tour; detailed save/collision tests recorded separately |
| VioletAcademy | 75:63 | MAP_VIOLET_POKEMON_SCHOOL | Both-way doors/stairs in native controller tour; detailed save/collision tests recorded separately |
| VioletCity_PokemonCenter_1F | 75:44 | MAP_VIOLET_POKECENTER_1F | Both-way doors/stairs in native controller tour; detailed save/collision tests recorded separately; healing/PC/respawn |
| VioletCity_Mart | 75:45 | MAP_VIOLET_POKEMART | Both-way doors/stairs in native controller tour; detailed save/collision tests recorded separately; accepted shop stock |
| VioletCity_PokemonCenter_B1F | 76:31 | MAP_VIOLET_POKECENTER_B1F | Both-way doors/stairs in native controller tour; detailed save/collision tests recorded separately |
| VioletCity_Gym | 75:46 | MAP_VIOLET_GYM | Both-way doors/stairs in native controller tour; detailed save/collision tests recorded separately |
| SproutTower_1F | 75:54 | MAP_SPROUT_TOWER_1F | Both-way doors/stairs in native controller tour; detailed save/collision tests recorded separately |
| SproutTower_2F | 75:55 | MAP_SPROUT_TOWER_2F | Both-way doors/stairs in native controller tour; detailed save/collision tests recorded separately |
| SproutTower_3F | 75:56 | MAP_SPROUT_TOWER_3F | Both-way doors/stairs in native controller tour; detailed save/collision tests recorded separately |
| VioletCity_WestGate | 76:32 | MAP_VIOLET_ROUTE_36_GATEHOUSE | Both-way doors/stairs in native controller tour; detailed save/collision tests recorded separately |
| VioletCity_EastGate | 76:33 | MAP_ROUTE_31_VIOLET_GATEHOUSE | Both-way doors/stairs in native controller tour; detailed save/collision tests recorded separately |

## Unfinished

Most Johto streets/routes/landmarks/interiors still need their HGSS reconstruction. Generic exploration buildings remain outside the reconstructed areas even though the eight Gym exteriors are replaced. Violet DS lift mechanics, dynamic Sprout pillar, DS lightposts/elevation presentation and additional interior raster comparisons are not complete. The GBA interpretation and exact tested source/ROM are described in VIOLET_QA06.md and the release artifact manifest. Existing facilities remain useful; this checklist does not mark placeholder rooms polished.

## Next geographic section

Reconstruct Routes31/32/36 from their recovered geometry and inspected raster references, retaining current route and cave-mouth IDs. Then inspect the corresponding cave/ruins headers and room references. Continue source sections systematically; do not propagate a generic town template. Olivine original plot conflicts require a documented solution rather than deleting the office, residence or harbor.
