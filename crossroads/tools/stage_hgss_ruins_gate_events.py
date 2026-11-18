#!/usr/bin/env python3
"""Stage no-permanent-flag HGSS gate candidates without registering them.

Checks current Water Stone / Ho-Oh party state on interaction. The original
persistent-open state is intentionally not implemented; the planned neutral
return tile remains safe if the condition later changes. Behavior and the
conditional art require real engine and visual testing before installation.
"""
import copy
from stage_hgss_ruins_hidden_graph import FIRST,IDS


def stage(first_proposals,source_scripts,open_metatile):
    assert set(first_proposals)==set(FIRST) and set(source_scripts)==set(FIRST)
    assert open_metatile==40
    maps=copy.deepcopy(first_proposals);scripts=copy.deepcopy(source_scripts)
    for index,first_id in enumerate(FIRST):
        room=maps[first_id];name=room['name'];label=name+'_HiddenGate';closed=label+'_Closed';text=label+'_ClosedText'
        assert len(room['warp_events'])==2 and (room['warp_events'][1]['x'],room['warp_events'][1]['y'])==(5,2)
        assert not any((e['x'],e['y'])==(5,1) for e in room['bg_events'])
        room['bg_events'].append(dict(type='sign',x=5,y=1,elevation=0,
            player_facing_dir='BG_EVENT_PLAYER_FACING_NORTH',script=label))
        condition='checkitem ITEM_WATER_STONE, 1' if index==0 else 'checkspecies SPECIES_HO_OH'
        scripts[first_id] += (f'\n{label}::\n    lockall\n    {condition}\n'
          f'    goto_if_eq VAR_RESULT, FALSE, {closed}\n'
          f'    setmetatile 5, 1, {open_metatile}, FALSE\n    special DrawWholeMapView\n'
          f'    warp {IDS[index]}, 6, 17\n    waitstate\n    releaseall\n    end\n'
          f'{closed}::\n    msgbox {text}, MSGBOX_SIGN\n    releaseall\n    end\n'
          f'{text}:\n    .string "Nothing happened...$"\n')
    return maps,scripts
