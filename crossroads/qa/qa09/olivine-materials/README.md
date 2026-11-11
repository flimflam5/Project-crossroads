# Olivine BUILD9 material and collision regression

Tested ROM SHA256: `d5abac0deabc7d592eba302122b3d15c08501947f0f601eda7b5026da9ac6772`.
This evidence is from fresh cold title/Continue on the actual BUILD9 delivery ROM,
using a copied normal battery. No older emulator state or test result was reused.
The original battery was unchanged (before/after SHA256 recorded in results.json).

Actual normal-controller gameplay checks passed:

- All 12 obsolete source-table cells crossed on dry ground, in three recorded groups.
- All 20 surviving source-backed white fence cells tested: 43 accessible-side bumps
  blocked movement. 37 unavailable sides are individually disclosed in results.json
  and were not counted as passes.
- Timber promenade crossed; all three parasol canopies traversed and all three
  real table bases blocked movement. Foreground canopy overlap remains intentional.
- Four distinct gray offshore rock groups blocked actual Surf movement.
- Joe actually Surfed through the formerly blocked Port model body, confirming
  restored native sea rather than an invisible grass island.
- The southern engine sea boundary blocked movement; Joe returned to dry Port
  ground and then the Center forecourt at (16,34).
- Zero unexplained ground-arrow visibility samples across 18 native recordings.

The harness uses the real optional survey desk for RAM-only Surf access, leaving
saved flags unchanged. It suppresses random encounters only in the emulator's
memory to make movement repeatable. It never writes player coordinates, map IDs,
warps or permanent progress. The original copy-only battery remains private.

The nine compact MP4 files and PNG endpoints here are native 240×160 evidence.
The raw private build output contains all 18 clips. Representative first/middle/last
frames were visually inspected for table walking, parasol overlap, garden fencing,
gray rock contact, restored Port water and the southern sea edge. These are actual
emulator checks; owner visual acceptance and Delta testing remain separate.

Source tests independently pin all 4096 city collision/elevation words to V7,
except the 12 explicitly relocated table cells and 65 source model167 Port-body
cells restored to native sea. They also check correct materials, real cliffs,
boat/roof water and layer behavior, open arch roads and Route40 buffer compatibility.
See `crossroads/hgss/OLIVINE_MATERIAL_CORRECTIONS_QA09.md`.
