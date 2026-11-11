# QA09 — Ecruteak and Olivine city completion

Both cities' approved map/interior scope is implemented and verified on the
final BUILD11 bytes. Game source `489c404346f572aefb6856b3dd48a9b364a08ceb` is
pushed on `feature/olivine-ecruteak-completion-qa09`, draft PR16. Real Emerald
build, all60 local CI commands and all21 final serial test stages pass. ROM:
`df69e014e706168c56180828487a9ab12709a9bccd3dff063fee5f7af5d4f2f4`.
All51 maps/27,062 map+border cells and51 actual native frames pass independent
ground-layer checks. Scripted mGBA gameplay covers both complete city tours,
all118 door fronts/329 executable approaches, services, landmarks, collisions,
old-save fixtures/normal Continue, starters and Joe actions. No known reproduced
functional defect remains in the exercised scope. **Owner Delta/visual review
is still required.** This is separate from compilation and automated gameplay.

See [scope/references/results](hgss/CITIES_QA09.md), both per-building checklists,
[exact combined evidence](qa/qa09/verification-summary.json) and
[release/Delta procedure](RELEASE_CITIES_QA09.md). Final delivery source and checksum
are in the artifact's build-info.json; source489 is the game-code checkpoint.

Only these two cities are in scope. Existing designs, saves/IDs, Joe, title/music,
starters and approved encounters/practice battles remain. No region expansion,
engine upgrade, story/reward/badge progression or master merge. Older entries
below are historical checkpoints, not instructions to undo QA09.

# QA08 B2 — tested Ecruteak gate checkpoint

See [B2 scope, tests and remaining requirements](hgss/ECRUTEAK_QA08_B2.md).
Full-width green gates now have clear outside arrivals; all161 executable doorway
approaches and the27-map/308-transition tour pass on the B2 bytes. Immutable
route-seam/art/ID checks pass. Owner visual review and full interior raster
comparisons remain open. Olivine is authorized next; no expansion elsewhere.

# QA08 building-by-building review

Latest authority is [Ecruteak QA08](hgss/ECRUTEAK_QA08.md) and
[CITY_BUILDING_INVENTORY_QA08.json](hgss/CITY_BUILDING_INVENTORY_QA08.json).
The earlier all-door claims did not independently test every open segment. QA08
reproduces and repairs ten missing thresholds across Theater, Station and gates.
Separate segment trials, full landmark traversal and service/save regressions run
on the delivery ROM. Closed canonical facades, GBA deviations, missing references
and owner review are explicit. Neither city is declared100%. Olivine is now
authorized after Ecruteak; no other expansion is authorized in this pass.

# Ecruteak QA07 completion review

Use [the27-map checklist](hgss/ECRUTEAK_QA07.md) and its machine-readable
[evidence manifest](hgss/ecruteak-qa07-checklist.json) for current Ecruteak status.
All intended doors/stairs/connections were exercised both ways in mGBA; furnished
rooms/services inspected. Known reproduced ground-arrow/leaf overlap defects are
fixed. Owner Delta visual acceptance and the specific current green-roof report
are still open. Do not call Ecruteak finally complete or move to another region.
Older tables below are historical scope; structural connectivity is not visual QA.

# Current QA06 scope

Eight owner Gym facades; Violet exterior, two houses, school, Center/basement,
Mart, fixed Gym access, Sprout1–3F and west/east gates. Per-area source/deviation/
remaining checklist: [REGION_CHECKLIST.md](hgss/REGION_CHECKLIST.md).
Ecruteak QA05 remains preserved apart from its requested new Gym. Neither a
connected network nor the current increment means all Johto is polished.

# Current Ecruteak QA05 update

See [Ecruteak scope, reference adaptations and actual tests](hgss/ECRUTEAK_QA05.md)
and [Delta QA instructions](RELEASE_HGSS_QA05.md). New work preserves the QA04 city
exterior/IDs/saves and is awaiting owner visual acceptance. Older sections below
are historical milestones; they do not override the current reference-room geometry.

# Visual/collision QA — repair pass0.9.1

Owner reports0.9 network works but has NOT passed visual/collision QA. Expansion
is paused. The first repair pass covers Ecruteak exterior, Mahogany town/workshop,
Routes38/39 and shared ground-layer fixes also affecting Olivine. This is not a
region-wide polish claim. See RELEASE_0_9_1.md and qa/visual-0.9.1/manifest.json.
All other map visual reviews remain open; owner visual acceptance is pending.

---

# Current exploration coverage —0.9

The accepted western 37-map content is preserved. The new 149-map Johto network is implemented for traversal QA; manifest, topology and coverage are in johto/. New services/interiors and landmarks are accessible, but story, badges, new rosters/teams and final art/gameplay polish remain pending. Legacy notes below describe earlier checkpoints.

---

# Current western area — 0.8 QA candidate

Owner requested completion of Olivine, Routes 39/38 and Ecruteak before expansion.
All four remain connected; no new cities/routes were added. Implemented landmarks,
farm, encounters and optional battles are detailed in RELEASE_0_8.md with Delta QA.

Completed for QA: six-floor lighthouse, nine-floor Bell Tower, Burned basement,
theater performance, both Gym arenas, farm/barn/milk shop, approved encounter tables,
optional route trainers and repeatable Jasmine/Morty practice battles. Existing
services, offices, home rest, starter and save contracts are preserved.

Owner approved the exact route rosters/level bands and optional practice battles.
Badges, permanent story gates, legendary events and major narrative decisions stay
deferred. Delta acceptance of 0.8 is pending; do not expand beyond these locations
until the owner has tested this checkpoint and directs the next increment.
