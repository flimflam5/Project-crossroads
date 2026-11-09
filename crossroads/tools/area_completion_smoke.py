"""Actual controller traversal of completed landmarks, farm, and Gym halls."""
import json,struct
from collections import deque


def run(root,syms,lib,output,read,frames,key,walk,pos,verify_joe):
    group=json.loads((root/'data/maps/map_groups.json').read_text())['gMapGroup_CrossroadsOlivine']
    maps={n:json.loads((root/f'data/maps/{n}/map.json').read_text()) for n in group}
    byid={m['id']:n for n,m in maps.items()}
    def current():return group[read(read('gSaveBlock1Ptr')+5,1)]
    def close():
        for _ in range(18):
            if read('sLockFieldControls',1)==0:break
            key(1);frames(90)
        assert read('sLockFieldControls',1)==0
    def interact(e):
        name=current();x,y=e['x'],e['y']
        approaches=[((x,y+1),64),((x-1,y),16),((x+1,y),32),((x,y-1),128)]
        layout=next(l for l in json.loads((root/'data/layouts/layouts.json').read_text())['layouts'] if l['id']==maps[name]['layout'])
        if y==layout['height']-1:approaches=[((x,y-1),128)]+approaches[:-1]
        for target,k in approaches:
            try:walk(target,name)
            except AssertionError as err:
                if err.args:raise
                continue
            break
        else:raise AssertionError(('No approach',name,e))
        frames(1,k);frames(20);key(1);frames(180);close()
    def warp(index):
        name=current();e=maps[name]['warp_events'][index];x,y=e['x'],e['y']
        approaches=[((x,y+1),64),((x-1,y),16),((x+1,y),32),((x,y-1),128)]
        layout=next(l for l in json.loads((root/'data/layouts/layouts.json').read_text())['layouts'] if l['id']==maps[name]['layout'])
        if y==layout['height']-1:approaches=[((x,y-1),128)]+approaches[:-1]
        for target,k in approaches:
            try:walk(target,name)
            except AssertionError as err:
                if err.args:raise
                continue
            break
        else:raise AssertionError(('No warp approach',name,e))
        for _ in range(2):
            frames(16,k);frames(180)
            if current()!=name:break
        assert current()==byid[e['dest_map']],(name,e,current(),pos())
        verify_joe()
        return name
    def chain(ground,upcount):
        seen=[]
        for i in range(upcount):
            name=current();assert name==ground if i==0 else name in group
            seen.append(name)
            assert lib.emu_image(str(output/f'{name}.png').encode())
            for e in maps[name]['bg_events']:interact(e)
            if i==upcount-1:
                for o in maps[name]['object_events']:interact(o)
                assert lib.emu_state(str(output/f'{ground}-top.snapshot').encode(),0)
                break
            warp(2 if i==0 else 1)
        for name in reversed(seen[:-1]):warp(0);assert current()==name
        print('Full climb/descent and top interactions:',ground,len(seen),'floors: PASS',flush=True)
    # The baseline detail checks finish outside the harbor office in Olivine.
    walk((39,33),'OlivineCity');frames(16,64);frames(180)
    assert current()=='OlivineCity_Lighthouse_1F'
    chain(current(),6);warp(0);assert current()=='OlivineCity'
    # Both practice halls are entered/exited; battle tests use a separate fixture.
    walk((38,10));frames(16,64);frames(180);assert current()=='OlivineCity_Gym'
    warp(2);assert current()=='OlivineCity_Gym_Arena'
    assert lib.emu_image(str(output/'jasmine-hall.png').encode())
    warp(0);warp(0);assert current()=='OlivineCity'
    # Farm buildings reached from the existing road network, not debug warps.
    walk((28,0));frames(16,64);frames(180);assert current()=='JohtoRoute39'
    for i,n in [(0,'JohtoRoute39_FarmHouse'),(1,'JohtoRoute39_Barn')]:
        warp(i);assert current()==n
        assert lib.emu_image(str(output/f'{n}.png').encode())
        if i==1:
            for o in maps[n]['object_events']:interact(o)
        warp(0);assert current()=='JohtoRoute39'
    walk((12,0),'JohtoRoute39');frames(16,64);frames(180)
    walk((63,13),'JohtoRoute38');frames(16,16);frames(180);assert current()=='EcruteakCity'
    # Existing city warp indices: Burned Tower 0, Bell Tower 1, Theater 3, Gym 4.
    warp(0);assert current()=='EcruteakCity_BurnedTower'
    warp(2);assert current()=='EcruteakCity_BurnedTower_B1F'
    for e in maps[current()]['bg_events']:interact(e)
    assert lib.emu_image(str(output/'burned-basement.png').encode())
    warp(0);warp(0);assert current()=='EcruteakCity'
    warp(1);chain('EcruteakCity_BellTower',9);warp(0);assert current()=='EcruteakCity'
    warp(4);warp(2);assert current()=='EcruteakCity_Gym_Arena'
    assert lib.emu_image(str(output/'morty-hall.png').encode())
    warp(0);warp(0);assert current()=='EcruteakCity'
    warp(3);assert current()=='EcruteakCity_DanceTheater'
    host=maps[current()]['object_events'][0];interact(host)
    for o in maps[current()]['object_events'][1:]:
        lid=o['local_id'];event_id=read(syms['gSpecialVar_LastTalked'],2) if False else None
        # Movement scripts restore all authored dancer positions; inspect actual objects.
        assert any(read(syms['gObjectEvents']+j*36+0x10,2)==o['x']+7 and read(syms['gObjectEvents']+j*36+0x12,2)==o['y']+7 for j in range(16)),('Dancer did not return',o)
    assert lib.emu_image(str(output/'theater-performance.png').encode())
    warp(0)
    print('All landmark floors, farmhouse/barn, milk herd, both Gym halls and repeatable theater performance: PASS',flush=True)
