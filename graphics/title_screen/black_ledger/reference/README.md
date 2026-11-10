# Harbor title source provenance

harbor-black-ledger.png is an original generated edit of the repository's
crossroads/design/title-screen/harbor-proposal.png, following the owner's explicit
2026-11-08 clarification: preserve that harbor artwork, change the title to
Pokémon: Black Ledger. The later supplied coat/pagoda/book title image is not used.

The source is 1536×1024. ../../../../crossroads/tools/build_black_ledger_title.py
reduces the complete composition to 240×160 and quantizes to a shared 256-entry
RGB555 hardware palette, then writes 600 linear 8bpp tiles and a 32×32 text tilemap.
metadata.json records the source SHA-256. --check verifies exact reproduction.
No independent copyright or licensing claim is inferred from the owner reference.
