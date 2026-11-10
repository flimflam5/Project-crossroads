@ Explicit owner-requested persistent QA grants. Hold R when speaking to desk.
Johto_QAKit::
    msgbox Johto_QAKitPrompt, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Johto_TestEnd
    setflag FLAG_SYS_B_DASH
    goto_if_set FLAG_BLACK_LEDGER_QA_FLYER, Johto_QAKitDone
    getpartysize
    goto_if_ge VAR_RESULT, PARTY_SIZE, Johto_QAKitFull
    givemon SPECIES_PIDGEOT, 100, ITEM_NONE, move1=MOVE_FLY, move2=MOVE_AERIAL_ACE, move3=MOVE_ROOST, move4=MOVE_QUICK_ATTACK
    goto_if_eq VAR_RESULT, MON_CANT_GIVE, Johto_QAKitFull
    setflag FLAG_BLACK_LEDGER_QA_FLYER
Johto_QAKitDone:
    msgbox Johto_QAKitReady, MSGBOX_DEFAULT
    goto Johto_TestEnd
Johto_QAKitFull:
    msgbox Johto_QAKitNoRoom, MSGBOX_DEFAULT
    goto Johto_TestEnd
Johto_QAKitPrompt:
    .string "QA KIT: Level 100 PIDGEOT with\nFLY, and RUNNING SHOES?\pThese stay in this save.\nAccept the testing kit?$"
Johto_QAKitReady:
    .string "RUNNING SHOES enabled: hold B.\nYour QA PIDGEOT is ready.\pOnly one QA flyer per save.\nUse FLY outdoors to choose a city.$"
Johto_QAKitNoRoom:
    .string "RUNNING SHOES enabled.\nMake room for one POKeMON,\pthen return for your QA flyer.$"
