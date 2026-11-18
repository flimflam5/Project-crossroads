#!/usr/bin/env python3
"""Static art, reserved ID and no-reward checks; runtime still required."""
from pathlib import Path
import json, re, subprocess
from PIL import Image
from build_route33_apricorns import COLORS, MASK, generate
R=Path(__file__).resolve().parents[2]
generate(True)
source=Image.open(R/'graphics/object_events/pics/misc/apricorn_tree.png')
a=Image.open(R/'graphics/object_events/pics/misc/route33_apricorn_pink.png')
b=Image.open(R/'graphics/object_events/pics/misc/route33_apricorn_black.png')
assert a.mode==b.mode=='P' and a.size==b.size==source.size==(16,16)
assert a.getpalette()==b.getpalette()
for i,c in COLORS.items():assert tuple(a.getpalette()[i*3:i*3+3])==c
changed={(6+x,5+y) for y,row in enumerate(MASK) for x,index in enumerate(row) if index is not None}
for y in range(16):
 for x in range(16):
  if (x,y) not in changed:assert a.getpixel((x,y))==b.getpixel((x,y))==source.getpixel((x,y))
  else:assert a.getpixel((x,y)) in (1,2,3) and b.getpixel((x,y)) in (5,6,7)
header=(R/'include/constants/event_objects.h').read_text()
for name,val in [('OBJ_EVENT_GFX_ROUTE33_APRICORN_PINK','0x3F0E'),('OBJ_EVENT_GFX_ROUTE33_APRICORN_BLACK','0x3F0F'),('OBJ_EVENT_PAL_TAG_ROUTE33_APRICORN','0x1172')]:
 assert re.search(r'^#define\s+'+name+r'\s+'+val+r'$',header,re.M)
 assert len(re.findall(r'^#define\s+\w+\s+'+val+r'\b',header,re.M))==1,(name,'ID or palette tag collision')
base=subprocess.check_output(['git','show','83b587fac6:include/constants/event_objects.h'],cwd=R,text=True)
for line in base.splitlines():
 if 'NUM_OBJ_EVENT_GFX' in line or 'OBJ_EVENT_GFX_VARS' in line or 'OBJ_EVENT_GFX_VAR_F' in line:
  assert line in header,('Changed existing graphics enum',line)
movement=(R/'src/event_object_movement.c').read_text()
for name in ('PINK','BLACK'):assert f'if (graphicsId == OBJ_EVENT_GFX_ROUTE33_APRICORN_{name})' in movement
assert '{gObjectEventPal_Route33Apricorn, OBJ_EVENT_PAL_TAG_ROUTE33_APRICORN}' in movement
m=json.loads((R/'data/maps/JohtoRoute33/map.json').read_text()); trees=[v for v in m['object_events'] if 'ROUTE33_APRICORN_' in v['graphics_id']]
assert [(t['x'],t['y'],t['graphics_id']) for t in trees]==[(23,26,'OBJ_EVENT_GFX_ROUTE33_APRICORN_PINK'),(24,26,'OBJ_EVENT_GFX_ROUTE33_APRICORN_BLACK')]
assert all(t['flag']=='0' and t['trainer_type']=='TRAINER_TYPE_NONE' and t['script']=='Johto_JohtoRoute33_ApricornTree' for t in trees)
scripts=(R/'crossroads/scripts/johto_network.inc').read_text(); fragment=scripts.split('Johto_JohtoRoute33_ApricornTree::',1)[1].split('Johto_JohtoRoute33_ApricornTree_Text:',1)[0]
assert 'msgbox' in fragment and 'end' in fragment and not any(s in fragment for s in ('giveitem','setflag','setvar','special','call '))
print('PASS pink/black original-fruit art, unshifted reserved IDs, shared palette and no-reward tree events; runtime VRAM and Save/Continue pending.')
