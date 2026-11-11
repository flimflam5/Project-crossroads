#!/usr/bin/env python3
"""Actual controller service/ambient/practice tests of the delivery Olivine.

Uses a copied normal battery through the title and existing map network. Private
fixtures only reduce first-mon HP/set poison for heal/rest/loss checks. No other
party/box/bag/progress edits, no Pokemon/item grants and no coordinate writes.
Source save is hashed unchanged. Automated gameplay, not owner visual acceptance.
"""
import argparse,hashlib,json,runpy,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--save',type=Path,required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');p.add_argument('--output',type=Path,default=R/'build/olivine-service-check');p.add_argument('--skip-battle',action='store_true');a=p.parse_args();out=a.output;out.mkdir(parents=True,exist_ok=True);original_hash=hashlib.sha256(a.save.read_bytes()).hexdigest()
sys.argv=['johto_network_smoke.py','--save',str(a.save),'--library',a.library,'--output',str(out),'--targets',''];d=runpy.run_path(str(R/'crossroads/tools/johto_network_smoke.py'))
go,walk,read,write,frames,key,current,pos,close,lib,syms,sb=[d[n] for n in ['go','walk','read','write','frames','key','current','pos','close','lib','syms','sb']]
records=[]
def image(label):assert lib.emu_image(str(out/(label+'.png')).encode())
def memory(addr,size):return bytes(read(addr+i,1) for i in range(size))
def party():return memory(read('gPlayerPartyPtr'),read(read('gPlayerPartyCountPtr'),1)*100)
def task(name):return any(read(syms['gTasks']+i*40)==syms[name]|1 and read(syms['gTasks']+i*40+4,1) for i in range(16))
def talk(point,button=64):walk(point);frames(1,button);frames(20);key(1);frames(120)
def item_count(item):
 secret=read(read('gSaveBlock2Ptr')+0xac,4)&0xffff
 return sum(read(sb()+0x562+i*4,2)^secret for i in range(186) if read(sb()+0x560+i*4,2)==item)
def money():return read(sb()+0x490)^read(read('gSaveBlock2Ptr')+0xac)
def text(label):
 address=syms[label];b=bytearray()
 for i in range(768):
  value=read(address+i,1);b.append(value)
  if value==255:return bytes(b)
 raise AssertionError(('Unterminated text buffer',label))
def interact(event,label,expected_text=None):
 n=current();x,y=event['x'],event['y'];candidates=[((x,y+1),64),((x-1,y),16),((x+1,y),32),((x,y-1),128)]
 for point,button in candidates:
  if d['path'](n,point) is not None:break
 else:raise AssertionError((n,'No usable interaction approach',event))
 talk(point,button);assert read('sLockFieldControls',1),(n,label,'Interaction did not open')
 if expected_text:assert text('gStringVar4')==text(expected_text),(n,label,'Wrong actual displayed message')
 image(label);close();assert current()==n and pos()==point and not read('sLockFieldControls',1)
 records.append(dict(label=label,map=n,target=[x,y],approach=point,result='controller interaction, message, control return PASS'))
# Normal water rules for every service trip; no Surf-assisted path hides a door.
go('OlivineCity_HarborOffice');talk((1,6))
for _ in range(8):
 if not read('sLockFieldControls',1):break
 key(1);frames(180)
assert read('sJohtoTestAccess',1)==0
g=walk.__globals__;old_safe=g['safe']
def dry_safe(n,p):return old_safe(n,p) and d['raw'][n][p[1]*d['size'][n][0]+p[0]]>>12==3
g['safe']=dry_safe;g['route_cache'].clear()
choice=read(sb()+0x1590,2);count=read(read('gPlayerPartyCountPtr'),1)
# True nurse interaction and local respawn metadata.
go('OlivineCity_PokemonCenter_1F');walk((8,13));write(read('gPlayerPartyPtr')+86,1,2);talk((8,13))
for _ in range(12):key(1);frames(180)
close();p0=read('gPlayerPartyPtr');assert read(p0+86,2)==read(p0+88,2)>1
assert (read(sb()+0x1c,1),read(sb()+0x1d,1))==d['locations']['OlivineCity'];assert (read(sb()+0x20,2),read(sb()+0x22,2))==(16,34)
image('nurse-healed');records.append(dict(label='nurse-healed',result='actual nurse, full HP, Olivine heal metadata PASS'))
# Native PC power/menu/cancel, retaining every party and boxed-mon byte.
before_party=party();before_boxes=memory(read('gPokemonStoragePtr'),0x83d0);talk((12,11))
for _ in range(8):
 if task('Task_HandleMultichoiceInput'):break
 key(1);frames(90)
assert task('Task_HandleMultichoiceInput'),'Native PC menu was not reached';image('center-pc-menu');key(2);frames(240);close()
assert party()==before_party and memory(read('gPokemonStoragePtr'),0x83d0)==before_boxes
records.append(dict(label='center-pc-menu',result='actual power/menu/cancel, exact party/box bytes PASS'))
# All six receptionists must work from the normal customer-side front, never a
# convenient side route. The old zero-behavior counter blocked every front A.
for n,xs,staff_y in [('OlivineCity_PokemonCenter_1F',[2,6,11],2),('OlivineCity_PokemonCenter_B1F',[4,8,12],4)]:
 go(n)
 for x in xs:
  assert d['behavior'](n,x,staff_y+1)==0x80,(n,x,'Counter front lacks native MB_COUNTER')
  point=(x,staff_y+2);talk(point,64);assert read('sLockFieldControls',1),(n,x,'Front A did not reach staff')
  expected_id=next(i+1 for i,e in enumerate(d['maps'][n]['object_events']) if (e['x'],e['y'])==(x,staff_y))
  assert read('gSpecialVar_LastTalked',2)==expected_id,(n,x,'Wrong staff local ID')
  assert text('gStringVar4')==text('Hgss_CommunicationText'),(n,x,'Wrong actual receptionist message')
  image(n+'-front-desk-'+str(x));close();assert current()==n and pos()==point and not read('sLockFieldControls',1)
  records.append(dict(label=n+'-front-desk-'+str(x),map=n,staff=[x,staff_y],approach=point,actual_staff_local_id=expected_id,result='front A across native counter, exact actual text/local ID, control return PASS'))
go('OlivineCity_PokemonCenter_1F');interact(d['maps'][current()]['object_events'][1],'center-visitor')
# Actual original-stock purchase. No test money or item grants are used.
go('OlivineCity_Mart');talk((4,6),32)
for _ in range(3):
 if task('Task_ShopMenu'):break
 key(1);frames(180)
assert task('Task_ShopMenu');image('mart-menu');before_money=money();before_balls=item_count(1);assert before_money>=200
key(1);frames(300);assert task('Task_BuyMenu');image('mart-stock');key(1);frames(300);assert task('Task_BuyHowManyDialogueHandleInput')
key(1);frames(300);key(1);frames(300);key(1);frames(300)
assert money()==before_money-200 and item_count(1)==before_balls+1,('Purchase balance/item mismatch',before_money,money(),before_balls,item_count(1));image('mart-purchase')
for _ in range(8):key(2);frames(180)
close();assert current()=='OlivineCity_Mart' and not read('sLockFieldControls',1);records.append(dict(label='mart-purchase',result='real one Poke Ball purchase at200, decoded balance and quantity PASS',money_before=before_money,money_after=money(),quantity_before=before_balls,quantity_after=item_count(1)))
interact(d['maps'][current()]['object_events'][1],'mart-visitor')
# Joe's accepted rest interaction must never replace the selected Center.
go('OlivineCity_Residence');m=d['maps'][current()];rest=next(e for e in m['bg_events'] if e['script']=='Olivine_HomeRest');walk((0,5));p0=read('gPlayerPartyPtr');write(p0+86,1,2);heal=memory(sb()+0x1c,8)
talk((0,5),64);key(128);key(1);frames(180);assert read('sLockFieldControls',1)==0 and read(read('gPlayerPartyPtr')+86,2)==1,'Declining rest healed or locked controls';image('home-rest-declined')
write(read('gPlayerPartyPtr')+80,8,4);talk((0,5),64);key(1);frames(600);close();p0=read('gPlayerPartyPtr');assert read(p0+86,2)==read(p0+88,2) and read(p0+80,4)==0 and memory(sb()+0x1c,8)==heal
image('home-rest-accepted');records.append(dict(label='home-rest',result='NO retains1HP; YES heals HP/poison and retains chosen Center PASS'))
for e in m['bg_events']:
 if e['script']!='Olivine_HomeRest':interact(e,e['script'])
# All three canonical homes and their actual present residents.
for n in ['OlivineCity_FishingHouse','OlivineCity_TradeHouse','OlivineCity_SealHouse']:
 go(n)
 for index,e in enumerate(d['maps'][n]['object_events']):interact(e,n+'-resident-'+str(index+1))
# Cafe host through native counter behavior: deliberately two tiles distant.
go('OlivineCity_Cafe');assert d['behavior'](current(),10,4)==0x80,'Cafe service counter must use native MB_COUNTER';talk((9,4),16);assert read('sLockFieldControls',1);image('cafe-host-across-counter');close();assert current()=='OlivineCity_Cafe' and pos()==(9,4)
records.append(dict(label='cafe-host-across-counter',result='native MB_COUNTER conversation at distance2 and control return PASS'))
for index,e in enumerate(d['maps'][current()]['object_events'][1:]):interact(e,'cafe-visitor-'+str(index+1))
# Actual five new plaques, not only physical sign metatiles.
go('OlivineCity');signs=[e for e in d['maps'][current()]['bg_events'] if e['script'].startswith('Hgss_OlivineSign_')];assert len(signs)==5
for e in signs:interact(e,e['script'])
# Retain office terminal/boards/checklists, Harbor records/dispatch and ambient
# clerk. Starter rescue itself has its dedicated all-three-choice regression.
for n in ['OlivineCity_SilphOffice','OlivineCity_HarborOffice']:
 go(n)
 for e in d['maps'][n]['bg_events']:interact(e,e['script'])
 for e in d['maps'][n]['object_events']:
  if e['script'] not in ['Crossroads_EventScript_ChooseStarter','Johto_TestDesk']:interact(e,n+'-'+e['script'])
# Every maritime caretaker/visitor/beacon and actual wayfinding sign is used,
# including the source-isolated southern3F reached by the real balcony chain.
for n in ['OlivineCity_Lighthouse_'+str(i)+'F' for i in range(1,7)]+['OlivineCity_Lighthouse_Balcony','OlivineCity_PortTerminal','OlivineCity_PortQuay']:
 if n=='OlivineCity_Lighthouse_3F':go(n,5)
 elif n=='OlivineCity_Lighthouse_4F':go(n,0) # Source eastern component holds the public floor plaque.
 else:go(n)
 for index,e in enumerate(d['maps'][n]['object_events']):
  script=e['script'];expected=script+'_Text' if script.startswith('Area_') else script+'Text'
  interact(e,n+'-ambient-'+str(index+1),expected)
 for index,e in enumerate(d['maps'][n]['bg_events']):
  script=e['script'];expected=script+'_Text' if script=='Area_LighthouseView' else script+'Text'
  interact(e,n+'-wayfinding-'+str(index+1),expected)
go('OlivineCity_NeighborHouse')
for index,e in enumerate(d['maps'][current()]['object_events']):interact(e,'accepted-neighbor-'+str(index+1))
if not a.skip_battle:
 # Revisit the nurse to make local whiteout unambiguous, then lose an existing
 # optional Jasmine practice battle.1HP is a fixture, not difficulty evidence.
 assert count==1,'The disclosed1HP practice-loss fixture requires the copied single-starter test save'
 go('OlivineCity_PokemonCenter_1F');talk((8,13))
 for _ in range(12):key(1);frames(180)
 close();go('OlivineCity_Gym_Arena');talk((6,6));key(1);frames(120);key(1);frames(300)
 assert read(syms['gTrainerBattleParameter']+2,2)==855,'Wrong practice trainer';image('jasmine-practice-battle');write(read('gPlayerPartyPtr')+86,1,2)
 for _ in range(240):
  key(1);frames(120)
  if current()!='OlivineCity_Gym_Arena':break
 close();assert current()=='OlivineCity_PokemonCenter_1F' and pos()==(8,13),(current(),pos());p0=read('gPlayerPartyPtr');assert read(p0+86,2)==read(p0+88,2)>0;image('jasmine-loss-local-whiteout');records.append(dict(label='jasmine-loss-local-whiteout',result='actual trainer855 practice loss, local nurse arrival8,13 and full heal PASS'))
assert read(sb()+0x1590,2)==choice and read(read('gPlayerPartyCountPtr'),1)==count
assert read('sJohtoTestAccess',1)==0 and not read('gPlayerAvatar',1)&8
assert hashlib.sha256(a.save.read_bytes()).hexdigest()==original_hash,'Input battery changed'
(out/'results.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest(),source_battery_sha256=original_hash,source_battery_unchanged=True,setup='Normal copied-save title/Continue and controller movement; actual survey desk OFF and dry-only paths. Only first-mon HP/status test fixtures. Real existing shop money used. No other party/box/bag/progress edits, no Pokemon/item grants, and no map/warp/player coordinate writes.',battle_tested=not a.skip_battle,records=records),indent=2)+'\n')
print('Olivine actual nurse/PC/purchase/rest/houses/counter/signs/office/'+('practice-whiteout' if not a.skip_battle else 'battle-skipped')+': PASS',len(records),'checks',flush=True)
