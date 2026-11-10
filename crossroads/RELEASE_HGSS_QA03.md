# Black Ledger QA03 — owner-requested exploration kit

All QA02 map fixes are retained. Hold R while pressing A to talk to the
exploration-desk sailor on the left in Olivine Harbor Office, then accept the
QA kit. New Center survey-desk sailors also support this gesture. Normal desk
interaction remains RAM-only water access, with no saved progress grants.

The kit enables Running Shoes (hold B) and adds level100 Pidgeot with Fly,
Aerial Ace, Roost and Quick Attack. Leave one free party slot. No existing party
member, boxed Pokemon or starter variable is replaced. A previously unused
flag0x20 records the one-time gift only after a successful grant. This does not
shift flags, IDs or save structures. Accepting this kit intentionally persists
in this test save; use a backup. Declining changes nothing. A full party still
receives Running Shoes and may return for the Pidgeot after making room.

Fly is a known move for battle; the Johto field Fly destination interface remains
unfinished. No badge flags or city-unlock flags are granted. No new permanent
encounter roster, story event or difficulty rule is established by this QA helper.

Delta: back up your battery save, import the new ROM and normal Continue; claim
kit, inspect Pidgeot level/moves, hold B outdoors, try the desk again (no second
Pidgeot), then save/reset/Continue to check persistence. Do not load an older
emulator save state. The HGSS city/region reconstruction remains unfinished.

The original validator still forbids saved grants inside the survey-water script.
The requested persistent kit lives in its own linked script, entered only through
R+talk and explicit confirmation. Additional assertions restrict its grants to
Pidgeot, Running Shoes and the one-time marker, with no badges or starter writes.

Verification: final Emerald build PASS; opening, Olivine, western Johto, area,
HGSS save-contract, network, kit restrictions and build-inclusion checks PASS.
Actual copied-old-save Continue and normal desk no-save-flag-change check PASS.
Controller R+talk/accept granted species18(Pidgeot), level100, move19(Fly),
Running Shoes and the one-time marker. Original party bytes and starter variable
unchanged; only the two authorized flags changed; repeat grant prevented PASS.
The test decodes species/moves with the engine's actual11-bit packed fields.
Normal post-grant save/reload and Delta running/visual QA remain pending.
