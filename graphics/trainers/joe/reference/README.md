# Joe Mercer trainer artwork provenance

Draft artwork generated on 2026-11-08 with the OpenAI image-generation tool,
using the owner's supplied `joe_mercer_overworld_draft.zip` directional sprites
(`joe_down_0.png`, `joe_up_0.png`, `joe_right_0.png`) as visual references.
The prompt requested the approved adult corporate outfit: messy brown hair,
tired expression/stubble, white shirt, maroon tie, dark slacks and brown satchel.
No external trainer sprite or commercial music/recording was imported into this
artwork. This record identifies its origin; it does not assert rights to Pokémon
branding or ownership/licensing of the supplied reference artwork.

- Preserved unmodified output: `generated-trainer-sheet.png`, RGBA 1536×1024.
- Source-sheet SHA-256: `c867e0d059451eb26165a024dde87e6da7df17125eec2ac28a1ae6c2e5dec606`.
- Supplied archive SHA-256: `66c0dcf8e63e7f6b60cf4586f47c029f1115b1c38fb3c7d92aa6cdca16eb63ea`.

`convert.py` crops the fixed 3×2 grid of 512×512 cells. The top-left cell is
the front view; top-middle, top-right, bottom-left and bottom-middle are the
four rear throw poses. Bottom-right is unused. Alpha below 128 is discarded
to remove the generated diffuse fringe/background; remaining alpha becomes
fully opaque. Each cell is reduced to 64×64 with nearest-neighbor sampling,
without redrawing or rescaling individual body parts. Rear frames retain their
cell alignment and are stacked vertically into a 64×256 sheet.

All frames use one fixed 16-entry indexed palette: transparent index 0 and
15 opaque colors, including reserved burgundy/red for the tie and capture ball.
Opaque colors are rounded to RGB555 precision, then source pixels map to the
nearest palette color by RGB distance. Outputs are `../front.png`, `../back.png`
and `../joe.pal`; no partial transparency remains.

Reproduce or verify from any working directory (Python 3 and Pillow 9.1+):

```sh
python3 graphics/trainers/joe/reference/convert.py
python3 graphics/trainers/joe/reference/convert.py --check
```

Optional `--source`, `--output-dir` and `--preview` paths support alternate
conversion destinations and an enlarged diagnostic preview. `--check` compares
the indexed pixels, palettes and transparency without modifying the outputs.
These are draft graphics awaiting in-game appearance and animation QA; asset
conversion success does not establish gameplay verification or owner acceptance.
