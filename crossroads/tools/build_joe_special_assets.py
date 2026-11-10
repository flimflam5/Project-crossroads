#!/usr/bin/env python3
"""Pack generated Joe action poses into existing engine frame contracts.

Art authored with image generation against owner walking sprites and engine poses.
This converter only crops atlas cells, scales, aligns and quantizes to Joe's palette.
"""
from PIL import Image
from pathlib import Path
import json,argparse
R=Path(__file__).resolve().parents[2];A=R/'graphics/object_events/pics/people/joe/corporate'
p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
base=Image.open(A/'walking.png');palette=base.getpalette()[:48];ref=Image.new('P',(1,1));ref.putpalette(palette+[0]*720)
src=Image.open(A/'reference/special-directions.png');field=Image.open(A/'reference/field-action-source.png')
def pose(row,col,fieldmove=False):
 im=field if fieldmove else src;cols,rows=(5,1) if fieldmove else (4,6)
 box=(round(col*im.width/cols),round(row*im.height/rows),round((col+1)*im.width/cols),round((row+1)*im.height/rows));im=im.crop(box)
 alpha=im.getchannel('A').point(lambda v:255 if v>=210 else 0);box=alpha.getbbox();assert box
 im=im.crop(box);alpha=alpha.crop(box);im.putalpha(alpha)
 target=24 if fieldmove else 24 if row==0 else 30;ratio=min(30/im.width,target/im.height);im=im.resize((max(1,round(im.width*ratio)),max(1,round(im.height*ratio))),Image.Resampling.NEAREST)
 indexed=im.convert('RGB').quantize(palette=ref,dither=Image.Dither.NONE);v=bytearray(indexed.tobytes());mask=im.getchannel('A').tobytes()
 for i in range(len(v)):
  if mask[i]<128:v[i]=0
  elif v[i]==0:v[i]=1
 indexed=Image.frombytes('P',im.size,bytes(v));indexed.putpalette(palette)
 canvas=Image.new('P',(32,32));canvas.putpalette(palette);canvas.paste(indexed,((32-im.width)//2,32-im.height));return canvas
standard=[0,1,2,0,0,1,1,2,2]
plans={
 'field_move':[pose(0,i,True) for i in range(5)],
 'surfing':[pose(0,c) for c in [0,0,1,1,2,2,3,3]],
 'underwater':[pose(1,c) for c in [0,1,2,3]],
 'mach_bike':[pose(2,c) for c in standard]+[pose(2,3)]*3,
 'acro_bike':[pose(2 if i<9 else 3,c) for i,c in enumerate(standard+[0]*4+[1]*4+[2]*4+[0]*2+[1]*2+[2]*2)]+[pose(2 if i<9 else 3,3) for i in [2,7,8,17,18,19,20,25,26]],
 'fishing':[pose(4,c) for c in [2]*4+[1]*4+[0]*4+[3]*4],
 'watering':[pose(5,c) for c in [0,0,1,1,2,2,3,3]],
}
for name,frames in plans.items():
 im=Image.new('P',(32*len(frames),32));im.putpalette(palette)
 for i,f in enumerate(frames):im.paste(f,(i*32,0))
 path=A/(name+'.png')
 if args.check:
  old=Image.open(path);assert old.size==im.size and old.tobytes()==im.tobytes() and old.getpalette()[:48]==palette,(name,'regenerate')
 else:im.save(path,bits=4,transparency=0)
print('Joe special-state frame contracts/palette conversion: PASS' if args.check else 'Packed Joe field, Surf, Dive, bikes, fishing and watering poses.')
