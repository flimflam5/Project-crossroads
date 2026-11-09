#!/usr/bin/env python3
"""Actual atlas, cross-group whiteout and ice sliding after normal old-save Continue."""
import sys,runpy,json,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--library',required=True);p.add_argument('--output',default='build/johto-recovery-check');a=p.parse_args()
sys.argv=['johto_network_smoke.py','--save',a.save,'--library',a.library,'--output',a.output,'--targets','']
d=runpy.run_path('crossroads/tools/johto_network_smoke.py')
go,walk,read,write,frames,key,current,pos,close,lib,syms,out=[d[n] for n in ['go','walk','read','write','frames','key','current','pos','close','lib','syms','args']];out=out.output
sb=lambda:read('gSaveBlock1Ptr')
go('CianwoodCity');walk((7,33));before=(current(),pos());frames(1,64);frames(20);key(1);frames(180)
assert read(syms['gMain']+4)==syms['CB2_Atlas']|1
nodes=json.load(open('crossroads/johto/atlas.json'))['nodes'];expected=next(i for i,n in enumerate(nodes) if n['name']=='CianwoodCity')
assert read('sAtlasPlayer',1)==expected
lib.emu_image(str(out/'cianwood-atlas.png').encode())
key(16);frames(30);assert read('sAtlasSelection',1)==(expected+1)%len(nodes)
key(2);frames(180);close();assert (current(),pos())==before
print('Actual group76 atlas board, player marker, cursor and field return: PASS',flush=True)
go('CianwoodCity_PokemonCenter_1F');walk((7,4));frames(1,64);frames(20);key(1);frames(180)
for _ in range(8):key(1);frames(180)
for _ in range(5):key(2);frames(60)
assert (read(sb()+0x1c,1),read(sb()+0x1d,1))==d['locations']['CianwoodCity']
go('OlivineCity_Gym_Arena');walk((6,4));frames(1,64);frames(20);write(read('gPlayerPartyPtr')+86,1,2)
key(1);frames(180);key(1);frames(120);key(1);frames(300)
for _ in range(150):
 key(1);frames(120)
 if current()!='OlivineCity_Gym_Arena':break
close();assert current()=='CianwoodCity_PokemonCenter_1F',(current(),pos())
p=read('gPlayerPartyPtr');assert read(p+86,2)==read(p+88,2)>0
assert read(sb()+0x1590,2)==d['choice'] and read(read('gPlayerPartyCountPtr'),1)==d['partycount']
lib.emu_image(str(out/'cianwood-whiteout.png').encode())
print('Actual battle loss returns to group76 Cianwood Center, heals, retains starter/party: PASS',flush=True)
go('IcePath_3F');walk((11,8));frames(16,32);frames(180)
assert pos()==(6,8),pos()
walk((6,9));lib.emu_image(str(out/'ice-slide.png').encode())
print('Actual Ice Path sliding and recovered walking control: PASS',flush=True)
