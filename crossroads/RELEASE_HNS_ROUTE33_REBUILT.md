# Black Ledger — Route 33 prototype, rebuilt QA checkpoint

This is an interim Route 33 donor adaptation, not a finished Johto or a complete HGSS reconstruction. It preserves the existing map ID, cave warp, Azalea connection and original events while importing privately packed Heart & Soul terrain. The 32×24 route is shorter than HGSS; the town seam, cave placement, Apricorn trees and NPC locations need further work. Union Cave is still the older exploration foundation. The subsequent 32×32 refinement branch is not included in this ROM.

Source: `5c308d1fbc66e202ee6da0c4de712079955851b0`. ROM SHA-256: `d78f533b7cbc67d69a7eba333bc95595ba14747e1669ee3516b5e0fc070f0faf`. A fresh rebuild reproduced the previously tested bytes. Credit and source details are in `crossroads/donor/hns-route33/README.md` and `crossroads/donor/hns_azalea_exterior/provenance.json`.

Fresh scripted mGBA controller checks on these exact bytes covered a genuine copied QA10 save, Azalea border and Union Cave both ways, 39 sampled blocked approaches and four directional ledge jumps, existing interactions and normal Save/cold Continue. Compiled metatiles, runtime VRAM and palettes, title, all three starters/duplicate guards, Fly, Surf and one optional battle also passed. Tests use disclosed Survey/encounter-suppression, temporary gear and fresh-game/1HP fixtures where needed. The starter suite skips the opening; Dive, watering, decoration and VS Seeker were not activated. The evidence is in `crossroads/qa/hns-route33-rebuilt-20261118/`.

Owner Delta and visual acceptance remain pending; collision and old-save cases are sampled, not exhaustive. The normal Continue recovery can relocate old positions that became blocked. The older Birch introduction, Union Cave/Ruins reconstruction, ship voyages and much of Johto remain unfinished.

For Delta: back up the save, import the ZIP's `.gba`, and use normal Continue rather than an older save state. Walk from Azalea through Route 33 to Union Cave and back; inspect the border, trees, cliff and cave entrance, talk to the resident, read the signs, and save/reload. Please report visual or collision problems and any old-save changes.
