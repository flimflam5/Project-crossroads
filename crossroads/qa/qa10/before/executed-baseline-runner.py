from pathlib import Path
import sys,runpy,json,hashlib,shutil,subprocess
R=Path('/workspace/Project-crossroads');sys.path.insert(0,str(R/'crossroads/tools'));out=R/'build/qa10-before-runtime';out.mkdir(exist_ok=True);romsha='df69e014e706168c56180828487a9ab12709a9bccd3dff063fee5f7af5d4f2f4';source=R/'build/area-delivery-sram/EcruteakCity_BellTower-save.state.sav';savehash=hashlib.sha256(source.read_bytes()).hexdigest();shutil.copyfile(source,out/'input-copy.sav')
assert hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest()==romsha
sys.argv=['johto_network_smoke.py','--save',str(out/'input-copy.sav'),'--library','/tmp/johto-bridge.so','--output',str(out),'--targets',''];d=runpy.run_path(str(R/'crossroads/tools/johto_network_smoke.py'));go,walk,frames,key,current,pos,close,read,lib=[d[n]for n in ['go','walk','frames','key','current','pos','close','read','lib']];records=[]
# Turn the actual optional Survey desk OFF, then use dry normal paths.
go('OlivineCity_HarborOffice');walk((1,6));frames(1,64);frames(20);key(1);frames(180);close();assert read('sJohtoTestAccess',1)==0
walk.__globals__['dry_only']=True;d['route_cache'].clear()
def facing():return read(d['syms']['gObjectEvents']+read(d['syms']['gPlayerAvatar']+5,1)*36+24,1)&15
def shot(label):frames(30);assert lib.emu_image(str(out/(label+'.png')).encode())
def clip(label,fn):
 g=walk.__globals__;old=g['frames'];local=globals()['frames'];folder=out/(label+'-frames');folder.mkdir(exist_ok=True);counter=[0]
 def record(n=60,k=0):
  while n:
   count=min(n,4);old(count,k);n-=count;lib.emu_image(str(folder/f'{counter[0]:04d}.png').encode());counter[0]+=1
 g['frames']=record;globals()['frames']=record
 try:fn()
 finally:g['frames']=old;globals()['frames']=local
 subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(out/(label+'.mp4'))],check=True)
def interact(event,label):
 n=current();x,y=event['x'],event['y']
 for p,k in [((x,y+1),64),((x-1,y),16),((x+1,y),32),((x,y-1),128)]:
  if d['path'](n,p)is not None:break
 else:raise AssertionError(('No physical approach',n,event))
 walk(p);frames(1,k);frames(20);shot(label+'-context');key(1);frames(140);assert read('sLockFieldControls',1),(label,'No message');shot(label+'-message');close();records.append(dict(case=label,map=n,event=event,position=list(pos()),facing=facing(),result='Normal controller sign/NPC message and control-return PASS'));print(label,'PASS',flush=True)
go('OlivineCity')
for event in d['maps'][current()]['bg_events']:interact(event,'city-sign-'+event['script'])
for label,p in [('city-port-north-approach',(23,46)),('city-port-forecourt',(23,53)),('city-directory-lot',(24,43)),('city-gym-sign-court',(9,15))]:walk(p);shot(label)
# Actual normal entrance/exit leaves; preserve arrival/facing evidence before walk-away.
port='OlivineCity_PortTerminal';quay='OlivineCity_PortQuay'
for i in range(len(d['maps'][port]['warp_events'])):
 go(port,i);e=d['maps'][port]['warp_events'][i];target=d['ids'][e['dest_map']];shot('terminal-before-leaf-'+str(i))
 def journey():d['warp'](i)
 if i in [0,1,2,3]:clip('terminal-leaf-'+str(i)+'-out',journey)
 else:journey()
 records.append(dict(case='terminal-out-'+str(i),source=port,leaf=[e['x'],e['y']],destination=current(),arrival=list(pos()),facing=facing(),result='PASS'));shot('terminal-arrival-'+str(i));d['warp'](int(e['dest_warp_id']));assert current()==port;records.append(dict(case='terminal-return-'+str(i),source=target,destination=current(),arrival=list(pos()),facing=facing(),result='PASS'))
go(quay);event=d['maps'][quay]['bg_events'][0];interact(event,'quay-ship-boarding-closed');shot('quay-current-ship');
# Show that the rail really blocks the source gangway approach; no fake warp.
walk((27,22));frames(1,64);frames(20)
def block():frames(48,64);frames(40)
clip('quay-gangway-current-solid',block);records.append(dict(case='gangway-baseline',position=list(pos()),facing=facing(),source_ship_warp_absent=not any((e['x'],e['y'])==(27,20)for e in d['maps'][quay]['warp_events']),result='Recorded existing solid rail/no ship interior'))
for n,p in [('OlivineCity_FishingHouse',(4,5)),('OlivineCity_Cafe',(7,6)),('OlivineCity_PortTerminal',(7,6))]:go(n);walk(p);shot(n+'-interior-context')
assert hashlib.sha256(source.read_bytes()).hexdigest()==savehash;assert hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest()==romsha
report=dict(phase='BEFORE QA10; actual QA09 delivery',source_revision='285cfa4ebddcb390a8a5bde6116748cbb5eaba6b',rom_sha256=romsha,source_battery_sha256=savehash,source_battery_unchanged=True,method='Cold normal Continue from private copied battery; normal go/walk/A inputs. RAM encounter suppression only; actual Survey OFF. No XY/map/warp writes. Native240x160 images and H264 movement clips.',records=records)
(out/'results.json').write_text(json.dumps(report,indent=2)+'\n');print('BASELINE COMPLETE',len(records),'records; source battery and ROM unchanged',flush=True)
