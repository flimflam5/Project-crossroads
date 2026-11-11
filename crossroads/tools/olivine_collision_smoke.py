#!/usr/bin/env python3
"""Normal controller wall/trunk/overhang tests over the actual delivery ROM.

All dry approaches around thirteen independently located building footprints and
three free trees are attempted; inaccessible approaches are reported, never
counted as passed. No player/map/warp/flag RAM setup or Surf substitutes walking.
"""
import argparse,hashlib,json,runpy,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');p.add_argument('--output',type=Path,default=R/'build/olivine-collision-check');a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True)
sys.argv=['johto_network_smoke.py','--save',a.save,'--library',a.library,'--output',str(out),'--targets',''];d=runpy.run_path(str(R/'crossroads/tools/johto_network_smoke.py'))
go,walk,frames,key,current,pos,read,lib,syms,close=[d[k] for k in ['go','walk','frames','key','current','pos','read','lib','syms','close']]
# Disable assistance by its actual public desk interaction, not a memory write.
go('OlivineCity_HarborOffice');walk((1,6));frames(1,64);frames(20);key(1);frames(180)
for _ in range(8):
 if not read('sLockFieldControls',1):break
 key(1);frames(180)
assert read('sJohtoTestAccess',1)==0,'Normal water rules must be restored at the desk'
g=walk.__globals__;native_safe=g['safe']
def dry_safe(n,p):return native_safe(n,p) and d['raw'][n][p[1]*d['size'][n][0]+p[0]]>>12==3
g['safe']=dry_safe;g['route_cache'].clear();go('OlivineCity');assert not read('gPlayerAvatar',1)&8
raw=d['raw']['OlivineCity'];w,h=d['size']['OlivineCity'];specs=json.loads((R/'crossroads/hgss/art/olivine/manifest.json').read_text())['specs']
# Coordinates and front wall points are independently pinned from source city
# entrances/owner artwork, rather than accepting whatever a generator paints.
buildings=[('joe-home','native',(7,20,4,4),[8]),('neighbor-home','native',(7,25,4,4),[8]),('silph-office','native',(29,36,5,5),[31]),('harbor-office','native',(7,37,4,4),[8]),('fishing-house','house',(16,20,4,4),[17]),('trade-house','house',(30,14,4,4),[31]),('seal-house','house',(35,14,4,4),[36]),('cafe','cafe',(8,30,4,4),[9]),('center','center',(14,29,6,5),[16,17]),('mart','mart',(28,30,5,4),[29]),('lighthouse','lighthouse',(42,31,7,9),[45]),('port','port',(20,47,8,6),[23,24]),('owner-gym','gym',(10,8,8,7),[13,14])]
assert len(buildings)==13
rows=[];skips=[];movies=[];trials=[];positive=[]
warps=d['active_warps']('OlivineCity');actors={(e['x'],e['y']) for e in d['maps']['OlivineCity']['object_events']}
def blocked(x,y):return bool(raw[y*w+x]&0xc00)
def direction(dx,dy):return 16 if dx==1 else 32 if dx==-1 else 128 if dy==1 else 64
def record(label,point,button,target=None):
 folder=out/(label+'-frames');folder.mkdir(exist_ok=True);lib.emu_image(str(out/(label+'-before.png')).encode());visible=0
 for i in range(24):
  frames(4,button if i<8 else 0);lib.emu_image(str(folder/f'{i:04d}.png').encode())
  obj=syms['gObjectEvents']+read(syms['gPlayerAvatar']+5,1)*36;arrow=read(obj+0x1b,1)
  visible+=int(not bool(read(syms['gSprites']+arrow*68+0x3e,1)&4))
 assert visible==0,(label,'Unexpected ground arrow',visible)
 assert current()=='OlivineCity' and pos()==(target or point),(label,point,target,current(),pos())
 assert not read('gPlayerAvatar',1)&8 and read('sJohtoTestAccess',1)==0
 lib.emu_image(str(out/(label+'.png')).encode());subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(out/(label+'.mp4'))],check=True);movies.append(label)
for label,kind,(ox,oy,ww,hh),doors in buildings:
 # Independent solid-base cases prevent an accidentally walkable wall from
 # being omitted merely because an automated search only discovers solids.
 independent=[(x,oy+hh-1) for x in range(ox,ox+ww) if x not in doors]
 if kind=='gym':independent=[(11,14),(12,14),(15,14),(16,14)] # transparent owner-art corners are intentional
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
assert {r['label'] for r in rows}>={r[0] for r in buildings}|{'residence-tree','south-tree','east-tree'},'Every building and free tree must have actual controller coverage'
assert {'fishing-house','silph-office','residence-tree'}<=recorded,'Representative green-roof/office/tree clips missing'
assert not read('gPlayerAvatar',1)&8 and read('sJohtoTestAccess',1)==0
(out/'results.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest(),setup='Read-only copied battery; normal title/Continue and controller travel. Actual desk toggles survey OFF; paths are dry only. No map/warp/player position/flag writes. Random encounters suppressed only in test RAM by shared harness.',buildings=[r[0] for r in buildings],normal_controller_bumps=rows,skipped_inaccessible_approaches=skips,intentional_canopy_overlap=positive,native_movement_recordings=movies),indent=2)+'\n')
print('Actual dry controller building/tree collision PASS:',len(rows),'bumps;',len(skips),'unreachable approaches explicitly skipped;',len(buildings),'buildings,3trees; no Surf or survey assistance',flush=True)
