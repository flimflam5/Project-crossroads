"""Bounded shared-primary buffers at the two existing Olivine connections."""
import struct,json
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def active():return (R/'crossroads/hgss/authoring/OlivineCity.json').exists()
def layout(name,l):
 if active() and name in ['JohtoRoute39','JohtoRoute40']:
  material=R/'crossroads/hgss/art/olivine/manifest.json'
  coast=name=='JohtoRoute40' and material.exists() and 'fence_h' in json.loads(material.read_text())['specs']
  l['primary_tileset']='gTileset_HgssOlivineCoastBuffer' if coast else 'gTileset_HgssEcruteakBuffer'
 return l
def patch(name,m):
 if not active():return m
 if name in ['JohtoRoute39','JohtoRoute40']:
  m['connections']=m['connections'] or []
  c=next((c for c in m['connections'] if c['map']=='MAP_OLIVINE_CITY'),None)
  if c is None:c=dict(map='MAP_OLIVINE_CITY',direction='down' if name=='JohtoRoute39' else 'right');m['connections'].append(c)
  c['offset']=-12 if name=='JohtoRoute39' else -10
 return m
def tiles(name,raw,w,h):
 if not active() or name not in ['JohtoRoute39','JohtoRoute40']:return raw
 t=list(struct.unpack('<'+str(w*h)+'H',raw))
 if name=='JohtoRoute39':
  for y in range(h-7,h):
   for x in range(9,14):t[y*w+x]=0x31ff
 if name=='JohtoRoute40':
  for y in range(24,29):
   for x in range(w-3,w):t[y*w+x]=0x3001
 for y in range(h):
  for x in range(w):
   if (name=='JohtoRoute39' and y>=h-7 or name=='JohtoRoute40' and x>=w-7) and t[y*w+x]&1023==0x202:t[y*w+x]=(t[y*w+x]&~1023)|0x1ff
 return struct.pack('<'+str(w*h)+'H',*t)
