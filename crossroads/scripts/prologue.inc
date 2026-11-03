@ Project Crossroads: Silph containment starter event (STAGED, NOT LINKED).
@ This version uses the engine's existing yes/no UI; no custom multichoice
@ constant is needed. Requires a reserved persistent VAR_CROSSROADS_STARTER.
@ Attach this script to a map object only after defining that variable.
@ 0 = unchosen, 1 = Elgyem, 2 = Seedot, 3 = Trubbish.

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
