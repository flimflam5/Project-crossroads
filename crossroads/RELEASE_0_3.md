# Joe corporate 0.3 — Delta QA checkpoint

Joe's supplied 16 directional frames now drive the playable walking character for
both saved genders. East uses its own artwork rather than mirroring the satchel.
Running uses the walking poses at faster timing. Dedicated draft trainer front,
battle back and local Trainer Card artwork represent the same corporate outfit.
Silph office rescue, saved starter IDs and Olivine acquisition metadata are preserved.
No existing Pokémon origin data is rewritten. The summary UI is unchanged.

## Verification

The recovered Emerald build passed. Both gender fixtures passed debugger-assisted
mGBA checks for four directional graphics, building returns, piers, all three
starters, metadata, duplicate guards, terminal travel and healing/menu stability.
Asset, script, map inclusion and reproducible layout validators passed again during
recovery. Additional emulator screenshots verify Joe's Trainer Card and battle back
artwork; a wild battle returned to the field with Joe visible. These are development
fixtures, not the owner's Delta save or a complete normal opening playthrough.

## Delta checklist

1. Back up your save, then load this ROM with a copy of your existing save.
2. Walk and run in all four directions; inspect the tie, hair and satchel. Enter
   and leave every Olivine building and save/reload indoors and outdoors.
3. Open Joe's Trainer Card. Start a battle, inspect Joe's throwing animation, and
   return to the field. Check the existing Pokémon summary still works.
4. On separate unchosen saves obtain Elgyem, Seedot and Trubbish from the Silph
   office case. Confirm level 5, OLIVINE CITY, and no duplicate from either case
   or old notebook. Existing partners must retain their previous origin.
5. Recheck signs, terminal, harbor return, Center healing and Mart interactions.
6. Report any wrong facing, flicker, invisible frames, save changes or softlocks.

## Remaining work

Release 1 is not complete or accepted. Bike, surf, underwater, fishing and other
special movement states still use stock artwork. Dedicated running poses are absent.
Original intro character presentation remains. Trainer artwork is a visual draft
requiring owner review. Lighthouse/Gym and city interiors retain documented temporary
content. Full Johto expansion is unfinished. The custom title concept is unapproved
and unimplemented. No summary-screen redesign is included.
