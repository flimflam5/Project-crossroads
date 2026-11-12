#!/usr/bin/env python3
"""Observe Joe's actual battle-back sprite during the existing first-loss test.

The reused harness discloses its fresh-game/1HP fixtures. This observer adds no
game-memory writes: it subdivides identical frame/input batches and compares an
active visible64x64 hardware sprite and palette against Joe's authored frames.
"""
import argparse
import ctypes as C
import hashlib
import json
import runpy
import shutil
import subprocess
import sys
from pathlib import Path

R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--library',default='/tmp/johto-bridge.so')
p.add_argument('--output',type=Path,required=True)
a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
syms={}
for line in subprocess.check_output([shutil.which('arm-none-eabi-nm')or'arm-none-eabi-nm','-an',str(R/'pokeemerald.elf')],text=True).splitlines():
    fields=line.split()
    if len(fields)==3:
        try:syms[fields[2]]=int(fields[0],16)
        except ValueError:pass
expected=(R/'build/assets/graphics/trainers/joe/back.png.4bpp').read_bytes()
palette=(R/'build/assets/graphics/trainers/joe/joe.pal.gbapal').read_bytes()
assert len(expected)==8192 and len(palette)==32
frames_expected={expected[i:i+2048]:i//2048 for i in range(0,len(expected),2048)}
original_cdll=C.CDLL;proof=[]


class FrameObserver:
    def __init__(self,lib):
        self.lib=lib
        self.raw=lib.emu_frames
        self.raw.argtypes=[C.c_int,C.c_int]
        self.argtypes=None

    def __call__(self,keys,count):
        if proof:return self.raw(keys,count)
        while count:
            step=min(4,count);self.raw(keys,step);count-=step
            if self.lib.emu_read(syms['gBattleTypeFlags'],4)&8:self.inspect()

    def inspect(self):
        read=self.lib.emu_read
        for i in range(64):
            address=syms['gSprites']+i*68
            if read(address+62,1)&5!=1:continue
            if read(address,2)>>14 or read(address+2,2)>>14!=3:continue
            attr=read(address+4,2);tile=attr&1023;bank=attr>>12
            sx=read(address+32,2)+read(address+36,2)
            sy=read(address+34,2)+read(address+38,2)
            sx=(sx+32768)%65536-32768;sy=(sy+32768)%65536-32768
            if not(0<=sx<240 and 0<=sy<160):continue
            actual_palette=bytes(read(0x05000200+bank*32+j,1)for j in range(32))
            if actual_palette!=palette:continue
            actual=bytes(read(0x06010000+tile*32+j,1)for j in range(2048))
            if actual not in frames_expected:continue
            path=a.output/'joe-battle-back.png';assert self.lib.emu_image(str(path).encode())
            proof.append(dict(result='PASS',sprite=i,position=[sx,sy],joe_authored_frame=frames_expected[actual],actual_obj_vram_sha256=hashlib.sha256(actual).hexdigest(),actual_obj_palette_sha256=hashlib.sha256(actual_palette).hexdigest(),native_frame=path.name,method='Visible active64x64 software OAM sprite, actual OBJ VRAM and hardware palette; identical controller frame/input totals; no observer game-memory writes'))
            print('Actual battle trainer-back Joe frame and hardware palette: PASS',proof[-1],flush=True)
            return


class BridgeProxy:
    def __init__(self,lib):
        self._lib=lib;self.emu_frames=FrameObserver(lib)
    def __getattr__(self,name):return getattr(self._lib,name)


def instrumented_cdll(*args,**kwargs):
    lib=original_cdll(*args,**kwargs)
    return BridgeProxy(lib)if hasattr(lib,'emu_frames')else lib


C.CDLL=instrumented_cdll
saved_argv=sys.argv
sys.argv=['emulator_smoke.py','--library',a.library,'--first-loss-only','--output',str(a.output)]
try:
    try:runpy.run_path(str(R/'crossroads/tools/emulator_smoke.py'),run_name='__main__')
    except SystemExit as error:
        if error.code not in [None,0]:raise
finally:
    C.CDLL=original_cdll;sys.argv=saved_argv
assert proof,'No actual visible Joe battle-back frame/palette was observed'
(a.output/'joe-battle-graphics-results.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest(),observer_writes_game_memory=False,reused_fixture='Existing emulator_smoke first-loss fresh rescue/1HP fixture, then actual optional Jasmine loss/local healing',records=proof),indent=2)+'\n')
