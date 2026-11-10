# Western Johto 0.4 — Route 39 traversal increment

The Olivine north road now connects directly to Route 39 through a normal map
border. Walk north from the central road, explore the countryside, and return
south. Route 39 has scenery, a pedestrian and direction signs. Its northern
boundary explicitly marks Route 38 as unfinished. No arbitrary teleport or new
starter grant is used. This is a connected exploration blockout, not finished
Route 39 or a claim that Johto is complete. Encounters, trainers, farm interiors
and Route 38/Ecruteak are not implemented in this increment.

The owner confirmed manual Delta QA PASS for Joe 0.3 (f40e5028c3). This increment
preserves its character integration, Silph rescue, origin metadata, saved choice
and existing city/interior IDs. Existing Pokémon origin data remains untouched.
The Johto region-map UI is not implemented; the internal Emerald build filter
remains REGION_HOENN. Route 39 has its own displayed map-section name.

## Delta checklist

1. Back up your Joe 0.3 save. Continue with this ROM; check Joe and your party.
2. Follow Olivine's central road north past the sign. Cross the border normally.
   Confirm ROUTE 39 appears and Joe remains visible while facing/walking each way.
3. Walk to the northern end, read its boundary sign, and speak to the pedestrian
   near the middle clearing. Route 38 is intentionally closed.
4. Walk south back to Olivine. Repeat the crossing near both edges of the road.
5. Save on Route 39, reload through Continue, and walk back to Olivine. Repeat
   saving on the city side. Confirm party, items and starter choice persist.
6. Recheck city doors, healing, signs, Silph rescue duplication guards and battles.

Known limitations: countryside art is a temporary compatible Emerald blockout;
no route encounters/trainers yet. Lighthouse/Gym/interiors remain temporary.
Joe's special movement states and original intro remain unfinished. The owner-supplied Pokémon: Black Ledger title
reference supersedes the prior proposal and is not implemented in this ROM.
The summary UI remains unchanged. Manual Delta QA is pending for 0.4.

## Verification at this checkpoint

BUILD PASS: Emerald linked ROM 26,779,092 bytes; EWRAM 226,420; IWRAM 28,392.
Asset/script/map validators and reproducible city/route layouts passed. Both
save-gender mGBA fixtures passed all existing regression checks plus actual
Route 39 border entry, full north/south traversal, sign dismissal and return.
Normal Route 39 SRAM Save/Continue and owner Delta QA remain pending.
