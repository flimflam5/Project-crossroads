# Olivine canonical exterior details — QA09

The actual HGSS city mosaic and pinned outdoor matrix props identify two moored
sailboats (model119) and three pennant street arches (model121). Their original
GBA artwork is `art/olivine/harbor-decor-source.png`; no HGSS textures are embedded.
The three canonical parasols were already reconstructed separately.

The native sailboat is96x80 pixels, instantiated twice. The mast/sails are a
foreground overhang; native sea graphics/Surf behavior/elevation remain beneath
it. Only the visible lower hull rows block movement. The actual seawall is
retained. Source DS ship-model collision footprints that the first ground pass
misread as cliff blocks become the correct boat-over-water composition.

The arches are112x48 pixels, with five unobstructed road cells between two posts.
Only the post bases block; the pennants render above Joe. Every opening retains
plain paved ground without warp/arrow behavior.

Necessary GBA/Black Ledger fit deviations are explicit:

- Boat origins are13,45 and30,45. The eastern instance shifts roughly three tiles
  east to keep the terminal's functioning external boardwalk clear. The mast
  silhouette also fits below the parasols instead of overwriting their graphics.
- The north arch starts20,7 so it lies beyond the seven-tile resource buffer at
  the Route39 seam; this prevents graphics corruption while crossing maps.
- The western arch starts7,16, shifted north of its DS ground-prop coordinate to
  preserve the accepted Black Ledger homes in the western housing court.
- The central arch starts20,28. The five-wide main street remains unobstructed.
- The new Olivine lighthouse's upper roof/spire and port roof use bilateral
  graphics modules so the details fit the GBA pool. These are the newly authored
  Olivine facades; all owner Gym pixels and accepted Black Ledger buildings remain
  protected, with exact source-pixel regression checks.
- The southern bound is visibly ocean, with normal GBA map-edge collision, rather
  than a forest hedge across the sea. No new regional connection is introduced.

The asset dry-run measures657 new graphics and144 free slots before the owner's
115-glyph Gym integration. Final generated counts, native preview, exact-ROM
movement tests and checksum must be recorded by the delivery checkpoint. Static
`validate_olivine_harbor_details.py` checks foreground/collision footprints,
water behavior, sea underlays, five-wide arch clearance and ocean boundaries.
It is not itself a controller or visual acceptance test.
