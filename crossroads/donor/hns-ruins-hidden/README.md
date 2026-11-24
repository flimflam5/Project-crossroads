# Ruins second and hidden-room prototype

This branch registers four distinct GBA prototype maps for the southwest and
northwest second rooms and their separate hidden rooms. The source geometry is
pinned to public pret HGSS commit `6bf138d6035aa6b43d6f8f4132a12df70f86dcec`.
`crossroads/tools/extract_hgss_ruins_hidden_reference.py` validates the
public terrain archive Git blob `33105ab54c804a33503fb52db0ffa93a4d38191a`,
source event/script blob hashes and the extracted numeric permission planes.
No DS graphics or commercial ROM data are stored here.

Both second rooms have HGSS's 115-cell walkable footprint, exit back toward
their own first room at (6,17), and fall at (6,3) into their own hidden room.
Northwest and southwest hidden-room arrival/exit positions are (11,14)/(20,21)
and (11,7)/(20,13). Their fall scripts target the reference Underground Hall
positions (5,24) and (5,42), respectively. The Hall uses a separate 32×64
layout and retains its map ID and old 29×32 layout for save migration.

The Water Stone gate requires using the stone while facing the correct wall;
it does not consume the stone. The Ho-Oh gate checks the player's party and
excludes eggs. Both walls open only for the current map visit and reclose on
reload; HGSS's persistent-open state is deliberately deferred because safe
unused save flags are not yet proven. Each first-room original exit remains
warp 0. A neutral arrival-only warp 1 at (5,2) provides a safe return if the
condition changes, and the open-wall entry is warp 2. No persistent flags,
item rewards, trainers, NPCs, or story events are added. In particular, the
four stone plinths in each second room correspond to HGSS item positions but
currently grant nothing. The 30 Hall markers and the hidden-room inscriptions
are visual only; their interactions and text remain unfinished.

GBA art is adapted from Pokémon Heart & Soul donor revision
`167aa6d537b109bb229c231ddce4616974c4da71`; the input hashes are in
`source-sha256.json`. The hidden inscriptions are spaced across the reference
footprints and are not claimed visually identical to HGSS's 3D originals.
The donor's north-door shortcuts have been replaced with source-backed falls.
The hall-entry corridor, temporary gate presentation and foreground layering
remain GBA adaptations requiring owner review.

HNS requests full credits. Its aggregate list attributes map work to Crystal
Advance / Kertra, Fire Gold / blackfragrant and SkidMarc25; tileset contributors
include Crystal Advance / Kertra, Ekat99, TheDeadHeroAlistair, Johto Redrawn
Team, zatavares852, lbsbezerra, WesleyFG and Kalarie. These are aggregate
acknowledgements, not attribution of particular files; file-specific terms
remain unverified.

`test_hgss_ruins_hidden_stage.py`, `test_hgss_ruins_hidden_graph.py`,
`test_hgss_ruins_gate_candidates.py`, `validate_hgss_ruins_hidden_installed.py`
and `test_hgss_ruins_mapjson.py` check source footprints, transition indices,
field elevations, donor gate pixels, no item/flag grants and Emerald map
inclusion. `test_alph_trigger_runtime.py` exercises the actual C predicate and
item dispatch in host mocks. These are not a full ROM build or gameplay test.
Actual Water Stone use, Ho-Oh/egg cases, every doorway and fall, reloads,
old-save compatibility, collision, graphics and owner visual acceptance remain
unverified until tested in the delivered emulator build.
