#!/usr/bin/env python3
"""Reconstruct Union Cave topology from pinned HGSS permission references.

Adapted Heart & Soul cave tiles supply GBA art. Existing map IDs and prior six
warp indices remain intact. The two HGSS 1F/B2F connector chains must target
separate, physically reconstructed Ruins pockets. Normal playtesting, Surf,
old-save migration, terrain art and owner visual acceptance remain mandatory.
"""
import copy, hashlib, io, json, struct, subprocess, sys, tempfile
from PIL import Image, ImageDraw
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
NEW_LAYOUTS={name:'LAYOUT_HGSS_UNION_CAVE_'+str(i)+'_F' for i,name in enumerate(FLOORS,1)}
# The appended metatile is blank in the private cave tileset. The collision
# bit keeps the repeated map border impassable, including at camera edges.
VOID_BORDER=0x0459
# The donor's common, collision-blocked cave rock top. Use it inside solid
# formations; actual exterior void remains black.
SOLID_ROCK=0x040f
# Delta screenshot of the east wall (1F around 28,57): three short edge
# notches interrupt a continuous solid shelf. Other exterior black remains.
OWNER_EDGE_NOTCHES={'UnionCave_1F':((31,56),(31,57),(31,59))}

def pack(v):return struct.pack('<%dH'%len(v),*v)
def read16(path):
    b=path.read_bytes();assert len(b)%2==0;return list(struct.unpack('<%dH'%(len(b)//2),b))
def js(path):return json.loads((R/path).read_text())

def register_layouts(layout_list, layouts, write):
    """Append new identities; leave legacy IDs and their layout files intact.

    Continue uses the saved layout identity to distinguish legacy coordinates
    from legitimate new isolated-pocket saves without another save field.
    """
    for name,lid in NEW_LAYOUTS.items():
        original=layouts['LAYOUT_UNION_CAVE_'+name[-2]+'_F']
        directory='data/layouts/Hgss'+name
        layout=dict(original,id=lid,name='Hgss'+name+'_Layout',
                    width=32,height=64 if name=='UnionCave_2F' else 96,
                    primary_tileset='gTileset_HgssUnionCave',secondary_tileset='gTileset_WesternInteriors',
                    border_filepath=directory+'/border.bin',blockdata_filepath=directory+'/map.bin')
        if lid not in layouts:layout_list.append(layout);layouts[lid]=layout
        else:assert layouts[lid]==layout,(lid,'Reconstructed layout changed unexpectedly')
        write(layout['border_filepath'],pack([VOID_BORDER]*4))

def preview_resources(maps,layouts,write):
    """Pack dormant layouts without installing any incomplete pocket map."""
    preview={n:copy.deepcopy(maps[n]) for n in FLOORS}
    preview.update({n:{'id':'MAP_PREVIEW_'+n.upper()} for n in ('RuinsOfAlph_SouthwestPocket','RuinsOfAlph_NorthwestPocket')})
    # Existing route target IDs are needed to preserve the original warp slots.
    for n in ('JohtoRoute32','JohtoRoute33'):preview[n]=maps[n]
    tiles={};sizes={};apply(preview,tiles,sizes,layouts,write)
    for name,values in tiles.items():
        write(layouts[NEW_LAYOUTS[name]]['blockdata_filepath'],pack(values))

def generate_assets(write):
    with tempfile.TemporaryDirectory(prefix='black-ledger-hgss-union-') as d:
        t=Path(d);subprocess.run([sys.executable,str(R/'crossroads/tools/prepare_hns_union_cave.py'),'--output',str(t)],check=True,stdout=subprocess.DEVNULL)
        # Private blank metatile for unreachable HGSS matrix space. Source
        # pixels/indices remain unchanged; blank art is appended to free slots.
        sheet=Image.open(t/'tiles.png');assert sheet.mode=='P' and sheet.width==128 and sheet.height>=88
        assert all(v==0 for v in sheet.crop((8,80,16,88)).get_flattened_data())
        sheet.paste(Image.new('P',(8,8),0),(8,80))
        # A small original sign uses the cave's existing neutral palette. It
        # keeps the three preserved notes events visible and interactable.
        sign=Image.new('P',(16,16),0);draw=ImageDraw.Draw(sign)
        draw.rectangle((2,2,13,10),fill=4,outline=5)
        draw.rectangle((3,3,12,8),fill=1)
        draw.line((4,5,11,5),fill=4);draw.line((4,7,9,7),fill=4)
        draw.rectangle((6,11,9,15),fill=4,outline=5)
        for j in range(4):
            tile=sign.crop(((j%2)*8,(j//2)*8,(j%2+1)*8,(j//2+1)*8))
            index=162+j;sheet.paste(tile,((index%16)*8,(index//16)*8))
        buffer=io.BytesIO();sheet.save(buffer,format='PNG',optimize=False)
        write(OUT+'/tiles.png',buffer.getvalue())
        original_meta=(t/'metatiles.bin').read_bytes();floor=read16(t/'metatiles.bin')[8:12]
        write(OUT+'/metatiles.bin',original_meta+pack([161]*8)+pack(floor+[(3<<12)|i for i in range(162,166)]))
        # COVERED places both blank layers over the black backdrop; NORMAL
        # exposes the engine's unrelated BG3 fill tile through transparency.
        write(OUT+'/metatile_attributes.bin',(t/'metatile_attributes.bin').read_bytes()+pack([0x1000,0x101d]))
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

def fill_enclosed_void(w,h,values):
    """Fill black holes enclosed by rock without changing exterior void.

    The reference permission grid has no artwork for solid cells. The old
    two-tile fringe put black holes inside thick cliff islands. Distinguish
    external black space by flooding only black cells from the matrix edges.
    Neither walkable/water cells nor the shape of the external void changes.
    """
    outside=set()
    q=deque()
    for y in range(h):
        for x in range(w):
            if (x in (0,w-1) or y in (0,h-1)) and values[y*w+x]==VOID_BORDER:
                outside.add((x,y));q.append((x,y))
    while q:
        x,y=q.popleft()
        for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0<=xx<w and 0<=yy<h and (xx,yy) not in outside and values[yy*w+xx]==VOID_BORDER:
                outside.add((xx,yy));q.append((xx,yy))
    # Only close islands whose entire perimeter is the authored rock-top
    # tile. An enclosed black area adjoining a different tile is ambiguous and
    # must be reviewed rather than silently reinterpreted as solid rock.
    remaining={(i%w,i//w) for i,v in enumerate(values)
               if v==VOID_BORDER and (i%w,i//w) not in outside}
    fill=set()
    while remaining:
        start=remaining.pop();component={start};q=deque([start]);perimeter=set()
        while q:
            x,y=q.popleft()
            for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if not (0<=xx<w and 0<=yy<h):continue
                if (xx,yy) in remaining:
                    remaining.remove((xx,yy));component.add((xx,yy));q.append((xx,yy))
                elif (xx,yy) not in component:
                    perimeter.add(values[yy*w+xx])
        if perimeter=={SOLID_ROCK}:fill.update(component)
    return [SOLID_ROCK if (i%w,i//w) in fill else v for i,v in enumerate(values)]

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
            if cls==0 and (x,y) not in wall_fringe:vals.append(VOID_BORDER);continue # appended black void metatile 89
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
    return w,h,classes,fill_enclosed_void(w,h,vals)

def validate_pocket_warps(maps):
    names=('RuinsOfAlph_SouthwestPocket','RuinsOfAlph_NorthwestPocket')
    assert all(n in maps for n in names),'Both distinct Ruins pockets are required'
    by_id={m['id']:m for m in maps.values()}
    cave_id=maps['UnionCave_1F']['id']
    targets=[]
    for pocket,cave_warp in zip(names,(6,7)):
        m=maps[pocket];events=m['warp_events']
        assert len(events)>=2 and events[0]['dest_map']==cave_id and int(events[0]['dest_warp_id'])==cave_warp,(pocket,'Missing reciprocal cave entrance or chamber')
        chambers={e['dest_map'] for e in events if e['dest_map']!=cave_id}
        assert chambers,'Pocket must have its own actual chamber'
        assert not chambers.intersection({maps[n]['id'] for n in names}),'Separate pockets cannot connect directly'
        targets.append(chambers)
        for i,e in enumerate(events):
            assert e['dest_map'] in by_id,(pocket,i,'Missing destination')
            target=by_id[e['dest_map']]['warp_events'];index=int(e['dest_warp_id'])
            assert 0<=index<len(target),(pocket,i,'Invalid target index')
            other=target[index]
            assert other['dest_map']==m['id'] and int(other['dest_warp_id'])==i,(pocket,i,'Nonreciprocal warp')
    assert not targets[0].intersection(targets[1]),'Distinct Ruins pockets cannot share a directly accessible chamber'

def apply(maps,tiles,sizes,layouts,write):
    attrs,catalog=generate_assets(write);facts=js('crossroads/hgss/canonical_events/union-cave-geometry.json');plan=js('crossroads/donor/hns-union-cave/hgss-corrected-warp-plan.json')
    for name,refname in FLOORS.items():
        assert name in maps and all(p in maps for p in ('RuinsOfAlph_SouthwestPocket','RuinsOfAlph_NorthwestPocket')),'Complete Ruins pocket destinations before integrating cave'
        m=maps[name];fact=facts[refname];w,h,classes,values=build_plane(fact,attrs,catalog)
        notches=set(OWNER_EDGE_NOTCHES.get(name,()))
        for x,y in notches:
            assert classes[y*w+x]==0 and values[y*w+x]==VOID_BORDER
            for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if 0<=xx<w and 0<=yy<h and (xx,yy) not in notches:
                    assert values[yy*w+xx]==SOLID_ROCK,(name,x,y,'notch perimeter changed',xx,yy)
        for x,y in notches:
            values[y*w+x]=SOLID_ROCK
        m['layout']=NEW_LAYOUTS[name]
        layout=layouts[m['layout']]
        assert (layout['width'],layout['height'])==(w,h)
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
                if group=='bg_events':values[y*w+x]=0x045a # visible preserved notes sign
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
