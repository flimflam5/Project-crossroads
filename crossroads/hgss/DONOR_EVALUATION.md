# Heart & Soul donor evaluation — 2026-11-17

## Recovered baseline

The new region directive authorizes Johto work beyond the earlier two-city pause.
The clean starting branch was `feature/qa10-download-delivery` at
`18212374f9277bf36185ce3412e38f32302139c3`; its parent is the latest game
and evidence revision `3138de89d9e57b816d3b7d03e727f04d69c2d168` on
`feature/olivine-port-ship-qa10`. The new evaluation branch is
`feature/johto-donor-evaluation-01`. No game content has been replaced in this
evaluation. Keep existing work, Joe, custom Gyms and the four Olivine additions;
preserve starter variable `0x40FA`, map/layout/heal IDs, old saves, approved
encounters, title and V5 music. Map group 75 has indices 0–126 in use: do not
allocate its reserved index 127.

The last tested QA10 ROM is SHA256
`ee2d81d5d0b55b7f1f9d36d1c9b055700164da439f51af7a66b5fb2d2147f90b`.
Its payload was 30,322,784 bytes in a 32 MiB image, leaving 3,231,648 bytes
before that capacity is reached. EWRAM was 226,448 bytes and IWRAM 28,392 bytes.
See [QA10 release](../RELEASE_OLIVINE_AQUA_QA10.md) for the exact emulator
coverage and the [location checklist](qa10/LOCATION_CHECKLIST.md) for remaining
limitations. Owner Delta and visual acceptance are pending. The latest delivered
build and evidence are available at the [QA10 release page](https://github.com/flimflam5/Project-crossroads/releases/tag/qa10-olivine-aqua-a1).

Ecruteak, Violet, and more recent Olivine/ship work have individual reference work;
most other Johto areas remain older connected exploration foundations. A valid
map entry is not evidence of finished HGSS reconstruction. The older
[region checklist](REGION_CHECKLIST.md) predates QA10 Olivine work and must be
read together with its newer checklist. There are 177 live entries in the two
Crossroads map groups; derive current links from live map files, not only the
older network manifest. Sailing to Vermilion and some services remain deferred.

## Donor and credit findings

[Pokémon Heart & Soul 2.0](https://github.com/PokemonHnS-Development/pokehns-expansion)
was inspected at master commit `167aa6d537b109bb229c231ddce4616974c4da71`.
Its [README](https://github.com/PokemonHnS-Development/pokehns-expansion/blob/167aa6d537b109bb229c231ddce4616974c4da71/README.md)
describes a GSC/HGSS blend based on Modern Emerald and RHH expansion 1.15.1,
calls it an open-source base for Johto hacks, and asks users to credit Pokémon
Heart and Soul and retain the full chain of credits as best possible. This
project uses expansion 1.17.2; do not merge the donor engine, save format, story,
player, event scripts or flags. The donor's own README warns that its pre-2.0
saves are incompatible. HGSS remains the authority for geography and appearance.

The GitHub license endpoint returned 404 and the inspected tree contained no
top-level license; individual asset terms and file-specific authorship were not
established. This observation is not a legal conclusion. Before distributing an
import, record its exact source files, revisions, modifications and available
upstream terms/credits; do not assume the person who imported a file authored it.
The donor's [in-game credits](https://github.com/PokemonHnS-Development/pokehns-expansion/blob/167aa6d537b109bb229c231ddce4616974c4da71/src/data/credits_hns.h)
list maps from Crystal Advance/Kertra, Fire Gold/blackfragrant and SkidMarc25;
tileset credits list Crystal Advance/Kertra, Ekat99, TheDeadHeroAlistair, Johto
Redrawn Team, zatavares852, lbsbezerra, WesleyFG and Kalarie. These are aggregate
credits, not proof that every listed person authored any particular map or tile.

## Contained structural probe

Donor `AzaleaTown_House1_hns` has an 11×10 map with 220 bytes of little-endian
map cells; it references `gTileset_Johto_Building_Hns` and `gTileset_Barn_Hns`.
Its map/event source contains donor-specific graphics, flags, warp destinations,
story and a reward. A raw `map.bin` copy would refer to foreign metatile IDs and
does not import the palettes, attributes, collision or valid Black Ledger events.
The donor uses a 640-entry primary metatile split; the usual Emerald-mode split
here is 512. This engine also has a separate FRLG path with a 640 split, but its
semantics and resource compatibility must be verified rather than assumed. Any
conversion needs to remap primary and secondary indices as well as all dependent
attributes and graphics.
This inspection is a data probe, **not** an imported room, emulator playtest or
proof of HGSS fidelity.

As a second candidate, the donor Route 29 source comprises:

| Pinned donor path | Git blob SHA | Size |
|---|---|---:|
| `data/maps/Route29_hns/map.json` | `5982f7579edf6553ef345447e5a617b7aa16e09f` | 9,028 B |
| `data/layouts/Route29_hns/map.bin` | `abb34db284cca6f78d52310bfd282370d76ee363` | 4,480 B |
| `data/layouts/Route29_hns/border.bin` | `a701312cfff9ef56ae960aed042d8b9e68eefb84` | 8 B |
| `data/tilesets/primary/johto_general_hns/metatiles.bin` | `db1b26a10fdac0a0e8f5eecdea93b0f934605a60` | 10,240 B |
| `data/tilesets/secondary/new_bark_town_hns/metatiles.bin` | `f226bb729cb31fd22994f42ce27ff296cb97460f` | 2,304 B |

These are candidates for source inspection, not a complete asset inventory.
Animations, images, palettes, attributes, border, warps and scripts require
separate review. Compare each candidate's actual HGSS reference before adapting.

## Resume safely

1. Preserve existing generated maps and save IDs. Choose one isolated donor room
   or route and record its complete source/credit/attribute dependencies.
2. Convert into a private destination tileset and Black Ledger-owned generator;
   map donor geometry to existing IDs and deliberate reciprocal warps without
   importing donor events. Preserve old-save arrival positions or add a tested,
   narrowly scoped migration where needed.
3. Inspect reference versus native 240×160 frames and test normal controller
   approaches, collision/layers, doors/stairs, entry and return, save/Continue,
   services and old saves. Measure ROM/RAM; run required generators and validators
   plus a real Emerald build. Do not claim a contained import passed before these.
4. Expand in geographic clusters only after the contained test. Maintain a
   per-area checklist of sources, original additions, deliberate deviations,
   missing content and runtime/owner visual coverage. Do not claim all of Johto
   complete while routes, interiors, landmarks or connections remain unverified.

At inspection the workspace filesystem had approximately 45 MiB free. A full donor
clone or new build may exceed this; retain existing ROMs, evidence and private
saves while arranging adequate build space. Do not delete them to create capacity.

Baseline checks run in this evaluation: `validate_opening.py`,
`validate_olivine.py`, `validate_olivine.py --built`,
`build_olivine_layout.py --check`, and
`build_johto_network.py --through west --check` passed. The built check used the
existing QA10 ROM; it is not a new build or a test of imported donor content.
