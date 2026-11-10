#!/usr/bin/env python3
"""Append authored regional clusters; keep the accepted 37-map foundation intact."""
import argparse,copy,json,re,struct,textwrap,hashlib
from pathlib import Path
from johto_world_spec import *
R=Path(__file__).resolve().parents[2]
def load(p):return json.loads((R/p).read_text())
def write(p,b):
 p=R/p;p.parent.mkdir(parents=True,exist_ok=True)
 if isinstance(b,str):b=b.encode()
 if not p.exists() or p.read_bytes()!=b:p.write_bytes(b)
def js(p,v):write(p,json.dumps(v,indent=2)+'\n')
def sym(n):return re.sub(r'([a-z0-9])([A-Z])',r'\1_\2',n).upper()
def sid(n):
 if n.startswith('JohtoRoute'):return 'MAPSEC_JOHTO_ROUTE_'+n[10:]
 return 'MAPSEC_'+sym(n)
def mid(n):return 'MAP_'+sym(n)
def script(n):return 'Johto_'+n

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--through',choices=CLUSTERS,default='west');ap.add_argument('--check',action='store_true');args=ap.parse_args()
 ambient=load('crossroads/johto/ambient.json');city_sites=load('crossroads/johto/city_sites.json')
 manifest=load('crossroads/johto/manifest.json');plans=manifest['planned'];selected=[p for p in plans if CLUSTERS.index(p['cluster'])<=CLUSTERS.index(args.through)]
 # --check runs the deterministic writer against an in-memory file comparison.
 global write
 realwrite=write
 if args.check:
  def compare(p,b):
   if isinstance(b,str):b=b.encode()
   assert (R/p).read_bytes()==b,('Regenerate',p)
  write=compare
 groups=load('data/maps/map_groups.json');old=groups['gMapGroup_CrossroadsOlivine']+groups.get('gMapGroup_CrossroadsJohtoExpansion',[]);names=[p['name'] for p in manifest['existing']]+[p['name'] for p in selected]
 assert old==names[:len(old)],'Never discard newer maps/IDs when selecting an earlier checkpoint'
 layouts=load('data/layouts/layouts.json');bylayout={l['id']:l for l in layouts['layouts']}
 service_templates=load('crossroads/hgss/contracts/ecruteak-rooms-qa04.json')
 existing={n:load(f'data/maps/{n}/map.json') for n in names[:37]};maps=copy.deepcopy(existing);tiles={};sizes={};meta={};sections={};protected={}
 source=struct.unpack('<2400H',(R/'data/layouts/SlateportCity/map.bin').read_bytes())
 oldbytes={n:(R/bylayout[m['layout']]['blockdata_filepath']).read_bytes() for n,m in existing.items()}
 def obj(x,y,label,gfx='MAN_1',local=None):
  d=dict(graphics_id='OBJ_EVENT_GFX_'+gfx,x=x,y=y,elevation=3,movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script=label,flag='0')
  if local:d['local_id']=local
  return d
 def sign(m,x,y,label):m['bg_events'].append(dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=label))
 scripts=[]
 def say(label,text,kind='NPC'):
  words=textwrap.wrap(text,31,break_long_words=False,break_on_hyphens=False);s=''
  for i,line in enumerate(words):s+=('\\p' if i and i%2==0 else '\\n' if i else '')+line
  scripts.append(f'{label}::\n    msgbox {label}_Text, MSGBOX_{kind}\n    end\n{label}_Text:\n    .string "{s}$"\n')
 def rect(n,x,y,w,h,t):
  W,H=sizes[n];assert x>=0 and y>=0 and x+w<=W and y+h<=H,(n,x,y,w,h)
  for yy in range(y,y+h):tiles[n][yy*W+x:yy*W+x+w]=[t]*w
 def stamp(n,sx,sy,w,h,x,y):
  W,H=sizes[n]
  for yy in range(h):tiles[n][(y+yy)*W+x:(y+yy)*W+x+w]=source[(sy+yy)*40+sx:(sy+yy)*40+sx+w]
 def roadrect(n,x,y,w,h,value):
  for yy in range(y,y+h):
   for xx in range(x,x+w):
    if (xx,yy) not in protected.get(n,set()):tiles[n][yy*sizes[n][0]+xx]=value
 def road(n,a,b,value=0x3202,width=3):
  x,y=a;xx,yy=b
  for X in range(min(x,xx),max(x,xx)+1):roadrect(n,max(0,min(sizes[n][0]-width,X-width//2)),max(0,min(sizes[n][1]-width,y-width//2)),width,width,value)
  for Y in range(min(y,yy),max(y,yy)+1):roadrect(n,max(0,min(sizes[n][0]-width,xx-width//2)),max(0,min(sizes[n][1]-width,Y-width//2)),width,width,value)
 def warp(a,x,y,b,u,v,at=None,bt=None):
  ia=len(maps[a]['warp_events']);ib=len(maps[b]['warp_events'])
  maps[a]['warp_events'].append(dict(x=x,y=y,elevation=0,dest_map=maps[b]['id'],dest_warp_id=str(ib)))
  maps[b]['warp_events'].append(dict(x=u,y=v,elevation=0,dest_map=maps[a]['id'],dest_warp_id=str(ia)))
  if at is not None:rect(a,x,y,1,1,at)
  if bt is not None:rect(b,u,v,1,1,bt)
  return ia,ib
 def addlayout(n,w,h,primary,secondary,data,border):
  lid='LAYOUT_'+sym(n);l=dict(id=lid,name=n+'_Layout',width=w,height=h,primary_tileset=primary,secondary_tileset=secondary,border_filepath=f'data/layouts/{n}/border.bin',blockdata_filepath=f'data/layouts/{n}/map.bin',layout_version='emerald')
  if lid not in bylayout:layouts['layouts'].append(l);bylayout[lid]=l
  elif bylayout[lid]!=l:
   # Only newly authored layouts pass here; their numeric IDs remain fixed.
   bylayout[lid].clear();bylayout[lid].update(l)
  tiles[n]=data;sizes[n]=(w,h);write(l['border_filepath'],struct.pack('<4H',*([border]*4)));return lid
 for n,m in existing.items():
  l=bylayout[m['layout']];sizes[n]=(l['width'],l['height']);tiles[n]=list(struct.unpack('<'+str(l['width']*l['height'])+'H',oldbytes[n]));sections[n]=m['region_map_section']
 for p in selected:
  n=p['name'];parent=p.get('parent');kind=p['kind'];c=p['cluster'];section=parent or n
  if kind=='hgss':
   m=load(f'data/maps/{n}/map.json');l=bylayout[m['layout']];maps[n]=m;sizes[n]=(l['width'],l['height']);tiles[n]=list(struct.unpack('<'+str(l['width']*l['height'])+'H',(R/l['blockdata_filepath']).read_bytes()));meta[n]=dict(kind='hgss',outdoor=n=='BellchimeTrail',parent=parent,theme='hgss',floor=0x3223);sections[n]=m['region_map_section'];continue
  if kind in ['cave','tower','ruins','well','ice','shrine','islandcave','falls','gate'] and re.search(r'_\d+F$',n):section=n.rsplit('_',1)[0]
  if section=='AlphChambers':section='RuinsOfAlph'
  if section in ['CliffCave','CliffEdgeGate','SafariZoneGate','SafariWetlands','SafariReception']:section='CianwoodCity'
  sec=sid(section);sections[n]=sec
  theme='';w,h=14,12;primary='gTileset_Building';secondary='gTileset_WesternInteriors';floor=0x3223;border=0x0601
  if n in CITIES:
   theme=CITIES[n][3];w,h=(60,56) if n=='GoldenrodCity' else (48,44);primary='gTileset_General';secondary='gTileset_WesternCity';floor=0x3001;border=0x4c6
  elif n.startswith('JohtoRoute'):
   _,pos,theme,(w,h)=ROUTES[int(n[10:])];primary='gTileset_General';secondary='gTileset_WesternCity';floor=0x1170 if theme in ['sea','islands'] else 0x3001;border=0x4c6
  elif any(n==s[0] for s in LANDMARKS):
   _,label,_,theme,(w,h),pos=next(s for s in LANDMARKS if s[0]==n);primary='gTileset_General';secondary='gTileset_WesternCity';floor=0x3001;border=0x4c6
  elif re.search(r'_\d+F$',n) and kind!='service':
   theme=kind;w,h=28,22
   if kind not in ['tower','shrine','gate']:primary='gTileset_General';secondary='gTileset_Cave';floor=0x3201;border=0x0611
  else:
   theme=n.split('_')[-1].lower()
   if n in ['NewBarkTown_Gym','CherrygroveCity_Gym']:theme='communityhall'
   if theme=='gym':w,h=18,20
   if n in ['GoldenrodDepartmentStore','VioletAcademy']:w,h=20,16
   if n=='GoldenrodRadioLobby':w,h=20,14
   if n=='GoldenrodUnderground':w,h=28,12
  isout=n in CITIES or n.startswith('JohtoRoute') or any(n==s[0] for s in LANDMARKS)
  m=dict(id=mid(n),name=n,layout='',music=('MUS_ROUTE119' if 'Route' in n else 'MUS_PETALBURG_WOODS' if not isout else 'MUS_LILYCOVE'),region='REGION_HOENN',region_map_section=sec,requires_flash=False,weather='WEATHER_RAIN' if n=='JohtoRoute33' else 'WEATHER_NONE' if not isout else 'WEATHER_SUNNY',map_type='MAP_TYPE_CITY' if n in CITIES else 'MAP_TYPE_ROUTE' if isout else 'MAP_TYPE_UNDERGROUND' if primary=='gTileset_General' else 'MAP_TYPE_INDOOR',allow_cycling=isout,allow_escaping=False,allow_running=True,show_map_name=isout or kind in ['cave','ice','tower'],battle_scene='MAP_BATTLE_SCENE_NORMAL',connections=None,object_events=[],warp_events=[],coord_events=[],bg_events=[])
  if not isout and primary=='gTileset_Building':m['music']='MUS_GYM' if theme=='gym' else 'MUS_LITTLEROOT'
  maps[n]=m;meta[n]=dict(theme=theme,kind=kind,outdoor=isout,parent=parent,floor=floor)
  if kind=='service':
   base=service_templates['EcruteakCity_PokemonCenter_1F' if 'PokemonCenter' in n else 'EcruteakCity_Mart'];m['layout']=base['layout'];l=bylayout[m['layout']];sizes[n]=(l['width'],l['height']);tiles[n]=list(struct.unpack('<'+str(l['width']*l['height'])+'H',(R/l['blockdata_filepath']).read_bytes()));m['music']='MUS_POKE_CENTER' if 'PokemonCenter' in n else 'MUS_POKE_MART';continue
  data=[floor]*(w*h);m['layout']=addlayout(n,w,h,primary,secondary,data,border)
  if isout:
   if theme not in ['sea','islands']:
    rect(n,0,0,w,2,0x4c6);rect(n,0,h-2,w,2,0x4c6);rect(n,0,0,2,h,0x4c6);rect(n,w-2,0,2,h,0x4c6)
    for x in range(2,w-3,4):stamp(n,3,2,2,4,x,0)
    for y in range(4,h-4,5):stamp(n,3,2,2,4,0,y);stamp(n,3,2,2,4,w-2,y)
    road(n,(w//2,3),(w//2,h-4));road(n,(3,h//2),(w-4,h//2))
    if theme in ['coastal','coast','commercial']:rect(n,3,h-11,w//3,7,0x1170)
    if theme in ['riverside','lakes','ponds','lake','wetlands']:rect(n,w-11,8,7,h-16,0x1170)
    if theme in ['ridge','mountain','foothills','cliff']:
     for y in range(7,h-6,10):rect(n,4,y,6,2,0x4c6)
    if theme in ['forest','woodland','orchard']:
     for x in range(7,w-7,7):
      for y in range(6,h-7,10):
       if abs(x-w//2)>3 and abs(y-h//2)>3:stamp(n,3,2,2,4,x,y)
    if n=='CherrygroveCity':
     rect(n,2,3,4,h-6,0x1170);rect(n,6,3,2,h-6,0x3124)
    if n=='NewBarkTown':rect(n,w-7,h//2-4,5,h//2+2,0x1170)
    if n=='CianwoodCity':
     rect(n,w-8,3,6,h-6,0x1170);rect(n,w-10,3,2,h-6,0x3124)
    if theme=='lake':
     rect(n,8,8,w-16,h-16,0x1170)
     road(n,(w//2,h//2),(w//2-3,h//2+3),width=1)
     road(n,(w//2,h//2),(w//2+3,h//2+3),width=1)
    if theme=='park':
     rect(n,7,7,w-14,h-14,0x3001)
     for x,y in [(7,7),(w-10,7),(7,h-11),(w-10,h-11)]:stamp(n,3,2,2,4,x,y)
     road(n,(7,11),(w-8,11));road(n,(7,h-12),(w-8,h-12))
    if theme=='ruins':
     for x in [6,16,26]:rect(n,x,6,4,5,0x4c6)
   # A real sign and a reachable resident give orientation, not story decisions.
   sx,sy=w//2-3,h//2+3
   if theme in ['sea','islands']:rect(n,sx-1,sy-1,3,3,0x3124)
   rect(n,sx,sy,1,1,0x403);label=script(n+'_Sign');sign(m,sx,sy,label)
   title=CITIES[n][0] if n in CITIES else 'ROUTE '+n[10:] if n.startswith('JohtoRoute') else next(s[1] for s in LANDMARKS if s[0]==n)
   say(label,title+'. Follow the marked roads and direction signs.','SIGN')
   if theme in ['sea','islands']:m['object_events'].append(obj(sx+1,sy+1,'Johto_TestDesk','SAILOR'))
   if theme not in ['sea','islands']:
    x,y=w//2+3,h//2+3;rect(n,x,y,1,1,floor);label=script(n+'_Resident');m['object_events'].append(obj(x,y,label,'WOMAN_3'));say(label,ambient[n] if n in ambient else {'commercial':'There is always another delivery crossing this city. I take the side streets when the market is busy.','academy':'The tower and the school are good landmarks. You can hear the bells from almost anywhere.','woodland':'The shade is welcome after a long walk. The forest path stays open in both directions.','ridge':'The mountain trail winds down to the south. Take your time on the descent.','mountain':'The lake road runs north. Pack something warm if you head toward the Ice Path.','village':'It is quiet here, apart from the wind off the water. The west road leads to Cherrygrove.','island':'The sea road reaches Olivine. Our pharmacy and Center are both near the main street.'}.get(theme,'The signs help when the paths turn. There is no need to rush the walk.'))
  else:
   rect(n,0,0,w,2,border);rect(n,0,h-1,w,1,border);rect(n,0,0,1,h,border);rect(n,w-1,0,1,h,border)
   if primary=='gTileset_General':
    for y in range(6,h-4,6):
     # Offset rock ribs leave perimeter and center bypasses for a genuine loop.
     for x in range(5,w-4):
      if x not in range(w//2-2,w//2+3) and (x+y)%7!=0:rect(n,x,y,1,2,border)
    if kind=='ice':
     # Visible ice panels; the walking ledge stays usable without slide puzzles.
     rect(n,7,8,4,4,0x338d)
    if kind in ['well','falls','islandcave']:rect(n,w-8,7,4,4,0x1170)
   else:
    rect(n,1,0,w-2,1,0x0605);rect(n,1,1,w-2,1,0x060d)
    if theme=='gym':
     rect(n,7,4,4,h-7,0x3224)
     for yy in range(5,h-4,4):rect(n,2,yy,1,1,0x0605);rect(n,w-3,yy,1,1,0x0605)
    if kind in ['tower','shrine']:
     for x in [4,w-5]:
      for y in [4,8,12,16]:rect(n,x,y,1,1,0x0605)
    else:
     for x in (2,3,4):rect(n,x,3,1,1,0x064c)
     rect(n,w-4,3,1,1,0x0654);rect(n,3,h-4,2,1,0x3224)
   label=script(n+'_Guide');x,y=3,4;rect(n,x,y,1,1,floor);m['object_events'].append(obj(x,y,label,'EXPERT_M'))
   text=ambient.get(n,ambient.get(n.rsplit('_',1)[0])) or ('The display cases hold local records and everyday tools. There is no admission charge.' if kind=='facility' else 'Visitors are welcome. Training sessions are not scheduled today.' if theme=='gym' else 'This is a quiet place to stop. The paths and stairs lead back the way you came.')
   say(label,text)
   label=script(n+'_Notes');sign(m,w-3,2,label);rect(n,w-3,2,1,1,0x064c if primary=='gTileset_Building' else border)
   say(label,('Local maps, repair notes and a well-used workbench.' if 'Workshop' in n else 'Please leave the displays as you found them. Take care on the stairs.'),'SIGN')
 # Border graph, with reciprocal offsets and matching edge corridors.
 for a,d,b in EDGES:
  if a not in maps or b not in maps:continue
  aw,ah=sizes[a];bw,bh=sizes[b];horizontal=d in ['left','right'];anchor=39 if a=='EcruteakCity' and d=='down' else 47 if a=='EcruteakCity' and d=='right' else (aw//2 if not horizontal else ah//2)
  offset=anchor-(bw//2 if not horizontal else bh//2)
  for n,other,direction,off in [(a,b,d,offset),(b,a,{'up':'down','down':'up','left':'right','right':'left'}[d],-offset)]:
   cs=maps[n]['connections'] or [];entry=dict(map=maps[other]['id'],offset=off,direction=direction)
   assert not any(c['direction']==direction and c!=entry for c in cs),(n,direction,'Overlapping border')
   if entry not in cs:cs.append(entry)
   maps[n]['connections']=cs
   w,h=sizes[n];axis=anchor if n==a else anchor-offset;sea=n in ['OlivineCity','JohtoRoute40','JohtoRoute41'];v=0x1170 if sea else 0x3202
   if n in existing:
    if n=='EcruteakCity' and direction=='down':pass # HGSS authoring owns this layout
    if n=='OlivineCity' and direction=='left':rect(n,6,24,1,3,0x3202)
   else:
    port=(0,axis) if direction=='left' else (w-1,axis) if direction=='right' else (axis,0) if direction=='up' else (axis,h-1)
    road(n,(w//2,h//2),port,v)
 if 'JohtoRoute40' in maps:
  label='Johto_OlivineSeaSign'
  if not any(e['script']==label for e in maps['OlivineCity']['bg_events']):sign(maps['OlivineCity'],8,25,label)
  rect('OlivineCity',8,25,1,1,0x403)
  say(label,'ROUTE 40. Western sea passage. South: WHIRL ISLANDS and CIANWOOD.','SIGN')
 # City buildings: distinct services, Gym, residence and workshop.
 services=[]
 for n,(_,cluster,pos,theme) in CITIES.items():
  if n not in maps:continue
  w,h=sizes[n];cx=w//2;placements=[('PokemonCenter_1F',8,15,18,16,4,4,1),('Mart',w-12,15,12,23,4,4,1),('Gym',w-14,h-15,25,7,7,6,3),('Residence',7,h-14,4,16,4,4,1),('Workshop',cx-2,5,4,16,4,4,1)]
  for suffix,x,y,sx,sy,ww,hh,doorx in placements:
   x,y=city_sites[n][suffix]
   if suffix=='Gym' and n not in GYM_CITIES:sx,sy,ww,hh,doorx=4,16,4,4,1
   dst=n+'_'+suffix;stamp(n,sx,sy,ww,hh,x,y);protected.setdefault(n,set()).update((xx,yy) for xx in range(x,x+ww) for yy in range(y,y+hh));dx,dy=x+doorx,y+hh-1
   road(n,(dx,dy+1),(cx,dy+1),width=1);say(script(dst+'_Plaque'),CITIES[n][0]+' '+('POKEMON CENTER' if 'PokemonCenter' in suffix else 'COMMUNITY HALL' if suffix=='Gym' and n not in GYM_CITIES else suffix.upper())+'.','SIGN');sign(maps[n],dx-1,dy+1,script(dst+'_Plaque'));rect(n,dx-1,dy+1,1,1,0x403)
   if suffix=='PokemonCenter_1F':
    sign(maps[n],dx-2,dy+1,'Johto_AtlasBoard');rect(n,dx-2,dy+1,1,1,0x403)
    warp(n,dx,dy,dst,7,8);maps[dst]['warp_events'].append(dict(x=6,y=8,elevation=0,dest_map=maps[n]['id'],dest_warp_id=str(len(maps[n]['warp_events'])-1)))
    nurse='LOCALID_JOHTO_NURSE_'+sym(n);label=script(n+'_Nurse');maps[dst]['object_events']=[obj(7,2,label,'NURSE',nurse),obj(2,3,'Johto_TestDesk','SAILOR')]
    scripts.append(f'{label}::\n    setvar VAR_0x800B, {nurse}\n    call Common_EventScript_PkmnCenterNurse\n    waitmessage\n    waitbuttonpress\n    release\n    end\n')
    services.append(dict(id='HEAL_LOCATION_'+sym(n),map=maps[n]['id'],x=dx,y=dy+1,respawn_map=maps[dst]['id'],respawn_npc=nurse))
   elif suffix=='Mart':
    warp(n,dx,dy,dst,3,7);maps[dst]['warp_events'].append(dict(x=4,y=7,elevation=0,dest_map=maps[n]['id'],dest_warp_id=str(len(maps[n]['warp_events'])-1)))
    maps[dst]['object_events']=copy.deepcopy(service_templates['EcruteakCity_Mart']['object_events'])
   else:
    warp(n,dx,dy,dst,6,sizes[dst][1]-1,bt=0x0208)
    if suffix=='Residence':
     label=script(n+'_Rest');maps[dst]['object_events'].append(obj(10,7,label,'WOMAN_5'));scripts.append(f'{label}::\n    goto Olivine_HomeRest\n')
 # Major civic facilities use a separate accessible building and fitting dialogue.
 for p in selected:
  if p['kind']!='facility':continue
  n=p['name'];parent=p['parent'];w,h=sizes[parent]
  x,y={'GoldenrodDepartmentStore':(44,22),'GoldenrodRadioLobby':(8,5),'GoldenrodUnderground':(7,42),'VioletAcademy':(22,32),'NewBarkLab':(33,7),'CianwoodPharmacy':(17,30),'SafariReception':(13,20)}.get(n,(w//2-3,h-10))
  stamp(parent,18,16,4,4,x,y);protected.setdefault(parent,set()).update((xx,yy) for xx in range(x,x+4) for yy in range(y,y+4));dx,dy=x+1,y+3;road(parent,(dx,dy+1),(w//2,dy+1),width=1);warp(parent,dx,dy,n,sizes[n][0]//2,sizes[n][1]-1,bt=0x0208)
  label=script(n+'_Entrance');sign(maps[parent],dx-1,dy+1,label);rect(parent,dx-1,dy+1,1,1,0x403);say(label,re.sub(r'([a-z])([A-Z])',r'\1 \2',n).upper()+'.','SIGN')
  if n=='GoldenrodUnderground':
   # A second public stair makes this a real through passage rather than a lobby.
   x2,y2=16,5;stamp(parent,4,16,4,4,x2,y2);protected.setdefault(parent,set()).update((xx,yy) for xx in range(x2,x2+4) for yy in range(y2,y2+4));road(parent,(x2+1,y2+4),(w//2,y2+4),width=1)
   warp(parent,x2+1,y2+3,n,3,3,bt=0x33fc)
  if 'Store' in n or 'Pharmacy' in n:
   maps[n]['object_events'].append(obj(9,7,'Olivine_Clerk','MAN_1'))
 # Caverns/towers: actual floor stairs and reciprocal external entrances.
 for base,label,cluster,count,theme,mouths in DUNGEONS:
  if base+'_1F' not in maps:continue
  for i in range(count-1):
   a=base+f'_{i+1}F';b=base+f'_{i+2}F';cave=meta[a]['floor']==0x3201
   warp(a,22,4,b,5,16,at=0x323f if cave else 0x33fc,bt=0x323f if cave else 0x33fd)
   road(a,(14,11),(22,5),meta[a]['floor'],1);road(b,(14,11),(5,15),meta[b]['floor'],1)
  for j,(parent,x,y,i) in enumerate(mouths):
   if parent not in maps:continue
   dst=base+f'_{i+1}F';u,v=(7+j*4)%20+3,19
   # A visible entrance marker and approach, never an unmarked teleport.
   if parent not in existing:
    if meta[parent]['theme']=='islands':rect(parent,x-3,y-3,7,7,0x3124)
    # General tiles 0x64/0x71/... are the native Route 106 cave mouth, no new art.
    for yy,row in enumerate([[0x0471,0x0471,0x0475],[0x047c,0x0464,0x047d],[0x0474,0x00a7,0x0491]]):
     for xx,t in enumerate(row):rect(parent,x-1+xx,y-2+yy,1,1,t)
    protected.setdefault(parent,set()).update((xx,yy) for xx in range(x-1,x+2) for yy in range(y-2,y+1))
    rect(parent,x-1,y+1,3,2,0x3202)
    if base!='TohjoFalls' and meta[parent]['theme'] not in ['sea','islands']:road(parent,(x,y+2),(sizes[parent][0]//2,y+2),0x3202,1)
   warp(parent,x,y,dst,u,v,at=0x00a7,bt=0x323f if meta[dst]['floor']==0x3201 else 0x33fd)
   if base in ['WhirlIslands','TohjoFalls']:maps[parent]['object_events'].append(obj(x+1,y+2,'Johto_TestDesk','SAILOR'))
   labelscript=script(base+f'_Mouth{j}');sign(maps[parent],x-1,y+1,labelscript);rect(parent,x-1,y+1,1,1,0x403);say(labelscript,label+'. Public walking access. Please respect the surroundings.','SIGN')
  if base=='TohjoFalls':
   final=base+f'_{count}F';lbl='Johto_KantoBoundary';sign(maps[final],24,5,lbl);rect(final,24,5,1,1,0x0611);say(lbl,'Beyond these falls is the Kanto approach to the Pokemon League. That destination is outside this exploration build. Return by the western passage.','SIGN')
 # Populate the new streets without blocking buildings, doors or survey aprons.
 for n in CITIES:
  if n not in maps:continue
  w,h=sizes[n];made=0
  candidates=[(w//2-5,h//2-4),(w//2+5,h//2-5),(w//2-7,h//2+6),(w//2+7,h//2+7),(w//2-9,h//2-7),(w//2+9,h//2+5)]
  for x,y in candidates:
   if made==3:break
   occupied={(e['x'],e['y']) for e in maps[n]['object_events']+maps[n]['bg_events']+maps[n]['warp_events']}
   if (x,y) in protected.get(n,set()) or any(abs(x-a)+abs(y-b)<3 for a,b in occupied):continue
   if tiles[n][y*w+x]&0xc00 or tiles[n][y*w+x]>>12!=3:continue
   label=script(n+f'_Local{made}');maps[n]['object_events'].append(obj(x,y,label,['MAN_1','WOMAN_5','EXPERT_M'][made]))
   say(label,ambient.get(n+f'_Local{made}', ['The Center is a good place to rest before taking the next road.','I like walking through town before the streets get busy.','There is no prize for arriving tired. Take a break when you need one.'][made]));made+=1
 # Restore accepted sign tiles if a new edge corridor crosses one.
 for n in existing:
  for e in maps[n]['bg_events']:
   if n=='EcruteakCity':rect(n,e['x'],e['y'],1,1,struct.unpack_from('<H',oldbytes[n],(e['y']*sizes[n][0]+e['x'])*2)[0])
 for r in load('crossroads/hgss/gate-review.json'):
  n=r['route'];old_gate=load(f'data/maps/{n}/map.json');gate_mid=load(f'data/maps/{r["name"]}/map.json')['id']
  if not any(e['dest_map']==gate_mid for e in maps[n]['warp_events']):
   maps[n]['warp_events'] += [copy.deepcopy(e) for e in old_gate['warp_events'] if e['dest_map']==gate_mid]
   maps[n]['coord_events'] += [copy.deepcopy(e) for e in old_gate['coord_events'] if e['script'].startswith('Hgss_') and 'GateEnter' in e['script']]
 for n,m in maps.items():
  if n=='EcruteakCity' or (n in meta and meta[n]['kind']=='hgss'):continue # Dedicated HGSS authoring
  if n=='CianwoodCity':rect(n,sizes[n][0]-3,sizes[n][1]//2-1,3,3,0x1170)
  if n not in existing and meta[n]['outdoor']:
   for e in m['bg_events']:rect(n,e['x'],e['y'],1,1,0x403)
  if n in existing and m==existing[n] and tiles[n]==list(struct.unpack('<'+str(len(oldbytes[n])//2)+'H',oldbytes[n])):continue
  js(f'data/maps/{n}/map.json',m)
  if n not in existing:
   extra=''
   if 'PokemonCenter_1F' in n:
    parent=n.rsplit('_PokemonCenter_1F',1)[0];lab=script(parent+'_CenterOnTransition');extra=f'    map_script MAP_SCRIPT_ON_TRANSITION, {lab}\n    map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume\n';scripts.append(f'{lab}::\n    setrespawn HEAL_LOCATION_{sym(parent)}\n    end\n')
   write(f'data/maps/{n}/scripts.inc',f'{n}_MapScripts::\n'+extra+'    .byte 0\n')
  # Reused Center/Mart layouts stay byte-for-byte unchanged.
  if n not in existing and meta[n]['kind']=='service':continue
  path=bylayout[m['layout']]['blockdata_filepath']
  from visual_repairs import repair
  write(path,repair(n,struct.pack('<'+str(len(tiles[n]))+'H',*tiles[n]),*sizes[n]))
 groups['gMapGroup_CrossroadsOlivine']=names[:127]
 if len(names)>127:
  groups['gMapGroup_CrossroadsJohtoExpansion']=names[127:]
  if 'gMapGroup_CrossroadsJohtoExpansion' not in groups['group_order']:groups['group_order'].append('gMapGroup_CrossroadsJohtoExpansion')
 js('data/maps/map_groups.json',groups);js('data/layouts/layouts.json',layouts)
 heals=load('src/data/heal_locations.json');byheal={h['id']:h for h in heals['heal_locations']}
 for s in services:
  if s['id'] not in byheal:heals['heal_locations'].append(s)
  elif byheal[s['id']]!=s:
   # These are new, unreleased town services; retain their assigned heal IDs.
   byheal[s['id']].clear();byheal[s['id']].update(s)
 js('src/data/heal_locations.json',heals)
 # Preserve all old section IDs including NONE=213; append 214..252, never 253+.
 secs=load('src/data/region_map/region_map_sections.json');known={s['id'] for s in secs['map_sections']}
 for n in SECTIONS:
  if sid(n) not in known:
   label=CITIES[n][0] if n in CITIES else 'ROUTE '+n[10:] if n.startswith('JohtoRoute') else next((d[1] for d in DUNGEONS if d[0]==n),next((d[1] for d in LANDMARKS if d[0]==n),n.upper()))
   secs['map_sections'].append(dict(id=sid(n),name=label))
 js('src/data/region_map/region_map_sections.json',secs)
 write('crossroads/scripts/johto_network.inc','@ Generated exploration-only dialogue/services. No story, badge, trainer or encounter grants.\n'+'\n'.join(scripts))
 linked=(R/'data/event_scripts.s').read_text()
 for n in names[37:]:
  inc=f'\t.include "data/maps/{n}/scripts.inc"'
  if inc not in linked:linked+='\n'+inc+'\n'
 inc='\t.include "crossroads/scripts/johto_network.inc"'
 if inc not in linked:linked+='\n'+inc+'\n'
 write('data/event_scripts.s',linked)
 # Record actual IDs, warps, services and explicit unverified runtime state.
 for linear,p in enumerate(plans,37):
  p['map_group']=75 if linear<127 else 76;p['map_num']=linear if linear<127 else linear-127
  if p['name'] in maps:
   n=p['name'];m=maps[n];linear=names.index(n);p['map_group']=75 if linear<127 else 76;p['map_num']=linear if linear<127 else linear-127;p.update(display_name=n.replace('_Gym','_CommunityHall') if n in ['NewBarkTown_Gym','CherrygroveCity_Gym'] else n,role='community hall (stable internal slot suffix Gym)' if n in ['NewBarkTown_Gym','CherrygroveCity_Gym'] else p['kind'],status='implemented',id=m['id'],layout=m['layout'],connections=m['connections'],entrances=m['warp_events']);p.setdefault('coverage','structural/build/runtime checks recorded separately; no owner QA yet')
 for p in manifest['existing']:
  m=maps[p['name']];p.update(connections=m['connections'],entrances=m['warp_events'])
 manifest['dungeons']=DUNGEONS;manifest['border_topology']=EDGES
 manifest['checkpoint']=args.through;js('crossroads/johto/manifest.json',manifest)
 from build_johto_atlas import generate as generate_atlas
 generate_atlas(args.check)
 from build_hgss_ecruteak import generate as generate_hgss
 generate_hgss(args.check)
 from build_hgss_ecruteak_chain import generate as generate_chain
 generate_chain(args.check)
 print('Johto cluster',args.through,':',len(names),'maps registered;',len(services),'new Centers; IDs preserved')
if __name__=='__main__':main()
