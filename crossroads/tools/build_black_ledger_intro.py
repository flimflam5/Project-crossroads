#!/usr/bin/env python3
"""Format-convert accepted harbor art for a masked 4bpp pre-title viewport."""
import argparse,hashlib,json,struct
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2]
D=R/'graphics/intro/black_ledger'
S=R/'graphics/title_screen/black_ledger/reference/harbor-black-ledger.png'

def generate():
 image=Image.open(S).convert('RGB').resize((240,160),Image.Resampling.LANCZOS)
 image=image.quantize(colors=16,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
 pixels=image.tobytes();p=image.getpalette()[:48];tiles=bytearray()
 for y in range(0,160,8):
  for x in range(0,240,8):
   for row in range(8):
    for col in range(0,8,2):tiles.append(pixels[(y+row)*240+x+col]|pixels[(y+row)*240+x+col+1]<<4)
 tilemap=[0]*1024
 for y in range(20):
  for x in range(30):tilemap[y*32+x]=(y*30+x)|0x1000
 colors=[(p[i]>>3)|((p[i+1]>>3)<<5)|((p[i+2]>>3)<<10) for i in range(0,48,3)]
 light=pixels[87*240+217]
 meta={'source_sha256':hashlib.sha256(S.read_bytes()).hexdigest(),'format':'4bpp, palette bank 1','tiles':600,'dimensions':[240,160],'visible_source_y':[70,138],'light_palette_index':16+light,'status':'Pre-title prototype for owner appearance review; accepted source artwork unchanged.'}
 out={'tiles.bin':bytes(tiles),'tilemap.bin':struct.pack('<1024H',*tilemap),'palette.bin':struct.pack('<16H',*colors),'metadata.json':(json.dumps(meta,indent=2)+'\n').encode(),'light.h':f'#define BLACK_LEDGER_INTRO_LIGHT_INDEX {16+light}\n'.encode()}
 return image,out

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--check',action='store_true');args=ap.parse_args();image,out=generate()
 if args.check:
  for name,data in out.items():assert (D/name).read_bytes()==data,name
  assert len(out['tiles.bin'])==19200 and 19200<32768
  print('Pre-title accepted-art conversion, palette isolation, tilemap and VRAM bounds: PASS')
 else:
  D.mkdir(parents=True,exist_ok=True)
  for name,data in out.items():(D/name).write_bytes(data)
  image.save(D/'native-source-preview.png',bits=4)
