#!/usr/bin/env python3
"""Stage a Ruins connector candidate, without registering it in the game.

This is an integration draft. The public facade and save-safe placement remain
unresolved. No cave or public map is modified by this script. The hall-entrance
corridor is a provisional GBA adaptation, not a verified HGSS reconstruction.
"""
from collections import deque
from build_hgss_ruins_assets import prepare

NAMES = ('RuinsOfAlph_SouthwestPocket', 'RuinsOfAlph_NorthwestPocket',
         'RuinsOfAlph_SouthwestChamber', 'RuinsOfAlph_NorthwestChamber',
         'RuinsOfAlph_UndergroundHall', 'RuinsOfAlph_HallEntrance')
IDS = ('MAP_RUINS_OF_ALPH_SOUTHWEST_POCKET', 'MAP_RUINS_OF_ALPH_NORTHWEST_POCKET',
       'MAP_RUINS_OF_ALPH_SOUTHWEST_CHAMBER', 'MAP_RUINS_OF_ALPH_NORTHWEST_CHAMBER',
       'MAP_RUINS_OF_ALPH_UNDERGROUND_HALL', 'MAP_RUINS_OF_ALPH_HALL_ENTRANCE')
SIZES = ((22,14),(16,17),(10,11),(10,11),(29,32),(13,15))


def warp(x, y, dest, index):
    return dict(x=x,y=y,elevation=0,dest_map=dest,dest_warp_id=str(index))


def make_map(name, map_id, layout_id, outside=False):
    return dict(id=map_id,name=name,layout=layout_id,music='MUS_PETALBURG_WOODS',
                region='REGION_HOENN',region_map_section='MAPSEC_RUINS_OF_ALPH',
                requires_flash=False,weather='WEATHER_SUNNY' if outside else 'WEATHER_NONE',
                map_type='MAP_TYPE_ROUTE' if outside else 'MAP_TYPE_UNDERGROUND',
                allow_cycling=False,allow_escaping=False,allow_running=True,
                show_map_name=False,battle_scene='MAP_BATTLE_SCENE_NORMAL',
                connections=None,object_events=[],warp_events=[],coord_events=[],bg_events=[])


def flood(cells, width, height, point):
    queue=deque([point]);seen=set(queue)
    while queue:
        x,y=queue.popleft()
        for xy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            a,b=xy
            if 0<=a<width and 0<=b<height and xy not in seen and not cells[b*width+a]&0xc00:
                seen.add(xy);queue.append(xy)
    return seen


def stage(write):
    data=prepare(write)
    tiles=[data['SouthwestPocket'],data['NorthwestPocket'],data['SouthwestChamber'],
           data['NorthwestChamber'],data['UndergroundHall']]
    # The donor puts a one-way ledge between cave and chamber. Reopen two
    # adjacent grass cells on its east end, preserving bidirectional access.
    sw=tiles[0]
    assert sw[4*22+18]==0x042b and sw[5*22+18]==0x042c
    sw[4*22+18]=sw[5*22+18]=0x3036
    assert (7,6) in flood(sw,22,14,(14,2))
    assert (14,2) in flood(sw,22,14,(7,6))
    assert (5,4) in flood(tiles[1],16,17,(13,6))
    # A provisional hall entry uses donor hall wall/floor graphics. Exact HGSS
    # room art, ladder presentation, and the entrance width require visual QA.
    # Warp tiles use the hall's ladder metatile; its source collision is cleared.
    entrance=[0x040c]*(13*15)
    for y in range(2,14):
        for x in range(2,11):entrance[y*13+x]=0x3001
    entrance[7*13+6]=entrance[13*13+6]=0x3019
    tiles.append(entrance)
    hall=tiles[4];assert hall[16*29+15]==0x4019;hall[16*29+15]=0x3019
    assert (15,16) in flood(hall,29,32,(5,6))
    assert (15,16) in flood(hall,29,32,(5,23))
    maps=[make_map(n,i,'LAYOUT_'+i[4:],j<2) for j,(n,i) in enumerate(zip(NAMES,IDS))]
    maps[0]['warp_events']=[warp(14,2,'MAP_UNION_CAVE_1_F',6),warp(7,6,IDS[2],0)]
    maps[1]['warp_events']=[warp(13,6,'MAP_UNION_CAVE_1_F',7),warp(5,4,IDS[3],0)]
    maps[2]['warp_events']=[warp(4,9,IDS[0],1)]
    maps[3]['warp_events']=[warp(4,9,IDS[1],1)]
    scripts={n: n+'_MapScripts::\n    .byte 0\n' for n in NAMES}
    for index, puzzle, landing in ((2,1,(5,23)),(3,3,(5,6))):
        name=NAMES[index]; label=name+'_Puzzle'; success=label+'_Success'
        maps[index]['bg_events'].append(dict(type='sign',x=5,y=4,elevation=0,
            player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=label))
        scripts[name] += (f'{label}::\n    lockall\n    fadescreen FADE_TO_BLACK\n'
                          f'    setvar VAR_0x8004, {puzzle}\n    setvar VAR_0x8005, FALSE\n'
                          f'    special DoSlidingPuzzle\n    goto_if_eq VAR_RESULT, TRUE, {success}\n'
                          f'    releaseall\n    end\n{success}::\n'
                          f'    warp {IDS[4]}, {landing[0]}, {landing[1]}\n'
                          f'    waitstate\n    releaseall\n    end\n')
        assert (5,5) in flood(tiles[index],10,11,(4,9))
    maps[4]['warp_events']=[warp(15,16,IDS[5],1)]
    maps[5]['warp_events']=[warp(6,13,'MAP_RUINS_OF_ALPH',2),warp(6,7,IDS[4],0)]
    primaries=('gTileset_HgssRuinsPocket','gTileset_HgssRuinsPocket',
               'gTileset_HgssRuinsChamber','gTileset_HgssRuinsChamber',
               'gTileset_HgssRuinsHall','gTileset_HgssRuinsHall')
    layouts={}
    borders={}
    for name,m,(w,h),plane,primary in zip(NAMES,maps,SIZES,tiles,primaries):
        layouts[m['layout']]=dict(id=m['layout'],name=name+'_Layout',width=w,height=h,
            primary_tileset=primary,secondary_tileset='gTileset_WesternInteriors',
            border_filepath=f'data/layouts/{name}/border.bin',
            blockdata_filepath=f'data/layouts/{name}/map.bin',layout_version='emerald')
        borders[name]=[(plane[0]&1023)|0x400]*4
    return dict(zip(NAMES,maps)),dict(zip(NAMES,tiles)),layouts,borders,scripts
