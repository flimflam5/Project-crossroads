#!/usr/bin/env python3
"""Reproducible Route 39 exploration blockout using compatible existing tiles."""
import argparse
import struct
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
WIDTH, HEIGHT = 24, 48


def generate():
    source = struct.unpack('<2400H', (ROOT / 'data/layouts/SlateportCity/map.bin').read_bytes())
    tiles = [0x3001] * (WIDTH * HEIGHT)
    def rect(x, y, w, h, value):
        for row in range(y, y+h):
            tiles[row*WIDTH+x:row*WIDTH+x+w] = [value]*w
    def trees(x, y):
        for row in range(4):
            tiles[(y+row)*WIDTH+x:(y+row)*WIDTH+x+2] = source[(2+row)*40+3:(2+row)*40+5]
    # Bounded countryside. The southern road aligns with city x27..29.
    rect(0, 0, WIDTH, 2, 0x04C6)
    for y in range(0, 48, 4):
        trees(0, y)
        trees(22, y)
    for x in range(2, 22, 2):
        trees(x, 0)
    rect(11, 4, 3, 44, 0x3202)
    rect(7, 20, 10, 3, 0x3202)
    # Meadow clearings and shrubs provide landmarks without HM/encounter gates.
    for x, y in ((4, 9), (18, 8), (4, 30), (18, 33), (17, 25)):
        trees(x, y)
    for x in (4, 6, 8, 16, 18, 20):
        for y in (15, 37):
            rect(x, y, 1, 1, 0x0415)
    for x, y in ((9, 44), (13, 3)):
        rect(x, y, 1, 1, 0x0403)
    return struct.pack('<1152H', *tiles)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    target = ROOT / 'data/layouts/JohtoRoute39/map.bin'
    data = generate()
    if args.check:
        assert target.read_bytes() == data, 'Regenerate Route 39 layout'
        print('Route 39 layout reproducibility: PASS')
    else:
        target.write_bytes(data)
