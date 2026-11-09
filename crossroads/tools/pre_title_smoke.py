#!/usr/bin/env python3
"""Cold-boot the pre-title, exercise its cards/skips and preserve title controls."""
import argparse,ctypes as C,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2]
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--library',type=Path,required=True);ap.add_argument('--output',type=Path,default=R/'build/black-ledger-pre-title');a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
syms={}
for line in subprocess.check_output(['arm-none-eabi-nm','-an',str(R/'pokeemerald.elf')],text=True).splitlines():
 words=line.split()
 if len(words)==3:
  try:syms[words[2]]=int(words[0],16)
  except ValueError:pass
lib=C.CDLL(str(a.library.resolve()));lib.emu_init.argtypes=[C.c_char_p];lib.emu_init.restype=C.c_int;lib.emu_frames.argtypes=[C.c_int,C.c_int];lib.emu_read.argtypes=[C.c_uint,C.c_int];lib.emu_read.restype=C.c_uint;lib.emu_state.argtypes=[C.c_char_p,C.c_int];lib.emu_state.restype=C.c_int;lib.emu_image.argtypes=[C.c_char_p];lib.emu_image.restype=C.c_int
assert lib.emu_init(str(R/'pokeemerald.gba').encode())
def read(addr,width=4):return lib.emu_read(syms.get(addr,addr),width)
def frames(n=1,keys=0):lib.emu_frames(keys,n)
def callback():return read(syms['gMain']+4)
def scene():return read('sBlackLedgerIntroScene',1)
def wait_for(test,limit=1200):
 for _ in range(limit):
  if test():return
  frames()
 raise AssertionError('Timed out waiting for scene/callback')
intro=syms['CB2_BlackLedgerIntro']|1;title=syms['CB2_BlackLedgerTitle']|1;menu=syms['CB2_MainMenu']|1
wait_for(lambda:callback()==intro)
assert scene()==0
snapshot=a.output/'intro-start.snapshot';assert lib.emu_state(str(snapshot).encode(),0)
seen=[]
for target in range(3):
 wait_for(lambda:callback()==intro and scene()==target and read('sBlackLedgerIntroTimer',2)>=35)
 assert read('gMPlayInfo_BGM')!=syms['mus_black_ledger_title'],'Custom title track starts only at the actual title'
 seen.append(scene())
 assert read(0x04000008,2)&0x1f0c==(30<<8)|(2<<2),'Text BG uses separate char/map blocks'
 expected=(R/'graphics/intro/black_ledger/tiles.bin').read_bytes()
 assert bytes(read(0x06000000+i,1) for i in range(len(expected)))==expected
 assert any(read(0x06008020+i,1) for i in range(19000)),'Engine text glyphs must reach VRAM'
 assert lib.emu_image(str(a.output/f'scene-{target}.png').encode())
 if target==1:
  assert read(0x04000000,2)&0x2200==0x2200,'Harbor BG/window enabled'
  assert read(syms['sGpuRegBuffer']+0x44,2)==(44<<8)|112 # WIN0V is write-only on GBA
 else:assert read(0x04000000,2)&0x2200==0
wait_for(lambda:callback()==title)
frames(60)
assert seen==[0,1,2]
assert read('gMPlayInfo_BGM')==syms['mus_black_ledger_title']
assert lib.emu_image(str(a.output/'title-handoff.png').encode())
print('Cold boot: branded cards in order, isolated text/harbor VRAM, silent pre-title and actual title handoff PASS',flush=True)
# Exact current-ROM snapshots speed up controller cases; no RAM writes are made.
for target in range(3):
 for label,key in [('A',1),('B',2),('START',8)]:
  assert lib.emu_state(str(snapshot).encode(),1)
  wait_for(lambda:scene()==target and read('sBlackLedgerIntroTimer',2)>=35)
  frames(120,key) # Keep it held across the transition to expose input leakage.
  assert callback()==title,(target,label,'Held skip must not also start the main menu')
  frames(20)
  frames(1,8);frames(180)
  assert callback()==menu,(target,label,'Fresh Start must retain menu behavior')
  print('Controller skip/held key/released Start:',target,label,'PASS',flush=True)
# A skip during the first fade must be accepted rather than flashing a card.
assert lib.emu_state(str(snapshot).encode(),1)
frames(120,8);assert callback()==title
print('Skip during initial palette fade: PASS',flush=True)
# Actual reset chord while in the harbor must return through the new boot flow.
assert lib.emu_state(str(snapshot).encode(),1)
wait_for(lambda:scene()==1 and read('sBlackLedgerIntroTimer',2)>=35)
frames(3,15);frames(4)
wait_for(lambda:callback()==intro and scene()==0)
wait_for(lambda:callback()==title)
frames(60)
assert read('gMPlayInfo_BGM')==syms['mus_black_ledger_title']
print('Real soft reset during pre-title returns through branding and starts custom title music: PASS',flush=True)
print('Owner appearance/pacing QA and combined battery-save Continue are separate checks.',flush=True)
