# Black Ledger 0.6 — Route 38 and Ecruteak foundation

A continuous on-foot network now connects **Olivine → Route 39 → Route 38 →
Ecruteak**, with working return connections. Route 39's former north boundary is
open. Route 38 turns east toward Ecruteak, with scenery, signs and pedestrians.
Ecruteak has seven enterable locations: Burned Tower entrance, Bell Tower entrance,
a residence, Dance Theater lobby, Gym lobby, Pokémon Center and Mart.

The Center heals the party and registers Ecruteak as its respawn destination.
The Mart reuses the accepted basic stock and clerk logic. Tower/Gym/theater rooms
are explicitly temporary lobbies. No tower progression, Gym battles or badges are
claimed. Routes 37/42 remain closed and labeled. No route encounters or trainer
teams were added before regional balancing. Existing Emerald tiles/music remain
placeholders for the eventual Johto art/audio pass.

## Preserved baseline

The owner accepted Black Ledger 0.5: “Everything works as expected.” The approved
harbor title, Joe corporate sprites, Olivine exploration/services, office rescue,
level-5 Olivine acquisition metadata and duplication guards remain intact. Old
Pokémon data is not migrated. Existing map IDs 75.0–75.8 and all existing valid
map-section/layout/heal IDs retain their ordering; new entries append. No save
structure changes or engine upgrade were made. The summary UI is unchanged.

## Verification

BUILD PASS: Emerald linked ROM 26,825,252 bytes, EWRAM 226,424, IWRAM 28,392.
AUTOMATED TEST PASS: source/script/asset checks, generated Emerald map inclusion,
reciprocal connections/warps, cross-map pedestrian reachability for every new door,
outdoor NPC/sign and respawn point, and reproducible city/route layouts.

EMULATOR TEST PASS: both saved gender fixtures crossed all map borders in both
directions, entered/left all seven Ecruteak interiors, interacted with outdoor
city NPCs/signs and landmark guides, and retained Joe graphics. Both also passed
the existing Olivine seven-building/pier/starter trio/met-location/duplicate-guard/
terminal/healing regressions. Ecruteak's nurse healed an acquired partner from
1 HP to full, preserved font/menu stability and registered the correct respawn.
Initial tour/rescue fixtures use debugger-assisted setup with actual controller
movement/events. They are not a normal opening playthrough.

Additional normal UI/SRAM checks: the new ROM loaded a pre-0.6 Route 39 Seedot
save through the title and Continue, preserving position, choice and every one of
its 100 Pokémon bytes. A normal save in Ecruteak Center reloaded through Continue
in a fresh emulator core with position, starter data and respawn intact. A separate
Route 38 save reloaded and returned on foot through Route 39 to Olivine. These are
synthetic development saves, not the owner's private Delta save.

## Delta checklist — manual QA pending

1. Back up your accepted 0.5 save. Load it with this ROM; check title, Joe, party,
   inventory and existing origin metadata.
2. Walk north from Olivine through Route 39; continue onto Route 38 and follow the
   eastbound road into Ecruteak. Speak to route pedestrians and read route signs.
3. Explore Ecruteak, speak to its residents, and enter/leave every building. Tower,
   theater and Gym lobbies are temporary. Routes 37/42 are intentionally closed.
4. Heal an injured partner at the new Center. Open the Mart and buy an item.
5. Save and fully close/reopen Delta in Ecruteak Center, outdoors in Ecruteak, and
   on Route 38. Continue and walk back to Olivine; verify party/items/choice.
6. Recheck Olivine's services, office starter duplication guards, summary and an
   existing battle. Report any collision, wrong destination, repeated event,
   invisible Joe, changed save data or softlock.

## Still unfinished

Original Birch introduction remains. A concrete opening proposal is saved at
crossroads/design/opening/PROPOSAL_01.md and awaits owner creative approval; it is
not implemented. Joe special-state art, Olivine lighthouse progression, finished
Johto art, tower/Gym/theater progression, encounters/trainers and the remaining
region remain unfinished. Actual battle-loss/blackout respawn, new Mart purchase
and outdoor Ecruteak Save/Continue were not newly exercised in emulator; the
registered respawn, nurse, Center/Route 38 saves and existing save compatibility
were checked separately. No full Johto or complete-release claim is made.
