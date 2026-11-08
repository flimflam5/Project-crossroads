# Updated owner title reference — Pokémon: Black Ledger

On 2026-11-08 the owner supplied a new title image reading **Pokémon: Black Ledger**,
presented by **Voidstar Interactive**. This explicitly supersedes the earlier
Project Crossroads harbor title proposal below, including its title treatment.
Use the new supplied image for the next title-screen prototype. Its coat artwork
is title illustration, not approval to replace Joe's corporate gameplay outfit.
The engine/repository identifiers and save contracts remain unchanged.
No Black Ledger title graphics are implemented in the current Route 39 increment.

---

# Title-screen visual direction — owner approved

![Harbor title proposal](harbor-proposal.png)

Original generated concept for Pokémon: Project Crossroads: navy/charcoal Olivine
harbor, Silph office/freight quay, muted teal lights, burgundy accents and lighthouse.
This illustration was generated for the project; it is not copied game art.
The owner approved this visual direction on 2026-11-08 with the requirement to use
the official game title: Pokémon: Project Crossroads. The approval is for the
visual direction; the artwork is not yet integrated or runtime-verified.

Source PNG: 1536×1024. Native target: 240×160, 3:2, palette/tile limits and legibility
verified in an emulator. The concept image is not claimed to meet those constraints.
Do not silently treat it as an engine-ready sprite sheet or palette asset.

After art-direction review, implement a separate title-screen prototype using the
existing graphics/sound systems. Test Start, main menu, New Game, Continue and reset.
Keep the accepted exploration/met-location increment independently buildable. Audio
may use an explicitly identified temporary existing engine track until original or
appropriately licensed new music is ready. This proposal does not change gameplay,
menus, save data, protagonist graphics or the original introduction.

Architecture inspected: src/intro.c handles boot/copyright and old introductory
animation; src/title_screen.c initializes the Emerald logo, version sprites,
Rayquaza/cloud backgrounds and Start transition; src/main_menu.c owns Continue and
Birch/new-game presentation; src/new_game.c still selects the truck start. Preserve
these underlying contracts when replacing the presentation. Do not remove legacy
assets needed by legitimate later Hoenn content.
