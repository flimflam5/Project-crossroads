# Johto exploration topology

Existing western maps are retained. Append-only IDs and coverage: [manifest.json](manifest.json).

```mermaid
graph LR
  OlivineCity --- JohtoRoute39
  JohtoRoute39 --- JohtoRoute38
  JohtoRoute38 --- EcruteakCity
  EcruteakCity --- JohtoRoute37
  JohtoRoute37 --- JohtoRoute36
  JohtoRoute36 --- VioletCity_WestGate
  VioletCity_WestGate --- VioletCity
  JohtoRoute36 --- NationalPark
  NationalPark --- JohtoRoute35
  JohtoRoute35 --- GoldenrodCity
  JohtoRoute36 --- RuinsOfAlph
  GoldenrodCity --- JohtoRoute34
  JohtoRoute34 --- IlexForest
  IlexForest --- AzaleaTown
  AzaleaTown --- JohtoRoute33
  JohtoRoute32 --- VioletCity
  JohtoRoute32 --- RuinsOfAlph
  VioletCity --- VioletCity_EastGate
  VioletCity_EastGate --- JohtoRoute31
  JohtoRoute31 --- JohtoRoute30
  JohtoRoute30 --- CherrygroveCity
  CherrygroveCity --- JohtoRoute29
  JohtoRoute29 --- NewBarkTown
  EcruteakCity --- JohtoRoute42
  JohtoRoute42 --- MahoganyTown
  MahoganyTown --- JohtoRoute43
  JohtoRoute43 --- LakeOfRage
  MahoganyTown --- JohtoRoute44
  BlackthornCity --- JohtoRoute45
  JohtoRoute45 --- JohtoRoute46
  JohtoRoute46 --- JohtoRoute29
  OlivineCity --- JohtoRoute40
  JohtoRoute40 --- JohtoRoute41
  JohtoRoute41 --- CianwoodCity
  JohtoRoute47 --- JohtoRoute48
  JohtoRoute48 --- SafariZoneGate
  SafariZoneGate --- SafariWetlands
  VioletCity --- SproutTower
  RuinsOfAlph --- AlphChambers
  RuinsOfAlph --- AlphChambers
  JohtoRoute32 --- UnionCave
  JohtoRoute33 --- UnionCave
  AzaleaTown --- SlowpokeWell
  JohtoRoute31 --- DarkCave
  JohtoRoute46 --- DarkCave
  JohtoRoute45 --- DarkCave
  JohtoRoute42 --- MtMortar
  JohtoRoute42 --- MtMortar
  JohtoRoute42 --- MtMortar
  JohtoRoute44 --- IcePath
  BlackthornCity --- IcePath
  BlackthornCity --- DragonsDen
  JohtoRoute41 --- WhirlIslands
  JohtoRoute41 --- WhirlIslands
  JohtoRoute41 --- WhirlIslands
  JohtoRoute41 --- WhirlIslands
  CianwoodCity --- CliffEdgeGate
  JohtoRoute47 --- CliffEdgeGate
  JohtoRoute47 --- CliffCave
  JohtoRoute47 --- CliffCave
  NewBarkTown --- TohjoFalls
```

League approach terminates at a labeled Kanto boundary beyond Tohjo Falls; no other region or League completion is claimed.

Each cluster must compile and pass topology checks before the next. Services/rooms have reciprocal exits. New rosters and teams remain pending. Test water access will be session-only and explicitly labeled.

## Current validation

149 maps built;112 new maps controller-visited. Final tour checked141 unique
roundtrip door/border pairs and622 transitions. See coverage.json and DELTA_QA.md.
Group75 uses nums0..126; group 76 uses0..21, avoiding reserved dynamic mapNum 127.
Field atlas is informational; routes/caves/water provide actual travel.
Kanto/League beyond Tohjo is a documented safe boundary, not a completed region.

QA06 retains the same city/route traversal through actual Violet gatehouse rooms.
The direct draft west/east border connections are replaced by reciprocal doorway
portals; Route32 remains a normal scrolling connection with offset9/-9. All old
map/layout/heal IDs are retained; Violet basement and two gates append.
