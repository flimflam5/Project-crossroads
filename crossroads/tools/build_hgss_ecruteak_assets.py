#!/usr/bin/env python3
"""Quantize reference-directed facades into isolated Ecruteak GBA tilesets.

Never overwrites shared General/Slateport graphics. Native terrain and animation
slots are reserved before assigning building tiles. Stable map IDs are unrelated.
"""
import json,struct,argparse,hashlib
from pathlib import Path
from PIL import Image
from hgss_ecruteak_terrain import PAVING,neutral_metadata,neutral_graphics
R=Path(__file__).resolve().parents[2]
A=R/'crossroads/hgss/art';P=R/'data/tilesets/primary/hgss_ecruteak';S=R/'data/tilesets/secondary/hgss_ecruteak'
SPECS=[('gate','gate',(0,0,1536,1024),(112,112),2,3),('house','a',(750,0,1250,724),(80,64),7,3),('barrier','a',(1280,0,2172,724),(160,80),7,7),('burned','b',(0,0,565,724),(96,112),8,3),('theater','b',(565,0,1175,724),(96,80),9,3),('center','b',(1180,0,1665,724),(80,80),10,2),('mart','b',(1670,0,2172,724),(80,64),11,1)]
# Every primary terrain metatile used by the authored city/trail. Animation slots
#432..511 are reserved even when not currently referenced, preventing live corruption.
TERRAIN=[0,1,3,4,13,0xc6,0x24,0x15,0x19,0x71,0x75,0x7c,0x7d,0xa7,0x170,0x1d4,0x1d5,0x1dc,0x1dd,0x1e4,0x1e5,PAVING]
def generate(check=False,variant="city"):
 spec_list=SPECS if variant=="city" else [("bell","tower",(0,0,724,2172),(112,304),8,3),("trail_station","trail",(0,0,1774,887),(160,80),7,8)]
 primary_dir=P if variant=="city" else R/"data/tilesets/primary/hgss_bell"
 secondary_dir=S if variant=="city" else R/"data/tilesets/secondary/hgss_bell"
 def write(p,b):
  if isinstance(b,str):b=b.encode()
  # Match .gitattributes and clean checkouts exactly; keep strict byte checks.
  if p.suffix=='.pal':b=b.replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
  if check:assert p.read_bytes()==b,('Regenerate',str(p))
  elif not p.exists() or p.read_bytes()!=b:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
 general=R/'data/tilesets/primary/general';gm,ga=neutral_metadata(struct.unpack('<4096H',(general/'metatiles.bin').read_bytes()),struct.unpack('<512H',(general/'metatile_attributes.bin').read_bytes()))
 from hgss_ecruteak_family import route_primary_ids,route_primary_graphics,GATE_PRIMARY
 family_ids=route_primary_ids()-set(range(GATE_PRIMARY,GATE_PRIMARY+49)) if variant=='city' else set()
 reserved=set(range(432,512))|{v&1023 for n in set(TERRAIN)|family_ids for v in gm[n*8:n*8+8]}|(route_primary_graphics() if variant=='city' else set())
 free=[n for n in range(1024) if n>=512 or n not in reserved];primary=neutral_graphics();secondary=Image.new('P',(128,256));secondary.putpalette(primary.getpalette())
 images={}
 for name,src,box,size,bank,door in spec_list:
  im=Image.open(A/('gate-facade-source.png' if src=='gate' else 'bell-tower-source.png' if src=='tower' else 'trail-station-source.png' if src=='trail' else f'ecruteak-facades-{src}.png')).convert('RGBA').crop(box);alpha=im.getchannel('A').point(lambda x:255 if x>=(250 if src=='gate' else 180) else 0);im.putalpha(alpha);im=im.crop(alpha.getbbox());im=im.resize(size,Image.Resampling.NEAREST);images[name]=im
 pals={}
 for bank in [2,4]:pals[bank]=[v for line in (general/f'palettes/{bank:02}.pal').read_text().splitlines()[3:] for v in map(int,line.split())]
 for bank in range(6,12):
  ims=[images[n] for n,src,box,size,b,d in spec_list if b==bank]
  if not ims:continue
  strip=Image.new('RGB',(sum(i.width for i in ims),max(i.height for i in ims)))
  x=0
  for im in ims:strip.paste(im,(x,0),im.getchannel('A'));x+=im.width
  colors=strip.quantize(colors=11,method=Image.Quantize.MEDIANCUT).getpalette()[:33]+[0]*12;pals[bank]=[0,0,0]+colors
 words=[];attrs=[];unique={};cursor=0;specs={}
 # Transparent tile has a real zero source; don't depend on mutable General tile0.
 def alloc(tile,bank):
  nonlocal cursor
  key=tile.tobytes()
  if key not in unique:
   assert cursor<len(free),('Graphics capacity',cursor,len(free));n=free[cursor];cursor+=1;unique[key]=n
   sheet=primary if n<512 else secondary;i=n%512;sheet.paste(tile,(i%16*8,i//16*8))
   # Hardware H/V flips save graphics slots without changing a single displayed
   # pixel. Palette and metatile identities are independent of this packing.
   for flags,im in [(0x400,tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)),(0x800,tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)),(0xc00,tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT).transpose(Image.Transpose.FLIP_TOP_BOTTOM))]:unique.setdefault(im.tobytes(),n|flags)
  return unique[key]|(bank<<12)
 under=list(gm[8:12]);empty=alloc(Image.new('P',(8,8)),6)
 for name,src,box,size,bank,door in spec_list:
  print('Allocating',name,'after',cursor,'tiles',flush=True)
  im=images[name];ref=Image.new('P',(1,1));ref.putpalette(pals[bank]+[0]*(768-48));indexed=im.convert('RGB').quantize(palette=ref,dither=Image.Dither.NONE);values=bytearray(indexed.tobytes());alpha=im.getchannel('A').tobytes()
  for i in range(len(values)):
   if alpha[i]<128:values[i]=0
   elif not values[i]:values[i]=1
  indexed=Image.frombytes('P',im.size,bytes(values));indexed.putpalette(pals[bank]);write(A/(name+'-native.png'),b'') if False else None
  gate_layers={2:indexed}
  if name=='gate':
   ref4=Image.new('P',(1,1));ref4.putpalette(pals[4]+[0]*720);q=im.convert('RGB').quantize(palette=ref4,dither=Image.Dither.NONE);vals=bytearray(q.tobytes())
   for i,v in enumerate(vals):vals[i]=0 if alpha[i]<128 else v or 1
   q=Image.frombytes('P',im.size,bytes(vals));q.putpalette(pals[4]);gate_layers[4]=q
   preview=indexed.convert('RGBA');preview.paste(q.convert('RGBA').crop((0,64,im.width,im.height)),(0,64))
   if not check:preview.save(A/(name+'-native.png'))
  elif not check:indexed.save(A/(name+'-native.png'),bits=4)
  w,h=size[0]//16,size[1]//16;start=512+len(attrs)
  gate_preview=Image.new('RGBA',size) if name=='gate' else None
  # The Theater and Barrier have two visible door leaves. Both are real
  # thresholds; metadata/collision must not turn the left leaf into a wall.
  doors=[] if name=='gate' else [(door,h-1)]+([(door-1,h-1)] if name in ('barrier','theater') else [])
  for y in range(h):
   for x in range(w):
    draw=gate_layers[4 if y>=4 else 2] if name=='gate' else indexed;drawbank=(4 if y>=4 else 2) if name=='gate' else bank
    # A tileable center preserves the new gate silhouette while fitting the
    # hardware pool alongside the immutable owner Gym. Existing facades are
    # never resampled/repeated by this conversion rule.
    source_x=3 if name=='gate' and (1<x<5 if y<4 else 0<x<6) else x
    top=[alloc(draw.crop((source_x*16+dx,y*16+dy,source_x*16+dx+8,y*16+dy+8)),drawbank) for dx,dy in [(0,0),(8,0),(0,8),(8,8)]]
    if gate_preview is not None:
     patch=draw.crop((source_x*16,y*16,source_x*16+16,y*16+16));patch.info['transparency']=0;gate_preview.paste(patch.convert('RGBA'),(x*16,y*16))
    ground=list(gm[PAVING*8:PAVING*8+4]) if name=='gate' else under
    words.extend(ground+top);attrs.append((0x1000 if (y>=4 if name=='gate' else y>=h-2) else 0)|(0x60 if (x,y) in doors else 0x61 if name=='trail_station' and (x,y)==(door,h-2) else 0))
  specs[name]=dict(start=start,width=w,height=h,door_x=door,door_y=h-1,door_cells=[list(p) for p in doors],palette=bank,solid_footprint=[[x,y] for y in range(h) for x in range(w) if y>0 and (y>=h-2 or 0<x<w-1) and (x,y) not in doors],walkable_overhang=[[x,y] for y in range(h) for x in range(w) if y==0 or (y<h-2 and x in (0,w-1))])
  if gate_preview is not None and not check:gate_preview.save(A/'gate-native.png')
 # Original General canopy pixels are in the bottom layer, so simply choosing
 # NORMAL does not put leaves over Joe. Duplicate only leaf colors (1..4 in the
 # General tree palette) into the foreground. Grass/shadow colors stay below;
 # the static tree image is pixel-identical and the root footprint stays solid.
 original=Image.open(general/'tiles.png')
 def tree_words(n,bank):
  row=[(v&0xfff)|(bank<<12) for v in gm[n*8:n*8+8]]
  if n in [0x1d4,0x1d5]:
   for j,v in enumerate(row[:4]):
    i=v&1023;tile=original.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8))
    if v&0x400:tile=tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if v&0x800:tile=tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    mask=Image.frombytes('P',(8,8),bytes(c if 1<=c<=4 else 0 for c in tile.tobytes()))
    row[4+j]=alloc(mask,bank)
  return row
 # Solid roots draw behind Joe approached from the south; canopy masks above.
 for n in [0x1d4,0x1d5,0x1dc,0x1dd]:
  words.extend(tree_words(n,2));attrs.append(0x1000 if n in [0x1dc,0x1dd] else 0)
 specs['tree']=dict(start=512+len(attrs)-4,width=2,height=2)
 for n in [0x1d4,0x1d5,0x1dc,0x1dd]:
  words.extend(tree_words(n,5));attrs.append(0x1000 if n in [0x1dc,0x1dd] else 0)
 specs['autumn_tree']=dict(start=512+len(attrs)-4,width=2,height=2)
 # A source-compatible paved ground tile with its own palette.
 slate=R/'data/tilesets/secondary/slateport';sheet=Image.open(slate/'tiles.png');stone=sheet.crop((6*8,4*8,7*8,5*8));stone_ref=alloc(stone,12)
 specs['paving']=512+len(attrs);words.extend([stone_ref]*4+[empty]*4);attrs.append(0x1000)
 colors=[pals[8][j:j+3] for j in range(3,48,3)]
 soilindex=1+min(range(15),key=lambda j:sum((colors[j][k]-[142,122,102][k])**2 for k in range(3)))
 soil=Image.new('P',(8,8),soilindex);soilref=alloc(soil,8)
 specs['earth']=512+len(attrs);words.extend([soilref]*4+[empty]*4);attrs.append(0x1000)
 assert len(attrs)<=512
 specs['leaf_ground']=512+len(attrs);words.extend([(v&0xfff)|(5<<12) for v in gm[8:16]]);attrs.append(0x1000)
 if variant=='city':
  from hgss_ecruteak_courtyard import assets as courtyard_assets
  courtyard_assets(alloc,words,attrs,specs,empty)
 if variant=='city':
  # Only the gate uses a previously unused PRIMARY metatile range. Its graphics
  # also fit below512, so routes retain their original WesternCity secondary.
  s=specs['gate'];old=s['start']-512;gm[GATE_PRIMARY*8:(GATE_PRIMARY+49)*8]=words[old*8:(old+49)*8];ga[GATE_PRIMARY:GATE_PRIMARY+49]=attrs[old:old+49]
  assert max(v&1023 for v in gm[GATE_PRIMARY*8:(GATE_PRIMARY+49)*8])<432
  s['secondary_start']=s['start'];s['start']=GATE_PRIMARY
 for path,im in [(primary_dir/'tiles.png',primary),(secondary_dir/'tiles.png',secondary)]:
  if not check:path.parent.mkdir(parents=True,exist_ok=True);im.save(path,bits=4)
 for i in range(16):
  native=(general/f'palettes/{i:02}.pal').read_bytes()
  if i==5:
   colors=[tuple(map(int,l.split())) for l in (general/'palettes/02.pal').read_text().splitlines()[3:]]
   native=('JASC-PAL\n0100\n16\n'+'\n'.join(f'{min(255,int(g*1.2))} {int(g*.55)} {int(g*.13)}' for r,g,b in colors)+'\n').encode()
  write(primary_dir/f'palettes/{i:02}.pal',native)
  pal=pals.get(i)
  if i==12:
   old=[tuple(map(int,l.split())) for l in (R/'data/tilesets/secondary/slateport/palettes/06.pal').read_text().splitlines()[3:]]
   pal=[v for rgb in old for v in (int(sum(rgb)/3*.8),int(sum(rgb)/3*.84),int(sum(rgb)/3*.73))]
  write(secondary_dir/f'palettes/{i:02}.pal','JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,pal[j:j+3])) for j in range(0,48,3))+'\n' if pal else (general/f'palettes/{i:02}.pal').read_bytes())
 write(primary_dir/'metatiles.bin',struct.pack('<4096H',*gm));write(primary_dir/'metatile_attributes.bin',struct.pack('<512H',*ga));write(secondary_dir/'metatiles.bin',struct.pack('<'+str(len(words))+'H',*words));write(secondary_dir/'metatile_attributes.bin',struct.pack('<'+str(len(attrs))+'H',*attrs));write(A/('native-manifest.json' if variant=='city' else 'bell-native-manifest.json'),json.dumps(dict(specs=specs,terrain=TERRAIN,reserved_primary_tiles=sorted(reserved),allocated_tiles=cursor,available_tiles=len(free)),indent=2)+'\n')
 print('HGSS-directed Ecruteak facades:',cursor,'of',len(free),'available graphics tiles;',len(attrs),'metatiles. Visual acceptance pending.')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--variant',choices=['city','bell'],default='city');args=p.parse_args();generate(args.check,args.variant)
