#!/usr/bin/env python3
"""Normal controller wall/trunk/overhang tests over the actual delivery ROM.

Dry approaches around the twelve land buildings and three free trees remain
separate from a disclosed actual-Surf pass around the relocated waterfront
terminal. All thirteen buildings still require real controller coverage.
No player/map/warp/flag RAM setup or Surf substitutes ordinary dry walking.
"""
import argparse,hashlib,json,runpy,subprocess,sys
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');p.add_argument('--output',type=Path,default=R/'build/olivine-collision-check');a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True)
sys.argv=['johto_network_smoke.py','--save',a.save,'--library',a.library,'--output',str(out),'--targets',''];d=runpy.run_path(str(R/'crossroads/tools/johto_network_smoke.py'))
go,walk,frames,key,current,pos,read,lib,syms,close=[d[k] for k in ['go','walk','frames','key','current','pos','read','lib','syms','close']]
save_hash=hashlib.sha256(Path(a.save).read_bytes()).hexdigest()
def survey(enabled):
 # The shared cold-load harness enabled the existing desk once. Every change
 # here is another real public interaction; saved flags must remain untouched.
 assert read('sJohtoTestAccess',1)==int(not enabled)
 go('OlivineCity_HarborOffice');walk((1,6))
 before=bytes(read(d['sb']()+0x1270+i,1) for i in range(300))
 frames(1,64);frames(20);key(1);frames(180)
 for _ in range(8):
  if not read('sLockFieldControls',1):break
  key(1);frames(180)
 assert read('sJohtoTestAccess',1)==int(enabled)
 assert bytes(read(d['sb']()+0x1270+i,1) for i in range(300))==before
survey(False)
g=walk.__globals__;native_safe=g['safe']
def dry_safe(n,p):return native_safe(n,p) and d['raw'][n][p[1]*d['size'][n][0]+p[0]]>>12==3
g['safe']=dry_safe;g['dry_only']=True;g['route_cache'].clear();go('OlivineCity');assert not read('gPlayerAvatar',1)&8
raw=d['raw']['OlivineCity'];w,h=d['size']['OlivineCity'];specs=json.loads((R/'crossroads/hgss/art/olivine/manifest.json').read_text())['specs']
# Coordinates and front wall points are independently pinned from source city
# entrances/owner artwork, rather than accepting whatever a generator paints.
buildings=[('joe-home','native',(7,20,4,4),[8]),('neighbor-home','native',(7,25,4,4),[8]),('silph-office','native',(29,36,5,5),[31]),('harbor-office','native',(7,37,4,4),[8]),('fishing-house','house',(16,20,4,4),[17]),('trade-house','house',(30,14,4,4),[31]),('seal-house','house',(35,14,4,4),[36]),('cafe','cafe',(8,30,4,4),[9]),('center','center',(14,29,6,5),[16,17]),('mart','mart',(28,30,5,4),[29]),('lighthouse','lighthouse',(42,31,7,9),[45]),('port','port',(20,51,8,6),[23,24]),('owner-gym','gym',(10,8,8,7),[13,14])]
assert len(buildings)==13
rows=[];skips=[];movies=[];trials=[];positive=[];port_water=[];landing_visibility=[]
warps=d['active_warps']('OlivineCity');actors={(e['x'],e['y']) for e in d['maps']['OlivineCity']['object_events']}
def blocked(x,y):return bool(raw[y*w+x]&0xc00)
def direction(dx,dy):return 16 if dx==1 else 32 if dx==-1 else 128 if dy==1 else 64
def joe_pixels(frame):
 # Compare actual composed framebuffer pixels to independently decoded Joe
 # OAM/OBJ data. A correct sprite pointer alone cannot reveal canopy clipping.
 s=syms['gSprites']+read(syms['gPlayerAvatar']+4,1)*68;tile=read(s+4,2)&1023;palette=read(s+4,2)>>12;matches=[]
 for i in range(128):
  addr=0x07000000+i*8;v0,v1,v2=read(addr,2),read(addr+2,2),read(addr+4,2)
  if(v2&1023)==tile and v2>>12==palette and not v0&0x300:matches.append((v0,v1,v2))
 assert len(matches)==1,('Cannot identify Joe OAM',tile,palette,matches)
 v0,v1,v2=matches[0];assert not v0&0x2c00
 dims=[[(8,8),(16,16),(32,32),(64,64)],[(16,8),(32,8),(32,16),(64,32)],[(8,16),(8,32),(16,32),(32,64)]];width,height=dims[v0>>14][v1>>14];x0,y0=v1&511,v0&255;x0=x0-512 if x0>=256 else x0;y0=y0-256 if y0>=160 else y0
 assert 0<=x0<=240-width and 0<=y0<=160-height
 colors=[]
 for i in range(16):
  value=read(0x05000200+palette*32+i*2,2);colors.append(tuple(((value>>shift)&31)<<3|((value>>shift)&31)>>2 for shift in(0,5,10)))
 stride=width//8 if read(0x04000000,2)&64 else 32;expected=visible=0
 for y in range(height):
  for x in range(width):
   X=width-1-x if v1&0x1000 else x;Y=height-1-y if v1&0x2000 else y;index=tile+(Y//8)*stride+X//8;value=read(0x06010000+index*32+(Y%8)*4+(X%8)//2,1);color=(value>>(4*(X%2)))&15
   if color:expected+=1;visible+=int(frame.getpixel((x0+x,y0+y))==colors[color])
 return dict(opaque_expected=expected,opaque_visible=visible,opaque_hidden=expected-visible)
def record(label,point,button,target=None,water=False):
 folder=out/(label+'-frames');folder.mkdir(exist_ok=True);lib.emu_image(str(out/(label+'-before.png')).encode());visible=0
 for i in range(24):
  frames(4,button if i<8 else 0);lib.emu_image(str(folder/f'{i:04d}.png').encode())
  obj=syms['gObjectEvents']+read(syms['gPlayerAvatar']+5,1)*36;arrow=read(obj+0x1b,1)
  visible+=int(not bool(read(syms['gSprites']+arrow*68+0x3e,1)&4))
 if not water:assert visible==0,(label,'Unexpected ground arrow',visible)
 assert current()=='OlivineCity' and pos()==(target or point),(label,point,target,current(),pos())
 assert bool(read('gPlayerAvatar',1)&8)==water and read('sJohtoTestAccess',1)==int(water)
 lib.emu_image(str(out/(label+'.png')).encode());subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(out/(label+'.mp4'))],check=True);movies.append(label)
for label,kind,(ox,oy,ww,hh),doors in buildings:
 # Independent solid-base cases prevent an accidentally walkable wall from
 # being omitted merely because an automated search only discovers solids.
 independent=[(x,oy+hh-1) for x in range(ox,ox+ww) if x not in doors]
 if kind=='gym':independent=[(11,14),(12,14),(15,14),(16,14)] # transparent owner-art corners are intentional
 if kind=='port':
  # Both actual doors are NORTH at23/24,52. Every SOUTH rear-base cell must
  # block, including the former south-door columns; do not omit those two.
  independent=[(x,56) for x in range(20,28)]
  independent += [(21,52),(22,52),(25,52),(26,52),(21,53),(26,53),(21,54),(26,54)]
 for x,y in independent:assert blocked(x,y),(label,'Known wall/base became passable',x,y)
 solid={(x,y) for y in range(oy,oy+hh) for x in range(ox,ox+ww) if blocked(x,y) and (x,y) not in warps}
 # Include every exposed side of the entire physical footprint, not just a
 # favorable front sample. Internal wall-to-wall edges have no valid approach.
 for x,y in solid:
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   point=(x-dx,y-dy)
   if not(0<=point[0]<w and 0<=point[1]<h) or point in warps or point in actors or not dry_safe('OlivineCity',point):continue
   trials.append((label,point,(x,y),direction(dx,dy)))
for label,ox,oy in [('residence-tree',12,19),('south-tree',12,27),('east-tree',39,19)]:
 for x in [ox,ox+1]:
  y=oy+1;assert blocked(x,y),(label,'Known tree trunk became passable',x,y)
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   point=(x-dx,y-dy)
   if 0<=point[0]<w and 0<=point[1]<h and point not in warps and dry_safe('OlivineCity',point):trials.append((label,point,(x,y),direction(dx,dy)))
 for x in [ox,ox+1]:assert not blocked(x,oy),(label,'Canopy overhang was blanket-blocked',x,oy)
seen=set();recorded=set()
while trials:
 trials.sort(key=lambda row:(abs(row[1][0]-pos()[0])+abs(row[1][1]-pos()[1]),row));label,point,target,button=trials.pop(0)
 ident=(point,target)
 if ident in seen:continue
 seen.add(ident)
 if d['path']('OlivineCity',point) is None:skips.append(dict(label=label,point=point,wall=target,reason='No dry accessible approach'));continue
 walk(point);assert not read('gPlayerAvatar',1)&8 and read('sJohtoTestAccess',1)==0
 if label in ['fishing-house','silph-office','residence-tree'] and label not in recorded:
  record(label+'-wall-bump',point,button);recorded.add(label)
 else:frames(24,button);frames(30)
 assert current()=='OlivineCity' and pos()==point,(label,'Entered known solid wall/trunk',point,target,current(),pos())
 rows.append(dict(label=label,approach=point,solid=target,button=button,result='normal controller movement blocked'))
for label,ox,oy in [('residence-tree',12,19),('south-tree',12,27),('east-tree',39,19)]:
 target=(ox,oy)
 if d['path']('OlivineCity',target) is None:skips.append(dict(label=label+'-canopy',point=target,reason='Canopy not accessible from public ground'));continue
 walk(target);assert pos()==target;lib.emu_image(str(out/(label+'-under-canopy.png')).encode());positive.append(dict(label=label,canopy=target,result='Walkable intentional foreground overhang'))
assert {r['label'] for r in rows}>={r[0] for r in buildings if r[0]!='port'}|{'residence-tree','south-tree','east-tree'},'Every land building and free tree must retain actual dry controller coverage'
assert {'fishing-house','silph-office','residence-tree'}<=recorded,'Representative green-roof/office/tree clips missing'
assert not read('gPlayerAvatar',1)&8 and read('sJohtoTestAccess',1)==0
# Reproduce both genuine terminal exits, then inspect the actual framebuffer at
# the north landing before walking away. B2's canopy hid Joe's lower body here.
for inside_leaf,column in [(0,23),(3,24)]:
 go('OlivineCity_PortTerminal',0);label='port-north-landing-'+str(column);folder=out/(label+'-frames');folder.mkdir(exist_ok=True);native=g['frames'];count=[0]
 def landing_frames(n=60,k=0):
  while n:
   step=min(n,4);native(step,k);n-=step;lib.emu_image(str(folder/f'{count[0]:04d}.png').encode());count[0]+=1
 g['frames']=landing_frames
 try:
  d['warp'](inside_leaf);landing_frames(30)
  assert current()=='OlivineCity' and pos()==(column,51),(label,'Wrong north arrival',current(),pos())
  object_id=read(syms['gPlayerAvatar']+5,1);facing=read(syms['gObjectEvents']+object_id*36+24,1)&15;assert facing==2,(label,'North exit must face the city',facing)
  image=out/(label+'.png');lib.emu_image(str(image).encode());visibility=joe_pixels(Image.open(image).convert('RGB'))
  assert visibility['opaque_expected']>0 and visibility['opaque_hidden']==0,(label,'Canopy hides Joe on arrival',visibility)
  walk((column,50));landing_frames(24);assert not read('gPlayerAvatar',1)&8 and read('sJohtoTestAccess',1)==0
  landing_visibility.append(dict(inside_leaf=inside_leaf,arrival=[column,51],facing=facing,actual_framebuffer=visibility,walk_away=pos(),result='PASS'))
 finally:
  g['frames']=native
  if count[0]:subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(out/(label+'.mp4'))],check=True);movies.append(label)
assert len(landing_visibility)==2
# The new terminal body stands over sea. Restore the original safe predicate
# before actual Survey/native Surf; leaving dry_safe installed would silently
# exclude the building from testing. Every accessible exposed water side is tried.
survey(True);g['safe']=native_safe;g['dry_only']=False;g['route_cache'].clear();go('OlivineCity')
solid={(x,y) for y in range(51,57) for x in range(20,28) if blocked(x,y) and (x,y) not in warps}
water_trials=[]
for x,y in sorted(solid):
 for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
  point=(x-dx,y-dy)
  if not (0<=point[0]<w and 0<=point[1]<h) or point in warps or point in actors:continue
  if native_safe('OlivineCity',point) and raw[point[1]*w+point[0]]>>12==1:
   water_trials.append((point,(x,y),direction(dx,dy)))
assert water_trials,'Port body must have actual water approaches'
water_recorded=set()
while water_trials:
 water_trials.sort(key=lambda row:(abs(row[0][0]-pos()[0])+abs(row[0][1]-pos()[1]),row));point,target,button=water_trials.pop(0)
 assert d['path']('OlivineCity',point) is not None,('Exposed port body has no public water approach',point,target)
 walk(point);assert read('gPlayerAvatar',1)&8 and read('sJohtoTestAccess',1)==1
 side={16:'west',32:'east',128:'north',64:'south'}[button]
 if side not in water_recorded:
  record('port-body-surf-'+side,point,button,water=True);water_recorded.add(side)
 else:frames(24,button);frames(30)
 assert current()=='OlivineCity' and pos()==point and read('gPlayerAvatar',1)&8,('Surf entered solid port body',point,target,current(),pos())
 port_water.append(dict(label='port',mode='actual native Surf with desk-enabled session access',side=side,approach=point,solid=target,button=button,result='normal controller movement blocked'))
assert water_recorded=={'north','south','east','west'},'All exposed port-body sides require actual Surf recordings'
assert {(r['solid'][0],r['solid'][1]) for r in port_water if r['side']=='south'} >= {(x,56) for x in range(20,28)},'All8 rear bases require actual south-side Surf bumps'
assert {r['label'] for r in rows+port_water}>={r[0] for r in buildings}|{'residence-tree','south-tree','east-tree'},'Every building and free tree must have actual controller coverage'
walk((24,49));assert pos()==(24,49) and not read('gPlayerAvatar',1)&8,'Return to actual north pier must disembark normally'
g['safe']=dry_safe;g['dry_only']=True;g['route_cache'].clear();survey(False);go('OlivineCity');walk((16,34))
assert not read('gPlayerAvatar',1)&8 and read('sJohtoTestAccess',1)==0
assert hashlib.sha256(Path(a.save).read_bytes()).hexdigest()==save_hash,'Original source battery changed'
(out/'results.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest(),source_battery_sha256=save_hash,source_battery_unchanged=True,setup='Read-only copied battery; normal title/Continue and controller travel. Dry land-building/tree phase uses actual Survey OFF. Both actual port exits require full composed-frame Joe visibility at north landing before walk-away. Separate port-body phase restores native safe paths, enables Survey through the desk and enters actual native Surf. All four water-facing sides and8 rear bases checked; normal disembark and actual desk OFF restore dry play. No map/warp/player position/flag writes. Random encounters suppressed only in test RAM by shared harness.',buildings=[r[0] for r in buildings],normal_controller_bumps=rows,port_north_landing_visibility=landing_visibility,port_actual_surf_bumps=port_water,port_surf_recorded_sides=sorted(water_recorded),skipped_inaccessible_approaches=skips,intentional_canopy_overlap=positive,native_movement_recordings=movies,final_dry_return=pos()),indent=2)+'\n')
print('Actual controller building/tree collision PASS:',len(rows),'dry bumps;',len(port_water),'separate actual Surf port bumps;',len(skips),'unreachable dry approaches explicitly skipped;',len(buildings),'buildings,3trees; desk OFF and dry return',flush=True)
