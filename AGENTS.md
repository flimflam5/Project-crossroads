# Project Crossroads development instructions

Owner/creative director: J Fritts. Continue the existing Pokémon Emerald project.
Read docs/PROJECT_CROSSROADS.md and crossroads/STATUS.md, TECHNICAL.md, TESTING.md,
and ROADMAP.md before changing content. Current owner instructions outrank old docs.

- Joe: adult in his thirties, Olivine resident, Silph subsidiary middle manager.
- Starters: exactly one Elgyem (saved value 1), Seedot (2), or Trubbish (3).
  VAR_CROSSROADS_STARTER is 0x40FA; 0 means none. Preserve that save contract.
- Legacy Mara/Meridian/Vale/Mercer text is a proposal, not approved canon.
- Preserve the Alpha bedroom rescue, terminal preview, and Slateport prototype.
  Append new map/layout/heal IDs; do not renumber old ones or alter save structures.
- Work on feature branches. Never merge into master, force-push, delete working
  systems, or upgrade the engine without owner approval.
- Make routine programming decisions autonomously; request major creative choices.
  Do not ask the owner to write code or configure map headers.
- Do not commit ROMs, commercial base ROMs, private saves, or credentials.
- For map/event changes run python3 crossroads/tools/validate_opening.py,
  python3 crossroads/tools/validate_olivine.py and an Emerald build. Also run
  python3 crossroads/tools/build_olivine_layout.py --check for the city blockout.
  Update that generator when editing its authored map.
- Report implemented, compiled, automatically tested, emulator-tested,
  owner-playtested, and accepted separately. Record exact commits/artifacts.
- Update documentation and give an actionable owner playtest checklist.
