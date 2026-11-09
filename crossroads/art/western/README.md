# Western-area art sources

architecture-source.png and leaders-source.png are original AI-generated source
art produced for this project, not extracted commercial map or trainer sheets.
The source compositions are draft inputs, not engine-ready assets.

build_area_art.py crops, thresholds transparency, sizes and quantizes the source
art to 15 colors plus transparent index 0, then assembles isolated WesternCity
metatiles. architecture.json records source SHA, dimensions and allocated tile
slots. preserved-city-metatiles.json freezes previously used map IDs. Never allocate
an old tile merely because the new map no longer references it: old saves matter.
The unchanged original Slateport tileset remains available elsewhere.

Leader front art is 64×64; fixed front-facing overworld art is 16×32. Bell/lantern
props are 16×16 crops of bell.png (16,22,32,38) and lighthouse.png (16,14,32,30),
using palette 08. These fixed props currently have their own committed native PNGs.
All new art remains subject to the owner's in-game visual QA. No outfit system or
legendary story scene is implied by these graphics.
