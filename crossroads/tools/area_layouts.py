"""Authoring helpers for the existing western footprint and its interiors."""
import json,struct
from pathlib import Path
R=Path(__file__).resolve().parents[2]


def decorate(name,data,w,h):
    t=list(struct.unpack('<'+str(w*h)+'H',data));art=json.loads((R/'crossroads/art/western/architecture.json').read_text())
    def rect(x,y,ww,hh,v):
        for yy in range(y,y+hh):t[yy*w+x:yy*w+x+ww]=[v]*ww
    def building(kind,x,y):
        a=art[kind]
        for yy in range(a['height']):
            for xx in range(a['width']):
                door=(xx,yy)==(a['door_x'],a['door_y'])
                t[(y+yy)*w+x+xx]=a['start']+yy*a['width']+xx+(0x3000 if door else 0x0400)
    if name=='OlivineCity':
        rect(37,28,5,5,0x3202);building('lighthouse',38,28)
    elif name=='EcruteakCity':
        for x,y,ww,hh in [(8,2,7,6),(34,2,7,6),(10,15,4,4),(20,15,5,4)]:rect(x,y,ww,hh,0x3001)
        building('burned',9,4);building('bell',36,2);building('house',10,16);building('theater',20,16)
    elif name=='JohtoRoute39':
        rect(5,5,3,3,0x3001);rect(3,15,4,3,0x3001)
        building('house',5,5);building('barn',3,15)
        rect(6,8,2,7,0x3202);rect(6,12,6,2,0x3202)
        rect(5,18,2,5,0x3202);rect(5,21,7,1,0x3202)
        t[18*w+3]=0x0403
    if name in ('JohtoRoute39','JohtoRoute38'):
        a=(R/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()
        grass=next(i for i,v in enumerate(struct.unpack('<'+str(len(a)//2)+'H',a)) if v&255==2)
        patches=[(16,16,5,7),(4,33,6,4)] if name.endswith('39') else [(18,17,8,5),(39,5,7,5),(53,18,8,5)]
        for x,y,ww,hh in patches:
            for yy in range(y,y+hh):
                for xx in range(x,x+ww):
                    v=t[yy*w+xx]
                    if v&0xc00==0 and v>>12==3 and (v&1023)!=0x202:t[yy*w+xx]=0x3000|grass
    # Regional expansion opens the existing south road; preserve the accepted sign.
    phase=R/'crossroads/johto/manifest.json'
    if name=='EcruteakCity' and phase.exists() and 'checkpoint' in json.loads(phase.read_text()):
        for yy in range(43,48):
            for xx in range(24,27):
                if (xx,yy)!=(24,44):t[yy*w+xx]=0x3202
    return struct.pack('<'+str(len(t))+'H',*t)


def rooms():
    specs=json.loads((R/'crossroads/art/western/rooms.json').read_text())
    for spec in specs:
        name=spec['name'];w,h=spec['width'],spec['height'];theme=spec['theme'];floor=spec['floor']
        m=json.loads((R/f'data/maps/{name}/map.json').read_text());t=[0x3223]*(w*h)
        for x in range(w):t[x]=0x0605;t[w+x]=0x060d;t[(h-1)*w+x]=0x0601
        for y in range(h):t[y*w]=t[y*w+w-1]=0x0601
        (R/f'data/layouts/{name}/border.bin').write_bytes(struct.pack('<4H',*([0x0601]*4)))
        def put(x,y,v):t[y*w+x]=v
        # Distinct pillar/aisle patterns, always leaving the perimeter walkable.
        if h>8:
            for y in range(4,h-3,3):
                gap=3+(floor+y)%max(1,w-6)
                for x in range(4,w-3):
                    if abs(x-gap)>1:put(x,y,0x0605)
        if theme=='gym':
            for y in range(4,h-1):put(6,y,0x3224)
            for x,y in [(5,3),(7,3),(6,2)]:put(x,y,0x0605)
        if theme=='theater':
            for y in range(2,4):
                for x in range(1,9):put(x,y,0x3224)
        if theme=='farmhouse':
            for x in (0,1,8,9):put(x,3,0x064c)
        if theme=='barn':
            for x in (0,4,8):put(x,3,0x0654)
        for e in m['warp_events']:
            x,y=e['x'],e['y']
            if y==7 and w==10:put(x,y,0x0208+(x==4))
            elif theme=='gym':put(x,y,0x0208)
            else:put(x,y,0x33fc if x>w//2 else 0x33fd)
        for o in m['object_events']:
            put(o['x'],o['y'],0x3224 if theme=='theater' else 0x3223)
        # Clear interactable wall targets on upper floors.
        (R/f'data/layouts/{name}/map.bin').write_bytes(struct.pack('<'+str(w*h)+'H',*t))

if __name__=='__main__':rooms();print('Landmark/arena/farm/theater rooms generated')
