#!/usr/bin/env python3
"""Normal-controller tests of source-derived QA09 seats/furniture, no warp writes.

Uses the shared copied-battery harness and its disclosed encounter suppression.
Every asserted move/collision below is executed by controller input; only reads
inspect game state. Selected movements produce native-resolution MP4 clips.
"""
import argparse,hashlib,json,runpy,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--output',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');p.add_argument('--resume',help='Optional private snapshot; shared harness requires exact ROM SHA256');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
sys.argv=['johto_network_smoke.py','--save',a.save,'--library',a.library,'--output',str(out),'--targets','']+(['--resume',a.resume]if a.resume else []);d=runpy.run_path(str(Path(__file__).with_name('johto_network_smoke.py')));go,walk,frames,current,pos,lib=[d[k]for k in ['go','walk','frames','current','pos','lib']];records=[]
def trial(label,n,point,button,expected=None,record=False):
 go(n);walk(point);assert current()==n and pos()==point
 lib.emu_image(str(out/(label+'-before.png')).encode());folder=out/label
 if record:folder.mkdir(exist_ok=True)
 for i in range(20):
  frames(4,button if i<4 else 0)
  if record:lib.emu_image(str(folder/f'{i:04}.png').encode())
 assert current()==n and pos()==(expected or point),(label,current(),pos(),expected or point)
 lib.emu_image(str(out/(label+'.png')).encode())
 if record:subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','15','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(out/(label+'.mp4'))],check=True)
 records.append(dict(label=label,map=n,approach=point,button=button,expected=expected or point,result='PASS'));print(label,'PASS',flush=True)
# The source front passage previously overlapped the rectangular seating fill.
trial('theater-front-aisle','EcruteakCity_DanceTheater',(8,9),128,(8,10),True)
trial('theater-front-aisle-east','EcruteakCity_DanceTheater',(8,10),16,(9,10),True)
facts=json.loads(Path('crossroads/hgss/canonical_events/ecruteak-interior-geometry.json').read_text())['MAP_ECRUTEAK_DANCE_THEATER'];benches=sorted({(int(p['tile_x']),int(p['tile_z']))for c in facts['chunks']for p in c['props']if p['model']==56})
for x,y in benches:
 # Source actors do not occupy the lower approaches; every seat is checked
 # individually rather than substituting a nearby working furniture cell.
 trial(f'bench-{x}-{y}-south','EcruteakCity_DanceTheater',(x,y+1),64,record=(x,y)==(12,10))
for n in ['EcruteakCity_Residence','EcruteakCity_DowsingHouse']:
 for x in [2,3,8,9]:trial(n+'-furniture-'+str(x),n,(x,4),64,record=x==8)
# The source riser blocks14/15,16; the second lower plant's root is enclosed
# by that riser, its neighbour and the wall. Test each exposed reachable face,
# never fabricate access through the canonical architecture.
for label,point,button in [('center-plant-15-4',(15,5),64),('center-plant-14-15-west',(13,15),16),('center-plant-15-14-north',(15,13),128)]:trial(label,'EcruteakCity_PokemonCenter_1F',point,button,record=label.endswith('north'))
(out/'results.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256(Path('pokeemerald.gba').read_bytes()).hexdigest(),setup=('Exact-ROM SHA-checked private snapshot from prior cold-Continue controller tour' if a.resume else 'Copied normal battery/cold Continue')+'; shared RAM-only encounter suppression/survey fixture. No player/map/warp/party writes in these movement trials.',records=records),indent=2)+'\n')
print('All13 source benches, front aisle, both house kitchens/bookcases and3Center plants: controller PASS')
