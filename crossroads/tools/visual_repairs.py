"""Authored repair overlays. Stable dimensions, events, IDs and thresholds.

Only listed maps are redesigned. This is not a region-wide visual acceptance.
"""
import json,struct
from pathlib import Path
R=Path(__file__).resolve().parents[2]
REVIEWED=('EcruteakCity','MahoganyTown','MahoganyTown_Workshop','JohtoRoute38','JohtoRoute39')

def repair(name,data,w,h):
 from hgss_connection_buffer import repair as repair_seam
 if name not in REVIEWED:return repair_seam(name,data,w,h)
 t=list(struct.unpack('<'+str(w*h)+'H',data))
 m=json.loads((R/f'data/maps/{name}/map.json').read_text())
 saved=t[:]
 def rect(x,y,ww,hh,v):
  assert 0<=x<x+ww<=w and 0<=y<y+hh<=h,(name,x,y,ww,hh)
  for yy in range(y,y+hh):t[yy*w+x:yy*w+x+ww]=[v]*ww
 def stamp(x,y,rows):
  for yy,row in enumerate(rows):
   for xx,v in enumerate(row):t[(y+yy)*w+x+xx]=v
 def tree(x,y):
  # Complete native canopy/middle/root assembly. Roots are solid, covered layer;
  # Joe's head in the south apron remains in front of the trunk, not behind it.
  stamp(x,y,[[0x5d4,0x5d5],[0x5dc,0x5dd],[0x7e8,0x7e9]])
 def path(points,width=2):
  for (x,y),(a,b) in zip(points,points[1:]):
   assert x==a or y==b
   rect(min(x,a),min(y,b),abs(a-x)+width,abs(b-y)+width,0x3202)
 def restore(x,y,ww,hh):
  for yy in range(y,y+hh):t[yy*w+x:yy*w+x+ww]=saved[yy*w+x:yy*w+x+ww]
 if name=='EcruteakCity':
  # Keep the town footprint/services, replace the isolated tower strips with
  # separate shared precincts, broad forecourts, side gardens and a cross lane.
  rect(3,2,42,23,0x3001);rect(34,1,7,1,0x3001)
  path([(3,12),(42,12)],3);path([(24,12),(24,25)],3)
  rect(7,4,9,7,0x3202);rect(33,5,10,6,0x3202)
  path([(11,10),(11,12)],2);path([(37,10),(37,12)],2)
  # A shaded approach bends around the theater/residential courts.
  rect(8,19,8,4,0x3202);path([(12,22),(12,26)],2)
  rect(19,19,8,3,0x3202);path([(23,21),(23,26)],2)
  # Northwest memorial grove; northeast temple garden. Deliberate gaps/aisles.
  for x,y in [(3,3),(5,7),(16,3),(16,7),(29,3),(29,7),(43,3),(42,16),(32,17),(16,17),(4,17)]:tree(x,y)
  # Preserve every authored building as a whole; no road is painted through it.
  for x,y,ww,hh in [(9,4,4,4),(36,2,3,6),(10,16,3,3),(20,16,4,3)]:restore(x,y,ww,hh)
  # Restore the southern services and their paths; change only the repeated
  # foliage screens in this reviewed city to complete trees.
  for x,y in [(4,40),(16,40),(29,33)]:
   rect(x,y,2,4,0x3001);tree(x,y+1)
 elif name=='MahoganyTown':
  # Small northern crossroads: compact north street, workshop delivery yard,
  # southern service lane and staggered forest margins rather than a cross grid.
  rect(2,2,w-4,h-4,0x3001)
  path([(0,21),(45,21)],3);path([(23,0),(23,21)],3)
  path([(8,12),(8,15),(24,15)],2)
  path([(21,11),(21,15)],2)
  rect(32,11,10,5,0x3202);path([(35,15),(35,21)],2)
  path([(18,23),(18,35),(35,35),(35,33)],2)
  path([(9,35),(18,35)],2)
  for suffix,(x,y) in json.loads((R/'crossroads/johto/city_sites.json').read_text())[name].items():
   ww,hh=(7,6) if suffix=='Gym' else (4,4);restore(x,y,ww,hh)
  # Local storage yard uses assembled freight stacks, with a clear work aisle.
  s=struct.unpack('<2400H',(R/'data/layouts/SlateportCity/map.bin').read_bytes())
  for yy in range(2):
   for xx in range(3):t[(16+yy)*w+39+xx]=s[(33+yy)*40+3+xx]
  for x,y in [(3,2),(5,4),(11,2),(14,5),(29,3),(39,3),(42,6),(3,27),(3,33),(12,38),(23,38),(39,36),(42,30),(42,25)]:tree(x,y)
  # Replace two rigid edge strips with an irregular woodland silhouette.
  for y in (3,9,15,27,33):tree(0,y);tree(46,y+1)
 elif name in ('JohtoRoute38','JohtoRoute39'):
  # Restore complete trees at all old isolated foliage stamps, with the same
  # southern collision boundary and generous walking aprons.
  sites=[(5,6),(20,19),(26,5),(39,20),(46,3),(56,19),(34,6)] if name.endswith('38') else []
  for x,y in sites:rect(x,y,2,4,0x3001);tree(x,y+1)
  if name.endswith('38'):
   # Two offset meadows joined by a bend, with a clear direct east approach.
   rect(14,12,37,3,0x3001)
   path([(12,14),(24,14),(24,10),(36,10),(36,13),(62,13)],2)
   # Preserve trainer sight/interaction aprons and approved grass islands.
   for x,y in [(17,5),(21,5),(29,20),(43,21),(51,5)]:tree(x,y)
   path([(12,14),(12,26)],2)
  else:
   # Farm lane and open pasture with split approaches around planted groves.
   for x,y in [(18,4),(18,9),(3,28),(5,32),(18,36),(20,39)]:tree(x,y)
   path([(12,1),(12,22),(14,22),(14,37),(12,37),(12,46)],2)
   path([(6,8),(6,12),(12,12)],2);path([(5,18),(5,21),(12,21)],2)
 elif name=='MahoganyTown_Workshop':
  # 14x12 retained for save coordinates. Assemble native furniture pieces;
  # no lone chair/table/wall fragments. Storage, two benches, sink and work aisle.
  t=[0x3223]*(w*h)
  rect(0,0,w,1,0x0605);rect(0,1,w,1,0x060d)
  rect(0,2,1,h-2,0x0601);rect(w-1,2,1,h-2,0x0601);rect(0,h-1,w,1,0x0601)
  stamp(1,0,[[0x0779,0x077a],[0x0781,0x0782],[0x3389,0x338a]])
  stamp(4,0,[[0x0766,0x0767],[0x076e,0x076f],[0x3376,0x3377]])
  stamp(8,0,[[0x0738,0x0738],[0x0756,0x0757],[0x335e,0x335f]])
  # Two full 2x2 work tables, intentionally separated from the door/guide.
  for x,y in [(8,4),(2,7)]:stamp(x,y,[[0x376a,0x376b],[0x3772,0x3773]])
  # Paired storage cabinets at the east wall, with a readable notes shelf.
  stamp(11,0,[[0x0779,0x077a],[0x0781,0x0782],[0x3389,0x338a]])
  stamp(10,7,[[0x0779,0x077a],[0x0781,0x0782],[0x3389,0x338a]])
 # Preserve all event anchors/arrival tiles, including old service/travel contracts.
 # Solid sign tiles stay solid, doors keep native behavior/elevation. Actors remain
 # on clear floor with a reachable interaction apron; this never carves buildings.
 for e in m['warp_events']+m['bg_events']:
  x,y=e['x'],e['y'];t[y*w+x]=0x3389 if name=='MahoganyTown_Workshop' and e in m['bg_events'] else saved[y*w+x]
 for e in m['object_events']:
  x,y=e['x'],e['y'];t[y*w+x]=0x3223 if name.endswith('Workshop') else 0x3001
 return repair_seam(name,struct.pack('<'+str(w*h)+'H',*t),w,h)
