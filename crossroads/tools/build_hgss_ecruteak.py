#!/usr/bin/env python3
"""Reference-led Ecruteak city authoring. Work-in-progress, not full HGSS acceptance.

Reference: archived HGSS city mosaic1032x785. Projected into64x50 native metatiles.
Existing map/layout/warp indexes retain identities; positions follow the reference.
"""
import json,struct,argparse,copy
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def canonical_positions():
 source=json.loads((R/'crossroads/hgss/canonical_events/075_T27.json').read_text())
 names=['MAP_BURNED_TOWER_1F','MAP_ECRUTEAK_BELL_TOWER_BARRIER_STATION','MAP_ECRUTEAK_SOUTHWEST_HOUSE','MAP_ECRUTEAK_DANCE_THEATER','MAP_ECRUTEAK_GYM','MAP_ECRUTEAK_POKECENTER_1F','MAP_ECRUTEAK_POKEMART']
 positions=[(next(e for e in source['warps'] if e['header']==n)['x']-352,next(e for e in source['warps'] if e['header']==n)['z']-128) for n in names]
 # GBA facade's visible Mart door is its left panel. Keep the building's
 # established footprint; only move its entrance one tile west.
 positions[-1]=(positions[-1][0]-1,positions[-1][1])
 return positions

def city_data(with_gym=True):
 specs=json.loads((R/'crossroads/hgss/art/native-manifest.json').read_text())['specs'];w=h=64;t=[0x3001]*(w*h);pave=0x3000|specs['paving'];earth=0x3000|specs['earth']
 def rect(x,y,ww,hh,v):
  assert 0<=x<x+ww<=w and 0<=y<y+hh<=h,(x,y,ww,hh)
  for yy in range(y,y+hh):t[yy*w+x:yy*w+x+ww]=[v]*ww
 def tree(x,y,autumn=False,overhang=True):
  a=specs['autumn_tree' if autumn else 'tree']
  for yy in range(a['height']):
   for xx in range(2):t[(y+yy)*w+x+xx]=a['start']+yy*2+xx+(0x3000 if yy==0 and overhang else 0x400)
 def building(kind,x,y,open_door=True):
  a=specs[kind]
  for yy in range(a['height']):
   for xx in range(a['width']):
    door=[xx,yy] in a['door_cells']
    blocked=([xx,yy] in a['solid_footprint'] and not door) or (kind=='barrier' and not door) or (door and not open_door)
    t[(y+yy)*w+x+xx]=a['start']+yy*a['width']+xx+(0x400 if blocked else 0x3000)
 # Absolute HGSS event coordinates translated by(-352,-128). This preserves
 # actual relative entrance spacing rather than estimating DS perspective pixels.
 for y in range(0,62,2):
  for x in range(0,64,2):
   if x<17 or x>=60 or y<29 or y>=61:tree(x,min(y,61),y<29,False)
 rect(17,29,26,3,pave);rect(33,26,11,3,pave);rect(6,38,56,3,pave)
 for x in [17,29,40,49,60]:rect(x,31 if x<43 else 38,2,30 if x<43 else 23,pave)
 for y in [48,59]:rect(17,y,45,3,pave)
 # Canonical housing plots: two accessible houses; unused decorative buildings
 # stay closed, not invented generic interiors. Dowsing house awaits its interior.
 houses=[(20,33,False),(32,33,False),(20,42,True),(31,52,True),(51,52,False)]
 for x,y,opened in houses:rect(x-1,y-1,8,7,earth)
 rect(31,42,8,5,earth);rect(42,40,7,8,earth);rect(52,41,7,7,earth)
 rect(21,49,8,9,earth);rect(43,50,7,8,earth)
 # Burned Tower's raised precinct and south stair axis. Actual height/ledge
 # behavior is still pending; the surrounding visual terrain is not final.
 rect(18,17,12,12,0x471);rect(19,17,10,11,pave);rect(23,21,3,9,pave)
 positions=canonical_positions()
 for kind,(dx,dy) in zip(['burned','barrier','house','theater','gym','center','mart'],positions):
  asset=specs[kind];building(kind,dx-asset['door_x'],dy-asset['door_y'])
 rect(44,28,10,5,0x1170);rect(49,33,5,2,0x1170)
 for x,y,opened in houses:
  if (x,y)!=(20,42):building('house',x,y,opened)
 for x,y in [(26,33),(38,33),(26,42),(29,52),(49,52),(58,42)]:tree(x,y)
 # Existing regional destinations retained. Port coordinates now follow the
 # actual HGSS gate positions; adjacent route interiors remain pending.
 rect(0,37,18,3,pave);rect(60,46,4,3,pave);rect(38,59,3,5,pave)
 # Legacy Black Ledger shuttle arrival must remain safe.
 rect(26,27,1,1,pave)
 for x,y in [(26,25),(42,26),(25,46),(43,46),(26,56),(43,56),(55,46),(8,37),(61,49),(39,61),(36,45)]:rect(x,y,1,1,0x403)
 # The map perimeter is solid except the three documented road apertures.
 # Do not expose the full neighboring map width as an accidental crossing.
 for x in range(w):
  t[x]=0x4c6
  if x not in range(38,41):t[(h-1)*w+x]=0x4c6
 for y in range(h):
  if y not in range(37,40):t[y*w]=0x4c6
  if y not in range(46,49):t[y*w+w-1]=0x4c6
 from hgss_connection_buffer import repair
 from build_eight_gym_integration import overlay
 data=repair('EcruteakCity',struct.pack('<'+str(w*h)+'H',*t),w,h,specs)
 return overlay('EcruteakCity',data,w,h) if with_gym else data

def generate(check=False):
 def write(p,b):
  if p.startswith('data/maps/') and p.endswith('/map.json'):
   from build_eight_gym_integration import patch_events
   b=json.dumps(patch_events(p.split('/')[2],json.loads(b)),indent=2)+'\n'
  if isinstance(b,str):b=b.encode()
  p=R/p
  if check:assert p.read_bytes()==b,('Regenerate',p)
  elif not p.exists() or p.read_bytes()!=b:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 def js(p,v):write(p,json.dumps(v,indent=2)+'\n')
 from hgss_ecruteak_terrain import generate as neutral,NEIGHBORS
 neutral(check)
 layouts=json.loads((R/'data/layouts/layouts.json').read_text());l=next(l for l in layouts['layouts'] if l['id']=='LAYOUT_ECRUTEAK_CITY');l.update(width=64,height=64,primary_tileset='gTileset_HgssEcruteakPrimary',secondary_tileset='gTileset_HgssEcruteakSecondary')
 for route in NEIGHBORS:
  layout=json.loads((R/f'data/maps/{route}/map.json').read_text())['layout']
  next(v for v in layouts['layouts'] if v['id']==layout)['primary_tileset']='gTileset_HgssEcruteakBuffer'
 from build_eight_gym_integration import relocate_layout
 relocate_layout('EcruteakCity',l);js('data/layouts/layouts.json',layouts)
 m=json.loads((R/'data/maps/EcruteakCity/map.json').read_text());positions=canonical_positions()
 for e,(x,y) in zip(m['warp_events'],positions):e.update(x=x,y=y)
 # Both visible leaves of the station doorway enter the same room. Append the
 # alias so all existing warp indices and return destinations remain stable.
 alias=dict(m['warp_events'][1],x=39,y=25,dest_warp_id='0')
 if len(m['warp_events'])==7:m['warp_events'].append(alias)
 else:assert len(m['warp_events'])>=8;m['warp_events'][7]=alias
 # Append missing Theater leaf; preserve every historical event index.
 m['warp_events'][3]['dest_warp_id']='1'
 m['warp_events'][1]['dest_warp_id']='2'
 alias=dict(m['warp_events'][3],x=44,y=45,dest_warp_id='0')
 matches=[i for i,e in enumerate(m['warp_events']) if e['dest_map']==alias['dest_map'] and e['x']==44 and e['y']==45]
 if matches:assert matches==[16];m['warp_events'][16]=alias
 else:assert len(m['warp_events'])==16;m['warp_events'].append(alias)
 # Sign/NPC identities and scripts remain stable; only their physical placements
 # follow the new town. Bell sign currently explicitly labels an unfinished approach.
 signpos=[(26,25),(42,26),(25,46),(43,46),(26,56),(43,56),(55,46),(8,37),(61,49),(39,61),(36,45)]
 for e,(x,y) in zip(m['bg_events'],signpos):e.update(x=x,y=y)
 # HGSS has only two enterable homes here. Explain the three preserved closed
 # facades through interaction instead of leaving their visible doors ambiguous.
 private=[dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='Hgss_PrivateResidence') for x,y in [(23,36),(35,36),(54,55)]]
 if len(m['bg_events'])==len(signpos):m['bg_events'].extend(private)
 else:assert m['bg_events'][len(signpos):]==private
 npcpos=[(27,27),(29,34),(26,48),(44,34),(40,43),(52,57)]
 for e,(x,y) in zip(m['object_events'],npcpos):e.update(x=x,y=y)

 for c in m['connections']:
  c['offset']={'left':25,'right':33,'down':25}[c['direction']]
 js('data/maps/EcruteakCity/map.json',m)
 for n,d,off in [('JohtoRoute38','right',-25),('JohtoRoute42','left',-33),('JohtoRoute37','up',-25)]:
  other=json.loads((R/f'data/maps/{n}/map.json').read_text())
  next(c for c in other['connections'] if c['direction']==d)['offset']=off
  js(f'data/maps/{n}/map.json',other)
 heals=json.loads((R/'src/data/heal_locations.json').read_text());next(h for h in heals['heal_locations'] if h['id']=='HEAL_LOCATION_ECRUTEAK_CITY').update(x=45,y=56,respawn_x=8,respawn_y=13);js('src/data/heal_locations.json',heals)
 # Return destinations reference stable warp indices, so reciprocal destination
 # positions need no changes; the native door engine resolves current coordinates.
 # Current authored city is the input to the isolated owner Gym packer. Keep its
 # immutable QA05 baseline unchanged; otherwise a later generator undoes fixes.
 source_layout=dict(l,primary_tileset='gTileset_HgssEcruteakPrimary',secondary_tileset='gTileset_HgssEcruteakSecondary')
 raw_path='crossroads/hgss/authoring/EcruteakCity.bin'
 write(raw_path,city_data(False))
 inside=json.loads((R/'data/maps/EcruteakCity_Gym/map.json').read_text())
 il=next(v for v in layouts['layouts'] if v['id']==inside['layout'])
 write('crossroads/hgss/authoring/EcruteakCity_Gym.bin',(R/il['blockdata_filepath']).read_bytes())
 js('crossroads/hgss/authoring/EcruteakCity.json',dict(map=m,layout=source_layout,gym_warp=4,gym_alias=15,interior=inside,raw_path=raw_path))
 write('data/layouts/EcruteakCity/map.bin',city_data());print('HGSS-directed Ecruteak city generated; owner visual acceptance remains separate.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');generate(p.parse_args().check)
