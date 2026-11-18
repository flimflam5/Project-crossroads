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
    warp MAP_RUINS_OF_ALPH_UNDERGROUND_HALL, 5, 6
    waitstate
    releaseall
    end
