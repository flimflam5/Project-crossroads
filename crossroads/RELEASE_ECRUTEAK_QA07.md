# Pokémon: Black Ledger — Ecruteak QA07 A1

Ecruteak dependability build for owner Delta review. Regional expansion is paused.
The accepted exterior, custom Ghost Gym, saves, Joe, starters, approved encounters,
title and V5 music are preserved. This is not a claim of final city acceptance.

Download the uniquely named `BlackLedger-Ecruteak-QA07-A1.gba`, or extract it from
the same-name ZIP. `build-info.json` records the exact source and checksum. The
companion Evidence ZIP contains native screenshots, short normal-movement clips,
the city checklist and actual test logs; it contains no saves or ROM.

ROM SHA256:
`1553ad2872e5e0b4a5c5d9fe78d47b73d8f7a541ce294e897db20ded8a6e21c3`

## Changed

- Removed stray walking arrows caused by ordinary paving carrying south-warp
  behavior; restored neutral brick at city seams and their immediate route buffers.
- Leaves now cover Joe naturally; roots still block. Building art and intended
  roof overhangs are preserved. Every current Ecruteak facade was checked.
- Three intentionally closed houses now identify their doors as private/locked.
- Furnished houses, Theater, services, both Gym bridge halves, both gatehouses,
  Station/corridor, Bellchime Trail, Bell1–10F/roof and both Burned floors inspected.

The exact green-roof report is not matched to a current attached screenshot or
confirmed Delta ROM. Keep that issue open. Reference/deviation details and the
city-wide checklist: [hgss/ECRUTEAK_QA07.md](hgss/ECRUTEAK_QA07.md).

## Actual verification

Emerald build PASS;30 static/generator checks PASS. Controller-driven mGBA:27 maps,
288 transitions,500 exterior collision probes,36 specified trunk approaches,
19 recorded examples; all intended warp pairs tested both ways. Actual shop
purchase, PC/healing, performance, falls/whiteout, old-save/cold Continue, Fly/Joe,
all three starters and title/menu checks PASS. These are automated emulator tests
with inspected native images, not owner Delta acceptance or a human full playthrough.

## Delta checklist

1. Export a backup of your existing battery save. Import the new uniquely named
   ROM; if Delta makes a separate game entry, import a **copy** of that battery
   save into it. Start through the title and normal **Continue**. Test emulator
   save states only with their original build; never replace your only save.
2. Confirm Delta is loading **BlackLedger-Ecruteak-QA07-A1.gba**. Report the full
   filename with problems. Reach Ecruteak through Route39→38→west gate, or use the
   already available QA Pidgeot's party-menu Fly. Existing shoes/kit remain.
3. Walk north/south/east/west around the freestanding trees near the houses/Mart.
   Trunks should block; Joe should disappear behind leaves rather than draw on top.
   Walk the south road and both gate approaches: no arrows should follow normal
   walking. Genuine doorway/stair indicators elsewhere are separate behaviors.
4. Circle the Gym, Theater, Center, Mart, houses, Burned Tower and orange Barrier
   Station. Try their front/side walls. Joe may pass behind a projecting roof;
   he must not walk through the building's ground-plane walls. Recheck the reported
   green-roof building and capture its current location if it still behaves badly.
5. Enter/leave every intended door, including both leaves of the Gym/Station.
   The three closed houses respond to A with a private/locked message. West/east
   roads pass through their gate rooms; south connects normally to Route37.
6. Inspect both furnished houses, the Theater's optional show, Mart Buy/Cancel,
   Center healing/PC and basement stairs. Try both Gym bridges, falls/return and
   optional practices. No badges or mandatory story gates should be granted.
7. Walk Station→corridor→Bellchime→Bell Tower, all ten floors/roof and back. Test
   stairs, ledges/pads and Burned Tower's basement both ways. Watch for traps or
   bad stair arrival positions. Pond Surf uses existing temporary survey assistance
   from the Olivine Harbor Office desk; cold Continue clears that RAM-only access.
8. Save normally in a house, outdoors and on a tower floor; close/reopen Delta and
   Continue. Check Joe, exact position, starter, party/boxes and items. Recheck Fly
   and Surf. Keep your original backup until you accept this build.

Report each issue with map/build filename, approach direction, where Joe's feet
were, and whether it followed normal Continue or a save state. Visual acceptance
remains yours. DS online desks are offline; Gym badge/candle story gates and the
main-story prologue remain deliberately outside this map repair.
