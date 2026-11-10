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


## Current Johto exploration authorization

The latest owner directive explicitly supersedes the previous four-area expansion
pause. Preserve the accepted 37-map western foundation and newer 0.8.3 boot/audio
successor. Expand Johto exploration in geographic clusters using the manifest and
topology in crossroads/johto. No new story, regions, encounter/trainer rosters,
badge order, difficulty definitions or permanent progress grants. Current Act I
direction: oblivious corporate supervisor opens at work with deadlines and a
coffee errand; preserve this direction without implementing a full prologue here.
Append IDs only. Existing MAPSEC_NONE stays 213; new section IDs 214..252 use the
remaining safe met-location space and must not collide with 253..255 special IDs.
Survey Surf assistance is opt-in RAM only; reset/Continue must not grant moves or
badges. Native atlas is informational and must not grant travel destinations.

## Current visual/collision repair priority

Owner confirms 0.9 connectivity works but explicitly rejects its visual/collision
QA. Stop geographic expansion. Preserve map/save IDs, connections, old saves,
approved encounters/practice battles, Joe, title/music and accepted functions.
Review representative areas visually before propagation. Record every reviewed
map in crossroads/qa/visual-0.9.1/manifest.json; unreviewed maps stay unreviewed.
Connectivity/build success is not visual acceptance. Keep existing assertions;
run validate_visual_repairs.py in addition to existing map checks.

## Authoritative HGSS reconstruction milestone

Owner now requires faithful HGSS Johto layouts, architecture, terrain and interiors
in GBA style. All map work comes before the next gameplay/story step. Start with
Ecruteak and its relevant landmarks; use actual references and record missing
references. No generic Emerald Gym/house stand-ins described as accurate. Preserve
IDs/saves/network, title/music/Joe/starters/approved content. Record additions,
necessary technical deviations and unfinished areas separately. Reference manifest
in crossroads/hgss. No region-wide accuracy claims based on sample maps.

## Owner-requested QA Fly exception

Owner explicitly requested working Fly before map QA. The optional QA03 kit
marker0x20 permits Fly in Johto without badge grants. A separate party-menu Fly
mode of the atlas uses existing ten city heal arrivals; ordinary atlas remains
informational. All cities are available only as QA assistance, not final story
progression. Preserve native Fly effects, map/layout/heal IDs and saved data.

## Current owner assignment: Ecruteak and Joe field states

Finish Ecruteak interiors/landmark floors, terrain details, entrances/boundaries
and clipping against HGSS without replacing the exterior the owner likes. Audit
all player action states for Joe, preserve saves/unrelated work, build and test
actual emulator traversal/actions/save copies. Show native screenshots/evidence.
No completion claim from compilation or a sample. Active checkpoint and exact
unfinished operations: crossroads/hgss/ACTIVE_COMPLETION.md.

## Ecruteak QA05 generator ownership and continuation

Read crossroads/hgss/ACTIVE_COMPLETION.md and ECRUTEAK_QA05.md before changes.
Native evidence is crossroads/qa/hgss-qa05; source/artifact identity is build-info.
The city exterior is owner-liked; preserve it. Dedicated chain/interior/room/service/
gate generators own Ecruteak. area_layouts skips those rooms. The network generator
uses pinned generic service templates, never clones rebuilt Ecruteak rooms into
other cities. Run build_johto_network.py --through west --check after any change.
Reference extraction-selection and Git blob SHA facts are versioned; no raw NARC,
ROM, private save or commercial asset pack is committed. Re-run exact source/escape
checks, not old rectangular-room assumptions. Native escalators need side landing
space; Center respawn_x/y is8,13. Do not revert to default7,4 or alter heal IDs.
Joe special IDs0x3f04–0x3f0b and NPC0x3f0c/d append without changing the engine enum.
Owner visual acceptance remains required. No master merge is authorized.

## Latest owner direction — remaining Johto and eight custom Gyms

The owner now authorizes continuing the rest of the map and supplied
Black_Ledger_Eight_Gym_Engine_Assets_v1.zip. Its eight original designs supersede
literal HGSS Gym facade art as explicit Black Ledger additions; other geography
still follows HGSS. Read crossroads/hgss/ACTIVE_REGION.md before resuming. Keep
QA05 city/exploration/starter/save/title/Joe functionality. The pack's installer
only registers unused assets; actual integration uses private city resource
packing/overlays with independent pixel/door checks. Never assign a Gym-only
secondary over a populated city or enlarge engine limits to fit it.


## QA06 continuation ownership

The eight owner Gyms and canonical Violet reconstruction now exist; do not
regenerate the old Violet draft. Read hgss/ACTIVE_REGION.md and VIOLET_QA06.md
under crossroads. New assets/generators are independently checked; network
--check must still pass. Source North padding8, explicit Gym alias7/school8/
gates9–12 and append-only CenterB1F/gate IDs are contracted. Route31/36 only have
new gate portals; Route32 only its northern7-row shared-compatible buffer.
Most of Johto remains unreconstructed. Next geographic work is Routes31/32/36
from recovered references, not a generic-town propagation. SaveObjectEvents
byte-swaps graphics IDs; any pre-load migration must mirror LoadObjectEvents.
Survey Surf assistance clears at cold boot; tests must use the actual desk again.
