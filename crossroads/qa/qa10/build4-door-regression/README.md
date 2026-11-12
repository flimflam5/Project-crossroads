# Build 4 doorway regression — candidate rejected by independent facing review

Actual ROM: `4fb28fe64fc44c0546462a935655346a61f13b644bc3040468146d136cd6d656`.
All 519 normal controller approaches completed: 482 exact destination, position
and walk-away assertions passed; 37 lateral starts are physically unavailable.
The old scoped test asserted facing only where its contract supplied
expectations. Legacy rows with null expectations were recorded, not verified.

An independent physical-opening contract for all 45 groups then audited those
actual recorded facing values: **415 correct; 67 FAIL**. These are real legacy
facing defects. This candidate is therefore **not accepted or complete**.
Build 5 must correct the source and rerun all 519 cases with `--require-facing`.
The original executed script, its hash and the raw scoped report remain intact.
No earlier Build 4 frames or results are relabelled as Build 5.
