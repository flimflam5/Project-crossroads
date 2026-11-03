@ Project Crossroads - first GBA event script prototype.
@ Staged source: not yet included in the engine's global script table.
@ Before wiring, reserve a dedicated VAR_CROSSROADS_STARTER in constants/vars.h.
@ Values: 0 = none, 1 = Porygon, 2 = Houndour, 3 = Trubbish.
@ Use an interactable object on the eventual Silph containment map to call this event.
@ The givepokemon command is supported by pokeemerald's event script system.

Crossroads_EventScript_ChooseStarter::
    lockall
    goto_if_ne VAR_CROSSROADS_STARTER, 0, Crossroads_EventScript_AlreadyChosen
    msgbox Crossroads_Text_Containment, MSGBOX_DEFAULT
Crossroads_EventScript_Menu::
    multichoice 0, 0, MULTI_CHOICE_CROSSROADS_STARTERS, FALSE
    switch VAR_RESULT
    case 0, Crossroads_EventScript_Porygon
    case 1, Crossroads_EventScript_Houndour
    case 2, Crossroads_EventScript_Trubbish
    goto Crossroads_EventScript_Menu

Crossroads_EventScript_Porygon::
    givepokemon SPECIES_PORYGON, 5, ITEM_NONE
    goto_if_eq VAR_RESULT, FALSE, Crossroads_EventScript_NoRoom
    setvar VAR_CROSSROADS_STARTER, 1
    msgbox Crossroads_Text_Porygon, MSGBOX_DEFAULT
    goto Crossroads_EventScript_Finish

Crossroads_EventScript_Houndour::
    givepokemon SPECIES_HOUNDOUR, 5, ITEM_NONE
    goto_if_eq VAR_RESULT, FALSE, Crossroads_EventScript_NoRoom
    setvar VAR_CROSSROADS_STARTER, 2
    msgbox Crossroads_Text_Houndour, MSGBOX_DEFAULT
    goto Crossroads_EventScript_Finish

Crossroads_EventScript_Trubbish::
    givepokemon SPECIES_TRUBBISH, 5, ITEM_NONE
    goto_if_eq VAR_RESULT, FALSE, Crossroads_EventScript_NoRoom
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
    .string "Three POKeMON are trapped in the\ncontainment room.\\p"
    .string "JOE: I can't leave them here!$"

Crossroads_Text_Porygon:
    .string "JOE: A company prototype?\nYou're coming with me.$"

Crossroads_Text_Houndour:
    .string "JOE: Easy, buddy.\nWe're getting out of here.$"

Crossroads_Text_Trubbish:
    .string "JOE: You too, huh?\nNobody wanted either of us.$"

Crossroads_Text_NoRoom:
    .string "There's no room for another\nPOKeMON!$"

Crossroads_Text_AlreadyChosen:
    .string "JOE: We already have a partner.\nTime to get moving.$"
