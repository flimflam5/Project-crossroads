	.include "sound/MPlayDef.s"
	.section .rodata
	.align 2

@ Dedicated voice and sample; no stock instrument/song is replaced.
BlackLedgerTitleVoice:
	.byte 8, 60, 0, 0 @ fixed-rate voice: no second resampling stage
	.word BlackLedgerTitleWave
	.byte 255, 0, 255, 0

	.align 2
BlackLedgerTitleWave:
	.word 0x40000000 @ ordinary direct sound with sample looping enabled
	.word 31536 * 1024 @ source rate at MIDI C3 (60)
	.word 0 @ provisional loop starts at sample zero
	.word BlackLedgerTitleSamplesEnd - BlackLedgerTitleSamples
BlackLedgerTitleSamples:
	.incbin "sound/direct_sound_samples/crossroads/black_ledger_title.pcm"
BlackLedgerTitleSamplesEnd:
	.align 2

BlackLedgerTitleTrack:
	.byte KEYSH, 0
	.byte TEMPO, 60
	.byte VOICE, 0
	.byte VOL, 127
	.byte PAN, c_v
	.byte TIE, Cn3, v127
BlackLedgerTitleWait:
	.byte W96
	.byte GOTO
	.word BlackLedgerTitleWait
	.byte FINE

	.align 2
	.global mus_black_ledger_title
mus_black_ledger_title:
	.byte 1, 0, 0, 0 @ one track, no blocks, normal priority, no reverb
	.word BlackLedgerTitleVoice
	.word BlackLedgerTitleTrack
