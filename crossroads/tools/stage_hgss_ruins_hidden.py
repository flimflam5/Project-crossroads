#!/usr/bin/env python3
"""Stage four unregistered Ruins rooms from pinned HGSS geometry and HNS art.

The existing map network, reward flags, scripts and saves are never modified.
The returned GBA adaptation needs separately approved entrance/exit scripts,
a compatible underground hall, visual review and emulator testing.
"""
from collections import deque
import hashlib, json, struct, tempfile
from pathlib import Path
import prepare_hns_ruins_pockets as packer

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'crossroads/donor/hns-ruins-hidden'
FACTS=ROOT/'crossroads/hgss/canonical_events/ruins-hidden-geometry.json'
NAMES=('RuinsOfAlph_SouthwestSecondRoom','RuinsOfAlph_NorthwestSecondRoom',
       'RuinsOfAlph_SouthwestHiddenRoom','RuinsOfAlph_NorthwestHiddenRoom')
GROUPS={
 'second': {'source':'RuinsOfAlph_PuzzleAndRewardChambers_hns','width':26,'height':68,
            'primary':'johto_building_hns','secondary':'ruins_of_alph_writing_hns',
            'crops':{'NorthwestSecond':(0,34,10,11),'SouthwestSecond':(0,51,10,11)}},
 'northwest': {'source':'RuinsOfAlph_WordsRoom1_hns','width':20,'height':17,
               'primary':'johto_building_hns','secondary':'ruins_of_alph_writing_hns',
               'crops':{'NorthwestHidden':(0,0,20,17)}},
 'southwest': {'source':'RuinsOfAlph_WordsRoom3_hns','width':20,'height':13,
               'primary':'johto_building_hns','secondary':'ruins_of_alph_writing_hns',
               'crops':{'SouthwestHidden':(0,0,20,13)}}}


def readwords(path):
    data=path.read_bytes();assert len(data)%2==0
    return list(struct.unpack('<%dH'%(len(data)//2),data))


def reference_component(perms,seed):
    q=deque([tuple(seed)]);seen=set(q)
    while q:
        x,y=q.popleft()
        for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0<=xx<32 and 0<=yy<32 and (xx,yy) not in seen and not perms[yy*32+xx]&0x8000:
                seen.add((xx,yy));q.append((xx,yy))
    return seen


def stage(write):
    manifest=json.loads((SOURCE/'source-sha256.json').read_text())
    assert manifest['revision']=='167aa6d537b109bb229c231ddce4616974c4da71'
    for path,digest in manifest['files'].items():
        assert hashlib.sha256((SOURCE/path).read_bytes()).hexdigest()==digest,path
    facts=json.loads(FACTS.read_text());assert facts['revision']=='6bf138d6035aa6b43d6f8f4132a12df70f86dcec'
    # The shared conversion routine verifies visual tile/palette mapping and
    # source collision bits before any separately documented GBA adaptation.
    with tempfile.TemporaryDirectory(prefix='ruins-hidden-') as td:
        root=Path(td);old=packer.SOURCE;packer.SOURCE=SOURCE
        try:
            reports={k:packer.convert(g,root/k) for k,g in GROUPS.items()}
        finally:packer.SOURCE=old
        blanks={};pits={}
        for group in GROUPS:
            src=root/group;dst='data/tilesets/primary/hgss_ruins_hidden_'+group
            meta=readwords(src/'metatiles.bin');attributes=readwords(src/'metatile_attributes.bin')
            assert len(meta)==len(attributes)*8
            blanks[group]=len(attributes);meta += [0]*8;attributes.append(0)
            if group!='second':
                donor_name='SouthwestHidden' if group=='southwest' else 'NorthwestHidden'
                y=10 if group=='southwest' else 14
                old=readwords(src/(donor_name+'.bin'))[y*20+17]&1023
                assert attributes[old]==0x000f
                pits[group]=len(attributes);meta += meta[old*8:old*8+8];attributes.append(0x0008)
            write(dst+'/tiles.png',(src/'tiles.png').read_bytes())
            write(dst+'/metatiles.bin',struct.pack('<%dH'%len(meta),*meta))
            write(dst+'/metatile_attributes.bin',struct.pack('<%dH'%len(attributes),*attributes))
            for i in range(16):write(dst+f'/palettes/{i:02}.pal',(src/'palettes'/f'{i if i<5 else 0:02}.pal').read_bytes())
        source_second=readwords(root/'second'/'SouthwestSecond.bin')
        assert source_second[10:]==readwords(root/'second'/'NorthwestSecond.bin')[10:]
        words={'southwest':readwords(root/'southwest'/'SouthwestHidden.bin'),
               'northwest':readwords(root/'northwest'/'NorthwestHidden.bin')}
        attrs={g:readwords(root/g/'metatile_attributes.bin') for g in GROUPS}
    assert {g:(r['metatiles'],r['tiles'],len(r['palette_banks'])) for g,r in reports.items()}=={
        'second':(27,50,5),'southwest':(36,101,5),'northwest':(37,105,5)}
    second=facts['second'];component=reference_component(second['permissions'],second['exit'])
    assert len(component)==115 and tuple(second['fall']) in component
    # Donor stone, columns and four empty plinths; the first room's conditional
    # gate and the actual scripted drop are separate future integration work.
    plane=[0x0400|blanks['second']]*(14*20)
    for x,y in component:plane[y*14+x]=0x3013
    for x in range(2,11):plane[2*14+x]=0x0400
    for y in range(3,18):plane[y*14+1]=0x040b;plane[y*14+11]=0x040c
    for x in range(1,12):plane[18*14+x]=0x0408
    for x in (4,8):
        assert (x,3) not in component and (x,4) not in component
        plane[3*14+x]=0x0419;plane[4*14+x]=0x0415
    for x,y in second['southwest_object_positions']:
        assert (x,y) in component;plane[y*14+x]=0x3018
    assert second['southwest_object_positions']==second['northwest_object_positions']
    plane[17*14+6]=0x301a  # HNS south-warp graphic/behavior, no event yet.
    planes={NAMES[0]:plane.copy(),NAMES[1]:plane.copy()}
    layouts={};borders={};transitions={}
    for name in NAMES[:2]:
        layouts[name]=(14,20,'gTileset_HgssRuinsHiddenSecond')
        borders[name]=[0x0400|blanks['second']]*4
        transitions[name]=dict(ordinary_exit=[6,17],scripted_fall=[6,3],
            unapproved_reward_positions=second['southwest_object_positions'],
            events_installed=False)
    for direction,index,donor_height in [('southwest',2,13),('northwest',3,17)]:
        f=facts[direction+'_hidden'];seed=f['landing'];exit=f['exit'];component=reference_component(f['permissions'],seed)
        assert tuple(exit) in component
        assert len(component)==(260 if direction=='southwest' else 420)
        w,h=(24,19) if direction=='southwest' else (24,27)
        assert all(0<=x<w and 0<=y<h for x,y in component)
        donor=words[direction];a=attrs[direction]
        # Preserve HNS inscription motifs where they are usable floor; all
        # collisions are set by the HGSS permission component, not donor doors.
        ground=donor[3*20+3];assert not ground&0xc00 and a[ground&1023]&255==8
        output=[0x0400|blanks[direction]]*(w*h)
        xmin,xmax=min(x for x,y in component),max(x for x,y in component)
        ymin,ymax=min(y for x,y in component),max(y for x,y in component)
        for x,y in component:output[y*w+x]=(ground&1023)|0x3000
        for sy in range(3,donor_height-1):
            for sx in range(1,19):
                x=xmin+round((sx-1)*(xmax-xmin)/17)
                y=ymin+round((sy-2)*(ymax-ymin)/(donor_height-3))
                t=donor[sy*20+sx]
                if (x,y) in component and not t&0xc00 and a[t&1023]&255 in (0,8):
                    output[y*w+x]=(t&1023)|0x3000
        # Neutral behavior: the future coordinate event owns the fall rather
        # than HNS's incompatible donor hole behavior 0x0f.
        output[exit[1]*w+exit[0]]=0x3000|pits[direction]
        # Edge stone uses the corresponding donor room's top/bottom/side art.
        for y in range(h):
            for x in range(w):
                if (x,y) in component:continue
                if (x,y+1) in component:output[y*w+x]=0x0401
                elif (x,y-1) in component:output[y*w+x]=0x040a
                elif (x+1,y) in component:output[y*w+x]=0x0407
                elif (x-1,y) in component:output[y*w+x]=0x0408
        name=NAMES[index];planes[name]=output
        layouts[name]=(w,h,'gTileset_HgssRuinsHidden'+direction.title())
        borders[name]=[0x0400|blanks[direction]]*4
        transitions[name]=dict(fall_arrival=seed,scripted_fall=exit,
                                hgss_hall_landing=f['hall_landing'],events_installed=False)
    return planes,layouts,borders,transitions
