#!/usr/bin/env python3
"""Normal-controller material regressions on the frozen delivery ROM.

No player/map/warp coordinate writes. Uses copied normal battery, native title/
Continue and real desk interaction. Dry tests never use Surf; water tests opt in
through the existing session-only desk. Exact original source save is preserved.
"""
import argparse,hashlib,json,runpy,shutil,subprocess,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True);src=Path(a.save).resolve();original_hash=hashlib.sha256(src.read_bytes()).hexdigest();copy=out/'input-copy.sav';assert src!=copy.resolve();shutil.copyfile(src,copy)
sys.argv=['johto_network_smoke.py','--save',str(copy),'--library',a.library,'--output',str(out),'--targets',''];d=runpy.run_path(str(R/'crossroads/tools/johto_network_smoke.py'))
go,walk,frames,key,current,pos,read,lib,syms=[d[k] for k in ['go','walk','frames','key','current','pos','read','lib','syms']];g=walk.__globals__;g['dry_only']=True;g['route_cache'].clear()
def survey(enabled):
 assert read('sJohtoTestAccess',1)==int(not enabled)
 go('OlivineCity_HarborOffice');walk((1,6))
 flags=bytes(read(d['sb']()+0x1270+i,1) for i in range(300))
 frames(1,64);frames(20);key(1);frames(180)
 for _ in range(8):
  if not read('sLockFieldControls',1):break
  key(1);frames(180)
 assert read('sJohtoTestAccess',1)==int(enabled)
 assert bytes(read(d['sb']()+0x1270+i,1) for i in range(300))==flags
survey(False);go('OlivineCity');assert not read('gPlayerAvatar',1)&8
rows=[];clips=[];skips=[];buttons={(1,0):16,(-1,0):32,(0,-1):64,(0,1):128}
def arrow_visible():
 obj=syms['gObjectEvents']+read(syms['gPlayerAvatar']+5,1)*36;sprite=read(obj+0x1b,1)
 return not bool(read(syms['gSprites']+sprite*68+0x3e,1)&4)
def capture(label,action,dry=True):
 native=g['frames'];folder=out/(label+'-frames');folder.mkdir(exist_ok=True);count=[0];arrows=[0];lib.emu_image(str(out/(label+'-before.png')).encode())
 def record(n=60,k=0):
  while n:
   q=min(n,4);native(q,k);n-=q;lib.emu_image(str(folder/f'{count[0]:04}.png').encode());count[0]+=1;arrows[0]+=int(arrow_visible())
 g['frames']=record
 try:
  action();record(20)
  assert current()=='OlivineCity'
  if dry:assert not read('gPlayerAvatar',1)&8 and read('sJohtoTestAccess',1)==0 and arrows[0]==0,(label,'Dry path used Survey/Surf or displayed an unexplained ground arrow',arrows[0])
 finally:
  g['frames']=native
  if count[0]:subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(out/(label+'.mp4'))],check=True)
 lib.emu_image(str(out/(label+'.png')).encode());clips.append(dict(label=label,frame_count=count[0],arrow_visible_samples=arrows[0],position=pos(),surfing=bool(read('gPlayerAvatar',1)&8)));print(label,'PASS',pos(),flush=True)
def dry_walk(target):
 assert g['dry_only'];walk(target);assert current()=='OlivineCity' and pos()==target and not read('gPlayerAvatar',1)&8
# Each old model115 blocker is entered independently through normal movement.
for start in [7,14,29]:
 dry_walk((start+1,41));label='relocated-table-'+str(start)
 def action(start=start):
  for x in range(start,start+4):dry_walk((x,42));rows.append(dict(kind='old-table-now-deck',point=(x,42),result='PASS'))
  dry_walk((start+3,43))
 capture(label,action)
# Actual timber traversal and blue parasol foreground/base behavior.
dry_walk((13,43));capture('timber-promenade',lambda:[dry_walk(q) for q in [(14,43),(15,43),(16,43),(17,43),(18,43)]])
for ox in [11,16,32]:
 dry_walk((ox-1,42));capture('parasol-'+str(ox)+'-canopy',lambda ox=ox:dry_walk((ox,42)))
 dry_walk((ox,45));point=pos();assert d['raw']['OlivineCity'][44*64+ox]&0xc00
 def bump(point=point):g['frames'](32,64);assert pos()==point,('Entered parasol/table base',point,pos())
 capture('parasol-'+str(ox)+'-base',bump)
# Independently enumerated source fence cells; attempt each accessible side.
fences={(6,y) for y in range(10,20)}|{(x,10) for x in [7,8,9,17,18,19,20]}|{(13,y) for y in [21,22,23]};fence_clips=set();warps=d['active_warps']('OlivineCity')
for x,y in sorted(fences,key=lambda q:(q[1],q[0])):
 assert d['raw']['OlivineCity'][y*64+x]&0xc00
 for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
  point=(x-dx,y-dy)
  if point in warps or d['path']('OlivineCity',point) is None:skips.append(dict(kind='fence',target=(x,y),approach=point,reason='No dry public approach'));continue
  dry_walk(point);button=buttons[dx,dy]
  def bump(point=point,button=button):g['frames'](24,button);g['frames'](20);assert pos()==point,('White fence pass-through',point,(x,y),pos())
  label='garden-fence' if x==13 else 'outer-fence'
  if label not in fence_clips:capture(label,bump);fence_clips.add(label)
  else:bump()
  rows.append(dict(kind='white-fence',target=(x,y),approach=point,result='normal movement blocked'))
assert fence_clips=={'garden-fence','outer-fence'}
# Survey assistance only for real native Surf entry, not coordinate/flag setup.
survey(True);g['dry_only']=False;g['route_cache'].clear();go('OlivineCity');assert current()=='OlivineCity' and read('sJohtoTestAccess',1)==1
for label,target in [('east-rock-a',(58,20)),('east-rock-b',(59,24)),('east-rock-c',(55,26)),('east-rock-chain',(58,30))]:
 x,y=target;assert d['raw']['OlivineCity'][y*64+x]&0xc00
 candidates=[((x-dx,y-dy),buttons[dx,dy]) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]]
 candidates=[(q,k) for q,k in candidates if 0<=q[0]<64 and 0<=q[1]<64 and d['raw']['OlivineCity'][q[1]*64+q[0]]>>12==1 and d['path']('OlivineCity',q) is not None]
 assert candidates,(label,'No actual water approach to specified source rock');point,button=candidates[0];walk(point);assert read('gPlayerAvatar',1)&8
 def bump(point=point,button=button):g['frames'](24,button);g['frames'](20);assert pos()==point and read('gPlayerAvatar',1)&8,('Surf entered solid gray boulder',point,pos())
 capture(label,bump,False);rows.append(dict(kind='gray-boulder',target=target,approach=point,result='actual Surf movement blocked'))
# The southern old model cells outside the new north-entry body remain real
# sea. Do not claim every old model cell is sea: the corrected terminal now
# intentionally occupies53..56, including the former dry apron24,54.
assert d['raw']['OlivineCity'][54*64+24]&0xc00,'Former south apron must be actual new solid terminal body'
walk((24,57));assert read('gPlayerAvatar',1)&8
capture('south-of-terminal-native-sea',lambda:[walk(q) for q in [(24,58),(25,58),(26,58)]],False)
walk((40,62));assert read('gPlayerAvatar',1)&8;point=pos()
def sea_edge():g['frames'](32,128);assert pos()==point and current()=='OlivineCity'
capture('southern-sea-boundary',sea_edge,False)
assert d['raw']['OlivineCity'][50*64+24]>>12==3 and not d['raw']['OlivineCity'][50*64+24]&0xc00
assert (24,50) not in d['active_warps']('OlivineCity'),'North apron return must not cross an active threshold'
walk((24,50));assert pos()==(24,50) and not read('gPlayerAvatar',1)&8;lib.emu_image(str(out/'returned-to-dry-north-port-forecourt.png').encode());g['dry_only']=True;g['route_cache'].clear();survey(False);go('OlivineCity');dry_walk((16,34))
assert hashlib.sha256(src.read_bytes()).hexdigest()==original_hash,'Original source save changed'
assert read('sJohtoTestAccess',1)==0 and not read('gPlayerAvatar',1)&8
(out/'results.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest(),source_save_sha256_before=original_hash,source_save_sha256_after=hashlib.sha256(src.read_bytes()).hexdigest(),setup='Copied battery, normal title/Continue, actual desk OFF for dry phases then ON for native Surf and OFF after normal north-pier disembark. Saved flags remain exact across desk interactions.12 cleared table,43 fence and4 rock cases retained. Only shared test-RAM encounter suppression; no map/warp/player XY writes, no permanent grants.',cases=rows,unavailable_fence_approaches=skips,native_recordings=clips,former_south_apron_now_solid=[24,54],actual_dry_north_apron=[24,50],final_survey_access=read('sJohtoTestAccess',1),final_dry_return=pos()),indent=2)+'\n')
print('Materials controller regression PASS:',len(rows),'semantic cases;',len(skips),'unavailable fence sides explicitly skipped;',len(clips),'native clips; actual Surf and dry return',flush=True)
