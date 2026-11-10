#include "global.h"
#include "johto_exploration.h"
#include "main.h"
#include "event_data.h"
#include "constants/maps.h"

// Explicit survey assistance: RAM only. No badges, moves, flags or save changes.
static EWRAM_DATA bool8 sJohtoTestAccess = FALSE;

bool32 Johto_IsExplorationGroup(u8 group)
{
    return !IS_FRLG && (group == MAP_GROUP(MAP_OLIVINE_CITY) || group == JOHTO_EXTRA_MAP_GROUP);
}

bool32 Johto_CanTestSurf(void)
{
    bool32 emergency = JOY_HELD(L_BUTTON | R_BUTTON | SELECT_BUTTON) == (L_BUTTON | R_BUTTON | SELECT_BUTTON);
    return Johto_IsExplorationGroup(gSaveBlock1Ptr->location.mapGroup)
        && gPartiesCount[B_TRAINER_PLAYER] != 0 && (sJohtoTestAccess || emergency);
}

void Johto_ToggleTestAccess(void)
{
    sJohtoTestAccess = !sJohtoTestAccess;
    gSpecialVar_Result = sJohtoTestAccess;
}

void Johto_EnableTestAccess(void)
{
    sJohtoTestAccess = TRUE;
}

// Owner-requested QA kit is explicit and separate from RAM-only survey access.
void Johto_QAKitRequested(void)
{
    gSpecialVar_Result = JOY_HELD(R_BUTTON) != 0;
}
