@ Existing-area completion: no badges, new regions, legends or story gates.
Area_LighthouseKeeper::
    msgbox Area_LighthouseKeeper_Text, MSGBOX_NPC
    end
Area_LighthouseKeeper_Text:
    .string "Keep the stairs clear. The upper\nfloors lead to the lantern room.$"

Area_BellCaretaker::
    msgbox Area_BellCaretaker_Text, MSGBOX_NPC
    end
Area_BellCaretaker_Text:
    .string "The stairs lead up through the tower.\nPlease treat this place with care.$"

Area_TowerVisitor::
    msgbox Area_TowerVisitor_Text, MSGBOX_NPC
    end
Area_TowerVisitor_Text:
    .string "It is a good place to slow down\nand look at the world below.$"

Area_LighthouseView::
    msgbox Area_LighthouseView_Text, MSGBOX_NPC
    end
Area_LighthouseView_Text:
    .string "OLIVINE spreads out below.\pFreight ships edge into the harbor.\nThe beacon stays steady above them.$"

Area_BurnedCaretaker::
    msgbox Area_BurnedCaretaker_Text, MSGBOX_NPC
    end
Area_BurnedCaretaker_Text:
    .string "Watch your footing downstairs.\nThe old beams are still fragile.$"

Area_BurnedVisitor::
    msgbox Area_BurnedVisitor_Text, MSGBOX_NPC
    end
Area_BurnedVisitor_Text:
    .string "There is more here than broken wood.\nPlease leave everything as it is.$"

Area_BurnedMemorial::
    msgbox Area_BurnedMemorial_Text, MSGBOX_NPC
    end
Area_BurnedMemorial_Text:
    .string "A quiet corner beneath the tower.\nThe fallen timbers remain undisturbed.$"

Area_GymGuide::
    msgbox Area_GymGuide_Text, MSGBOX_NPC
    end
Area_GymGuide_Text:
    .string "The practice hall is upstairs.\pPractice battles are optional.\nNo badges are awarded here.$"

Area_BarnKeeper::
    msgbox Area_BarnKeeper_Text, MSGBOX_NPC
    end
Area_BarnKeeper_Text:
    .string "The barn is quieter than the docks.\nFresh milk is sold at the farmhouse.$"

Area_FarmSign::
    msgbox Area_FarmSign_Text, MSGBOX_NPC
    end
Area_FarmSign_Text:
    .string "MOOMOO FARM\nMilk at the farmhouse. Barn below.$"

Area_OlivineNeighbor::
    msgbox Area_OlivineNeighbor_Text, MSGBOX_NPC
    end
Area_OlivineNeighbor_Text:
    .string "Ships keep their own schedules.\nI prefer a quiet evening at home.$"

Area_EcruteakNeighbor::
    msgbox Area_EcruteakNeighbor_Text, MSGBOX_NPC
    end
Area_EcruteakNeighbor_Text:
    .string "The theater is nearby, and both\ntowers are open to visitors.$"

Area_Dancer::
    msgbox Area_Dancer_Text, MSGBOX_NPC
    end
Area_Dancer_Text:
    .string "A steady step matters more than\na hurried one.$"

Area_RingBell::
    lockall
    playse SE_M_HEAL_BELL
    waitse
    msgbox Area_BellText, MSGBOX_DEFAULT
    releaseall
    end
Area_BellText:
    .string "The bell rings out over ECRUTEAK.\nFor a moment, the city seems still.$"

Area_Miltank::
    lock
    faceplayer
    playmoncry SPECIES_MILTANK, CRY_MODE_NORMAL
    waitmoncry
    msgbox Area_MiltankText, MSGBOX_DEFAULT
    release
    end
Area_MiltankText:
    .string "MILTANK: Mooo!$"

Area_MilkShop::
    lock
    faceplayer
    msgbox Area_MilkText, MSGBOX_DEFAULT
    pokemart Area_MilkStock
    msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
    release
    end
Area_MilkText:
    .string "Fresh milk for the road?\nHave a look.$"
    .align 2
Area_MilkStock:
    .2byte ITEM_MOOMOO_MILK
    .2byte ITEM_POTION
    pokemartlistend

Area_TheaterHost::
    lockall
    msgbox Area_PerformancePrompt, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Area_PerformanceEnd
    playbgm MUS_CONTEST_LOBBY, 0
    applymovement LOCALID_AREA_DANCER_1, Area_DanceLeft
    applymovement LOCALID_AREA_DANCER_2, Area_DanceLeft
    applymovement LOCALID_AREA_DANCER_3, Area_DanceLeft
    waitmovement 0
    applymovement LOCALID_AREA_DANCER_1, Area_DanceRight
    applymovement LOCALID_AREA_DANCER_2, Area_DanceRight
    applymovement LOCALID_AREA_DANCER_3, Area_DanceRight
    waitmovement 0
    applymovement LOCALID_AREA_DANCER_1, Area_DanceBow
    applymovement LOCALID_AREA_DANCER_2, Area_DanceBow
    applymovement LOCALID_AREA_DANCER_3, Area_DanceBow
    waitmovement 0
    playbgm MUS_LILYCOVE, 0
    msgbox Area_PerformanceDone, MSGBOX_DEFAULT
Area_PerformanceEnd:
    releaseall
    end
Area_PerformancePrompt:
    .string "Watch a short performance?$"
Area_PerformanceDone:
    .string "The dancers finish together.\nThe room settles into quiet again.$"
Area_DanceLeft:
    walk_left
    delay_16
    face_down
    step_end
Area_DanceRight:
    walk_right
    delay_16
    face_down
    step_end
Area_DanceBow:
    jump_in_place_down
    delay_16
    face_down
    step_end

Area_NoParty:
    msgbox Area_NoPartyText, MSGBOX_DEFAULT
    release
    end
Area_NoPartyText:
    .string "Bring a POKEMON partner first.\nWe can practice when you are ready.$"

Area_PracticeJasmine::
    lock
    getpartysize
    goto_if_eq VAR_RESULT, 0, Area_NoParty
    msgbox Area_PracticeJasminePrompt, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Area_BattleEnd
    cleartrainerflag TRAINER_CROSSROADS_JASMINE
    trainerbattle_single TRAINER_CROSSROADS_JASMINE, Area_PracticeJasmineIntro, Area_PracticeJasmineLose, Area_BattleDone
    goto Area_BattleDone
Area_PracticeJasminePrompt:
    .string "Jasmine: Ready for a\npractice battle?$"
Area_PracticeJasmineIntro:
    .string "Let us see how your team works!$"
Area_PracticeJasmineLose:
    .string "That was good practice!$"

Area_PracticeMorty::
    lock
    getpartysize
    goto_if_eq VAR_RESULT, 0, Area_NoParty
    msgbox Area_PracticeMortyPrompt, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Area_BattleEnd
    cleartrainerflag TRAINER_CROSSROADS_MORTY
    trainerbattle_single TRAINER_CROSSROADS_MORTY, Area_PracticeMortyIntro, Area_PracticeMortyLose, Area_BattleDone
    goto Area_BattleDone
Area_PracticeMortyPrompt:
    .string "Morty: Ready for a\npractice battle?$"
Area_PracticeMortyIntro:
    .string "Let us see how your team works!$"
Area_PracticeMortyLose:
    .string "That was good practice!$"

Area_JasmineApprentice::
    lock
    getpartysize
    goto_if_eq VAR_RESULT, 0, Area_NoParty
    msgbox Area_JasmineApprenticePrompt, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Area_BattleEnd
    cleartrainerflag TRAINER_CROSSROADS_STEEL_STUDENT
    trainerbattle_single TRAINER_CROSSROADS_STEEL_STUDENT, Area_JasmineApprenticeIntro, Area_JasmineApprenticeLose, Area_BattleDone
    goto Area_BattleDone
Area_JasmineApprenticePrompt:
    .string "Steel student: Ready for a\npractice battle?$"
Area_JasmineApprenticeIntro:
    .string "Let us see how your team works!$"
Area_JasmineApprenticeLose:
    .string "That was good practice!$"

Area_MortyApprentice::
    lock
    getpartysize
    goto_if_eq VAR_RESULT, 0, Area_NoParty
    msgbox Area_MortyApprenticePrompt, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Area_BattleEnd
    cleartrainerflag TRAINER_CROSSROADS_GHOST_STUDENT
    trainerbattle_single TRAINER_CROSSROADS_GHOST_STUDENT, Area_MortyApprenticeIntro, Area_MortyApprenticeLose, Area_BattleDone
    goto Area_BattleDone
Area_MortyApprenticePrompt:
    .string "Ghost student: Ready for a\npractice battle?$"
Area_MortyApprenticeIntro:
    .string "Let us see how your team works!$"
Area_MortyApprenticeLose:
    .string "That was good practice!$"

Area_Route39Trainer::
    lock
    getpartysize
    goto_if_eq VAR_RESULT, 0, Area_NoParty
    msgbox Area_Route39TrainerPrompt, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Area_BattleEnd
    cleartrainerflag TRAINER_CROSSROADS_FARMHAND
    trainerbattle_single TRAINER_CROSSROADS_FARMHAND, Area_Route39TrainerIntro, Area_Route39TrainerLose, Area_BattleDone
    goto Area_BattleDone
Area_Route39TrainerPrompt:
    .string "Farmhand: Ready for a\npractice battle?$"
Area_Route39TrainerIntro:
    .string "Let us see how your team works!$"
Area_Route39TrainerLose:
    .string "That was good practice!$"

Area_Route38Trainer::
    lock
    getpartysize
    goto_if_eq VAR_RESULT, 0, Area_NoParty
    msgbox Area_Route38TrainerPrompt, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Area_BattleEnd
    cleartrainerflag TRAINER_CROSSROADS_BIRDWATCHER
    trainerbattle_single TRAINER_CROSSROADS_BIRDWATCHER, Area_Route38TrainerIntro, Area_Route38TrainerLose, Area_BattleDone
    goto Area_BattleDone
Area_Route38TrainerPrompt:
    .string "Birdwatcher: Ready for a\npractice battle?$"
Area_Route38TrainerIntro:
    .string "Let us see how your team works!$"
Area_Route38TrainerLose:
    .string "That was good practice!$"

Area_BattleDone:
    msgbox Area_BattleDoneText, MSGBOX_DEFAULT
Area_BattleEnd:
    release
    end
Area_BattleDoneText:
    .string "Come back whenever you want\nanother practice battle.$"

Area_Floor_OlivineCity_Lighthouse_1F::
    msgbox Area_Floor_OlivineCity_Lighthouse_1FText, MSGBOX_SIGN
    end
Area_Floor_OlivineCity_Lighthouse_1FText:
    .string "OLIVINE LIGHTHOUSE - 1F\pKeep the stairway clear.$"

Area_Floor_OlivineCity_Lighthouse_2F::
    msgbox Area_Floor_OlivineCity_Lighthouse_2FText, MSGBOX_SIGN
    end
Area_Floor_OlivineCity_Lighthouse_2FText:
    .string "OLIVINE LIGHTHOUSE - 2F\pThe handrail is worn smooth.$"

Area_Floor_OlivineCity_Lighthouse_3F::
    msgbox Area_Floor_OlivineCity_Lighthouse_3FText, MSGBOX_SIGN
    end
Area_Floor_OlivineCity_Lighthouse_3FText:
    .string "OLIVINE LIGHTHOUSE - 3F\pA breeze moves through the landing.$"

Area_Floor_OlivineCity_Lighthouse_4F::
    msgbox Area_Floor_OlivineCity_Lighthouse_4FText, MSGBOX_SIGN
    end
Area_Floor_OlivineCity_Lighthouse_4FText:
    .string "OLIVINE LIGHTHOUSE - 4F\pThe floorboards creak softly.$"

Area_Floor_OlivineCity_Lighthouse_5F::
    msgbox Area_Floor_OlivineCity_Lighthouse_5FText, MSGBOX_SIGN
    end
Area_Floor_OlivineCity_Lighthouse_5FText:
    .string "OLIVINE LIGHTHOUSE - 5F\pLight reaches through the windows.$"

Area_Floor_OlivineCity_Lighthouse_6F::
    msgbox Area_Floor_OlivineCity_Lighthouse_6FText, MSGBOX_SIGN
    end
Area_Floor_OlivineCity_Lighthouse_6FText:
    .string "OLIVINE LIGHTHOUSE - 6F\pYou can hear the city below.$"

Area_Floor_EcruteakCity_BellTower::
    msgbox Area_Floor_EcruteakCity_BellTowerText, MSGBOX_SIGN
    end
Area_Floor_EcruteakCity_BellTowerText:
    .string "BELL TOWER - 1F\pKeep the stairway clear.$"

Area_Floor_EcruteakCity_BellTower_2F::
    msgbox Area_Floor_EcruteakCity_BellTower_2FText, MSGBOX_SIGN
    end
Area_Floor_EcruteakCity_BellTower_2FText:
    .string "BELL TOWER - 2F\pThe handrail is worn smooth.$"

Area_Floor_EcruteakCity_BellTower_3F::
    msgbox Area_Floor_EcruteakCity_BellTower_3FText, MSGBOX_SIGN
    end
Area_Floor_EcruteakCity_BellTower_3FText:
    .string "BELL TOWER - 3F\pA breeze moves through the landing.$"

Area_Floor_EcruteakCity_BellTower_4F::
    msgbox Area_Floor_EcruteakCity_BellTower_4FText, MSGBOX_SIGN
    end
Area_Floor_EcruteakCity_BellTower_4FText:
    .string "BELL TOWER - 4F\pThe floorboards creak softly.$"

Area_Floor_EcruteakCity_BellTower_5F::
    msgbox Area_Floor_EcruteakCity_BellTower_5FText, MSGBOX_SIGN
    end
Area_Floor_EcruteakCity_BellTower_5FText:
    .string "BELL TOWER - 5F\pLight reaches through the windows.$"

Area_Floor_EcruteakCity_BellTower_6F::
    msgbox Area_Floor_EcruteakCity_BellTower_6FText, MSGBOX_SIGN
    end
Area_Floor_EcruteakCity_BellTower_6FText:
    .string "BELL TOWER - 6F\pYou can hear the city below.$"

Area_Floor_EcruteakCity_BellTower_7F::
    msgbox Area_Floor_EcruteakCity_BellTower_7FText, MSGBOX_SIGN
    end
Area_Floor_EcruteakCity_BellTower_7FText:
    .string "BELL TOWER - 7F\pA quiet place above the rooftops.$"

Area_Floor_EcruteakCity_BellTower_8F::
    msgbox Area_Floor_EcruteakCity_BellTower_8FText, MSGBOX_SIGN
    end
Area_Floor_EcruteakCity_BellTower_8FText:
    .string "BELL TOWER - 8F\pThe stairs climb toward the bell.$"

Area_Floor_EcruteakCity_BellTower_9F::
    msgbox Area_Floor_EcruteakCity_BellTower_9FText, MSGBOX_SIGN
    end
Area_Floor_EcruteakCity_BellTower_9FText:
    .string "BELL TOWER - 9F\pThe bell waits above ECRUTEAK.$"
