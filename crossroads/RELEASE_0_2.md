# Olivine 0.2 — acquisition metadata increment

This is an independently buildable first part of Release 1, **not completed Joe
Mercer integration**, a completed title/intro, or a complete Johto region.
The owner accepted Foundation 0.1 on Delta/iPhone. This increment requires new QA.

## Implemented behavior

The starter rescue now takes place at a visible case in the **Olivine Silph office**.
The old Alpha notebook offers travel to that office before selection; after a
selection, both notebook and case use the same saved duplication guard. The
original level-5 Elgyem/Seedot/Trubbish give/failure/choice logic is retained once,
in crossroads/scripts/starter_rescue.inc. No second grant path is created.

Root cause: CreateBoxMon stores GetCurrentRegionMapSectionId() at acquisition.
Previously that genuinely was Littleroot, because the event was on the old test
bedroom map. It now executes on MAP_OLIVINE_CITY_SILPH_OFFICE, whose map section
is MAPSEC_OLIVINE_CITY. New partners therefore record OLIVINE CITY naturally.
The summary UI is unchanged. No SetMonData met-location override, saved-Pokémon
migration, save-layout change, or existing location-ID renumbering is introduced.
Old partners retain their historical origin, even if it says Littleroot.

The case uses the existing item-ball graphic as temporary case art. The office
interior is still temporary. This is not the final robbery/containment scene.

## Verification

BUILD PASS: Emerald compiled locally with the existing ARM GCC 14.2.1 toolchain.
Linked ROM: 26,762,760 bytes; EWRAM: 226,420 bytes; IWRAM: 28,392 bytes.

AUTOMATED TEST PASS: structural checks; generated Emerald map inclusion; the
mGBA 0.10.5 runtime runner tests all seven entrance/returns, both piers, all three
rescues, stored Olivine met location and met level 5, both duplication guards,
terminal travel, and healing/menu stability. Runtime setup is debugger-assisted,
not a normal opening playthrough. The runner physically uses the new case.

Additional emulator checks: the unchanged summary displayed Trubbish's
"Met at Lv.5, OLIVINE CITY." A pre-fix Seedot save loaded through normal Continue;
a repeat notebook visit preserved all 100 Pokémon bytes and its Littleroot origin.
Those saves are synthetic development fixtures, not the owner's Delta saves.

MANUAL QA PENDING for 0.2. The owner's Foundation 0.1 verdict is preserved separately.
New-game opening, Joe graphics, battles in this increment, and every save/movement
case have not been newly verified. Existing summary screens remain in use.

## Delta checklist

1. Back up your existing save. On an unchosen save, use the Alpha notebook and accept
   travel. Inspect the item-ball case in the middle of the Silph office.
2. On separate saves choose Elgyem, Seedot, and Trubbish. Confirm level 5 and
   OLIVINE CITY in the normal summary. Decline every choice once, then choose.
3. Revisit the case and old notebook. Neither should grant a second starter.
4. Save/reload; check choice, met location, party and inventory. Try an old 0.1
   save too: an existing Littleroot partner must remain unchanged.
5. Recheck the accepted exploration/signs, return travel, Center and Mart.

## Blocked or pending tracks

Joe's approved design and story handoff are recorded in docs/PROJECT_CROSSROADS.md.
The owner is attaching joe_mercer_overworld_draft.zip; it was not present during
this increment. No supplied PNG has been inspected or integrated yet. Player,
trainer back/front and Trainer Card artwork remain original placeholders.

A generated harbor title-screen visual proposal is presented for creative review.
It is not a native 240×160 tile/palette asset and is not in this ROM. Title Start,
Continue and original-intro replacements are separate, forthcoming increments.
Regional expansion remains the approved western-first route network plan.
