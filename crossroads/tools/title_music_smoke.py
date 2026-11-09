#!/usr/bin/env python3
"""Cold-boot audio, actual sample progression/wrap, Start fade and reset checks."""
import argparse,array,ctypes as C,json,math,subprocess,wave
from pathlib import Path
r=Path(__file__).resolve().parents[2]
ap=argparse.ArgumentParser();ap.add_argument('--library',type=Path,required=True);ap.add_argument('--output',type=Path,default=r/'build/title-music-smoke');a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
syms={}
for line in subprocess.check_output(['arm-none-eabi-nm','-an',str(r/'pokeemerald.elf')],text=True).splitlines():
 parts=line.split()
 if len(parts)==3:
  try:syms[parts[2]]=int(parts[0],16)
  except ValueError:pass
lib=C.CDLL(str(a.library.resolve()));lib.emu_init.argtypes=[C.c_char_p];lib.emu_init.restype=C.c_int;lib.emu_frames.argtypes=[C.c_int,C.c_int];lib.emu_read.argtypes=[C.c_uint,C.c_int];lib.emu_read.restype=C.c_uint;lib.emu_audio.argtypes=[C.c_char_p,C.c_int];lib.emu_audio.restype=C.c_int
assert lib.emu_init(str(r/'pokeemerald.gba').encode())
def read(address,width=4):return lib.emu_read(syms.get(address,address),width)
def frames(n,k=0):lib.emu_frames(k,n)
def active():
 return [syms['gSoundInfo']+0x50+i*64 for i in range(12) if read(syms['gSoundInfo']+0x50+i*64+36)==syms['BlackLedgerTitleWave'] and read(syms['gSoundInfo']+0x50+i*64,1)&0xc7]
frames(4500)
assert read(syms['gMain']+4)==syms['CB2_BlackLedgerTitle']|1
assert read('gMPlayInfo_BGM')==syms['mus_black_ledger_title']
assert read(syms['BlackLedgerTitleWave']+4)==31536*1024
assert read(syms['BlackLedgerTitleWave']+12)==2522880
assert len(active())==1
assert read(syms['gSoundInfo']+8,1)==9, 'Title mixer must use 31.5 kHz'
assert read(syms['gSoundInfo']+7,1)==15
assert read(0x04000089,1)&0xc0==0, 'Title DAC must use 9-bit mode'
assert read(active()[0]+1,1)&8, 'Fixed-rate voice must avoid resampling'
raw=a.output/'title-audio.s16le';assert lib.emu_audio(str(raw).encode(),180)
samples=array.array('h',raw.read_bytes());rms=math.sqrt(sum(v*v for v in samples)/len(samples));peak=max(abs(v) for v in samples)
assert rms>20 and peak<32767,('Audio silent or clipped',rms,peak)
with wave.open(str(a.output/'title-audio.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(32768);w.writeframes(samples.tobytes())
print('Actual emulator audio signal: PASS; RMS',round(rms,1),'peak',peak,flush=True)
last=read(active()[0]+40);wrapped=False
for _ in range(48):
 frames(120);assert read(syms['gMain']+4)==syms['CB2_BlackLedgerTitle']|1
 channels=active();assert len(channels)==1
 now=read(channels[0]+40)
 assert syms['BlackLedgerTitleSamples']<=now<syms['BlackLedgerTitleSamplesEnd']
 if now<last:wrapped=True
 last=now
assert wrapped,'The actual sound channel must wrap across the full-track loop'
print('96 seconds of continued title playback, bounded sample pointer and actual end-to-start loop: PASS',flush=True)
frames(1,8);frames(180)
assert read(syms['gMain']+4)==syms['CB2_MainMenu']|1
assert not active(),'Title sample must fade/stop on Start'
assert read(syms['gSoundInfo']+8,1)==4, 'Restore normal gameplay frequency'
assert read(syms['gSoundInfo']+7,1)==12, 'Restore normal gameplay volume'
assert read(0x04000089,1)&0xc0==0x40, 'Restore normal gameplay DAC mode'
frames(3,15);frames(4500)
assert read(syms['gMain']+4)==syms['CB2_BlackLedgerTitle']|1
assert read('gMPlayInfo_BGM')==syms['mus_black_ledger_title'] and len(active())==1
print('Start reaches menu, sample stops, soft reset restarts custom title music: PASS',flush=True)
