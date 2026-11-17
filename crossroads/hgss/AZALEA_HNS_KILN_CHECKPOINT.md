# Azalea Charcoal Kiln — donor integration checkpoint

Status: source and generated assets are in progress on
`feature/johto-donor-evaluation-01`. **A completed build, actual door and movement
playtest, old-save test on the new ROM and owner visual review are pending.** This
is one location in an otherwise unfinished regional reconstruction, not a claim
that Azalea or Johto is complete.

## Implementation scope

- Adds `AzaleaTown_CharcoalKiln` as map **76:50**, retaining existing map and
  layout order. The indoor map is 11 × 10; its exit at (5,8) targets Azalea's
  appended warp index 7. Azalea remains **75:64**, with a new exterior entrance
  at (20,33). Its existing seven warp indices remain in place. The kiln is a
  separate map; the existing `AzaleaTown_Workshop` and its old map ID and events
  are not replaced.
- Takes the Heart & Soul Azalea House1 room's geometry and used artwork through
  `crossroads/tools/build_hns_charcoal_kiln.py` into a privately registered
  Emerald-format tileset. The converter maps 37 donor metatiles, 79 referenced
  8 × 8 graphics and five palette banks. It keeps donor floor, display attributes,
  collision and elevation outside a nine-cell blocked brick kiln drawn for this
  project. The room has a Black Ledger worker and exit, not the donor's
  progression, event flags, reward, trainers or storyline.
- `crossroads/tools/hns_kiln_facade.py` converts a 4 × 4 Heart & Soul facade
  into unallocated Azalea city resources and adjusts the door behavior for the
  Emerald engine. `build_eight_gym_integration.py` and `build_johto_network.py`
  own the generated facade and town warp respectively; their checks must pass
  after any future changes. Existing Azalea Gym resources share that city's
  packed secondary tileset, so the validation explicitly checks the Gym artwork
  and unchanged area in addition to the new donor facade; do not assume a new
  tileset file means the rest of the city is untouched.

The donor uses a 640-entry primary metatile split; the usual Emerald-mode split
is 512. The packed conversion remaps the used data and palettes. Retaining a
map ID does not guarantee a save's exact coordinates remain safe: the new town
facade changes a 4 × 4 footprint and old in-town saves require movement and
Continue checks. A genuine QA10 Workshop save has been captured for a future
new-ROM cold-Continue test; the fact it was captured is not a pass on the new
ROM. Party, boxes, starter data and save structure have not been intentionally
changed, but compatibility remains subject to actual runtime regression.

## References and attribution

Source: [Pokémon Heart & Soul](https://github.com/PokemonHnS-Development/pokehns-expansion/tree/167aa6d537b109bb229c231ddce4616974c4da71),
commit `167aa6d537b109bb229c231ddce4616974c4da71`. Exact source paths and
SHA-256 hashes are recorded in `crossroads/donor/hns-charcoal-kiln/source-sha256.json`
and `crossroads/donor/hns_azalea_exterior/provenance.json`. The donor asks for
Heart and Soul and upstream contributor credit; its aggregate credits include
Crystal Advance / Kertra, Fire Gold / blackfragrant, SkidMarc25, Ekat99,
TheDeadHeroAlistair, Johto Redrawn Team, zatavares852, lbsbezerra, WesleyFG
and Kalarie. Attribution of individual files and their explicit redistribution
terms remains unverified; see `DONOR_EVALUATION.md`.

The HGSS reference places the kiln east of the Gym; the existing extracted
`MAP_AZALEA` geometry records its entrance at (35,20) in the HGSS 64 × 32 city.
The current 48 × 44 Azalea foundation is not the same geometry: the new entrance
is east of the current Gym at (20,33), an interim placement to be revisited with
the city's HGSS reconstruction. The [HGSS kiln reference](https://guidestrats.com/pokemon-hgss-charcoal/)
shows a larger workroom with a brick kiln, raised wooden workspace and furnishings.
The donor room plus original kiln overlay is a GBA adaptation and is **not**
claimed to match that reference. Preserve the separate workshop and existing
services when reconstructing the surrounding town.

## Checks and outstanding work

At this checkpoint, the following source-only checks have been run:

- `python3 crossroads/tools/build_hns_charcoal_kiln.py --check` passed.
- `python3 crossroads/tools/validate_hns_charcoal_kiln.py` passed for 101
  preserved donor cells, nine deliberate blocked kiln cells, remapped 8 × 8
  graphics/palettes and a 51-cell conservative walkable component. This static
  model does not establish real movement, priority, visual quality or save safety.
- `python3 crossroads/tools/validate_eight_gyms.py` passed its owner Gym pixel,
  legacy-area, new facade and conservative old-cell escape assertions.
- `python3 crossroads/tools/build_johto_network.py --through west --check`
  passed for the current 178-map generated network and atlas.

Before calling the area playable, complete and record:

- [ ] Remaining map, opening and Olivine regression checks, including the
      Emerald map inclusion check, without weakening existing assertions.
- [ ] Fresh Emerald build and measured ROM, EWRAM and IWRAM use; identify the
      exact ROM hash and source revision used by every runtime test.
- [ ] Controller-driven approach, entrance and exit from both directions, walking
      away from the arrival, building/tree collision and layering, interaction,
      save and cold Continue on the delivery ROM.
- [ ] Copied genuine QA10 save Continue and exit, including an old Workshop save
      and old Azalea positions around the changed facade; starter/party checks.
- [ ] Native in-game screenshots and comparison with HGSS; owner Delta and visual
      review. Mark any HGSS differences or unfinished furnishings explicitly.

Route 33's next-step reference and donor comparison is tracked in
`ROUTE33_DONOR_CHECKLIST.md`. All other Johto cities, routes, caves, landmarks,
interiors and transport still require individual implementation and verification;
the existing connected network does not establish that they are complete.
