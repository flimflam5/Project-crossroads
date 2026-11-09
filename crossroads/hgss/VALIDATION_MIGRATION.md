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
