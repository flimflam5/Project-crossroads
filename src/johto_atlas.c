#include "global.h"
#include "field_effect.h"
#include "party_menu.h"
#include "overworld.h"
#include "constants/heal_locations.h"
#include "johto_atlas.h"
#include "bg.h"
#include "gpu_regs.h"
#include "menu.h"
#include "palette.h"
#include "sprite.h"
#include "task.h"
#include "text.h"
#include "window.h"
#include "constants/rgb.h"

struct JohtoAtlasNode { const u8 *label; const u8 *abbr; u8 x, y; };
#include "data/johto_atlas.h"
static EWRAM_DATA MainCallback sAtlasReturn = NULL;
static EWRAM_DATA u8 sAtlasSelection = 0;
static EWRAM_DATA u8 sAtlasPlayer = 0;
static EWRAM_DATA bool8 sAtlasClosing = FALSE;
static EWRAM_DATA bool8 sAtlasFlyMode = FALSE;
static EWRAM_DATA bool8 sAtlasFlyConfirmed = FALSE;
static const struct BgTemplate sBgs[] = {{.bg=0,.charBaseIndex=0,.mapBaseIndex=31,.priority=0}};
static const struct WindowTemplate sWindows[] = {{.bg=0,.width=30,.height=20,.paletteNum=0,.baseBlock=1},DUMMY_WIN_TEMPLATE};
static const u16 sPalette[16] = {RGB(1,3,7),RGB(30,30,31),RGB(2,5,10),RGB(10,18,19),RGB(8,21,14),RGB(31,25,3),RGB(4,10,18),RGB(8,15,12),RGB(29,13,8)};
static const u8 sText[] = {2,1,0};
static const u8 sTitle[] = _("JOHTO ATLAS");
static const u8 sControls[] = _("D-PAD: PLACE   A/B: CLOSE");
static const u8 sFlyTitle[] = _("JOHTO QA FLY");
static const u8 sFlyControls[] = _("D-PAD: CITY   A: FLY   B: CANCEL");
static const u8 sYou[] = _("YOU");
static void DrawAtlas(void)
{
    u32 i;
    const struct JohtoAtlasNode *node;
    FillWindowPixelBuffer(0,PIXEL_FILL(2));
    AddTextPrinterParameterized3(0,FONT_SMALL,80,1,sText,TEXT_SKIP_DRAW,sAtlasFlyMode ? sFlyTitle : sTitle);
    FillWindowPixelRect(0,PIXEL_FILL(6),8,19,28,108);
    for (i=0;i<ARRAY_COUNT(sAtlasEdges);i++)
    {
        const struct JohtoAtlasNode *a=&sAtlasNodes[sAtlasEdges[i][0]], *b=&sAtlasNodes[sAtlasEdges[i][1]];
        u16 x=a->x<b->x?a->x:b->x, y=a->y<b->y?a->y:b->y;
        FillWindowPixelRect(0,PIXEL_FILL(3),x,a->y,b->x>a->x?b->x-a->x+1:a->x-b->x+1,1);
        FillWindowPixelRect(0,PIXEL_FILL(3),b->x,y,1,b->y>a->y?b->y-a->y+1:a->y-b->y+1);
    }
    for (i=0;i<ARRAY_COUNT(sAtlasNodes);i++)
    {
        node=&sAtlasNodes[i];
        FillWindowPixelRect(0,PIXEL_FILL(4),node->x-1,node->y-1,3,3);
        AddTextPrinterParameterized3(0,FONT_SMALL,node->x+3,node->y-5,sText,TEXT_SKIP_DRAW,node->abbr);
    }
    node=&sAtlasNodes[sAtlasSelection];
    FillWindowPixelRect(0,PIXEL_FILL(8),node->x-2,node->y-2,5,5);
    node=&sAtlasNodes[sAtlasPlayer];
    FillWindowPixelRect(0,PIXEL_FILL(5),node->x-1,node->y-1,3,3);
    AddTextPrinterParameterized3(0,FONT_SMALL,node->x+2,node->y+2,sText,TEXT_SKIP_DRAW,sYou);
    AddTextPrinterParameterized3(0,FONT_NORMAL,8,128,sText,TEXT_SKIP_DRAW,sAtlasNodes[sAtlasSelection].label);
    AddTextPrinterParameterized3(0,FONT_SMALL,8,146,sText,TEXT_SKIP_DRAW,sAtlasFlyMode ? sFlyControls : sControls);
    PutWindowTilemap(0);CopyWindowToVram(0,COPYWIN_FULL);
}
static void VBlank_Atlas(void) { LoadOam();TransferPlttBuffer(); }
static void CB2_Atlas(void)
{
    if (UpdatePaletteFade()) return;
    if (sAtlasClosing)
    {
        SetVBlankCallback(NULL);FreeAllWindowBuffers();
        if (sAtlasFlyConfirmed)
        {
            SetWarpDestinationToHealLocation(sAtlasFlyHealLocations[sAtlasSelection]);
            ReturnToFieldFromFlyMapSelect();
        }
        else SetMainCallback2(sAtlasReturn);
        return;
    }
    if (JOY_NEW(B_BUTTON) || (!sAtlasFlyMode && JOY_NEW(A_BUTTON)))
    {
        sAtlasClosing=TRUE;BeginNormalPaletteFade(PALETTES_ALL,0,0,16,RGB_BLACK);
    }
    else if (sAtlasFlyMode && JOY_NEW(A_BUTTON) && sAtlasFlyHealLocations[sAtlasSelection] != HEAL_LOCATION_NONE)
    {
        sAtlasFlyConfirmed=TRUE;sAtlasClosing=TRUE;
        BeginNormalPaletteFade(PALETTES_ALL,0,0,16,RGB_BLACK);
    }
    else if (JOY_NEW(DPAD_RIGHT|DPAD_DOWN))
    {
        do {sAtlasSelection=(sAtlasSelection+1)%ARRAY_COUNT(sAtlasNodes);}
        while (sAtlasFlyMode && sAtlasFlyHealLocations[sAtlasSelection] == HEAL_LOCATION_NONE);
        DrawAtlas();
    }
    else if (JOY_NEW(DPAD_LEFT|DPAD_UP))
    {
        do {sAtlasSelection=sAtlasSelection?sAtlasSelection-1:ARRAY_COUNT(sAtlasNodes)-1;}
        while (sAtlasFlyMode && sAtlasFlyHealLocations[sAtlasSelection] == HEAL_LOCATION_NONE);
        DrawAtlas();
    }
}
static u8 FindPlayerNode(void)
{
    u32 i;
    for (i=0;i<ARRAY_COUNT(sMapAtlasNode);i++)
        if (sMapAtlasGroup[i]==gSaveBlock1Ptr->location.mapGroup && sMapAtlasNumber[i]==gSaveBlock1Ptr->location.mapNum)
            return sMapAtlasNode[i];
    return 0;
}

const u8 *Johto_GetCurrentMapName(void) {return sAtlasNodes[FindPlayerNode()].label;}

static void CB2_InitAtlas(void)
{
    SetVBlankCallback(NULL);SetHBlankCallback(NULL);SetGpuReg(REG_OFFSET_DISPCNT,0);
    SetGpuReg(REG_OFFSET_BLDCNT,0);SetGpuReg(REG_OFFSET_BLDY,0);SetGpuReg(REG_OFFSET_BLDALPHA,0);
    SetGpuReg(REG_OFFSET_WININ,0);SetGpuReg(REG_OFFSET_WINOUT,0);
    DmaFill16(3,0,(void *)VRAM,VRAM_SIZE);DmaFill32(3,0,(void *)OAM,OAM_SIZE);
    ResetTasks();ResetSpriteData();FreeAllSpritePalettes();ResetPaletteFade();
    ResetBgsAndClearDma3BusyFlags(0);InitBgsFromTemplates(0,sBgs,ARRAY_COUNT(sBgs));
    if (!InitWindows(sWindows)) {SetMainCallback2(sAtlasReturn);return;}
    DeactivateAllTextPrinters();LoadPalette(sPalette,0,sizeof(sPalette));
    SetGpuReg(REG_OFFSET_BG0HOFS,0);SetGpuReg(REG_OFFSET_BG0VOFS,0);
    sAtlasPlayer=FindPlayerNode();
    sAtlasSelection=sAtlasPlayer;
    if (sAtlasFlyMode && sAtlasFlyHealLocations[sAtlasSelection] == HEAL_LOCATION_NONE) sAtlasSelection=0;
    sAtlasFlyConfirmed=FALSE;sAtlasClosing=FALSE;DrawAtlas();
    BeginNormalPaletteFade(PALETTES_ALL,0,16,0,RGB_BLACK);ShowBg(0);SetGpuReg(REG_OFFSET_DISPCNT,DISPCNT_MODE_0|DISPCNT_BG0_ON);
    SetVBlankCallback(VBlank_Atlas);SetMainCallback2(CB2_Atlas);
}
void Johto_OpenAtlas(MainCallback callback) {sAtlasFlyMode=FALSE;sAtlasReturn=callback;SetMainCallback2(CB2_InitAtlas);}
void CB2_OpenJohtoFlyMap(void) {sAtlasFlyMode=TRUE;sAtlasReturn=CB2_ReturnToPartyMenuFromFlyMap;SetMainCallback2(CB2_InitAtlas);}
