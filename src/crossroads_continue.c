#include "global.h"
#include "johto_exploration.h"
#include "crossroads_continue.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "constants/maps.h"
#include "constants/layouts.h"
#include "constants/event_objects.h"
#include "constants/heal_locations.h"
#include "constants/azalea_kiln_door.h"
#include "overworld.h"

// Authored masks are generated with the corresponding reconstructed floors.
// Bit 0 marks walkable saves; bit 1 marks Surf saves; bit 2 marks dry fallback
// tiles in the public component. Valid new saves in other components stay put,
// but a blocked legacy position must not be moved into an isolated side area.
// Matching map IDs and exact dimensions prevent use on earlier 28x22 floors.
#define UNION_CONTINUE_DRY      1
#define UNION_CONTINUE_SURF     2
#define UNION_CONTINUE_FALLBACK 4
static const u8 sUnionCave1FContinueMask[] = INCBIN_U8("data/layouts/UnionCave_1F/safe_continue.bin");
static const u8 sUnionCaveB1FContinueMask[] = INCBIN_U8("data/layouts/UnionCave_2F/safe_continue.bin");
static const u8 sUnionCaveB2FContinueMask[] = INCBIN_U8("data/layouts/UnionCave_3F/safe_continue.bin");
_Static_assert(sizeof(sUnionCave1FContinueMask) == 32 * 96, "Union Cave 1F continue mask size");
_Static_assert(sizeof(sUnionCaveB1FContinueMask) == 32 * 64, "Union Cave B1F continue mask size");
_Static_assert(sizeof(sUnionCaveB2FContinueMask) == 32 * 96, "Union Cave B2F continue mask size");

static const u8 *GetUnionCaveContinueMask(void)
{
    const struct MapLayout *layout = gMapHeader.mapLayout;
    if (gSaveBlock1Ptr->location.mapGroup != MAP_GROUP(MAP_UNION_CAVE_1_F))
        return NULL;
    if (gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_UNION_CAVE_1_F)
     && layout->width == 32 && layout->height == 96)
        return sUnionCave1FContinueMask;
    if (gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_UNION_CAVE_2_F)
     && layout->width == 32 && layout->height == 64)
        return sUnionCaveB1FContinueMask;
    if (gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_UNION_CAVE_3_F)
     && layout->width == 32 && layout->height == 96)
        return sUnionCaveB2FContinueMask;
    return NULL;
}

// The newly built kiln replaced formerly walkable grass. Its roof can draw
// over a player even on an otherwise passable cell, so old saves in its small
// footprint must land on visible open ground when continuing.
static bool32 IsAzaleaKilnFootprint(s16 x, s16 y)
{
    return gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_AZALEA_TOWN)
        && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_AZALEA_TOWN)
        && x >= AZALEA_KILN_ORIGIN_X && x < AZALEA_KILN_ORIGIN_X + AZALEA_KILN_WIDTH
        && y >= AZALEA_KILN_ORIGIN_Y && y < AZALEA_KILN_ORIGIN_Y + AZALEA_KILN_HEIGHT;
}

static bool32 IsClearContinueTile(s16 x, s16 y)
{
    const struct MapLayout *layout = gMapHeader.mapLayout;
    const u8 *unionMask = GetUnionCaveContinueMask();
    u16 block;
    u32 i;
    if (x < 0 || y < 0 || x >= layout->width || y >= layout->height || IsAzaleaKilnFootprint(x, y))
        return FALSE;
    block = layout->map[y * layout->width + x];
    if ((block & MAPGRID_COLLISION_MASK) || (block >> 12) != 3)
        return FALSE;
    if (unionMask != NULL && !(unionMask[y * layout->width + x] & UNION_CONTINUE_FALLBACK))
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

static bool32 NeedsUnionCaveRelocation(s16 x, s16 y)
{
    const struct MapLayout *layout = gMapHeader.mapLayout;
    const u8 *mask = GetUnionCaveContinueMask();
    u8 needed;
    if (mask == NULL)
        return FALSE;
    if (x < 0 || y < 0 || x >= layout->width || y >= layout->height)
        return TRUE;
    needed = SavedPlayerWasSurfing() ? UNION_CONTINUE_SURF : UNION_CONTINUE_DRY;
    return !(mask[y * layout->width + x] & needed);
}

// New cave geometry has appended layout identities. The saved layout ID is
// still the legacy ID on the first Continue, before SetCurrentMapLayout updates
// it. This distinguishes an old coordinate which happens to be walkable in an
// isolated pocket from a deliberate new save there without adding save fields.
static bool32 IsLegacyUnionCaveLayout(u16 savedLayout)
{
    if (gSaveBlock1Ptr->location.mapGroup != MAP_GROUP(MAP_UNION_CAVE_1_F))
        return FALSE;
    switch (gSaveBlock1Ptr->location.mapNum)
    {
    case MAP_NUM(MAP_UNION_CAVE_1_F):
        return savedLayout == LAYOUT_UNION_CAVE_1_F && gMapHeader.mapLayoutId == LAYOUT_HGSS_UNION_CAVE_1_F;
    case MAP_NUM(MAP_UNION_CAVE_2_F):
        return savedLayout == LAYOUT_UNION_CAVE_2_F && gMapHeader.mapLayoutId == LAYOUT_HGSS_UNION_CAVE_2_F;
    case MAP_NUM(MAP_UNION_CAVE_3_F):
        return savedLayout == LAYOUT_UNION_CAVE_3_F && gMapHeader.mapLayoutId == LAYOUT_HGSS_UNION_CAVE_3_F;
    default:
        return FALSE;
    }
}

static bool32 NeedsLegacyUnionCaveRelocation(bool32 legacy, s16 x, s16 y)
{
    const struct MapLayout *layout = gMapHeader.mapLayout;
    const u8 *mask = GetUnionCaveContinueMask();
    if (!legacy || mask == NULL)
        return FALSE;
    if (x < 0 || y < 0 || x >= layout->width || y >= layout->height)
        return TRUE;
    return !(mask[y * layout->width + x] & UNION_CONTINUE_FALLBACK);
}

bool32 Crossroads_PrepareContinue(void)
{
    const struct MapLayout *layout;
    s16 x, y, nx, ny, radius;
    u32 i;
    bool32 legacyUnionCave;
    if (!Johto_IsExplorationGroup(gSaveBlock1Ptr->location.mapGroup))
        return FALSE;
    Crossroads_EnsureAreaRespawn();
    legacyUnionCave = IsLegacyUnionCaveLayout(gSaveBlock1Ptr->mapLayoutId);
    // The old B2F was a single room. In the reconstructed map its dry
    // components require Surf or a Ruins puzzle to reach the public exit;
    // a legacy save cannot be assumed to have either. Migrate it once to the
    // public B1F component instead of potentially trapping the player.
    if (legacyUnionCave
     && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_UNION_CAVE_3_F))
    {
        gSaveBlock1Ptr->location.mapGroup = MAP_GROUP(MAP_UNION_CAVE_2_F);
        gSaveBlock1Ptr->location.mapNum = MAP_NUM(MAP_UNION_CAVE_2_F);
        gSaveBlock1Ptr->location.warpId = WARP_ID_NONE;
        gSaveBlock1Ptr->location.x = WARP_ID_NONE;
        gSaveBlock1Ptr->location.y = WARP_ID_NONE;
        gMapHeader = *Overworld_GetMapHeaderByGroupAndId(MAP_GROUP(MAP_UNION_CAVE_2_F), MAP_NUM(MAP_UNION_CAVE_2_F));
    }
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
     && !IsAzaleaKilnFootprint(x, y)
     && !NeedsDryLanding(x, y)
     && !NeedsLegacyUnionCaveRelocation(legacyUnionCave, x, y)
     && !NeedsUnionCaveRelocation(x, y))
    {
        bool32 occupied = FALSE;
        for (i = 0; i < gMapHeader.events->objectEventCount; i++)
            if (gMapHeader.events->objectEvents[i].x == x && gMapHeader.events->objectEvents[i].y == y)
                occupied = TRUE;
        if (!occupied)
            return TRUE;
    }
    // Repair blocked positions and legacy cave saves outside the public
    // component. Valid saves on the new layout keep their exact position.
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
