#!/usr/bin/env python3
"""Pack original anonymous temple/theater NPC art into GBA16x32 frames."""
from pathlib import Path
from PIL import Image
import argparse
R=Path(__file__).resolve().parents[2];D=R/'graphics/object_events/pics/people/ecruteak';src=Image.open(D/'source.png');p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
for row,name in enumerate(['monk','performer']):
 cells=[]
 for c in range(3):
  im=src.crop((round(c*src.width/3),round(row*src.height/2),round((c+1)*src.width/3),round((row+1)*src.height/2)));a=im.getchannel('A').point(lambda n:255 if n>=210 else 0);im.putalpha(a);im=im.crop(a.getbbox());scale=min(16/im.width,28/im.height);cells.append(im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST))
 strip=Image.new('RGB',(sum(i.width for i in cells),32));x=0
 for im in cells:strip.paste(im,(x,0),im.getchannel('A'));x+=im.width
 palette=[0,0,0]+strip.quantize(colors=15,method=Image.Quantize.MEDIANCUT).getpalette()[:45];ref=Image.new('P',(1,1));ref.putpalette(palette+[0]*720);out=Image.new('P',(48,32));out.putpalette(palette)
 for c,im in enumerate(cells):
  indexed=im.convert('RGB').quantize(palette=ref,dither=Image.Dither.NONE);v=bytearray(indexed.tobytes());a=im.getchannel('A').tobytes()
  for i in range(len(v)):
   if a[i]<128:v[i]=0
   elif not v[i]:v[i]=1
  indexed=Image.frombytes('P',im.size,bytes(v));indexed.putpalette(palette);out.paste(indexed,(c*16+(16-im.width)//2,32-im.height))
 path=D/(name+'.png')
 if args.check:
  old=Image.open(path);assert old.tobytes()==out.tobytes() and old.getpalette()[:48]==palette
 else:out.save(path,bits=4,transparency=0)
print('Ecruteak monk/performer16x32 palette and frame packing: PASS')
