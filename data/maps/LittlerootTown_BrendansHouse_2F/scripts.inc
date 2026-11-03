LittlerootTown_BrendansHouse_2F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LittlerootTown_BrendansHouse_2F_OnTransition
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, LittlerootTown_BrendansHouse_2F_OnWarp
	.byte 0

LittlerootTown_BrendansHouse_2F_OnTransition:
	call_if_lt VAR_LITTLEROOT_RIVAL_STATE, 2, LittlerootTown_BrendansHouse_2F_EventScript_CheckSetReadyToMeetBrendan
	call_if_ge VAR_LITTLEROOT_RIVAL_STATE, 3, LittlerootTown_BrendansHouse_2F_EventScript_CheckShouldUpdateBrendanPos
	call_if_eq VAR_LITTLEROOT_INTRO_STATE, 4, PlayersHouse_2F_EventScript_BlockStairsUntilClockIsSet
	call SecretBase_EventScript_SetDecorationFlags
	setvar VAR_SECRET_BASE_INITIALIZED, 0
	end

LittlerootTown_BrendansHouse_2F_EventScript_CheckShouldUpdateBrendanPos::
	goto_if_set FLAG_MET_RIVAL_LILYCOVE, LittlerootTown_BrendansHouse_2F_EventScript_TryUpdateBrendanPos
	goto_if_ge VAR_BIRCH_LAB_STATE, 2, LittlerootTown_BrendansHouse_2F_EventScript_Ret
	goto LittlerootTown_BrendansHouse_2F_EventScript_TryUpdateBrendanPos

LittlerootTown_BrendansHouse_2F_EventScript_TryUpdateBrendanPos::
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, LittlerootTown_BrendansHouse_2F_EventScript_Ret
	@ Odd that the MaysHouse equivalent was used below instead
	goto_if_ge VAR_DEX_UPGRADE_JOHTO_STARTER_STATE, 2, LittlerootTown_MaysHouse_2F_EventScript_Ret
	setobjectxyperm LOCALID_RIVALS_HOUSE_2F_RIVAL, 0, 2
	setobjectmovementtype LOCALID_RIVALS_HOUSE_2F_RIVAL, MOVEMENT_TYPE_FACE_UP
	return

LittlerootTown_BrendansHouse_2F_EventScript_Ret::
	return

LittlerootTown_BrendansHouse_2F_EventScript_CheckSetReadyToMeetBrendan::
	checkplayergender
	goto_if_eq VAR_RESULT, FEMALE, LittlerootTown_BrendansHouse_2F_EventScript_SetReadyToMeetBrendan
	return

LittlerootTown_BrendansHouse_2F_EventScript_SetReadyToMeetBrendan::
	setvar VAR_LITTLEROOT_RIVAL_STATE, 2
	return

LittlerootTown_BrendansHouse_2F_OnWarp:
	map_script_2 VAR_SECRET_BASE_INITIALIZED, 0, LittlerootTown_BrendansHouse_2F_EventScript_CheckInitDecor
	.2byte 0

LittlerootTown_BrendansHouse_2F_EventScript_CheckInitDecor::
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, SecretBase_EventScript_InitDecorations
	end

LittlerootTown_BrendansHouse_2F_EventScript_RivalsPokeBall::
	lockall
	goto_if_eq VAR_LITTLEROOT_RIVAL_STATE, 2, LittlerootTown_BrendansHouse_2F_EventScript_MeetBrendan
	msgbox RivalsHouse_2F_Text_ItsRivalsPokeBall, MSGBOX_DEFAULT
	releaseall
	end

LittlerootTown_BrendansHouse_2F_EventScript_MeetBrendan::
	delay 10
	addobject LOCALID_RIVALS_HOUSE_2F_RIVAL
	applymovement LOCALID_RIVALS_HOUSE_2F_RIVAL, LittlerootTown_BrendansHouse_2F_Movement_BrendanEnters
	waitmovement 0
	playse SE_PIN
	applymovement LOCALID_RIVALS_HOUSE_2F_RIVAL, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement LOCALID_RIVALS_HOUSE_2F_RIVAL, Common_Movement_Delay48
	waitmovement 0
	delay 10
	playbgm MUS_ENCOUNTER_BRENDAN, TRUE
	call_if_eq VAR_FACING, DIR_NORTH, LittlerootTown_BrendansHouse_2F_EventScript_MeetBrendanNorth
	call_if_eq VAR_FACING, DIR_SOUTH, LittlerootTown_BrendansHouse_2F_EventScript_MeetBrendanSouth
	call_if_eq VAR_FACING, DIR_WEST, LittlerootTown_BrendansHouse_2F_EventScript_MeetBrendanWest
	call_if_eq VAR_FACING, DIR_EAST, LittlerootTown_BrendansHouse_2F_EventScript_MeetBrendanEast
	setvar VAR_LITTLEROOT_RIVAL_STATE, 3
	setflag FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F_POKE_BALL
	clearflag FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_RIVAL_BEDROOM
	setvar VAR_LITTLEROOT_TOWN_STATE, 1
	savebgm MUS_DUMMY
	fadedefaultbgm
	releaseall
	end

LittlerootTown_BrendansHouse_2F_EventScript_MeetBrendanNorth::
	applymovement LOCALID_RIVALS_HOUSE_2F_RIVAL, LittlerootTown_BrendansHouse_2F_Movement_BrendanApproachPlayerNorth
	waitmovement 0
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	msgbox RivalsHouse_2F_Text_BrendanWhoAreYou, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, LittlerootTown_BrendansHouse_2F_Movement_PlayerWatchBrendanNorth
	applymovement LOCALID_RIVALS_HOUSE_2F_RIVAL, LittlerootTown_BrendansHouse_2F_Movement_BrendanWalkToPCNorth
	waitmovement 0
	return

LittlerootTown_BrendansHouse_2F_EventScript_MeetBrendanSouth::
	applymovement LOCALID_RIVALS_HOUSE_2F_RIVAL, LittlerootTown_BrendansHouse_2F_Movement_BrendanApproachPlayerSouth
	waitmovement 0
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	msgbox RivalsHouse_2F_Text_BrendanWhoAreYou, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, LittlerootTown_BrendansHouse_2F_Movement_PlayerWatchBrendanSouth
	applymovement LOCALID_RIVALS_HOUSE_2F_RIVAL, LittlerootTown_BrendansHouse_2F_Movement_BrendanWalkToPCSouth
	waitmovement 0
	return

LittlerootTown_BrendansHouse_2F_EventScript_MeetBrendanWest::
	applymovement LOCALID_RIVALS_HOUSE_2F_RIVAL, LittlerootTown_BrendansHouse_2F_Movement_BrendanApproachPlayerWest
	waitmovement 0
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
	waitmovement 0
	msgbox RivalsHouse_2F_Text_BrendanWhoAreYou, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, LittlerootTown_BrendansHouse_2F_Movement_PlayerWatchBrendanWest
	applymovement LOCALID_RIVALS_HOUSE_2F_RIVAL, LittlerootTown_BrendansHouse_2F_Movement_BrendanWalkToPCWest
	waitmovement 0
	return

LittlerootTown_BrendansHouse_2F_EventScript_MeetBrendanEast::
	applymovement LOCALID_RIVALS_HOUSE_2F_RIVAL, LittlerootTown_BrendansHouse_2F_Movement_BrendanApproachPlayerEast
	waitmovement 0
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	msgbox RivalsHouse_2F_Text_BrendanWhoAreYou, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_RIVALS_HOUSE_2F_RIVAL, LittlerootTown_BrendansHouse_2F_Movement_BrendanWalkToPCEast
	waitmovement 0
	return

LittlerootTown_BrendansHouse_2F_Movement_BrendanEnters:
	walk_down
	walk_down
	walk_in_place_faster_left
	step_end

LittlerootTown_BrendansHouse_2F_Movement_BrendanApproachPlayerNorth:
	walk_left
	walk_left
	walk_down
	walk_down
	walk_left
	step_end

LittlerootTown_BrendansHouse_2F_Movement_BrendanWalkToPCNorth:
	walk_up
	walk_up
	walk_up
	walk_left
	walk_left
	walk_left
	walk_left
	walk_in_place_faster_up
	step_end

LittlerootTown_BrendansHouse_2F_Movement_PlayerWatchBrendanNorth:
	delay_16
	walk_in_place_faster_up
	delay_16
	delay_16
	delay_16
	delay_16
	walk_in_place_faster_left
	step_end

LittlerootTown_BrendansHouse_2F_Movement_BrendanApproachPlayerSouth:
	walk_left
	walk_left
	walk_left
	step_end

LittlerootTown_BrendansHouse_2F_Movement_BrendanWalkToPCSouth:
	walk_up
	walk_left
	walk_left
	walk_left
	walk_left
	walk_in_place_faster_up
	step_end

LittlerootTown_BrendansHouse_2F_Movement_PlayerWatchBrendanSouth:
	delay_16
	walk_in_place_faster_up
	delay_16
	delay_16
	walk_in_place_faster_left
	step_end

LittlerootTown_BrendansHouse_2F_Movement_BrendanApproachPlayerWest:
	walk_left
	walk_left
	walk_down
	walk_in_place_faster_left
	step_end

LittlerootTown_BrendansHouse_2F_Movement_BrendanWalkToPCWest:
	walk_up
	walk_up
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_in_place_faster_up
	step_end

LittlerootTown_BrendansHouse_2F_Movement_PlayerWatchBrendanWest:
	delay_8
	delay_16
	walk_in_place_faster_up
	delay_16
	delay_16
	walk_in_place_faster_left
	step_end

LittlerootTown_BrendansHouse_2F_Movement_BrendanApproachPlayerEast:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_in_place_faster_down
	step_end

LittlerootTown_BrendansHouse_2F_Movement_BrendanWalkToPCEast:
	walk_up
	walk_left
	walk_left
	walk_in_place_faster_up
	step_end

@ Unused, the player is already facing this direction so its unneeded
LittlerootTown_BrendansHouse_2F_Movement_PlayerWatchBrendanEast:
	delay_16
	delay_16
	walk_in_place_faster_left
	step_end

LittlerootTown_BrendansHouse_2F_EventScript_PC::
	lockall
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, LittlerootTown_BrendansHouse_2F_EventScript_CheckPlayersPC
	goto_if_eq VAR_RESULT, FEMALE, LittlerootTown_BrendansHouse_2F_EventScript_CheckRivalsPC
	end

LittlerootTown_BrendansHouse_2F_EventScript_CheckPlayersPC::
	setvar VAR_0x8004, PC_LOCATION_BRENDANS_HOUSE
	special DoPCTurnOnEffect
	playse SE_PC_ON
	msgbox gText_PlayerHouseBootPC, MSGBOX_DEFAULT
	special BedroomPC
	releaseall
	end

LittlerootTown_BrendansHouse_2F_EventScript_TurnOffPlayerPC::
	setvar VAR_0x8004, PC_LOCATION_BRENDANS_HOUSE
	playse SE_PC_OFF
	special DoPCTurnOffEffect
	releaseall
	end

LittlerootTown_BrendansHouse_2F_EventScript_CheckRivalsPC::
	msgbox gText_PokemonTrainerSchoolEmail, MSGBOX_DEFAULT
	releaseall
	end

PlayersHouse_2F_EventScript_Notebook::
	msgbox PlayersHouse_2F_Text_Notebook, MSGBOX_SIGN
	end

PlayersHouse_2F_EventScript_GameCube::
	msgbox PlayersHouse_2F_Text_ItsAGameCube, MSGBOX_SIGN
	end

PlayersHouse_2F_Text_ClockIsStopped:
	.string "The clock is stopped…\p"
	.string "Better set it and start it!$"

PlayersHouse_2F_Text_HowDoYouLikeYourRoom:
	.string "MOM: {PLAYER}, how do you like your\n"
	.string "new room?\p"
	.string "Good! Everything's put away neatly!\p"
	.string "They finished moving everything in\n"
	.string "downstairs, too.\p"
	.string "POKéMON movers are so convenient!\p"
	.string "Oh, you should make sure that\n"
	.string "everything's all there on your desk.$"

PlayersHouse_2F_Text_Notebook:
	.string "{PLAYER} flipped open the notebook.\p"
	.string "ADVENTURE RULE NO. 1\n"
	.string "Open the MENU with START.\p"
	.string "ADVENTURE RULE NO. 2\n"
	.string "Record your progress with SAVE.\p"
	.string "The remaining pages are blank…$"

Common_Text_LookCloserAtMap:
	.string "{PLAYER} took a closer look at the\n"
	.string "{REGION} region map.$"

PlayersHouse_2F_Text_ItsAGameCube:
	.string "It's a Nintendo GameCube.\p"
	.string "A Game Boy Advance is connected to\n"
	.string "serve as the Controller.$"


@ Project Crossroads alpha test: starter interaction on bedroom desk.
Crossroads_EventScript_ChooseStarter::
    lockall
    goto_if_ne VAR_CROSSROADS_STARTER, 0, Crossroads_EventScript_AlreadyChosen
    msgbox Crossroads_Text_Containment, MSGBOX_DEFAULT
Crossroads_EventScript_AskElgyem::
    msgbox Crossroads_Text_AskElgyem, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, YES, Crossroads_EventScript_Elgyem
Crossroads_EventScript_AskSeedot::
    msgbox Crossroads_Text_AskSeedot, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, YES, Crossroads_EventScript_Seedot
Crossroads_EventScript_AskTrubbish::
    msgbox Crossroads_Text_AskTrubbish, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, YES, Crossroads_EventScript_Trubbish
    msgbox Crossroads_Text_NoChoice, MSGBOX_DEFAULT
    goto Crossroads_EventScript_Finish

Crossroads_EventScript_Elgyem::
    givemon SPECIES_ELGYEM, 5, ITEM_NONE
    goto_if_eq VAR_RESULT, MON_CANT_GIVE, Crossroads_EventScript_NoRoom
    setvar VAR_CROSSROADS_STARTER, 1
    msgbox Crossroads_Text_Elgyem, MSGBOX_DEFAULT
    goto Crossroads_EventScript_Finish

Crossroads_EventScript_Seedot::
    givemon SPECIES_SEEDOT, 5, ITEM_NONE
    goto_if_eq VAR_RESULT, MON_CANT_GIVE, Crossroads_EventScript_NoRoom
    setvar VAR_CROSSROADS_STARTER, 2
    msgbox Crossroads_Text_Seedot, MSGBOX_DEFAULT
    goto Crossroads_EventScript_Finish

Crossroads_EventScript_Trubbish::
    givemon SPECIES_TRUBBISH, 5, ITEM_NONE
    goto_if_eq VAR_RESULT, MON_CANT_GIVE, Crossroads_EventScript_NoRoom
    setvar VAR_CROSSROADS_STARTER, 3
    msgbox Crossroads_Text_Trubbish, MSGBOX_DEFAULT
    goto Crossroads_EventScript_Finish

Crossroads_EventScript_NoRoom::
    msgbox Crossroads_Text_NoRoom, MSGBOX_DEFAULT
    goto Crossroads_EventScript_Finish

Crossroads_EventScript_AlreadyChosen::
    msgbox Crossroads_Text_AlreadyChosen, MSGBOX_DEFAULT

Crossroads_EventScript_Finish::
    releaseall
    end

Crossroads_Text_Containment:
    .string "Three POKeMON are trapped!\p"
    .string "JOE: I can't leave them here!$"

Crossroads_Text_AskElgyem:
    .string "Rescue ELGYEM?$"

Crossroads_Text_AskSeedot:
    .string "Rescue SEEDOT?$"

Crossroads_Text_AskTrubbish:
    .string "Rescue TRUBBISH?$"

Crossroads_Text_NoChoice:
    .string "JOE: I need to choose one.\nBut which one?$"

Crossroads_Text_Elgyem:
    .string "JOE: What are you doing here?\nYou're coming with me.$"

Crossroads_Text_Seedot:
    .string "JOE: Easy, little guy.\nWe're getting out of here.$"

Crossroads_Text_Trubbish:
    .string "JOE: You too, huh?\nNobody wanted either of us.$"

Crossroads_Text_NoRoom:
    .string "There's no room for another\nPOKeMON!$"

Crossroads_Text_AlreadyChosen:
    .string "JOE: We already have a partner.\nTime to get moving.$"


@ Crossroads alpha: the GameCube doubles as Joe's Silph work terminal.
@ This is a dialogue-only Olivine prologue preview, not the finished Johto map.
Crossroads_EventScript_SilphTerminal::
    lockall
    goto_if_ne VAR_CROSSROADS_STARTER, 0, Crossroads_EventScript_SilphTerminalAfterRescue
    msgbox Crossroads_Text_OfficeMorning, MSGBOX_DEFAULT
    msgbox Crossroads_Text_OfficeAlarm, MSGBOX_DEFAULT
    msgbox Crossroads_Text_MaraCase, MSGBOX_DEFAULT
    releaseall
    end

Crossroads_EventScript_SilphTerminalAfterRescue::
    msgbox Crossroads_Text_OfficeAfterRescue, MSGBOX_DEFAULT
    msgbox Crossroads_Text_OlivineHarbor, MSGBOX_DEFAULT
    msgbox Crossroads_Text_MeridianExtraction, MSGBOX_DEFAULT
    msgbox Crossroads_Text_MeridianSafehouse, MSGBOX_DEFAULT
    releaseall
    end

Crossroads_Text_OfficeMorning:
    .string "OLIVINE SILPH - 6:45 AM\p"
    .string "SUPERVISOR: Your time-off\nrequest was denied.\p"
    .string "JOE: Of course it was.$"

Crossroads_Text_OfficeAlarm:
    .string "INTERCOM: Security alert!\nRemain at your stations!\p"
    .string "JOE: Eleven years here...\nWhat now?$"

Crossroads_Text_MaraCase:
    .string "MARA: Hold this case.\p"
    .string "JOE: What is it?\p"
    .string "MARA: Don't open it.\p"
    .string "SECURITY: Drop the case!\p"
    .string "JOE: I WORK HERE!$"

Crossroads_Text_OfficeAfterRescue:
    .string "SILPH SECURITY BULLETIN\p"
    .string "JOSEPH MERCER - WANTED\nFOR QUESTIONING.\p"
    .string "JOE: I just wanted a day off.$"

@ Project Crossroads: Olivine harbor escape story slice (temporary terminal preview).
Crossroads_Text_OlivineHarbor:
    .string "OLIVINE CITY - HARBOR ROAD\\p"
    .string "Cargo cranes loom over the\\nwater. Sirens echo behind Joe.\\p"
    .string "JOE: I move freight for a living.\\nI do not steal it!$"

Crossroads_Text_MeridianExtraction:
    .string "MARA: You want to explain\\nthe case, or get in the truck?\\p"
    .string "JOE: I want my day off!\\p"
    .string "MARA: Then get in.$"

Crossroads_Text_MeridianSafehouse:
    .string "MERIDIAN SAFEHOUSE\\p"
    .string "VALE: Exceptional work, Mercer.\\p"
    .string "JOE: You have the wrong guy.\\p"
    .string "VALE: So everyone keeps saying.$"
