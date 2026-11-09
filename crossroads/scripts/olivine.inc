@ Olivine City foundation 0.1. Temporary exploration access, not story progression.
@ Keep Alpha rescue scripts and VAR_CROSSROADS_STARTER values unchanged.

Olivine_OfferVisit::
    msgbox Olivine_Text_Visit, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Olivine_EndVisit
    closemessage
    warp MAP_OLIVINE_CITY, 12, 13
    waitstate
Olivine_EndVisit:
    releaseall
    end

Olivine_ReturnToAlpha::
    lock
    faceplayer
    msgbox Olivine_Text_Return, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Olivine_EndVisit
    closemessage
    warp MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F, 3, 2
    waitstate
    releaseall
    end

Olivine_OnTransition:
    callnative Crossroads_EnsureAreaRespawn
    @ Standard menu availability after a successful Alpha rescue.
    goto_if_eq VAR_CROSSROADS_STARTER, 0, Olivine_NoPartnerYet
    setflag FLAG_SYS_POKEMON_GET
Olivine_NoPartnerYet:
    end

Olivine_CenterOnTransition:
    setrespawn HEAL_LOCATION_OLIVINE_CITY
    end

Olivine_Nurse::
    setvar VAR_0x800B, LOCALID_OLIVINE_NURSE
    call Common_EventScript_PkmnCenterNurse
    waitmessage
    waitbuttonpress
    release
    end

Olivine_Clerk::
    lock
    faceplayer
    message gText_HowMayIServeYou
    waitmessage
    pokemart Olivine_MartStock
    msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
    release
    end

    .align 2
Olivine_MartStock:
    .2byte ITEM_POKE_BALL
    .2byte ITEM_POTION
    .2byte ITEM_ANTIDOTE
    .2byte ITEM_PARALYZE_HEAL
    pokemartlistend

Olivine_Terminal::
    msgbox Olivine_Text_Terminal, MSGBOX_DEFAULT
    end

Olivine_PartnerReaction::
    lock
    faceplayer
    goto_if_eq VAR_CROSSROADS_STARTER, 1, Olivine_ElgyemReaction
    goto_if_eq VAR_CROSSROADS_STARTER, 2, Olivine_SeedotReaction
    goto_if_eq VAR_CROSSROADS_STARTER, 3, Olivine_TrubbishReaction
    msgbox Olivine_Text_NoPartner, MSGBOX_DEFAULT
    release
    end

Olivine_ElgyemReaction:
    msgbox Olivine_Text_Elgyem, MSGBOX_DEFAULT
    release
    end

Olivine_SeedotReaction:
    msgbox Olivine_Text_Seedot, MSGBOX_DEFAULT
    release
    end

Olivine_TrubbishReaction:
    msgbox Olivine_Text_Trubbish, MSGBOX_DEFAULT
    release
    end

Olivine_Text_Visit:
    .string "OLIVINE EXPLORATION BUILD 0.1\p"
    .string "Visit the city blockout?\nStory events are not active yet.$"

Olivine_Text_Return:
    .string "Return to the Alpha test room?\p"
    .string "Your partner and saved progress\nwill stay with you.$"

Olivine_Text_Terminal:
    .string "SILPH OLIVINE: STAFF TERMINAL\p"
    .string "Freight schedules and delivery\nrecords fill the screen.\p"
    .string "Incoming loads: check the seals.\nOutgoing loads: match the records.$"

Olivine_Text_NoPartner:
    .string "A partner makes a long walk\nfeel a little shorter.$"

Olivine_Text_Elgyem:
    .string "Your ELGYEM keeps watching\nthe lights on the waterfront.$"

Olivine_Text_Seedot:
    .string "Your SEEDOT looks settled.\nTry the shade by the houses.$"

Olivine_Text_Trubbish:
    .string "Your TRUBBISH seems happy here.\nThere's room for everyone.$"

Olivine_HomeNotes::
    msgbox Olivine_Text_HomeNotes, MSGBOX_DEFAULT
    end

Olivine_Text_HomeNotes:
    .string "JOE: Rent, work, groceries.\p"
    .string "An ordinary week, on paper.$"

Olivine_Neighbor::
    msgbox Olivine_Text_Neighbor, MSGBOX_NPC
    end

Olivine_Text_Neighbor:
    .string "I open my windows in the morning.\p"
    .string "Salt air beats an alarm clock.$"

Olivine_GymGuide::
    msgbox Olivine_Text_GymGuide, MSGBOX_NPC
    end

Olivine_Text_GymGuide:
    .string "OLIVINE GYM - temporary lobby.\p"
    .string "Battles and the Gym interior\nare not in this build yet.$"

Olivine_OfficeWorker::
    msgbox Olivine_Text_OfficeWorker, MSGBOX_NPC
    end

Olivine_Text_OfficeWorker:
    .string "Another delivery, another form.\p"
    .string "The harbor keeps us busy.$"

Olivine_HarborClerk::
    msgbox Olivine_Text_HarborClerk, MSGBOX_NPC
    end

Olivine_Text_HarborClerk:
    .string "The piers are open for a walk.\p"
    .string "There are no passenger departures\ntoday. Freight crews report here.$"

Olivine_CenterVisitor::
    msgbox Olivine_Text_CenterVisitor, MSGBOX_NPC
    end

Olivine_Text_CenterVisitor:
    .string "A rest and a fresh start.\p"
    .string "Some days, that is all you need.$"

Olivine_MartVisitor::
    msgbox Olivine_Text_MartVisitor, MSGBOX_NPC
    end

Olivine_Text_MartVisitor:
    .string "I keep an ANTIDOTE in my bag.\p"
    .string "Better to have it and not need it.$"

Olivine_DockWorker::
    msgbox Olivine_Text_DockWorker, MSGBOX_NPC
    end

Olivine_Text_DockWorker:
    .string "The early shift gets the sunrise.\p"
    .string "The late shift gets the paperwork.$"

Olivine_Commuter::
    msgbox Olivine_Text_Commuter, MSGBOX_NPC
    end

Olivine_Text_Commuter:
    .string "You can hear the harbor from here.\p"
    .string "I hardly notice it anymore.$"

Olivine_Resident::
    msgbox Olivine_Text_Resident, MSGBOX_NPC
    end

Olivine_Text_Resident:
    .string "The Center and MART are just west.\p"
    .string "The office is across the street.$"

Olivine_OfficeCommuter::
    msgbox Olivine_Text_OfficeCommuter, MSGBOX_NPC
    end

Olivine_Text_OfficeCommuter:
    .string "I took the long way to work.\p"
    .string "Five extra minutes by the sea.$"

Olivine_LighthouseVisitor::
    msgbox Olivine_Text_LighthouseVisitor, MSGBOX_NPC
    end

Olivine_Text_LighthouseVisitor:
    .string "The lighthouse belongs down here,\nwatching over the harbor.\p"
    .string "You can climb to the lantern room.\nThe view is worth the stairs.$"

Olivine_PierWorker::
    msgbox Olivine_Text_PierWorker, MSGBOX_NPC
    end

Olivine_Text_PierWorker:
    .string "Mind the railings.\p"
    .string "No ship departures in this build.$"

Olivine_ResidenceSign::
    msgbox Olivine_Text_ResidenceSign, MSGBOX_SIGN
    end

Olivine_Text_ResidenceSign:
    .string "JOE'S RESIDENCE\p"
    .string "Return to the Alpha room inside.$"

Olivine_NeighborSign::
    msgbox Olivine_Text_NeighborSign, MSGBOX_SIGN
    end

Olivine_Text_NeighborSign:
    .string "OLIVINE RESIDENTIAL STREET$"

Olivine_GymSign::
    msgbox Olivine_Text_GymSign, MSGBOX_SIGN
    end

Olivine_Text_GymSign:
    .string "OLIVINE GYM\p"
    .string "Optional practice battles inside.$"

Olivine_CenterSign::
    msgbox Olivine_Text_CenterSign, MSGBOX_SIGN
    end

Olivine_Text_CenterSign:
    .string "POKEMON CENTER\p"
    .string "Rest and PC storage available.$"

Olivine_MartSign::
    msgbox Olivine_Text_MartSign, MSGBOX_SIGN
    end

Olivine_Text_MartSign:
    .string "POKEMON MART\p"
    .string "Everyday supplies for your team.$"

Olivine_OfficeSign::
    msgbox Olivine_Text_OfficeSign, MSGBOX_SIGN
    end

Olivine_Text_OfficeSign:
    .string "SILPH CO. - OLIVINE OFFICE\p"
    .string "Logistics and freight coordination.$"

Olivine_HarborSign::
    msgbox Olivine_Text_HarborSign, MSGBOX_SIGN
    end

Olivine_Text_HarborSign:
    .string "OLIVINE HARBOR OFFICE\p"
    .string "Freight records and berth schedules.$"

Olivine_LighthouseSign::
    msgbox Olivine_Text_LighthouseSign, MSGBOX_SIGN
    end

Olivine_Text_LighthouseSign:
    .string "OLIVINE LIGHTHOUSE\p"
    .string "Six floors. Lantern room above.$"

Olivine_CityDirectory::
    msgbox Olivine_Text_CityDirectory, MSGBOX_SIGN
    end

Olivine_Text_CityDirectory:
    .string "OLIVINE CITY\p"
    .string "NORTH: Homes and GYM practice hall.\nCENTRE: Healing, MART and SILPH.\p"
    .string "SOUTH: Harbor offices and LIGHTHOUSE.\nNorth road: ROUTE 39.$"

Olivine_NorthBoundary::
    msgbox Olivine_Text_NorthBoundary, MSGBOX_SIGN
    end

Olivine_Text_NorthBoundary:
    .string "NORTH: ROUTE 39\p"
    .string "Follow the road north to ROUTE 39.\nThe road back remains open.$"

@ Keep old Alpha saves usable without granting a new mon in Littleroot.
Crossroads_EventScript_VisitRescueCase::
    lockall
    goto_if_ne VAR_CROSSROADS_STARTER, 0, Crossroads_EventScript_AlreadyChosen
    msgbox Crossroads_Text_VisitRescueCase, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Olivine_EndVisit
    closemessage
    warp MAP_OLIVINE_CITY_SILPH_OFFICE, 3, 6
    waitstate
    releaseall
    end

Crossroads_Text_VisitRescueCase:
    .string "The rescue case is at SILPH's\nOLIVINE office now.\p"
    .string "Visit the SILPH office?$"
