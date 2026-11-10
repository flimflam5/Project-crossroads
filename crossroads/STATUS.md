# QA04 Johto Fly integration

Owner requested functioning Fly before Delta QA. Party-menu QA Fly connects ten
existing town/city heal arrivals with native animation; no badges/story flags.
See RELEASE_HGSS_QA04.md. Full map reconstruction and owner visual QA stay open.

# QA03 owner-requested testing kit

Optional level100 Pidgeot with Fly and Running Shoes via R+talk at the survey
desk. See RELEASE_HGSS_QA03.md. Build/controller grant checks pass; owner Delta
QA and post-grant save/reload pending. Johto field Fly destination UI unfinished.

# Ecruteak preliminary QA 02 repair

Owner likes the city exterior but reports boundary and entrance issues.
See RELEASE_HGSS_PRELIM_02.md for the focused fixes and remaining work.
This is not full city/region acceptance.

# Preliminary HGSS QA checkpoint 01

Owner requested a preliminary test build before reconstruction is complete.
See RELEASE_HGSS_PRELIM_01.md for scope, limitations and Delta checklist.
The reconstruction remains unfinished and owner visual acceptance is pending.

# Active HGSS reconstruction — not a release

Branch: feature/hgss-ecruteak-reconstruction-01. Asset/reference checkpoint93d8e8b02c
is committed; city/transition/validator integration is in progress. The existing
0.9.1 download remains the last delivered repair build, not an accepted visual map.
Actual HGSS references cover all ten towns/cities and Routes29–48; most are not
yet visually inspected/reconstructed. Ecruteak's logical64x64 area and entrance
positions are verified against canonical event/world-matrix facts. Dedicated
facades replace the warehouse stand-in in the draft. No full-region completion
claim. Do not advance story/gameplay while the map milestone remains unfinished.

---

# Visual/collision QA — repair pass0.9.1

Owner reports0.9 network works but has NOT passed visual/collision QA. Expansion
is paused. The first repair pass covers Ecruteak exterior, Mahogany town/workshop,
Routes38/39 and shared ground-layer fixes also affecting Olivine. This is not a
region-wide polish claim. See RELEASE_0_9_1.md and qa/visual-0.9.1/manifest.json.
All other map visual reviews remain open; owner visual acceptance is pending.

---

# Current QA candidate — Johto exploration0.9

149 maps registered/built (37 preserved +112 new); all ten towns and Routes29–48 connected. Final emulator tour:112 new maps,622 transitions,141 roundtrip pairs PASS. Five normal Save/Continue checks PASS. Owner Delta acceptance pending. See RELEASE_0_9.md and johto/DELTA_QA.md. The newer owner directive supersedes historical expansion pauses below.

---

# Current QA candidate — 0.8.3 boot/audio

Inherited title reverb explicitly disabled/restored; custom Black Ledger pre-title
prototype implemented independently. Combined Emerald build, native boot/skip/
reset, title audio per-frame continuity, title UI and real old-save Continue pass.
Delta static/skip comparison and pre-title appearance/pacing QA remain pending.
See RELEASE_0_8_3.md for exact coverage and limitations. Original New Game prologue
remains unchanged. No map or story expansion in this increment.

# Active audio/boot refinement after 0.8.2

Owner says 0.8.2 is a bit better, but reports remaining static and track skips.
Audio listening QA remains open. An inherited reverb=50 effect was verified and
is now explicitly disabled for the title and restored on exit. See
AUDIO_REFINEMENT.md for actual checks and limits. Owner also confirmed replacing
the Emerald/Game Freak pre-title boot movie with a Black Ledger sequence. A
second agent is implementing that independent branded harbor prototype. This
is separate from the unapproved New Game prologue and adds no story canon.

# Owner QA accepted — 0.8 and 0.8.1; title audio refinement

Owner: “the music is there it loops and everything is good in 8 and 8.1,” with
“the new music is kinda static-y” as the reported issue. Record manual QA PASS
for the tested 0.8 area and 0.8.1 music/loop functionality; do not infer any extra
individual test beyond this blanket verdict. Audio quality remains a known issue.

feature/title-audio-cleanup-01 prepares 0.8.2 for listening QA: native 31.5 kHz
title playback and 9-bit DAC, restoring normal audio before gameplay. Build and
emulator checks pass; whether the static is sufficiently improved needs owner
Delta comparison. Source MP3, accepted loop, art, maps, starter and saves retained.
See RELEASE_0_8_2.md. No additional cities/routes or story content in this fix.

Historical checkpoint notes follow.

---

# Latest audio increment — 0.8.1

feature/title-music-01 integrates the owner-supplied 80-second title recording
using the existing sound engine. Emerald build, actual emulator audio/progression/
loop/Start/reset checks and normal Continue from a 0.8 battery save passed.
Owner listening QA and final loop selection pending. See RELEASE_0_8_1.md.
The 0.8 current-area completion candidate remains awaiting owner Delta QA.

# Current checkpoint — western area 0.8

Current branch: feature/western-area-completion-01. Current-area exploration content
is implemented and compiled for QA; see RELEASE_0_8.md and AREA_COMPLETION.md.
Owner Delta QA is pending. Earlier accepted 0.6 behavior is the regression baseline.
No additional cities/routes, badges, story gates or unapproved prologue scenes.

Historical development record follows; older unfinished-content statements refer
to their respective checkpoints, not the current candidate.

---

# Development status

## Audit baseline — 2026-11-07

- Branch inspected: master at d3ac7cf7884d5e645c4b8179d5d94af7bbd2306e.
- Engine: expansion/1.17.2-35-gd3ac7cf788; pre-Crossroads ancestor c460a8661d.
  No engine upgrade is part of this milestone.
- No existing AGENTS.md was found. The old bible's Saffron opening, old starters,
  fixed difficulty labels and criminal factions are superseded by the directive.
- Live Alpha rescue is linked to the notebook in Brendan's bedroom. It grants
  one level-5 Elgyem/Seedot/Trubbish, checks MON_CANT_GIVE before saving the choice,
  and guards repeat interactions with persistent var 0x40FA.
- The GameCube runs a dialogue-only Silph preview that changes after rescue.
  crossroads/scripts/prologue.inc is a staged duplicate, not the linked event.
- Existing Olivine consists of three relabeled Slateport signs. No dedicated
  Olivine map, Johto city geometry, or playable robbery chain existed on master.
- The seven Alpha v2 PASS results are historical owner reports. No Alpha-v2 tag
  was found and no emulator/save evidence was supplied. Source inspection does
  not reproduce those gameplay results.
- Baseline GitHub CI succeeded:
  https://github.com/flimflam5/Project-crossroads/actions/runs/41859106151
  The preceding prototype-wiring commit failed CI; latest master adds the missing
  script labels. A separate local master worktree is used for the baseline build.

## Olivine foundation 0.1

Branch: feature/olivine-city-foundation.

Scope: standalone 48×48 city blockout, western sea, southern harbor, two piers,
residential streets, seven linked interiors, NPCs, functional Center/Mart,
starter-dependent pedestrian dialogue, and return access to the Alpha test room.
The Silph terminal offers optional exploration after its original preview.

This is a temporary blockout, **not final Olivine geography**. House, office, Gym
and beacon graphics reuse existing Emerald assets. The Gym is a temporary lobby
without battles; the lighthouse tower is not built. No new story canon, crime
system, starter grant, difficulty rules, or regional travel is introduced.
Original new-game introduction and player graphics remain.

Verification results: TESTING.md. This is an incremental city foundation, not a
claim that the entire city or game is complete. The owner has since accepted manual QA for the tested exploration alpha; see the handoff below.


## Verification update

Both baseline and city compiled locally. Debugger-assisted mGBA tests passed for
city traversal/returns, all three live starter branches and duplication guards,
terminal travel, and healing/menu stability. Normal UI purchase and real SRAM
Save/Continue were also checked; detailed coverage and gaps are in TESTING.md.
The complete opening and finished Olivine are not claimed. No merge into master
has been performed. Draft review: https://github.com/flimflam5/Project-crossroads/pull/1


## Accepted owner QA and next increment

Tester: Dr. QA Daddy (project owner), Delta on iPhone. Tested build: Olivine City
Exploration Alpha / Foundation 0.1. Verdict: PASS — "Yes everything is a pass."
Accepted coverage: exploration, listed signs, lighthouse placeholder dialogue,
Center/Mart access, Elgyem waterfront dialogue, harbor restriction, residence return,
Gym lobby, save prompt, Elgyem summary, save/reload, return with starter, stability.
Earlier starter trio, duplication and battle checks remain reported as passing.
This accepts the tested foundation, not untested future character/title/region work.
Placeholders are unfinished development work, not regressions in that QA verdict.

Current branch: feature/joe-integration-01, based on accepted c66b089815 rather than
master (PR #1 remains unmerged). Release 1 starts with actual acquisition metadata:
move the existing rescue case to the Olivine Silph office, keep the old notebook
as a travel bridge, preserve saved choice 0x40FA and all previous Pokémon data.
Joe graphics await joe_mercer_overworld_draft.zip; the owner is attaching it.
Do not fabricate inspection, replacement artwork, or completed Joe integration.

## Joe corporate 0.3 — owner QA accepted

Source f40e5028c31d3470f4795fdcc869c356898a784a; owner tested the delivered
Joe 0.3 ROM in Delta and confirmed everything tested works as intended.
Record this as manual QA PASS for that checkpoint, not completion of all character
states or future region/title content. Joe walking, draft trainer artwork and the
Silph rescue/met-location fixes are the preserved baseline. Special movement art
and the original introduction remain unfinished. PR #2 remains draft/unmerged.
The earlier “awaiting archive” paragraph describes the historical 0.2 state only.

## Western Johto 0.4

Route 39 is appended as map 75.8, with a reciprocal normal border connection to
Olivine's north road. The city/interior IDs 75.0 through 75.7 remain unchanged.
The reproducible exploration blockout has countryside scenery, a pedestrian,
signs and an explicit closed northern boundary. Route 38/Ecruteak, encounters,
trainers and farm interiors remain unfinished. See RELEASE_0_4.md for verification
and Delta checks. The owner has supplied Pokémon: Black Ledger / Voidstar
Interactive title artwork, superseding the former harbor proposal; implementation
is a separate forthcoming increment. No title replacement is included in 0.4.

## Black Ledger title 0.5

Owner clarification supersedes the intermediate 0.4 title note: retain the old
harbor scene with the new Pokémon: Black Ledger title. The coat/pagoda/book image
is not used. A native GBA title implementation now uses the revised harbor art.
Local build, cold boot/rendering/lighting, Start, New Game handoff, soft reset and
normal Continue checks passed. A Route 39 save reloaded through the title with
position, saved starter choice and all 100 Pokémon bytes preserved, then returned
to Olivine on foot. The Joe/city/starter/healing regression runner also passed.
See RELEASE_0_5.md for exact coverage and the accepted owner QA update. The original
Birch introduction remains; it has not been replaced by the new prologue.

## Accepted owner QA — Black Ledger 0.5

Owner verdict: “Everything works as expected.” Recorded for the delivered Delta
build from source 01b0ef25c8482e1c50a5a97244f119ae818931d6, artifact
black-ledger-harbor-0.5-01b0ef25c8.zip. Manual QA PASS for the tested 0.5
checkpoint, including its title and Route 39 exploration increment. This is the
new working baseline. No additional per-test results beyond the owner's blanket
verdict are inferred. Unfinished intro, special-state art and regional content
remain unfinished. This verdict does not authorize merging into master.

## Ecruteak connection 0.6

Connects Olivine/39/38/Ecruteak without teleport shortcuts. New map IDs append:
75.9 Route 38, 75.10 Ecruteak, 75.11–17 interiors. Seven doors have reciprocal
returns; Center healing/respawn and basic Mart services are wired. Landmark/Gym/
theater rooms and exterior art remain explicitly temporary. Routes 37/42 are
closed. Local Emerald build and both-gender emulator tours/regressions passed.
Normal old-save Continue plus new Center/Route 38 SRAM checks are documented in
RELEASE_0_6.md. Owner Delta QA pending. Full Johto is not complete.

Opening proposal 1 is pending owner review at design/opening/PROPOSAL_01.md; no
new intro dialogue has been made permanent or enabled. Accepted 0.5 remains the
owner-tested baseline until this next checkpoint is accepted.

## Accepted owner QA and content freeze — 0.6

Owner reported “Everything works” for the delivered 0.6 checkpoint from source
68bce285d2537c8e3960640234fd083f0a3886e0. Record owner Delta QA PASS for the
tested build; do not infer separate results for unreported tests. The owner now
requires completing existing Olivine/39/38/Ecruteak before new cities or routes.
The immediate detail pass targets distinct Olivine office interiors and useful
interactions while preserving existing rescues, doors, saved variables and returns.

## Olivine detail 0.7 — implementation checkpoint

Dedicated corporate and harbor office layouts replace their shared bedroom art.
Home rest supports decline/accept, empty party and party recovery without story,
starter or respawn changes. Staff/freight/dispatch/home records are interactable.
Map IDs, dimensions and accepted warps remain stable; layout IDs append. Final
Emerald build, structural checks and both-gender full emulator regressions passed.
Normal 0.6 save compatibility and new office Save/Continue/exit checks passed.
See RELEASE_0_7.md. Owner Delta QA pending for this increment. Existing-area
completion continues under AREA_COMPLETION.md; no new cities/routes were added.

## Current area completion approvals

Owner approved Route 39 Sentret/Hoothoot/Mareep/rare Miltank levels 4–7 and Route 38
Meowth/Farfetch’d/Magnemite/Hoothoot levels 5–9, optional grass/trainer battles and
safe roads. Owner also approved optional trainers plus repeatable Jasmine/Morty
practice battles, deferring badges and permanent story gates. No new cities/routes
are authorized in this completion pass. Current work adds actual lighthouse/tower
floors, farm, theater and arenas inside the existing footprint.
