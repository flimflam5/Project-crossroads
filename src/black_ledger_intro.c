#include "global.h"
#include "black_ledger_intro.h"
#include "bg.h"
#include "gpu_regs.h"
#include "main.h"
#include "menu.h"
#include "palette.h"
#include "scanline_effect.h"
#include "sprite.h"
#include "task.h"
#include "text.h"
#include "title_screen.h"
#include "util.h"
#include "window.h"
#include "constants/rgb.h"
#include "../graphics/intro/black_ledger/light.h"

// A reversible, branded boot prototype using the accepted harbor composition.
// No story flags, saved state, music settings or New Game initialization change.
static const u32 sHarborTiles[] = INCBIN_U32("graphics/intro/black_ledger/tiles.bin");
static const u16 sHarborTilemap[] = INCBIN_U16("graphics/intro/black_ledger/tilemap.bin");
static const u16 sHarborPalette[] = INCBIN_U16("graphics/intro/black_ledger/palette.bin");
static const struct BgTemplate sBgTemplates[] =
{
    {.bg = 0, .charBaseIndex = 2, .mapBaseIndex = 30, .priority = 0},
    {.bg = 1, .charBaseIndex = 0, .mapBaseIndex = 31, .priority = 1},
};
static const struct WindowTemplate sWindows[] =
{
    {.bg = 0, .width = 30, .height = 20, .paletteNum = 0, .baseBlock = 1},
    DUMMY_WIN_TEMPLATE,
};
static const u16 sTextPalette[16] =
{
    RGB(1, 2, 4), RGB(29, 29, 31), RGB(4, 6, 11), RGB(12, 22, 24),
    RGB(19, 10, 24), RGB(23, 17, 12),
};
static const u8 sWhiteText[] = {0, 1, 2};
static const u8 sMutedText[] = {0, 3, 2};
static const u8 sVoidstar[] = _("VOIDSTAR");
static const u8 sInteractive[] = _("INTERACTIVE");
static const u8 sPresents[] = _("PRESENTS");
static const u8 sOlivine[] = _("OLIVINE CITY");
static const u8 sJohto[] = _("JOHTO");
static const u8 sPokemon[] = _("POKéMON");
static const u8 sBlackLedger[] = _("BLACK LEDGER");
static const u8 sSkip[] = _("A / START: SKIP");
static const u16 sSceneDurations[] = {120, 210, 90};
static EWRAM_DATA u8 sBlackLedgerIntroScene = 0;
static EWRAM_DATA u16 sBlackLedgerIntroTimer = 0;
static EWRAM_DATA bool8 sChangingScene = FALSE;
static EWRAM_DATA bool8 sLeavingIntro = FALSE;

static void CenterText(const u8 *str, u8 font, u8 y, const u8 *colors)
{
    u16 x = (DISPLAY_WIDTH - GetStringWidth(font, str, -1)) / 2;
    AddTextPrinterParameterized3(0, font, x, y, colors, TEXT_SKIP_DRAW, str);
}

static void VBlankCB_BlackLedgerIntro(void)
{
    LoadOam();
    TransferPlttBuffer();
}

static void DrawScene(void)
{
    FillWindowPixelBuffer(0, PIXEL_FILL(0));
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0 | DISPCNT_BG0_ON);
    if (sBlackLedgerIntroScene == 0)
    {
        CenterText(sVoidstar, FONT_NORMAL, 51, sWhiteText);
        CenterText(sInteractive, FONT_SMALL, 71, sMutedText);
        FillWindowPixelRect(0, PIXEL_FILL(4), 72, 93, 96, 1);
        CenterText(sPresents, FONT_SMALL, 105, sWhiteText);
    }
    else if (sBlackLedgerIntroScene == 1)
    {
        CenterText(sOlivine, FONT_NORMAL, 18, sWhiteText);
        // Only the harbor portion of the accepted source art is shown. The old
        // title lettering/Press Start pixels remain outside this hardware mask.
        FillWindowPixelRect(0, PIXEL_FILL(3), 0, 43, DISPLAY_WIDTH, 1);
        FillWindowPixelRect(0, PIXEL_FILL(3), 0, 112, DISPLAY_WIDTH, 1);
        CenterText(sJohto, FONT_SMALL, 121, sWhiteText);
        SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0 | DISPCNT_BG0_ON | DISPCNT_BG1_ON | DISPCNT_WIN0_ON);
    }
    else
    {
        CenterText(sPokemon, FONT_NORMAL, 49, sWhiteText);
        FillWindowPixelRect(0, PIXEL_FILL(4), 44, 76, 152, 1);
        CenterText(sBlackLedger, FONT_NORMAL, 88, sWhiteText);
    }
    CenterText(sSkip, FONT_SMALL, 145, sMutedText);
    PutWindowTilemap(0);
    CopyWindowToVram(0, COPYWIN_FULL);
}

static void CB2_BlackLedgerIntro(void)
{
    if (!sLeavingIntro && JOY_NEW(A_BUTTON | B_BUTTON | START_BUTTON))
    {
        sLeavingIntro = TRUE;
        sChangingScene = FALSE;
        u8 coefficient = gPaletteFade.y;
        ResetPaletteFadeControl();
        BeginNormalPaletteFade(PALETTES_ALL, 0, coefficient, 16, RGB_BLACK);
    }
    if (UpdatePaletteFade())
        return;
    if (sLeavingIntro)
    {
        FreeAllWindowBuffers();
        SetGpuReg(REG_OFFSET_DISPCNT, 0);
        SetGpuReg(REG_OFFSET_WININ, 0);
        SetGpuReg(REG_OFFSET_WINOUT, 0);
        SetMainCallback2(CB2_InitBlackLedgerTitleScreen);
        return;
    }
    if (sChangingScene)
    {
        sChangingScene = FALSE;
        sBlackLedgerIntroScene++;
        sBlackLedgerIntroTimer = 0;
        DrawScene();
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
        return;
    }
    if (sBlackLedgerIntroScene == 1)
    {
        u8 phase = sBlackLedgerIntroTimer % 96;
        BlendPalette(BLACK_LEDGER_INTRO_LIGHT_INDEX, 1,
                     (phase < 48 ? phase : 95 - phase) / 12, RGB(31, 26, 16));
    }
    if (++sBlackLedgerIntroTimer >= sSceneDurations[sBlackLedgerIntroScene])
    {
        if (sBlackLedgerIntroScene + 1 == ARRAY_COUNT(sSceneDurations))
            sLeavingIntro = TRUE;
        else
            sChangingScene = TRUE;
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
    }
}

void CB2_InitBlackLedgerIntro(void)
{
    SetVBlankCallback(NULL);
    SetHBlankCallback(NULL);
    DisableInterrupts(INTR_FLAG_HBLANK);
    ScanlineEffect_Stop();
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDALPHA, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    SetGpuReg(REG_OFFSET_WININ, WININ_WIN0_BG0 | WININ_WIN0_BG1);
    SetGpuReg(REG_OFFSET_WINOUT, WINOUT_WIN01_BG0);
    SetGpuReg(REG_OFFSET_WIN0H, DISPLAY_WIDTH);
    SetGpuReg(REG_OFFSET_WIN0V, (44 << 8) | 112);
    DmaFill16(3, 0, (void *)VRAM, VRAM_SIZE);
    DmaFill32(3, 0, (void *)OAM, OAM_SIZE);
    ResetTasks();
    ResetSpriteData();
    BuildOamBuffer();
    FreeAllSpritePalettes();
    ResetPaletteFade();
    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0, sBgTemplates, ARRAY_COUNT(sBgTemplates));
    ShowBg(0);
    ShowBg(1);
    if (!InitWindows(sWindows))
    {
        SetMainCallback2(CB2_InitBlackLedgerTitleScreen);
        return;
    }
    DeactivateAllTextPrinters();
    CpuCopy16(sHarborTiles, (void *)BG_CHAR_ADDR(0), sizeof(sHarborTiles));
    CpuCopy16(sHarborTilemap, (void *)BG_SCREEN_ADDR(31), sizeof(sHarborTilemap));
    LoadPalette(sTextPalette, 0, sizeof(sTextPalette));
    LoadPalette(sHarborPalette, 16, sizeof(sHarborPalette));
    SetGpuReg(REG_OFFSET_BG0HOFS, 0);
    SetGpuReg(REG_OFFSET_BG0VOFS, 0);
    SetGpuReg(REG_OFFSET_BG1HOFS, 0);
    SetGpuReg(REG_OFFSET_BG1VOFS, 26); // Window y44..111 sees source y70..137.
    sBlackLedgerIntroScene = 0;
    sBlackLedgerIntroTimer = 0;
    sChangingScene = FALSE;
    sLeavingIntro = FALSE;
    DrawScene();
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetVBlankCallback(VBlankCB_BlackLedgerIntro);
    EnableInterrupts(INTR_FLAG_VBLANK);
    SetMainCallback2(CB2_BlackLedgerIntro);
}
