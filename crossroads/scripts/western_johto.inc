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
    .string "The GYM is in the southwest.\nPractice battles are open inside.$"

Ecruteak_TowerVisitor::
    msgbox Ecruteak_TowerVisitor_Text, MSGBOX_NPC
    end
Ecruteak_TowerVisitor_Text:
    .string "The BELL TOWER entrance is ahead.\nThe upper floors are open.$"

Ecruteak_Shopper::
    msgbox Ecruteak_Shopper_Text, MSGBOX_NPC
    end
Ecruteak_Shopper_Text:
    .string "I buy supplies before a long walk.\nIt saves a trip back.$"

Ecruteak_TheaterVisitor::
    msgbox Ecruteak_TheaterVisitor_Text, MSGBOX_NPC
    end
Ecruteak_TheaterVisitor_Text:
    .string "The DANCE THEATER is up this path.\nThere are short performances.$"

Ecruteak_BurnedGuide::
    msgbox Ecruteak_BurnedGuide_Text, MSGBOX_NPC
    end
Ecruteak_BurnedGuide_Text:
    .string "BURNED TOWER\pThe basement is open to visitors.\nPlease watch your footing.$"

Ecruteak_BellGuide::
    msgbox Ecruteak_BellGuide_Text, MSGBOX_NPC
    end
Ecruteak_BellGuide_Text:
    .string "BELL TOWER\pThe stairs lead to the upper floors.\nPlease treat the tower with care.$"

Ecruteak_Host::
    msgbox Ecruteak_Host_Text, MSGBOX_NPC
    end
Ecruteak_Host_Text:
    .string "Make yourself comfortable.\nThe port road is a long walk.$"

Ecruteak_TheaterGuide::
    msgbox Ecruteak_TheaterGuide_Text, MSGBOX_NPC
    end
Ecruteak_TheaterGuide_Text:
    .string "ECRUTEAK DANCE THEATER\pShort performances are held here.\nSpeak to the host inside.$"

Ecruteak_GymGuide::
    msgbox Ecruteak_GymGuide_Text, MSGBOX_NPC
    end
Ecruteak_GymGuide_Text:
    .string "ECRUTEAK GYM\pOptional practice battles inside.\nBadges are not awarded here.$"

Ecruteak_CenterVisitor::
    msgbox Ecruteak_CenterVisitor_Text, MSGBOX_NPC
    end
Ecruteak_CenterVisitor_Text:
    .string "A rest here makes the return\ntrip to OLIVINE much easier.$"

Ecruteak_BurnedTowerSign::
    msgbox Ecruteak_BurnedTowerSign_Text, MSGBOX_SIGN
    end
Ecruteak_BurnedTowerSign_Text:
    .string "BURNED TOWER\nOpen to visitors.$"

Ecruteak_BellTowerSign::
    msgbox Ecruteak_BellTowerSign_Text, MSGBOX_SIGN
    end
Ecruteak_BellTowerSign_Text:
    .string "BELL TOWER\nOpen to visitors.$"

Ecruteak_ResidenceSign::
    msgbox Ecruteak_ResidenceSign_Text, MSGBOX_SIGN
    end
Ecruteak_ResidenceSign_Text:
    .string "ECRUTEAK RESIDENCE$"

Ecruteak_DanceTheaterSign::
    msgbox Ecruteak_DanceTheaterSign_Text, MSGBOX_SIGN
    end
Ecruteak_DanceTheaterSign_Text:
    .string "ECRUTEAK DANCE THEATER\nPerformances inside.$"

Ecruteak_GymSign::
    msgbox Ecruteak_GymSign_Text, MSGBOX_SIGN
    end
Ecruteak_GymSign_Text:
    .string "ECRUTEAK GYM\nOptional practice battles inside.$"

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
    .string "ROUTE 42\nEast: MT. MORTAR and MAHOGANY.\pWest: The road to OLIVINE.$"

Ecruteak_SouthBoundary::
    msgbox Ecruteak_SouthBoundary_Text, MSGBOX_SIGN
    end
Ecruteak_SouthBoundary_Text:
    .string "ROUTE 37\nSouth: ROUTE 36 and the roads\pto NATIONAL PARK and GOLDENROD.$"

Ecruteak_Directory::
    msgbox Ecruteak_Directory_Text, MSGBOX_SIGN
    end
Ecruteak_Directory_Text:
    .string "ECRUTEAK CITY\pNorth: Tower entrances.\nSouthwest: GYM lobby.\pSouth: CENTER and MART.\nWest: ROUTE 38 to OLIVINE.$"

