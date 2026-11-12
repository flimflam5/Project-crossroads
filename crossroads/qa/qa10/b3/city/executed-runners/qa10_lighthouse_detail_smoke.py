#!/usr/bin/env python3
"""Actual lighthouse components, window/lift journeys and normal cold saves."""
import argparse
from pathlib import Path
from qa10_city_runtime import load
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');p.add_argument('--output',required=True);p.add_argument('--rom-sha256',required=True);args=p.parse_args()
h=load(args.save,args.library,args.output,args.rom_sha256)
journeys=[]
def main():
    go,walk=h['go'],h['walk'];d=h['d']
    # Public source components are selected through real doors/stairs, not XY writes.
    cases=[('1F',0,(8,12),0),('2F',0,(8,12),0),('3F',0,(13,9),0),('3F',5,(8,16),5),('4F',0,(12,9),0),('4F',3,(5,9),3),('5F',0,(8,12),0),('6F',0,(11,13),0),('Balcony',0,(14,9),0),('Elevator',None,(4,4),0)]
    for suffix,entry,near,exit_index in cases:
        name='OlivineCity_Lighthouse_'+suffix;go(name,entry);target=h['clear_point'](name,near);walk(target)
        label='lighthouse-'+suffix+'-component-'+str(entry);h['shot'](label+'-context');h['save_continue'](label+'-normal-save')
        x,y=h['pos']();away=next(q for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] if q not in d['active_warps'](name) and d['safe'](name,q) and d['raw'][name][q[1]*d['size'][name][0]+q[0]]>>12==3 and d['path'](name,q) is not None)
        walk(away);assert not h['read']('gPlayerAvatar',1)&8
        d['warp'](exit_index);departed=h['current']();assert departed!=name
        go(name,entry);walk(target);h['records'][-1].update(actual_walk_away=away,actual_exit=departed,actual_return_to_saved_point=True)
    go(d['WINDOW'],'window')
    def window_trip():
        d['window_fall']();assert h['current']()==d['BALCONY'] and h['pos']()==(14,9)
        h['shot']('lighthouse-window-balcony-arrival');walk((14,10))
    h['capture']('lighthouse-window-fall',window_trip)
    go('OlivineCity_Lighthouse_3F',3);go('OlivineCity_Lighthouse_4F',1);go('OlivineCity_Lighthouse_5F');go('OlivineCity_Lighthouse_6F');go('OlivineCity_Lighthouse_1F')
    journeys.append(dict(case='4F window/balcony/southern3F/western4F/5F/6F/ground return',result='PASS'))
    for floor in ['OlivineCity_Lighthouse_1F','OlivineCity_Lighthouse_6F']:
        for leaf in [0,1]:
            go(d['LIFT'])
            def ride(floor=floor,leaf=leaf):
                # Both source floor targets are native0x61 portals at8,4:
                # no animated-door exit step is inferred for this behavior.
                d['lift'](floor,leaf);arrival=h['pos']();facing=h['facing']();assert h['current']()==floor and arrival==(8,4) and facing==1,(floor,leaf,arrival,facing)
                h['shot'](floor+'-lift-leaf-'+str(leaf));walk((9,5));journeys.append(dict(case='native lift',floor=floor,exit_leaf=leaf,arrival=arrival,facing=facing,actual_walk_away=h['pos'](),result='PASS'))
            h['capture'](floor+'-lift-leaf-'+str(leaf),ride)
    # Both selected dynamic destinations must survive a normal cold Continue.
    for x,floor in [(2,'OlivineCity_Lighthouse_1F'),(5,'OlivineCity_Lighthouse_6F')]:
        go(d['LIFT']);walk((x,3));h['frames'](1,64);h['frames'](20);h['key'](1);h['frames'](180);h['close']()
        assert d['dynamic_destination']()[0]==floor
        h['save_continue']('lighthouse-selected-'+floor+'-normal-save');walk((4,4));d['warp'](0);assert h['current']()==floor
        h['records'][-1].update(selected_floor_retained=True,actual_exit=floor)
    go('OlivineCity');assert h['read']('sJohtoTestAccess',1)==0
    h['finish'](dict(journeys=journeys));print('Lighthouse details PASS:',len(h['records']),'normal Save/cold Continue cases;',len(journeys),'special journeys',flush=True)
try:main()
except Exception as error:
    h['lib'].emu_image(str(Path(args.output)/'failure.png').encode());h['finish'](dict(journeys=journeys),str(error));raise
