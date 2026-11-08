"""Controller-driven detail checks on the existing Olivine maps."""
import json


def run(root,syms,lib,output,read,write,frames,key,walk,pos,verify_joe,western):
    def location():
        sb=read('gSaveBlock1Ptr')
        return read(sb+4,1),read(sb+5,1)
    def exit_to_city(name):
        m=json.loads((root/f'data/maps/{name}/map.json').read_text())
        w=m['warp_events'][0]
        walk((w['x'],w['y']-1),name)
        for _ in range(2):
            frames(16,128);frames(180)
            if location()==(75,0):break
        assert location()==(75,0),(name,location(),pos())
        verify_joe()
    def close():
        for _ in range(12):
            if read('sLockFieldControls',1)==0:break
            key(1);frames(90)
        assert read('sLockFieldControls',1)==0
    def interact(name,event):
        x,y=event['x'],event['y']
        for target,button in [((x,y+1),64),((x-1,y),16),((x+1,y),32),((x,y-1),128)]:
            try:walk(target,name)
            except AssertionError as error:
                if error.args:raise
                continue
            break
        else:raise AssertionError(('No interaction approach',event))
        frames(1,button);frames(20);key(1);frames(180)
    # Existing regression finishes in Ecruteak Center with an actual rescued mon.
    walk((7,7),'EcruteakCity_PokemonCenter_1F')
    for _ in range(2):
        frames(16,128);frames(180)
        if location()==(75,10):break
    assert location()==(75,10)
    western[1]()
    walk((11,10));frames(16,64);frames(180)
    assert location()==(75,1)
    name='OlivineCity_Residence'
    home=json.loads((root/f'data/maps/{name}/map.json').read_text())
    rest=next(e for e in home['bg_events'] if e['script']=='Olivine_HomeRest')
    p=read('gPlayerPartyPtr');write(p+86,1,2)
    sb=read('gSaveBlock1Ptr')
    heal=bytes(read(sb+0x1c+i,1) for i in range(8))
    choice=read(sb+0x139c+500,2)
    interact(name,rest)
    key(128);key(1);frames(180)
    assert read(read('gPlayerPartyPtr')+86,2)==1,'Declining rest must not heal'
    assert read('sLockFieldControls',1)==0
    write(read('gPlayerPartyPtr')+80,8,4) # Poison, without taking another field step.
    interact(name,rest)
    key(1);frames(600);close()
    p=read('gPlayerPartyPtr')
    assert read(p+86,2)==read(p+88,2) and read(p+80,4)==0
    sb=read('gSaveBlock1Ptr')
    assert bytes(read(sb+0x1c+i,1) for i in range(8))==heal,'Home rest must preserve last Center respawn'
    assert read(sb+0x139c+500,2)==choice and read(read('gPlayerPartyCountPtr'),1)==1
    for e in home['bg_events']:
        if e['script']!='Olivine_HomeRest':interact(name,e);close()
    assert lib.emu_image(str(output/'joe-home-rest.png').encode())
    exit_to_city(name)
    for suffix,x,y,index in [('SilphOffice',37,22,6),('HarborOffice',12,33,7)]:
        walk((x,y));frames(16,64);frames(180)
        assert location()==(75,index)
        name='OlivineCity_'+suffix
        assert lib.emu_image(str(output/f'detailed-{suffix}.png').encode())
        m=json.loads((root/f'data/maps/{name}/map.json').read_text())
        for e in m['bg_events']:interact(name,e);close()
        exit_to_city(name)
    assert read('gFonts')!=0
    print('Home rest decline/accept, unchanged choice/respawn, home notes/books, office terminal/checklists and harbor records/dispatch: PASS',flush=True)
