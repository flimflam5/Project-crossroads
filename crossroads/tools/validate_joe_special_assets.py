#!/usr/bin/env python3
"""Player state identity, engine frame bounds, directional tables and stable IDs."""
from pathlib import Path
from PIL import Image
import json,re,subprocess
R=Path(__file__).resolve().parents[2];A=R/'graphics/object_events/pics/people/joe/corporate';palette=Image.open(A/'walking.png').getpalette()[:48]
physical={'field_move':5,'surfing':8,'underwater':4,'mach_bike':12,'acro_bike':36,'fishing':16,'watering':8};logical={'FieldMove':5,'Surfing':16,'Underwater':12,'MachBike':12,'AcroBike':36,'Fishing':16,'Watering':12}
for name,count in physical.items():
 im=Image.open(A/(name+'.png'));assert im.mode=='P' and im.size==(count*32,32) and im.info.get('transparency')==0 and max(im.tobytes())<16 and im.getpalette()[:48]==palette,name
 for i in range(count):assert im.crop((i*32,0,i*32+32,32)).convert('RGBA').getbbox(),(name,i)
for c in json.loads((A/'special-animation-contracts.json').read_text()):assert c['max_frame']<logical[c['state']] and c['mirroring'] is False
anims=(R/'src/data/object_events/joe_special_anims.h').read_text();assert 'hFlip' not in anims
constants=(R/'include/constants/event_objects.h').read_text();baseline=subprocess.check_output(['git','show','690485c997:include/constants/event_objects.h'],cwd=R,text=True)
# Preserve the entire actual enum, not just a count of apparent unused slots.
assert re.search(r'enum.*?NUM_OBJ_EVENT_GFX,.*?\};',constants,re.S)[0]==re.search(r'enum.*?NUM_OBJ_EVENT_GFX,.*?\};',baseline,re.S)[0]
for gender in ['MALE','FEMALE']:
 for state in ['MACH_BIKE','ACRO_BIKE','SURFING','UNDERWATER','FIELD_MOVE','FISHING','WATERING','VSSEEKER']:
  line=next(l for l in constants.splitlines() if l.startswith('#define PLAYER_AVATAR_GFX_'+gender+'_'+state+' '));assert ': OBJ_EVENT_GFX_JOE_' in line,(gender,state)
for n,v in re.findall(r'#define (OBJ_EVENT_GFX_JOE_\w+) (0x[0-9A-F]+)',constants):assert 0x3f04<=int(v,16)<=0x3f0b
movement=(R/'src/event_object_movement.c').read_text()
for state in ['MACH_BIKE','ACRO_BIKE','SURFING','UNDERWATER','FIELD_MOVE','FISHING','WATERING','DECORATING']:assert 'if (graphicsId == OBJ_EVENT_GFX_JOE_'+state+')' in movement
print('Joe action palette/frame bounds, authored east timing, both saved genders and unchanged graphics enum: PASS')
