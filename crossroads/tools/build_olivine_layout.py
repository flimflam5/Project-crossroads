#!/usr/bin/env python3
"""Author the Olivine foundation from existing, compatible Emerald metatiles.

No external art dependency. Source rectangles preserve door behaviors and collision.
Run after editing this file; --check detects an out-of-date map.bin.
This is a temporary city blockout, not a reproduction of final Johto geography.
"""
import argparse
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WIDTH = HEIGHT = 48


def generate():
    source = struct.unpack('<2400H', (ROOT / 'data/layouts/SlateportCity/map.bin').read_bytes())
    tiles = [0x3001] * (WIDTH * HEIGHT)  # passable grass, elevation 3

    def rect(x, y, w, h, value):
        for row in range(y, y + h):
            tiles[row * WIDTH + x:row * WIDTH + x + w] = [value] * w

    def stamp(sx, sy, w, h, dx, dy):
        for row in range(h):
            tiles[(dy + row) * WIDTH + dx:(dy + row) * WIDTH + dx + w] = source[(sy + row) * 40 + sx:(sy + row) * 40 + sx + w]

    # Western sea, southern waterfront, and a bounded north/east city edge.
    water = source[0 * 40 + 39]
    rect(0, 0, 6, HEIGHT, water)
    rect(0, 39, WIDTH, 9, water)
    # Quay walls keep this exploration slice enclosed, even with Surf unlocked.
    rect(6, 0, 1, 39, source[23 * 40 + 25])
    rect(7, 0, 41, 2, 0x04C6)
    rect(46, 0, 2, 39, 0x04C6)
    rect(7, 38, 39, 1, source[47 * 40 + 27])
    # Three east-west streets and a central spine. No HM or badge gates.
    for y in (12, 24, 35):
        rect(7, y, 39, 3, 0x3202)
    rect(27, 2, 3, 36, 0x3202)
    # Residential north-west, services centrally, gym in the north-east.
    stamp(4, 16, 4, 4, 10, 6)   # Joe's residence: door (11,9)
    stamp(4, 16, 4, 4, 20, 6)   # neighbor: door (21,9)
    stamp(25, 7, 7, 6, 35, 4)   # gym placeholder: door (38,9)
    stamp(18, 16, 4, 4, 10, 18) # Pokemon Center: door (11,21)
    stamp(12, 23, 4, 4, 21, 18) # Mart: door (22,21)
    stamp(2, 22, 5, 5, 35, 17)  # Silph office: door (37,21)
    stamp(4, 16, 4, 4, 11, 29)  # harbor office: door (12,32)
    # Short, safe paths connect every threshold to the street network.
    for x, y, length in ((11, 10, 2), (21, 10, 2), (38, 10, 2),
                          (11, 22, 2), (22, 22, 2), (37, 22, 2), (12, 33, 2)):
        rect(x, y, 2, length, 0x3202)
    # Lighthouse footprint and promenade. The small beacon is temporary art.
    rect(34, 29, 10, 6, 0x3202)
    stamp(32, 51, 4, 4, 37, 29)
    # Cargo quay and two piers, bounded with solid railings.
    rect(18, 29, 12, 6, 0x3202)
    for x in (18, 27):
        rect(x, 38, 5, 6, 0x3202)
        rect(x, 38, 1, 6, 0x064D)
        rect(x + 4, 38, 1, 6, 0x064D)
        rect(x, 43, 5, 1, 0x064D)
    # Visible signs, shrubs, and freight stacks, all solid.
    for x, y in ((9, 10), (20, 10), (36, 10), (9, 22), (20, 22),
                 (35, 22), (10, 33), (36, 33), (26, 26), (25, 3)):
        rect(x, y, 1, 1, 0x0403)
    for x in (8, 16, 25, 33, 43):
        for y in (5, 16, 28):
            rect(x, y, 1, 1, 0x0415)
    # Tree screens break up the blocks without narrowing access paths.
    for x in range(7, 27, 2):
        stamp(3, 2, 2, 4, x, 0)
    for y in range(0, 36, 4):
        stamp(3, 2, 2, 4, 46, y)
    for x, y in ((16, 6), (30, 17), (8, 28), (42, 18)):
        stamp(3, 2, 2, 4, x, y)
    for x, y in ((17, 11), (23, 11), (15, 23), (24, 23), (42, 27)):
        rect(x, y, 2, 1, 0x0404)
    stamp(3, 33, 3, 2, 19, 30)
    stamp(3, 33, 3, 2, 24, 30)
    return struct.pack('<2304H', *tiles)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    target = ROOT / 'data/layouts/OlivineCity/map.bin'
    data = generate()
    if args.check:
        if target.read_bytes() != data:
            raise SystemExit('Olivine layout differs from its authoring script')
        print('Olivine layout reproducibility: PASS')
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
