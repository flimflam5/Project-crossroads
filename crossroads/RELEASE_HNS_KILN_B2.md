# Black Ledger — Azalea Charcoal Kiln B2

This checkpoint adds one Heart & Soul-adapted Charcoal Kiln east of the existing Azalea Gym. It does not complete Azalea or Johto. The room uses a private converted tileset and original kiln/furnishing adaptations guided by HGSS. The existing Workshop, Gym, IDs, and story remain. Azalea's current blockout differs from the HGSS city, so the entrance placement is an interim adaptation. Credits and file-level source hashes are in `crossroads/donor/`.

Game source: `ae3aee29989e1fb7371c3b31c0aecc965eabfeeb`. Tested ROM SHA256: `6f9d45f8cc4c5b243f4264a129cc3d0695b875d8749518cbeef84727d8062ade`. The 32 MiB padded ROM uses 30,327,768 bytes; EWRAM 226,448 bytes and IWRAM 28,392 bytes. No save-format or starter variable change.

The generators, opening, Olivine, Violet, Ecruteak, Gym and source-specific checks passed; a fresh checkout passed generator checks. Actual scripted mGBA controller tests on this ROM covered kiln entry/exit, 31 accessible solid-cell approaches, worker, Save/cold Continue, two real older QA10 saves, title, all three starter grants, Fly, Surf/field actions and a practice battle. See `crossroads/qa/hns-kiln-b2/verification-summary.json` for fixtures, scope and limitations. They do not replace Delta or owner visual QA. Dive, watering, decoration and VS Seeker were not tested. The introductory Birch scene, full regional reconstruction and ship voyages remain unfinished.

Old saves under the new 4×4 building footprint use existing Continue recovery to move Joe to nearby open ground; future saves under that footprint also relocate. A tested outside-footprint save remained in position. Compatibility is not proven for every historical save.

For Delta: back up your save, import this ROM and use normal Continue rather than an older save state. Visit Azalea, find the kiln east of the Gym, enter and exit, speak to the worker, walk around its walls and furniture, and save/reload. Check the roof, door animation and interior against your expectations. Please report any visual, collision or save issues; your visual acceptance remains pending.
