@ Project Crossroads: Silph containment starter event (STAGED, NOT LINKED).
@ This version uses the engine's existing yes/no UI; no custom multichoice
@ constant is needed. Requires a reserved persistent VAR_CROSSROADS_STARTER.
@ Attach this script to a map object only after defining that variable.
@ 0 = unchosen, 1 = Porygon, 2 = Houndour, 3 = Trubbish.

Crossroads_EventScript_ChooseStarter::
    lockall
    goto_if_ne VAR_CROSSROADS_STARTER, 0, Crossroads_EventScript_AlreadyChosen
    msgbox Crossroads_Text_Containment, MSGBOX_DEFAULT
Crossroads_EventScript_AskPorygon::
    msgbox Crossroads_Text_AskPorygon, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, YES, Crossroads_EventScript_Porygon
Crossroads_EventScript_AskHoundour::
    msgbox Crossroads_Text_AskHoundour, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, YES, Crossroads_EventScript_Houndour
Crossroads_EventScript_AskTrubbish::
    msgbox Crossroads_Text_AskTrubbish, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, YES, Crossroads_EventScript_Trubbish
    msgbox Crossroads_Text_NoChoice, MSGBOX_DEFAULT
    goto Crossroads_EventScript_Finish

Crossroads_EventScript_Porygon::
    givepokemon SPECIES_PORYGON, 5, ITEM_NONE
    goto_if_eq VAR_RESULT, 0, Crossroads_EventScript_NoRoom
    setvar VAR_CROSSROADS_STARTER, 1
    msgbox Crossroads_Text_Porygon, MSGBOX_DEFAULT
    goto Crossroads_EventScript_Finish

Crossroads_EventScript_Houndour::
    givepokemon SPECIES_HOUNDOUR, 5, ITEM_NONE
    goto_if_eq VAR_RESULT, 0, Crossroads_EventScript_NoRoom
    setvar VAR_CROSSROADS_STARTER, 2
    msgbox Crossroads_Text_Houndour, MSGBOX_DEFAULT
    goto Crossroads_EventScript_Finish

Crossroads_EventScript_Trubbish::
    givepokemon SPECIES_TRUBBISH, 5, ITEM_NONE
    goto_if_eq VAR_RESULT, 0, Crossroads_EventScript_NoRoom
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
    .string "Three POKeMON are trapped!\\p"
    .string "JOE: I can't leave them here!$"

Crossroads_Text_AskPorygon:
    .string "Rescue PORYGON?$"

Crossroads_Text_AskHoundour:
    .string "Rescue HOUNDOUR?$"

Crossroads_Text_AskTrubbish:
    .string "Rescue TRUBBISH?$"

Crossroads_Text_NoChoice:
    .string "JOE: I need to choose one.\\nBut which one?$"

Crossroads_Text_Porygon:
    .string "JOE: A company prototype?\\nYou're coming with me.$"

Crossroads_Text_Houndour:
    .string "JOE: Easy, buddy.\\nWe're getting out of here.$"

Crossroads_Text_Trubbish:
    .string "JOE: You too, huh?\\nNobody wanted either of us.$"

Crossroads_Text_NoRoom:
    .string "There's no room for another\\nPOKeMON!$"

Crossroads_Text_AlreadyChosen:
    .string "JOE: We already have a partner.\\nTime to get moving.$"
