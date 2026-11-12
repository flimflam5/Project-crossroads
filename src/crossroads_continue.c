#include "global.h"
#include "johto_exploration.h"
#include "crossroads_continue.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "constants/maps.h"
#include "constants/event_objects.h"
#include "constants/heal_locations.h"
#include "overworld.h"

static bool32 IsClearContinueTile(s16 x, s16 y)
{
    const struct MapLayout *layout = gMapHeader.mapLayout;
    u16 block;
    u32 i;
    if (x < 0 || y < 0 || x >= layout->width || y >= layout->height)
        return FALSE;
    block = layout->map[y * layout->width + x];
    if ((block & MAPGRID_COLLISION_MASK) || (block >> 12) != 3)
        return FALSE;
    for (i = 0; i < gMapHeader.events->warpCount; i++)
        if (gMapHeader.events->warps[i].x == x && gMapHeader.events->warps[i].y == y)
            return FALSE;
    for (i = 0; i < gMapHeader.events->objectEventCount; i++)
        if (gMapHeader.events->objectEvents[i].x == x && gMapHeader.events->objectEvents[i].y == y)
            return FALSE;
    return TRUE;
}

// Fresh Alpha-based games have an all-zero heal warp until a Center is visited.
// Do not replace any real Center choice, including legitimate future Hoenn visits.
void Crossroads_EnsureAreaRespawn(void)
{
    const struct WarpData *heal = &gSaveBlock1Ptr->lastHealLocation;
    if (Johto_IsExplorationGroup(gSaveBlock1Ptr->location.mapGroup)
     && heal->mapGroup == 0 && heal->mapNum == 0 && heal->warpId == 0
     && heal->x == 0 && heal->y == 0)
        SetLastHealLocationWarp(HEAL_LOCATION_OLIVINE_CITY);
    // Preserve the chosen Center for pre-HGSS saves whose outdoor doorway moved.
    if (heal->mapGroup == MAP_GROUP(MAP_ECRUTEAK_CITY)
     && heal->mapNum == MAP_NUM(MAP_ECRUTEAK_CITY)
     && heal->warpId == WARP_ID_NONE && heal->x == 21 && heal->y == 35)
        SetLastHealLocationWarp(HEAL_LOCATION_ECRUTEAK_CITY);
    if (heal->mapGroup == MAP_GROUP(MAP_VIOLET_CITY)
     && heal->mapNum == MAP_NUM(MAP_VIOLET_CITY)
     && heal->warpId == WARP_ID_NONE && heal->x == 35 && heal->y == 33)
        SetLastHealLocationWarp(HEAL_LOCATION_VIOLET_CITY);
    if (heal->mapGroup == MAP_GROUP(MAP_OLIVINE_CITY)
     && heal->mapNum == MAP_NUM(MAP_OLIVINE_CITY)
     && heal->warpId == WARP_ID_NONE && heal->x == 11 && heal->y == 22)
        SetLastHealLocationWarp(HEAL_LOCATION_OLIVINE_CITY);
}

static bool32 SavedPlayerWasSurfing(void)
{
    u32 i;

    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
    {
        const struct ObjectEvent *event = &gSaveBlock1Ptr->objectEvents[i];
        u16 graphicsId = (event->graphicsId >> 8) | (event->graphicsId << 8);

        if (event->spriteId != 127)
            graphicsId &= 0xFF;
        if (event->isPlayer
         && (graphicsId == OBJ_EVENT_GFX_JOE_SURFING
          || graphicsId == OBJ_EVENT_GFX_BRENDAN_SURFING
          || graphicsId == OBJ_EVENT_GFX_MAY_SURFING))
            return TRUE;
    }
    return FALSE;
}

static bool32 NeedsDryLanding(s16 x, s16 y)
{
    const struct MapLayout *layout = gMapHeader.mapLayout;
    bool32 reconstructedWater =
        (gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_VIOLET_CITY)
         && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_VIOLET_CITY))
     || (gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_OLIVINE_CITY)
         && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_OLIVINE_CITY));
    if (!reconstructedWater
     || x < 0 || y < 0 || x >= layout->width || y >= layout->height
     || (layout->map[y * layout->width + x] >> 12) != 1)
        return FALSE;
    // An old walking save can now occupy the reference pond or waterfront.
    // Preserve actual Surf saves; only move a walking avatar to nearby dry
    // ground on Continue.
    return !SavedPlayerWasSurfing();
}

bool32 Crossroads_PrepareContinue(void)
{
    const struct MapLayout *layout;
    s16 x, y, nx, ny, radius;
    u32 i;
    if (!Johto_IsExplorationGroup(gSaveBlock1Ptr->location.mapGroup))
        return FALSE;
    Crossroads_EnsureAreaRespawn();
    // Old saves inside a shared-layout room must use that room's new dedicated
    // layout. Map/layout identities remain appended/stable; save format is intact.
    if (gSaveBlock1Ptr->mapLayoutId != gMapHeader.mapLayoutId)
        SetCurrentMapLayout(gMapHeader.mapLayoutId);
    layout = gMapHeader.mapLayout;
    // These authored maps do not use persistent terrain puzzles. Old cached tiles
    // must not overlay new buildings, stairways or approved encounter grass.
    CpuFill16(0, gSaveBlock1Ptr->mapView, sizeof(gSaveBlock1Ptr->mapView));
    x = gSaveBlock1Ptr->pos.x;
    y = gSaveBlock1Ptr->pos.y;
    if (x >= 0 && y >= 0 && x < layout->width && y < layout->height
     && !(layout->map[y * layout->width + x] & MAPGRID_COLLISION_MASK)
     && !NeedsDryLanding(x, y))
    {
        bool32 occupied = FALSE;
        for (i = 0; i < gMapHeader.events->objectEventCount; i++)
            if (gMapHeader.events->objectEvents[i].x == x && gMapHeader.events->objectEvents[i].y == y)
                occupied = TRUE;
        if (!occupied)
            return TRUE;
    }
    // Only repair positions that became blocked; valid saves never move.
    for (radius = 1; radius <= layout->width + layout->height; radius++)
        for (ny = y - radius; ny <= y + radius; ny++)
            for (nx = x - radius; nx <= x + radius; nx++)
            {
                s16 dx = nx > x ? nx - x : x - nx;
                s16 dy = ny > y ? ny - y : y - ny;
                if (dx + dy != radius || !IsClearContinueTile(nx, ny))
                    continue;
                // A relocated Surf save now lands on verified dry floor.
                // Continue restores avatar state from the saved/loaded player
                // graphics, not only its coordinates. Normalize both copies
                // here; valid water saves return above and remain untouched.
                // Mirror SaveObjectEvents' byte order and sentinel exactly.
                bool32 landFromSurf = SavedPlayerWasSurfing();
                u16 walkingGraphics = GetPlayerAvatarGraphicsIdByStateIdAndGender(
                    PLAYER_AVATAR_STATE_NORMAL, gSaveBlock2Ptr->playerGender);
                gSaveBlock1Ptr->pos.x = nx;
                gSaveBlock1Ptr->pos.y = ny;
                for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
                {
                    if (gObjectEvents[i].isPlayer)
                    {
                        gObjectEvents[i].initialCoords.x = gObjectEvents[i].currentCoords.x = gObjectEvents[i].previousCoords.x = nx + MAP_OFFSET;
                        gObjectEvents[i].initialCoords.y = gObjectEvents[i].currentCoords.y = gObjectEvents[i].previousCoords.y = ny + MAP_OFFSET;
                        if (landFromSurf)
                            gObjectEvents[i].graphicsId = walkingGraphics;
                    }
                    if (gSaveBlock1Ptr->objectEvents[i].isPlayer)
                    {
                        gSaveBlock1Ptr->objectEvents[i].initialCoords.x = gSaveBlock1Ptr->objectEvents[i].currentCoords.x = gSaveBlock1Ptr->objectEvents[i].previousCoords.x = nx + MAP_OFFSET;
                        gSaveBlock1Ptr->objectEvents[i].initialCoords.y = gSaveBlock1Ptr->objectEvents[i].currentCoords.y = gSaveBlock1Ptr->objectEvents[i].previousCoords.y = ny + MAP_OFFSET;
                        if (landFromSurf)
                        {
                            gSaveBlock1Ptr->objectEvents[i].graphicsId = (walkingGraphics >> 8) | (walkingGraphics << 8);
                            gSaveBlock1Ptr->objectEvents[i].spriteId = 127;
                        }
                    }
                }
                return TRUE;
            }
    return TRUE;
}
