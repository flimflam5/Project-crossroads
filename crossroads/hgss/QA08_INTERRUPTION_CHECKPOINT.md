# QA08 recovery checkpoint — 2026-11-11

Latest owner scope: finish Ecruteak, then Olivine only. Preserve accepted designs,
custom Gyms, saves/IDs, starter/office/travel systems, title/V5 music, Joe and all
approved battles/encounters. No expansion elsewhere; no major story or badges.

## Safely committed and pushed

Branch feature/ecruteak-olivine-doorways-qa08. Draft PR15 targets the unmerged QA07
feature branch; no master merge is authorized. Ecruteak A1 d3ab461912 and B2
fd151242458efe5759b18650f35a5e5b2fa47e45 are committed with source/evidence.
Follow-up f83de9ed16d625d31d3226e0da8c3a9a7499249f moves the Pillow import into the
actual graphics converter. A separate shallow structural job had failed on the
unnecessary top-level import; both rerun story checks now pass. No game data
changes in f83. Main fd15124245 Emerald/FRLG builds pass; its longer engine test
job was still running when inspected. Never equate a started workflow with PASS.

Exact local controller-tested B2 ROM SHA256:
11ff9e15387d431c6bfb3b6f7b9642a922c80d7988be578aeedc93adc11d3632.
32MiB; Emerald payload30,056,736, EWRAM226,448, IWRAM28,392.
Local packages created, ZIP CRC/content hash verified before workspace disconnect:
/workspace/BlackLedger-Ecruteak-QA08-B2.gba
/workspace/BlackLedger-Ecruteak-QA08-B2.zip
/workspace/BlackLedger-Ecruteak-QA08-B2-Evidence.zip
CI artifact13832724891 (run42970984164) is a separate compiler build of PR merge
bc08059348e300dce088f1e90d47db2b6598d5fc; do not claim its bytes were emulator-tested.

B2 actual mGBA:161 executed doorway approaches/13 physically unavailable side
approaches skipped,27-map/308-transition/73-round-trip tour,10 gate wall/roof clips,
19 ground/tree/facade recordings,36 trunk approaches,423/423 foreground leaf pixels,
Theater performers, real shop purchase, nurse/PC/box integrity, Gym falls/Morty
loss/local whiteout, cold Save/Continue, obsolete-coordinate fixture, Joe Surf/
bikes/rod/Fly and all3 starters/met location/duplicate guard. Disclosed RAM setup
is documented in each tool; normal movement trials never rewrite map/warp/player
coordinates. Owner visual acceptance, complete interior raster comparison and the
exact unmatched original green-roof report remain open. Read ECRUTEAK_QA08_B2.md.

## Workspace interruption: do not discard surviving work

The managed workspace disconnected during the Olivine phase. Status service later
reported connected/running, but exec_command still returns 'No usable execution
environment is available' and wait_for_environment rejects the unavailable
selection. No further local compilation, map integration or emulator work could
be performed. Inspect the surviving working tree before changing anything.

Expected LOCAL, UNCOMMITTED Olivine work, not yet pushed or a playable milestone:
- crossroads/tools/build_hgss_olivine_assets.py: original facade converter, already
  ran successfully:654 new gfx,151 free before owner Gym. Native preview inspected.
- crossroads/hgss/art/olivine/facades-source.png and services-source.png, original
  generated HGSS-directed art; house/cafe/blue square lighthouse/barrel port plus
  Center/Mart native PNGs and manifest.json.
- data/tilesets/{primary,secondary}/hgss_olivine resources, generated successfully.
- HGSS OLIVINE resource blocks appended in include/tilesets.h and
  src/data/tilesets/{graphics,headers,metatiles}.h. No map uses them yet.
- crossroads/hgss/canonical_events/olivine-interior-geometry.json and
  olivine-reference-selection.json:18 SHA-backed source headers (includes port).
- Build diagnostic images build/olivine-facade-native-review.png and
  build/western-metatiles.png. No new ROM build occurred after these asset writes.

Local git was fd15124245 when disconnected. Remote now includes f83 and this
checkpoint. Recover by fetching and a safe fast-forward while preserving all
uncommitted files; do not reset or overwrite. If the changed include/graphics
files interfere, preserve them in a patch/copy first, then reapply and inspect.

## Olivine actual reference data and next implementation

/workspace/scratch/hgss-reference/Olivine_City_HGSS.png was inspected against the
actual HGSS reference. City canonical source origin256,224,64x64; entrance facts
in canonical_events/johto-outdoor-geometry.json MAP_OLIVINE. Three canonical homes,
cafe and port are MISSING in the old48x48 native city; all four accepted Black
Ledger locations (Joe, neighbour, Silph, harbor office) must remain additions.
The old native city's defined75 doorway trials had passed; do not invent an old
regression to justify replacement. Canonical reconstruction is not implemented.

Source archive cached as terrain-reference.narc, Git blob33105ab54c804a33503fb52db0ffa93a4d38191a,
reference only; never commit it or any ROM. Pin pret tree
6bf138d6035aa6b43d6f8f4132a12df70f86dcec. Cached olivine-complete-needed.json,
olivine-complete-downloads.json and olivine-complete-geometry.json reproduce18
headers through extract_hgss_interior_references.py. Actual trade-house/Gym
screenshots were visually inspected; full other-room raster refs still needed.

Resume by implementing the dedicated Olivine city/room/lighthouse/port generators,
not by replacing Ecruteak or propagating generic rooms. All three homes share
source matrix0097 (confirmed actual trade-house screenshot); cafe matrix0136 has
its own seating/counter shape. Preserve office starter case4,4, accepted services,
practice teams, home rest and travel scripts. Gym packer needs HgssOlivine source
entries and an authored OlivineCity contract/raw input before regeneration.
Old build_olivine_layout must delegate to the dedicated source; area_layouts.rooms
must skip dedicated Olivine landmark floors. Update generators and outputs together.

Lighthouse source floors are branched, not a plain six-room chain. Preserve all
six native map/layout IDs; append exterior balcony/elevator only. Source4F east
window16,9 drops to the exterior balcony, whose door8,12 leads into the isolated
south3F section and west stairs to4F/5F/top. Respect source clearances/arrivals.
Use source-bounded floors to avoid flooding into unused DS model space. Native
GBA dynamic elevator support exists; no new save structures/progress flags needed.
Do not mark cabin/balcony implemented until connected and controller-tested.

Keep both existing route connections. Adjust geometry/offsets only as necessary,
and preserve scrolling-buffer graphics both ways; full private-secondary swaps
previously corrupted the Route38/39 farm seam. Keep IDs append-only. New canonical
city door positions require safe old-save landing/heal metadata migration while
preserving real Surf saves. Test copies only. Do not overwrite private fixtures.

Routine Olivine work remains authorized; do not ask for a general go-ahead again.
Deliver a separate identifiable Olivine build only after it compiles and the actual
delivery bytes pass doorway/service/landmark/Save/cold Continue regressions.
