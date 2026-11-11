# Olivine completion review — QA09

This inventory distinguishes **registered implementation**, reference matching,
technical adaptation and actual delivery verification. It does not certify100%.
Final source revision, ROM SHA256, final controller tests and owner Delta visual
acceptance remain pending. V5 is diagnostic evidence only.

The inspected current inventory has **all nine canonical enterable city buildings**,
**four preserved Black Ledger additions** and **24 native city/interior/landmark maps**.
The authoritative source manifest is [OLIVINE_COMPLETION_QA09.json](OLIVINE_COMPLETION_QA09.json).

## Buildings and intended interiors

| Building | Classification | Registered interiors | Final verification |
| --- | --- | --- | --- |
| Gym | HGSS canonical enterable building | Gym, Gym_Arena | PENDING final delivery/Delta |
| Pokemon Center | HGSS canonical enterable building | PokemonCenter_1F, PokemonCenter_B1F | PENDING final delivery/Delta |
| Poke Mart | HGSS canonical enterable building | Mart | PENDING final delivery/Delta |
| Glitter Lighthouse | HGSS canonical enterable building | Lighthouse_1F, Lighthouse_2F, Lighthouse_3F, Lighthouse_4F, Lighthouse_5F, Lighthouse_6F, Lighthouse_Balcony, Lighthouse_Elevator | PENDING final delivery/Delta |
| Fishing house | HGSS canonical enterable building | FishingHouse | PENDING final delivery/Delta |
| Trade house | HGSS canonical enterable building | TradeHouse | PENDING final delivery/Delta |
| Seal house | HGSS canonical enterable building | SealHouse | PENDING final delivery/Delta |
| Cafe | HGSS canonical enterable building | Cafe | PENDING final delivery/Delta |
| Port terminal | HGSS canonical enterable building | PortTerminal, PortQuay | PENDING final delivery/Delta |
| Joe Mercer residence | deliberate Black Ledger addition | Residence | PENDING final delivery/Delta |
| Accepted neighbour residence | deliberate Black Ledger addition | NeighborHouse | PENDING final delivery/Delta |
| Silph subsidiary office | deliberate Black Ledger addition | SilphOffice | PENDING final delivery/Delta |
| Harbor Office | deliberate Black Ledger addition | HarborOffice | PENDING final delivery/Delta |

## Reference matching and deliberate adaptations

Canonical building entrances and relative geography come from actual HGSS city
mosaic and pinned map/event/prop facts. Three native homes use the actual shared
0097 house matrix and inspected trade-house screenshot. The cafe's actual raster
was also inspected: cream/checkered floor, communal table, right bar/staff area,
two rear windows and kitchen have native counterparts. Center/Mart common source
matrices exactly match the already tested GBA service adaptation; Olivine gets
private layouts while all historical shared service modules remain untouched.
The long Gym hall spans its two existing native map IDs; the approved owner Gym
art deliberately supersedes literal HGSS exterior art. Raised DS reception and
3D perspective are adapted to native GBA layers. DS online desks are offline.

Joe's residence, neighbour home, Silph subsidiary and Harbor Office are retained
as separate Black Ledger locations. Canonical homes are not silently repurposed
or deleted. Forest infill/commercial plots and the shifted western parasol fit
these additions. The GBA south-facing terminal requires a bounded east boardwalk
back to the city, retaining the northern covered approach. The cafe's visible
one-cell staff aisle avoids an inaccessible dry-floor pocket; its counter stays
solid and supports actual native over-counter interaction.

All six lighthouse floor IDs remain. The source fourth-floor window, exterior
balcony, isolated southern3F branch and western stair route are recorded as one
intentional traversal chain, with actual two-stop native lift behavior. Final
controller evidence must verify the chain and every visible stair/door segment.
The terminal and quay are separate maps with reciprocal main/side doors. S.S. Aqua
sailing, ship interiors and other-region arrivals remain explicitly outside this
map pass; accepted Harbor Office travel is preserved separately.

## Work still assigned before final build

- Source city moored sailboats and pennant arches are being added to the exterior.
- Landmark pass is correcting the port rear facade/ship scenery, gray maritime
  walls, balcony rail and actual lift-door graphics; source plant/floor identity
  review remains part of that pass.
- Small source home/cafe potted plants require final fixture review; the widened
  GBA bookcase currently absorbs the home plant corner, and the cafe raster has
  NW/SW pots not yet separately depicted in the audited output. Parent notified.
- Final source/build/checksum, full generation/static checks, normal controller
  doorway/traversal/collision/service/whiteout/save tests and native evidence.
- Owner Delta review and final visual acceptance.

These entries must be updated against the final generated outputs and delivery
binary. They are not permission to silently leave known work unimplemented.
Story gates, badges, reward/trade distribution, Seal Case and curated new
encounters remain deferred by the owner's design boundary, not invented here.

## Per-map register

| Map | Stable map identity (group,map) | Layout | Classification | Final verification |
| --- | --- | --- | --- | --- |
| OlivineCity | `MAP_OLIVINE_CITY` (75,0) | `LAYOUT_OLIVINE_CITY` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_Residence | `MAP_OLIVINE_CITY_RESIDENCE` (75,1) | `LAYOUT_HOUSE_WITH_BED` | Black Ledger addition | PENDING |
| OlivineCity_NeighborHouse | `MAP_OLIVINE_CITY_NEIGHBOR_HOUSE` (75,2) | `LAYOUT_HOUSE_WITH_BED` | Black Ledger addition | PENDING |
| OlivineCity_Gym | `MAP_OLIVINE_CITY_GYM` (75,3) | `LAYOUT_OLIVINECITY_GYM` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_PokemonCenter_1F | `MAP_OLIVINE_CITY_POKEMON_CENTER_1F` (75,4) | `LAYOUT_HGSS_OLIVINECITY_POKEMONCENTER_1F` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_Mart | `MAP_OLIVINE_CITY_MART` (75,5) | `LAYOUT_HGSS_OLIVINECITY_MART` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_SilphOffice | `MAP_OLIVINE_CITY_SILPH_OFFICE` (75,6) | `LAYOUT_OLIVINE_SILPH_OFFICE` | Black Ledger addition | PENDING |
| OlivineCity_HarborOffice | `MAP_OLIVINE_CITY_HARBOR_OFFICE` (75,7) | `LAYOUT_OLIVINE_HARBOR_OFFICE` | Black Ledger addition | PENDING |
| OlivineCity_Lighthouse_1F | `MAP_OLIVINECITY_LIGHTHOUSE_1F` (75,18) | `LAYOUT_OLIVINECITY_LIGHTHOUSE_1F` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_Lighthouse_2F | `MAP_OLIVINECITY_LIGHTHOUSE_2F` (75,19) | `LAYOUT_OLIVINECITY_LIGHTHOUSE_2F` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_Lighthouse_3F | `MAP_OLIVINECITY_LIGHTHOUSE_3F` (75,20) | `LAYOUT_OLIVINECITY_LIGHTHOUSE_3F` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_Lighthouse_4F | `MAP_OLIVINECITY_LIGHTHOUSE_4F` (75,21) | `LAYOUT_OLIVINECITY_LIGHTHOUSE_4F` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_Lighthouse_5F | `MAP_OLIVINECITY_LIGHTHOUSE_5F` (75,22) | `LAYOUT_OLIVINECITY_LIGHTHOUSE_5F` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_Lighthouse_6F | `MAP_OLIVINECITY_LIGHTHOUSE_6F` (75,23) | `LAYOUT_OLIVINECITY_LIGHTHOUSE_6F` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_Gym_Arena | `MAP_OLIVINECITY_GYM_ARENA` (75,33) | `LAYOUT_OLIVINECITY_GYM_ARENA` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_FishingHouse | `MAP_HGSS_OLIVINECITY_FISHINGHOUSE` (76,34) | `LAYOUT_HGSS_OLIVINECITY_FISHINGHOUSE` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_TradeHouse | `MAP_HGSS_OLIVINECITY_TRADEHOUSE` (76,35) | `LAYOUT_HGSS_OLIVINECITY_TRADEHOUSE` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_SealHouse | `MAP_HGSS_OLIVINECITY_SEALHOUSE` (76,36) | `LAYOUT_HGSS_OLIVINECITY_SEALHOUSE` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_Cafe | `MAP_HGSS_OLIVINECITY_CAFE` (76,37) | `LAYOUT_HGSS_OLIVINECITY_CAFE` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_PokemonCenter_B1F | `MAP_HGSS_OLIVINECITY_POKEMONCENTER_B1F` (76,38) | `LAYOUT_HGSS_OLIVINECITY_POKEMONCENTER_B1F` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_Lighthouse_Balcony | `MAP_OLIVINE_CITY_LIGHTHOUSE_BALCONY` (76,39) | `LAYOUT_OLIVINE_CITY_LIGHTHOUSE_BALCONY` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_Lighthouse_Elevator | `MAP_OLIVINE_CITY_LIGHTHOUSE_ELEVATOR` (76,40) | `LAYOUT_OLIVINE_CITY_LIGHTHOUSE_ELEVATOR` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_PortTerminal | `MAP_OLIVINE_CITY_PORT_TERMINAL` (76,41) | `LAYOUT_OLIVINE_CITY_PORT_TERMINAL` | HGSS geometry / GBA adaptation | PENDING |
| OlivineCity_PortQuay | `MAP_OLIVINE_CITY_PORT_QUAY` (76,42) | `LAYOUT_OLIVINE_CITY_PORT_QUAY` | HGSS geometry / GBA adaptation | PENDING |

Each JSON map record includes exact native doors/warps/connections, source header
and blob provenance, source prop model counts, object/service inventory and
adaptations. No record marks final emulator or owner acceptance passed before
those tests run on the actual uniquely identified delivery ROM.
