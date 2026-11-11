#!/usr/bin/env python3
"""HGSS Olivine ground plan with explicitly recorded Black Ledger infill.

Preserves map/layout/warp identities. The original four Black Ledger interiors
remain independent of the three canonical HGSS homes and cafe. Source heights
are flattened into GBA terrain; canonical relative entrances retain coordinates.
"""
import argparse,json,struct,copy
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def load(p):return json.loads((R/p).read_text())
DOORS=[(8,23),(8,28),(13,14),(16,33),(29,33),(31,40),(8,40),(45,39),(14,14),(17,23),(31,17),(36,17),(9,33),(23,52),(17,33),(24,52)]
def city_data(with_gym=True):
 f=load('crossroads/hgss/canonical_events/johto-outdoor-geometry.json')['areas']['MAP_OLIVINE'];spec=load('crossroads/hgss/art/olivine/manifest.json')['specs'];w=h=64;t=[0x4c6]*(w*h);perms={}
 for c in f['cells']:
  for y in range(32):
   for x in range(32):
    X,Y=c['x']*32+x,c['y']*32+y;v=c['permissions'][y*32+x];perms[X,Y]=v
    t[Y*w+X]=0x1170 if v&255==21 else 0x4c6 if v&0x8000 and v&255==6 else 0x471 if v&0x8000 else 0x3202 if v&0x600==0x600 else 0x3001
 # Assemble solid cliff faces from native matching pieces instead of a flat
 # repeated rock cap. Source collision remains unchanged.
 for (x,y),v in perms.items():
  if v&0x8000 and v&255==0:
   lower=perms.get((x,y+1),0x8000);left=perms.get((x-1,y),0x8000);right=perms.get((x+1,y),0x8000)
   if not lower&0x8000:t[y*w+x]=0x47c if lower&255==21 else 0x479
   elif not right&0x8000:t[y*w+x]=0x476
   elif not left&0x8000:t[y*w+x]=0x475
 def rect(x,y,ww,hh,v):
  assert 0<=x and 0<=y and x+ww<=w and y+hh<=h
  for Y in range(y,y+hh):t[Y*w+x:Y*w+x+ww]=[v]*ww
 def facade(kind,door):
  a=spec[kind];ox,oy=door[0]-a['door_x'],door[1]-a['door_y']
  # Flat sprites need an unobstructed apron and ground under the roof silhouette.
  rect(ox,oy,a['width'],a['height'],0x3001)
  for y in range(a['height']):
   for x in range(a['width']):
    solid=[x,y] in a['solid'];door=[x,y] in a['doors']
    # The waterfront port stands over sea: thin roof eaves retain surfable
    # water, the actual body/glass/upper door blocks, and both ground-level
    # entrance leaves stay dry. Never turn the whole center into a roof tunnel.
    flags=(0x1400 if solid else 0x3000 if door else 0x1000) if kind=='port' else (0x400 if solid else 0x3000)
    t[(oy+y)*w+ox+x]=flags|a['metatiles'][y*a['width']+x]
  for x,y in a['doors']:rect(ox+x,oy+y+1,1,1,0x3202)
 for x,y,ww,hh in [(14,19,8,7),(28,12,6,8),(34,12,6,8),(6,28,7,7),(13,27,8,8),(27,28,8,7),(41,29,9,11)]:rect(x,y,ww,hh,0x3001)
 for kind,door in [('house',DOORS[9]),('house',DOORS[10]),('house',DOORS[11]),('cafe',DOORS[12]),('center',DOORS[3]),('mart',DOORS[4]),('lighthouse',DOORS[7]),('port',DOORS[13])]:facade(kind,door)
 # DS height is compressed, but its paths, house court, lighthouse cliff and
 # central waterfront axis remain. No rectangles overwrite canonical buildings.
 rect(21,0,5,10,0x3202);rect(21,9,5,30,0x3202)
 rect(7,34,31,3,0x3202);rect(5,39,33,3,0x3202)
 rect(21,42,5,5,0x3202)
 facade('port',DOORS[13])
 # The GBA facade faces south, unlike the DS roof-entry model. A bounded
 # east boardwalk joins its forecourt back to the city without stepping across
 # an active doorway; never cut a passage through the facade walls.
 rect(28,45,2,10,0x3202);rect(22,53,8,2,0x3202)
 rect(29,18,10,2,0x3001);rect(34,20,3,9,0x3202);rect(29,28,8,1,0x3202)
 rect(34,28,4,14,0x3202);rect(38,40,12,3,0x3202)
 # Paint source-specific fence/deck/breakwater materials before the four
 # accepted Black Ledger buildings and all props overwrite their real footprints.
 from hgss_olivine_materials import paint
 paint(t,w,h,perms,spec)
 # Four accepted original interiors survive as small infill plots. Canonical
 # homes are not repurposed as Joe's home or deleted to fit the office.
 source=struct.unpack('<2400H',(R/'data/layouts/SlateportCity/map.bin').read_bytes())
 def native(door,sx,sy,ww,hh,dx):
  x,y=door[0]-dx,door[1]-hh+1
  rect(x-1,y,ww+2,hh+1,0x3202)
  for yy in range(hh):t[(y+yy)*w+x:(y+yy)*w+x+ww]=source[(sy+yy)*40+sx:(sy+yy)*40+sx+ww]
 native(DOORS[0],4,16,4,4,1);native(DOORS[1],4,16,4,4,1)
 native(DOORS[5],2,22,5,5,2);native(DOORS[6],4,16,4,4,1)
 rect(12,24,5,2,0x3202);rect(7,29,5,1,0x3202)
 # Connection apertures use only shared primary terrain within scrolling range.
 # Route39's farm graphics/palette are never borrowed into this city secondary.
 rect(0,34,7,5,0x3001)
 for y in range(h):
  if y not in range(34,39) and y<47:t[y*w]=0x4c6
 for x in range(w):
  if x not in range(21,26):t[x]=0x4c6
  t[63*w+x]=0x1570 # visible sea at the GBA edge; collision prevents out-of-map Surf
 # Make the preserved survey shuttle's arrival a real central landing.
 rect(24,35,1,2,0x3202)
 # Direction/service signs retain existing event IDs/scripts and sit off doors.
 signs=[(7,24),(7,29),(9,14),(14,34),(27,34),(29,41),(7,41),(46,40),(24,42),(28,7),(7,36)]
 for x,y in signs:rect(x,y,1,1,0x403)
 for x,y in [(16,24),(30,18),(35,18),(8,34),(22,53)]:rect(x,y,1,1,0x403)
 # Road seams are General-only. Replacing facade IDs in neighbouring resources
 # would corrupt scrolling before the engine finishes the map transition.
 for y in range(h):
  for x in range(w):
   if y<7 or x<7:
    v=t[y*w+x]
    if v&1023==0x202:t[y*w+x]=(v&~1023)|0x1ff
 # Native full trees in the two small residential courts, roots solid/leaves
 # foreground. The larger source forest uses solid native forest metatiles.
 for ox,oy in [(12,19),(12,27),(39,19)]:
  a=spec['tree']
  for y in range(2):
   for x in range(2):t[(oy+y)*w+ox+x]=a['metatiles'][y*2+x]|(0x3000 if y==0 else 0x400)
 # Canonical harbor terrace furniture. The western parasol shifts three tiles
 # east to keep the preserved Harbor Office approach open.
 a=spec['parasol']
 for ox,oy in [(11,42),(16,42),(32,42)]:
  for y in range(3):
   for x in range(2):t[(oy+y)*w+ox+x]=a['metatiles'][y*2+x]|(0x400 if y==2 else 0x3000)
 # Two actual HGSS moored sailboat models replace the source ship-model
 # collision silhouettes previously misread as chunks of cliff. Preserve the
 # quay seawall at y46; below it the sail/mast hangs above real surfable water,
 # and only the two lower hull rows are solid. The second boat shifts east to
 # retain the GBA terminal's functional east boardwalk.
 a=spec['sailboat'];b=spec['sailboat_paving']
 for ox,oy in [(13,45),(30,45)]:
  for y in range(a['height']):
   for x in range(a['width']):
    X,Y=ox+x,oy+y;i=y*a['width']+x;old=t[Y*w+X]
    if y==0:t[Y*w+X]=b['metatiles'][i]|0x3000
    elif y==1:
     base=old&1023;key=f'{base}:{i}';assert key in a['shore_variants'],('Boat seawall underlay',X,Y,hex(old));t[Y*w+X]=a['shore_variants'][key]|(old&~1023)
    else:t[Y*w+X]=a['metatiles'][i]|(0x1400 if [x,y] in a['solid'] else 0x1000)
 # Colorful source street pennants: five clear road cells between the posts.
 # North arch stays beyond the seven-tile shared-resource buffer; western arch
 # shifts clear of the accepted Black Ledger housing court. No new warp/gate.
 a=spec['pennant_arch']
 for ox,oy in [(20,7),(7,16),(20,28)]:
  for y in range(a['height']):
   for x in range(a['width']):t[(oy+y)*w+ox+x]=a['metatiles'][y*a['width']+x]|(0x400 if [x,y] in a['solid'] else 0x3000)
 raw=struct.pack('<4096H',*t)
 if with_gym:
  from build_eight_gym_integration import overlay
  return overlay('OlivineCity',raw,64,64)
 return raw
def generate(check=False):
 def write(p,b):
  if isinstance(b,str):b=b.encode()
  p=R/p
  if check:assert p.exists() and p.read_bytes()==b,('Regenerate HGSS Olivine',str(p))
  elif not p.exists() or p.read_bytes()!=b:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 def js(p,v):write(p,json.dumps(v,indent=2)+'\n')
 layouts=load('data/layouts/layouts.json');m=load('data/maps/OlivineCity/map.json');l=next(v for v in layouts['layouts'] if v['id']==m['layout']);l.update(width=64,height=64,primary_tileset='gTileset_HgssOlivinePrimary',secondary_tileset='gTileset_HgssOlivineSecondary')
 for i,(x,y) in enumerate(DOORS[:9]):m['warp_events'][i].update(x=x,y=y)
 destinations=['OlivineCity_FishingHouse','OlivineCity_TradeHouse','OlivineCity_SealHouse','OlivineCity_Cafe','OlivineCity_PortTerminal','OlivineCity_PokemonCenter_1F','OlivineCity_PortTerminal']
 for i,n in enumerate(destinations,9):
  inside=load(f'data/maps/{n}/map.json');e=dict(x=DOORS[i][0],y=DOORS[i][1],elevation=0,dest_map=inside['id'],dest_warp_id=str(1 if i==14 else 3 if i==15 else 0))
  if len(m['warp_events'])==i:m['warp_events'].append(e)
  else:m['warp_events'][i]=e
 for e,point in zip(m['bg_events'],[(7,24),(7,29),(9,14),(14,34),(27,34),(29,41),(7,41),(46,40),(24,42),(28,7),(7,36)]):e.update(x=point[0],y=point[1])
 extra=[((16,24),'FishingHouse','FISHING HOUSE'),((30,18),'TradeHouse','NORTH HOUSE'),((35,18),'SealHouse','NORTHEAST HOUSE'),((8,34),'Cafe','OLIVINE CAFE'),((22,53),'Port','OLIVINE PORT TERMINAL')]
 # Appended event IDs; all accepted sign scripts remain intact.
 for point,label,title in extra:
  event=dict(type='sign',x=point[0],y=point[1],elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='Hgss_OlivineSign_'+label)
  found=next((i for i,e in enumerate(m['bg_events']) if e['script']==event['script']),None)
  if found is None:m['bg_events'].append(event)
  else:m['bg_events'][found]=event
 text='@ Generated canonical Olivine plaques. No story or reward grants.\n'
 for point,label,title in extra:text+=f'Hgss_OlivineSign_{label}::\n    msgbox Hgss_OlivineSign_{label}_Text, MSGBOX_SIGN\n    end\nHgss_OlivineSign_{label}_Text:\n    .string "{title}.$"\n'
 write('crossroads/scripts/hgss_olivine_city.inc',text)
 linked=(R/'data/event_scripts.s').read_text();line='\t.include "crossroads/scripts/hgss_olivine_city.inc"'
 if line not in linked:linked+='\n'+line+'\n'
 write('data/event_scripts.s',linked)
 for e,p in zip(m['object_events'],[(17,38),(19,18),(26,36),(28,35),(44,42),(18,25),(22,45)]):e.update(x=p[0],y=p[1])
 m['connections']=[dict(map='MAP_JOHTO_ROUTE39',offset=12,direction='up'),dict(map='MAP_JOHTO_ROUTE40',offset=10,direction='left')]
 for n,d,off in [('JohtoRoute39','down',-12),('JohtoRoute40','right',-10)]:
  a=load(f'data/maps/{n}/map.json')
  from hgss_olivine_connections import layout as seam_layout,tiles as seam_tiles
  al=next(v for v in layouts['layouts'] if v['id']==a['layout']);seam_layout(n,al);write(al['blockdata_filepath'],seam_tiles(n,(R/al['blockdata_filepath']).read_bytes(),al['width'],al['height']))
  next(c for c in a['connections'] if c['direction']==d)['offset']=off;js(f'data/maps/{n}/map.json',a)
 js('data/maps/OlivineCity/map.json',m)
 # The primary seam tile is identical to QA07 neutral paving. Never modify
 # General or expose its south-arrow tile0x24 as an ordinary road.
 from hgss_ecruteak_terrain import neutral_metadata,neutral_graphics
 # Assets own this neutral tile; assert rather than mutate their generated data.
 raw_path='crossroads/hgss/authoring/OlivineCity.bin';write(raw_path,city_data(False))
 gym=load('data/maps/OlivineCity_Gym/map.json');il=next(v for v in layouts['layouts'] if v['id']==gym['layout']);write('crossroads/hgss/authoring/OlivineCity_Gym.bin',(R/il['blockdata_filepath']).read_bytes())
 from build_hgss_olivine_assets import primary_ids
 js('crossroads/hgss/authoring/OlivineCity.json',dict(map=m,layout=dict(l),gym_warp=2,gym_alias=8,interior=gym,raw_path=raw_path,shared_primary_ids=sorted(primary_ids())))
 from build_eight_gym_integration import relocate_layout
 relocate_layout('OlivineCity',l);js('data/layouts/layouts.json',layouts);write(l['border_filepath'],struct.pack('<4H',*([0x1170]*4)));write('data/layouts/OlivineCity/map.bin',city_data())
 heals=load('src/data/heal_locations.json');next(v for v in heals['heal_locations'] if v['id']=='HEAL_LOCATION_OLIVINE_CITY').update(x=16,y=34,respawn_x=8,respawn_y=13);js('src/data/heal_locations.json',heals)
 print('HGSS64x64 Olivine; canonical buildings + four documented original additions; owner review pending')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');generate(p.parse_args().check)
