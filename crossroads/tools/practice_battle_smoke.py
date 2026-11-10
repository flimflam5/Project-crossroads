"""Real optional battle flows; RAM-only boosted Elgyem tests flow, not balance."""
import json
import struct


def run(root,syms,lib,out,read,write,frames,key,walk,pos,verify_joe):
    names=json.loads((root/'data/maps/map_groups.json').read_text())['gMapGroup_CrossroadsOlivine']
    def current():return names[read(read('gSaveBlock1Ptr')+5,1)]
    def cross(k,name):
        old=current()
        for _ in range(2):
            frames(16,k);frames(180)
            if current()!=old:break
        assert current()==name,(name,current(),pos())
    def close():
        for _ in range(12):
            if not read('sLockFieldControls',1):break
            key(1);frames(90)
        assert not read('sLockFieldControls',1)
    p=read('gPlayerPartyPtr')
    # Keep secure EXP consistent with the private level-50 fixture; a raw level
    # change alone makes the normal EXP-bar animation wait on an invalid range.
    personality=read(p);ot=read(p+4);cipher=personality^ot
    secure=bytearray().join(struct.pack('<I',read(p+32+i*4)^cipher) for i in range(12))
    order=[0,0,0,0,0,0,1,1,2,3,2,3,1,1,2,3,2,3,1,1,2,3,2,3]
    struct.pack_into('<I',secure,order[personality%24]*12+4,125000)
    write(p+28,sum(struct.unpack('<24H',secure))&0xffff,2)
    for i in range(12):write(p+32+i*4,struct.unpack_from('<I',secure,i*4)[0]^cipher)
    write(p+84,50,1)
    for off,value in [(86,500),(88,500),(90,200),(92,200),(94,200),(96,200),(98,200)]:write(p+off,value,2)
    badge_base=0x867
    def badges():
        sb=read('gSaveBlock1Ptr');return tuple((read(sb+0x1270+(i//8),1)>>(i%8))&1 for i in range(badge_base,badge_base+8))
    before=badges()
    def battle(x,y,label,trainer_id):
        name=current();walk((x,y+1),name);frames(1,64);frames(20)
        key(1);frames(180);key(1);frames(120);key(1);frames(180)
        assert read(syms['gMain']+4)!=syms['CB2_Overworld']|1,(label,'did not enter battle')
        assert read(syms['gTrainerBattleParameter']+2,2)==trainer_id,(label,read(syms['gTrainerBattleParameter']+2,2))
        frames(240)
        assert lib.emu_image(str(out/f'{label}-intro.png').encode())
        for _ in range(100):
            if read(syms['gMain']+4)==syms['CB2_Overworld']|1:break
            key(1);frames(120)
        if read(syms['gMain']+4)!=syms['CB2_Overworld']|1:
            lib.emu_image(str(out/f'{label}-pending.png').encode())
            lib.emu_state(str(out/f'{label}-pending.snapshot').encode(),0)
        assert read(syms['gMain']+4)==syms['CB2_Overworld']|1,(label,'battle did not return')
        close();assert current()==name;verify_joe();assert badges()==before,'No badges may be awarded'
        print('Practice battle and return, no badge:',label,'PASS',flush=True)
    walk((38,10));cross(64,'OlivineCity_Gym')
    walk((7,3),'OlivineCity_Gym');cross(64,'OlivineCity_Gym_Arena')
    battle(6,3,'jasmine',855);battle(6,3,'jasmine-repeat',855);battle(2,10,'steel-student',857)
    walk((6,16),current());cross(128,'OlivineCity_Gym')
    walk((3,6),current());cross(128,'OlivineCity')
    walk((28,0));cross(64,'JohtoRoute39');battle(16,27,'farmhand',859)
    walk((12,0),current());cross(64,'JohtoRoute38');battle(39,17,'birdwatcher',860)
    walk((63,13),current());cross(16,'EcruteakCity')
    city=json.loads((root/'data/maps/EcruteakCity/map.json').read_text());w=city['warp_events'][4]
    walk((w['x'],w['y']+1),current());cross(64,'EcruteakCity_Gym')
    walk((7,3),current());cross(64,'EcruteakCity_Gym_Arena')
    battle(6,3,'morty',856);battle(2,10,'ghost-student',858)
    print('Six optional trainers, leader repeat, proper returns and no badge/progression award: PASS. Balance requires normal-level owner QA.',flush=True)
