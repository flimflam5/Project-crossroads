#!/usr/bin/env python3
"""QA09 independent doorway leaves and actual lighthouse special journeys.

Starts from a read-only copied normal battery save and uses controller travel.
Same-ROM snapshots isolate trials. No map/warp/position RAM writes are used.
Encounter suppression and opt-in survey Surf are disclosed by the shared harness.
"""
import argparse,hashlib,json,runpy,shutil,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');p.add_argument('--output',required=True);p.add_argument('--city',choices=['olivine','ecruteak','both'],default='olivine');p.add_argument('--filter',default='');p.add_argument('--start-label',help='Resume with this named group after completed earlier groups were recorded on the identical ROM');p.add_argument('--special-only',action='store_true');p.add_argument('--doors-only',action='store_true');p.add_argument('--skip-elevator',action='store_true',help='Resume remaining special cases only after four panel/leaf checks are already recorded on the exact same ROM');p.add_argument('--manifest',type=Path,help='Explicit reviewed visible-opening contract; defaults to the original QA09 contract');p.add_argument('--require-facing',action='store_true',help='Reject groups that omit independent intended arrival-facing expectations');p.add_argument('--require-facing-for',action='append',default=[],metavar='PREFIX',help='Require explicit facing for these group prefixes within a larger historical contract; repeatable');p.add_argument('--record-fronts-only',action='store_true',help='Run every controller/assertion case; record video only for required fronts and one actual arrival PNG for every executed approach');a=p.parse_args()
R=Path(__file__).resolve().parents[2];out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
source_save=Path(a.save).resolve();save_hash=hashlib.sha256(source_save.read_bytes()).hexdigest();trial_save=out/'input-copy.sav'
assert source_save!=trial_save.resolve(),'Output copy must differ from original source save'
shutil.copyfile(source_save,trial_save)
sys.argv=['johto_network_smoke.py','--save',str(trial_save),'--library',a.library,'--output',str(out),'--targets',''];d=runpy.run_path(str(Path(__file__).with_name('johto_network_smoke.py')))
go,walk,frames,current,pos,lib=[d[k] for k in ['go','walk','frames','current','pos','lib']]
manifest_path=a.manifest or R/'crossroads/hgss/doorways-qa09.json';manifest=json.loads(manifest_path.read_text());results=[];special=[]
# Pedestrian doors/return journeys must never be satisfied with Survey Surf.
walk.__globals__['dry_only']=True;d['route_cache'].clear()
BUTTON={(0,-1):64,(0,1):128,(-1,0):32,(1,0):16}
def capture(label,action):
 # runpy returns a dictionary copy; patch the functions' real shared globals.
 g=walk.__globals__;original=g['frames'];original_local=globals()['frames'];folder=out/label;folder.mkdir(exist_ok=True);counter=[0]
 def record(count=60,k=0):
  while count:
   q=min(4,count);original(q,k);count-=q;lib.emu_image(str(folder/f'{counter[0]:04}.png').encode());counter[0]+=1
 g['frames']=record;globals()['frames']=record
 try:return action()
 finally:
  g['frames']=original;globals()['frames']=original_local
  if counter[0]:clip(folder,label)
def clip(folder,label):
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(out/(label+'.mp4'))],check=True)
if not a.special_only:
 started=not a.start_label
 for group in manifest['groups']:
  if a.city!='both' and group['city']!=a.city or a.filter and a.filter not in group['label']:continue
  if not started:
   if group['label']!=a.start_label:continue
   started=True
  for side in ['outside','inside']:
   source=group[side];n=source['map'];other=group['inside' if side=='outside' else 'outside']['map'];first=tuple(source['segments'][0]);entry=next(i for i,e in enumerate(d['maps'][n]['warp_events']) if (e['x'],e['y'])==first);go(n,entry);anchor=tuple(source['anchor']);anchor_route=d['path'](n,anchor);assert anchor_route is not None and all(d['raw'][n][q[1]*d['size'][n][0]+q[0]]>>12==3 for q in anchor_route),('Door anchor lacks a dry path',n,anchor);walk(anchor);state=out/'trial.snapshot';assert lib.emu_state(str(state).encode(),0)
   for i,cell in enumerate(source['segments']):
    x,y=cell;nx,ny=source.get('press',[0,-1] if side=='outside' else [0,1]);button=BUTTON[nx,ny]
    for approach,offset in [('front',0),('lateral-negative',-1),('lateral-positive',1)]:
     assert lib.emu_state(str(state).encode(),1);label=f"{group['label']}-{side}-{i}-{approach}";folder=out/label;folder.mkdir(exist_ok=True);row=dict(label=label,source=n,segment=cell,expected_destination=other);counter=[0];capture_video=not a.record_fronts_only or approach=='front'
     def record(count,keys=0):
      if not capture_video:frames(count,keys);return
      while count:
       q=min(4,count);frames(q,keys);count-=q;lib.emu_image(str(folder/f'{counter[0]:04}.png').encode());counter[0]+=1
     try:
      landing=x-nx,y-ny;start=landing[0]-offset*ny,landing[1]+offset*nx
      if d['path'](n,start) is None:
       assert offset,('Required front landing unreachable',n,cell,landing)
       row.update(result='inaccessible lateral approach',position=pos());results.append(row);print(json.dumps(row),flush=True);continue
      route=d['path'](n,start);assert all(d['raw'][n][q[1]*d['size'][n][0]+q[0]]>>12==3 for q in route),('Door approach would require Surf',n,cell,start)
      walk(start);record(4)
      if offset:
       dx,dy=landing[0]-start[0],landing[1]-start[1];record(16,BUTTON[dx,dy]);record(24)
      assert current()==n and pos()==landing,('Lateral landing failed',current(),pos(),landing)
      record(16,button);record(180)
      if current()==n and pos()==(x,y):record(16,button);record(180)
      assert current()==other,('Exact segment did not warp',current(),pos());arrival=pos();frames(40)
      event=next(e for e in d['maps'][n]['warp_events'] if (e['x'],e['y'])==(x,y));back=d['maps'][other]['warp_events'][int(event['dest_warp_id'])];expected_arrival=(back['x'],back['y'])
      # Emerald's native animated/nonanimated doors take exactly one south
      # exit step. Ladders, arrow thresholds and neutral gate anchors do not.
      # Check actual engine arrival instead of accepting any point in the city.
      if d['behavior'](other,*expected_arrival) in [0x60,0x69]:expected_arrival=(expected_arrival[0],expected_arrival[1]+1)
      assert arrival==expected_arrival,('Wrong native arrival position',other,arrival,expected_arrival)
      targetside=group['inside' if side=='outside' else 'outside']
      object_id=d['read'](d['syms']['gPlayerAvatar']+5,1);facing=d['read'](d['syms']['gObjectEvents']+object_id*36+24,1)&15
      expected_facing=targetside.get('expected_facing')
      if isinstance(expected_facing,list):expected_facing=expected_facing[i]
      if a.require_facing or any(group['label'].startswith(v)for v in a.require_facing_for):assert expected_facing is not None,('Visible-opening contract lacks intended arrival facing',group['label'],other)
      if expected_facing is not None:assert facing==expected_facing,('Arrival faces the wrong physical direction',group['label'],other,arrival,facing,expected_facing)
      row.update(facing=facing,expected_facing=expected_facing)
      if 'arrivals' in targetside:assert arrival==tuple(targetside['arrivals'][i]),('Incorrect arrival',arrival,targetside['arrivals'][i])
      if a.record_fronts_only:assert lib.emu_image(str(out/(label+'-actual-arrival.png')).encode())
      candidates=[(arrival[0],arrival[1]+v) for v in [1,-1]]+[(arrival[0]+v,arrival[1]) for v in [-1,1]]
      if 'arrivals' in targetside:
       vx,vy=targetside.get('press',[0,-1]);candidates.insert(0,(arrival[0]-vx,arrival[1]-vy))
      target=next((q for q in candidates if d['safe'](other,q) and d['raw'][other][q[1]*d['size'][other][0]+q[0]]>>12==3 and q not in d['active_warps'](other) and d['path'](other,q) is not None),None)
      assert target is not None,('No walk-away after arrival',other,arrival);walk(target);record(24)
      row.update(result='PASS',arrival=arrival,expected_arrival=expected_arrival,walk_away=pos())
     except (AssertionError,StopIteration) as error:
      row.update(result='FAIL',error=str(error),actual_map=current(),position=pos());lib.emu_image(str(out/(label+'-failure.png')).encode())
     if counter[0]:clip(folder,label)
     results.append(row);print(json.dumps(row),flush=True)
if not a.doors_only and a.city in ['olivine','both'] and not a.filter:
 # Each native dynamic exit leaf is exercised after each panel independently.
 # The destination is read from the actual engine; no synthetic warp is written.
 for floor in ([] if a.skip_elevator else d['LIFT_FLOORS']):
  for leaf in [0,1]:
   go(d['LIFT']);capture(f'{floor}-lift-{leaf}',lambda:d['lift'](floor,leaf));arrival=pos();walk((9,5));assert current()==floor
   row=dict(action='native elevator',panel_destination=floor,exit_leaf=leaf,arrival=arrival,walk_away=pos(),result='PASS');special.append(row);lib.emu_image(str(out/(floor+'-lift-'+str(leaf)+'.png')).encode());print(json.dumps(row),flush=True)
 # The window is intentionally one-way, but the balcony branch must return by
 # normal stairs/elevator; simply reaching an isolated map does not satisfy it.
 go(d['WINDOW'],'window');capture('window-drop',d['window_fall']);arrival=pos();walk((14,10));lib.emu_image(str(out/'window-balcony-arrival.png').encode());go('OlivineCity_Lighthouse_3F',3);go('OlivineCity_Lighthouse_4F',1);go('OlivineCity_Lighthouse_5F');go('OlivineCity_Lighthouse_6F');go('OlivineCity_Lighthouse_1F');go('OlivineCity')
 special.append(dict(action='4F window, balcony, south3F, west4F,5F,6F,elevator and city return',arrival=arrival,returned_map=current(),result='PASS'))
 # Preserve real sea under the thin roof overhang while blocking its body.
 # This is the actual V6 reproduced column pass-through, now a normal-input
 # regression for both central columns; no metadata-only probe substitutes it.
 for x in [23,24]:
  go('OlivineCity');walk((x,46))
  def north_body():
   assert d['raw']['OlivineCity'][47*d['size']['OlivineCity'][0]+x]>>12==1,'Port thin overhang must retain real sea, not a grass corner'
   frames(32,128);frames(30);assert current()=='OlivineCity' and pos()==(x,46),('Walked directly off dry pier onto sea',current(),pos())
   # Survey access was explicitly enabled at the actual Harbor Office desk.
   # walk performs native A/YES Surf interaction, never a player-state write.
   walk.__globals__['dry_only']=False
   walk((x,47));assert d['read']('gPlayerAvatar',1)&8 and pos()==(x,47),('Real sea under roof lost native Surf access',current(),pos())
   frames(48,128);frames(40);assert current()=='OlivineCity' and pos()==(x,47),('Surfed through port solid roof/body',current(),pos())
   walk((x,46));assert not d['read']('gPlayerAvatar',1)&8 and pos()==(x,46),'Native Surf disembark did not restore walking'
   walk.__globals__['dry_only']=True
  capture(f'port-north-body-column-{x}',north_body);lib.emu_image(str(out/(f'port-north-body-column-{x}.png')).encode());special.append(dict(action='Port north sea/overhang/body collision',column=x,surfable_overhang=[x,47],blocked_body=[x,48],normal_surf_and_disembark=True,result='PASS'))
 # An open door is not dependable if its outdoor arrival is a trapped apron.
 # Walk away to the main promenade, return around the outside of the facade,
 # then enter the other leaf; never cross an active door to fake the detour.
 def port_return():
  before=walk.__globals__['water_entries'];d['warp'](0);assert current()=='OlivineCity';walk((24,45));frames(60);walk((24,53));d['warp'](15);assert current()=='OlivineCity_PortTerminal';assert walk.__globals__['water_entries']==before,'Pedestrian boardwalk journey used Surf'
 go('OlivineCity_PortTerminal',0);capture('port-forecourt-boardwalk-return',port_return);special.append(dict(action='port exit, dry boardwalk to main promenade and right-leaf return',result='PASS'))
 # The lighthouse balcony overlooks sea; it is not a shore Surf entrance.
 # Try the native A interaction after pushing at each formerly open edge.
 for label,point,button in [('balcony-west-inner-rail',(2,5),16),('balcony-north-left-rail',(1,2),64)]:
  go(d['BALCONY'],0);walk(point)
  def push_rail():
   frames(32,button);frames(30);d['key'](1);frames(180);d['key'](1);frames(180)
   assert current()==d['BALCONY'] and pos()==point,(label,'Left elevated balcony',current(),pos())
   assert not d['read']('gPlayerAvatar',1)&8,(label,'Surf permitted over elevated railing')
   assert not d['read']('sLockFieldControls',1),(label,'Unexpected Surf/dialogue prompt')
  capture(label,push_rail);lib.emu_image(str(out/(label+'.png')).encode());special.append(dict(action=label,normal_controller_and_A=True,result='PASS'))
assert hashlib.sha256(source_save.read_bytes()).hexdigest()==save_hash,'Source battery file changed'
report=dict(recording_scope='Every required front video and every executed actual-arrival PNG'if a.record_fronts_only else'Every executed approach video',all_controller_cases_and_assertions_unchanged=True,visible_opening_contract=str(manifest_path),visible_opening_contract_sha256=hashlib.sha256(manifest_path.read_bytes()).hexdigest(),explicit_arrival_facing_required=a.require_facing,explicit_arrival_facing_required_for=a.require_facing_for,source_save_sha256=save_hash,source_save_unchanged=True,rom_sha256=hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest(),source_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),source_dirty=bool(subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=R)),setup='Read-only copied battery; cold Continue; normal controller travel. Only disclosed RAM encounter suppression and opt-in survey desk; no map/warp/position writes. Same-ROM trial snapshots.',results=results,special_journeys=special)
(out/'doorway-results.json').write_text(json.dumps(report,indent=2)+'\n');failures=[r for r in results if r['result']=='FAIL'];executed=sum(r['result']=='PASS' for r in results);skipped=sum(r['result']=='inaccessible lateral approach' for r in results)
print('QA09 doorway segments:',executed,'passed;',skipped,'physically unavailable lateral approaches;',len(failures),'failed;',len(special),'special journeys',flush=True);assert not failures,failures
