#!/usr/bin/env python3
"""Reproducible connected Route 38/Ecruteak exploration foundation.

Existing compatible Emerald metatiles are temporary art, not finished Johto assets.
"""
import argparse
import struct
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]


class Canvas:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.tiles = [0x3001] * (width * height)
        self.source = struct.unpack('<2400H', (ROOT/'data/layouts/SlateportCity/map.bin').read_bytes())

    def rect(self, x, y, w, h, value):
        assert 0 <= x <= x+w <= self.width and 0 <= y <= y+h <= self.height
        for row in range(y,y+h):
            self.tiles[row*self.width+x:row*self.width+x+w] = [value]*w

    def stamp(self, sx, sy, w, h, x, y):
        assert 0 <= x <= x+w <= self.width and 0 <= y <= y+h <= self.height
        for row in range(h):
            self.tiles[(y+row)*self.width+x:(y+row)*self.width+x+w] = self.source[(sy+row)*40+sx:(sy+row)*40+sx+w]

    def tree(self, x, y):
        self.stamp(3,2,2,4,x,y)

    def bounds(self):
        self.rect(0,0,self.width,2,0x04C6)
        self.rect(0,self.height-2,self.width,2,0x04C6)
        for x in range(0,self.width,2):
            self.tree(x,0)
            self.tree(x,self.height-4)
        for y in range(0,self.height,4):
            self.tree(0,y)
            self.tree(self.width-2,y)

    def packed(self):
        return struct.pack(f'<{self.width*self.height}H',*self.tiles)


def generate():
    route=Canvas(64,28)
    route.bounds()
    # Route 39 joins from the south-west; the road turns east toward Ecruteak.
    route.rect(11,12,3,16,0x3202)
    route.rect(11,12,53,3,0x3202)
    # Clearings, tree islands and a small northern pond give orientation landmarks.
    for x,y in [(5,6),(20,19),(26,5),(39,20),(46,3),(56,19),(34,6)]:
        route.tree(x,y)
    route.rect(16,4,7,4,route.source[39])
    for x in (7,18,25,34,42,53,58):
        route.rect(x,17,1,1,0x0415)
    for x,y in [(10,23),(59,11)]:
        route.rect(x,y,1,1,0x0403)

    city=Canvas(48,48)
    city.bounds()
    for y in (12,26,38):
        city.rect(2,y,44,3,0x3202)
    city.rect(24,10,3,34,0x3202)
    # Western border is a real Route 38 seam; the other exits remain closed.
    city.rect(0,26,48,3,0x3202)
    # Landmark footprints: Burned Tower NW, Bell Tower NE, Gym SW.
    # Existing gym/house art deliberately remains a temporary exterior blockout.
    city.stamp(25,7,7,6,8,2)   # Burned Tower door 11,7
    city.stamp(25,7,7,6,34,2)  # Bell Tower door 37,7
    city.stamp(4,16,4,4,10,15) # residence door 11,18
    city.stamp(4,16,4,4,21,15) # theater door 22,18
    city.stamp(25,7,7,6,7,31)  # Gym door 10,36
    city.stamp(18,16,4,4,20,31)# Center door 21,34
    city.stamp(12,23,4,4,34,31)# Mart door 35,34
    for x,y,length in [(11,8,4),(37,8,4),(11,19,7),(22,19,7),(10,37,1),(21,35,3),(35,35,3)]:
        city.rect(x,y,2,length,0x3202)
    city.rect(19,3,10,6,city.source[39])
    city.rect(33,41,8,3,city.source[39])
    for x,y in [(4,16),(16,17),(30,17),(42,19),(4,40),(16,40),(29,33)]:
        city.tree(x,y)
    for x,y in [(9,8),(35,8),(9,19),(20,19),(8,37),(19,35),(33,35),(4,25),(44,27),(24,44),(27,25)]:
        city.rect(x,y,1,1,0x0403)
    for x,y in [(6,11),(17,24),(30,25),(43,36),(28,39)]:
        city.rect(x,y,1,1,0x0415)
    return {'JohtoRoute38':route.packed(),'EcruteakCity':city.packed()}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    for name,data in generate().items():
        path=ROOT/f'data/layouts/{name}/map.bin'
        if args.check:
            assert path.read_bytes()==data, f'Regenerate {name}'
        else:
            path.write_bytes(data)
    if args.check:
        print('Route 38 and Ecruteak layout reproducibility: PASS')
