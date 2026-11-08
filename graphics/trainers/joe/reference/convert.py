#!/usr/bin/env python3
"""Reproduce Joe's indexed trainer assets from the preserved generated sheet.

Requires Pillow. Run from any directory; default paths are relative to this file.
"""

import argparse
from pathlib import Path

from PIL import Image


REFERENCE_DIR = Path(__file__).resolve().parent
CELL_ORDER = ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1))
# Reserve burgundy/red for the tie and capture ball instead of allowing the
# much larger rear shirt/hair regions to dominate automatic quantization.
OPAQUE_COLORS = (
    (16, 8, 8), (41, 24, 32), (65, 49, 57), (98, 65, 57), (131, 90, 82),
    (180, 123, 98), (246, 189, 156), (255, 222, 189), (246, 238, 230),
    (222, 206, 206), (172, 148, 148), (115, 90, 106), (98, 24, 41),
    (156, 41, 65), (230, 74, 82),
)


def convert(source):
    with Image.open(source) as opened:
        image = opened.convert("RGBA")
    if image.size != (1536, 1024):
        raise ValueError(f"Expected 1536x1024 source sheet, got {image.size}")

    colors = [tuple(round(v / 255 * 31) * 255 // 31 for v in rgb)
              for rgb in OPAQUE_COLORS]
    # Index zero is transparent. Its RGB value is only an editing matte.
    palette = [(106, 189, 164)] + colors
    flat_palette = [v for rgb in palette for v in rgb]
    frames = []
    for x, y in CELL_ORDER:
        frame = image.crop((x * 512, y * 512, (x + 1) * 512, (y + 1) * 512))
        frame.putalpha(frame.getchannel("A").point(lambda v: 255 if v >= 128 else 0))
        frame = frame.resize((64, 64), Image.Resampling.NEAREST)
        indices = []
        pixels = (frame.get_flattened_data() if hasattr(frame, "get_flattened_data")
                  else frame.getdata())
        for r, g, b, alpha in pixels:
            if not alpha:
                indices.append(0)
                continue
            nearest = min(range(len(colors)), key=lambda j:
                          sum((v - w) ** 2 for v, w in zip((r, g, b), colors[j])))
            indices.append(nearest + 1)
        indexed = Image.new("P", (64, 64))
        indexed.putdata(indices)
        indexed.putpalette(flat_palette)
        indexed.info["transparency"] = 0
        frames.append(indexed)

    back = Image.new("P", (64, 256))
    back.putpalette(flat_palette)
    back.info["transparency"] = 0
    for i, frame in enumerate(frames[1:]):
        back.paste(frame, (0, i * 64))
    pal_text = "JASC-PAL\n0100\n16\n" + "".join(f"{r} {g} {b}\n" for r, g, b in palette)
    return {"front.png": frames[0], "back.png": back}, pal_text, frames


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path,
                        default=REFERENCE_DIR / "generated-trainer-sheet.png")
    parser.add_argument("--output-dir", type=Path, default=REFERENCE_DIR.parent)
    parser.add_argument("--preview", type=Path, help="Optional enlarged comparison PNG")
    parser.add_argument("--check", action="store_true",
                        help="Compare existing outputs without modifying them")
    args = parser.parse_args()
    images, pal_text, frames = convert(args.source)

    if args.check:
        for name, expected in images.items():
            with Image.open(args.output_dir / name) as actual:
                assert actual.mode == "P" and actual.size == expected.size, name
                assert actual.tobytes() == expected.tobytes(), f"{name}: pixels differ"
                assert actual.getpalette() == expected.getpalette(), f"{name}: palette differs"
                assert actual.info.get("transparency") == 0, f"{name}: transparency differs"
        assert (args.output_dir / "joe.pal").read_text() == pal_text, "joe.pal differs"
        print("PASS: Joe trainer assets reproduce from preserved source")
    else:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for name, indexed in images.items():
            indexed.save(args.output_dir / name, bits=4, optimize=True)
        (args.output_dir / "joe.pal").write_text(pal_text)
        print(f"Wrote front.png, back.png, joe.pal to {args.output_dir}")

    if args.preview:
        preview = Image.new("RGB", (320, 64), (106, 189, 164))
        for i, frame in enumerate(frames):
            preview.paste(frame.convert("RGB"), (i * 64, 0),
                          frame.convert("RGBA").getchannel("A"))
        args.preview.parent.mkdir(parents=True, exist_ok=True)
        preview.resize((1280, 256), Image.Resampling.NEAREST).save(args.preview)


if __name__ == "__main__":
    main()
