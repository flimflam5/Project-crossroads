#!/usr/bin/env python3
"""Normal-controller tests of source-derived QA09 seats/furniture, no warp writes.

Uses the shared copied-battery harness and its disclosed encounter suppression.
Every asserted move/collision below is executed by controller input; only reads
inspect game state. Selected movements produce native-resolution MP4 clips.
"""
import argparse,hashlib,json,runpy,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--save',required=True);p.add_argument('--output',required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
sys.argv=['johto_network_smoke.py','--save',a.save,'--library',a.library,'--output',str(out),'--targets',''];d=runpy.run_path(str(Path(__file__).with_name('johto_network_smoke.py')));go,walk,frames,current,pos,lib=[d[k]for k in ['go','walk','frames','current','pos','lib']];records=[]
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
go('EcruteakCity_DanceTheater');walk((7,6));frames(30)
lib.emu_image(str(out/'theater-stage.png').encode())
subprocess.run([sys.executable,str(Path(__file__).with_name('validate_theater_stage.py')),'--screenshot',str(out/'theater-stage.png')],check=True)
walk((8,11));frames(30);lib.emu_image(str(out/'theater-audience.png').encode())
subprocess.run([sys.executable,str(Path(__file__).with_name('validate_theater_audience.py')),'--screenshot',str(out/'theater-audience.png')],check=True)
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
# Each restored B1F prop is checked through a genuinely reachable approach.
go('EcruteakCity_PokemonCenter_B1F');walk((8,6));frames(30)
lib.emu_image(str(out/'basement-three-booths.png').encode())
for x in [5,6,7,9,10,11]:trial('basement-lower-stool-'+str(x),'EcruteakCity_PokemonCenter_B1F',(x,11),128)
for label,point,button in [('plant-west',(3,12),16),('plant-east',(13,12),32),('stool-2-7',(2,6),128),('stool-3-7',(3,6),128),('stool-4-8',(5,8),32),('stool-4-9',(5,9),32),('table-west-upper',(1,8),16),('table-west-lower',(1,9),16),('table-south-left',(2,10),64),('table-south-right',(3,10),64),('terminal',(15,6),64)]:trial('basement-'+label,'EcruteakCity_PokemonCenter_B1F',point,button,record=label in('plant-west','table-west-upper','terminal'))
go('EcruteakCity_PokemonCenter_1F');walk((12,15));frames(30)
lib.emu_image(str(out/'center-floor-emblem.png').encode())
subprocess.run([sys.executable,str(Path(__file__).with_name('validate_center_basement.py')),'--reception-screenshot',str(out/'center-floor-emblem.png')],check=True)
# A bottom-layer contract alone is not the controller visibility check. Walk
# normally across every one of the20 emblem cells and retain native frames
# plus continuous footage so Joe's visibility can actually be inspected.
route=[(x,y)for y in range(14,18)for x in(range(6,11)if y%2==0 else range(10,5,-1))]
walk(route[0]);frames(30);folder=out/'floor-emblem-walking';folder.mkdir(exist_ok=True);frame_index=0
for point in route:
 if pos()!=point:
  dx,dy=point[0]-pos()[0],point[1]-pos()[1];assert abs(dx)+abs(dy)==1
  button={(1,0):16,(-1,0):32,(0,-1):64,(0,1):128}[dx,dy]
  for tick in range(40):
   frames(1,button if pos()!=point else 0)
   if tick%2==0:lib.emu_image(str(folder/f'{frame_index:04}.png').encode());frame_index+=1
   if tick>=24 and pos()==point:break
  assert current()=='EcruteakCity_PokemonCenter_1F'and pos()==point
 lib.emu_image(str(out/f'logo-Joe-{point[0]}-{point[1]}.png').encode())
subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','30','-i',str(folder/'%04d.png'),'-pix_fmt','yuv420p',str(out/'floor-emblem-walking.mp4')],check=True)
print('Normal controller walk across all20 emblem cells; native Joe frames/video captured for visual inspection: PASS',flush=True)
(out/'results.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256(Path('pokeemerald.gba').read_bytes()).hexdigest(),setup='Copied normal battery/cold Continue'+'; shared RAM-only encounter suppression/survey fixture. No player/map/warp/party writes in these movement trials.',records=records),indent=2)+'\n')
print('Source benches/aisle/houses/Center plants/restored basement furniture:',len(records),'controller cases PASS;20-cell emblem walk recorded')
