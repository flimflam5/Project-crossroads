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
   if 0<=a<W and 0<=b<H and (a,b) not in seen and not perms[b*W+a]&0x8000:seen.add((a,b));q.append((a,b))
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
 for k,c in enumerate(f['chunks']):
  for p in c['props']:
   x=int(p['tile_x'])+k%cw*32;y=int(p['tile_z'])+k//cw*32;model=p['model']
   if model in (169,117):stamp('statue',x,y-1)
   elif model==56:stamp('prayer_table',x,math.ceil(p['tile_z'])+k//cw*32)
   elif model in (4,66):stamp('stairs',x,y-1)
   elif model==67:stamp('ladder',x,y-1)
   elif model==65:
    # The central pillar's top remains foreground; actual base collision is from HGSS.
    stamp('pillar',x,y-2)
 # Native one-way jump behavior. Geometry is preserved; the runtime test must
 # understand the two-tile GBA jump instead of pretending it is normal walking.
 for x,y in seen:
  if not(0<=x<w and 0<=y<h):continue
  behavior=perms[y*W+x]&255
  if behavior in range(56,60):tiles[y*w+x]=0x3000|ART[['jump_east','jump_west','jump_north','jump_south'][behavior-56]]['start']
 return dict(width=w,height=h,tiles=tiles,walkable=seen,permissions=perms,source_width=W,stamp=stamp)

def warp_tile(tile):
 variants=json.loads((R/'crossroads/hgss/art/temple/manifest.json').read_text())['warp_variants']
 return 0x3000|variants.get(str(tile&1023),ART['warp']['start'])
