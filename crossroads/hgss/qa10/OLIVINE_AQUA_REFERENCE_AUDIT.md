# Olivine / S.S. Aqua reference audit — QA10

This audit starts from delivered QA09 source
`285cfa4ebddcb390a8a5bde6116748cbb5eaba6b`. It records actual HGSS reference
facts for the owner's new physical port/ship work. It does not report any new
map as implemented, built, playtested or visually accepted.

## What the reference recovery established

All seven S.S. Aqua interior headers are recovered from SHA-pinned public pret
reference data. They contain a passenger corridor, four paired cabin maps
(eight separate cabins), captain's cabin and the lower deck. The lower deck
contains a crew dormitory, galley and substantial engine room, not one empty hall.

Complete published HGSS map mosaics were found and inspected for the corridor,
all eight cabins, lower deck and captain's cabin. Eight additional native
256×192 gameplay views corroborate materials and furniture. The references
support purposeful individual rooms rather than generic furnished copies.

| Source header | Matrix / terrain chunks | Reference-matched physical purpose |
| --- | --- | --- |
| `MAP_SS_AQUA_1F` |0171 /643,644|Orange/gold passenger corridor, four vertical lounge benches plus two horizontal settees, portholes/life rings/planters, eight cabin hatches, entrance vestibule, two lower-deck stairs and east captain approach. |
| `MAP_SS_AQUA_CAPTAIN_ROOM` |0172 /645|Green striped floor/rug; chart desk, berth, sofa, tall bookcase, kitchenette/fridge, framed charts/windows. |
| `MAP_SS_AQUA_1F_SOUTHEAST_ROOMS` |0173 /646|Left: red sleeping-sailor cabin with portrait berths placed side by side and rear TV/kitchen. Right: mustard player/rest cabin with berth, four-stool table and rear fixtures. |
| `MAP_SS_AQUA_1F_SOUTHWEST_ROOMS` |0174 /647|Left: blue carpet, berth and dining table. Right: gold carpet, four-stool table, bookcase and picture. |
| `MAP_SS_AQUA_1F_NORTHEAST_ROOMS` |0175 /648|Left: red carpet, vertically arranged twin berths and two rear desks. Right: mustard room with berth and four-stool table. |
| `MAP_SS_AQUA_1F_NORTHWEST_ROOMS` |0176 /649|Left: blue grandfather cabin with berth and table/two diagonal red stools. Right: gold twin-bed cabin with yellow sofa. |
| `MAP_SS_AQUA_B1F` |0177 /650,651|Six-bed crew quarters with wardrobe/ladder units; six-chair galley with kitchen/fridge; metal engine bay with yellow hazard edging, equipment and stairs; perimeter corridor and western alcove. |

The four paired cabin maps have two genuinely separate floor components. Do not
connect them through walls to make traversal easier. Zero separate prop records
in a cabin does not mean it is empty: DS room terrain embeds beds, tables, sofas
and cabinetry. Geometry, visible furniture and event data must be considered
together.

The published cabin mosaic is arranged by ship geography: top row is northwest
left/right then northeast left/right; bottom row is southwest left/right then
southeast left/right. The actual source rest trigger is southeast right
coordinate(16,4), while the grandfather lives northwest left. These are HGSS
reference roles, not authorization to copy their quest into Black Ledger.

## Files and reproducibility

[Reference manifest](ss-aqua-reference-manifest.json) records all image URLs,
published dimensions and SHA256 checksums, plus30 SHA-pinned matrix/event/script/
message source files. [Seven-map stripped geometry](ss-aqua-geometry.json)
contains permissions, prop anchors, warps and actor positions, not DS textures
or raw model assets. [Selection](ss-aqua-reference-selection.json) identifies
the exact seven header/matrix/event triples.

Reference repository commit:
`pret/pokeheartgold@6bf138d6035aa6b43d6f8f4132a12df70f86dcec`.
Existing public terrain-reference archive Git blob:
`33105ab54c804a33503fb52db0ffa93a4d38191a`.
The standard project's extractor validated every downloaded Git blob and the
archive before producing these facts. Its independently computed public-floor
crops retain the source origin: corridor57×21, captain14×13, each paired cabin
28×13, lower deck57×21. The blocked permission flag is `0x8000`.

Original reference images/cache files remain under
`/workspace/scratch/hgss-reference`. The new full-floor files are:

- `SS_Aqua_1F_HGSS.png` —912×288.
- `SS_Aqua_1F_Rooms_HGSS.png` —912×384.
- `SS_Aqua_B1F_HGSS.png` —1056×288.
- `SS_Aqua_Captain_Cabin_HGSS.png` —224×192.
- `SS_Aqua_room_HGSS_reference_385.png` through `392.png` —256×192 each.

They are documentary comparisons. No screenshot pixels, source scripts, raw
NARC or commercial ROM are imported into game assets by this audit.

## Furniture interpretation safeguards

Actual inspected references identify source model17 as the six lower-deck beds,
model20 as kitchenette/sink/stove,21 as fridge,22 as green waste bin,23 as plant,
53 as stool/chair,60/139 as framed wall pictures and164 as engine equipment.
Some furnishings are embedded in terrain, independent of these prop models.

Do not apply temple-specific model assumptions to the ship: Captain model65 at
(1.5,3.0) corresponds to the rear-left bookcase in this reference, not the
`pillar_big` used by the generic temple projector. Model162 anchors accompany
cabin hatch panels and must not become arbitrary aisle obstacles. The small
round gray/white southeast-right rear fixture is visually recorded; its exact
purpose remains unverified and should not be invented in dialogue.

## Boarding and sailing are different requirements

QA09 deliberately bounded S.S. Aqua boarding and did not contain ship maps or a
voyage system. The owner's new directive now authorizes physical ship interiors.
It does not supply a Black Ledger Kanto destination, ticket/fare policy, schedule
or main-story unlock.

Actual HGSS behavior is not a drop-in travel system:

- Olivine reception checks game-clear state and the S.S. Ticket. Its pre-clear
  maintenance message is intentional in the original game.
- First departure sets boat direction/arrival/scene state. The sleeping sailor,
  missing granddaughter, captain and grandfather sequence controls arrival in
  Vermilion. Importing it would establish an unrelated quest and rewards.
- Repeat Olivine departures are Mondays and Fridays; sleep in the player cabin
  advances later voyages. Those rules are not automatically Black Ledger canon.
- The corridor source stores Olivine and Vermilion exit warps at the same
  coordinate(24,19). Its load script moves the selected exit to(27,20), according
  to `VAR_BOAT_DIRECTION`. A fixed Olivine dockside visit needs one reliable
  reciprocal Olivine return, not both competing destinations.
- Source grandfather Metal Coat and captain badge/daily plate gifts are story/
  reward dependencies. They must not be copied as a shortcut to apparent content.

Physical boarding/exploration and disembarking can work at Olivine while sailing
remains explicitly unavailable for the real missing-destination/design reasons.
The wording should explain that boundary without falsely presenting an engine
maintenance problem as completed travel or an approved plot event.

## Reported signed lot — exact new screenshot identification

The newly supplied D187C84F photos1–2 show **Ecruteak City**, not Olivine: the
courtyard west of the Dance Theater, with the directory at(36,45).
The actual pinned HGSS Ecruteak event data has a background sign at exactly
(36,45), and its city mosaic shows the vacant public courtyard there. Root's
normal-controller capture reproduces the same court, sign and surrounding Gym.
It is not evidence of a missing canonical building and must not be filled with
an invented structure to conceal a real source reference.

The earlier Olivine(24,42) directory hypothesis is superseded by this new exact
match. That Olivine sign is independently canonical, but is not the photograph.
All nine Olivine canonical enterable destinations remain in the inventory.

Actual Route40 separately has paired(13,10)/(14,10) entrances to its Frontier
gatehouse, absent in the old native route. This remains a documented geographic
gap for separately authorized route work; it is not the photographed city lot.

Owner photo4 is the Olivine Lighthouse1F tourist deck. New individual HGSS floor
rasters reveal genuine omitted floor/furniture detail there, independent of the
courtyard identification. See [the lighthouse reference/visual correction audit](LIGHTHOUSE_VISUAL_REFERENCE_QA10.md).

## Limits and required downstream testing

Published full-map mosaics have different perspective/framing from GBA240×160
views; flat native artwork requires documented adaptations. Full reverse-quay
coverage is less complete than the now-recovered ship interior coverage. Physical
map facts do not prove art fidelity, clearances, layer priority, doors or services.

Implementation must still be built, inspected at native resolution and tested
with normal controller movement on the actual delivery ROM: all hatch leaves,
reciprocal warps/arrival/facing, paired cabins independently, stairs, equipment/
furniture collision, water/body/roof priority, NPCs/signs and copied-save cold
Continue. Owner Delta/visual acceptance remains separate.
