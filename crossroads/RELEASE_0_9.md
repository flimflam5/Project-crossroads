# Black Ledger 0.9 — Johto exploration network

Feature branch: `feature/johto-exploration-network-01`. Exact commit and ROM SHA 256
are supplied by the accompanying build-info.json, generated after source commit.
No ROM or private save is committed. Master remains untouched.

## Implemented

149 registered Emerald maps: the preserved 37-map western foundation plus 112 new
maps. All ten towns, Routes 29–48, and connecting land/water/cave geography are
accessible. New Centers/Marts, homes, civic interiors, six new Gym halls and two
community halls provide services and ambient life. Existing eight Gym locations
are respected; only accepted Jasmine/Morty practice systems supply leader battles.

Landmarks include National Park, Ilex Forest, Ruins of Alph, Sprout Tower, Union
Cave, Slowpoke Well, Dark Cave, Mt. Mortar, Lake of Rage, Ice Path, Dragon's Den,
Whirl Islands, cliff approaches and Tohjo Falls boundary. Accepted lighthouse,
Bell Tower and Burned Tower content is preserved. Safari approach/wetlands are
exploration areas, not a completed Safari gameplay system.

A 51-node native field atlas maps all 149 locations. Opt-in RAM-only survey Surf
allows geography testing without granting moves, badges or story progress.

## Verified

- Real Emerald build PASS: ROM used 29,455,512 bytes of 32MiB; EWRAM 226,448 bytes;
  IWRAM 28,392 bytes. Padded ROM is 32MiB. No engine/save-structure upgrade.
- Structural graph PASS:149 maps,69,773 reachable tiles,285 warp entries,
  70 directed border connections,10 Centers. Checks include local exits, reciprocal
  warps, collision/elevation access, valid signed IDs and Emerald build inclusion.
- Final controller-driven mGBA tour PASS:112 new maps,622 transitions,
  141 distinct round-trip door/border pairs,28 survey Surf entries; returned to
  Olivine with starter/party retained. No debugger map/warp writes. Random wild
  encounters were disabled only in the test process to make traversal repeatable.
- Five normal in-game Save/fresh-core Continue checks PASS: Cianwood, Route 41,
  New Bark lab, Blackthorn and Goldenrod Center; exact 100-byte party record,
  starter choice, location and position preserved.
- Existing-area emulator regression PASS, including all three starter rescues,
  duplication guards, old landmarks/interactions and Joe graphics. Some regression
  fixtures use debugger-assisted setup; this is not a claim of owner playtesting.
- Actual Cianwood atlas interaction, cross-group battle-loss respawn and Ice Path
  sliding/recovered walking control PASS. Accepted six optional trainer flows and
  repeat leader battle PASS without badges. Title audio loop/Start/reset PASS;
  perceived static quality still requires owner listening.
- Prior cluster tours and generator checks supplement final coverage. Detailed
  runtime coverage is recorded in crossroads/johto/coverage.json.

Owner Delta QA: PENDING. See johto/DELTA_QA.md. Automated traversal does not verify
all dialogue, purchases, every save location, gameplay balance or visual polish.

## Compatibility and limits

Original 37 map IDs, layouts/heal IDs and critical save constants are retained.
Signed map numbers 0..126 occupy group 75; appended group 76 avoids the reserved
127 dynamic-warp value. Existing met section NONE 213 and special 253..255 remain;
new names 214..252 exhaust remaining byte-sized section names. Future additions
need deliberate metadata planning. Trainer flag capacity remains 864 (only three
unused reserved slots); no new teams/encounters were invented.

Old saves are continued normally, never silently rewritten. Existing party/box
structures and starter variable 0x 40FA are unchanged. NewBarkTown_Gym and
CherrygroveCity_Gym are stable internal authoring names for public community halls,
not extra Gyms. Field atlas is accurate; legacy PokeNav/Fly/habitat maps remain.
Kanto/Routes 26–27, Victory Road and League beyond Tohjo are outside this pass.
Original prologue, badges/story/legendary progression, most special Joe movement
art, final landmark artwork and future gameplay systems remain unfinished.
Boot/title/V 5 music are preserved from 0.8.3; reported audio quality still needs
owner listening QA. This is an exploration release, not a finished Johto game.
