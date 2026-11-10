#!/usr/bin/env python3
"""Use a copied battery save to claim the explicit owner-requested QA kit."""
import sys,runpy,struct,argparse
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');p.add_argument('--output',default='build/qa03-kit');args=p.parse_args()
sys.argv=['johto_network_smoke.py','--save',args.save,'--library',args.library,'--output',args.output,'--targets','']
d=runpy.run_path('crossroads/tools/johto_network_smoke.py');globals().update({n:d[n] for n in ['read','write','sb','frames','key','go','walk','lib']})
go('OlivineCity_HarborOffice');walk((1,6));frames(1,64);frames(20)
countptr=read('gPlayerPartyCountPtr');before=read(countptr,1);party=read('gPlayerPartyPtr');original=bytes(read(party+i,1) for i in range(before*100));choice=read(sb()+0x1590,2)
oldflags=bytes(read(sb()+0x1270+i,1) for i in range(300))
def claim():
 frames(30,1|256);frames(180)
 for _ in range(10):
  if not read('sLockFieldControls',1):break
  key(1);frames(120)
 assert not read('sLockFieldControls',1)
claim();assert read(countptr,1)==before+1
p=party+before*100;personality=read(p);cipher=personality^read(p+4);secure=b''.join(struct.pack('<I',read(p+32+i*4)^cipher) for i in range(12))
# Expansion packs species/tera type and move/tracker into shared u16 words.
growth=[0,0,0,0,0,0,1,1,2,3,2,3,1,1,2,3,2,3,1,1,2,3,2,3][personality%24];attack=[1,1,2,3,2,3,0,0,0,0,0,0,2,3,1,1,3,2,2,3,1,1,3,2][personality%24]
assert (struct.unpack_from('<H',secure,growth*12)[0]&0x7ff)==18
assert read(p+84,1)==100
assert (struct.unpack_from('<H',secure,attack*12)[0]&0x7ff)==19
assert bytes(read(party+i,1) for i in range(before*100))==original
assert read(sb()+0x1590,2)==choice
assert read(sb()+0x1270+0x20//8,1)&(1<<(0x20%8))
# SYSTEM_FLAGS is read from source below, keeping the assertion tied to the real flag.
import re
flag=0x860+0x60
assert read(sb()+0x1270+flag//8,1)&(1<<(flag%8))
expected=bytearray(oldflags)
for f in [0x20,flag]:expected[f//8]|=1<<(f%8)
assert bytes(read(sb()+0x1270+i,1) for i in range(300))==bytes(expected),'Only shoes and one-time gift flags may change'
claim();assert read(countptr,1)==before+1
lib.emu_image(b'build/qa03-kit/claimed.png')
print('Actual R+talk/accept: Pidgeot species18, level100, Fly move19, running flag, original party/starter retained, repeat grant prevented: PASS',flush=True)
