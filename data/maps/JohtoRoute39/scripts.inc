JohtoRoute39_MapScripts::
    .byte 0

Route39_SouthSign::
    msgbox Route39_Text_South, MSGBOX_SIGN
    end
Route39_Text_South:
    .string "ROUTE 39\nSouth: OLIVINE CITY$"

Route39_NorthSign::
    msgbox Route39_Text_North, MSGBOX_SIGN
    end
Route39_Text_North:
    .string "NORTHERN DEVELOPMENT BOUNDARY\p"
    .string "ROUTE 38 is not open in this build.\nReturn south to OLIVINE CITY.$"

Route39_Walker::
    lock
    faceplayer
    msgbox Route39_Text_Walker, MSGBOX_DEFAULT
    release
    end
Route39_Text_Walker:
    .string "The port gets noisy. I come out\nhere for a little quiet.$"
