#!/usr/bin/env python3
"""Fit owner-provided Gyms into eight private city tilesets, never shared sheets.

Retain legacy metatile numbers/graphics for every visible non-Gym cell and route
buffer. Relocate the new art into unused tile/metatile/palette slots; append door
aliases without renumbering maps/layouts/heals. No story, teams or badge flags.
"""
import argparse,copy,json,re,struct,hashlib
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2];A=R/'crossroads/art/eight_gyms_v1';B=A/'baseline';BASE=json.loads((B/'contracts.json').read_text());PLANS=R/'crossroads/art/eight_gyms_v1/integration.json'
SOURCES={'gTileset_HgssVioletPrimary':('primary','hgss_violet','InitTilesetAnim_General'),'gTileset_HgssVioletSecondary':('secondary','hgss_violet','NULL'),'gTileset_General':('primary','general','InitTilesetAnim_General'),'gTileset_WesternCity':('secondary','western_city','InitTilesetAnim_Slateport'),'gTileset_HgssEcruteakPrimary':('primary','hgss_ecruteak','InitTilesetAnim_General'),'gTileset_HgssEcruteakSecondary':('secondary','hgss_ecruteak','NULL')}
CODES={'EcruteakCity':'ecruteak','OlivineCity':'olivine','VioletCity':'violet','AzaleaTown':'azalea','GoldenrodCity':'goldenrod','CianwoodCity':'cianwood','MahoganyTown':'mahogany','BlackthornCity':'blackthorn'}
def load(p):return json.loads((R/p).read_text())
def source_contract(name):
 p=R/f'crossroads/hgss/authoring/{name}.json'
 return json.loads(p.read_text()) if p.exists() else BASE['cities'][name]
def source_bytes(name,c):
 return (R/c['raw_path']).read_bytes() if 'raw_path' in c else (B/(name+'.bin')).read_bytes()
def symbol(name,primary=False):return 'gTileset_BlGym'+CODES[name].title()+('Primary' if primary else 'Secondary')
def relocate_layout(name,l):
 if name in CODES:l.update(primary_tileset=symbol(name,True),secondary_tileset=symbol(name))
 return l
def overlay(name,data,w,h):
 if name not in CODES or not PLANS.exists():return data
 p=json.loads(PLANS.read_text())['cities'][name];t=list(struct.unpack('<'+str(w*h)+'H',data));x,y,ww,hh=p['old_footprint']
 for yy in range(y,y+hh):
  for xx in range(x,x+ww):t[yy*w+xx]=p['background']
 x,y=p['origin']
 for i,value in enumerate(p['stamp']):
  X,Y=x+i%8,y+i//8
  if value is not None:t[Y*w+X]=value
 return struct.pack('<'+str(w*h)+'H',*t)
def patch_events(name,m):
 if not PLANS.exists():return m
 plans=json.loads(PLANS.read_text())['cities']
 if name in CODES:
  p=plans[name];i,j=p['exterior_warps'];m['warp_events'][i].update(x=p['doors'][0][0],y=p['doors'][0][1]);e=dict(m['warp_events'][i],x=p['doors'][1][0],dest_warp_id='1')
  if len(m['warp_events'])==j:m['warp_events'].append(e)
  else:assert len(m['warp_events'])>j;m['warp_events'][j]=e
 else:
  city=next((n for n,p in plans.items() if p['interior']==name),None)
  if city:
   if len(m['warp_events'])==1:m['warp_events'].append(dict(m['warp_events'][0],x=m['warp_events'][0]['x']+1))
   m['warp_events'][1]['dest_warp_id']=str(plans[city]['exterior_warps'][1])
 return m
def interior_overlay(name,data,w,h):
 city=next((n for n,c in BASE['cities'].items() if c['interior']['name']==name),None)
 if not city or 'raw_path' in source_contract(city) or len(BASE['cities'][city]['interior']['warp_events'])!=1:return data
 t=list(struct.unpack('<'+str(w*h)+'H',data));e=BASE['cities'][city]['interior']['warp_events'][0];t[e['y']*w+e['x']+1]=0x209
 return struct.pack('<'+str(len(t))+'H',*t)
def normalize_map(name,m):
 """Project only the explicitly contracted Gym edits back to QA05 for validators."""
 if not PLANS.exists():return copy.deepcopy(m)
 plans=json.loads(PLANS.read_text())['cities'];m=copy.deepcopy(m)
 if name in CODES:
  p=plans[name];i,j=p['exterior_warps'];assert m['warp_events'][j]==dict(m['warp_events'][i],x=p['doors'][1][0],dest_warp_id='1')
  c=source_contract(name)
  if 'gym_alias' not in c:m['warp_events'].pop(j)
  old=c['map']['warp_events'][i];m['warp_events'][i]['x']=old['x'];m['warp_events'][i]['y']=old['y']
 else:
  city=next((n for n,c in BASE['cities'].items() if c['interior']['name']==name),None)
  if city:
   old=source_contract(city)['interior']
   if len(old['warp_events'])==1:m['warp_events'].pop(1)
   else:m['warp_events'][1]['dest_warp_id']=old['warp_events'][1]['dest_warp_id']
 return m
def generate(check=False):
 def write(p,b):
  p=R/p
  if isinstance(b,str):b=b.encode()
  if check:assert p.exists() and p.read_bytes()==b,('Regenerate eight Gym integration',str(p))
  elif not p.exists() or p.read_bytes()!=b:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 def js(p,v):write(p,json.dumps(v,indent=2)+'\n')
 layouts=load('data/layouts/layouts.json');ls={l['id']:l for l in layouts['layouts']};groups=load('data/maps/map_groups.json');names=groups['gMapGroup_CrossroadsOlivine']+groups['gMapGroup_CrossroadsJohtoExpansion'];allmaps={n:load(f'data/maps/{n}/map.json') for n in names};ids={m['id']:n for n,m in allmaps.items()};plans={};blocks={k:[] for k in ['graphics','metatiles','headers','externs']}
 for n,code in CODES.items():
  c=source_contract(n);old=c['map'];l=c['layout'];w,h=l['width'],l['height'];baseline=struct.unpack('<'+str(w*h)+'H',source_bytes(n,c));oldDoor=old['warp_events'][c['gym_warp']];dx=0 if 'raw_path' in c else 1 if n in ['VioletCity','MahoganyTown'] else 0;door=(oldDoor['x']+dx,oldDoor['y']);origin=(door[0]-3,door[1]-6);oldfoot=(oldDoor['x']-3,oldDoor['y']-5,7,6);background=0x3001
  if n=='EcruteakCity':background=0x3000|load('crossroads/hgss/art/native-manifest.json')['specs']['earth']
  pre=list(baseline)
  for x,y,ww,hh in [oldfoot,(*origin,8,7)]:
   assert 0<=x and 0<=y and x+ww<=w and y+hh<=h
   for Y in range(y,y+hh):
    for X in range(x,x+ww):pre[Y*w+X]=background
  dirs=[R/'data/tilesets'/SOURCES[l[k]][0]/SOURCES[l[k]][1] for k in ['primary_tileset','secondary_tileset']]
  metas=[list(struct.unpack('<'+str((p/'metatiles.bin').stat().st_size//2)+'H',(p/'metatiles.bin').read_bytes())) for p in dirs];attrs=[list(struct.unpack('<'+str((p/'metatile_attributes.bin').stat().st_size//2)+'H',(p/'metatile_attributes.bin').read_bytes())) for p in dirs];sheets=[Image.open(p/'tiles.png').copy() for p in dirs]
  primary_ids={v&1023 for v in pre if v&1023<512};secondary_ids={v&1023 for v in pre if v&1023>=512}
  # Preserve every neighbor cell potentially decoded in the seven-tile buffer.
  for conn in old['connections'] or []:
   other=ids[conn['map']];m=allmaps[other];ol=ls[m['layout']];ow,oh=ol['width'],ol['height'];b=(B/(other+'.bin')).read_bytes() if other in CODES else (R/ol['blockdata_filepath']).read_bytes();tt=struct.unpack('<'+str(ow*oh)+'H',b)
   for Y in range(oh):
    for X in range(ow):
     d=conn['direction'];visible=(Y>=oh-7 if d=='up' else Y<7 if d=='down' else X>=ow-7 if d=='left' else X<7)
     if not visible:continue
     id=tt[Y*ow+X]&1023
     if id<512:primary_ids.add(id)
     elif ol['secondary_tileset']==l['secondary_tileset'] or other not in CODES and l['secondary_tileset']=='gTileset_WesternCity' and ol['secondary_tileset']=='gTileset_WesternCity':secondary_ids.add(id)
  refs=[v for id in primary_ids for v in metas[0][id*8:id*8+8]]+[v for id in secondary_ids for v in metas[1][(id-512)*8:(id-511)*8]]
  protected={v&1023 for v in refs}|set(range(432,512))
  if SOURCES[l['secondary_tileset']][2]=='InitTilesetAnim_Slateport':protected|=set(range(512+224,512+228))
  banks={v>>12 for v in refs if any(sheets[(v&1023)//512].crop((((v&1023)%512)%16*8,((v&1023)%512)//16*8,((v&1023)%512)%16*8+8,((v&1023)%512)//16*8+8)).tobytes())};bank=next((i for i in range(6,13) if i not in banks),None);assert bank is not None,(n,'No palette slot',banks)
  free_meta=[i for i in range(512,1024) if i not in secondary_ids];assert len(free_meta)>=56
  gym_meta=free_meta[:56];gym=A/'assets'/code;source=Image.open(gym/'tiles.png');asset_metas=struct.unpack('<448H',(gym/'metatiles.bin').read_bytes());asset_attrs=struct.unpack('<56H',(gym/'metatile_attributes.bin').read_bytes());asset_stamp=struct.unpack('<56H',(gym/'stamp.bin').read_bytes());raw4=(gym/'tiles.4bpp').read_bytes();manifest=load(f'crossroads/art/eight_gyms_v1/assets/{code}/manifest.json');assert hashlib.sha256(raw4[:manifest['tile_count']*32]).hexdigest()==manifest['sha256_4bpp'];assert hashlib.sha256(raw4).hexdigest()==next(e for e in load('crossroads/art/eight_gyms_v1/manifest.json')['entries'] if e['name']==code)['sha256_4bpp']
  free_tiles=[i for i in range(512,1024) if i not in protected]+[i for i in range(432) if i not in protected];pixels={};allocated={};tile_mapping={}
  for id in range(1024):
   im=sheets[id//512];i=id%512;pixels.setdefault(im.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8)).tobytes(),[]).append(id)
  for id in sorted({v&1023 for i,v in enumerate(asset_metas) if i%8>=4}):
   i=id-512;im=source.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8));key=im.tobytes()
   if key in allocated:target=allocated[key]
   elif any(v in protected for v in pixels.get(key,[])):target=next(v for v in pixels[key] if v in protected);allocated[key]=target
   else:
    target=next((v for v in free_tiles if v not in protected),None);assert target is not None,(n,'Graphics capacity');allocated[key]=target;dest=sheets[target//512];j=target%512;dest.paste(im,(j%16*8,j//16*8))
   protected.add(target);tile_mapping[id]=target
  metas[1]+=[0]*(4096-len(metas[1]));attrs[1]+=[0]*(512-len(attrs[1]));stamp=[]
  for i,dest_id in enumerate(gym_meta):
   X,Y=origin[0]+i%8,origin[1]+i//8;oldvalue=baseline[Y*w+X];old_id=oldvalue&1023
   # Retain flat road/ground beneath overhangs; original building fragments do
   # not become the new roof's ground plane.
   if old_id>=512 or oldvalue&0xc00:old_id=background&1023
   if oldfoot[0]<=X<oldfoot[0]+7 and oldfoot[1]<=Y<oldfoot[1]+6:old_id=background&1023
   under=metas[old_id>=512][(old_id%512)*8:(old_id%512)*8+4];top=[tile_mapping[v&1023]|(v&0xc00)|(bank<<12) for v in asset_metas[i*8+4:i*8+8]];metas[1][(dest_id-512)*8:(dest_id-511)*8]=under+top;attrs[1][dest_id-512]=asset_attrs[i]
   empty=all(not any(source.crop((((v&1023)-512)%16*8,((v&1023)-512)//16*8,((v&1023)-512)%16*8+8,((v&1023)-512)//16*8+8)).tobytes()) for v in asset_metas[i*8+4:i*8+8])
   stamp.append(None if empty else (asset_stamp[i]&~1023)|dest_id)
  # Own every resource explicitly. Shared General/Western/HGSS files stay intact.
  for is_primary in [True,False]:
   k=0 if is_primary else 1;kind='primary' if is_primary else 'secondary';path=f'data/tilesets/{kind}/bl_gym_{code}';sym=symbol(n,is_primary).removeprefix('gTileset_');im=sheets[k]
   if check:
    oldim=Image.open(R/path/'tiles.png');assert oldim.tobytes()==im.tobytes(),(n,'Changed private tiles')
   else:(R/path).mkdir(parents=True,exist_ok=True);im.save(R/path/'tiles.png',bits=4)
   write(path+'/metatiles.bin',struct.pack('<'+str(len(metas[k]))+'H',*metas[k]));write(path+'/metatile_attributes.bin',struct.pack('<'+str(len(attrs[k]))+'H',*attrs[k]))
   for pal in range(16):write(path+f'/palettes/{pal:02}.pal',(gym/'palette.pal').read_bytes() if not is_primary and pal==bank else (dirs[k]/f'palettes/{pal:02}.pal').read_bytes())
   blocks['graphics'].append(f'const u32 gTilesetTiles_{sym}[] = INCGFX_U32("{path}/tiles.png", ".4bpp.fastSmol");\nconst u16 gTilesetPalettes_{sym}[][16] = {{\n'+''.join(f'    INCGFX_U16("{path}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n')
   blocks['metatiles'].append(f'const u16 gMetatiles_{sym}[] = INCBIN_U16("{path}/metatiles.bin");\nconst u16 gMetatileAttributes_{sym}[] = INCBIN_U16("{path}/metatile_attributes.bin");\n')
   blocks['headers'].append(f'const struct Tileset gTileset_{sym} = {{\n .isCompressed=TRUE, .isSecondary={"FALSE" if is_primary else "TRUE"},\n .tiles=gTilesetTiles_{sym}, .palettes=gTilesetPalettes_{sym},\n .metatiles=gMetatiles_{sym}, .metatileAttributes=gMetatileAttributes_{sym},\n .callback={SOURCES[l["primary_tileset" if is_primary else "secondary_tileset"]][2]},\n}};\n');blocks['externs'].append(f'extern const struct Tileset gTileset_{sym};\n')
  current=allmaps[n];index=c['gym_warp'];current['warp_events'][index].update(x=door[0],y=door[1]);alias=dict(current['warp_events'][index],x=door[0]+1,dest_warp_id='1');alias_index=c.get('gym_alias',len(old['warp_events']))
  if len(current['warp_events'])==alias_index:current['warp_events'].append(alias)
  else:assert len(current['warp_events'])>alias_index;current['warp_events'][alias_index]=alias
  inside=load(f'data/maps/{c["interior"]["name"]}/map.json')
  if len(inside['warp_events'])==1:inside['warp_events'].append(dict(inside['warp_events'][0],x=inside['warp_events'][0]['x']+1))
  inside['warp_events'][1]['dest_warp_id']=str(alias_index)
  if len(c['interior']['warp_events'])==1:
   il=ls[inside['layout']];ib=(R/il['blockdata_filepath']).read_bytes();it=list(struct.unpack('<'+str(il['width']*il['height'])+'H',ib));entry=inside['warp_events'][1];it[entry['y']*il['width']+entry['x']]=0x209;write(il['blockdata_filepath'],struct.pack('<'+str(len(it))+'H',*it))
  plan=dict(code=code,origin=origin,doors=[list(door),[door[0]+1,door[1]]],old_footprint=oldfoot,background=background,stamp=stamp,metatile_ids=gym_meta,tile_mapping=tile_mapping,palette=bank,source_sha256=hashlib.sha256((gym/'building.png').read_bytes()).hexdigest(),exterior_warps=[index,alias_index],interior=inside['name'],legacy_primary_ids=sorted(primary_ids),legacy_secondary_ids=sorted(secondary_ids),allocated_new_tiles=len(allocated),adaptations=['Owner-provided custom Black Ledger Gym, not literal HGSS art']+(['Entrance one tile east for border clearance; old warp ID retained'] if dx else []))
  plans[n]=plan;relocate_layout(n,ls[l['id']]);js(f'data/maps/{n}/map.json',current);js(f'data/maps/{inside["name"]}/map.json',inside)
 # Commit resource plan before authoring data; overlay reads exactly this mapping.
 js('crossroads/art/eight_gyms_v1/integration.json',dict(version=1,baseline=BASE['source_commit'],cities=plans))
 for n in CODES:
  c=source_contract(n);l=c['layout'];plan=plans[n];t=list(struct.unpack('<'+str(l['width']*l['height'])+'H',source_bytes(n,c)));x,y,ww,hh=plan['old_footprint']
  for yy in range(y,y+hh):
   for xx in range(x,x+ww):t[yy*l['width']+xx]=plan['background']
  for i,v in enumerate(plan['stamp']):
   if v is not None:t[(plan['origin'][1]+i//8)*l['width']+plan['origin'][0]+i%8]=v
  write(l['blockdata_filepath'],struct.pack('<'+str(len(t))+'H',*t))
 js('data/layouts/layouts.json',layouts)
 for key,path in [('graphics','src/data/tilesets/graphics.h'),('metatiles','src/data/tilesets/metatiles.h'),('headers','src/data/tilesets/headers.h'),('externs','include/tilesets.h')]:
  text=(R/path).read_text();start='// BEGIN OWNER EIGHT GYMS INTEGRATION';end='// END OWNER EIGHT GYMS INTEGRATION';block=start+'\n#if !IS_FRLG\n'+''.join(blocks[key])+'#endif\n'+end
  if start in text:text=re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda m:block,text,flags=re.S)
  elif key=='externs':p=text.rfind('#endif');text=text[:p]+block+'\n'+text[p:]
  else:text+='\n'+block+'\n'
  write(path,text)
 print('Eight owner Gym exteriors fitted into private city resources; all legacy IDs retained.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');generate(p.parse_args().check)
