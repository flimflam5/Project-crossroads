#!/usr/bin/env python3
"""Copied-save Continue at a gate landing and an obsolete blocked position.

Only the invalid-position fixture writes player XY in private test RAM, then uses
normal Save/cold Continue. Door/wall reproductions use controller movement only.
"""
import argparse,hashlib,json,runpy,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--output',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
sys.argv=['johto_network_smoke.py','--save',a.save,'--library',a.library,'--output',str(out),'--targets',''];d=runpy.run_path(str(Path(__file__).with_name('johto_network_smoke.py')));go,walk,read,write,frames,key,current,pos,lib,syms,sb=[d[n]for n in ['go','walk','read','write','frames','key','current','pos','lib','syms','sb']]
rows=[]
def save_continue(label,expected):
 count=read(read('gPlayerPartyCountPtr'),1);party=bytes(read(read('gPlayerPartyPtr')+i,1) for i in range(count*100));choice=read(sb()+0x1590,2)
 key(8);frames(90)
 for _ in range(12):
  cursor=read('sStartMenuCursorPos',1)
  if read(syms['sCurrentStartMenuActions']+cursor,1)==5:break
  key(128)
 else:raise AssertionError('Save menu missing')
 key(1);frames(180)
 for _ in range(8):key(1);frames(180)
 for _ in range(3):key(2);frames(180)
 assert read(syms['gMain']+4)==syms['CB2_Overworld']|1
 f=out/(label+'.sav');assert lib.emu_save(str(f).encode(),0)
 assert lib.emu_init(str(Path('pokeemerald.gba').resolve()).encode());assert lib.emu_save(str(f).encode(),1);frames(4500);key(8);frames(180);key(1);frames(300)
 assert current()=='EcruteakCity' and pos()==expected,(label,current(),pos(),expected)
 assert read(sb()+0x1590,2)==choice and bytes(read(read('gPlayerPartyPtr')+i,1) for i in range(count*100))==party
 lib.emu_image(str(out/(label+'.png')).encode());write('sWildEncountersDisabled',1,1);rows.append(dict(label=label,result='PASS',position=pos(),party_and_starter='exactly retained'));print(label,'PASS',flush=True)
go('EcruteakCity');walk((7,38));save_continue('outside-gate-normal-save',(7,38));walk((8,38))
# This is a deliberate obsolete-coordinate fixture, not claimed as naturally
# walked movement in the current ROM. Old QA08 A1 allowed6,40; the new wall does not.
walk((7,40));frames(90);player=syms['gObjectEvents']+read(syms['gPlayerAvatar']+5,1)*36
write(sb(),6,2);write(sb()+2,40,2)
for offset in [12,16,20]:write(player+offset,13,2);write(player+offset+2,47,2)
save_continue('old-gate-wall-coordinate-fixture',(7,40));walk((8,40))
(out/'results.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256(Path('pokeemerald.gba').read_bytes()).hexdigest(),setup='Original read-only battery copied. Normal menu saves and cold boots. Second fixture alone seeds obsolete player XY6,40 in private RAM; no map/warp/flag/party writes.',records=rows),indent=2)+'\n')
