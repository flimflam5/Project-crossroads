#include "global.h"
#include "johto_exploration.h"
#include "main.h"
#include "event_data.h"
#include "constants/maps.h"

// Explicit survey assistance: RAM only. No badges, moves, flags or save changes.
static EWRAM_DATA bool8 sJohtoTestAccess = FALSE;

bool32 Johto_CanTestSurf(void)
{
    bool32 emergency = JOY_HELD(L_BUTTON | R_BUTTON | SELECT_BUTTON) == (L_BUTTON | R_BUTTON | SELECT_BUTTON);
    return !IS_FRLG && gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_OLIVINE_CITY)
        && gPlayerPartyCount != 0 && (sJohtoTestAccess || emergency);
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
