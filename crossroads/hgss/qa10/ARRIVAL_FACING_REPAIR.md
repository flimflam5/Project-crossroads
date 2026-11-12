# QA10 — native gate/trail arrival-facing repair

The independent frozen B4 audit recorded all519 trials:415 correct facings,
37 unavailable lateral approaches,67 incorrect facings. Connectivity and walk-away
passed separately; they did not establish physical facing correctness.

## Actual causes

All four Ecruteak east/west city/route gate links arrived south. Outdoor coordinate
scripts use native `warp`, which resets the initial direction to south; gate-room
ladder thresholds retain that reset direction. In the reverse direction, neutral
outdoor arrival floor defaults south in `GetAdjustedInitialDirection`. Neither
mechanism knows the gate aisle's horizontal orientation.

Bellchime Trail→BarrierCorridor arrives at(6,3) facing north into the blocked
northern wall. That ladder retains the northward departure direction, although
the new room's public landing is south of the threshold.

## Narrow source correction

`build_qa10_arrival_facing.py` uses existing native
`MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE` plus a direct
`MAP_SCRIPT_ON_RETURN_TO_FIELD` hook into the same synchronous
`turnobject LOCALID_PLAYER` body. The native Sidney room establishes the
post-spawn OnWarp player-turn convention. It reads coordinates
into special scratch8004/8005 and turns only at25 exact public portal landings
in six maps. The table compares the existing TEMP0 variable with itself; it
writes no temp or persistent flag. There is no async movement/cutscene, forced
step, tile change, new save structure, engine constant or new geographic link.

| Map | Exact public landing and intended direction |
| --- | --- |
| EcruteakCity | x7,y37–39 east; x59,y46–48 west |
| JohtoRoute38 | x62,y12–14 west |
| JohtoRoute42 | x3,y13–15 east |
| EcruteakCity_WestGate | x1,y6–8 east; x10,y6–8 west |
| EcruteakCity_EastGate | x1,y6–8 east; x10,y6–8 west |
| EcruteakCity_BarrierCorridor |6,3 south |

Arrow metatile behaviors are deliberately avoided: `HideShowWarpArrow` can display
a moving ground arrow whenever the player stands on the relevant behavior and
faces its direction, including return-only anchors. Replacing these floors with
arrows would risk reintroducing the owner's reported artifact.

The two actual call chains differ. Ordinary warps use `InitObjectEventsLocal`,
which spawns Joe then calls `TryRunOnWarpIntoMapScript`. Normal Continue instead
uses `CB2_ContinueSavedGame`→`CB2_ReturnToField`→`ReturnToFieldLocal`→
`InitObjectEventsReturnToField`→`RunOnReturnToFieldMapScript`. Therefore OnWarp
alone does **not** cover Continue. The direct OnReturn hook runs after restored
objects spawn and covers normal Continue and menu/battle field returns. OnResume
is deliberately not used because it can run before player objects are restored.

A save exactly on one of these25 portal anchors is faced into its public landing;
other positions and all persistent party/box/bag/story data are untouched. Menu
or battle return while standing on one of these anchors also normalizes its
facing. Existing callbacks are not replaced: a conflicting authored OnWarp or
OnReturn callback causes generation to stop for explicit composition. This
limited pose normalization is explicit, not a save migration or Pokémon-data
rewrite. The earlier source-only one-hook prototype was corrected before any
claim of built/played repair.

## Generator ownership and checks

The city, chain, gate and regional-network writers call the same idempotent native
script renderer. They therefore generate/check the corrected scripts themselves;
a late postprocessor cannot make their old `--check` expectations stale. The map
JSON format has no separate map-script table field to add: all six existing
`scripts.inc` files are already registered in `data/event_scripts.s`. Other
callbacks and authored script text are preserved.

The aggregate doorway generator projects independent desired directions into
**all45 groups/173 segments**. Final controller runs can use `--require-facing`
for every group, instead of checking only the new maritime links.

`validate_qa10_arrival_facing_source.py` independently interprets the permitted
script instructions across8188 coordinates: exactly the25 expected points turn,
all other points do nothing. It checks scratch-only effects and unchanged B4 map
JSON, blockdata, graphics/attributes, constants, IDs and existing script text
apart from the six named hooks. It imports no generator as expected truth.
The initial source-only prototype passed this control-flow audit. Compilation,
full strict519 controller runs, saved-position/Continue behavior and actual
repair screenshots are still pending the coordinator's repaired build; no
runtime fix is claimed merely because the script source exists.


`--built` additionally resolves the actual ROM group/map headers, reads each
header's script pointer, finds its OnWarp table and direct OnReturn pointer,
checks TEMP0/self→callback and the terminator, and checks the actual
getplayerxy/player-turn/end byte sequences.
All six callback, table, branch and native map symbols must exist in the ELF.
Thus unreferenced source text or a stale ROM cannot pass. Preservation covers
all tracked/untracked game inputs under `data`, `src`, `include`, `graphics`,
`sound` and `Makefile`, allowing only the six scoped native script files.
CI must fetch the immutable full baseline before checking:
`git fetch --no-tags origin df8c4598d88c7770626be4621a5f39cf60dadb95`.
The source-only prototype passes; the unchanged B4 ELF was correctly rejected
because it lacks the new callback symbols. Actual compiled repair checks remain
pending central generation/build.
