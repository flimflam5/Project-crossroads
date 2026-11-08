@ Western Johto exploration only. No new story flags, starter grant or Gym rewards.
Ecruteak_CenterOnTransition::
    setrespawn HEAL_LOCATION_ECRUTEAK_CITY
    end

Ecruteak_Nurse::
    setvar VAR_0x800B, LOCALID_ECRUTEAK_NURSE
    call Common_EventScript_PkmnCenterNurse
    waitmessage
    waitbuttonpress
    release
    end

Route38_Traveler::
    msgbox Route38_Traveler_Text, MSGBOX_NPC
    end
Route38_Traveler_Text:
    .string "The road east reaches ECRUTEAK.\nOLIVINE is back to the southwest.$"

Route38_Walker::
    msgbox Route38_Walker_Text, MSGBOX_NPC
    end
Route38_Walker_Text:
    .string "The trees shelter this road\nwhen the sea wind picks up.$"

Route38_WestSign::
    msgbox Route38_WestSign_Text, MSGBOX_SIGN
    end
Route38_WestSign_Text:
    .string "ROUTE 38\nSouth: ROUTE 39 and OLIVINE CITY.$"

Route38_EastSign::
    msgbox Route38_EastSign_Text, MSGBOX_SIGN
    end
Route38_EastSign_Text:
    .string "ROUTE 38\nEast: ECRUTEAK CITY.$"

Ecruteak_Traveler::
    msgbox Ecruteak_Traveler_Text, MSGBOX_NPC
    end
Ecruteak_Traveler_Text:
    .string "Follow the western street for\nROUTE 38 and the road to OLIVINE.$"

Ecruteak_Resident::
    msgbox Ecruteak_Resident_Text, MSGBOX_NPC
    end
Ecruteak_Resident_Text:
    .string "The towers make useful landmarks.\nI still get turned around sometimes.$"

Ecruteak_GymVisitor::
    msgbox Ecruteak_GymVisitor_Text, MSGBOX_NPC
    end
Ecruteak_GymVisitor_Text:
    .string "The GYM is in the southwest.\nIts battle area is not open yet.$"

Ecruteak_TowerVisitor::
    msgbox Ecruteak_TowerVisitor_Text, MSGBOX_NPC
    end
Ecruteak_TowerVisitor_Text:
    .string "The BELL TOWER entrance is ahead.\nThe upper floors are not open yet.$"

Ecruteak_Shopper::
    msgbox Ecruteak_Shopper_Text, MSGBOX_NPC
    end
Ecruteak_Shopper_Text:
    .string "I buy supplies before a long walk.\nIt saves a trip back.$"

Ecruteak_TheaterVisitor::
    msgbox Ecruteak_TheaterVisitor_Text, MSGBOX_NPC
    end
Ecruteak_TheaterVisitor_Text:
    .string "The DANCE THEATER is up this path.\nThere are no performances yet.$"

Ecruteak_BurnedGuide::
    msgbox Ecruteak_BurnedGuide_Text, MSGBOX_NPC
    end
Ecruteak_BurnedGuide_Text:
    .string "BURNED TOWER\pThis is a temporary entrance room.\nThe tower interior is not built yet.$"

Ecruteak_BellGuide::
    msgbox Ecruteak_BellGuide_Text, MSGBOX_NPC
    end
Ecruteak_BellGuide_Text:
    .string "BELL TOWER\pThis is a temporary entrance room.\nThe upper floors are not built yet.$"

Ecruteak_Host::
    msgbox Ecruteak_Host_Text, MSGBOX_NPC
    end
Ecruteak_Host_Text:
    .string "Make yourself comfortable.\nThe port road is a long walk.$"

Ecruteak_TheaterGuide::
    msgbox Ecruteak_TheaterGuide_Text, MSGBOX_NPC
    end
Ecruteak_TheaterGuide_Text:
    .string "ECRUTEAK DANCE THEATER\pThis is a temporary lobby.\nThe stage is not built yet.$"

Ecruteak_GymGuide::
    msgbox Ecruteak_GymGuide_Text, MSGBOX_NPC
    end
Ecruteak_GymGuide_Text:
    .string "ECRUTEAK GYM\pThis is a temporary lobby.\nBattles and badges come later.$"

Ecruteak_CenterVisitor::
    msgbox Ecruteak_CenterVisitor_Text, MSGBOX_NPC
    end
Ecruteak_CenterVisitor_Text:
    .string "A rest here makes the return\ntrip to OLIVINE much easier.$"

Ecruteak_BurnedTowerSign::
    msgbox Ecruteak_BurnedTowerSign_Text, MSGBOX_SIGN
    end
Ecruteak_BurnedTowerSign_Text:
    .string "BURNED TOWER\nTemporary exterior and entrance.$"

Ecruteak_BellTowerSign::
    msgbox Ecruteak_BellTowerSign_Text, MSGBOX_SIGN
    end
Ecruteak_BellTowerSign_Text:
    .string "BELL TOWER\nTemporary exterior and entrance.$"

Ecruteak_ResidenceSign::
    msgbox Ecruteak_ResidenceSign_Text, MSGBOX_SIGN
    end
Ecruteak_ResidenceSign_Text:
    .string "ECRUTEAK RESIDENCE$"

Ecruteak_DanceTheaterSign::
    msgbox Ecruteak_DanceTheaterSign_Text, MSGBOX_SIGN
    end
Ecruteak_DanceTheaterSign_Text:
    .string "ECRUTEAK DANCE THEATER\nTemporary exterior and lobby.$"

Ecruteak_GymSign::
    msgbox Ecruteak_GymSign_Text, MSGBOX_SIGN
    end
Ecruteak_GymSign_Text:
    .string "ECRUTEAK GYM\nTemporary lobby. Battles pending.$"

Ecruteak_PokemonCenter_1FSign::
    msgbox Ecruteak_PokemonCenter_1FSign_Text, MSGBOX_SIGN
    end
Ecruteak_PokemonCenter_1FSign_Text:
    .string "POKEMON CENTER\nRest and care for your team.$"

Ecruteak_MartSign::
    msgbox Ecruteak_MartSign_Text, MSGBOX_SIGN
    end
Ecruteak_MartSign_Text:
    .string "POKEMON MART\nSupplies for the road.$"

Ecruteak_WestSign::
    msgbox Ecruteak_WestSign_Text, MSGBOX_SIGN
    end
Ecruteak_WestSign_Text:
    .string "West: ROUTE 38.\nOLIVINE via ROUTE 39.$"

Ecruteak_EastBoundary::
    msgbox Ecruteak_EastBoundary_Text, MSGBOX_SIGN
    end
Ecruteak_EastBoundary_Text:
    .string "EASTERN DEVELOPMENT BOUNDARY\pROUTE 42 is not open in this build.\nThe road west remains open.$"

Ecruteak_SouthBoundary::
    msgbox Ecruteak_SouthBoundary_Text, MSGBOX_SIGN
    end
Ecruteak_SouthBoundary_Text:
    .string "SOUTHERN DEVELOPMENT BOUNDARY\pROUTE 37 is not open in this build.\nThe road west remains open.$"

Ecruteak_Directory::
    msgbox Ecruteak_Directory_Text, MSGBOX_SIGN
    end
Ecruteak_Directory_Text:
    .string "ECRUTEAK CITY\pNorth: Tower entrances.\nSouthwest: GYM lobby.\pSouth: CENTER and MART.\nWest: ROUTE 38 to OLIVINE.$"

