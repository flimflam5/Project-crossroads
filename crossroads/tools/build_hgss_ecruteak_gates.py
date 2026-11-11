#!/usr/bin/env python3
"""HGSS gatehouses inserted into existing road apertures, IDs appended.

Keep the existing border metadata and compatible buffer tiles. Ground coordinate
triggers handle the horizontal portals, avoiding facade metatiles in the shared
seven-tile scrolling buffer. Native warp indices/coordinates remain inspectable.
"""
import argparse,json,struct,copy
from pathlib import Path
from hgss_room_projection import project,ART,FACTS
R=Path(__file__).resolve().parents[2]
def load(p):return json.loads((R/p).read_text())
def generate(check=False):
 def write(p,b):
  if isinstance(b,str):b=b.encode()
  dest=R/p
  if check:assert dest.exists() and dest.read_bytes()==b,('Regenerate Ecruteak gate',p)
  elif not dest.exists() or dest.read_bytes()!=b:dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
 def js(p,v):write(p,json.dumps(v,indent=2)+'\n')
 layouts=load('data/layouts/layouts.json');ls={l['id']:l for l in layouts['layouts']};groups=load('data/maps/map_groups.json');manifest=load('crossroads/johto/manifest.json');city=load('data/maps/EcruteakCity/map.json');records=[];scripts=[];inc=(R/'data/event_scripts.s').read_text()
 for direction,number,aperture in [('West',38,range(37,40)),('East',42,range(46,49))]:
  name='EcruteakCity_'+direction+'Gate';mid='MAP_ECRUTEAK_CITY_'+direction.upper()+'_GATE';header=f'MAP_ROUTE_{number}_ECRUTEAK_GATEHOUSE';route=load(f'data/maps/JohtoRoute{number}/map.json');rl=ls[route['layout']];rw,rh=rl['width'],rl['height'];connection=next(c for c in city['connections'] if c['direction']==('left' if direction=='West' else 'right'));cx=6 if direction=='West' else 63;rx=rw-1 if direction=='West' else 0
  m=copy.deepcopy(load('data/maps/EcruteakCity_BarrierStation/map.json'));m.update(id=mid,name=name,layout='LAYOUT_HGSS_'+name.upper(),object_events=[],bg_events=[],coord_events=[],warp_events=[])
  room=project(header,'stone');w,h=room['width'],room['height'];t=room['tiles']
  for y in (2,3):
   for x in range(1,w-1):t[y*w+x]=0x400|ART['house_wall']['start']+(y-2)*4+x%4
  for x in (2,10):
   for y in (1,9):
    a=ART['pillar_stone']
    for yy in range(a['height']):
     if y+yy<h:t[(y+yy)*w+x]=(t[(y+yy)*w+x]&0xfc00)|a['start']+yy*a['width']
  guard=copy.deepcopy(load('data/maps/EcruteakCity_BarrierStation/map.json')['object_events'][0]);guard.update(x=5,y=6,graphics_id='OBJ_EVENT_GFX_MAN_1',script='Hgss_'+direction+'GateGuide');guard.pop('local_id',None);m['object_events']=[guard]
  # Append only, retaining all accepted city/route indices. Three aliases cover
  # the owner's three-tile road openings; center is the source entrance axis.
  endpoints={}
  for outer,is_city in [(city,True),(route,False)]:
   previous=[(i,e) for i,e in enumerate(outer['warp_events']) if e['dest_map']==mid][:3]
   if not previous:
    start=len(outer['warp_events'])
    for Y in aperture:
     source_index=next(i for i,e in enumerate(FACTS[header]['warps']) if (e['header']=='MAP_ECRUTEAK')==is_city)
     outer['warp_events'].append(dict(x=cx if is_city else rx,y=Y if is_city else Y-connection['offset'],elevation=0,dest_map=mid,dest_warp_id=str(source_index)))
   else:start=previous[0][0];assert len(previous)==3
   for j,Y in enumerate(aperture):outer['warp_events'][start+j].update(x=cx if is_city else rx,y=Y if is_city else Y-connection['offset'])
   source_index=next(i for i,e in enumerate(FACTS[header]['warps']) if (e['header']=='MAP_ECRUTEAK')==is_city)
   # The visible horizontal aisle is three cells high. Keep canonical center
   # indices0/1 and append upper/lower exit aliases2..5. Match each road row.
   door_indices=[2+source_index*2,source_index,3+source_index*2]
   for j,index in enumerate(door_indices):outer['warp_events'][start+j]['dest_warp_id']=str(index)
   key='city' if is_city else 'route';endpoints[key+'_entry']=start+1
   # Return to public ground OUTSIDE the model, not inside its entrance trigger.
   # These append-only warp anchors have no entry behavior/coordinate script.
   ax=(7 if direction=='West' else 59) if is_city else (rw-2 if direction=='West' else 3)
   points=[(ax,Y if is_city else Y-connection['offset']) for Y in aperture]
   arrivals=[(i,e) for i,e in enumerate(outer['warp_events']) if e['dest_map']==mid and (e['x'],e['y']) in points]
   if not arrivals:
    arrival_start=len(outer['warp_events'])
    for point,index in zip(points,door_indices):outer['warp_events'].append(dict(x=point[0],y=point[1],elevation=0,dest_map=mid,dest_warp_id=str(index)))
   else:
    assert len(arrivals)==3;arrival_start=arrivals[0][0]
    assert [i for i,e in arrivals]==list(range(arrival_start,arrival_start+3))
   endpoints[key]=arrival_start+1
   label='Hgss_'+direction+('City' if is_city else 'Route')+'GateEnter';source_index=next(i for i,e in enumerate(FACTS[header]['warps']) if (e['header']=='MAP_ECRUTEAK')==is_city)
   old=[e for e in outer['coord_events'] if e['script']!=label];old += [dict(type='trigger',x=e['x'],y=e['y'],elevation=0,var='VAR_TEMP_0',var_value='0',script=label) for e in outer['warp_events'][start:start+3]];outer['coord_events']=old
   # Each coordinate script selects its own row; no collapse onto the middle.
   old=[e for e in outer['coord_events'] if not e['script'].startswith(label)]
   for j,index in enumerate(door_indices):
    row_label=label+str(j);event=outer['warp_events'][start+j]
    old.append(dict(type='trigger',x=event['x'],y=event['y'],elevation=0,var='VAR_TEMP_0',var_value='0',script=row_label))
    scripts.append(f'{row_label}::\n    lockall\n    warp {mid}, {index}\n    waitstate\n    releaseall\n    end\n')
   outer['coord_events']=old
  for e in FACTS[header]['warps']:
   is_city=e['header']=='MAP_ECRUTEAK';m['warp_events'].append(dict(x=e['x'],y=e['z'],elevation=0,dest_map=city['id'] if is_city else route['id'],dest_warp_id=str(endpoints['city' if is_city else 'route'])));t[e['z']*w+e['x']]=0x3000|ART['stone_warp']['start']
  for i,e in enumerate(FACTS[header]['warps']):
   is_city=e['header']=='MAP_ECRUTEAK';center=endpoints['city' if is_city else 'route']
   for delta in [-1,1]:
    m['warp_events'].append(dict(x=e['x'],y=e['z']+delta,elevation=0,dest_map=city['id'] if is_city else route['id'],dest_warp_id=str(center+delta)))
    t[(e['z']+delta)*w+e['x']]=0x3000|ART['stone_warp']['start']
  text='West: ROUTE 38.\\nEast: ECRUTEAK CITY.' if direction=='West' else 'West: ECRUTEAK CITY.\\nEast: ROUTE 42.'
  scripts.append(f'Hgss_{direction}GateGuide::\n    msgbox Hgss_{direction}GateText, MSGBOX_NPC\n    end\nHgss_{direction}GateText:\n    .string "{text}$"\n')
  l=dict(id=m['layout'],name=name+'_Layout',width=w,height=h,primary_tileset='gTileset_Building',secondary_tileset='gTileset_HgssTemple',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin',layout_version='emerald')
  if l['id'] in ls:ls[l['id']].clear();ls[l['id']].update(l)
  else:layouts['layouts'].append(l);ls[l['id']]=l
  js(f'data/maps/{name}/map.json',m);js(f'data/maps/JohtoRoute{number}/map.json',route);write(l['blockdata_filepath'],struct.pack('<'+str(w*h)+'H',*t));write(l['border_filepath'],struct.pack('<4H',*([0x600]*4)))
  if name not in groups['gMapGroup_CrossroadsJohtoExpansion']:groups['gMapGroup_CrossroadsJohtoExpansion'].append(name)
  if not any(p['name']==name for p in manifest['planned']):manifest['planned'].append(dict(name=name,kind='hgss',parent='EcruteakCity',cluster='west',status='reference-runtime-review-pending'))
  write(f'data/maps/{name}/scripts.inc',name+'_MapScripts::\n    .byte 0\n');line=f'\t.include "data/maps/{name}/scripts.inc"'
  if line not in inc:inc+='\n'+line+'\n'
  records.append(dict(name=name,source_header=header,source=FACTS[header]['source'],dimensions=[w,h],city_alias_indices=list(range(endpoints['city_entry']-1,endpoints['city_entry']+2)),city_arrival_indices=list(range(endpoints['city']-1,endpoints['city']+2)),route=f'JohtoRoute{number}',route_alias_indices=list(range(endpoints['route_entry']-1,endpoints['route_entry']+2)),route_arrival_indices=list(range(endpoints['route']-1,endpoints['route']+2)),adaptations=['GBA flat gatehouse/pillars instead of DS models','All three aisle rows work; source west entrance x6 retained','Visible native roof/front-wall models and shared resources across the east seam','Explicit return-only anchors put Joe on public ground outside each model'],visual_qa='pending',runtime_qa='pending'))
 js('data/maps/EcruteakCity/map.json',city);js('data/layouts/layouts.json',layouts);js('data/maps/map_groups.json',groups);js('crossroads/johto/manifest.json',manifest);js('crossroads/hgss/gate-review.json',records);write('crossroads/scripts/hgss_gates.inc','@ Reference gatehouses; no story/save flags.\n'+'\n'.join(scripts))
 line='\t.include "crossroads/scripts/hgss_gates.inc"'
 if line not in inc:inc+='\n'+line+'\n'
 write('data/event_scripts.s',inc)
 print('HGSS west/east gatehouses and road-width reciprocal portals registered; no existing IDs removed.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');generate(p.parse_args().check)
