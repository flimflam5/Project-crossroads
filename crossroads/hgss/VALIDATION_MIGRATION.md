# Validation migration for the HGSS reconstruction

The0.9.1 screenshots, manifest and assertions describe that historical release.
They are retained as evidence; their geometry is not an HGSS golden reference.

Authorized changes in the current Ecruteak stage:

- Replace projected48x48/64x50 draft geometry with the verified64x64 logical area.
  The HGSS world matrix assigns header78 to cells(11,4),(12,4),(11,5),(12,5).
  Translate event coordinates by(-352,-128), keeping actual relative entrance spacing.
- Preserve all seven existing city warp indices/destinations, scripts, graphics IDs,
  map/group/layout/heal IDs. Only physical coordinates and reciprocal route offsets
  change. The missing canonical house/gates/station chain are explicitly unfinished.
- Update Ecruteak's existing heal-location coordinates to its relocated Center door.
- Convert only the seven-tile terrain buffers adjoining the city to compatible
  native terrain, retaining collision/elevation, signs and encounter-grass behavior.
- Refresh primary graphics/palettes/animations only when a scrolling transition
  actually changes the primary tileset. Other transitions retain their old behavior.

validate_hgss_ecruteak.py supplies replacement semantic assertions for those exact
changes: all map/layout/heal identities; all unrelated metadata; old event scripts,
IDs and destinations; canonical entrance coordinates; full public-ground connectivity
(no old-save canopy pockets); exact limited buffer transformations; and preserved
General terrain/animation graphics slots. Neither it nor a build proves visual fidelity.

Before updating historical exact-layout checks, run the replacement checks and
record actual movement/save/graphics results. Do not silently refresh a snapshot
hash to bless arbitrary edits or remove reciprocal-warp/reachability assertions.

## Canonical tower floor migration (QA05 development)

The old validators assumed that every floor was one connected rectangular room
and every exit could be reached from warp0 without changing floors. Actual HGSS
Bell Tower has one-way plank jumps, branching stairs and same-map teleport pads.
Those assumptions reject the correct reference graph and cannot test ledges.

The thirteen explicitly reviewed Bell/Burned floors now use
hgss_tower_validation.py: source-SHA-backed stair coordinates and destination
anchors, unchanged legacy map/layout IDs/ambient scripts, valid native metatiles,
all exits reachable from outdoors, and a directed route outside from **every
public tile**, with NPC collision included. The global Johto flood also models
native two-tile directional jumps. Other maps retain their old local exit checks.
No reciprocal-warp, source-coordinate or escape assertion was removed to bless a
failure. A blocked-passage NPC actually failed the new escape check and was moved.

The emulator helper now plans by entry position (not just map name), and taps a
ledge once then releases the button while the jump finishes. Holding40frames
repeatedly jumped past the intended landing: that was a test-controller error.
These tests do not certify visual fidelity, owner acceptance, or an unplayed mode.

## Houses, services, gates and respawn

The explicit room/service/gate review manifests replace only their corresponding
old geometry hashes. New checks retain source door/bridge coordinates, old IDs and
actor scripts/local IDs, paired destinations, all public-floor escape, five safe
performance steps, every Gym fall trigger and all road-width gate aliases. Shared
HouseWithBed/Mart/OlivineCenter layouts remain pinned. Unrelated maps still use
the historical exact metadata/layout assertions. Western scripts now include the
new gate file, and side gates require lateral approaches instead of south-only
building approaches. This does not exempt their reachability.

The Center's supported respawn_x/respawn_y metadata now explicitly uses(8,13).
No heal IDs or save structs change. Emulator testing caught both the old default
(7,4) whiteout arrival and the native escalator's sideways arrival into a blocked
corner; geometry/respawn metadata were fixed, not the assertions. The old shared
layout fixture deliberately changes only the private test copy's cached layout ID,
saves through the normal menu, then cold-boots/Continues and requires migration.

--starters-only retains the original Olivine doors/rescue/duplicate/VRAM checks,
then exits before its obsolete pre-HGSS hardcoded western tour. The replacement
controller tour follows current JSON/native ledges and tests the complete reviewed
Ecruteak graph. A passing short starter test is never reported as a region playtest.
