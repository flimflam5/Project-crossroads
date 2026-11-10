@ Explicit, reversible development-only access. No saved progression grants.
Johto_TestDesk::
    lockall
    faceplayer
    special Johto_QAKitRequested
    goto_if_eq VAR_RESULT, 1, Johto_QAKit
    msgbox Johto_TestDeskPrompt, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Johto_TestEnd
    special Johto_ToggleTestAccess
    goto_if_eq VAR_RESULT, 0, Johto_TestDisabled
    msgbox Johto_TestEnabledText, MSGBOX_DEFAULT
    goto Johto_TestEnd
Johto_TestDisabled:
    msgbox Johto_TestDisabledText, MSGBOX_DEFAULT
Johto_TestEnd:
    releaseall
    end
Johto_TestDeskPrompt:
    .string "EXPLORATION TEST DESK\pToggle session-only water access?\nThis grants no moves or badges.$"
Johto_TestEnabledText:
    .string "Test access enabled until reset.\nFace water and press A.\pThis is development assistance,\nnot permanent story progress.$"
Johto_TestDisabledText:
    .string "Normal water rules restored.$"

Johto_TestSurf::
    lockall
    msgbox Johto_TestSurfPrompt, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, Johto_TestEnd
    special Johto_EnableTestAccess
    setfieldeffectargument 0, 0
    dofieldeffect FLDEFF_USE_SURF
    releaseall
    end
Johto_TestSurfPrompt:
    .string "EXPLORATION TEST ACCESS\nCross the water with your partner?$"

Johto_AtlasBoard::
    lockall
    fadescreen FADE_TO_BLACK
    special FieldShowRegionMap
    releaseall
    end
