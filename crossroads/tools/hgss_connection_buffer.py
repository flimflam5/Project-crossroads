"""Shared General-only terrain within scrolling distance of Ecruteak seams.

Different city facade tilesets must not be used to decode the neighbor's buffer.
No geography, encounters, events or IDs change; native grass tiles are retained.
"""
import struct

def repair(name,data,w,h,specs=None):
 if name not in ['EcruteakCity','JohtoRoute38','JohtoRoute42','JohtoRoute37']:return data
 t=list(struct.unpack('<'+str(w*h)+'H',data))
 for y in range(h):
  for x in range(w):
   applies=(name=='EcruteakCity' and (x<7 or x>=w-7 or y>=h-7) or name=='JohtoRoute38' and x>=w-7 or name=='JohtoRoute42' and x<7 or name=='JohtoRoute37' and y<7)
   if not applies:continue
   i=y*w+x;n=t[i]&1023
   if n<512:continue
   if name=='EcruteakCity':
    assert specs is not None
    if n in (specs['paving'],specs['earth']):t[i]=(t[i]&~1023)|0x114;continue
    matched=False
    for key in ['tree','autumn_tree']:
     offset=n-specs[key]['start']
     if 0<=offset<6:t[i]=(t[i]&~1023)|[0x1d4,0x1d5,0x1dc,0x1dd,0x1e6,0x1e7][offset];matched=True;break
    assert matched,('Facade intrudes into scrolling buffer',x,y,n)
   else:
    assert n in (0x202,0x3e8,0x3e9),('Unmapped secondary tile at city seam',name,x,y,n)
    t[i]=(t[i]&~1023)|({0x202:0x114,0x3e8:0x1e6,0x3e9:0x1e7}[n])
 return struct.pack('<'+str(w*h)+'H',*t)
