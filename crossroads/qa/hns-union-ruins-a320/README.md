# Union Cave and Ruins of Alph — emulator checkpoint

Game source revision: `00f5742b2cdb48a2256e79e796849dea8f070d1c`  
Tested ROM SHA-256: `a320fc5947e7b207e5d496008e3593ef68a403fd5dbba7e73fd2830ccc4539d5`  
Matching ELF SHA-256: `b5126e02d3f834f7d85e98d2dda4284fbe842c2d1d51eac02e7099922527cea6`

The earlier candidate had green checker borders on all three cave floors. The corrected candidate uses the cave's black-void metatile. The before images come from diagnostic ROM `4f3be1b36cd26a891c73eeba7f214667ad6c2ba1858a0924df4c939a802b8341`; after images come from the tested corrected ROM above. Each is an in-game 240×160 capture at the same position:

| Area | Position (x, y) | Before | After |
| --- | --- | --- | --- |
| Union Cave 1F | (27, 43) | `border/floor1-before.png` | `border/floor1-after.png` |
| Union Cave B1F (existing `UnionCave_2F`) | (2, 60) | `border/floor2-before.png` | `border/floor2-after.png` |
| Union Cave B2F (existing `UnionCave_3F`) | (2, 19) | `border/floor3-before.png` | `border/floor3-after.png` |

Source border bytes, linked ROM and referenced live graphics/palette matched for each corrected floor. This verifies the observed defect at these positions; it does not constitute full visual acceptance.

On the exact corrected ROM, scripted emulator controller tests covered 15 reciprocal cave/Ruins warp pairs, 12 sampled collision bumps, both puzzle cancels and solves, a real Surf Save/cold Continue, and a separate dry Route 33–Union Cave–Route 32 journey in both directions. `tour/coverage.json` gives the scope; the three `*-bump.mp4` files show example movement. Survey access was enabled through the in-game development desk; wild encounters were disabled in the test process.

Twelve old QA10 batteries were created from one profile through controller movement and normal Save. On the corrected ROM, all passed exact recovery or unchanged-position checks, native Save/cold Continue, a walk to a public dry exit, and comparisons of party, boxes, flags, decoded inventory, starter and heal location. Party bytes were exactly equal through migration and re-save. After the longer exit walk, the test counted engine friendship steps and verified both complete decrypted checksums and that no party byte changed except the friendship byte and its checksum within the engine's step-derived bound. These cases do not establish compatibility for every possible save.

Cross-game scripted checks passed for the title and soft reset, all three starter selections and duplicate prevention, ten Fly destinations with cancel and Save/Continue, Surf, bikes, fishing, Joe graphics, and a practice-battle loss and healing. The starter test skipped the opening with a RAM fixture; Fly and field tests used the opt-in QA kit, Survey access and temporary test gear. See `crossgame/summary.json`.

All five private cave/Ruins tilesets passed source-to-linked-ROM metatile, attribute and palette comparisons and source-to-live-VRAM comparisons for graphics and palette banks referenced by the sampled maps. Reports are under `tiles/` and `compiled-assets.json`. These are asset integrity checks, not visual acceptance.

The controller tests are sampled; they do not establish that every boundary, interaction or old save is safe. The four hidden rooms and their conditional gates remain staged and unregistered. Other Johto areas, the full story and eventual transport are not completed by this checkpoint. User Delta and visual review remain outstanding. No ROM, battery save, emulator snapshot or memory dump is included here.

## Attribution and reference

Union Cave adaptation uses material from [Pokémon Heart & Soul](https://github.com/PokemonHnS-Development/pokehns-expansion/tree/167aa6d537b109bb229c231ddce4616974c4da71), donor commit `167aa6d537b109bb229c231ddce4616974c4da71`. The donor requests credit for Pokémon Heart and Soul and its full upstream chain. Its aggregate credits list map work by Crystal Advance/Kertra, Fire Gold/blackfragrant and SkidMarc25, and tileset contributors Crystal Advance/Kertra, Ekat99, TheDeadHeroAlistair, Johto Redrawn Team, zatavares852, lbsbezerra, WesleyFG and Kalarie. Specific authorship of individual files and asset-specific redistribution terms remain unverified. The project records pinned donor input paths and hashes in `crossroads/donor/hns-union-cave/source-sha256.json`.

The connector layout was compared with HGSS event records pinned to [pret/pokeheartgold](https://github.com/pret/pokeheartgold/tree/6bf138d6035aa6b43d6f8f4132a12df70f86dcec) commit `6bf138d6035aa6b43d6f8f4132a12df70f86dcec` and the [HGSS Union Cave reference](https://archives.bulbagarden.net/wiki/File:Union_Cave_1F_HGSS.png). This checkpoint does not claim an exact HGSS visual match.
