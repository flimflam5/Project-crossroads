RuinsOfAlph_NorthwestChamber_MapScripts::
    .byte 0
RuinsOfAlph_NorthwestChamber_Puzzle::
    lockall
    fadescreen FADE_TO_BLACK
    setvar VAR_0x8004, 3
    setvar VAR_0x8005, FALSE
    special DoSlidingPuzzle
    goto_if_eq VAR_RESULT, TRUE, RuinsOfAlph_NorthwestChamber_Puzzle_Success
    releaseall
    end
RuinsOfAlph_NorthwestChamber_Puzzle_Success::
    warp MAP_RUINS_OF_ALPH_UNDERGROUND_HALL, 5, 24
    waitstate
    releaseall
    end

RuinsOfAlph_NorthwestChamber_HiddenGate::
    lockall
    specialvar VAR_RESULT, Crossroads_AlphHasNonEggHoOh
    goto_if_eq VAR_RESULT, FALSE, RuinsOfAlph_NorthwestChamber_HiddenGate_Closed
    setmetatile 5, 1, 40, FALSE
    special DrawWholeMapView
    releaseall
    end
RuinsOfAlph_NorthwestChamber_HiddenGate_Closed::
    msgbox RuinsOfAlph_NorthwestChamber_HiddenGate_Text, MSGBOX_SIGN
    releaseall
    end
RuinsOfAlph_NorthwestChamber_HiddenGate_Text:
    .string "HO-OH$"
