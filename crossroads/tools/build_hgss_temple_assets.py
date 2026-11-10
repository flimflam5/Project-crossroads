#!/usr/bin/env python3
"""Convert original reference-directed temple assets; no HGSS graphics embedded."""
from pathlib import Path
from PIL import Image
import struct,json,argparse
R=Path(__file__).resolve().parents[2];A=R/'crossroads/hgss/art/temple';D=R/'data/tilesets/secondary/hgss_temple';p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
spec=[('wood',(16,16)),('burned_floor',(16,16)),('stone',(16,16)),('tatami',(16,16)),('temple_wall',(64,32)),('burned_wall',(64,32)),('house_wall',(64,32)),('stage',(64,32)),('pillar',(16,48)),('statue',(16,32)),('prayer_table',(32,16)),('partition',(16,32)),('rail_h',(64,16)),('rail_v',(16,64)),('stairs',(32,32)),('ladder',(16,32))]
base_spec=spec.copy()
src=Image.open(A/'source.png');images={}
for i,(name,size) in enumerate(spec):
 x=i%4;y=i//4;cell=src.crop((round(x*src.width/4+6),round(y*src.height/4+6),round((x+1)*src.width/4-6),round((y+1)*src.height/4-6)))
 alpha=cell.getchannel('A').point(lambda n:255 if n>=220 else 0);cell.putalpha(alpha);box=alpha.getbbox();assert box;images[name]=cell.crop(box).resize(size,Image.Resampling.NEAREST)
extra=[('roof_nw',(32,32)),('roof_ne',(32,32)),('roof_sw',(32,32)),('roof_se',(32,32)),('gold_spire',(32,96)),('braces',(32,32)),('warp_pad',(16,16)),('ramp',(16,16)),('dark_pit',(32,32)),('rubble',(16,16)),('bed',(32,48)),('dining_table',(32,32)),('chair',(16,16)),('fridge',(16,32)),('cabinet',(32,32)),('television',(32,32))]
esrc=Image.open(A/'extra-source.png')
for i,(name,size) in enumerate(extra):
 x=i%4;y=i//4;im=esrc.crop((round(x*esrc.width/4+8),round(y*esrc.height/4+8),round((x+1)*esrc.width/4-8),round((y+1)*esrc.height/4-8)));alpha=im.getchannel('A').point(lambda n:255 if n>=220 else 0);im.putalpha(alpha);im=im.crop(alpha.getbbox());images[name]=im.resize(size,Image.Resampling.NEAREST)
spec+=extra
images['pillar_big']=images['pillar'].resize((32,80),Image.Resampling.NEAREST);spec.append(('pillar_big',(32,80)))
images['roof_skin']=images['roof_nw'].crop((16,16,32,32));spec.append(('roof_skin',(16,16)))
# Reuse the engine's crisp timber grain, palette-converted to temple wood.
# The generated floor study was too noisy at16x16; this retains actual GBA pixels.
native=Image.open(R/'data/tilesets/secondary/generic_building/tiles.png').crop((0,24,16,32))
for name,colors in [('wood',{2:(71,45,33),5:(148,112,84),6:(182,157,119)}),('burned_floor',{2:(44,31,27),5:(71,45,33),6:(110,78,54)})]:
 im=Image.new('RGBA',(16,16));im.putdata([colors[native.getpixel((x,y%8))]+(255,) for y in range(16) for x in range(16)]);images[name]=im
# One consistent GBA palette for timber, burgundy, tatami and gray stone.
strip=Image.new('RGB',(sum(im.width for im in images.values()),64));x=0
for im in images.values():strip.paste(im,(x,0),im.getchannel('A'));x+=im.width
palette=[v for c in [(0,0,0),(239,232,209),(182,157,119),(148,112,84),(110,78,54),(71,45,33),(44,31,27),(144,150,151),(83,95,101),(52,60,66),(104,142,114),(154,181,139),(71,107,91),(149,49,55),(91,28,39),(225,202,145)] for v in c];ref=Image.new('P',(1,1));ref.putpalette(palette+[0]*720)
roofpal=[v for c in [(0,0,0),(224,229,232),(169,183,205),(119,140,173),(77,99,141),(49,69,112),(29,44,82),(19,29,59),(9,17,39),(229,195,78),(182,139,39),(122,83,21),(71,58,35),(151,160,167),(83,98,112),(42,55,69)] for v in c]
roofref=Image.new('P',(1,1));roofref.putpalette(roofpal+[0]*720)
converted={}
sheet=Image.new('P',(128,256));sheet.putpalette(palette);unique={bytes(64):0};cursor=1;words=[];attrs=[];specs={}
def tile(im,bank=6):
 global cursor
 k=im.tobytes()
 if k not in unique:
  assert cursor<512;unique[k]=cursor;sheet.paste(im,(cursor%16*8,cursor//16*8));cursor+=1
 return (unique[k]+512)|(bank<<12)
def add(name,im,behavior=0,bank=6):
 start=512+len(attrs);w,h=im.width//16,im.height//16
 for y in range(h):
  for x in range(w):
   refs=[tile(im.crop((x*16+dx,y*16+dy,x*16+dx+8,y*16+dy+8)),bank) for dx,dy in [(0,0),(8,0),(0,8),(8,8)]]
   under=words[(specs['wood']['start']-512)*8+4:(specs['wood']['start']-512)*8+8] if 'wood' in specs and name not in ['wood','burned_floor','stone','tatami','void','braces','dark_pit'] and not name.startswith('roof_') else [0x6200]*4
   words.extend(under+refs);attrs.append((0 if name in ['pillar','pillar_big','gold_spire','statue','partition','rail_v'] and y<h-1 else 0x1000)|behavior)
 specs[name]=dict(start=start,width=w,height=h)
add('void',Image.new('P',(16,16)))
for name,size in spec:
 im=images[name];bank=7 if name.startswith('roof_') or name=='gold_spire' else 6;pal=roofpal if bank==7 else palette;indexed=im.convert('RGB').quantize(palette=roofref if bank==7 else ref,dither=Image.Dither.NONE);v=bytearray(indexed.tobytes());mask=im.getchannel('A').tobytes()
 for i in range(len(v)):
  if mask[i]<128:v[i]=0
  elif not v[i]:v[i]=1
 indexed=Image.frombytes('P',im.size,bytes(v));indexed.putpalette(pal);converted[name]=indexed;add(name,indexed,bank=bank)
 if not args.check:indexed.save(A/(name+'.png'),bits=4,transparency=0)
for name,size in base_spec[4:]+[('pillar_big',(32,80))]:
 original=specs[name]
 for theme in ['burned_floor','stone','tatami']:
  start=512+len(attrs);under=words[(specs[theme]['start']-512)*8+4:(specs[theme]['start']-512)*8+8]
  for i in range(original['width']*original['height']):
   k=original['start']-512+i;words.extend(under+words[k*8+4:k*8+8]);attrs.append(attrs[k])
  specs[name+'_'+theme]=dict(original,start=start)
for theme in ['stone','roof_skin']:
 a=specs['gold_spire'];start=512+len(attrs);under=words[(specs[theme]['start']-512)*8+4:(specs[theme]['start']-512)*8+8]
 for i in range(a['width']*a['height']):
  k=a['start']-512+i;words.extend(under+words[k*8+4:k*8+8]);attrs.append(attrs[k])
 specs['gold_spire_'+theme]=dict(a,start=start)
# Preserve stair artwork on every actual warp cell.
warp_variants={}
for name in ['wood','stairs','ladder']+[n+'_'+t for n in ['stairs','ladder'] for t in ['burned_floor','stone','tatami']]:
 a=specs[name]
 for i in range(a['width']*a['height']):
  old=a['start']+i;new=512+len(attrs);words.extend(words[(old-512)*8:(old-512)*8+8]);attrs.append(0x1061);warp_variants[str(old)]=new
# Reuse the wood/stone drawing with distinct native movement behavior.
for name,behavior in [('warp',0x61),('exit',0x65),('jump_east',0x38),('jump_west',0x39),('jump_north',0x3a),('jump_south',0x3b),('panel',0x67)]:
 if name.startswith('jump_'):
  angle={'jump_east':270,'jump_west':90,'jump_north':0,'jump_south':180}[name];add(name,converted['ramp'].rotate(angle),behavior)
 elif name in ['exit','panel']:add(name,converted['warp_pad'],behavior)
 else:
  base=specs['wood']['start']-512;start=512+len(attrs);words.extend(words[base*8:base*8+8]);attrs.append(0x1000|behavior);specs[name]=dict(start=start,width=1,height=1)
base=specs['stone']['start']-512;specs['stone_warp']=dict(start=512+len(attrs),width=1,height=1);words.extend(words[base*8:base*8+8]);attrs.append(0x1061)
assert len(attrs)<=512,('Temple metatile capacity',len(attrs))
def write(p,b):
 if isinstance(b,str):b=b.encode()
 if p.suffix=='.pal':b=b.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
 if args.check:assert p.exists() and p.read_bytes()==b,('Regenerate temple',str(p))
 elif not p.exists() or p.read_bytes()!=b:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
if args.check:
 old=Image.open(D/'tiles.png');assert old.tobytes()==sheet.tobytes() and old.getpalette()[:48]==palette
else:sheet.save(D/'tiles.png',bits=4)
write(D/'metatiles.bin',struct.pack('<'+str(len(words))+'H',*words));write(D/'metatile_attributes.bin',struct.pack('<'+str(len(attrs))+'H',*attrs))
write(D/'palettes/06.pal','JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,palette[i:i+3])) for i in range(0,48,3))+'\n')
write(D/'palettes/07.pal','JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,roofpal[i:i+3])) for i in range(0,48,3))+'\n')
write(A/'manifest.json',json.dumps(dict(specs=specs,warp_variants=warp_variants,tiles=cursor,metatiles=len(attrs),source='Original generated GBA adaptations of temple references; no HGSS graphics copied'),indent=2)+'\n')
print('Temple asset conversion:',cursor,'tiles;',len(attrs),'metatiles; PASS')
