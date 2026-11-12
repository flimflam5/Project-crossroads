@ Docked exploration only; no canonical plot, quest, trainer, reward or sailing flags.
SSAqua_GangwayCrew::
    msgbox SSAqua_GangwayCrewText, MSGBOX_NPC
    end
SSAqua_GangwayCrewText:
    .string "The gangway leads back to OLIVINE.\nMind your footing on the quay.$"
SSAqua_LoungeCrew::
    msgbox SSAqua_LoungeCrewText, MSGBOX_NPC
    end
SSAqua_LoungeCrewText:
    .string "These seats are a good place to\nwatch the harbor between shifts.$"
SSAqua_OfficerCrew::
    msgbox SSAqua_OfficerCrewText, MSGBOX_NPC
    end
SSAqua_OfficerCrewText:
    .string "The lower deck links both sides\nof the ship. Keep the stairs clear.$"
SSAqua_Captain::
    msgbox SSAqua_CaptainText, MSGBOX_NPC
    end
SSAqua_CaptainText:
    .string "We're alongside the OLIVINE quay.\nThe gangway is your way ashore.$"
SSAqua_CabinVisitor::
    msgbox SSAqua_CabinVisitorText, MSGBOX_NPC
    end
SSAqua_CabinVisitorText:
    .string "A quiet berth, a window, and a\nchance to sit down. That's enough.$"
SSAqua_DiningVisitor::
    msgbox SSAqua_DiningVisitorText, MSGBOX_NPC
    end
SSAqua_DiningVisitorText:
    .string "The table is bolted to the deck.\nA sensible precaution, I think.$"
SSAqua_RestingCrew::
    msgbox SSAqua_RestingCrewText, MSGBOX_NPC
    end
SSAqua_RestingCrewText:
    .string "Off-duty crew use these berths.\nPlease keep your voice down.$"
SSAqua_TwinBerthVisitor::
    msgbox SSAqua_TwinBerthVisitorText, MSGBOX_NPC
    end
SSAqua_TwinBerthVisitorText:
    .string "Two bunks and a sofa. There's\nmore room here than I expected.$"
SSAqua_MaintenanceCrew::
    msgbox SSAqua_MaintenanceCrewText, MSGBOX_NPC
    end
SSAqua_MaintenanceCrewText:
    .string "The crew quarters and galley are\nhere. The engine bay is farther on.$"
SSAqua_EngineCrew::
    msgbox SSAqua_EngineCrewText, MSGBOX_NPC
    end
SSAqua_EngineCrewText:
    .string "Stay outside the machinery's\nmarked safety boundary, please.$"
SSAqua_Chart::
    msgbox SSAqua_ChartText, MSGBOX_SIGN
    end
SSAqua_ChartText:
    .string "A harbor chart and a neatly\nsecured set of navigation tools.$"
SSAqua_Berth::
    lockall
    msgbox SSAqua_BerthText, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, SSAqua_BerthDecline
    closemessage
    call Common_EventScript_OutOfCenterPartyHeal
SSAqua_BerthDecline:
    releaseall
    end
SSAqua_BerthText:
    .string "A clean berth. Let your POKEMON\nrest for a little while?$"
