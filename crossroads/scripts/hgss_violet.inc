@ Dedicated HGSS Violet wayfinding/services. Stable labels; no new story or rewards.
Johto_VioletCity_Sign::
    msgbox Johto_VioletCity_Sign_Text, MSGBOX_SIGN
    end
Johto_VioletCity_Sign_Text:
    .string "VIOLET CITY. Follow the marked\nroads and direction signs.$"

Johto_VioletCity_Resident::
    msgbox Johto_VioletCity_Resident_Text, MSGBOX_NPC
    end
Johto_VioletCity_Resident_Text:
    .string "The monks walk so softly. The\nold tower does the creaking for\pthem.$"

Johto_VioletCity_Gym_Guide::
    msgbox Johto_VioletCity_Gym_Guide_Text, MSGBOX_NPC
    end
Johto_VioletCity_Gym_Guide_Text:
    .string "The perches leave plenty of\nroom to watch movement. Our\ptraining floor is open to\nvisitors; battles are not\pscheduled today.$"

Johto_VioletCity_Gym_Notes::
    msgbox Johto_VioletCity_Gym_Notes_Text, MSGBOX_SIGN
    end
Johto_VioletCity_Gym_Notes_Text:
    .string "Please leave the displays as\nyou found them. Take care on\pthe stairs.$"

Johto_VioletCity_Residence_Guide::
    msgbox Johto_VioletCity_Residence_Guide_Text, MSGBOX_NPC
    end
Johto_VioletCity_Residence_Guide_Text:
    .string "The monks walk so softly. The\nold tower does the creaking for\pthem.$"

Johto_VioletCity_Residence_Notes::
    msgbox Johto_VioletCity_Residence_Notes_Text, MSGBOX_SIGN
    end
Johto_VioletCity_Residence_Notes_Text:
    .string "Please leave the displays as\nyou found them. Take care on\pthe stairs.$"

Johto_VioletCity_Workshop_Guide::
    msgbox Johto_VioletCity_Workshop_Guide_Text, MSGBOX_NPC
    end
Johto_VioletCity_Workshop_Guide_Text:
    .string "The monks walk so softly. The\nold tower does the creaking for\pthem.$"

Johto_VioletCity_Workshop_Notes::
    msgbox Johto_VioletCity_Workshop_Notes_Text, MSGBOX_SIGN
    end
Johto_VioletCity_Workshop_Notes_Text:
    .string "Local maps, repair notes and a\nwell-used workbench.$"

Johto_SproutTower_1F_Guide::
    msgbox Johto_SproutTower_1F_Guide_Text, MSGBOX_NPC
    end
Johto_SproutTower_1F_Guide_Text:
    .string "The center pillar is built to\nsway. Take the outer walkway\pand keep the steps clear.$"

Johto_SproutTower_1F_Notes::
    msgbox Johto_SproutTower_1F_Notes_Text, MSGBOX_SIGN
    end
Johto_SproutTower_1F_Notes_Text:
    .string "Please leave the displays as\nyou found them. Take care on\pthe stairs.$"

Johto_SproutTower_2F_Guide::
    msgbox Johto_SproutTower_2F_Guide_Text, MSGBOX_NPC
    end
Johto_SproutTower_2F_Guide_Text:
    .string "The center pillar is built to\nsway. Take the outer walkway\pand keep the steps clear.$"

Johto_SproutTower_2F_Notes::
    msgbox Johto_SproutTower_2F_Notes_Text, MSGBOX_SIGN
    end
Johto_SproutTower_2F_Notes_Text:
    .string "Please leave the displays as\nyou found them. Take care on\pthe stairs.$"

Johto_SproutTower_3F_Guide::
    msgbox Johto_SproutTower_3F_Guide_Text, MSGBOX_NPC
    end
Johto_SproutTower_3F_Guide_Text:
    .string "The center pillar is built to\nsway. Take the outer walkway\pand keep the steps clear.$"

Johto_SproutTower_3F_Notes::
    msgbox Johto_SproutTower_3F_Notes_Text, MSGBOX_SIGN
    end
Johto_SproutTower_3F_Notes_Text:
    .string "Please leave the displays as\nyou found them. Take care on\pthe stairs.$"

Johto_VioletAcademy_Guide::
    msgbox Johto_VioletAcademy_Guide_Text, MSGBOX_NPC
    end
Johto_VioletAcademy_Guide_Text:
    .string "A status condition can matter\nas much as a strong attack.\pWatch speed, accuracy and the\ncondition of your team.$"

Johto_VioletAcademy_Notes::
    msgbox Johto_VioletAcademy_Notes_Text, MSGBOX_SIGN
    end
Johto_VioletAcademy_Notes_Text:
    .string "Please leave the displays as\nyou found them. Take care on\pthe stairs.$"

Johto_VioletCity_PokemonCenter_1F_Plaque::
    msgbox Johto_VioletCity_PokemonCenter_1F_Plaque_Text, MSGBOX_SIGN
    end
Johto_VioletCity_PokemonCenter_1F_Plaque_Text:
    .string "VIOLET CITY POKEMON CENTER.$"

Johto_VioletCity_Nurse::
    setvar VAR_0x800B, LOCALID_JOHTO_NURSE_VIOLET_CITY
    call Common_EventScript_PkmnCenterNurse
    waitmessage
    waitbuttonpress
    release
    end

Johto_VioletCity_Mart_Plaque::
    msgbox Johto_VioletCity_Mart_Plaque_Text, MSGBOX_SIGN
    end
Johto_VioletCity_Mart_Plaque_Text:
    .string "VIOLET CITY MART.$"

Johto_VioletCity_Gym_Plaque::
    msgbox Johto_VioletCity_Gym_Plaque_Text, MSGBOX_SIGN
    end
Johto_VioletCity_Gym_Plaque_Text:
    .string "VIOLET CITY GYM.$"

Johto_VioletCity_Residence_Plaque::
    msgbox Johto_VioletCity_Residence_Plaque_Text, MSGBOX_SIGN
    end
Johto_VioletCity_Residence_Plaque_Text:
    .string "VIOLET CITY\nGUEST HOUSE.$"

Johto_VioletCity_Rest::
    goto Olivine_HomeRest

Johto_VioletCity_Workshop_Plaque::
    msgbox Johto_VioletCity_Workshop_Plaque_Text, MSGBOX_SIGN
    end
Johto_VioletCity_Workshop_Plaque_Text:
    .string "VIOLET CITY\nNORTHWEST HOUSE.$"

Johto_VioletAcademy_Entrance::
    msgbox Johto_VioletAcademy_Entrance_Text, MSGBOX_SIGN
    end
Johto_VioletAcademy_Entrance_Text:
    .string "VIOLET ACADEMY.$"

Johto_SproutTower_Mouth0::
    msgbox Johto_SproutTower_Mouth0_Text, MSGBOX_SIGN
    end
Johto_SproutTower_Mouth0_Text:
    .string "SPROUT TOWER. Public walking\naccess. Please respect the\psurroundings.$"

Johto_VioletCity_Local0::
    msgbox Johto_VioletCity_Local0_Text, MSGBOX_NPC
    end
Johto_VioletCity_Local0_Text:
    .string "The Center is a good place to\nrest before taking the next\proad.$"

Johto_VioletCity_Local1::
    msgbox Johto_VioletCity_Local1_Text, MSGBOX_NPC
    end
Johto_VioletCity_Local1_Text:
    .string "Today was map reading at the\nacademy. I am taking the\ppractical part very seriously.$"

Johto_VioletCity_Local2::
    msgbox Johto_VioletCity_Local2_Text, MSGBOX_NPC
    end
Johto_VioletCity_Local2_Text:
    .string "There is no prize for arriving\ntired. Take a break when you\pneed one.$"

Johto_VioletCity_CenterOnTransition::
    setrespawn HEAL_LOCATION_VIOLET_CITY
    end


HgssViolet_Student::
    msgbox HgssViolet_Student_Text, MSGBOX_NPC
    end
HgssViolet_Student_Text:
    .string "A Pokemon can have two types.\nI keep forgetting the second one!$"
HgssViolet_WestGateGuide::
    msgbox HgssViolet_WestGate_Text, MSGBOX_NPC
    end
HgssViolet_WestGate_Text:
    .string "West: ROUTE 36.\nEast: VIOLET CITY.$"
HgssViolet_EastGateGuide::
    msgbox HgssViolet_EastGate_Text, MSGBOX_NPC
    end
HgssViolet_EastGate_Text:
    .string "West: VIOLET CITY.\nEast: ROUTE 31.$"
HgssViolet_WestEnter::
    warp MAP_VIOLET_CITY_WEST_GATE, 0
    waitstate
    end
HgssViolet_EastEnter::
    warp MAP_VIOLET_CITY_EAST_GATE, 0
    waitstate
    end
HgssViolet_WestRouteEnter::
    warp MAP_VIOLET_CITY_WEST_GATE, 1
    waitstate
    end
HgssViolet_EastRouteEnter::
    warp MAP_VIOLET_CITY_EAST_GATE, 1
    waitstate
    end
