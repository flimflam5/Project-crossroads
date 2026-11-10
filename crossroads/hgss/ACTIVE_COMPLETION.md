# Active Ecruteak completion after QA04 — not a release

Continue branch feature/hgss-ecruteak-reconstruction-01 from690485c997.
The owner likes the city exterior. Preserve its facade/street composition. This
pass completes interiors, landmark floors and Joe's remaining player graphics.
No story actors, HGSS plot/reward flags, new rosters, badges or engine upgrades.

## Implemented checkpoint1

- Joe corporate field/Surf/Dive/bike/fish/water/decorating graphics; reserved custom
  IDs0x3f04–0x3f0b, no enum/dynamic-ID shift. Six dedicated animation tables retain
  timing and use authored east views rather than mirroring his satchel.
- Link-room and contest local-avatar source also points to Joe; remote/rival art
  remains. These modes are not playtested. See JOE_FIELD_AUDIT.md for exact scope.
- Station/corridor physical layouts and red prayer tables/tatami alcoves now follow
  HGSS geometry; original GBA temple assets. Station guard moves(15,7)->(16,6) to
  avoid the source's story-gated one-tile choke, without adding flags.
- Published Bell/Burned1–10F/summit references retrieved into scratch. Canonical
  interior permissions/prop/warp facts extracted for24 source headers. No HGSS
  graphics/story scripts are embedded in game data.

## Verified before tower reconstruction

Joe direction build /tmp/qa05-joe-direction-build.log PASS. Actual Fly ID+VRAM,
all ten cities, normal Save/fresh-core Continue PASS in
/tmp/qa05-directions-fly-runtime.log. Bikes, Acro wheelie, four-direction survey
Surf, rod casting/return to Surf and disembark PASS in
/tmp/qa05-directions-field-runtime.log. Temporary bike/rod inventory only exists
in private test emulator RAM. Existing opening/area/visual/save-contract/network
validators PASS before further map changes. Station/corridor two-way tour33
transitions PASS in /tmp/qa05-stage1b-station-runtime.log.

Latest build /tmp/qa05-checkpoint1-build.log PASS (ROM29,599,040bytes) includes local
contest/link previews and crisper palette-converted native timber floor. These later preview modes remain unplayed.

## Genuinely unfinished

build_hgss_ecruteak_interiors.py is authored but not yet executed/validated. It
projects canonical tower grids/branching warps and appends10F/roof. Preserve the
existing bell interaction by relocating it to the roof. Review actual rendering,
ramps/warp pads, all floor traversal and save compatibility before acceptance.

Still to implement/review: houses and Dowsing entrance, Theater, Center/Mart
reconstruction, Gym geometry/practice integration, region gates, city terrain
finishing and final whole-area regressions. Source branch is not owner-accepted
as finished. No QA05 download has been delivered. Original QA04 download remains.
