#!/usr/bin/env python3
from pathlib import Path
from PIL import Image,ImageDraw
import struct,json,hashlib
P=Path(__file__).resolve().parent;m=json.loads((P/'manifest.json').read_text());report=[]
for e in m['entries']:
 d=P/'assets'/e['name'];png=Image.open(d/'tiles.png');raw=(d/'tiles.4bpp').read_bytes();pal=(d/'palette.gbapal').read_bytes();assert png.mode=='P' and png.size==(128,256)
 assert len(raw)==16384 and len(pal)==32 and max(png.getdata())<16
 # independent unpack of hardware nibble order vs indexed PNG tile ordering
 tiles=[]
 for k in range(512):
  a=[]
  for b in raw[k*32:(k+1)*32]:a += [b&15,b>>4]
  tiles.append(a);assert a==list(png.crop(((k%16)*8,(k//16)*8,(k%16)*8+8,(k//16)*8+8)).getdata())
 meta=struct.unpack('<448H',(d/'metatiles.bin').read_bytes());attrs=struct.unpack('<56H',(d/'metatile_attributes.bin').read_bytes());stamp=struct.unpack('<56H',(d/'stamp.bin').read_bytes())
 reconstructed=Image.new('P',(128,112));reconstructed.putpalette(png.getpalette())
 for idx in range(56):
  mx,my=idx%8,idx//8
  assert (stamp[idx]&1023)==512+idx and stamp[idx]>>12==3
  for q,v in enumerate(meta[idx*8+4:idx*8+8]):
   assert v>>12==6 and 512<=(v&1023)<1024 and not v&0xc00
   tile=Image.new('P',(8,8));tile.putdata(tiles[(v&1023)-512]);reconstructed.paste(tile,(mx*16+(q%2)*8,my*16+(q//2)*8))
  door=(mx,my) in [(3,6),(4,6)]
  assert attrs[idx]&255==(96 if door else 0)
  assert bool(stamp[idx]&0xc00)==(my>=5 and 1<=mx<=6 and not door)
 assert list(reconstructed.getdata())==list(Image.open(d/'building.png').getdata())
 reconstructed.save(d/'binary_roundtrip.png',transparency=0)
 # 16x16 minimal demonstration layout. Requires General primary and this secondary.
 demo=[0x3001]*256
 for y in range(7):demo[(y+2)*16+4:(y+2)*16+12]=stamp[y*8:y*8+8]
 (d/'demo_16x16_map.bin').write_bytes(struct.pack('<256H',*demo))
 e['sha256_4bpp']=hashlib.sha256(raw).hexdigest()
 report.append({'gym':e['name'],'passed':['indexed PNG 16 colors','GBA 4bpp round-trip','RGB555 palette length','56 metatiles','indices and palette bank','roof/facade layer flags','door behavior','collision stencil','binary art reconstruction'],'unique_tiles':e['tile_count'],'allocated_tiles':512,'storage_bytes':len(raw)})
(P/'manifest.json').write_text(json.dumps(m,indent=2));(P/'validation.json').write_text(json.dumps(report,indent=2));print('PASS: all eight assets, binary round trips and stencils.')
