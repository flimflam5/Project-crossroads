@ Ambient exploration only. No badge, reward, encounter or plot flags.
Hgss_OlivineWindowDrop::
    lockall
    playse SE_FALL
    delay 16
    warp MAP_OLIVINE_CITY_LIGHTHOUSE_BALCONY, 14, 9
    waitstate
    releaseall
    end
Hgss_OlivineLift1F::
    lockall
    msgbox Hgss_OlivineLift1FText, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Hgss_OlivineLiftCancel
    setdynamicwarp MAP_OLIVINECITY_LIGHTHOUSE_1F, 3
    playse SE_ELEVATOR
    delay 45
    msgbox Hgss_OlivineLiftArrived, MSGBOX_DEFAULT
    releaseall
    end
Hgss_OlivineLift6F::
    lockall
    msgbox Hgss_OlivineLift6FText, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Hgss_OlivineLiftCancel
    setdynamicwarp MAP_OLIVINECITY_LIGHTHOUSE_6F, 1
    playse SE_ELEVATOR
    delay 45
    msgbox Hgss_OlivineLiftArrived, MSGBOX_DEFAULT
    releaseall
    end
Hgss_OlivineLiftCancel:
    releaseall
    end
Hgss_OlivineLift1FText:
    .string "1F - VISITOR DECK\nTake the lift to the ground floor?$"
Hgss_OlivineLift6FText:
    .string "6F - LANTERN ROOM\nTake the lift to the top floor?$"
Hgss_OlivineLiftArrived:
    .string "The lift settles at the landing.$"
Hgss_OlivinePortDesk::
    msgbox Hgss_OlivinePortDeskText, MSGBOX_NPC
    end
Hgss_OlivinePortDeskText:
    .string "The quays are open to visitors.\nThe HARBOR OFFICE handles travel.$"
Hgss_OlivinePortVisitor::
    msgbox Hgss_OlivinePortVisitorText, MSGBOX_NPC
    end
Hgss_OlivinePortVisitorText:
    .string "The side passage leads back to\nthe older inspection pier.$"
Hgss_OlivineShipBoundary::
    msgbox Hgss_OlivineShipBoundaryText, MSGBOX_SIGN
    end
Hgss_OlivineShipBoundaryText:
    .string "S.S. AQUA BOARDING\nPassenger sailings are not operating.$"
