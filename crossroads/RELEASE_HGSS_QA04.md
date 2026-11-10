# Black Ledger QA04 — working Johto QA Fly

Retains QA02 boundary/entrance/tree fixes and QA03 optional Pidgeot/Running Shoes.
Claim the kit by holding R while talking to the left survey sailor in Olivine
Harbor Office, then Yes. Have one party slot free. Existing QA03 recipients do
not need another Pidgeot; the same saved one-time marker enables this QA access.

Outdoors: Pokemon -> Pidgeot -> Fly. The Johto QA Fly map cycles among all ten
existing town/city landing points. D-pad chooses a city, A flies, B cancels back
to the party menu. The engine's existing departure/arrival animation is retained.
Routes/caves/landmarks are informational labels, not selectable landing points.

All ten destinations are available for this explicit QA kit, including places
not yet visited, to facilitate the requested map testing. No badges, city-unlock
flags or story progress are granted. This is development access, not a permanent
creative decision about the eventual game's Fly progression. Without the kit,
normal field-move unlock rules remain unchanged. Indoor departure remains blocked.
Ordinary field/wall atlas use remains informational and does not fly the player.

Destination IDs come from the existing heal-location data and are generated with
the atlas; current arrivals are outside each Center. Existing map/layout/heal IDs,
last-heal behavior and save structures are unchanged. Ecruteak uses its updated
(45,56) arrival. Native Fly does not replace normal Center healing/respawn choice.

Delta QA: back up a battery save; normal Continue (no older emulator state), claim
kit if needed; try Fly from an outdoor road/city, cancel once, then fly Olivine ->
Ecruteak -> another town and back. Check arrival/collision, enter/exit the Center,
then save normally, reset and Continue. Confirm Pidgeot, starter, Running Shoes,
party and inventory. Do not infer that unfinished maps/interiors are accepted.

## Verification performed

Emerald build PASS: ROM29,540,616bytes used (padded32MiB); EWRAM226,448bytes,
IWRAM28,392bytes. Opening/starter, Olivine, western Johto, area completion,
visual/save-contract, network/build-inclusion, atlas/generator and safe Fly
arrival checks PASS. Actual controller party-menu Fly/B cancel PASS; native
animated flights to all ten towns/cities landed at the expected heal coordinates
PASS; starter, party count and badge flags retained. Normal post-flight menu Save
and fresh-core title/Continue preserved exact party and position, and Fly reopened
PASS. Screenshots and coverage are packaged separately from private test saves.
Owner Delta QA remains pending; this is not visual acceptance of the full region.
