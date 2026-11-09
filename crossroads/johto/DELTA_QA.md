# Black Ledger 0.9 — Delta exploration QA

Back up/export your existing battery save before importing this ROM. Keep the old ROM.
Extract the ZIP in iPhone Files, import **Black Ledger 0.9.gba** into Delta, and
import a COPY of the old game's battery save if Delta treats the new filename as a
separate game. Use normal Continue, not an older-version emulator save state.

1. Cold boot: inspect the existing branded boot/title, listen through the V5 music
   loop, press Start and Continue. Audio quality remains an open listening check.
2. With your old save, confirm Joe, starter species/level, party, inventory and money.
   Try the Silph rescue case again: it must not grant a second starter.
3. Olivine → Route39 → Route38 → Ecruteak. Check the accepted buildings, lighthouse,
   Bell/Burned towers, theater, farm and optional practice battles remain functional.
4. Ecruteak south →37→36→Violet; branch through National Park→35→Goldenrod.
   Visit Centers, Marts, public buildings, Underground and both Underground doors.
5. Goldenrod→34→Ilex→Azalea→33→Union Cave→32→Violet. Explore Sprout Tower,
   Ruins of Alph chambers and Slowpoke Well. Return through the same entrances.
6. Violet→31→30→Cherrygrove→29→New Bark. Check the lab and public halls.
   Route29 north→46→45→Blackthorn is another land connection.
7. Ecruteak east→42→Mahogany; check all Mt. Mortar entrances and floors.
   Route43→Lake of Rage; Route44→Ice Path→Blackthorn→Dragon's Den.
   Test ice sliding as well as the safe walking ledges. Explore Dark Cave mouths
   on31/45/46 and check you can return to each road.
8. For sea exploration, explicitly enable the survey desk in Olivine Harbor Office
   or any NEW Center. With a real starter in your party, face water and press A.
   This session-only helper grants no badge, move or permanent progress. Save/reset
   turns the desk mode off; small-island caretakers can re-enable it. Emergency
   fallback: hold L+R+Select while pressing A facing water in Johto.
9. Olivine west→40→41→Cianwood. Explore four Whirl Island mouths and floors.
   Cianwood→Cliff Edge Gate→47→48→Safari approach/wetlands; check Cliff Cave.
   New Bark's offshore Tohjo Falls approach is a safe exploration boundary;
   Kanto/League access beyond it is not implemented in this pass.
10. Open a field/wall atlas in both an old town and Cianwood. Check the current
    location marker and labels; D-pad selects labels, A/B closes. It grants no travel.
11. In each cluster: heal, buy an item, enter/leave each building, save normally,
    reset and Continue. On a COPY of a save, lose a battle after healing at a new
    Center; confirm safe local recovery, intact starter and no unwanted badges.
12. On separate new games, test Elgyem, Seedot and Trubbish rescues, met location,
    duplication prevention, save/reload and return travel. Do not overwrite your
    main save to do this.

Report the location, last entrance used, save/new-game status and a screenshot for
any obstruction, incorrect collision, warp, camera or dialogue issue.

## What this build is and is not

All ten towns and Routes29–48 are connected for exploration, with 149 maps total.
Existing 37 maps and accepted encounters/battles are retained. New population,
services, signs, caves and public interiors are implemented using compatible
project tiles. New Gyms are explorable halls; badges, leader teams and story roles
remain undecided. New routes have no unapproved encounter/trainer tables.

Department store/radio/pharmacy/lab/academy are public exploration interiors,
not complete future gameplay systems; Safari has no capture minigame or new roster.
No new legendary events, major story scenes, additional regions or full-game ending.
The original New Game prologue remains; Joe's special movement artwork is still
inherited in some states. Field atlas/popups are Johto-aware, but legacy PokeNav,
Fly and Pokédex habitat interfaces are not converted to a Johto world map.

Compilation and controller automation are separate from owner Delta acceptance.
