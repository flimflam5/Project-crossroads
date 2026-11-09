# Project Crossroads development instructions

Owner/creative director: J Fritts. Continue the existing Pokémon Emerald project.
Read docs/PROJECT_CROSSROADS.md and crossroads/STATUS.md, TECHNICAL.md, TESTING.md,
and ROADMAP.md before changing content. Current owner instructions outrank old docs.

- Joe: Joseph "Joe" Mercer, 35, Olivine resident, Silph subsidiary logistics manager.
- Starters: exactly one Elgyem (saved value 1), Seedot (2), or Trubbish (3).
  VAR_CROSSROADS_STARTER is 0x40FA; 0 means none. Preserve that save contract.
- Latest owner directive approves Meridian Syndicate, Atlas Drive, Mara Voss and
  Cassian Vale as core premise. Do not assume every legacy preview line, relationship
  or ending is approved. Corporate outfit design is in docs/PROJECT_CROSSROADS.md.
- Preserve the existing Pokémon summary UI; its redesign is out of scope.
- Preserve the accepted Olivine exploration baseline, terminal and Slateport prototype.
  New starter grants now belong to the Olivine Silph office case; the old Alpha
  notebook is a travel bridge. Never silently rewrite old Pokémon met data.
  Append new map/layout/heal IDs; do not renumber old ones or alter save structures.
- Work on feature branches. Never merge into master, force-push, delete working
  systems, or upgrade the engine without owner approval.
- Make routine programming decisions autonomously; request major creative choices.
  Do not ask the owner to write code or configure map headers.
- Do not commit ROMs, commercial base ROMs, private saves, or credentials.
- For map/event changes run python3 crossroads/tools/validate_opening.py,
  python3 crossroads/tools/validate_olivine.py and an Emerald build. Also run
  python3 crossroads/tools/build_olivine_layout.py --check for the city blockout.
  Update that generator when editing its authored map. After building, also use
  validate_olivine.py --built to catch maps omitted by the build-target filter.
  Optional runtime regression: python3 crossroads/tools/emulator_smoke.py (libmgba-dev).
- Report implemented, compiled, automatically tested, emulator-tested,
  owner-playtested, and accepted separately. Record exact commits/artifacts.
- Update documentation and give an actionable owner playtest checklist.

## Current owner priority

Owner accepted 0.6 QA (“Everything works”) and paused expansion beyond the existing
Olivine, Route 39, Route 38 and Ecruteak footprint. Fully flesh out these areas
before adding new cities/routes. Interiors/landmark floors inside these locations
are within scope; major story, curated roster and Gym progression decisions still
require creative review. Preserve accepted saves, title and starter behavior.

Owner approved curated Route 39 Sentret/Hoothoot/Mareep/rare Miltank levels 4–7 and
Route 38 Meowth/Farfetch’d/Magnemite/Hoothoot levels 5–9. Optional trainers and
repeatable Jasmine/Morty practice battles are approved; defer badges/story gates.
Trainer IDs 855–860 use existing reserved space; keep MAX_TRAINERS_COUNT=864 so
system/save flag offsets never shift. Custom NPC IDs 0x3F00–03 must not change
NUM_OBJ_EVENT_GFX or dynamic graphics IDs.


## Latest audio and boot QA

Owner accepted 0.8/0.8.1 tested content/music loop, except title static. 0.8.2
is only partly improved and has reported skips; do not mark audio quality fixed.
Current work explicitly disables inherited reverb for the recorded title track
and restores prior settings on exit. Owner explicitly requested/confirmed a
Black Ledger pre-title boot movie replacing Game Freak/Emerald scenes and asked
for another agent on that track. Keep the New Game prologue separate and preserve
its creative approval boundary. No new region expansion is part of this work.
