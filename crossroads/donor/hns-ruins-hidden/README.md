# Ruins second and hidden-room source

This reference package pins Pokémon Heart & Soul donor revision
`167aa6d537b109bb229c231ddce4616974c4da71`. `source-sha256.json` records
all input bytes. The donor's combined chamber map includes two second-room
crops; WordsRoom1 and WordsRoom3 supply northwest and southwest hidden-room
visual references respectively. Donor exits are **not** authoritative: it
uses directly walkable north doors where HGSS uses scripted falls.

HGSS reference geometry was independently extracted from public pret
`pokeheartgold` commit `6bf138d6035aa6b43d6f8f4132a12df70f86dcec` using
`crossroads/tools/extract_hgss_ruins_hidden_reference.py`. The public terrain
archive's Git blob is `33105ab54c804a33503fb52db0ffa93a4d38191a`; only numeric
permissions and event anchors are stored in the project, not DS graphics.
Both second rooms return to their own first chamber at (6,17) and trigger a
fall at (6,3). Northwest and southwest hidden rooms are separate maps: their
respective arrival/exit coordinates are (11,14)/(20,21) and (11,7)/(20,13).
Those exits fall to the Underground Hall at (5,24) and (5,42), respectively.
Story/Unown flags and the four items in each HGSS second room are not ported.

HNS requests full credits. Its aggregate list attributes map work to Crystal
Advance / Kertra, Fire Gold / blackfragrant and SkidMarc25; tileset contributors
include Crystal Advance / Kertra, Ekat99, TheDeadHeroAlistair, Johto Redrawn
Team, zatavares852, lbsbezerra, WesleyFG and Kalarie. These are aggregate
acknowledgements, not attribution of particular files; file-specific terms
remain unverified.

This source and geometry checkpoint does not register playable maps, add item
rewards, change saves or implement the fall scripts. All GBA adaptation and
runtime/visual validation remains pending.

## Staged geometry candidate

`crossroads/tools/stage_hgss_ruins_hidden.py` returns four separate room planes,
layout dimensions, blocked borders and transition facts through a caller-owned
writer. It does not register maps, install the proposed tilesets, add flags,
place items, or write room scripts. `test_hgss_ruins_hidden_stage.py` checks each
walkable cell against its pinned HGSS permission component, field elevation,
metatile behavior, exact anchors and deterministic output. It also checks that
only the south-facing room exit uses a warp behavior; future hidden-room falls
need explicit script events.

The two second-room layouts share HGSS's 115-cell footprint, each with its own
map name. The four stone plinths mark reference item positions but grant no
items. Separate donor-inscription visual adaptations use HGSS's 260-cell SW
and 420-cell NW footprints. Donor letters are spaced onto the GBA footprints;
no claim is made that their visual layout is identical to the 3D original.
The donor north-door shortcuts are removed. These are offline candidate planes,
not in-game screenshots or proof of collision, transitions, saves or visual
quality. The predecessor 29×32 GBA Underground Hall cannot represent HGSS's
southwest fall landing at (5,42). This development branch appends a separate
32×64 HGSS-shaped hall layout, retaining the same map ID and old layout files.
Both verified fall landings exist there; old-layout Continue uses a generated
safe-floor mask. Build, old-save and full movement tests remain required.

The larger Underground Hall candidate follows the HGSS 816-cell dry component
and uses the source (5,42)/(5,24) puzzle-fall destinations and two separately
reciprocal exits. Its 30 donor-styled markers are visual-only; the original
HGSS marker dialogue and conditional NPCs remain unimplemented. An old-save
Continue mask and host fixture are present, but normal hardware/emulator save
loading, both thresholds, puzzle returns and foreground layers need playtesting.
