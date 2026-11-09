#include "global.h"
#include "crossroads_continue.h"
#include "event_object_movement.h"
#include "fieldmap.h"
#include "constants/maps.h"
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
    if (!IS_FRLG && gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_OLIVINE_CITY)
     && heal->mapGroup == 0 && heal->mapNum == 0 && heal->warpId == 0
     && heal->x == 0 && heal->y == 0)
        SetLastHealLocationWarp(HEAL_LOCATION_OLIVINE_CITY);
}

bool32 Crossroads_PrepareContinue(void)
{
    const struct MapLayout *layout;
    s16 x, y, nx, ny, radius;
    u32 i;
    if (IS_FRLG || gSaveBlock1Ptr->location.mapGroup != MAP_GROUP(MAP_OLIVINE_CITY))
        return FALSE;
    Crossroads_EnsureAreaRespawn();
    layout = gMapHeader.mapLayout;
    // These authored maps do not use persistent terrain puzzles. Old cached tiles
    // must not overlay new buildings, stairways or approved encounter grass.
    CpuFill16(0, gSaveBlock1Ptr->mapView, sizeof(gSaveBlock1Ptr->mapView));
    x = gSaveBlock1Ptr->pos.x;
    y = gSaveBlock1Ptr->pos.y;
    if (x >= 0 && y >= 0 && x < layout->width && y < layout->height
     && !(layout->map[y * layout->width + x] & MAPGRID_COLLISION_MASK))
        return TRUE;
    // Only repair positions that became blocked; valid saves never move.
    for (radius = 1; radius <= layout->width + layout->height; radius++)
        for (ny = y - radius; ny <= y + radius; ny++)
            for (nx = x - radius; nx <= x + radius; nx++)
            {
                s16 dx = nx > x ? nx - x : x - nx;
                s16 dy = ny > y ? ny - y : y - ny;
                if (dx + dy != radius || !IsClearContinueTile(nx, ny))
                    continue;
                gSaveBlock1Ptr->pos.x = nx;
                gSaveBlock1Ptr->pos.y = ny;
                for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
                {
                    if (gObjectEvents[i].isPlayer)
                    {
                        gObjectEvents[i].initialCoords.x = gObjectEvents[i].currentCoords.x = gObjectEvents[i].previousCoords.x = nx + MAP_OFFSET;
                        gObjectEvents[i].initialCoords.y = gObjectEvents[i].currentCoords.y = gObjectEvents[i].previousCoords.y = ny + MAP_OFFSET;
                    }
                    if (gSaveBlock1Ptr->objectEvents[i].isPlayer)
                    {
                        gSaveBlock1Ptr->objectEvents[i].initialCoords.x = gSaveBlock1Ptr->objectEvents[i].currentCoords.x = gSaveBlock1Ptr->objectEvents[i].previousCoords.x = nx + MAP_OFFSET;
                        gSaveBlock1Ptr->objectEvents[i].initialCoords.y = gSaveBlock1Ptr->objectEvents[i].currentCoords.y = gSaveBlock1Ptr->objectEvents[i].previousCoords.y = ny + MAP_OFFSET;
                    }
                }
                return TRUE;
            }
    return TRUE;
}
