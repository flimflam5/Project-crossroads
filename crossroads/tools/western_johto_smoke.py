"""Controller-driven western Johto tour, called by emulator_smoke.py."""
import json


def tour(root, syms, lib, output, read, frames, key, walk, pos, verify_joe):
    def location():
        sb=read('gSaveBlock1Ptr')
        return read(sb+4,1),read(sb+5,1)

    def expect(index, xy=None):
        assert location()==(75,index),(index,location(),pos())
        assert read(syms['gMain']+4)==syms['CB2_Overworld']|1
        if xy is not None:assert pos()==xy,(xy,pos())
        verify_joe()

    def cross(button,index,xy):
        before=location()
        # Interior arrow exits trigger when walking off the doorway tile.
        for _ in range(2):
            frames(16,button)
            frames(180)
            if location()==(75,index):break
            assert location()==before, ('Unexpected transition',before,location())
        expect(index,xy)

    def close_dialogue():
        for _ in range(12):
            if read('sLockFieldControls',1)==0:break
            key(1)
            frames(90)
        assert read('sLockFieldControls',1)==0,'Interaction must release controls'

    def outbound():
        walk((28,0))
        cross(64,8,(12,47))
        walk((12,0),'JohtoRoute39')
        cross(64,9,(12,27))
        walk((63,13),'JohtoRoute38')
        cross(16,10,(0,27))

    def inbound():
        walk((0,27),'EcruteakCity')
        cross(32,9,(63,13))
        walk((12,27),'JohtoRoute38')
        cross(128,8,(12,0))
        walk((12,47),'JohtoRoute39')
        cross(128,0,(28,0))

    outbound()
    assert lib.emu_image(str(output/'ecruteak-arrival.png').encode())
    city=json.loads((root/'data/maps/EcruteakCity/map.json').read_text())
    map_names=json.loads((root/'data/maps/map_groups.json').read_text())['gMapGroup_CrossroadsOlivine']
    for i,warp in enumerate(city['warp_events']):
        walk((warp['x'],warp['y']+1),'EcruteakCity')
        cross(64,11+i,None)
        name=map_names[11+i]
        assert lib.emu_image(str(output/f'ecruteak-interior-{i}.png').encode())
        if i<5:
            walk((7,6),name)
            frames(1,64)
            frames(20)
            key(1)
            frames(150)
            close_dialogue()
            interior=json.loads((root/f'data/maps/{name}/map.json').read_text())
            exit=interior['warp_events'][0]
            walk((exit['x'],exit['y']-1),name)
        if i==5:
            sb=read('gSaveBlock1Ptr')
            assert (read(sb+0x1c,1),read(sb+0x1d,1))==(75,10),'Center must register Ecruteak respawn'
        cross(128,10,None)
        print('Ecruteak doorway/return and Joe:',name,flush=True)
    # All outdoor signs/NPCs are interacted with through actual controller input.
    for event in city['object_events']+city['bg_events']:
        x,y=event['x'],event['y']
        for target,button in [((x,y+1),64),((x-1,y),16),((x+1,y),32),((x,y-1),128)]:
            try:
                walk(target,'EcruteakCity')
                break
            except AssertionError:
                continue
        else:
            raise AssertionError(('No reachable interaction approach',event))
        frames(1,button)
        frames(20)
        key(1)
        frames(150)
        close_dialogue()
        expect(10)
    assert lib.emu_image(str(output/'ecruteak-tour.png').encode())
    inbound()
    print('Olivine/39/38/Ecruteak border round-trip, seven interiors, NPC/sign interactions and respawn registration: PASS',flush=True)
    return outbound, inbound
