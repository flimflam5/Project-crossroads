# QA10 B4 — independent arrival-facing audit

The desired directions below were recorded before reading actual facing records.
They follow the target landing and its physical doorway normal, using the existing
visible-opening approach vectors and actual native/HGSS layouts. The current
controller opening inventory was not modified. This is an additional strict check,
not a replacement for door, collision, walking-away or owner visual QA.

Contract: [all45 physical groups](doorway-intended-facing-b4.json).
Checker: `crossroads/tools/validate_qa10_arrival_facing.py`.

## Physical expectations

For ordinary thresholds, arrival faces away from the target threshold into its
landing: the inverse of that target side's exit/approach vector. North entrances
therefore face south indoors; south entrances face north indoors. Side gates
must face along their east/west aisle, not automatically south.

Two explicit exceptions are the same-orientation right ship stairs: the north
rim arrives south into the lower landing; the south rim arrives north into the
upper landing. The actual source B1F ordinal2 maps to canonical1F row9; native
aliases preserve this. This exception was determined from the source stair
geometry, not copied from an observed facing. Both west ship stairs instead
have north-facing mouths and arrive south into their landings.

| Group | Arrive on outside side | Arrive on inside side |
| --- | --- | --- |
| theater | South | North |
| barrier | South | North |
| gym | South | North |
| southwest-house | South | North |
| dowsing-house | South | North |
| center | South | North |
| mart | South | North |
| burned-tower | South | North |
| west-city-gate | East | West |
| west-route-gate | West | East |
| east-city-gate | West | East |
| east-route-gate | East | West |
| bell-tower | South | North |
| trail-station-return | South | South |
| station-corridor-stairs | South | North |
| olivine-joe-residence | South | North |
| olivine-accepted-neighbour | South | North |
| olivine-custom-gym | South | North |
| olivine-pokemon-center | South | North |
| olivine-poke-mart | South | North |
| olivine-silph-office | South | North |
| olivine-harbor-office | South | North |
| olivine-lighthouse | South | North |
| olivine-fishing-house | South | North |
| olivine-trade-house | South | North |
| olivine-seal-house | South | North |
| olivine-cafe | South | North |
| olivine-port-city-entrance | North | South |
| olivine-gym-hallway | South | North |
| olivine-port-quay-main | South | North |
| olivine-port-inspection-side | West | East |
| olivine-lighthouse-balcony | South | North |
| aqua-gangway | South | North |
| aqua-southwestcabins-0 | North | South |
| aqua-southwestcabins-1 | North | South |
| aqua-southeastcabins-0 | North | South |
| aqua-southeastcabins-1 | North | South |
| aqua-northwestcabins-0 | South | North |
| aqua-northwestcabins-1 | South | North |
| aqua-northeastcabins-0 | South | North |
| aqua-northeastcabins-1 | South | North |
| aqua-captainroom-0 | South | North |
| aqua-west-stairs | South | South |
| aqua-right-stairs-north-rim | South | South |
| aqua-right-stairs-south-rim | North | North |

## Implementation cross-check

`GetAdjustedInitialDirection` in `src/overworld.c` explains the mechanics: native
nonanimated/animated doors force south, north/south/east/west arrow warps force
their respective exit direction, ladders preserve the stored entering direction,
and ordinary floor defaults south. Some existing gate arrival-only anchors are
ordinary floor, which cannot establish a correct horizontal arrival automatically.
The actual controller records, not static behavior alone, establish the result.

## Real B4 defects found

Final frozen B4 audit: all519 attempts are recorded. The new strict postcheck rejects67 actual arrivals:
65 attempts through the four Ecruteak east/west city/route gate links face south
instead of west/east into their landings; two Trail→BarrierCorridor attempts at
(6,3) face north toward the threshold instead of south into the corridor. The
remaining37 unavailable lateral approaches are separately reported and receive
no facing pass.415 actual successful arrivals face correctly. There are no missing
attempts. Exact final audit: `build/qa10-b4-facing-audit-final.json`.
These are real legacy direction defects, not grounds to weaken the expectation.

The complete519-record result must be checked after the active run ends. A
controller traversal result labelled PASS can still fail this independently added
facing requirement. No game source/resource changes or extra emulator runs were
made during this audit; the coordinator decides and tests the narrow repair.

Final invocation after the result file exists:

```sh
python3 crossroads/tools/validate_qa10_arrival_facing.py \
  --results build/qa10-b4-doorways/doorway-results.json \
  --output build/qa10-b4-facing-audit-final.json
```

The strict checker requires all519 unique attempts, valid source/destination/cell
identities, the exact frozen ROM/opening-contract hashes and unchanged original
save. Unavailable approaches may only be lateral; front approaches cannot be
omitted. Every successful attempt must match the independently intended facing.
An incomplete raw-log diagnostic can never become FINAL PASS.
