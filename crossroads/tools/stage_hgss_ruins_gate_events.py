#!/usr/bin/env python3
"""Stage nonpersistent, source-conditioned Ruins gate interactions.

SW opens only when Water Stone is actually used on the correct wall; NW uses
an explicit non-egg Ho-Oh party special. The opening is temporary and resets
when the map reloads; return arrivals are always on safe neutral floor.
"""
import copy
from stage_hgss_ruins_hidden_graph import FIRST,IDS,warp


def stage(first_proposals,source_scripts,open_metatile):
    assert set(first_proposals)==set(FIRST) and set(source_scripts)==set(FIRST)
    assert open_metatile==40
    maps=copy.deepcopy(first_proposals);scripts=copy.deepcopy(source_scripts)
    for index,first_id in enumerate(FIRST):
        room=maps[first_id];name=room['name'];label=name+'_HiddenGate';text=label+'_Text'
        assert len(room['warp_events'])==2 and (room['warp_events'][1]['x'],room['warp_events'][1]['y'])==(5,2)
        assert not any((e['x'],e['y'])==(5,1) for e in room['bg_events'])
        # Warp 1 is a neutral return-only arrival; warp 2 is the actual gate.
        room['warp_events'].append(warp(5,1,IDS[index],0))
        room['bg_events'].append(dict(type='sign',x=5,y=1,elevation=0,
            player_facing_dir='BG_EVENT_PLAYER_FACING_NORTH',script=label))
        if index==0:
            # The field-use callback calls this exported label only after the
            # Water Stone is used while facing the correct wall.
            used=name+'_WaterStoneUsed'
            scripts[first_id] += (f'\n{label}::\n    msgbox {text}, MSGBOX_SIGN\n    end\n'
                f'{text}:\n    .string "WATER$"\n'
                f'{used}::\n    lockall\n    setmetatile 5, 1, {open_metatile}, FALSE\n'
                f'    special DrawWholeMapView\n    releaseall\n    end\n')
        else:
            closed=label+'_Closed'
            scripts[first_id] += (f'\n{label}::\n    lockall\n'
                '    specialvar VAR_RESULT, Crossroads_AlphHasNonEggHoOh\n'
                f'    goto_if_eq VAR_RESULT, FALSE, {closed}\n'
                f'    setmetatile 5, 1, {open_metatile}, FALSE\n    special DrawWholeMapView\n'
                f'    releaseall\n    end\n{closed}::\n    msgbox {text}, MSGBOX_SIGN\n    releaseall\n    end\n'
                f'{text}:\n    .string "HO-OH$"\n')
    return maps,scripts
