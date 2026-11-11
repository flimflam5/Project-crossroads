import hashlib,json,os,subprocess,sys,time
from pathlib import Path
sha='df69e014e706168c56180828487a9ab12709a9bccd3dff063fee5f7af5d4f2f4';save='build/area-delivery-sram/EcruteakCity_BellTower-save.state.sav';common=['--save',save,'--library','/tmp/johto-bridge.so'];names=','.join(r['map']for r in json.load(open('crossroads/hgss/ecruteak-qa09-building-checklist.json'))['maps']);commands=[('tour',[sys.executable,'crossroads/tools/johto_network_smoke.py']+common+['--output','build/qa09-ecruteak-tour-v11','--targets',names,'--all-edges']),('details',[sys.executable,'crossroads/tools/ecruteak_detail_smoke.py']+common+['--output','build/qa09-ecruteak-details-v11']),('furniture',[sys.executable,'crossroads/tools/ecruteak_furniture_smoke.py']+common+['--output','build/qa09-ecruteak-furniture-v11']),('gates',[sys.executable,'/tmp/qa09-ecruteak-gates-v11-runner.py']),('ground',[sys.executable,'crossroads/tools/ecruteak_qa07_repro.py']+common+['--output','build/qa09-ecruteak-ground-v11','--expect-fixed']),('pixels',[sys.executable,'crossroads/tools/validate_ecruteak_qa07.py','--recordings','build/qa09-ecruteak-ground-v11'])];results=[]
for name,cmd in commands:
 assert hashlib.sha256(Path('pokeemerald.gba').read_bytes()).hexdigest()==sha
 print('START',name,time.strftime('%H:%M:%S'),flush=True)
 with open('/tmp/qa09-ecruteak-'+name+'-v11.log','w')as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
 results.append(dict(name=name,command=cmd,exit_code=r.returncode,rom_sha256=sha));Path('/tmp/qa09-ecruteak-v11-suite-results.json').write_text(json.dumps(results,indent=2)+'\n');print('END',name,'exit',r.returncode,time.strftime('%H:%M:%S'),flush=True)
 if r.returncode:sys.exit(r.returncode)
assert hashlib.sha256(Path('pokeemerald.gba').read_bytes()).hexdigest()==sha
assert hashlib.sha256(Path(save).read_bytes()).hexdigest()=='b03ff1ef488fbd25de016e828483bc3001787b84e450a45eaa0ac12a11de30ab'
print('ALL FINAL V11 ECRUTEAK SUITES PASS; original copied battery unchanged',flush=True)
