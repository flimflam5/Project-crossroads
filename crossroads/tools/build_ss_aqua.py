#!/usr/bin/env python3
"""Source-shaped, docked S.S. Aqua exploration without imported HGSS plot.

Seven append-only maps preserve the actual HGSS coordinate origin and paired
cabin components. Source permissions are the starting geometry, not a substitute
for DS model collision: explicit native furniture bases supply documented solid
footprints. No sailing state, other-region destination, badge or quest is added.

The coordinated build runs this AFTER the existing Olivine landmark generator.
It does not edit the existing city, terminal or quay; those own the two gangway
warp aliases to SSAqua_1F indices0/12. --output-root is a safe review prototype.
"""
import argparse
import copy
import json
import re
import struct
from collections import deque
from pathlib import Path

from hgss_room_projection import project
from build_ss_aqua_assets import generate as generate_assets

R = Path(__file__).resolve().parents[2]
FACTS = 'crossroads/hgss/qa10/ss-aqua-geometry.json'
ART = 'crossroads/hgss/art/ss_aqua/manifest.json'
REVIEW = 'crossroads/hgss/qa10/ss-aqua-build-review.json'
OPENINGS = 'crossroads/hgss/qa10/ss-aqua-doorways.json'
SPECS = [
    ('SSAqua_1F', 'MAP_SS_AQUA_1F', 'MAP_SS_AQUA_1F'),
    ('SSAqua_CaptainRoom', 'MAP_SS_AQUA_CAPTAIN_ROOM', 'MAP_SS_AQUA_CAPTAIN_ROOM'),
    ('SSAqua_SoutheastCabins', 'MAP_SS_AQUA_SOUTHEAST_CABINS', 'MAP_SS_AQUA_1F_SOUTHEAST_ROOMS'),
    ('SSAqua_SouthwestCabins', 'MAP_SS_AQUA_SOUTHWEST_CABINS', 'MAP_SS_AQUA_1F_SOUTHWEST_ROOMS'),
    ('SSAqua_NortheastCabins', 'MAP_SS_AQUA_NORTHEAST_CABINS', 'MAP_SS_AQUA_1F_NORTHEAST_ROOMS'),
    ('SSAqua_NorthwestCabins', 'MAP_SS_AQUA_NORTHWEST_CABINS', 'MAP_SS_AQUA_1F_NORTHWEST_ROOMS'),
    ('SSAqua_B1F', 'MAP_SS_AQUA_B1F', 'MAP_SS_AQUA_B1F'),
]
NAMES = [s[0] for s in SPECS]
SOURCE_NAMES = {s[2]: s[0] for s in SPECS}
IDS = {s[0]: s[1] for s in SPECS}
OWNED = set(NAMES)


def load(path):
    return json.loads((R / path).read_text())


def components(cells):
    todo = set(cells)
    result = []
    while todo:
        first = min(todo)
        todo.remove(first)
        group = {first}
        q = deque([first])
        while q:
            x, y = q.popleft()
            for p in ((x-1, y), (x+1, y), (x, y-1), (x, y+1)):
                if p in todo:
                    todo.remove(p)
                    group.add(p)
                    q.append(p)
        result.append(group)
    return result


def generate(check=False, output_root=None):
    out = Path(output_root) if output_root else R

    def write(path, value):
        dest = out / path
        if isinstance(value, str):
            value = value.encode()
        if check:
            assert dest.exists() and dest.read_bytes() == value, ('Regenerate S.S. Aqua', path)
        elif not dest.exists() or dest.read_bytes() != value:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(value)

    def js(path, value):
        write(path, json.dumps(value, indent=2) + '\n')

    art = generate_assets(check=check, output_root=output_root, register=output_root is None)
    facts = load(FACTS)
    layouts = load('data/layouts/layouts.json')
    groups = load('data/maps/map_groups.json')
    manifest = load('crossroads/johto/manifest.json')
    bylayout = {l['id']: l for l in layouts['layouts']}
    old_groups = copy.deepcopy(groups)
    maps = {}
    rooms = {}
    review = []
    source_index = {}

    def spec(name, theme=None):
        variant = art.get('background_variants', {}).get(name, {}).get(theme)
        return variant or art['specs'][name]

    def tile(name, theme=None, x=0, y=0):
        a = spec(name, theme)
        return a['start'] + y % a['height'] * a['width'] + x % a['width']

    def theme_at(name, x, y):
        if name == 'SSAqua_1F':
            return 'officer' if x >= 40 else 'orange'
        if name == 'SSAqua_CaptainRoom':
            return 'green'
        if name == 'SSAqua_B1F':
            if 8 <= x <= 20 and 3 <= y <= 15:
                return 'crew'
            if x >= 28:
                return 'metal'
            if x <= 3 and 8 <= y <= 13:
                return 'blue'
            return 'wood'
        return ('red' if 'Northeast' in name or 'Southeast' in name else 'blue') if x < 14 else ('mustard' if 'Northeast' in name or 'Southeast' in name else 'gold')

    for name, ident, header in SPECS:
        # project() supplies only source floor geometry here. Its temple-specific
        # model artwork is deliberately ignored (model65 is a ship bookcase).
        geom = project(header, facts=facts)
        w, h = geom['width'], geom['height']
        public = set(geom['walkable'])
        raw = [0x400 | tile('void')] * (w*h)
        roles = {}
        fixtures = []
        alias_records = []
        for y in range(h):
            for x in range(w):
                if (x, y) in public:
                    raw[y*w+x] = 0x3000 | tile('floor_' + theme_at(name, x, y), x=x, y=y)
                elif any(p in public for p in ((x-1,y),(x+1,y),(x,y-1),(x,y+1))):
                    wall = 'wall_metal' if name == 'SSAqua_B1F' else 'wall_ship' if name == 'SSAqua_1F' else 'wall_cabin'
                    raw[y*w+x] = 0x400 | tile(wall, x=x, y=y)
                    roles[(x,y)] = 'source room hull/bulkhead boundary'

        # A complete two-row rear wall must support the windows/portholes.
        # Merely outlining collision neighbours leaves their upper halves
        # floating as disconnected strips in black space. These drawings do
        # not change a single source movement bit or open any new floor.
        wall_spans=[]
        if 'Cabins' in name:wall_spans=[(1,12,1,2),(15,26,1,2)]
        elif name=='SSAqua_CaptainRoom':wall_spans=[(1,12,1,2)]
        elif name=='SSAqua_1F':wall_spans=[(3,8,1,2),(24,26,1,2),(41,55,1,2),(9,20,7,8),(27,38,7,8)]
        elif name=='SSAqua_B1F':wall_spans=[(8,20,1,2),(28,36,1,2),(40,55,1,1)]
        for left,right,top,bottom in wall_spans:
            for y in range(top,bottom+1):
                for x in range(left,right+1):
                    if (x,y) not in public:
                        wall='wall_metal'if name=='SSAqua_B1F'else'wall_ship'if name=='SSAqua_1F'else'wall_cabin'
                        raw[y*w+x]=0x400|tile(wall,x=x,y=y)
                        roles[(x,y)]='Continuous source rear wall / bulkhead background'

        m = dict(id=ident, name=name, layout='LAYOUT_' + ident[4:],
                 region='REGION_HOENN', region_map_section='MAPSEC_OLIVINE_CITY',
                 music='MUS_SAILING', requires_flash=False, weather='WEATHER_NONE',
                 map_type='MAP_TYPE_INDOOR', allow_cycling=False,
                 allow_escaping=False, allow_running=True, show_map_name=False,
                 battle_scene='MAP_BATTLE_SCENE_NORMAL', connections=None,
                 object_events=[], warp_events=[], coord_events=[], bg_events=[])
        for i, e in enumerate(facts[header]['warps']):
            if name == 'SSAqua_1F' and i == 12:
                # Same physical hatch as0, conditionally Vermilion in HGSS.
                # No unimplemented Kanto destination is registered in this pass.
                continue
            dest = IDS[SOURCE_NAMES[e['header']]] if e['header'] in SOURCE_NAMES else 'MAP_OLIVINE_CITY_PORT_QUAY'
            target = e['anchor'] if e['header'] in SOURCE_NAMES else 4
            m['warp_events'].append(dict(x=e['x'], y=e['z'], elevation=0,
                                        dest_map=dest, dest_warp_id=str(target)))
        source_index[name] = {i:i for i in range(len(m['warp_events']))}
        rooms[name] = dict(width=w, height=h, tiles=raw, source_public=public,
                           source=geom, roles=roles, fixtures=fixtures,
                           aliases=alias_records, theme_at=theme_at)
        maps[name] = m

    def fixture(name, kind, x, y, *, theme=None, solid=True, overhang=0, label=None, size=None):
        r = rooms[name]
        w, h, raw = r['width'], r['height'], r['tiles']
        theme = theme or theme_at(name, x, y)
        a = spec(kind, theme)
        ww, hh = size or (a['width'], a['height'])
        body = []
        def art_axis(pos, native, drawn):
            # Stretch only the middle panels of a larger projection. Modulo
            # wrapping would repeat outer table rims and draw several tables.
            if native==drawn or native==1:return pos % native
            if pos==0:return 0
            if pos==drawn-1:return native-1
            return max(1,min(native-2,pos)) if native>2 else 0
        for yy in range(hh):
            for xx in range(ww):
                X, Y = x+xx, y+yy
                assert 0 <= X < w and 0 <= Y < h, (name, kind, x, y, ww, hh)
                idx = Y*w+X
                old = raw[idx]
                n = tile(kind, theme, art_axis(xx,a['width'],ww), art_axis(yy,a['height'],hh))
                blocked = bool(old & 0xc00) or bool(solid and yy >= overhang)
                raw[idx] = (0x3400 if blocked else 0x3000) | n
                r['roles'][(X,Y)] = label or kind
                if solid and yy >= overhang:
                    body.append([X,Y])
        rec = dict(kind=kind, theme=theme, anchor=[x,y], size=[ww,hh],
                   solid_body_cells=body, overhang_rows=overhang,
                   reference=label or 'Actual complete HGSS room mosaic')
        r['fixtures'].append(rec)
        return rec

    def pattern_floor(name, kind, x, y, ww, hh):
        r = rooms[name]
        for yy in range(y,y+hh):
            for xx in range(x,x+ww):
                idx=yy*r['width']+xx
                r['tiles'][idx] = (r['tiles'][idx]&0xfc00) | tile(kind, x=xx-x, y=yy-y)

    def threshold(name, x, y, theme):
        """South-room exits have a low sill, not a tall door painted on floor."""
        r=rooms[name];a=spec('door_ship',theme)
        for xx in range(2):
            i=y*r['width']+x+xx
            r['tiles'][i]=(r['tiles'][i]&0xfc00)|a['start']+2+xx
            r['roles'][(x+xx,y)]='Visible two-leaf low hatch threshold'
        r['fixtures'].append(dict(kind='door_ship',theme=theme,anchor=[x,y],size=[2,1],source_art_rows=[1],solid_body_cells=[],overhang_rows=0,reference='South-facing interior sill projection; avoids painting a tall opaque door on public floor'))

    # Main deck: four vertical benches, north/south settees and life-ring/
    # porthole walls are visible in the complete HGSS first-floor mosaic.
    n='SSAqua_1F'
    for x,y in [(3,7),(5,7),(3,12),(5,12)]:
        fixture(n,'bench_vertical',x,y,overhang=1)
    for x,y in [(4,3),(4,18)]:fixture(n,'bench_blue',x,y,overhang=1)
    for x,y in [(1,4),(1,16)]:fixture(n,'plant',x,y,overhang=1)
    for x in [3,5,7]:fixture(n,'porthole',x,1,solid=False)
    for x in [24,26]:fixture(n,'porthole',x,1,solid=False)
    for x,y in [(3,2),(7,2)]:fixture(n,'life_ring',x,y,solid=False)
    fixture(n,'control_cabinet',42,1,theme='metal',overhang=1)
    fixture(n,'control_cabinet',48,1,theme='metal',overhang=1)
    fixture(n,'ladder',41,9,theme='metal',solid=False)

    # Two blue/red-bed cabin pairs and two mustard/gold dining pairs. Embedded
    # furniture is taken from the complete mosaic even when source props=[] .
    for n in ['SSAqua_SouthwestCabins','SSAqua_NorthwestCabins']:
        fixture(n,'bed_blue',1,3)
    n='SSAqua_SouthwestCabins'
    fixture(n,'painting',3,1,solid=False)
    fixture(n,'table',8,8)
    for x,y in [(7,9),(10,8)]:fixture(n,'chair_red',x,y)
    fixture(n,'cabinet',15,1,theme='gold',overhang=1)
    fixture(n,'bin',16,3,theme='gold')
    fixture(n,'painting',19,1,theme='gold',solid=False)
    fixture(n,'bin',15,11,theme='gold')
    fixture(n,'table_square',22,6,theme='mustard')
    for x,y in [(21,6),(25,6),(21,9),(25,9)]:fixture(n,'chair_green',x,y,theme='gold')
    n='SSAqua_NorthwestCabins'
    fixture(n,'table_wide',6,6,theme='blue')
    for x,y in [(5,7),(10,6)]:fixture(n,'chair_red',x,y)
    for x in [3,7,11,17,21,25]:fixture(n,'porthole',x,1,solid=False)
    for x in [19,23]:fixture(n,'bed_blue',x,4,theme='gold')
    fixture(n,'sofa_vertical',15,7,theme='gold')
    n='SSAqua_NortheastCabins'
    for x in [1,10]:fixture(n,'desk_white',x,3,theme='red')
    for y in [6,9]:fixture(n,'bed_blue',1,y,theme='red')
    fixture(n,'painting',5,1,theme='red',solid=False)
    for x in [3,9,16,21,25]:fixture(n,'porthole',x,1,solid=False)
    fixture(n,'bed_blue',15,9,theme='mustard')
    fixture(n,'table_square',20,6,theme='mustard',size=(4,3))
    for x,y in [(19,6),(24,6),(19,9),(24,9)]:fixture(n,'chair_yellow',x,y,theme='mustard')
    n='SSAqua_SoutheastCabins'
    fixture(n,'tv_counter',1,3,theme='red',size=(6,2))
    for x in [6,10]:fixture(n,'bed_blue',x,9,theme='red')
    fixture(n,'bin',1,11,theme='red')
    fixture(n,'painting',5,1,theme='red',solid=False)
    fixture(n,'bed_blue',15,3,theme='mustard')
    fixture(n,'ladder',15,1,theme='mustard',solid=False)
    fixture(n,'galley_sink',25,2,theme='mustard',solid=True)
    fixture(n,'painting',18,1,theme='mustard',solid=False)
    fixture(n,'bin',15,11,theme='mustard')
    fixture(n,'table_square',21,7,theme='mustard')
    for x,y in [(20,7),(24,7),(20,10),(24,10)]:fixture(n,'chair_yellow',x,y,theme='mustard')

    n='SSAqua_CaptainRoom'
    # The original central rug is a chosen original nine-slice projection.
    if 'rug_green' in art['specs']:
        for yy in range(4,10):
            for xx in range(5,12):
                ax=0 if xx==5 else 2 if xx==11 else 1
                ay=0 if yy==4 else 2 if yy==9 else 1
                i=yy*rooms[n]['width']+xx
                rooms[n]['tiles'][i]=(rooms[n]['tiles'][i]&0xfc00)|tile('rug_green',x=ax,y=ay)
    fixture(n,'captain_desk',8,5,theme='green')
    fixture(n,'bed_brown',1,3,theme='green')
    fixture(n,'cabinet',1,1,theme='green',overhang=1)
    fixture(n,'galley_counter',5,1,theme='green',solid=False)
    fixture(n,'fridge',7,1,theme='green',solid=False)
    fixture(n,'map_board',5,1,theme='green',solid=False)
    for x in [3,10,12]:fixture(n,'window',x,1,solid=False)
    fixture(n,'bin',8,4,theme='green')
    fixture(n,'sofa_orange',1,9,theme='green',size=(2,3))

    n='SSAqua_B1F'
    for x in [9,13,17]:
        for y in [4,8]:fixture(n,'bed_blue',x,y,theme='crew')
    for x in [9,14,19]:fixture(n,'locker_crew',x,2,theme='crew',overhang=1)
    for x in [9,19]:fixture(n,'ladder',x,1,theme='metal',solid=False)
    fixture(n,'bin',8,3,theme='crew')
    fixture(n,'clock',17,1,theme='crew',solid=False)
    fixture(n,'clock',33,1,theme='metal',solid=False)
    fixture(n,'fridge',28,2,theme='metal',solid=False)
    fixture(n,'galley_stove',32,2,theme='metal',solid=False)
    fixture(n,'galley_sink',34,2,theme='metal',solid=False)
    fixture(n,'galley_counter',36,2,theme='metal',solid=False)
    fixture(n,'galley_table',32,6,theme='metal',size=(3,5))
    for x in [31,35]:
        for y in [6,8,10]:fixture(n,'chair_orange',x,y,theme='metal')
    for y in range(5,16):
        for x in range(43,54):
            if x in [43,53] or y in [5,15]:
                if (x,y) in rooms[n]['source_public']:
                    pattern_floor(n,'hazardfloor',x,y,1,1)
    # The source engine collision volume is larger than its visible upper
    # machinery. Plate/grille infill makes the full solid body visible.
    fixture(n,'machine_panel',44,6,theme='metal',size=(9,9))
    fixture(n,'engine',44,7,theme='metal')
    fixture(n,'ladder',42,6,theme='metal',solid=False)
    fixture(n,'control_cabinet',54,1,theme='metal',overhang=1)
    fixture(n,'engine_pipe',54,12,theme='metal',solid=True)

    # Source hatch graphics are decorative; the actual public threshold is the
    # warp coordinate. One native leaf is drawn for each source single-cell door.
    # All five gangway floor cells and both source right-stair rows remain live.
    aliases = [
        ('SSAqua_1F',25,19,'MAP_OLIVINE_CITY_PORT_QUAY',5,0),
        ('SSAqua_1F',22,19,'MAP_OLIVINE_CITY_PORT_QUAY',4,0),
        ('SSAqua_1F',23,19,'MAP_OLIVINE_CITY_PORT_QUAY',4,0),
        ('SSAqua_1F',26,19,'MAP_OLIVINE_CITY_PORT_QUAY',5,0),
        ('SSAqua_1F',42,8,IDS['SSAqua_B1F'],2,10),
    ]
    for n,x,y,dest,target,parent in aliases:
        i=len(maps[n]['warp_events'])
        maps[n]['warp_events'].append(dict(x=x,y=y,elevation=0,dest_map=dest,dest_warp_id=str(target)))
        rooms[n]['aliases'].append(dict(native_index=i,source_parent=parent,x=x,y=y,reason='Every visible public gangway leaf / source right stair row operates'))

    # The original GBA hatches are two visible leaves. Every second leaf gets
    # its own reciprocal warp, including source single-cell entrances. This is
    # an explicit flat-projection adaptation, not an excuse to block half a door.
    cabin_pairs=[(1,'SSAqua_SouthwestCabins',0),(2,'SSAqua_SouthwestCabins',1),
                 (3,'SSAqua_SoutheastCabins',0),(4,'SSAqua_SoutheastCabins',1),
                 (5,'SSAqua_NorthwestCabins',0),(6,'SSAqua_NorthwestCabins',1),
                 (7,'SSAqua_NortheastCabins',0),(8,'SSAqua_NortheastCabins',1),
                 (11,'SSAqua_CaptainRoom',0)]
    def alias(n,x,y,dest,target,parent):
        i=len(maps[n]['warp_events'])
        maps[n]['warp_events'].append(dict(x=x,y=y,elevation=0,dest_map=dest,dest_warp_id=str(target)))
        rooms[n]['aliases'].append(dict(native_index=i,source_parent=parent,x=x,y=y,reason='Second visible native hatch/stair leaf; reciprocal destination preserved'))
        return i
    for deck_index,cabin,cabin_index in cabin_pairs:
        a=maps['SSAqua_1F']['warp_events'][deck_index]
        b=maps[cabin]['warp_events'][cabin_index]
        di=len(maps['SSAqua_1F']['warp_events']);ci=len(maps[cabin]['warp_events'])
        alias('SSAqua_1F',a['x']+1,a['y'],IDS[cabin],ci,deck_index)
        alias(cabin,b['x']+1,b['y'],IDS['SSAqua_1F'],di,cabin_index)
    for x,y,source_a,source_b in [(43,9,10,1),(43,8,10,2),(25,3,9,0)]:
        a=len(maps['SSAqua_1F']['warp_events']);b=len(maps['SSAqua_B1F']['warp_events'])
        alias('SSAqua_1F',x,y,IDS['SSAqua_B1F'],b,source_a)
        alias('SSAqua_B1F',x,y,IDS['SSAqua_1F'],a,source_b)
    # The wider west stair needs a visible landing immediately south in B1F;
    # it is a single explicitly recorded native clearance, never a hidden warp.
    for n in ['SSAqua_1F','SSAqua_B1F']:
        r=rooms[n];i=4*r['width']+25
        r['tiles'][i]=0x3000|tile('floor_'+theme_at(n,25,4),x=25,y=4)
        r['roles'][(25,4)]='Visible clearance for second west-stair leaf'

    south_mouth = {('SSAqua_1F',i) for i in [5,6,7,8,9,11]}
    south_mouth |= {('SSAqua_B1F',0)}
    south_mouth |= {(n,i) for n in ['SSAqua_SouthwestCabins','SSAqua_SoutheastCabins'] for i in range(4)}
    for n in ['SSAqua_1F','SSAqua_B1F']:
        for a in rooms[n]['aliases']:
            if (n,a['source_parent']) in south_mouth:south_mouth.add((n,a['native_index']))
    for n,m in maps.items():
        r=rooms[n];w=r['width']
        for i,e in enumerate(m['warp_events']):
            x,y=e['x'],e['y'];theme=theme_at(n,x,y)
            original = i < len(facts[next(s[2]for s in SPECS if s[0]==n)]['warps']) and not any(a['native_index']==i for a in r['aliases'])
            if original and n=='SSAqua_1F' and i in range(1,5):
                threshold(n,x,y,theme)
            elif original and n=='SSAqua_1F' and i in range(5,9):
                fixture(n,'door_ship',x,y-1,theme=theme,solid=False)
            elif original and n=='SSAqua_1F' and i==11:
                fixture(n,'door_ship',x,y-1,theme='officer',solid=False)
            elif original and (n in ['SSAqua_NorthwestCabins','SSAqua_NortheastCabins','SSAqua_CaptainRoom']):
                threshold(n,x,y,theme)
            elif original and 'Cabins' in n:
                fixture(n,'door_ship',x,y-1,theme=theme,solid=False)
            elif original and (n,i) in [('SSAqua_1F',9),('SSAqua_B1F',0)]:
                fixture(n,'stairs_down' if n=='SSAqua_1F' else 'stairs_up',x,y-1,theme='wood' if n=='SSAqua_B1F' else 'metal',solid=False)
            elif original and (x,y)==(42,9):
                fixture(n,'stairs_up' if n=='SSAqua_B1F' else 'stairs_down',42,8,theme='metal',solid=False)
            base=r['tiles'][y*w+x]&1023
            variants=art.get('south_facing_warp_variants',{}) if (n,i)in south_mouth else art['warp_variants']
            # All source warp cells are forcibly reopened only if a decorative
            # fixture's overhang touched them; thresholds are not solid furniture.
            assert str(base) in variants,(n,i,'Missing exact pixel-identical warp variant',base)
            r['tiles'][y*w+x]=0x3000|variants[str(base)]
            r['roles'][(x,y)]='operable source doorway/stair/gangway'

    def actor(n,x,y,label,gfx='SAILOR'):
        r=rooms[n];w,h=r['width'],r['height']
        if not(0<=x<w and 0<=y<h)or r['tiles'][y*w+x]&0xc00:
            candidates=[(a,b)for a,b in r['source_public']if not r['tiles'][b*w+a]&0xc00 and (a,b)not in {(e['x'],e['y'])for e in maps[n]['warp_events']}]
            x,y=min(candidates,key=lambda p:abs(p[0]-x)+abs(p[1]-y))
        maps[n]['object_events'].append(dict(graphics_id='OBJ_EVENT_GFX_'+gfx,x=x,y=y,elevation=3,movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script=label,flag='0'))

    actor('SSAqua_1F',25,17,'SSAqua_GangwayCrew')
    actor('SSAqua_1F',7,11,'SSAqua_LoungeCrew')
    actor('SSAqua_1F',52,17,'SSAqua_OfficerCrew')
    actor('SSAqua_CaptainRoom',9,4,'SSAqua_Captain')
    actor('SSAqua_SouthwestCabins',5,7,'SSAqua_CabinVisitor','MAN_1')
    actor('SSAqua_SouthwestCabins',25,5,'SSAqua_DiningVisitor','WOMAN_3')
    actor('SSAqua_SoutheastCabins',9,7,'SSAqua_RestingCrew')
    actor('SSAqua_NortheastCabins',9,7,'SSAqua_CabinVisitor','WOMAN_3')
    actor('SSAqua_NortheastCabins',25,5,'SSAqua_DiningVisitor','MAN_1')
    actor('SSAqua_NorthwestCabins',10,4,'SSAqua_CabinVisitor','EXPERT_M')
    actor('SSAqua_NorthwestCabins',25,8,'SSAqua_TwinBerthVisitor','WOMAN_3')
    actor('SSAqua_B1F',26,13,'SSAqua_MaintenanceCrew')
    actor('SSAqua_B1F',37,16,'SSAqua_EngineCrew')
    # Source player-cabin berth interaction is available at dock without calling
    # native Tidal cruise progression. It grants no item or persistent story flag.
    maps['SSAqua_SoutheastCabins']['bg_events']=[dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='SSAqua_Berth') for x,y in [(16,4),(16,5)]]
    maps['SSAqua_CaptainRoom']['bg_events']=[dict(type='sign',x=9,y=6,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='SSAqua_Chart')]

    for n,ident,header in SPECS:
        m=maps[n];r=rooms[n];w,h=r['width'],r['height'];raw=r['tiles'];S=r['source_public']
        # Every collision-free tile must belong to a real public component and
        # escape via one of its actual doors; actors may never own a warp mouth.
        walk={(x,y)for y in range(h)for x in range(w)if not raw[y*w+x]&0xc00}
        warps={(e['x'],e['y'])for e in m['warp_events']}
        for comp in components(walk):
            assert comp&warps,(n,'Public floor without a real exit',min(comp),len(comp))
        for o in m['object_events']:
            assert (o['x'],o['y'])not in warps,(n,'Actor blocks a doorway')
            assert not raw[o['y']*w+o['x']]&0xc00,(n,'Actor inside furniture')
        changes=[]
        for y in range(h):
            for x in range(w):
                before=(x,y)not in S;after=bool(raw[y*w+x]&0xc00)
                if before!=after:
                    changes.append(dict(x=x,y=y,before_blocked=before,after_blocked=after,reason=r['roles'].get((x,y),'UNEXPLAINED')))
        assert all(c['reason']!='UNEXPLAINED'for c in changes),(n,'Unexplained physics delta')
        lid=m['layout'];l=dict(id=lid,name=n+'_Layout',width=w,height=h,primary_tileset='gTileset_HgssSSAquaPrimary',secondary_tileset='gTileset_HgssSSAqua',border_filepath=f'data/layouts/{n}/border.bin',blockdata_filepath=f'data/layouts/{n}/map.bin',layout_version='emerald')
        if lid not in bylayout:layouts['layouts'].append(l);bylayout[lid]=l
        else:assert bylayout[lid]==l,('Existing Aqua layout changed',n)
        group=groups['gMapGroup_CrossroadsJohtoExpansion']
        if n not in group:group.append(n)
        assert group.index(n)<127
        if not any(p['name']==n for p in manifest['planned']):manifest['planned'].append(dict(name=n,kind='hgss',parent='OlivineCity',cluster='west',status='implemented-runtime-review-pending'))
        write(l['blockdata_filepath'],struct.pack('<'+str(w*h)+'H',*raw))
        write(l['border_filepath'],struct.pack('<4H',*([0x400|tile('void')]*4)))
        js(f'data/maps/{n}/map.json',m)
        write(f'data/maps/{n}/scripts.inc',f'{n}_MapScripts::\n    .byte 0\n')
        props=[]
        for k,c in enumerate(facts[header]['chunks']):
            for j,p in enumerate(c['props']):
                x=int(p['tile_x'])+k%facts[header]['matrix_dimensions'][0]*32;y=int(p['tile_z'])+k//facts[header]['matrix_dimensions'][0]*32
                candidates_by_model={16:['clock'],17:['bed_blue'],20:['galley_sink','galley_stove','galley_counter'],21:['fridge'],22:['bin'],23:['plant'],53:['chair_orange'],60:['painting'],65:['cabinet'],67:['ladder'],70:['locker_crew'],71:['cabinet'],138:['galley_sink'],139:['painting'],162:['door_ship'],164:['engine']}
                choices=[z for z in r['fixtures']if z['kind']in candidates_by_model[p['model']]]
                assert choices,(n,'Actual source prop lacks rendered native fixture',p)
                rendered=min(choices,key=lambda z:(z['anchor'][0]+z['size'][0]/2-x)**2+(z['anchor'][1]+z['size'][1]/2-y)**2)
                props.append(dict(chunk=k,instance=j,model=p['model'],source_anchor=[p['tile_x'],p['tile_z']],source_world_anchor=[x,y],native_anchor=rendered['anchor'],render_kind=rendered['kind'],native_size=rendered['size'],projection='Original GBA flat art follows complete-room raster; DS model origin/height is not its flat visual top-left',semantic_limit='Model138 exact fixture purpose unverified; no new labelled function'if p['model']==138 else 'Multiple wardrobe/ladders may share a compound native locker visual'if p['model']in[67,70]else None))
        review.append(dict(name=n,id=ident,source_header=header,source=facts[header]['source'],crop_origin=[0,0],dimensions=[w,h],source_public_cells=len(S),native_public_cells=len(walk),native_components=[dict(cells=len(c),doors=sorted([list(p)for p in c&warps]))for c in components(walk)],map_group=groups['group_order'].index('gMapGroup_CrossroadsJohtoExpansion'),map_num=group.index(n),source_warps=facts[header]['warps'],native_warps=m['warp_events'],aliases=r['aliases'],collision_adaptations=changes,fixtures=r['fixtures'],props=props,actors=m['object_events'],services=m['bg_events'],runtime='PENDING exact delivery-ROM gameplay',owner_visual_acceptance='PENDING'))
    # Old native group prefixes stay exactly intact, including unrelated maps.
    for key in old_groups['group_order']:
        assert groups[key][:len(old_groups[key])]==old_groups[key],('Renumbered existing map',key)
    js('data/layouts/layouts.json',layouts);js('data/maps/map_groups.json',groups);js('crossroads/johto/manifest.json',manifest)
    js(REVIEW,dict(scope='Seven physical docked HGSS S.S. Aqua maps; no voyages/plot imported',maps=review,source_warp12='HGSS conditional Vermilion duplicate of0 is intentionally inactive; native12 is an appended right gangway leaf, not travel',gangway=dict(quay_map='OlivineCity_PortQuay',quay_warps=[4,5],ship_map='SSAqua_1F',ship_warps=[0,12,13,14,15],physical_projection='Source five-tile inside corridor projects to two visible outside hatch leaves; deliberate GBA art decision, not hardware necessity')))
    # Independent normal-play test contract: destinations are source-derived,
    # widths describe the drawn opening rather than merely listing map events.
    def side(name,indices,anchor,press,facing):
        es=[maps[name]['warp_events'][i]for i in indices]
        return dict(map=name,segments=[[e['x'],e['y']]for e in es],anchor=anchor,press=press,expected_facing=facing)
    opening_groups=[dict(city='olivine',label='aqua-gangway',
        outside=dict(map='OlivineCity_PortQuay',segments=[[27,20],[28,20]],anchor=[27,23],press=[0,-1],expected_facing=1,arrivals=[[27,20],[28,20],[27,20],[27,20],[28,20]]),
        inside=dict(map='SSAqua_1F',segments=[[24,19],[25,19],[22,19],[23,19],[26,19]],anchor=[24,18],press=[0,1],expected_facing=2,arrivals=[[24,19],[25,19]]))]
    for deck_index,cabin,cabin_index in cabin_pairs:
        de=maps['SSAqua_1F']['warp_events'][deck_index];ce=maps[cabin]['warp_events'][cabin_index]
        da=next(i for i,e in enumerate(maps['SSAqua_1F']['warp_events'])if(e['x'],e['y'])==(de['x']+1,de['y']))
        ca=next(i for i,e in enumerate(maps[cabin]['warp_events'])if(e['x'],e['y'])==(ce['x']+1,ce['y']))
        lower=deck_index in range(1,5)
        opening_groups.append(dict(city='olivine',label='aqua-'+cabin.removeprefix('SSAqua_').lower()+'-'+str(cabin_index),
            outside=side('SSAqua_1F',[deck_index,da],[de['x'],de['y']-2 if lower else de['y']+2],[0,1]if lower else[0,-1],2 if lower else 1),
            inside=side(cabin,[cabin_index,ca],[ce['x'],ce['y']+3 if lower else ce['y']-2],[0,-1]if lower else[0,1],1 if lower else 2)))
    opening_groups.append(dict(city='olivine',label='aqua-west-stairs',outside=side('SSAqua_1F',[9,28],[24,5],[0,-1],1),inside=side('SSAqua_B1F',[0,5],[24,5],[0,-1],1)))
    north_out=side('SSAqua_1F',[16,27],[42,6],[0,1],1)
    north_in=side('SSAqua_B1F',[2,4],[42,6],[0,1],1)
    # Actual HGSS B1F source ordinal2 returns to canonical1F ordinal10 (42,9),
    # while the added right leaf returns to its own reciprocal top-right alias.
    # Arrival lists are indexed by the OPPOSITE side's two attempted leaves.
    north_out['arrivals']=[[42,9],[43,8]]
    north_in['arrivals']=[[42,8],[43,8]]
    opening_groups.append(dict(city='olivine',label='aqua-right-stairs-north-rim',outside=north_out,inside=north_in))
    opening_groups.append(dict(city='olivine',label='aqua-right-stairs-south-rim',outside=side('SSAqua_1F',[10,26],[42,11],[0,-1],2),inside=side('SSAqua_B1F',[1,3],[42,11],[0,-1],2)))
    assert sum(len(g[s]['segments'])for g in opening_groups for s in ['outside','inside'])==55
    js(OPENINGS,dict(baseline_revision='285cfa4ebddcb390a8a5bde6116748cbb5eaba6b',notes='Every visible two-leaf hatch and all five interior gangway leaves; asymmetric arrival lists are indexed by OPPOSITE incoming side. Right stair has two exposed approach rims, both source rows and both drawn columns.',groups=opening_groups))
    inc=(R/'data/event_scripts.s').read_text();paths=[f'data/maps/{n}/scripts.inc'for n in NAMES]+['crossroads/scripts/ss_aqua.inc']
    for p in paths:
        if not re.search(r'\.include\s+"'+re.escape(p)+r'"',inc):inc+='\t.include "'+p+'"\n'
    write('data/event_scripts.s',inc)
    write('crossroads/scripts/ss_aqua.inc',SCRIPTS)
    print('S.S. Aqua seven source-shaped docked maps generated; voyages remain unimplemented and owner visual/runtime review required')
    return dict(maps=maps,rooms=rooms,review=review,art=art)


SCRIPTS='''@ Docked exploration only; no canonical plot, quest, trainer, reward or sailing flags.
SSAqua_GangwayCrew::
    msgbox SSAqua_GangwayCrewText, MSGBOX_NPC
    end
SSAqua_GangwayCrewText:
    .string "The gangway leads back to OLIVINE.\\nMind your footing on the quay.$"
SSAqua_LoungeCrew::
    msgbox SSAqua_LoungeCrewText, MSGBOX_NPC
    end
SSAqua_LoungeCrewText:
    .string "These seats are a good place to\\nwatch the harbor between shifts.$"
SSAqua_OfficerCrew::
    msgbox SSAqua_OfficerCrewText, MSGBOX_NPC
    end
SSAqua_OfficerCrewText:
    .string "The lower deck links both sides\\nof the ship. Keep the stairs clear.$"
SSAqua_Captain::
    msgbox SSAqua_CaptainText, MSGBOX_NPC
    end
SSAqua_CaptainText:
    .string "We're alongside the OLIVINE quay.\\nThe gangway is your way ashore.$"
SSAqua_CabinVisitor::
    msgbox SSAqua_CabinVisitorText, MSGBOX_NPC
    end
SSAqua_CabinVisitorText:
    .string "A quiet berth, a window, and a\\nchance to sit down. That's enough.$"
SSAqua_DiningVisitor::
    msgbox SSAqua_DiningVisitorText, MSGBOX_NPC
    end
SSAqua_DiningVisitorText:
    .string "The table is bolted to the deck.\\nA sensible precaution, I think.$"
SSAqua_RestingCrew::
    msgbox SSAqua_RestingCrewText, MSGBOX_NPC
    end
SSAqua_RestingCrewText:
    .string "Off-duty crew use these berths.\\nPlease keep your voice down.$"
SSAqua_TwinBerthVisitor::
    msgbox SSAqua_TwinBerthVisitorText, MSGBOX_NPC
    end
SSAqua_TwinBerthVisitorText:
    .string "Two bunks and a sofa. There's\\nmore room here than I expected.$"
SSAqua_MaintenanceCrew::
    msgbox SSAqua_MaintenanceCrewText, MSGBOX_NPC
    end
SSAqua_MaintenanceCrewText:
    .string "The crew quarters and galley are\\nhere. The engine bay is farther on.$"
SSAqua_EngineCrew::
    msgbox SSAqua_EngineCrewText, MSGBOX_NPC
    end
SSAqua_EngineCrewText:
    .string "Stay outside the machinery's\\nmarked safety boundary, please.$"
SSAqua_Chart::
    msgbox SSAqua_ChartText, MSGBOX_SIGN
    end
SSAqua_ChartText:
    .string "A harbor chart and a neatly\\nsecured set of navigation tools.$"
SSAqua_Berth::
    lockall
    msgbox SSAqua_BerthText, MSGBOX_YESNO
    goto_if_eq VAR_RESULT, NO, SSAqua_BerthDecline
    closemessage
    call Common_EventScript_OutOfCenterPartyHeal
SSAqua_BerthDecline:
    releaseall
    end
SSAqua_BerthText:
    .string "A clean berth. Let your POKEMON\\nrest for a little while?$"
'''

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');p.add_argument('--output-root',type=Path)
    a=p.parse_args();generate(a.check,a.output_root)
