#!/usr/bin/env python3
"""Stage distinct Ruins second/hidden maps and script-controlled falls.

Nothing is registered or activated. The first-room wall conditions and future
flag policy are deliberately unspecified; no item, flag or story is changed.
A neutral arrival-only warp prevents a changed party/bag from trapping return.
"""
import copy
from stage_hgss_ruins_hidden import stage as stage_rooms, NAMES

IDS=('MAP_RUINS_OF_ALPH_SOUTHWEST_SECOND_ROOM','MAP_RUINS_OF_ALPH_NORTHWEST_SECOND_ROOM',
     'MAP_RUINS_OF_ALPH_SOUTHWEST_HIDDEN_ROOM','MAP_RUINS_OF_ALPH_NORTHWEST_HIDDEN_ROOM')
FIRST=('MAP_RUINS_OF_ALPH_SOUTHWEST_CHAMBER','MAP_RUINS_OF_ALPH_NORTHWEST_CHAMBER')
LAYOUTS=('LAYOUT_RUINS_OF_ALPH_SOUTHWEST_SECOND_ROOM','LAYOUT_RUINS_OF_ALPH_NORTHWEST_SECOND_ROOM',
         'LAYOUT_RUINS_OF_ALPH_SOUTHWEST_HIDDEN_ROOM','LAYOUT_RUINS_OF_ALPH_NORTHWEST_HIDDEN_ROOM')


def warp(x,y,dest,index):return dict(x=x,y=y,elevation=0,dest_map=dest,dest_warp_id=str(index))


def map_data(name,map_id,layout):
    return dict(id=map_id,name=name,layout=layout,music='MUS_PETALBURG_WOODS',
        region='REGION_HOENN',region_map_section='MAPSEC_RUINS_OF_ALPH',
        requires_flash=False,weather='WEATHER_NONE',map_type='MAP_TYPE_UNDERGROUND',
        allow_cycling=False,allow_escaping=False,allow_running=True,show_map_name=False,
        battle_scene='MAP_BATTLE_SCENE_NORMAL',connections=None,object_events=[],
        warp_events=[],coord_events=[],bg_events=[])


def transition(x,y,label):
    return dict(type='trigger',x=x,y=y,elevation=0,var='VAR_TEMP_0',var_value='0',script=label)


def stage(write,first_rooms,read=None):
    """Return isolated map/layout/script and first-room proposals, not live changes."""
    tiles,sizes,borders,facts=stage_rooms(write,read)
    assert set(first_rooms)==set(FIRST)
    proposals=copy.deepcopy(first_rooms)
    for i,first_id in enumerate(FIRST):
        room=proposals[first_id]
        assert room['id']==first_id and len(room['warp_events'])==1
        assert all((e['x'],e['y'])!=(5,2) for e in room['warp_events'])
        # Return-only landing: its normal floor has no warp behavior. Gated
        # first-room interaction is still required to enter the second room.
        room['warp_events'].append(warp(5,2,IDS[i],0))
    maps={n:map_data(n,i,l) for n,i,l in zip(NAMES,IDS,LAYOUTS)}
    scripts={n:n+'_MapScripts::\n    .byte 0\n' for n in NAMES}
    # First pair: exit back to first room; north fall to its own hidden room.
    for i in (0,1):
        m=maps[NAMES[i]];m['warp_events']=[warp(6,17,FIRST[i],1)]
        dest=IDS[i+2];landing=facts[NAMES[i+2]]['fall_arrival']
        label=NAMES[i]+'_Fall';m['coord_events']=[transition(6,3,label)]
        scripts[NAMES[i]]+=(f'{label}::\n    lockall\n    warp {dest}, {landing[0]}, {landing[1]}\n'
                            '    waitstate\n    releaseall\n    end\n')
    # Second pair: only a scripted one-way fall into the actual expanded hall.
    for i in (2,3):
        m=maps[NAMES[i]];x,y=facts[NAMES[i]]['scripted_fall'];landing=facts[NAMES[i]]['hgss_hall_landing']
        label=NAMES[i]+'_Fall';m['coord_events']=[transition(x,y,label)]
        scripts[NAMES[i]]+=(f'{label}::\n    lockall\n    warp MAP_RUINS_OF_ALPH_UNDERGROUND_HALL, {landing[0]}, {landing[1]}\n'
                            '    waitstate\n    releaseall\n    end\n')
    layouts={}
    for n,lid in zip(NAMES,LAYOUTS):
        w,h,primary=sizes[n]
        layouts[lid]=dict(id=lid,name=n+'_Layout',width=w,height=h,
            primary_tileset=primary,secondary_tileset='gTileset_WesternInteriors',
            border_filepath=f'data/layouts/{n}/border.bin',
            blockdata_filepath=f'data/layouts/{n}/map.bin',layout_version='emerald')
    gates={FIRST[i]:dict(wall=[5,1],return_only_warp_index=1,return_floor=[5,2],
        second_room=IDS[i],condition_pending=True,open_art_pending=True,installed=False) for i in (0,1)}
    return maps,tiles,layouts,borders,scripts,proposals,gates
