"""Shared directed GBA ledge semantics for validators/controller pathfinding.

A ledge is not a walkable tile: enter only in its direction and land two tiles
from the starting position. Collision checks still apply to the landing tile.
"""
JUMPS={0x38:(1,0),0x39:(-1,0),0x3a:(0,-1),0x3b:(0,1)}
def next_position(x,y,dx,dy,behavior_at):
 a,b=x+dx,y+dy;behavior=behavior_at(a,b)
 if behavior in JUMPS:
  if JUMPS[behavior]!=(dx,dy):return None
  a+=dx;b+=dy
 return a,b
