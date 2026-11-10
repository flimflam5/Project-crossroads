#!/usr/bin/env python3
"""Generate Joe's own animation tables: preserve engine timing, authored east art.

No player enum/dynamic graphics IDs change. Rival and remote-NPC assets remain.
"""
from pathlib import Path
import re,argparse,json
R=Path(__file__).resolve().parents[2];p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args();s=(R/'src/data/object_events/object_event_anims.h').read_text();out=['// Generated Joe special-action animations: no mirrored satchel.\n'];records=[]
plans=[('MachBike','Standard',{2:9,7:10,8:11}),('AcroBike','AcroBike',{n:27+i for i,n in enumerate([2,7,8,17,18,19,20,25,26])}),('Surfing','Surfing',{2:12,7:13,8:14,11:15}),('Underwater','Standard',{2:9,7:10,8:11}),('Fishing','Fishing',{i:12+i for i in range(4)}),('Watering','Standard',{2:9,7:10,8:11})]
for state,table,remap in plans:
 body=re.search(r'static const union AnimCmd \*const sAnimTable_'+table+r'\[\] = \{(.*?)\n\};',s,re.S)[1];functions=list(dict.fromkeys(re.findall(r'= (sAnim_\w+)',body)));names={fn:'sAnim_Joe'+state+'_'+fn.removeprefix('sAnim_') for fn in functions};indices=[]
 for fn in functions:
  code=re.search(r'static const union AnimCmd '+fn+r'\[\] =\s*\{(.*?)\n\};',s,re.S)[1]
  if fn.endswith('East'):
   def east(m):
    old=int(m[1]);assert old in remap,(state,fn,old);return 'ANIMCMD_FRAME('+str(remap[old])+','
   code=re.sub(r'ANIMCMD_FRAME\((\d+),',east,code)
  code=code.replace(', .hFlip = TRUE','');indices.extend(map(int,re.findall(r'ANIMCMD_FRAME\((\d+),',code)))
  out.append('static const union AnimCmd '+names[fn]+'[] = {'+code+'\n};\n')
 for fn,replacement in names.items():body=re.sub(r'\b'+fn+r'\b',replacement,body)
 out.append('static const union AnimCmd *const sAnimTable_Joe'+state+'[] = {'+body+'\n};\n');records.append(dict(state=state,animation_indices=len(functions),max_frame=max(indices),east_mapping=remap,mirroring=False))
def write(path,data):
 p=R/path
 if args.check:assert p.exists() and p.read_text()==data,('Regenerate Joe action animation tables',path)
 elif not p.exists() or p.read_text()!=data:p.write_text(data)
write('src/data/object_events/joe_special_anims.h','\n'.join(out));write('graphics/object_events/pics/people/joe/corporate/special-animation-contracts.json',json.dumps(records,indent=2)+'\n')
print('Joe action timing/east-frame tables:',len(plans),'states; no mirrored satchel: PASS')
