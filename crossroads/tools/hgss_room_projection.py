"""Reference collision/prop projection into GBA temple metatiles.

Terrain facts retain provenance. This does not import story scripts or assets.
"""
import json,math
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[2]
FACTS=json.loads((R/'crossroads/hgss/canonical_events/ecruteak-interior-geometry.json').read_text())
ART=json.loads((R/'crossroads/hgss/art/temple/manifest.json').read_text())['specs']
def project(header,theme='wood',bounds=None):
 f=FACTS[header];cw,ch=f['matrix_dimensions'];W,H=cw*32,ch*32;perms=[0x8000]*(W*H)
 for k,c in enumerate(f['chunks']):
  for y in range(32):
   for x in range(32):perms[(k//cw*32+y)*W+k%cw*32+x]=c['permissions'][y*32+x]
 seeds={(e['x'],e['z']) for e in f['warps']};seen=set(seeds);q=deque(seeds)
 while q:
  x,y=q.popleft()
  for a,b in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if not(0<=a<W and 0<=b<H):continue
   behavior=perms[b*W+a]&255
   if behavior in range(56,60):
    dx,dy=[(1,0),(-1,0),(0,-1),(0,1)][behavior-56]
    if (a-x,b-y)!=(dx,dy):continue
    a,b=a+dx,b+dy
    if not(0<=a<W and 0<=b<H):continue
   if (a,b) not in seen and not perms[b*W+a]&0x8000:seen.add((a,b));q.append((a,b))
 if bounds:w,h=bounds
 else:w=min(W,max(x for x,y in seen)+2);h=min(H,max(y for x,y in seen)+2)
 # Keep original coordinate origin; crop only unused southern/eastern cells.
 tiles=[0x400|ART['void']['start']]*(w*h)
 def art(name):return ART.get(name+'_'+theme,ART[name])
 def stamp(name,x,y):
  a=art(name)
  for yy in range(a['height']):
   for xx in range(a['width']):
    X,Y=x+xx,y+yy
    if 0<=X<w and 0<=Y<h:
     collision=tiles[Y*w+X]&0xfc00;tiles[Y*w+X]=collision|a['start']+yy*a['width']+xx
 for y in range(h):
  for x in range(w):
   if (x,y) in seen:tiles[y*w+x]=0x3000|ART[theme]['start']
 # Decorative structure stays visible outside the reachable walking strip.
 # Closed floors inside rails remain drawn but blocked; open joists are distinct.
 if header.startswith('MAP_BELL_TOWER_') and header!='MAP_BELL_TOWER_ROOF':
  for y in range(6,min(27,h)):
   for x in range(5,min(26,w)):
    if (x,y) not in seen:
     a=ART['braces'];tiles[y*w+x]=0x400|(ART[theme]['start'] if not perms[y*W+x]&0x8000 else a['start']+(y%2)*2+x%2)
  for y in [4,5]:
   for x in range(5,min(26,w)):tiles[y*w+x]=0x400|ART['temple_wall']['start']+(y%2)*4+x%4
 # Rear walls and rail footprints are source-derived, never blanket walkable.
 for y in range(h):
  for x in range(w):
   if (x,y) in seen:continue
   if any((a,b) in seen for a,b in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):
    n='rail_h' if (x,y-1) in seen or (x,y+1) in seen else 'rail_v';
    if 'BARRIER' in header:n='temple_wall'
    a=art(n);tiles[y*w+x]=0x400|a['start']+(x%a['width'])+(y%a['height'])*a['width']
 if 'BARRIER' in header:
  for y in range(2):
   for x in range(1,w-2):
    if (x,y) not in seen:tiles[y*w+x]=0x400|ART['temple_wall']['start']+(y%2)*4+x%4
 if header.startswith('MAP_BURNED_TOWER'):
  for y in [4,5]:
   for x in range(5,min(26,w)):tiles[y*w+x]=0x400|ART['burned_wall']['start']+(y%2)*4+x%4
 if header=='MAP_BURNED_TOWER_1F':
  for y in range(10,min(24,h)):
   for x in range(8,min(23,w)):
    if (x,y) not in seen:tiles[y*w+x]=0x400|ART['stone']['start']
 if header=='MAP_BURNED_TOWER_B1F':
  for y in range(7,min(26,h)):
   for x in range(5,min(26,w)):
    if (x,y) not in seen and sum((x+dx,y+dy) in seen for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)])>=2:tiles[y*w+x]=0x400|ART['rubble']['start']
 for k,c in enumerate(f['chunks']):
  for p in c['props']:
   x=int(p['tile_x'])+k%cw*32;y=int(p['tile_z'])+k//cw*32;model=p['model']
   if model in (169,117):stamp('statue',x,y-1)
   elif model==56:stamp('prayer_table',x,math.ceil(p['tile_z'])+k//cw*32)
   elif model in (4,66):stamp('stairs',x,y-1)
   elif model==67:stamp('ladder',x,y-1)
   elif model==65:
    # Compression of DS vertical height; the source base footprint stays blocked.
    stamp('pillar_big',x-1,y-4)
 # Native one-way jump behavior. Geometry is preserved; the runtime test must
 # understand the two-tile GBA jump instead of pretending it is normal walking.
 for y in range(h):
  for x in range(w):
   behavior=perms[y*W+x]&255
   if behavior in range(56,60):tiles[y*w+x]=0x3400|ART[['jump_east','jump_west','jump_north','jump_south'][behavior-56]]['start']
 return dict(width=w,height=h,tiles=tiles,walkable=seen,permissions=perms,source_width=W,stamp=stamp)

def warp_tile(tile):
 variants=json.loads((R/'crossroads/hgss/art/temple/manifest.json').read_text())['warp_variants']
 return 0x3000|variants.get(str(tile&1023),ART['warp']['start'])
