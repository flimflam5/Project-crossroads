#include "global.h"
#include "title_screen.h"
#include "main.h"
#include "main_menu.h"
#include "palette.h"
#include "util.h"
#include "gpu_regs.h"
#include "sprite.h"
#include "task.h"
#include "scanline_effect.h"
#include "sound.h"
#include "event_data.h"
#include "reset_rtc_screen.h"
#include "clear_save_data_menu.h"
#include "berry_fix_program.h"
#include "constants/rgb.h"
#include "constants/songs.h"
#include "../graphics/title_screen/black_ledger/light.h"

// One 600-tile 8bpp text background, below screen block 31 in BG VRAM.
static const u32 sHarborTiles[] = INCBIN_U32("graphics/title_screen/black_ledger/tiles.bin");
static const u16 sHarborTilemap[] = INCBIN_U16("graphics/title_screen/black_ledger/tilemap.bin");
static const u16 sHarborPalette[] = INCBIN_U16("graphics/title_screen/black_ledger/palette.bin");
static EWRAM_DATA MainCallback sNextCallback = NULL;
static EWRAM_DATA u16 sLightTimer = 0;

static void VBlankCB_BlackLedgerTitle(void)
{
    LoadOam();
    TransferPlttBuffer();
}

static void CB2_BlackLedgerTitle(void)
{
    if (UpdatePaletteFade())
        return;
    if (sNextCallback != NULL)
    {
        SetMainCallback2(sNextCallback);
        return;
    }

    // Retain the established title shortcuts and their confirmation screens.
    if (JOY_HELD(B_BUTTON | SELECT_BUTTON | DPAD_UP) == (B_BUTTON | SELECT_BUTTON | DPAD_UP))
        sNextCallback = CB2_InitClearSaveDataScreen;
    else if (JOY_HELD(B_BUTTON | SELECT_BUTTON | DPAD_LEFT) == (B_BUTTON | SELECT_BUTTON | DPAD_LEFT) && CanResetRTC())
        sNextCallback = CB2_InitResetRtcScreen;
    else if (JOY_HELD(B_BUTTON | SELECT_BUTTON) == (B_BUTTON | SELECT_BUTTON))
        sNextCallback = CB2_InitBerryFixProgram;
    else if (JOY_NEW(A_BUTTON | START_BUTTON))
        sNextCallback = CB2_InitMainMenu;

    if (sNextCallback != NULL)
    {
        FadeOutBGM(4);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        return;
    }

    // Subtle palette-only harbor lighting; no sprite/tile tearing or save writes.
    sLightTimer = (sLightTimer + 1) & 127;
    BlendPalette(BLACK_LEDGER_LIGHT_PALETTE_INDEX, 1,
                 (sLightTimer < 64 ? sLightTimer : 127 - sLightTimer) / 16, RGB_BLACK);
}

void CB2_InitBlackLedgerTitleScreen(void)
{
    SetVBlankCallback(NULL);
    SetHBlankCallback(NULL);
    DisableInterrupts(INTR_FLAG_HBLANK);
    ScanlineEffect_Stop();
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDALPHA, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    SetGpuReg(REG_OFFSET_WININ, 0);
    SetGpuReg(REG_OFFSET_WINOUT, 0);
    SetGpuReg(REG_OFFSET_BG0HOFS, 0);
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    DmaFill16(3, 0, (void *)VRAM, VRAM_SIZE);
    DmaFill32(3, 0, (void *)OAM, OAM_SIZE);
    ResetTasks();
    ResetSpriteData();
    FreeAllSpritePalettes();
    ResetPaletteFade();
    CpuCopy16(sHarborTiles, (void *)BG_CHAR_ADDR(0), sizeof(sHarborTiles));
    CpuCopy16(sHarborTilemap, (void *)BG_SCREEN_ADDR(31), sizeof(sHarborTilemap));
    LoadPalette(sHarborPalette, 0, sizeof(sHarborPalette));
    SetGpuReg(REG_OFFSET_BG0CNT, BGCNT_CHARBASE(0) | BGCNT_SCREENBASE(31) | BGCNT_256COLOR | BGCNT_TXT256x256);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0 | DISPCNT_BG0_ON);
    sNextCallback = NULL;
    sLightTimer = 0;
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetVBlankCallback(VBlankCB_BlackLedgerTitle);
    EnableInterrupts(INTR_FLAG_VBLANK);
    PlayBGM(MUS_ABANDONED_SHIP); // Existing engine track, temporary title audio.
    SetMainCallback2(CB2_BlackLedgerTitle);
}
