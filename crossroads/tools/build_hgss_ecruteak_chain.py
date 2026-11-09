#!/usr/bin/env python3
"""Append the reference-backed Station/corridor/Trail chain; retain Bell IDs.

Verified: actual HGSS entrance/stair coordinates and graph. Furnishing/terrain
conversion remains subject to detailed visual comparison; never claims full1:1.
"""
import json,struct,argparse,copy
from pathlib import Path
R=Path(__file__).resolve().parents[2]
AREAS=['EcruteakCity_BarrierStation','EcruteakCity_BarrierCorridor','BellchimeTrail']
MID={AREAS[0]:'MAP_ECRUTEAK_CITY_BARRIER_STATION',AREAS[1]:'MAP_ECRUTEAK_CITY_BARRIER_CORRIDOR',AREAS[2]:'MAP_BELLCHIME_TRAIL'}
LID={n:'LAYOUT_'+MID[n][4:] for n in AREAS}

def generate(check=False):
 def load(p):return json.loads((R/p).read_text())
 def write(p,b):
  if isinstance(b,str):b=b.encode()
  p=R/p
  if check:assert p.exists() and p.read_bytes()==b,('Regenerate HGSS chain',str(p))
  elif not p.exists() or p.read_bytes()!=b:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 def js(p,v):write(p,json.dumps(v,indent=2)+'\n')
 # Dedicated warm timber palette; all shared assets/IDs stay untouched.
 generic=R/'data/tilesets/secondary/generic_building'
 for i in range(16):
  data=(generic/f'palettes/{i:02}.pal').read_bytes()
  if i==6:
   colors=[tuple(map(int,l.split())) for l in data.decode().splitlines()[3:]];out=[]
   for r,g,b in colors:
    v=.3*r+.59*g+.11*b;out.append((min(255,int(v*.75+18)),min(255,int(v*.58+12)),min(255,int(v*.43+8))))
   data=('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in out)+'\n').encode()
  write(f'data/tilesets/secondary/hgss_temple/palettes/{i:02}.pal',data)
 sizes={AREAS[0]:(20,12),AREAS[1]:(10,22),AREAS[2]:(64,36)};maps={};tiles={}
 def rect(n,x,y,w,h,v):
  W,H=sizes[n];assert 0<=x<x+w<=W and 0<=y<y+h<=H,(n,x,y,w,h)
  for yy in range(y,y+h):tiles[n][yy*W+x:yy*W+x+w]=[v]*w
 def stamp(n,x,y,rows):
  for yy,row in enumerate(rows):
   for xx,v in enumerate(row):rect(n,x+xx,y+yy,1,1,v)
 def warp(x,y,dest,idx):return dict(x=x,y=y,elevation=0,dest_map=dest,dest_warp_id=str(idx))
 def actor(x,y):return dict(graphics_id='OBJ_EVENT_GFX_OLD_MAN',x=x,y=y,elevation=3,movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script='Hgss_TempleCaretaker',flag='0')
 for n in AREAS:
  outdoor=n==AREAS[2];w,h=sizes[n]
  maps[n]=dict(id=MID[n],name=n,layout=LID[n],music='MUS_LILYCOVE',region='REGION_HOENN',region_map_section='MAPSEC_ECRUTEAK_CITY',requires_flash=False,weather='WEATHER_SUNNY' if outdoor else 'WEATHER_NONE',map_type='MAP_TYPE_ROUTE' if outdoor else 'MAP_TYPE_INDOOR',allow_cycling=False,allow_escaping=False,allow_running=True,show_map_name=outdoor,battle_scene='MAP_BATTLE_SCENE_NORMAL',connections=None,object_events=[],warp_events=[],coord_events=[],bg_events=[])
  tiles[n]=[0x601]*(w*h) if not outdoor else [0x3001]*(w*h)
 # Station: actual stairs15,3, entrance9,11 and caretaker coordinates.
 n=AREAS[0];rect(n,1,2,18,9,0x3223);rect(n,1,0,18,1,0x605);rect(n,1,1,18,1,0x60d)
 for x in [2,8]:stamp(n,x,0,[[0x779,0x77a],[0x781,0x782],[0x3389,0x338a]])
 for x,y in [(3,7),(11,8)]:stamp(n,x,y,[[0x376a,0x376b],[0x3772,0x3773]])
 maps[n]['object_events']=[actor(15,7),actor(9,2),actor(3,2)]
 maps[n]['warp_events']=[warp(9,11,'MAP_ECRUTEAK_CITY',1),warp(15,3,MID[AREAS[1]],0)]
 rect(n,9,11,1,1,0x208);rect(n,15,3,1,1,0x33fc)
 # Narrow returnable passage; source-confirmed endpoints, no new progress gates.
 n=AREAS[1];rect(n,2,17,5,3,0x3223);rect(n,5,3,2,16,0x3223)
 maps[n]['warp_events']=[warp(3,19,MID[AREAS[0]],1),warp(6,3,MID[AREAS[2]],0)]
 rect(n,3,19,1,1,0x33fd);rect(n,6,3,1,1,0x33fc)
 # Trail coordinates translated south four tiles to contain the tall2D tower.
 n=AREAS[2];a=load('crossroads/hgss/art/bell-native-manifest.json')['specs'];w,h=sizes[n];leaf=0x3000|a['leaf_ground'];pave=0x3000|a['paving'];tree=a['autumn_tree']
 rect(n,0,0,w,h,leaf)
 for y in range(0,h-2,2):
  for x in range(0,w,2):
   for yy in range(3):
    for xx in range(2):rect(n,x+xx,y+yy,1,1,tree['start']+yy*2+xx+0x400)
 def path(points):
  for (x,y),(u,v) in zip(points,points[1:]):
   assert x==u or y==v;rect(n,min(x,u),min(y,v),abs(x-u)+2,abs(y-v)+2,pave)
 path([(9,15),(15,15),(15,12),(27,12),(27,16),(32,16),(32,21),(37,21)])
 # Exact canonical tower door37,16 plus4; station lower warp is a safe GBA
 # arrival tile, avoiding immediate re-entry through a vertically paired doorway.
 for kind,x,y in [('trail_station',1,10),('bell',34,2)]:
  s=a[kind]
  for yy in range(s['height']):
   for xx in range(s['width']):
    opened= (xx,yy)==(s['door_x'],s['door_y'])
    rect(n,x+xx,y+yy,1,1,s['start']+yy*s['width']+xx+(0x3000 if opened else 0x400))
 rect(n,9,15,2,2,pave);rect(n,36,21,3,2,pave)
 maps[n]['warp_events']=[warp(9,14,MID[AREAS[1]],1),warp(37,20,'MAP_ECRUTEAK_CITY_BELL_TOWER',0)]
 # Keep the front approach clear and readable; no legendary/story triggers.
 rect(n,35,22,1,1,0x403);maps[n]['bg_events']=[dict(type='sign',x=35,y=22,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='Hgss_BellTrailSign')]
 layouts=load('data/layouts/layouts.json');byid={l['id']:l for l in layouts['layouts']}
 groups=load('data/maps/map_groups.json');group=groups['gMapGroup_CrossroadsJohtoExpansion'];manifest=load('crossroads/johto/manifest.json');plans={p['name']:p for p in manifest['planned']}
 for n in AREAS:
  w,h=sizes[n];outdoor=n==AREAS[2];l=dict(id=LID[n],name=n+'_Layout',width=w,height=h,primary_tileset='gTileset_HgssBellPrimary' if outdoor else 'gTileset_Building',secondary_tileset='gTileset_HgssBellSecondary' if outdoor else 'gTileset_HgssTemple',border_filepath=f'data/layouts/{n}/border.bin',blockdata_filepath=f'data/layouts/{n}/map.bin',layout_version='emerald')
  if LID[n] not in byid:layouts['layouts'].append(l)
  else:
   assert byid[LID[n]]['id']==l['id'] and byid[LID[n]]['name']==l['name']
   byid[LID[n]].clear();byid[LID[n]].update(l) # Author dimensions without renumbering IDs
  if n not in group:group.append(n)
  assert group.index(n)<127,'Reserved dynamic warp number127'
  js(f'data/maps/{n}/map.json',maps[n]);write(f'data/maps/{n}/scripts.inc',f'{n}_MapScripts::\n    .byte 0\n');write(l['blockdata_filepath'],struct.pack('<'+str(w*h)+'H',*tiles[n]));write(l['border_filepath'],struct.pack('<4H',*([0x4c6 if outdoor else 0x601]*4)))
  if n not in plans:manifest['planned'].append(dict(name=n,kind='hgss',parent='EcruteakCity',cluster='west',status='implemented-reference-review-pending'))
 js('data/layouts/layouts.json',layouts);js('data/maps/map_groups.json',groups);js('crossroads/johto/manifest.json',manifest)
 city=load('data/maps/EcruteakCity/map.json');city['warp_events'][1].update(dest_map=MID[AREAS[0]],dest_warp_id='0');js('data/maps/EcruteakCity/map.json',city)
 bell=load('data/maps/EcruteakCity_BellTower/map.json')
 for e in bell['warp_events'][:2]:e.update(dest_map=MID[AREAS[2]],dest_warp_id='1')
 js('data/maps/EcruteakCity_BellTower/map.json',bell)
 inc=(R/'data/event_scripts.s').read_text()
 for n in AREAS:
  entry=f'\t.include "data/maps/{n}/scripts.inc"'
  if entry not in inc:inc+='\n'+entry+'\n'
 entry='\t.include "crossroads/scripts/hgss_ecruteak.inc"'
 if entry not in inc:inc+='\n'+entry+'\n'
 write('data/event_scripts.s',inc)
 write('crossroads/scripts/hgss_ecruteak.inc','''@ HGSS reconstruction: ordinary wayfinding only. No flags, gifts or battles.
Hgss_TempleCaretaker::
    msgbox Hgss_TempleText, MSGBOX_NPC
    end
Hgss_TempleText:
    .string "Please keep the steps clear.\\nThe corridor leads to BELLCHIME TRAIL.$"
Hgss_BellTrailSign::
    msgbox Hgss_BellTrailText, MSGBOX_SIGN
    end
Hgss_BellTrailText:
    .string "BELL TOWER\\nReturn west through BELLCHIME TRAIL.$"
''')
 print('Station/corridor/Bellchime Trail registered; existing Bell floor IDs/stairs retained. Full visual reference review pending.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');generate(p.parse_args().check)
