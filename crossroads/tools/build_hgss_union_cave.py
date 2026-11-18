#!/usr/bin/env python3
"""Reconstruct Union Cave topology from pinned HGSS permission references.

Adapted Heart & Soul cave tiles supply GBA art. Existing map IDs and prior six
warp indices remain intact. The two HGSS 1F/B2F connector chains must target
separate, physically reconstructed Ruins pockets. Normal playtesting, Surf,
old-save migration, terrain art and owner visual acceptance remain mandatory.
"""
import hashlib, io, json, struct, subprocess, sys, tempfile
from PIL import Image
from collections import Counter, defaultdict, deque
from pathlib import Path
from tileset_registration import upsert

R=Path(__file__).resolve().parents[2]
REF=R/'crossroads/hgss/canonical_events/union-cave-geometry.json'
PLAN=R/'crossroads/donor/hns-union-cave/hgss-corrected-warp-plan.json'
OUT='data/tilesets/primary/hgss_union_cave'
FLOORS={'UnionCave_1F':'MAP_UNION_CAVE_1F','UnionCave_2F':'MAP_UNION_CAVE_B1F','UnionCave_3F':'MAP_UNION_CAVE_B2F'}
DONOR={'UnionCave_1F_hns':(48,60),'UnionCave_B1F_hns':(48,48),'UnionCave_B2F_hns':(40,50)}
POCKETS={'UnionCave_1F':{6:('RuinsOfAlph_SouthwestPocket',0),7:('RuinsOfAlph_NorthwestPocket',0)}}

def pack(v):return struct.pack('<%dH'%len(v),*v)
def read16(path):
    b=path.read_bytes();assert len(b)%2==0;return list(struct.unpack('<%dH'%(len(b)//2),b))
def js(path):return json.loads((R/path).read_text())

def generate_assets(write):
    with tempfile.TemporaryDirectory(prefix='black-ledger-hgss-union-') as d:
        t=Path(d);subprocess.run([sys.executable,str(R/'crossroads/tools/prepare_hns_union_cave.py'),'--output',str(t)],check=True,stdout=subprocess.DEVNULL)
        # Private blank metatile for unreachable HGSS matrix space. Source
        # pixels/indices remain unchanged; blank art is appended to free slots.
        sheet=Image.open(t/'tiles.png');assert sheet.mode=='P' and sheet.width==128 and sheet.height>=88
        assert all(v==0 for v in sheet.crop((8,80,16,88)).get_flattened_data())
        sheet.paste(Image.new('P',(8,8),0),(8,80));buffer=io.BytesIO();sheet.save(buffer,format='PNG',optimize=False)
        write(OUT+'/tiles.png',buffer.getvalue())
        write(OUT+'/metatiles.bin',(t/'metatiles.bin').read_bytes()+pack([161]*8))
        write(OUT+'/metatile_attributes.bin',(t/'metatile_attributes.bin').read_bytes()+pack([0]))
        for i in range(16):
            src=t/'palettes'/f'{i if i<6 else 0:02}.pal'
            write(OUT+f'/palettes/{i:02}.pal',src.read_bytes())
        source={n:read16(t/(n+'.bin')) for n in DONOR};attrs=read16(t/'metatile_attributes.bin')
    name='HgssUnionCave';mark='HGSS UNION CAVE PRIVATE'
    sections={
      'graphics':f'const u32 gTilesetTiles_{name}[] = INCGFX_U32("{OUT}/tiles.png", ".4bpp.fastSmol");\nconst u16 gTilesetPalettes_{name}[][16] = {{\n'+''.join(f'    INCGFX_U16("{OUT}/palettes/{i:02}.pal", ".gbapal"),\n' for i in range(16))+'};\n',
      'metatiles':f'const u16 gMetatiles_{name}[] = INCBIN_U16("{OUT}/metatiles.bin");\nconst u16 gMetatileAttributes_{name}[] = INCBIN_U16("{OUT}/metatile_attributes.bin");\n',
      'headers':f'const struct Tileset gTileset_{name} = {{ .isCompressed=TRUE, .isSecondary=FALSE, .tiles=gTilesetTiles_{name}, .palettes=gTilesetPalettes_{name}, .metatiles=gMetatiles_{name}, .metatileAttributes=gMetatileAttributes_{name}, .callback=NULL }};\n',
      'externs':f'extern const struct Tileset gTileset_{name};\n'}
    for kind,path in [('graphics','src/data/tilesets/graphics.h'),('metatiles','src/data/tilesets/metatiles.h'),('headers','src/data/tilesets/headers.h'),('externs','include/tilesets.h')]:
        begin='// BEGIN '+mark;end='// END '+mark;body=begin+'\n#if !IS_FRLG\n'+sections[kind]+'#endif\n'+end
        write(path,upsert((R/path).read_text(),begin,end,body,externs=kind=='externs'))
    # Compare nearby donor walls/water to reconstruct an actual varied cave
    # rather than substitute a uniform block. Sampling is deterministic.
    def category(raw):
        if raw&0xc00:return 0
        if attrs[raw&1023]&255==0x15:return 2
        return 1
    catalog=defaultdict(Counter)
    for name,(w,h) in DONOR.items():
        values=source[name]
        for y in range(h):
            for x in range(w):
                raw=values[y*w+x];cls=category(raw);behavior=attrs[raw&1023]&255
                if cls==1 or (cls==0 and behavior not in (0,8)) or (cls==2 and behavior!=0x15):continue
                bits=0
                for i,(dx,dy) in enumerate(((0,-1),(1,0),(0,1),(-1,0))):
                    xx,yy=x+dx,y+dy
                    n=category(values[yy*w+xx]) if 0<=xx<w and 0<=yy<h else 0
                    if n==cls:bits|=1<<i
                # Wall collision and water elevation are kept from the donor.
                catalog[(cls,bits)][raw]+=1
    assert attrs[1]&255==8 and attrs[5]&255==0x61 and attrs[6]&255==0x65 and attrs[0]&255==0x15
    return attrs,catalog

def reference_planes(fact):
    cols,rows=fact['matrix_dimensions'];w,h=cols*32,rows*32;data=[0]*(w*h)
    for index,c in enumerate(fact['chunks']):
        x=(index%cols)*32;y=(index//cols)*32
        for j,p in enumerate(c['permissions']):data[(y+j//32)*w+x+j%32]=p
    return w,h,data

def flood(w,h,classes,start,allow_water):
    q=deque([start]);seen={start}
    while q:
        x,y=q.popleft()
        for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if not(0<=xx<w and 0<=yy<h) or (xx,yy) in seen:continue
            if classes[yy*w+xx]==0 or (not allow_water and classes[yy*w+xx]==2):continue
            seen.add((xx,yy));q.append((xx,yy))
    return seen

def build_plane(fact,attrs,catalog):
    w,h,perms=reference_planes(fact)
    # Conservative interpretation of referenced permission plane. Field actions
    # and height changes are not modeled; runtime playtesting is required.
    classes=[0 if n&0x8000 else 2 if n&255==0x15 else 1 for n in perms]
    # Source matrices include unmodeled exterior/void cells with a zero
    # permission value. Retain only the components anchored by actual HGSS
    # events; never turn those disconnected voids into traversable cave floor.
    reachable=set()
    for event in fact['warps']:
        start=(event['x'],event['z']);reachable|=flood(w,h,classes,start,True)
    for i,cls in enumerate(classes):
        if cls and (i%w,i//w) not in reachable:classes[i]=0
    # Keep one or two rings of authored wall around actual walkable space;
    # render the unmodeled interior of solid matrix void in black.
    wall_fringe=set(reachable)
    for _ in range(2):
        wall_fringe|={(xx,yy) for x,y in tuple(wall_fringe) for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)) if 0<=xx<w and 0<=yy<h}
    vals=[]
    for y in range(h):
        for x in range(w):
            i=y*w+x;cls=classes[i]
            if cls==0 and (x,y) not in wall_fringe:vals.append(0x0459);continue # appended black void metatile 89
            if cls==1:vals.append(0x3001);continue
            bits=0
            for j,(dx,dy) in enumerate(((0,-1),(1,0),(0,1),(-1,0))):
                xx,yy=x+dx,y+dy;n=classes[yy*w+xx] if 0<=xx<w and 0<=yy<h else 0
                if n==cls:bits|=1<<j
            candidates=catalog.get((cls,bits))
            if candidates:
                raw=candidates.most_common(1)[0][0]
                vals.append(((raw&1023)|0x400) if cls==0 else ((raw&1023)|0x1000))
            else:vals.append(0x040f if cls==0 else 0x1000)
    return w,h,classes,vals

def apply(maps,tiles,sizes,layouts,write):
    attrs,catalog=generate_assets(write);facts=js('crossroads/hgss/canonical_events/union-cave-geometry.json');plan=js('crossroads/donor/hns-union-cave/hgss-corrected-warp-plan.json')
    for name,refname in FLOORS.items():
        assert name in maps and all(p in maps for p in ('RuinsOfAlph_SouthwestPocket','RuinsOfAlph_NorthwestPocket')),'Complete Ruins pocket destinations before integrating cave'
        m=maps[name];fact=facts[refname];w,h,classes,values=build_plane(fact,attrs,catalog)
        layout=layouts[m['layout']];layout.update(width=w,height=h,primary_tileset='gTileset_HgssUnionCave',secondary_tileset='gTileset_WesternInteriors')
        old=m['warp_events'];assert len(old)=={'UnionCave_1F':3,'UnionCave_2F':2,'UnionCave_3F':1}[name]
        entries=sorted((e for e in plan['warps'] if e['existing_map']==name),key=lambda e:e['proposed_index'])
        assert [e['proposed_index'] for e in entries]==list(range(len(entries)))
        warps=[]
        for e in entries:
            x,y=e['hgss_x'],e['hgss_y'];index=e['proposed_index'];dst=e['destination'];target=e['destination_index']
            if index in POCKETS.get(name,{}):dst,target=POCKETS[name][index]
            assert dst in maps,(name,index,dst)
            target_id=maps[dst]['id']
            if index<len(old):assert (old[index]['dest_map'],int(old[index]['dest_warp_id']))==(target_id,target)
            # 0x65 is the native south-facing cave exit; 0x61 is a ladder.
            values[y*w+x]=0x3006 if e['destination'] in ('JohtoRoute32','JohtoRoute33','RuinsOfAlph') else 0x3005
            classes[y*w+x]=1
            warps.append(dict(x=x,y=y,elevation=0,dest_map=target_id,dest_warp_id=str(target)))
        m['warp_events']=warps;sizes[name]=(w,h);tiles[name]=values
        # Keep both existing guide and notes scripts. Relocate only their event
        # positions onto ordinary accessible ground in the public dry component.
        start=(fact['warps'][0]['x'],fact['warps'][0]['z']);public=flood(w,h,classes,start,False)
        occupied={(e['x'],e['y']) for e in warps}
        floor=[(x,y) for x,y in public if values[y*w+x]==0x3001 and (x,y) not in occupied]
        assert len(floor)>4,(name,'no safe place for retained interactions')
        floor.sort(key=lambda p:abs(p[0]-start[0])+abs(p[1]-start[1]))
        for group in ('object_events','bg_events'):
            for event in m[group]:
                while floor and any(abs(floor[0][0]-x)+abs(floor[0][1]-y)<2 for x,y in occupied):floor.pop(0)
                x,y=floor.pop(0);event['x']=x;event['y']=y;occupied.add((x,y))
        # Bit0=dry, bit1=surf, bit2=public dry fallback. Plain selected
        # floor tiles have no authored foreground; warps and actors excluded.
        water_reachable=set()
        dry_reachable=set()
        for e in fact['warps']:
            p=(e['x'],e['z']);dry_reachable|=flood(w,h,classes,p,False);water_reachable|=flood(w,h,classes,p,True)
        mask=bytearray(w*h)
        for y in range(h):
            for x in range(w):
                i=y*w+x;p=(x,y)
                if p in occupied:continue
                if p in dry_reachable and values[i]==0x3001:mask[i]|=1
                if p in water_reachable and classes[i]==2:mask[i]|=2
                if p in public and mask[i]&1:mask[i]|=4
        assert all(not(v&4) or v&1 for v in mask) and sum(bool(v&4) for v in mask)>10
        write(f'data/layouts/{name}/safe_continue.bin',bytes(mask))
    print('HGSS Union Cave: 3 reference-shaped floors, six old warp indices and two separate connector chains; runtime and owner QA required.')
