import sys,os,subprocess,json,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--rom-sha256',required=True);p.add_argument('--fixtures',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--library',default='/tmp/johto-bridge.so');a=p.parse_args();sha=a.rom_sha256;root=a.fixtures.resolve();out=a.output.resolve();assert root!=out;out.mkdir(parents=True,exist_ok=True)
cases=[
('UnionCave_1F-blocked','UnionCave_1F',5,24,True),('UnionCave_1F-isolated','UnionCave_1F',4,24,True),('UnionCave_1F-ladder','UnionCave_1F',5,24,True),
('UnionCave_2F-blocked','UnionCave_2F',10,41,True),('UnionCave_2F-isolated','UnionCave_2F',10,41,True),('UnionCave_2F-ladder','UnionCave_2F',10,41,True),
('UnionCave_3F-blocked','UnionCave_2F',10,41,True),('UnionCave_3F-water','UnionCave_2F',27,30,True),('UnionCave_3F-isolated','UnionCave_2F',27,30,True),('UnionCave_3F-ladder','UnionCave_2F',27,30,True),
('RuinsOfAlph-footprint','RuinsOfAlph',14,11,True),('RuinsOfAlph-control','RuinsOfAlph',17,16,False)]
results={}
for name,dst,x,y,relocate in cases:
 args=[sys.executable,str(Path(__file__).with_name('old_position.py')),'--save',str(root/(name+'.sav')),'--baseline',str(root/(name+'-baseline.json')),'--output',str(out/name),'--rom-sha256',sha,'--library',a.library,'--expect-map',dst,'--expect-x',str(x),'--expect-y',str(y),'--exit-map','JohtoRoute32' if dst=='RuinsOfAlph' else 'JohtoRoute33']
 if relocate:args+=['--expect-relocation']
 with (out/(name+'.log')).open('w') as f:r=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT)
 results[name]=r.returncode;print(name,'PASS' if not r.returncode else 'FAIL',flush=True)
(out/'summary.json').write_text(json.dumps(dict(rom_sha256=sha,returncodes=results),indent=2)+'\n')
sys.exit(bool(any(results.values())))
