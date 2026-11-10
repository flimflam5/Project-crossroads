# Ecruteak QA07 traversal overview

All nodes below are existing maps. IDs, connection offsets and entrance indexes
are unchanged. Actual doorway/pad pairs and map-header connections are recorded
individually in [the checklist](ecruteak-qa07-checklist.json) and
[controller coverage](../qa/ecruteak-qa07/city-tour/coverage.json).

```mermaid
flowchart LR
  R38[Route 38] <--> W[West Gate]
  W <--> C[Ecruteak City]
  C <--> E[East Gate]
  E <--> R42[Route 42]
  C <--> R37[Route 37]
  C <--> H1[Southwest Residence]
  C <--> H2[Dowsing House]
  C <--> T[Dance Theater]
  C <--> M[Mart]
  C <--> P[Center 1F]
  P <--> PB[Center B1F]
  C <--> G[Gym lower bridge]
  G <--> GA[Gym upper bridge]
  C <--> B[Burned Tower 1F]
  B <--> BB[Burned Tower B1F]
  C <--> S[Barrier Station]
  S <--> SC[Barrier Corridor]
  SC <--> BT[Bellchime Trail]
  BT <--> F1[Bell 1F]
  F1 <--> F2[Bell 2F]
  F2 <--> F3[Bell 3F]
  F3 <--> F4[Bell 4F]
  F4 <--> F5[Bell 5F]
  F5 <--> F6[Bell 6F]
  F6 <--> F7[Bell 7F]
  F7 <--> F8[Bell 8F]
  F8 <--> F9[Bell 9F]
  F7 <--> F9
  F9 <--> F10[Bell 10F]
  F10 <--> RF[Bell Roof]
```

The Bell outline shows floor order; individual same-map pads, cross-floor branches,
one-way ledges and disjoint walkway components require the exact warp graph in
the JSON/coverage. The emulator plans by entry position, not just floor name.
Gym falls return to the lower entrance without granting badges or story flags.

The city retains its west/east map-header scrolling connections for rendering;
walking the three-cell apertures executes the existing coordinate gate scripts.
South remains a normal route border. Blocked north/perimeter and pond edges were
checked; decorative closed homes have explicit private-door text, no empty rooms.
