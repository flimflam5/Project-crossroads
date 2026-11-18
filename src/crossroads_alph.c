#include "global.h"
#include "crossroads_alph.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "item_menu.h"
#include "pokemon.h"
#include "constants/battle.h"
#include "constants/event_objects.h"
#include "constants/items.h"
#include "constants/maps.h"
#include "constants/species.h"

#if !IS_FRLG
// Equivalent to HGSS's (6,3) north-facing check in the 10x11 chamber crop.
// Only selects the field reaction; it neither consumes an item nor saves state.
bool32 Crossroads_AlphShouldUseWaterStone(void)
{
    s16 x, y;
    if (gSpecialVar_ItemId != ITEM_WATER_STONE
     || gSaveBlock1Ptr->location.mapGroup != MAP_GROUP(MAP_RUINS_OF_ALPH_SOUTHWEST_CHAMBER)
     || gSaveBlock1Ptr->location.mapNum != MAP_NUM(MAP_RUINS_OF_ALPH_SOUTHWEST_CHAMBER))
        return FALSE;
    PlayerGetDestCoords(&x, &y);
    return x == 5 + MAP_OFFSET && y == 2 + MAP_OFFSET
        && GetPlayerFacingDirection() == DIR_NORTH;
}
#endif

// HGSS checks only the player's party, and excludes eggs, but accepts fainted
// Ho-Oh. Do not use CheckPartyHasSpecies: that helper does not exclude eggs.
u16 Crossroads_AlphHasNonEggHoOh(void)
{
    u32 i;
    u8 count = CalculatePlayerPartyCount();
    for (i = 0; i < count; i++)
    {
        struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][i];
        if (!GetMonData(mon, MON_DATA_IS_EGG) && GetMonData(mon, MON_DATA_SPECIES) == SPECIES_HO_OH)
            return TRUE;
    }
    return FALSE;
}
