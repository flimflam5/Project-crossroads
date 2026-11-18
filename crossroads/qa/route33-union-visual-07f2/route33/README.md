# Route 33: pavement layer correction

Native 240×160 screenshots and normal-controller recordings from a copied QA10 test battery. Before is the delivered ROM SHA-256 `a320fc5947e7b207e5d496008e3593ef68a403fd5dbba7e73fd2830ccc4539d5`; after is candidate `07f2a10ca19e3eb585c1114ce656caa2475f4de487a4d416dc5bef461a2627a5`. Before/after PNG names indicate identical map coordinates (7,15), (7,16) and (7,17). Best frames were selected from up to 30 samples to avoid incidental rain overlap.

For the three cells, player visibility changed from 66/186, 0/187 and 32/192 opaque sprite pixels to 186/186, 187/187 and 192/192 respectively. Four approaches to the center cell worked on both ROMs. Each of the two Apricorn objects blocked its single accessible north side; remaining sides are blocked by other objects or terrain. These checks are sampled, not owner visual acceptance. Wild encounters were suppressed only in the emulator process. No saves, emulator states or ROMs are included.
