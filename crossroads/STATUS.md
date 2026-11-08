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
