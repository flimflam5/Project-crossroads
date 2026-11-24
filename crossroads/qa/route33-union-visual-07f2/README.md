# Route 33 and Union Cave visual repairs: QA checkpoint

Game source: `04f88ee948c26c8da06d239b8203453147c171d1`  
Tested ROM SHA-256: `07f2a10ca19e3eb585c1114ce656caa2475f4de487a4d416dc5bef461a2627a5`  
Matching ELF SHA-256: `ce32b5ba4d016bbb62054c4f97ac40630d461f58a693b4ae96f168eb7c6de92f`  
Before ROM SHA-256: `a320fc5947e7b207e5d496008e3593ef68a403fd5dbba7e73fd2830ccc4539d5`

The Route 33 transition metatiles now render below Joe. At the photographed middle position, scripted normal-controller visibility changed from 0/187 to 187/187 opaque player pixels. Four approaches and the reachable sides of the two Apricorn trees were checked. See `route33/` for native before/after images, clips and scope.

Union Cave's generator now fills enclosed black rock holes and three photographed wall notches with existing blocked rock. Walkable, water, warp and collision data are preserved. Normal-controller runs on both builds captured the three reported views, a ladder round trip, four exit round trips and Survey Surf. The four arrow sprites are intentional cues on directional exit thresholds. See `cave/` for paired images, recordings and scope.

The Olivine terminal photograph matches its established north entrance. Both leaves, arrivals, facing and walking away passed controller checks on the earlier a320 ROM, before these Route 33/Cave-only changes. The perspective remains a visual question for the owner. See `port-a320/`.

On the exact 07f2 ROM, scripted mGBA checks also passed 12 old QA10 saves from one profile through load, save/cold Continue, relevant payload checks and dry escape; 15 reciprocal cave/Ruins warp pairs, 12 collision samples, both puzzle cancels and solves, Survey Surf save/cold Continue, a dry Route 33–Route 32 round trip, title, all three starters and duplicate prevention, Fly, other field actions and a practice battle loss/healing. Wild encounters were disabled in emulator RAM, Survey/temporary QA gear used and the starter test skipped the opening with a RAM fixture. These are sampled checks, not proof of every save or every location. Owner Delta and visual approval remain pending.

The full HGSS Ruins hall, hidden rooms and Route 32 reconstruction remain separate unfinished work. No ROM, private save, emulator snapshot or memory dump is part of this evidence.
