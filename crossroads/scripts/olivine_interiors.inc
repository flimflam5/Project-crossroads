@ Everyday interactions. No new canon, persistent flags, item grants or rescue path.
Olivine_HomeRest::
    lockall
    msgbox Olivine_Text_RestPrompt, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Olivine_HomeRestEnd
    fadescreen FADE_TO_BLACK
    special HealPlayerParty
    playfanfare MUS_HEAL
    waitfanfare
    fadescreen FADE_FROM_BLACK
    msgbox Olivine_Text_Rested, MSGBOX_DEFAULT
Olivine_HomeRestEnd:
    releaseall
    end
Olivine_Text_RestPrompt:
    .string "Take a short rest?$"
Olivine_Text_Rested:
    .string "A quiet moment at home.\nYou feel ready to head out.$"

Olivine_HomeBooks::
    msgbox Olivine_Text_HomeBooks, MSGBOX_SIGN
    end
Olivine_Text_HomeBooks:
    .string "Shipping guides, an old atlas,\nand a book with a folded page.$"

Olivine_FreightChecklist::
    msgbox Olivine_Text_FreightChecklist, MSGBOX_SIGN
    end
Olivine_Text_FreightChecklist:
    .string "FREIGHT CHECKLIST\pCount the cases. Check the seals.\nMatch each load to its manifest.$"

Olivine_StaffBoard::
    msgbox Olivine_Text_StaffBoard, MSGBOX_SIGN
    end
Olivine_Text_StaffBoard:
    .string "STAFF NOTICE\pLog every handover. Return keys\nto the desk before leaving.$"

Olivine_HarborLedger::
    msgbox Olivine_Text_HarborLedger, MSGBOX_SIGN
    end
Olivine_Text_HarborLedger:
    .string "HARBOR LEDGER\pBerths, arrival times and freight\nweights fill the open pages.$"

Olivine_HarborDispatch::
    msgbox Olivine_Text_HarborDispatch, MSGBOX_SIGN
    end
Olivine_Text_HarborDispatch:
    .string "HARBOR DISPATCH\pCargo crews report here before\nloading or unloading.\pPassenger departures are handled\nseparately. No tickets here.$"
