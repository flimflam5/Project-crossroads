/* Optional mGBA 0.10 development test bridge. Never patches ROM bytes. */
#include <mgba/flags.h> /* Must precede API headers to match the library ABI. */
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba-util/vfs.h>
#include <stdio.h>

static struct mCore *core;
static color_t pixels[240 * 160];

static void QuietLog(struct mLogger *logger, int category, enum mLogLevel level,
                     const char *format, va_list args)
{
    if (level & (mLOG_FATAL | mLOG_ERROR))
        vfprintf(stderr, format, args);
}

static struct mLogger logger = {.log = QuietLog};

int emu_init(const char *rom)
{
    mLogSetDefaultLogger(&logger);
    core = mCoreFind(rom);
    if (!core || !core->init(core))
        return 0;
    mCoreInitConfig(core, NULL);
    core->setVideoBuffer(core, pixels, 240);
    core->setAudioBufferSize(core, 1024);
    if (!mCoreLoadFile(core, rom))
        return 0;
    core->reset(core);
    return 1;
}

void emu_frames(int keys, int frames)
{
    core->setKeys(core, keys);
    for (int i = 0; i < frames; i++)
        core->runFrame(core);
    core->setKeys(core, 0);
}

unsigned emu_read(unsigned address, int width)
{
    if (width == 4) return core->busRead32(core, address);
    if (width == 2) return core->busRead16(core, address);
    return core->busRead8(core, address);
}

void emu_write(unsigned address, unsigned value, int width)
{
    if (width == 4) core->busWrite32(core, address, value);
    else if (width == 2) core->busWrite16(core, address, value);
    else core->busWrite8(core, address, value);
}

int emu_state(const char *path, int load)
{
    size_t size = core->stateSize(core);
    void *data = malloc(size);
    FILE *file = fopen(path, load ? "rb" : "wb");
    if (!file || !data)
    {
        if (file) fclose(file);
        free(data);
        return 0;
    }
    int ok;
    if (load)
        ok = fread(data, 1, size, file) == size && core->loadState(core, data);
    else
        ok = core->saveState(core, data) && fwrite(data, 1, size, file) == size;
    fclose(file);
    free(data);
    return ok;
}

int emu_image(const char *path)
{
    struct VFile *file = VFileOpen(path, O_CREAT | O_TRUNC | O_WRONLY);
    if (!file) return 0;
    int ok = mCoreTakeScreenshotVF(core, file);
    file->close(file);
    return ok;
}
