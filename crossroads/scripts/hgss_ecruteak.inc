@ HGSS reconstruction: ordinary wayfinding only. No flags, gifts or battles.
Hgss_TempleCaretaker::
    msgbox Hgss_TempleText, MSGBOX_NPC
    end
Hgss_TempleText:
    .string "Please keep the steps clear.\nThe corridor leads to BELLCHIME TRAIL.$"
Hgss_PrivateResidence::
    msgbox Hgss_PrivateResidenceText, MSGBOX_SIGN
    end
Hgss_PrivateResidenceText:
    .string "Private residence.\nThe door is locked.$"
Hgss_GymLamp::
    msgbox Hgss_GymLampText, MSGBOX_NPC
    end
Hgss_GymLampText:
    .string "The lamp lights the narrow bridge.$"
Hgss_GymReturn::
    lockall
    playse SE_FALL
    delay 20
    warp MAP_ECRUTEAK_CITY_GYM, 10, 20
    waitstate
    releaseall
    end
Hgss_CommunicationDesk::
    msgbox Hgss_CommunicationText, MSGBOX_NPC
    end
Hgss_CommunicationText:
    .string "Communication services are\ncurrently offline.$"
Hgss_HouseResident::
    msgbox Hgss_HouseText, MSGBOX_NPC
    end
Hgss_HouseText:
    .string "The streets get quiet after dark.\nYou can hear the tower from here.$"
Hgss_HouseChild::
    msgbox Hgss_ChildText, MSGBOX_NPC
    end
Hgss_ChildText:
    .string "I like watching the dancers.\nThey always finish together.$"
Hgss_BellTrailSign::
    msgbox Hgss_BellTrailText, MSGBOX_SIGN
    end
Hgss_BellTrailText:
    .string "BELL TOWER\nReturn west through BELLCHIME TRAIL.$"
