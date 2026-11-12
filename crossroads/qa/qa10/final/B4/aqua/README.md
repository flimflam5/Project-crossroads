# QA10 B4 physical S.S.Aqua evidence

Game source: `df8c4598d88c7770626be4621a5f39cf60dadb95`.
ROM SHA256: `4fb28fe64fc44c0546462a935655346a61f13b644bc3040468146d136cd6d656`.

[Native images and movement recordings](gallery.html) · [exact results](results.json) ·
[reproducible command and hashes](runner-mapping.json) · [checksums](evidence-manifest.json).

The overall B4 candidate FAILED a separate Ecruteak gate/trail intended-facing
audit. These scoped B4 ship passes are historical evidence, not overall delivery
acceptance or a claim that the pending B5 correction has been tested.

The FULL default detail runner executed on the frozen B4 candidate ROM. No
`--skip-bumps` option was used. Actual controller travel covers all seven ship
maps and all twelve physical source-room components, including paired cabins;
each room has a normal menu Save and cold Continue. Source-derived solid-target
bumps, furnishing contexts, actual NPC/sign interactions, berth decline/accept
and the real return to Olivine are recorded in results.json.

Two isolated same-ROM snapshot fixtures temporarily lower the first party
member's HP/status solely to test actual berth NO/YES behavior. The native
choice task and cursor are verified; NO preserves low HP/poison, YES heals all
party HP/status, then exact pre-fixture payload is restored. No party identity,
item, coordinate or story flags are seeded. Whole-tour integrity normalizes only
the normal-walking friendship byte and its checksum; every individual Save/NPC
check requires exact party bytes. Shared test-RAM encounter/Survey assistance is
disclosed. The input battery remains unchanged, with per-phase ROM/ELF and
original/copy battery guards in serial-completion.json.

These are actual scripted emulator tests, distinct from source checks, build
success, image inspection and owner acceptance. Native PNGs and H264 MP4s are
240x160. No private saves, snapshots, ROM/ELF, memory dumps or raw frame folders
are included. The owner's newest private save was not available.

Physical visitor boarding and furnished ship exploration do not authorize or
implement an unapproved destination, timetable, ticket, reward or story event.
Interregional sailings remain separately documented and owner visual acceptance
is pending. Source/reproduction commands are in runner-mapping.json.
