#!/usr/bin/env python3
"""Controller capture of owner-reported cave holes and native exit arrows.

Run from a fully linked checkout with its matching pokeemerald.gba/.elf. The
mGBA bridge and a copied-compatible QA10 battery are required. This runs real
controller input. The shared network helper enables Survey at its in-game desk
and disables random encounters only in emulator RAM. It does not write map,
warp, inventory, or player-position state. Never pass the owner's only save.

    python3 crossroads/tools/union_cave_visual_smoke.py --save QA.sav \\
        --rom-sha256 SHA256 --elf-sha256 SHA256 --library /tmp/johto-bridge.so --output /tmp/cave-captures

Output contains still frames, optional clips and coverage, not the input save.
Individual arrow animation frames are kept for inspection; black pixels alone
are not an assertion because exterior void is intentional. Repeat independently
on baseline and candidate ROMs before comparing same-named captures.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

R=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('--save',type=Path,required=True)
parser.add_argument('--rom-sha256',required=True)
parser.add_argument('--elf-sha256',required=True)
parser.add_argument('--library',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
out=args.output.resolve()
if out.exists() and any(out.iterdir()):raise SystemExit('Use a new, empty output directory')
out.mkdir(parents=True,exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rom=R/'pokeemerald.gba';elf=R/'pokeemerald.elf'
assert sha(rom)==args.rom_sha256 and elf.is_file() and sha(elf)==args.elf_sha256,'ROM or ELF hash mismatch'
original=sha(args.save)
report={'rom_sha256':args.rom_sha256,'elf_sha256':args.elf_sha256,'cases':[],'setup':'copied battery; Survey enabled in-game; encounters disabled only in emulator RAM','result':'IN PROGRESS'}

def save_report():
    (out/'coverage.json').write_text(json.dumps(report,indent=2)+'\n')
def record(**case):
    report['cases'].append(case);save_report();print('PASS',case,flush=True)

with tempfile.TemporaryDirectory(prefix='black-ledger-cave-private-') as tmp:
    private=Path(tmp);battery=private/'qa-copy.sav';shutil.copyfile(args.save,battery)
    sys.path.insert(0,str(R/'crossroads/tools'))
    sys.argv=['johto_network_smoke.py','--save',str(battery),'--library',str(args.library.resolve()),'--output',str(private/'network'),'--targets','']
    network=R/'crossroads/tools/johto_network_smoke.py';source=network.read_text()
    # Match actual engine traversal at elevation-0 threshold cells. Fail closed
    # if the helper changes, rather than silently running a different test.
    changes=[('arrival_only=arrivals();gate_borders=gate_connections();warp_trials=[];dry_only=False','arrival_only=arrivals();gate_borders=gate_connections();warp_trials=[];dry_only=True'),
             ("assert read('sJohtoTestAccess',1)==1\nfor n in targets:","assert read('sJohtoTestAccess',1)==1\ndry_only=False\nroute_cache.clear()\nfor n in targets:"),
             ('raw[n][y*w+x]>>12==3','raw[n][y*w+x]>>12 in (0,3)'),
             ('raw[n][y*w+x]>>12 in (1,3)','raw[n][y*w+x]>>12 in (0,1,3)')]
    for old,new in changes:
        assert source.count(old)==1,('network smoke helper drift',old)
        source=source.replace(old,new)
    d={'__file__':str(network),'__name__':'__main__'}
    exec(compile(source,str(network),'exec'),d)
    go,walk,frames,current,pos,lib=[d[n] for n in ('go','walk','frames','current','pos','lib')]
    def capture(name):
        assert lib.emu_image(str(out/(name+'.png')).encode()),name
    def on_map(name):assert current()==name,(name,current(),pos())

    # Match screenshot compositions at the ladder pocket, 2-cell hole, and
    # eastern edge notches. The adjacent ladder viewpoint captures camera drift.
    views=[('ladder-pocket',(7,27),0),('ladder-pocket-south',(7,28),0),
           ('two-tile-shelf',(23,69),2),('eastern-edge',(28,57),2)]
    for title,target,warp_index in views:
        go('UnionCave_1F',warp_index);walk(target)
        on_map('UnionCave_1F');assert pos()==target;frames(60);capture(title)
        record(kind='owner_viewpoint',map='UnionCave_1F',position=target,image=title+'.png')

    # Confirm native ladders still connect and return through reciprocal indices.
    go('UnionCave_1F',0);d['warp'](0);on_map('UnionCave_2F');capture('ladder-basement-arrival')
    d['warp'](0);on_map('UnionCave_1F');record(kind='ladder_roundtrip',source_index=0)

    # Capture every frame of each south-facing threshold approach. Each actual
    # transition must complete and return by its reciprocal warp. The recording
    # allows visual inspection of the cue without assuming a particular palette.
    for index in (1,2,6,7):
        go('UnionCave_1F',index);event=d['maps']['UnionCave_1F']['warp_events'][index]
        x,y=event['x'],event['y'];approach=(x,y-1);walk(approach)
        on_map('UnionCave_1F');assert pos()==approach and d['behavior']('UnionCave_1F',x,y)==0x65
        folder=out/f'arrow-{index}-frames';folder.mkdir()
        samples=[]
        for frame in range(36):
            frames(1,128 if frame<16 else 0)
            assert lib.emu_image(str(folder/f'{frame:03}.png').encode())
            # Observe the engine's actual warp-arrow object rather than infer
            # it from pixels. Struct sizes/offsets match global.fieldmap.h and
            # sprite.h; guard IDs because objects change during map transition.
            read,syms=d['read'],d['syms']
            oid=read(syms['gPlayerAvatar']+5,1)
            if oid<16:
                obj=syms['gObjectEvents']+oid*0x24
                sid=read(obj+0x1b,1)
                if sid<64:
                    flags=read(syms['gSprites']+sid*0x44+0x3e,1)
                    samples.append(dict(frame=frame,map=current(),
                                        behavior=read(obj+0x1e,1),
                                        direction=(read(obj+0x18,1)>>4)&15,
                                        visible=bool(flags&1) and not bool(flags&4)))
        # First step lands on a directional threshold; the arrow points to the
        # next southward step, which triggers the actual warp.
        on_map('UnionCave_1F');assert pos()==(x,y),(index,'did not reach exit threshold',pos())
        capture(f'arrow-{index}-threshold')
        frames(16,128);frames(180);dest=d['ids'][event['dest_map']];on_map(dest)
        back=int(event['dest_warp_id']);d['warp'](back);on_map('UnionCave_1F')
        clip=out/f'arrow-{index}.mp4'
        if shutil.which('ffmpeg'):
            subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','30','-i',str(folder/'%03d.png'),'-pix_fmt','yuv420p',str(clip)],check=True)
        visible=[sample for sample in samples if sample['visible'] and sample['map']=='UnionCave_1F']
        for sample in visible:
            assert sample['behavior']==0x65 and sample['direction']==1,(index,sample,'unexpected warp arrow')
        record(kind='exit_roundtrip',source_index=index,threshold=[x,y],destination=dest,
               frames=folder.name,clip=clip.name if clip.exists() else None,
               visible_source_frames=[sample['frame'] for sample in visible],
               note='Zero visible frames means the animation needs manual review; it is not a pass for arrow visibility.')

    # Exercise one actual Survey Surf entry from reachable shore. The helper
    # opens the in-game field-action prompt with buttons; no move is granted.
    go('UnionCave_1F',2);n='UnionCave_1F';w,h=d['size'][n];raw=d['raw'][n];shore=None
    for y in range(1,h-1):
        if shore:break
        for x in range(1,w-1):
            if raw[y*w+x]>>12!=3 or not d['safe'](n,(x,y)) or d['path'](n,(x,y)) is None:continue
            for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if raw[yy*w+xx]>>12==1 and d['safe'](n,(xx,yy)):
                    shore=((x,y),(xx,yy));break
            if shore:break
    assert shore,'No reachable Surf shore';walk(shore[0]);capture('shore-before-surf');walk(shore[1])
    on_map(n);assert d['read']('gPlayerAvatar',1)&8;capture('surf-entry')
    record(kind='surf_entry',shore=shore[0],water=shore[1])

assert sha(args.save)==original and sha(rom)==args.rom_sha256,'Input fixture or ROM changed'
report['result']='PASS';save_report();print('PASS sampled cave visual controller capture; human visual review required')
