# Joe corporate integration recovery

Recovered from local 400e179bc0 without resetting source. Dedicated Joe ID reuses
unused slot250; dynamic graphics IDs and saved gender remain unchanged. Supplied
16 frames are repacked with explicit four-direction animation and running fallback.
Dedicated draft trainer front/back/Card artwork is integrated; source and conversion
provenance are under graphics/trainers/joe/reference.

Verified surviving logs: Emerald build PASS (ROM26776384, EWRAM226420,IWRAM28392).
Both gender0 and gender1 runtime smoke tests PASS: Joe directional VRAM, all seven
building returns, both piers, all three rescue/met-location branches, duplicate
guards, terminal travel and healing/menu stability. Asset validator PASS.

Recovery verification: the resumed old-save Continue/100-byte comparison produced
a Trainer Card screenshot showing Joe. A debugger-started wild battle visibly
rendered Joe’s back artwork and returned to the Center with Joe visible.
Still required: comprehensive normal SRAM save/reload, special movement return
tests, and owner Delta QA. These checks do not constitute a complete opening playthrough.
Special bike/surf/fish/field-move art and original introduction remain placeholders.
Running reuses supplied walk poses at faster timing. Title concept is unapproved
and unintegrated. Do not mark full Release1 accepted or complete from these checks.

Resume runtime verification before adding title/region changes. Complete current
commit/push/artifact delivery first; preserve Silph starter case and metadata logic.
