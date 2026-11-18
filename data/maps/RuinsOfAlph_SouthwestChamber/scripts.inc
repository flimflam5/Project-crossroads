RuinsOfAlph_SouthwestChamber_MapScripts::
    .byte 0
RuinsOfAlph_SouthwestChamber_Puzzle::
    lockall
    fadescreen FADE_TO_BLACK
    setvar VAR_0x8004, 1
    setvar VAR_0x8005, FALSE
    special DoSlidingPuzzle
    goto_if_eq VAR_RESULT, TRUE, RuinsOfAlph_SouthwestChamber_Puzzle_Success
    releaseall
    end
RuinsOfAlph_SouthwestChamber_Puzzle_Success::
    warp MAP_RUINS_OF_ALPH_UNDERGROUND_HALL, 5, 42
    waitstate
    releaseall
    end

RuinsOfAlph_SouthwestChamber_HiddenGate::
    msgbox RuinsOfAlph_SouthwestChamber_HiddenGate_Text, MSGBOX_SIGN
    end
RuinsOfAlph_SouthwestChamber_HiddenGate_Text:
    .string "WATER$"
RuinsOfAlph_SouthwestChamber_WaterStoneUsed::
    lockall
    setmetatile 5, 1, 40, FALSE
    special DrawWholeMapView
    releaseall
    end
