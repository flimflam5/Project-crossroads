"""Reference-specific city materials; collision permissions are not building types.

HGSS uses the same blocked permission for earth cliffs, picket fences, furniture
and sea boulders. These explicit architectural masks prevent treating all of them
as a generic earth wall. Original BL/genuine facade stamps are applied later.
"""
import collections
TABLES={(x,42) for start in [7,14,29] for x in range(start,start+4)}
def fence_kind(x,y):
 if x==6 and y in [10,20,29]:return 'fence_corner'
 if x==6 and 10<=y<=33 or x==13 and 21<=y<=23:return 'fence_v'
 if y in [10,20,29] and 6<=x<=25:return 'fence_h'
 return None
def obsolete_port_model(perms):
 return {(x,y) for y in range(54,61) for x in range(16,28) if perms[x,y]==0x8000}
def boulder_cells(perms):
 # Eastern isolated breakwater groups, not the attached lighthouse earth cliff.
 remaining={p for p,v in perms.items() if v==0x8000};out=set()
 while remaining:
  p=remaining.pop();seen={p};q=collections.deque([p])
  while q:
   x,y=q.popleft()
   for other in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if other in remaining:remaining.remove(other);seen.add(other);q.append(other)
  if min(x for x,y in seen)>=53 and min(y for x,y in seen)>=18:out.update(seen)
 # Source southern offshore chain; explicit new modeled footprints overlay later.
 out.update(p for p,v in perms.items() if v==0x8000 and p[1]>=47)
 return out-obsolete_port_model(perms)
def paint(t,w,h,perms,spec):
 rocks=boulder_cells(perms);obsolete_port=obsolete_port_model(perms)
 def tile(name):return spec[name]['metatiles'][0]
 for (x,y),source in perms.items():
  old=t[y*w+x];raw=old&~1023;kind=fence_kind(x,y)
  # Dedicated canonical facades already stamped before this pass are protected.
  # New BL facades and all props stamp later. Never paint furniture or a
  # model's obsolete blocked permission over a newer deliberately clear road.
  if old&1023>=512 and old&1023!=0x202:continue
  solid=bool(old&0xc00)
  # The north-entry DS port model was moved for the GBA south-facing facade.
  # Its obsolete solid body is sea, not a new rectangular mass of boulders.
  # Preserve the current door apron/boardwalk and every existing public pier.
  if (x,y) in obsolete_port and solid:t[y*w+x]=0x1170;continue
  if kind and source==0x8000 and solid:t[y*w+x]=raw|tile(kind)
  elif (x,y) in rocks and solid:t[y*w+x]=raw|tile('sea_boulder')
  # The actual public terrace is timber; the existing lower dock remains an
  # explicitly adapted wooden access pier, never a grass island in the sea.
  elif (39<=y<=45 and 5<=x<=37 or y>=47) and old>>12==3 and not old&0xc00:t[y*w+x]=raw|tile('deck')
  if y==46 and source==0x8000 and solid and 5<=x<=37:t[y*w+x]=raw|tile('quay_fence')
 # The old source tables move with the complete native parasol models. Only
 # these12 obsolete furniture blockers open; no true cliff/fence is cleared.
 for x,y in TABLES:t[y*w+x]=0x3000|tile('deck')
 return t

def relocate_layout(name,layout):
 if name=='JohtoRoute40':layout['primary_tileset']='gTileset_HgssOlivineCoastBuffer'
 return layout
