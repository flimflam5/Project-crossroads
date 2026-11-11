"""Positive source-backed Bell lamps and Burned Tower collapsed opening.

Copies the existing original GBA temple resources into one private secondary.
The three upper-floor model186 wall lamps use the project's existing lantern
sprite. The collapsed opening reuses original dark-pit/charred-wall motifs.
No HGSS texture, collision, public floor, warp, actor or save ID changes.
"""
import argparse,functools,hashlib,io,json,re,struct,subprocess
from collections import deque
from pathlib import Path
from tileset_registration import upsert
R=Path(__file__).resolve().parents[2]
BASE='fd151242458efe5759b18650f35a5e5b2fa47e45'
RESOURCE='data/tilesets/secondary/hgss_ecruteak_tower_details'
MANIFEST='crossroads/hgss/tower-details-qa09.json'
SYMBOL='gTileset_HgssEcruteakTowerDetails'
HEADERS={f'MAP_BELL_TOWER_{i}F':f'EcruteakCity_BellTower_{i}F' for i in [5,6,7]}
HEADERS['MAP_BURNED_TOWER_1F']='EcruteakCity_BurnedTower'
def load(p):return json.loads((R/p).read_text())
def words(b):return list(struct.unpack('<'+str(len(b)//2)+'H',b))
@functools.lru_cache(None)
def old(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R)
def art():return load('crossroads/hgss/art/temple/manifest.json')['specs']
def tileset(header):return SYMBOL if header in HEADERS else 'gTileset_HgssTemple'
def _hole(tiles,w,h,ox,oy):
 stone=art()['stone']['start']
 # This is precisely the filled source-blocked central area in the existing
 # projection. Props/ledges/public cells are not eligible for a visual override.
 eligible={(x,y) for y in range(h) for x in range(w) if 8<=x+ox<23 and 10<=y+oy<24 and tiles[y*w+x]&0xc00 and tiles[y*w+x]&1023==stone}
 seed=(15-ox,15-oy);assert seed in eligible,'Source collapsed shaft was changed'
 seen={seed};q=deque(seen)
 while q:
  x,y=q.popleft()
  for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if p in eligible and p not in seen:seen.add(p);q.append(p)
 return seen
def patch(header,tiles,w,h,ox=4,oy=4):
 """Return a copy; preserve every raw collision/elevation bit exactly."""
 if header not in HEADERS:return list(tiles)
 t=list(tiles);a=art();manifest=load(MANIFEST)
 if header.startswith('MAP_BELL_TOWER_'):
  facts=load('crossroads/hgss/canonical_events/ecruteak-interior-geometry.json')[header]
  lamps=[p for chunk in facts['chunks'] for p in chunk['props'] if p['model']==186]
  assert [(int(p['tile_x']),int(p['tile_z'])) for p in lamps]==[(9,5),(15,5),(21,5)]
  for p in lamps:
   x,y=int(p['tile_x'])-ox,int(p['tile_z'])-oy;assert 0<=x<w and 0<=y<h
   original=t[y*w+x];assert original&0xc00,'Wall lamp may not occupy a public tile'
   target=manifest['lamp_by_base'][str(original&1023)];t[y*w+x]=(original&~1023)|target
 else:
  mask=_hole(t,w,h,ox,oy)
  for x,y in mask:
   top=min(v for u,v in mask if u==x);bottom=max(v for u,v in mask if u==x);left=min(u for u,v in mask if v==y);right=max(u for u,v in mask if v==y)
   if y-top<2:meta=a['burned_wall_burned_floor']['start']+(y-top)*4+(x+ox)%4
   elif x in [left,right] or y==bottom:meta=a['dark_pit']['start']+(2 if y==bottom else 0)+(1 if x==right else 0)
   else:meta=a['void']['start']
   t[y*w+x]=(t[y*w+x]&~1023)|meta
 return t
def generate(check=False):
 """Root runs after the shared temple converter, before tower map generation."""
 from PIL import Image
 def write(p,b):
  target=R/p
  if isinstance(b,str):b=b.encode()
  if target.suffix=='.pal':b=b.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
  if check:assert target.exists() and target.read_bytes()==b,('Regenerate tower details',p)
  elif not target.exists() or target.read_bytes()!=b:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
 source=R/'data/tilesets/secondary/hgss_temple';sheet=Image.open(source/'tiles.png').copy();metas=words((source/'metatiles.bin').read_bytes());attrs=words((source/'metatile_attributes.bin').read_bytes());original_meta=len(attrs)
 assert all(v>>12 in [6,7] for v in metas),'Private lantern palette8 must be unused by original temple art'
 used={v&1023 for v in metas};free=[i for i in range(512) if 512+i not in used];cache={}
 for i in range(512):cache.setdefault(sheet.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8)).tobytes(),512+i)
 lantern=Image.open(R/'graphics/object_events/pics/misc/area_lantern.png');assert lantern.size==(16,16) and lantern.mode=='P';refs=[];allocated=[]
 for x,y in [(0,0),(8,0),(0,8),(8,8)]:
  im=lantern.crop((x,y,x+8,y+8));key=im.tobytes()
  if key not in cache:
   assert free,'Private tower graphics exceed existing512 slots';i=free.pop(0);sheet.paste(im,(i%16*8,i//16*8));cache[key]=512+i;allocated.append(i)
  refs.append(cache[key]|0x8000)
 # The source-directed rear railing sometimes shares the wall's cell. Preserve
 # its actual delivered background under each fixture rather than guessing a
 # uniform wall pattern or reading an already-patched mutable map.
 baseline_layouts={l['id']:l for l in json.loads(old('data/layouts/layouts.json'))['layouts']};bases=set()
 for header,name in HEADERS.items():
  if not header.startswith('MAP_BELL_TOWER_'):continue
  m=json.loads(old(f'data/maps/{name}/map.json'));l=baseline_layouts[m['layout']];t=words(old(l['blockdata_filepath']))
  bases.update(t[l['width']+x]&1023 for x in [5,11,17])
 mapping={}
 for base in sorted(bases):
  n=512+len(attrs);mapping[str(base)]=n;metas.extend(metas[(base-512)*8+4:(base-512)*8+8]+refs);attrs.append(0x1000)
 assert len(attrs)<=512
 target=R/RESOURCE;target.mkdir(parents=True,exist_ok=True)
 if check:assert Image.open(target/'tiles.png').tobytes()==sheet.tobytes()
 else:sheet.save(target/'tiles.png',bits=4)
 write(RESOURCE+'/metatiles.bin',struct.pack('<'+str(len(metas))+'H',*metas));write(RESOURCE+'/metatile_attributes.bin',struct.pack('<'+str(len(attrs))+'H',*attrs))
 for pal in range(16):write(RESOURCE+f'/palettes/{pal:02}.pal',(R/'graphics/object_events/pics/misc/area_lantern.pal').read_bytes() if pal==8 else (source/f'palettes/{pal:02}.pal').read_bytes())
 manifest=dict(source_commit=BASE,targets=HEADERS,source_references='Pinned HGSS matrix/permissions/props in canonical_events/ecruteak-interior-geometry.json; actual Bell5F/7F/Burned1F mosaics inspected',lamp_source_model=186,lamp_source_positions=[[9,5],[15,5],[21,5]],lamp_native_positions=[[5,1],[11,1],[17,1]],lamp_by_base=mapping,base_metatiles=original_meta,new_metatiles=len(attrs)-original_meta,new_graphics=allocated,original_lantern_sha256=hashlib.sha256((R/'graphics/object_events/pics/misc/area_lantern.png').read_bytes()).hexdigest(),adaptations=['Existing original GBA lantern replaces perspective HGSS wall light; no new actor or interaction','Collapsed opening uses charred rear wall/dark interior/fragmented rim on source-blocked cells;2D depth replaces visible DS basement model','Public geometry, stairs, warps, actors, movement behaviors and stable IDs are unchanged'])
 write(MANIFEST,json.dumps(manifest,indent=2)+'\n')
 sym='HgssEcruteakTowerDetails';blocks={
 'src/data/tilesets/graphics.h':f'const u32 gTilesetTiles_{sym}[] = INCGFX_U32("{RESOURCE}/tiles.png", ".4bpp.fastSmol");\nconst u16 gTilesetPalettes_{sym}[][16] = {{\n'+''.join(f' INCGFX_U16("{RESOURCE}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n',
 'src/data/tilesets/metatiles.h':f'const u16 gMetatiles_{sym}[] = INCBIN_U16("{RESOURCE}/metatiles.bin");\nconst u16 gMetatileAttributes_{sym}[] = INCBIN_U16("{RESOURCE}/metatile_attributes.bin");\n',
 'src/data/tilesets/headers.h':f'const struct Tileset gTileset_{sym} = {{ .isCompressed=TRUE, .isSecondary=TRUE, .tiles=gTilesetTiles_{sym}, .palettes=gTilesetPalettes_{sym}, .metatiles=gMetatiles_{sym}, .metatileAttributes=gMetatileAttributes_{sym}, .callback=NULL }};\n',
 'include/tilesets.h':f'extern const struct Tileset gTileset_{sym};\n'}
 for p,body in blocks.items():
  text=(R/p).read_text();begin='// BEGIN ECRUTEAK TOWER DETAILS';end='// END ECRUTEAK TOWER DETAILS';block=begin+'\n#if !IS_FRLG\n'+body+'#endif\n'+end
  text=upsert(text,begin,end,block,externs=p=='include/tilesets.h')
  write(p,text)
 print('Private Bell wall lamps/Burned collapsed opening:',len(allocated),'new graphics;',len(attrs),'metatiles; shared temple resources untouched')
def validate():
 """Exact raw/event/physics and existing-resource identity, plus positive motifs."""
 from PIL import Image
 source=R/'data/tilesets/secondary/hgss_temple';target=R/RESOURCE;manifest=load(MANIFEST);shared_meta=(source/'metatiles.bin').read_bytes();private_meta=(target/'metatiles.bin').read_bytes();shared_attrs=(source/'metatile_attributes.bin').read_bytes();private_attrs=(target/'metatile_attributes.bin').read_bytes()
 assert private_meta[:len(shared_meta)]==shared_meta and private_attrs[:len(shared_attrs)]==shared_attrs
 a=Image.open(source/'tiles.png');b=Image.open(target/'tiles.png');refs={v&1023 for v in words(shared_meta)}
 for n in refs:
  assert 512<=n<1024;n-=512;box=(n%16*8,n//16*8,n%16*8+8,n//16*8+8);assert a.crop(box).tobytes()==b.crop(box).tobytes(),('Original temple graphic changed',n)
 for pal in [6,7]:assert (target/f'palettes/{pal:02}.pal').read_bytes()==(source/f'palettes/{pal:02}.pal').read_bytes()
 assert (target/'palettes/08.pal').read_text().splitlines()==(R/'graphics/object_events/pics/misc/area_lantern.pal').read_text().splitlines()
 # Decode the actual before/after layers independently of the packer's mutable
 # source sheet. This detects a palette-bank leak or glyph remap even where a
 # raw map word did not change. RGB555 matches the hardware's palette precision.
 def resource(previous):
  roots=['data/tilesets/primary/building','data/tilesets/secondary/hgss_temple' if previous else RESOURCE]
  data=lambda p:old(p) if previous else (R/p).read_bytes()
  sheets=[Image.open(io.BytesIO(data(p+'/tiles.png'))) for p in roots]
  metas=[words(data(p+'/metatiles.bin')) for p in roots];attrs=[words(data(p+'/metatile_attributes.bin')) for p in roots]
  palettes=[[tuple(int(c)//8 for c in line.split()) for line in data(roots[int(bank>=6)]+f'/palettes/{bank:02}.pal').decode().splitlines()[3:]] for bank in range(16)]
  return sheets,metas,attrs,palettes
 resources={previous:resource(previous) for previous in [True,False]}
 @functools.lru_cache(None)
 def signature(meta,previous):
  sheets,metas,attrs,palettes=resources[previous];pieces=[]
  for v in metas[int(meta>=512)][meta%512*8:meta%512*8+8]:
   index=v&1023;i=index%512;im=sheets[int(index>=512)].crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8))
   if v&0x400:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
   if v&0x800:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
   pieces.append(tuple(palettes[v>>12][n] if n else None for n in im.tobytes()))
  return attrs[int(meta>=512)][meta%512],tuple(pieces)
 ls={l['id']:l for l in load('data/layouts/layouts.json')['layouts']};oldls={l['id']:l for l in json.loads(old('data/layouts/layouts.json'))['layouts']};modified=0;lamps=0;hole=0
 for header,name in HEADERS.items():
  m=load(f'data/maps/{name}/map.json');before=json.loads(old(f'data/maps/{name}/map.json'));assert m==before,('Tower events/IDs/actors changed',name)
  l=ls[m['layout']];prior=oldls[before['layout']];assert l==dict(prior,secondary_tileset=SYMBOL),(name,'Unexpected tower layout mutation')
  raw=words((R/l['blockdata_filepath']).read_bytes());baseline=words(old(prior['blockdata_filepath']));w,h=l['width'],l['height'];expected=patch(header,baseline,w,h)
  assert raw==expected,(name,'Unexpected raw change beyond exact source details')
  assert all(x&0xfc00==y&0xfc00 for x,y in zip(raw,baseline)),(name,'Physics/elevation changed')
  changed=[i for i,(x,y) in enumerate(zip(raw,baseline)) if x!=y];modified+=len(changed)
  for i,(current,prior) in enumerate(zip(raw,baseline)):
   before_signature=signature(prior&1023,True);after_signature=signature(current&1023,False)
   assert before_signature[0]==after_signature[0],(name,'Metatile behavior/layer priority changed',i%w,i//w)
   if current==prior:assert before_signature==after_signature,(name,'Unchanged cell pixels/layers/palette changed',i%w,i//w)
  if header.startswith('MAP_BELL_TOWER_'):
   assert [(i%w,i//w) for i in changed]==[(5,1),(11,1),(17,1)];lamps+=len(changed)
   # Every fixture retains all four exact original lantern glyphs and palette.
   for i in changed:
    tile=raw[i]&1023;mt=words(private_meta)[(tile-512)*8:(tile-511)*8]
    original=Image.open(R/'graphics/object_events/pics/misc/area_lantern.png')
    for j,v in enumerate(mt[4:]):
     n=(v&1023)-512;assert v>>12==8 and b.crop((n%16*8,n//16*8,n%16*8+8,n//16*8+8)).tobytes()==original.crop((j%2*8,j//2*8,j%2*8+8,j//2*8+8)).tobytes()
  else:
   assert changed and all(baseline[i]&0xc00 for i in changed)
   assert any(raw[i]&1023==art()['void']['start'] for i in changed),'Collapsed center must read as an opening, not filled stone'
   assert any(art()['burned_wall_burned_floor']['start']<=raw[i]&1023<art()['burned_wall_burned_floor']['start']+8 for i in changed),'Source shaft needs a charred rear wall'
   hole=len(changed)
 assert lamps==9
 print('Positive original-native Bell lamp fixtures and collapsed Burned shaft; exact prior raw outside',modified,'cells, all physics/events/IDs/old graphics retained: PASS',lamps,'lamps,',hole,'shaft cells')
 return set(HEADERS.values())
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--validate',action='store_true');a=p.parse_args();validate() if a.validate else generate(a.check)
